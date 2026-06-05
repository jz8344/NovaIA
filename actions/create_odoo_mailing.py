from loguru import logger
from ai.odoo_vendor_worker import OdooVendorWorker

async def handle_create_odoo_mailing(
    subject: str,
    create_list: str = "auto",
    list_name: str = "",
    session=None,
    **kwargs
) -> dict:
    from django_project.state import db
    user_id = getattr(session, "user_id", None) if session else None
    if not user_id:
        user_id = 1

    if not session or "last_contact_search" not in session.metadata or not session.metadata["last_contact_search"].get("partners"):
        return {"output": "Por favor, busca contactos primero antes de crear una lista de correo."}

    partners = session.metadata["last_contact_search"]["partners"]

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

        use_list = False
        if create_list == "yes":
            use_list = True
        elif create_list == "no":
            use_list = False
        else:
            use_list = len(partners) > 50

        res = await worker.create_mailing_draft(
            subject=subject,
            partners=partners,
            use_list=use_list,
            list_name=list_name or None
        )

        if not res.get("success"):
            return {"output": f"Error al crear el mailing en Odoo: {res.get('message')}"}

        mailing_id = res.get("mailing_id")
        mode = res.get("mode")
        mode_str = "Lista estática" if mode == "list" else "Dominio dinámico"

        msg = f"¡Excelente! He creado el borrador de correo masivo con el asunto '{subject}' en Odoo.\n"
        msg += f"Folio del mailing: MASS/{mailing_id}\n"
        msg += f"Destinatarios asociados: {len(partners)} (Modo: {mode_str}).\n"
        msg += "El cuerpo del mensaje ha quedado vacío para que puedas redactarlo directamente en tu panel de Odoo y enviarlo cuando esté listo."

        return {"output": msg}

    except Exception as e:
        logger.error(f"Error en handle_create_odoo_mailing: {e}")
        return {"output": f"Ocurrió un error al crear el correo masivo: {str(e)}"}
