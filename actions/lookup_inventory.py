from loguru import logger
from database.manager import DatabaseManager
from core.security import SecurityGuard
from ai.router import IntelligentRouter

_db: DatabaseManager | None = None

MAX_RESULTS = 2


def set_db(db: DatabaseManager):
    global _db
    _db = db


async def handle_lookup_inventory(product_query: str, session=None, **kwargs) -> dict:
    if SecurityGuard.is_injection(product_query):
        return {"output": SecurityGuard.get_safe_response()}

    route_res = IntelligentRouter.route(product_query)
    if route_res:
        return {"output": route_res["response"]}

    if not _db:
        return {"output": "Base de datos no disponible."}

    q_norm = product_query.lower() if product_query else ""
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]:
        q_norm = q_norm.replace(a, b)

    is_additional = any(
        kw in q_norm for kw in [
            "adicional", "restante", "faltante", "los otros", "los demas",
            "los dema", "los 3", "los tres", "mas", "siguientes", "continuar",
            "listame todos", "todos los demas", "todos los restantes", "dame los demas", "dame todos",
            "todo", "todos", "todas", "toda", "completo", "completa", "entero", "todo lo que tengas", "dame todo"
        ]
    )

    ORDINALES = [
        "El primero es", "El segundo es", "El tercero es", "El cuarto es",
        "El quinto es", "El sexto es", "El séptimo es", "El octavo es",
        "El noveno es", "El décimo es"
    ]

    if is_additional and session and "last_inventory_results" in session.metadata:
        cached = session.metadata["last_inventory_results"]
        results = cached.get("results", [])
        original_query = cached.get("query", "")
        start_idx = cached.get("current_index", 2)
        
        remaining_results = results[start_idx:]
        if not remaining_results:
            return {"output": "Ya te he mencionado todas las opciones que encontré para esa búsqueda. ¿Hay algún otro producto o categoría que te interese?"}
            
        page_results = remaining_results[:10]
        next_index = start_idx + len(page_results)
        cached["current_index"] = next_index
        
        items = []
        for idx, r in enumerate(page_results):
            pos = start_idx + idx
            ord_str = ORDINALES[pos] if pos < len(ORDINALES) else f"El número {pos + 1} es"
            stock_str = f"con {r['stock']} en stock" if r["stock"] > 0 else "agotado"
            items.append(f"{ord_str} {r['product_name']} a ${r['price']:,.0f} MXN, {stock_str}")
        
        text = f"Aquí tienes las siguientes opciones para '{original_query}': " + ". ".join(items) + "."
        
        has_even_more = len(results) > next_index
        if has_even_more:
            left = len(results) - next_index
            text += f" Todavía quedan {left} opciones más. ¿Deseas que sigamos con las siguientes, o prefieres buscar algo específico?"
        else:
            text += " Esos son todos los resultados que tenemos disponibles por ahora."
            
        logger.info(f"Paginación para sesión {session.session_id}: enviando {len(page_results)} productos.")
        return {"output": text}

    results = await _db.search_inventory(product_query)

    if not results:
        return {"output": "No encontré nada con eso, ¿quieres que busque algo similar o hay algún otro producto que te interese?"}

    total = len(results)
    if total <= 5:
        items = []
        for idx, r in enumerate(results):
            ord_str = ORDINALES[idx] if idx < len(ORDINALES) else f"El número {idx + 1} es"
            stock_str = f"con {r['stock']} en stock" if r["stock"] > 0 else "agotado"
            items.append(f"{ord_str} {r['product_name']} a ${r['price']:,.0f} MXN, {stock_str}")
        
        text = f"Encontré {total} resultado(s) para '{product_query}': " + ". ".join(items) + "."
        logger.info(f"Inventario '{product_query}': {total} resultados devueltos de forma completa (1-5)")
        return {"output": text}

    if session:
        session.metadata["last_inventory_results"] = {
            "query": product_query,
            "results": results
        }

    if 6 <= total <= 20:
        if session:
            session.metadata["last_inventory_results"]["current_index"] = 3

        top = results[:3]
        items = []
        for idx, r in enumerate(top):
            ord_str = ORDINALES[idx]
            stock_str = f"con {r['stock']} en stock" if r["stock"] > 0 else "agotado"
            items.append(f"{ord_str} {r['product_name']} a ${r['price']:,.0f} MXN, {stock_str}")
        
        remaining_results = results[3:]
        remaining_names = [r["product_name"] for r in remaining_results]
        preview_names = ", ".join(remaining_names[:3])
        if len(remaining_names) > 3:
            preview_names += ", entre otros"

        text = f"Encontré {total} opciones para '{product_query}'. "
        text += ". ".join(items) + "."
        text += f" También tenemos en existencia: {preview_names}. Si deseas escuchar los detalles de las demás opciones o saber de alguna en específico, puedes pedírmelo directamente. ¿Te gustaría escuchar más opciones?"
        logger.info(f"Inventario '{product_query}': {total} resultados (6-20), enviando top 3 + preview")
        return {"output": text}

    if total > 20:
        if session:
            session.metadata["last_inventory_results"]["current_index"] = 0

        brands = sorted(list(set(r["brand"] for r in results if r.get("brand"))))
        if brands:
            preview_brands = ", ".join(brands[:3])
        else:
            preview_brands = "Dell, HP, Lenovo o Apple"
            
        text = (
            f"Encontré un catálogo muy completo con {total} opciones de '{product_query}'. "
            f"Para ayudarte a elegir el ideal para ti de la manera más sencilla, ¿tienes alguna marca en mente, como {preview_brands}, "
            f"o prefieres decirme tu presupuesto aproximado para mostrarte las mejores opciones?"
        )
        logger.info(f"Inventario '{product_query}': {total} resultados (20+), activando filtro conversacional de vendedor")
        return {"output": text}

    return {"output": "Error al procesar la consulta."}
