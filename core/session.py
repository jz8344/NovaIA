import asyncio
import uuid
import time
from dataclasses import dataclass, field
from typing import Optional
from loguru import logger
from core.events import event_bus

TOKEN_LIMIT_PER_SESSION = 50_000


@dataclass
class CallSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    call_id: str = ""
    channel: str = ""
    caller_id: str = ""
    source: str = "unknown"
    started_at: float = field(default_factory=time.time)
    active: bool = True
    gemini_session: Optional[object] = None
    audio_queue_in: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=100))
    audio_queue_out: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=100))
    metadata: dict = field(default_factory=dict)
    tokens_input: int = 0
    tokens_output: int = 0

    @property
    def tokens_total(self) -> int:
        return self.tokens_input + self.tokens_output

    @property
    def token_limit_reached(self) -> bool:
        return self.tokens_total >= TOKEN_LIMIT_PER_SESSION

    @property
    def duration(self) -> float:
        return time.time() - self.started_at


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, CallSession] = {}
        self._lock = asyncio.Lock()

    async def create_session(self, source: str = "unknown", **kwargs) -> CallSession:
        session = CallSession(source=source, **kwargs)
        async with self._lock:
            self._sessions[session.session_id] = session
        logger.info(f"Sesión creada: {session.session_id} (fuente: {source})")
        await event_bus.emit("session_created", session=session)
        return session

    async def get_session(self, session_id: str) -> Optional[CallSession]:
        return self._sessions.get(session_id)

    async def end_session(self, session_id: str, reason: str = "normal"):
        async with self._lock:
            session = self._sessions.pop(session_id, None)
        if session:
            session.active = False
            logger.info(f"Sesión terminada: {session_id} ({reason}) - Duración: {session.duration:.1f}s")
            await event_bus.emit("session_ended", session=session, reason=reason)
        return session

    @property
    def active_sessions(self) -> dict[str, CallSession]:
        return {k: v for k, v in self._sessions.items() if v.active}

    @property
    def count(self) -> int:
        return len(self.active_sessions)
