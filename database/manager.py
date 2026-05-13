import aiosqlite
import os
from loguru import logger
from config.settings import get_settings
from database.models import SCHEMA_SQL


class DatabaseManager:
    def __init__(self):
        self.db_path = get_settings().db_path
        self._db: aiosqlite.Connection | None = None

    async def connect(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        await self._db.executescript(SCHEMA_SQL)
        await self._db.commit()
        logger.info(f"Base de datos conectada: {self.db_path}")

    async def disconnect(self):
        if self._db:
            await self._db.close()
            logger.info("Base de datos desconectada")

    async def search_extension(self, query: str) -> list[dict]:
        sql = """
            SELECT name, extension, department, email, available
            FROM extensions
            WHERE LOWER(name) LIKE LOWER(?) OR LOWER(department) LIKE LOWER(?)
        """
        pattern = f"%{query}%"
        async with self._db.execute(sql, (pattern, pattern)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def search_inventory(self, query: str) -> list[dict]:
        sql = """
            SELECT product_name, description, price, stock, category, brand, color, weight
            FROM inventory
            WHERE LOWER(product_name) LIKE LOWER(?) OR LOWER(category) LIKE LOWER(?) OR LOWER(brand) LIKE LOWER(?)
        """
        pattern = f"%{query}%"
        async with self._db.execute(sql, (pattern, pattern, pattern)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def log_call(self, session_id: str, caller_id: str, source: str,
                       duration: float, actions: str, transcript: str):
        sql = """
            INSERT INTO call_logs (session_id, caller_id, source, duration, actions_taken, transcript)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        await self._db.execute(sql, (session_id, caller_id, source, duration, actions, transcript))
        await self._db.commit()

    async def get_all_extensions(self) -> list[dict]:
        async with self._db.execute("SELECT * FROM extensions ORDER BY name") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def add_extension(self, name: str, extension: str, department: str = "", email: str = ""):
        sql = "INSERT INTO extensions (name, extension, department, email) VALUES (?, ?, ?, ?)"
        await self._db.execute(sql, (name, extension, department, email))
        await self._db.commit()

    async def delete_extension(self, ext_id: int):
        await self._db.execute("DELETE FROM extensions WHERE id = ?", (ext_id,))
        await self._db.commit()

    async def get_all_inventory(self) -> list[dict]:
        async with self._db.execute("SELECT * FROM inventory ORDER BY product_name") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def add_inventory_item(self, product_name: str, description: str,
                                 price: float, stock: int, category: str,
                                 brand: str = "", color: str = "", weight: str = ""):
        sql = """INSERT INTO inventory (product_name, description, price, stock, category, brand, color, weight)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        await self._db.execute(sql, (product_name, description, price, stock, category, brand, color, weight))
        await self._db.commit()

    async def delete_inventory_item(self, item_id: int):
        await self._db.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        await self._db.commit()

    async def get_call_logs(self, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM call_logs ORDER BY created_at DESC LIMIT ?"
        async with self._db.execute(sql, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
