import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from actions.create_odoo_order import handle_create_odoo_order
from database.manager import DatabaseManager
from config.settings import get_settings

async def test_creation():
    print("=" * 60)
    print("  TEST DE CREACIÓN DE PRESUPUESTO EN ODOO — JSON-2 API")
    print("=" * 60)

    # 1. Cargar base de datos local para inicializar el singleton en state.py
    # dado que handle_create_odoo_order importa "db" de django_project.state,
    # debemos inicializar esa base de datos antes o pasarle un mock, pero
    # para ser realistas, podemos inicializarla.
    from django_project import state
    await state.db.connect()

    # Productos simulados
    products_to_order = [
        {"product_name": "Cable prearmado de 18mts CAT6", "quantity": 3},
        {"product_name": "Acces Point V12NR", "quantity": 1},
        {"product_name": "IPC-P413-X20K", "quantity": 2},
        {"product_name": "Producto Inexistente XYZ", "quantity": 1} # Debería reportarse como no enlazado
    ]

    customer = "Cliente Llamada Nova 999"

    print(f"\n> Cliente: {customer}")
    print(f"> Productos a ordenar:")
    for p in products_to_order:
        print(f"  - {p['product_name']} | Cantidad: {p['quantity']}")

    products_names_str = ", ".join(p["product_name"] for p in products_to_order)
    quantities_str = ", ".join(str(p["quantity"]) for p in products_to_order)

    print("\nGenerando requisición de venta en Odoo...")
    res = await handle_create_odoo_order(
        products_names=products_names_str,
        quantities=quantities_str,
        customer_name=customer
    )

    print("\n" + "=" * 60)
    print("  RESULTADO DE LA ACCIÓN:")
    print("=" * 60)
    print(res.get("output"))
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_creation())
