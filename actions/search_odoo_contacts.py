from loguru import logger
from ai.odoo_vendor_worker import OdooVendorWorker

async def handle_search_odoo_contacts(
    product_query: str = "",
    days_back: int = 30,
    state_filter: str = "",
    city_filter: str = "",
    category_filter: str = "",
    min_amount: float = 0.0,
    source: str = "sales",
    session=None,
    **kwargs
) -> dict:
    from django_project.state import db
    user_id = getattr(session, "user_id", None) if session else None
    if not user_id:
        user_id = 1

    try:
        config = await db.get_agent_data_source(user_id)
        if not config or config.get("source_type") != "odoo":
            return {"output": "El data source activo no es Odoo."}

        odoo_url = config.get("odoo_url", "")
        odoo_api_key = config.get("odoo_api_key", "")
        if not odoo_url or not odoo_api_key:
            return {"output": "Faltan credenciales para conectar con Odoo."}

        worker = OdooVendorWorker(
            base_url=odoo_url,
            api_key=odoo_api_key,
            db_name=config.get("odoo_db", ""),
            odoo_user=config.get("odoo_user", "")
        )

        res = await worker.search_customers_by_product(
            product_query=product_query or None,
            days_back=days_back,
            state_filter=state_filter or None,
            city_filter=city_filter or None,
            category_filter=category_filter or None,
            min_amount=min_amount or None,
            source=source
        )

        if not res.get("success"):
            return {"output": f"Error al buscar contactos en Odoo: {res.get('message')}"}

        partners = res.get("partners", [])
        if session:
            if "last_contact_search" not in session.metadata:
                session.metadata["last_contact_search"] = {}
            session.metadata["last_contact_search"] = {
                "partners": partners,
                "filters": {
                    "product_query": product_query,
                    "days_back": days_back,
                    "state_filter": state_filter,
                    "city_filter": city_filter,
                    "category_filter": category_filter,
                    "min_amount": min_amount,
                    "source": source
                }
            }

        if not partners:
            return {"output": "No se encontró ningún contacto con esos criterios en Odoo."}

        summary = f"Encontré {len(partners)} contactos en Odoo.\n"
        for p in partners[:10]:
            state_str = ""
            state_id = p.get("state_id")
            if isinstance(state_id, (list, tuple)) and len(state_id) >= 2:
                state_str = f", {state_id[1]}"
            elif isinstance(state_id, str):
                state_str = f", {state_id}"

            city = p.get("city") or ""
            loc = f" ({city}{state_str})" if city or state_str else ""
            summary += f"- {p.get('name')} | Email: {p.get('email')}{loc}\n"

        if len(partners) > 10:
            summary += f"... y {len(partners) - 10} contactos más."

        return {"output": summary}

    except Exception as e:
        logger.error(f"Error en handle_search_odoo_contacts: {e}")
        return {"output": f"Ocurrió un error al buscar los contactos: {str(e)}"}
