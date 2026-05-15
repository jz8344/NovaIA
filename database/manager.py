import aiosqlite
import os
import unicodedata
from loguru import logger
from config.settings import get_settings
from database.models import SCHEMA_SQL


class DatabaseManager:
    def __init__(self):
        self.db_path = get_settings().db_path
        self._db: aiosqlite.Connection | None = None

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalizar texto: remover acentos y convertir a minúsculas"""
        nfd = unicodedata.normalize('NFD', text)
        return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn').lower()

    @staticmethod
    def _extract_numbers(text: str) -> list[str]:
        """Extraer números en palabras y dígitos de un texto"""
        text_lower = text.lower()
        
        # Mapeo de palabras a números
        word_to_num = {
            'cero': '0', 'uno': '1', 'dos': '2', 'tres': '3', 'cuatro': '4',
            'cinco': '5', 'seis': '6', 'siete': '7', 'ocho': '8', 'nueve': '9',
            'diez': '10', 'once': '11', 'doce': '12', 'trece': '13', 'catorce': '14',
            'quince': '15', 'dieciséis': '16', 'diecisiete': '17', 'dieciocho': '18',
            'diecinueve': '19', 'veinte': '20', 'treinta': '30', 'cuarenta': '40',
            'cincuenta': '50', 'sesenta': '60', 'setenta': '70', 'ochenta': '80',
            'noventa': '90', 'cien': '100', 'ciento': '100'
        }
        
        numbers = []
        
        # Extraer dígitos
        import re
        digits = re.findall(r'\d+', text)
        numbers.extend(digits)
        
        # Convertir palabras a números
        for word, num in word_to_num.items():
            if word in text_lower:
                numbers.append(num)
        
        return numbers

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
        normalized_query = self._normalize_text(query)
        extracted_numbers = self._extract_numbers(query)
        
        logger.info(f"[DEBUG] Query: '{query}' (normalizado: '{normalized_query}') | Números: {extracted_numbers}")
        
        async with self._db.execute("SELECT * FROM extensions") as cursor:
            all_rows = await cursor.fetchall()
        
        results = []
        for row in all_rows:
            normalized_name = self._normalize_text(row["name"])
            normalized_dept = self._normalize_text(row["department"])
            
            # Búsqueda por texto normalizado
            if normalized_query in normalized_name or normalized_query in normalized_dept:
                results.append(row)
            # Búsqueda por números extraídos
            elif any(num in row["extension"] for num in extracted_numbers):
                results.append(row)
        
        logger.info(f"[DEBUG] Filas encontradas: {len(results)}")
        
        return [{
            "name": row["name"],
            "extension": row["extension"],
            "department": row["department"],
            "email": row["email"],
            "available": row["available"]
        } for row in results]

    async def search_inventory(self, query: str) -> list[dict]:
        normalized_query = self._normalize_text(query)
        pattern = f"%{normalized_query}%"
        logger.info(f"[DEBUG] Inventory Query: '{query}' (normalizado: '{normalized_query}') | Pattern: '{pattern}'")
        
        async with self._db.execute("SELECT * FROM inventory") as cursor:
            all_rows = await cursor.fetchall()
        
        results = []
        for row in all_rows:
            normalized_name = self._normalize_text(row["product_name"])
            normalized_cat = self._normalize_text(row["category"])
            normalized_brand = self._normalize_text(row["brand"])
            if normalized_query in normalized_name or normalized_query in normalized_cat or normalized_query in normalized_brand:
                results.append({
                    "product_name": row["product_name"],
                    "description": row["description"],
                    "price": row["price"],
                    "stock": row["stock"],
                    "category": row["category"],
                    "brand": row["brand"],
                    "color": row["color"],
                    "weight": row["weight"]
                })
        
        return results

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

    # --- Prompts ---
    async def save_prompt(self, name: str, system_prompt: str, description: str = "") -> dict:
        sql = """
            INSERT INTO prompts (name, system_prompt, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(name) DO UPDATE SET 
                system_prompt = excluded.system_prompt,
                description = excluded.description,
                updated_at = CURRENT_TIMESTAMP
        """
        await self._db.execute(sql, (name, system_prompt, description))
        await self._db.commit()
        logger.info(f"Prompt guardado: {name}")
        return {"success": True, "message": f"Prompt '{name}' guardado correctamente"}

    async def get_prompt(self, name: str) -> dict | None:
        sql = "SELECT * FROM prompts WHERE name = ?"
        async with self._db.execute(sql, (name,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_all_prompts(self) -> list[dict]:
        async with self._db.execute("SELECT id, name, description, updated_at FROM prompts ORDER BY updated_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def delete_prompt(self, prompt_id: int):
        await self._db.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        await self._db.commit()
        logger.info(f"Prompt eliminado: ID {prompt_id}")
