from loguru import logger
from core.security import SecurityGuard
from ai.router import IntelligentRouter
from ai.inventory_worker import InventoryWorker

_worker: InventoryWorker | None = None


def set_worker(worker: InventoryWorker):
    global _worker
    _worker = worker


async def handle_lookup_inventory(product_query: str, session=None, **kwargs) -> dict:
    if SecurityGuard.is_injection(product_query):
        return {"output": SecurityGuard.get_safe_response()}

    route_res = IntelligentRouter.route(product_query)
    if route_res:
        return {"output": route_res["response"]}

    if not _worker:
        return {"output": "Sistema de inventario no disponible."}

    result = await _worker.process(product_query, session)
    logger.info(f"Inventario '{product_query}': Worker retornó {len(result)} chars")
    return {"output": result}
