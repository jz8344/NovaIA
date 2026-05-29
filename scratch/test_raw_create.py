import os
import asyncio
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

async def main():
    base_url = os.getenv("ODOO_BASE_URL").rstrip("/")
    api_key = os.getenv("ODOO_API_KEY")
    
    url = f"{base_url}/json/2/sale.order/create"
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ID del cliente Michael Williams (ID 12)
    partner_id = 12
    # ID del producto Laptop Gamer ASUS (ID 24), precio 18163.0
    product_id = 24
    from ai.odoo_worker import OdooInventoryWorker
    worker = OdooInventoryWorker(base_url, api_key)
    logger.info("Buscando tarifa de precios activa en Odoo...")
    pricelist_id = 1
    try:
        result_price = await worker._search_read("product.pricelist", [], ["id", "name"], limit=1)
        if result_price:
            pricelist_id = result_price[0]["id"]
            logger.info(f"Tarifa de precios encontrada en Odoo Online: '{result_price[0]['name']}' con ID {pricelist_id}")
        else:
            logger.warning("No se encontraron tarifas de precios en Odoo. Usando ID 1 por defecto.")
    except Exception as e:
        logger.error(f"Error consultando tarifas: {e}")

    payload = {
        "vals_list": [
            {
                "partner_id": partner_id,
                "order_line": [
                    (0, 0, {
                        "product_id": product_id,
                        "product_uom_qty": 1,
                        "price_unit": 18163.0
                    })
                ],
                "note": "Prueba de creación directa con vals_list autocompletado."
            }
        ]
    }

    logger.info(f"Enviando petición de creación a: {url}")
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            logger.info(f"Código de respuesta HTTP: {resp.status_code}")
            data = resp.json()
            logger.info(f"Respuesta JSON completa de Odoo: {data}")
    except Exception as e:
        logger.error(f"Error en la petición: {e}")

if __name__ == "__main__":
    asyncio.run(main())
