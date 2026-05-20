import asyncio
import struct
import uuid
from loguru import logger
from core.session import SessionManager, CallSession
from core.audio_processor import AudioProcessor
from core.vad import VoiceActivityDetector
from core.events import event_bus
from config.settings import get_settings

# AudioSocket Protocol:
# Header: 1 byte type + 2 bytes length (big-endian) + N bytes payload
# Types: 0x01 = UUID, 0x10 = Audio (slin16), 0x00 = Hangup/Error
MSG_TYPE_UUID = 0x01
MSG_TYPE_AUDIO = 0x10
MSG_TYPE_HANGUP = 0x00
MSG_TYPE_ERROR = 0xFF


class AudioSocketServer:
    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager
        self._server: asyncio.AbstractServer | None = None
        settings = get_settings()
        self.host = settings.audiosocket_host
        self.port = settings.audiosocket_port

    async def start(self):
        self._server = await asyncio.start_server(
            self._handle_connection, self.host, self.port
        )
        logger.info(f"AudioSocket Server escuchando en {self.host}:{self.port}")

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            logger.info("AudioSocket Server detenido")

    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername")
        logger.info(f"AudioSocket: nueva conexión desde {peer}")
        session: CallSession | None = None

        try:
            session = await self._session_manager.create_session(
                source="asterisk",
                call_id=str(uuid.uuid4())
            )

            vad = VoiceActivityDetector()

            send_task = asyncio.create_task(
                self._send_audio_to_asterisk(session, writer)
            )

            await event_bus.emit("asterisk_call_started", session=session)

            while session.active:
                header = await reader.readexactly(3)
                msg_type = header[0]
                msg_len = struct.unpack(">H", header[1:3])[0]

                if msg_len > 0:
                    payload = await reader.readexactly(msg_len)
                else:
                    payload = b""

                if msg_type == MSG_TYPE_UUID:
                    call_uuid = payload.decode("utf-8", errors="ignore").strip()
                    session.call_id = call_uuid
                    logger.info(f"AudioSocket UUID recibido: {call_uuid}")

                elif msg_type == MSG_TYPE_AUDIO:
                    pcm_16khz = AudioProcessor.asterisk_to_gemini(payload)
                    if vad.is_speech(pcm_16khz):
                        try:
                            session.audio_queue_in.put_nowait(pcm_16khz)
                        except asyncio.QueueFull:
                            try:
                                session.audio_queue_in.get_nowait()
                            except asyncio.QueueEmpty:
                                pass
                            session.audio_queue_in.put_nowait(pcm_16khz)
                            logger.warning(f"[{session.session_id}] Cola de audio llena en AudioSocket: descartando frame antiguo.")

                elif msg_type == MSG_TYPE_HANGUP:
                    logger.info(f"AudioSocket: colgado recibido para {session.session_id}")
                    break

                elif msg_type == MSG_TYPE_ERROR:
                    logger.error(f"AudioSocket: error recibido para {session.session_id}")
                    break

        except asyncio.IncompleteReadError:
            logger.info(f"AudioSocket: conexión cerrada por Asterisk")
        except Exception as e:
            logger.error(f"AudioSocket error: {e}")
        finally:
            if session:
                session.active = False
                await session.audio_queue_in.put(None)
                await self._session_manager.end_session(session.session_id, "asterisk_disconnect")
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            logger.info(f"AudioSocket: conexión cerrada para {peer}")

    async def _send_audio_to_asterisk(self, session: CallSession, writer: asyncio.StreamWriter):
        try:
            while session.active:
                try:
                    audio_data = await asyncio.wait_for(
                        session.audio_queue_out.get(), timeout=0.5
                    )
                    if audio_data is None:
                        break

                    pcm_8khz = AudioProcessor.gemini_to_asterisk(audio_data)

                    chunk_size = 320  # 20ms de audio a 8kHz 16-bit mono
                    for i in range(0, len(pcm_8khz), chunk_size):
                        chunk = pcm_8khz[i:i + chunk_size]
                        if len(chunk) == 0:
                            break
                        header = struct.pack(">BH", MSG_TYPE_AUDIO, len(chunk))
                        writer.write(header + chunk)
                    
                    # Un solo drain tras enviar todos los chunks de la ráfaga actual
                    await writer.drain()

                except asyncio.TimeoutError:
                    continue
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if session.active:
                logger.error(f"Error enviando audio a Asterisk: {e}")
