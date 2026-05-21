import json
import asyncio
from loguru import logger
from channels.generic.websocket import AsyncWebsocketConsumer

from django_project import state
from core.audio_processor import AudioProcessor
from core.vad import VoiceActivityDetector

class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar la conexión WebSocket
        await self.accept()
        self.session = await state.session_manager.create_session(source="web")
        logger.info(f"WebSocket de voz conectado (Django): {self.session.session_id}")

        self.vad = VoiceActivityDetector()

        # Iniciar las tareas en segundo plano
        self.gemini_task = asyncio.create_task(
            state.gemini_client.start_session(self.session)
        )
        self.send_task = asyncio.create_task(
            self._send_audio_to_browser()
        )

    async def disconnect(self, close_code):
        logger.info(f"WebSocket desconectado (Django): {self.session.session_id}")
        self.session.active = False
        await self.session.audio_queue_in.put(None)

        # Cancelar tareas de fondo
        if hasattr(self, 'gemini_task') and not self.gemini_task.done():
            self.gemini_task.cancel()
            try:
                await self.gemini_task
            except (asyncio.CancelledError, Exception):
                pass

        if hasattr(self, 'send_task') and not self.send_task.done():
            self.send_task.cancel()
            try:
                await self.send_task
            except (asyncio.CancelledError, Exception):
                pass

        # Registrar llamada en base de datos si la sesión finalizó
        ended = await state.session_manager.end_session(self.session.session_id, "websocket_disconnect")
        if ended:
            try:
                await state.db.log_call(
                    session_id=ended.session_id,
                    caller_id=ended.caller_id or "web",
                    source=ended.source,
                    duration=round(ended.duration, 2),
                    actions=str(ended.metadata.get("actions", [])),
                    transcript="",
                    tokens_input=ended.tokens_input,
                    tokens_output=ended.tokens_output,
                )
            except Exception as _log_err:
                logger.warning(f"No se pudo registrar log de llamada en Django: {_log_err}")
        logger.info(f"Sesión WebSocket limpia (Django): {self.session.session_id}")

    async def receive(self, text_data=None, bytes_data=None):
        if not self.session.active:
            return

        if bytes_data is not None:
            # Procesar datos binarios de audio
            pcm_16khz = AudioProcessor.browser_to_gemini(bytes_data)
            if self.vad.is_speech(pcm_16khz):
                try:
                    self.session.audio_queue_in.put_nowait(pcm_16khz)
                except asyncio.QueueFull:
                    try:
                        self.session.audio_queue_in.get_nowait()
                    except asyncio.QueueEmpty:
                        pass
                    self.session.audio_queue_in.put_nowait(pcm_16khz)
                    logger.warning(f"[{self.session.session_id}] Cola de audio llena: se descarta frame antiguo.")

        elif text_data is not None:
            # Procesar mensajes de texto (comandos)
            try:
                msg = json.loads(text_data)
                if msg.get("type") == "end":
                    await self.close()
            except Exception as e:
                logger.error(f"Error procesando mensaje de texto en ws (Django): {e}")

    async def _send_audio_to_browser(self):
        try:
            while self.session.active:
                try:
                    audio_data = await asyncio.wait_for(
                        self.session.audio_queue_out.get(), timeout=0.5
                    )
                    if audio_data is None:
                        break

                    pcm_16khz = AudioProcessor.gemini_to_browser(audio_data)
                    await self.send(bytes_data=pcm_16khz)

                except asyncio.TimeoutError:
                    continue
        except Exception as e:
            if self.session.active:
                logger.debug(f"Send audio to browser cerrado (Django): {e}")
