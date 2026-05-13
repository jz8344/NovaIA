from loguru import logger
from core.session import CallSession
from database.manager import DatabaseManager

_db: DatabaseManager | None = None
_ami_client = None


def set_dependencies(db: DatabaseManager, ami_client=None):
    global _db, _ami_client
    _db = db
    _ami_client = ami_client


async def handle_transfer_call(target_name: str, session: CallSession = None, **kwargs) -> dict:
    if not _db:
        return {"error": "Base de datos no disponible"}

    results = await _db.search_extension(target_name)

    if not results:
        return {
            "success": False,
            "message": f"No se encontró la extensión de '{target_name}'",
            "action": "inform_user"
        }

    target = results[0]
    extension = target["extension"]
    name = target["name"]

    if not target["available"]:
        return {
            "success": False,
            "message": f"{name} no está disponible en este momento (extensión {extension})",
            "action": "offer_voicemail"
        }

    if _ami_client and session and session.channel:
        try:
            await _ami_client.transfer(session.channel, extension)
            logger.info(f"Llamada transferida a {name} (ext. {extension})")
            return {
                "success": True,
                "message": f"Transfiriendo la llamada a {name} en la extensión {extension}",
                "transferred_to": name,
                "extension": extension,
                "action": "transferred"
            }
        except Exception as e:
            logger.error(f"Error transfiriendo llamada: {e}")
            return {
                "success": False,
                "message": f"Hubo un error al transferir la llamada: {str(e)}",
                "action": "retry"
            }

    logger.info(f"[SIMULACIÓN] Transferencia a {name} (ext. {extension})")
    return {
        "success": True,
        "message": f"Transfiriendo la llamada a {name} en la extensión {extension}",
        "transferred_to": name,
        "extension": extension,
        "action": "transferred",
        "simulated": True
    }
