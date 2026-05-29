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

    logger.info(f"Conectando a Odoo en: {base_url}")
    worker = OdooInventoryWorker(base_url, api_key, db_name, odoo_user)
    
    # Forzar que no use Gemini para validar la potencia del motor local de stemming
    worker.ai_client = None

    pruebas = ["computadoras", "impresoras", "perifericos"]
    for query in pruebas:
        logger.info(f"\n--- PROBANDO BÚSQUEDA DINÁMICA DE: '{query}' ---")
        
        # Probar la extracción de raíces
        roots = await worker._extract_intelligent_terms(query)
        logger.info(f"Raíces léxicas dinámicas generadas: {roots}")
        
        # Ejecutar la búsqueda en Odoo Online
        result = await worker.process(query)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
