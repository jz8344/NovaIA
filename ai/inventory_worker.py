from loguru import logger
from database.manager import DatabaseManager
from collections import defaultdict


class InventoryWorker:
    def __init__(self, db: DatabaseManager):
        self._db = db

    async def process(self, query: str, session=None) -> str:
        q_norm = query.lower() if query else ""
        for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]:
            q_norm = q_norm.replace(a, b)

        is_additional = any(
            kw in q_norm for kw in [
                "adicional", "restante", "faltante", "los otros", "los demas",
                "los dema", "mas", "siguientes", "continuar",
                "listame todos", "todos los demas", "todos los restantes",
                "dame los demas", "dame todos", "todo", "todos", "todas",
                "toda", "completo", "completa", "entero", "todo lo que tengas",
                "dame todo"
            ]
        )

        if is_additional and session and "last_inventory_results" in session.metadata:
            return self._paginate_cached(session)

        results = await self._db.search_inventory(query)

        if not results:
            return f"No se encontraron productos para '{query}'."

        total = len(results)

        if session:
            session.metadata["last_inventory_results"] = {
                "query": query,
                "results": results,
                "current_index": min(total, 30),
            }

        if total <= 30:
            catalog = self._build_catalog(results, query)
        else:
            catalog = self._build_catalog(results[:30], query)
            all_categories = sorted(set(r.get("category", "General") or "General" for r in results))
            all_brands = sorted(set(r.get("brand", "") for r in results if r.get("brand")))
            catalog += f"\n\nMostrando 30 de {total} productos."
            catalog += f"\nCategorías disponibles: {', '.join(all_categories)}."
            if all_brands:
                catalog += f"\nMarcas disponibles: {', '.join(all_brands)}."

        logger.info(f"Worker: '{query}' → {total} productos, catálogo de {len(catalog)} chars")
        return catalog

    def _paginate_cached(self, session) -> str:
        cached = session.metadata["last_inventory_results"]
        results = cached.get("results", [])
        original_query = cached.get("query", "")
        start_idx = cached.get("current_index", 0)

        remaining = results[start_idx:]
        if not remaining:
            return "Ya se han mostrado todos los productos de esa búsqueda."

        page = remaining[:15]
        next_index = start_idx + len(page)
        cached["current_index"] = next_index

        catalog = self._build_catalog(page, original_query, continuation=True)

        has_more = len(results) > next_index
        if has_more:
            left = len(results) - next_index
            catalog += f"\n\nQuedan {left} productos adicionales."
        else:
            catalog += "\n\nEstos son todos los productos restantes."

        logger.info(f"Worker paginación: enviando {len(page)} productos (idx {start_idx}-{next_index})")
        return catalog

    def _build_catalog(self, products: list[dict], query: str, continuation: bool = False) -> str:
        grouped = defaultdict(lambda: defaultdict(list))
        for p in products:
            cat = p.get("category", "General") or "General"
            brand = p.get("brand", "Otros") or "Otros"
            grouped[cat][brand].append(p)

        lines = []
        if not continuation:
            lines.append("=== INVENTARIO CONSULTADO ===")
            lines.append("")

        for category in sorted(grouped.keys()):
            lines.append(category.upper())
            brands = grouped[category]
            for brand in sorted(brands.keys()):
                lines.append(f"  {brand}:")
                for p in brands[brand]:
                    name = p.get("product_name", "Producto")
                    price = p.get("price", 0)
                    stock = p.get("stock", 0)
                    desc = p.get("description", "")

                    price_str = f"${price:,.0f} MXN"
                    stock_str = f"stock: {stock}" if stock > 0 else "agotado"

                    line = f"    - {name} — {price_str} ({stock_str})"
                    if desc:
                        line += f" | {desc}"
                    lines.append(line)
            lines.append("")

        all_categories = list(grouped.keys())
        all_brands = sorted(set(
            brand for brands in grouped.values() for brand in brands.keys() if brand != "Otros"
        ))

        lines.append(f"Total: {len(products)} productos | Categorías: {len(all_categories)} | Marcas: {', '.join(all_brands) if all_brands else 'varias'}")

        return "\n".join(lines)
