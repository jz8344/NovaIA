import os
import asyncio
from loguru import logger
from dotenv import load_dotenv
from ai.odoo_worker import OdooInventoryWorker

load_dotenv()

async def main():
    base_url = os.getenv("ODOO_BASE_URL")
    api_key = os.getenv("ODOO_API_KEY")
    db_name = os.getenv("ODOO_DB", "")
    odoo_user = os.getenv("ODOO_USER", "")

    if not base_url or not api_key:
        logger.error("Faltan variables ODOO_BASE_URL o ODOO_API_KEY en el archivo .env")
        return

    logger.info(f"Conectando a Odoo en: {base_url} para consultar cotizaciones...")
    worker = OdooInventoryWorker(base_url, api_key, db_name, odoo_user)

    fields = ["name", "partner_id", "amount_total", "state", "date_order"]
    
    # Consultar las últimas 10 órdenes/cotizaciones de venta (sale.order)
    quotes = await worker._search_read("sale.order", [], fields, limit=10, order="id desc")

    if not quotes:
        logger.warning("No se encontraron cotizaciones en Odoo o falló la consulta.")
        return

    logger.info("\n=== COTIZACIONES EN ODOO REAL ===")
    for q in quotes:
        name = q.get("name")
        q_id = q.get("id")
        partner = q.get("partner_id")
        partner_name = partner[1] if isinstance(partner, (list, tuple)) and len(partner) >= 2 else str(partner)
        total = q.get("amount_total", 0.0)
        state = q.get("state", "unknown")
        date = q.get("date_order", "")

        state_es = {
            "draft": "Borrador (Presupuesto)",
            "sent": "Presupuesto Enviado",
            "sale": "Pedido de Venta",
            "done": "Realizado",
            "cancel": "Cancelado"
        }.get(state, state)

        print(f"- ID: {q_id} | Folio: {name} | Cliente: {partner_name} | Total: ${total:,.2f} | Estado: {state_es} | Fecha: {date}")

if __name__ == "__main__":
    asyncio.run(main())
