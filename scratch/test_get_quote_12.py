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

    logger.info(f"Buscando cotización con ID 12 en Odoo...")
    worker = OdooInventoryWorker(base_url, api_key, db_name, odoo_user)

    fields = ["name", "partner_id", "amount_total", "state", "date_order", "company_id"]
    
    # Consultar la orden de venta con ID 12
    quote_12 = await worker._search_read("sale.order", [["id", "=", 12]], fields, limit=1)
    logger.info(f"Resultado búsqueda ID 12: {quote_12}")

    # Consultar todas las órdenes de venta sin filtros para ver los IDs que realmente existen
    all_quotes = await worker._search_read("sale.order", [], ["id", "name", "partner_id"], limit=100)
    logger.info(f"Todas las cotizaciones encontradas: {all_quotes}")

if __name__ == "__main__":
    asyncio.run(main())
