from loguru import logger
from core.security import SecurityGuard


async def _get_pms_worker_for_session(session=None):
    from django_project.state import db
    user_id = getattr(session, "user_id", None) if session else None
    if not user_id:
        user_id = 1

    try:
        config = await db.get_agent_data_source(user_id)
        if not config or config.get("source_type") != "pms":
            return None

        pms_url = config.get("pms_url", "")
        pms_username = config.get("pms_username", "")
        pms_password = config.get("pms_password", "")

        if not pms_url or not pms_username or not pms_password:
            logger.warning(f"[user_id={user_id}] PMS configurado pero faltan credenciales")
            return None

        from ai.pms_worker import get_pms_worker
        return get_pms_worker(pms_url, pms_username, pms_password, user_id)

    except Exception as e:
        logger.error(f"Error resolviendo PmsWorker para user_id={user_id}: {e}")
        return None


async def handle_pms_check_rooms(room_type: str = "", session=None, **kwargs) -> dict:
    if room_type and SecurityGuard.is_injection(room_type):
        return {"output": SecurityGuard.get_safe_response()}

    worker = await _get_pms_worker_for_session(session)
    if not worker:
        return {"output": "El sistema de gestión hotelera (PMS) no está configurado."}

    result = await worker.get_available_rooms(room_type or None)
    return {"output": result}


async def handle_pms_room_status(room_number: str, session=None, **kwargs) -> dict:
    if SecurityGuard.is_injection(room_number):
        return {"output": SecurityGuard.get_safe_response()}

    worker = await _get_pms_worker_for_session(session)
    if not worker:
        return {"output": "El sistema de gestión hotelera (PMS) no está configurado."}

    result = await worker.check_room_status(room_number)
    return {"output": result}


async def handle_pms_get_reservations(guest_name: str = "", session=None, **kwargs) -> dict:
    if guest_name and SecurityGuard.is_injection(guest_name):
        return {"output": SecurityGuard.get_safe_response()}

    worker = await _get_pms_worker_for_session(session)
    if not worker:
        return {"output": "El sistema de gestión hotelera (PMS) no está configurado."}

    result = await worker.get_reservations(guest_name or None)
    return {"output": result}


async def handle_pms_create_reservation(
    guest_name: str,
    room_number: str,
    check_in: str,
    check_out: str,
    adults: str = "1",
    session=None,
    **kwargs,
) -> dict:
    for field in [guest_name, room_number, check_in, check_out]:
        if SecurityGuard.is_injection(field):
            return {"output": SecurityGuard.get_safe_response()}

    worker = await _get_pms_worker_for_session(session)
    if not worker:
        return {"output": "El sistema de gestión hotelera (PMS) no está configurado."}

    try:
        adults_int = int(adults)
    except (ValueError, TypeError):
        adults_int = 1

    result = await worker.create_reservation(guest_name, room_number, check_in, check_out, adults_int)
    return {"output": result}


async def handle_pms_query(query: str, session=None, **kwargs) -> dict:
    if SecurityGuard.is_injection(query):
        return {"output": SecurityGuard.get_safe_response()}

    worker = await _get_pms_worker_for_session(session)
    if not worker:
        return {"output": "El sistema de gestión hotelera (PMS) no está configurado para este agente."}

    result = await worker.process(query, session)
    return {"output": result}
