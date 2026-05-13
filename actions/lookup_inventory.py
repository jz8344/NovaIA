from loguru import logger
from database.manager import DatabaseManager

_db: DatabaseManager | None = None


def set_db(db: DatabaseManager):
    global _db
    _db = db


async def handle_lookup_inventory(product_query: str, **kwargs) -> dict:
    if not _db:
        return {"error": "Base de datos no disponible"}

    results = await _db.search_inventory(product_query)

    if not results:
        return {
            "found": False,
            "message": f"No se encontró el producto '{product_query}' en el inventario",
            "suggestions": "Intenta con otra descripción o categoría"
        }

    formatted = []
    for r in results:
        availability = "en stock" if r["stock"] > 0 else "agotado"
        formatted.append({
            "product": r["product_name"],
            "description": r["description"],
            "price": f"${r['price']:,.2f} MXN",
            "stock": r["stock"],
            "availability": availability,
            "category": r["category"]
        })

    logger.info(f"Búsqueda de inventario '{product_query}': {len(formatted)} resultados")
    return {
        "found": True,
        "count": len(formatted),
        "products": formatted
    }
