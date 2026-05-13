from loguru import logger
from core.session import CallSession
from core.events import event_bus


async def handle_end_call(reason: str = "user_request", session: CallSession = None, **kwargs) -> dict:
    if session:
        session.active = False
        logger.info(f"Llamada finalizada: {session.session_id} - Razón: {reason}")
        await event_bus.emit("call_ended", session_id=session.session_id, reason=reason)

    return {
        "success": True,
        "message": f"La llamada ha sido finalizada. Razón: {reason}",
        "action": "call_ended"
    }
