import sys
import os
import csv
import asyncio

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.manager import DatabaseManager

async def main():
    db = DatabaseManager()
    await db.connect()
    
    csv_path = os.path.join(os.path.dirname(__file__), 'inventario_telecom.csv')
    if not os.path.exists(csv_path):
        print(f"No se encontró el archivo CSV en: {csv_path}")
        return
        
    print(f"Iniciando importación a la base de datos activa: {db.db_type.upper()}")
    if db.db_type == "sqlite":
        print(f"Archivo SQLite: {db.sqlite_path}")
    else:
        print(f"Servidor PostgreSQL: {db.postgres_url.split('@')[-1] if db.postgres_url else 'En la nube'}")
        
    # Limpiar tabla de inventario antes de importar para evitar duplicados
    print("Limpiando la tabla 'inventory' existente...")
    await db.execute("DELETE FROM inventory")
    print("Tabla limpiada con éxito.")
        
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            await db.add_inventory_item(
                product_name=row['product_name'],
                description=row['description'],
                price=float(row['price']),
                stock=int(row['stock']),
                category=row['category'],
                brand=row['brand'],
                color=row['color'],
                weight=row['weight']
            )
            count += 1
            print(f"[{count}] Importado: {row['product_name']}")
            
    await db.disconnect()
    print("\n¡Importación finalizada con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
