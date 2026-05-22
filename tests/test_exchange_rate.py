import sys
import os
import asyncio
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.exchange_updater import ExchangeRateUpdater, EXCHANGE_RATES_FILE
from ai.inventory_worker import InventoryWorker

class DummyDB:
    async def search_inventory(self, query):
        return []

async def test_exchange_rate_updater():
    # Eliminar archivo si existe para prueba limpia
    if os.path.exists(EXCHANGE_RATES_FILE):
        try:
            os.remove(EXCHANGE_RATES_FILE)
        except Exception:
            pass

    updater = ExchangeRateUpdater()
    # Ejecutar la actualización una vez de forma directa
    await updater.update_rates()

    assert os.path.exists(EXCHANGE_RATES_FILE) is True, "El archivo exchange_rates.json debería existir tras update_rates()"
    
    with open(EXCHANGE_RATES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "USD" in data
    assert "MXN" in data
    assert "ARS" in data
    assert data["USD"] == 1.0

def test_inventory_worker_conversion():
    # Asegurar que el archivo de tipos de cambio existe con valores de prueba controlados
    rates_test = {
        "USD": 1.0,
        "MXN": 17.37,
        "ARS": 900.0,
        "BOB": 6.91,
        "GBP": 0.79,
        "RUB": 90.0,
        "CNY": 7.24,
        "KRW": 1360.0
    }
    
    os.makedirs(os.path.dirname(EXCHANGE_RATES_FILE), exist_ok=True)
    with open(EXCHANGE_RATES_FILE, "w", encoding="utf-8") as f:
        json.dump(rates_test, f)

    db = DummyDB()
    worker = InventoryWorker(db)

    products = [
        {
            "product_name": "Test Router",
            "price": 1737.0,  # 1737 MXN = 100 USD con tasa 17.37
            "stock": 5,
            "category": "Networking",
            "brand": "Cisco",
            "description": "Powerful router"
        }
    ]

    catalog = worker._build_catalog(products, "router")
    
    assert "~$100.00 USD" in catalog, f"El catálogo debería contener el precio convertido en USD: {catalog}"
    assert "~£79.00 GBP" in catalog, f"El catálogo debería contener el precio convertido en GBP: {catalog}"
    assert "~90,000 ARS" in catalog, f"El catálogo debería contener el precio convertido en ARS: {catalog}"

if __name__ == "__main__":
    # Ejecutar tests sincrónicamente si se corre directo
    print("=== Ejecutando pruebas de tipo de cambio ===")
    try:
        test_inventory_worker_conversion()
        print("OK: test_inventory_worker_conversion paso exitosamente.")
        
        # Correr la prueba asíncrona
        asyncio.run(test_exchange_rate_updater())
        print("OK: test_exchange_rate_updater paso exitosamente.")
        
        print("\nSUCCESS: Todas las pruebas de divisas pasaron con éxito!")
    except AssertionError as e:
        print(f"\nASSERTION ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR INESPERADO: {e}")
        sys.exit(1)
