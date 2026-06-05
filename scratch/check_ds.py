import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.manager import DatabaseManager

async def main():
    db = DatabaseManager()
    await db.connect()
    try:
        rows = await db.fetch_all("SELECT * FROM agent_data_source")
        print("REGISTROS DATA SOURCE (SINGULAR):", rows)
        
        users = await db.fetch_all("SELECT * FROM admin_users")
        print("USUARIOS REGISTRADOS:", users)
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
