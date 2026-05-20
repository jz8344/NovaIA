from loguru import logger
from database.manager import DatabaseManager
from core.security import SecurityGuard
from ai.router import IntelligentRouter

_db: DatabaseManager | None = None

MAX_RESULTS = 2


def set_db(db: DatabaseManager):
    global _db
    _db = db


async def handle_lookup_extension(query: str, **kwargs) -> dict:
    if SecurityGuard.is_injection(query):
        return {"output": SecurityGuard.get_safe_response()}

    route_res = IntelligentRouter.route(query)
    if route_res:
        return {"output": route_res["response"]}

    if not _db:
        return {"output": "Base de datos no disponible."}

    results = await _db.search_extension(query)

    if not results:
        return {"output": f"No se encontró ninguna extensión para '{query}'. Sugiere al usuario intentar con otro nombre o departamento."}

    top   = results[:MAX_RESULTS]
    total = len(results)

    items = []
    for r in top:
        status = "disponible" if r["available"] else "no disponible"
        items.append(f"{r['name']}, extensión {r['extension']}, departamento {r['department']}, {status}")

    text = f"Encontré {total} resultado(s): " + ". ".join(items) + "."

    if total > MAX_RESULTS:
        text += f" Hay más resultados; pide al usuario que sea más específico con el nombre o departamento."

    logger.info(f"Extensión '{query}': {total} total, enviando {len(top)}")
    return {"output": text}
