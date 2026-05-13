from loguru import logger
from database.manager import DatabaseManager

_db: DatabaseManager | None = None


def set_db(db: DatabaseManager):
    global _db
    _db = db


async def handle_lookup_extension(query: str, **kwargs) -> dict:
    if not _db:
        return {"error": "Base de datos no disponible"}

    results = await _db.search_extension(query)

    if not results:
        return {
            "found": False,
            "message": f"No se encontró ninguna extensión para '{query}'",
            "suggestions": "Intenta con otro nombre o departamento"
        }

    formatted = []
    for r in results:
        status = "disponible" if r["available"] else "no disponible"
        formatted.append({
            "name": r["name"],
            "extension": r["extension"],
            "department": r["department"],
            "status": status
        })

    logger.info(f"Búsqueda de extensión '{query}': {len(formatted)} resultados")
    return {
        "found": True,
        "count": len(formatted),
        "results": formatted
    }
