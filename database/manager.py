import aiosqlite
import os
import re
import json
import unicodedata
from loguru import logger
from config.settings import get_settings
from database.models import SCHEMA_SQL, SCHEMA_POSTGRES_SQL


def _normalize(text: str) -> str:
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn').lower()


def _tokenize_query(query: str) -> list[str]:
    norm = _normalize(query)
    terms = {norm}
    words = [w for w in norm.split() if len(w) >= 2]
    terms.update(words)
    for w in words:
        if len(w) >= 5:
            terms.add(w[:4])
    return list(terms)


def _sanitize_fts_query(query: str) -> str:
    cleaned = re.sub(r'[^\w\s]', ' ', query)
    forbidden = {"or", "and", "not"}
    tokens = [t for t in cleaned.split() if t.lower() not in forbidden]
    return ' OR '.join(f'"{t}"*' for t in tokens if t)


class DatabaseManager:
    def __init__(self):
        self.config_path = "./data/db_config.json"
        self.db_type = "postgres"
        self.sqlite_path = get_settings().db_path
        self.postgres_url = get_settings().database_url
        self._db = None
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.db_type = cfg.get("db_type", "postgres")
                    self.sqlite_path = cfg.get("sqlite_path", "./data/nova.db")
                    self.postgres_url = cfg.get("postgres_url", get_settings().database_url)
            else:
                settings = get_settings()
                if settings.database_url:
                    self.db_type = "postgres"
                    self.postgres_url = settings.database_url
                else:
                    self.db_type = "sqlite"
                    self.sqlite_path = settings.db_path
        except Exception as e:
            logger.error(f"Error cargando db_config.json: {e}")

    @staticmethod
    def _normalize_text(text: str) -> str:
        return _normalize(text)

    def _convert_query(self, sql: str) -> str:
        if self.db_type == "postgres":
            count = 1
            def repl(match):
                nonlocal count
                res = f"${count}"
                count += 1
                return res
            return re.sub(r'\?', repl, sql)
        return sql

    async def connect(self):
        self.load_config()
        if self.db_type == "postgres":
            import asyncpg
            logger.info("Conectando a PostgreSQL (Railway)...")
            try:
                self._db = await asyncpg.connect(self.postgres_url)
                await self._db.execute(SCHEMA_POSTGRES_SQL)
                # Migración dinámica para PostgreSQL si ya existía la tabla
                try:
                    await self._db.execute("ALTER TABLE admin_users ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'user'")
                except Exception as _mig_err:
                    logger.debug(f"Migración PostgreSQL role: {_mig_err}")
                logger.info("Base de datos PostgreSQL conectada")
                return
            except Exception as e:
                logger.error(f"Falla al conectar a PostgreSQL (Railway): {e}")
                logger.warning("Activando FALLBACK automático a SQLite local para evitar crash en el arranque del servidor...")
                self.db_type = "sqlite"
                self.sqlite_path = "./data/nova.db"

        os.makedirs(os.path.dirname(self.sqlite_path), exist_ok=True)
        self._db = await aiosqlite.connect(self.sqlite_path)
        self._db.row_factory = aiosqlite.Row
        await self._db.executescript(SCHEMA_SQL)
        await self._db.commit()
        # Migración dinámica para SQLite si ya existía la tabla
        try:
            await self._db.execute("ALTER TABLE admin_users ADD COLUMN role TEXT DEFAULT 'user'")
            await self._db.commit()
            logger.info("Migración: Columna 'role' añadida exitosamente a 'admin_users' en SQLite")
        except Exception:
            pass
        await self._rebuild_fts_index()
        logger.info(f"Base de datos SQLite conectada: {self.sqlite_path}")

    async def reconnect(self, db_type: str, sqlite_path: str, postgres_url: str):
        await self.disconnect()
        config_data = {
            "db_type": db_type,
            "sqlite_path": sqlite_path,
            "postgres_url": postgres_url
        }
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        self.db_type = db_type
        self.sqlite_path = sqlite_path
        self.postgres_url = postgres_url
        await self.connect()

    async def test_connection(self, db_type: str, sqlite_path: str, postgres_url: str):
        if db_type == "postgres":
            import asyncpg
            conn = await asyncpg.connect(postgres_url)
            await conn.close()
        else:
            conn = await aiosqlite.connect(sqlite_path)
            await conn.close()

    async def _rebuild_fts_index(self):
        if self.db_type == "postgres":
            return
        try:
            await self._db.execute("INSERT INTO inventory_fts(inventory_fts) VALUES('rebuild')")
            await self._db.execute("INSERT INTO extensions_fts(extensions_fts) VALUES('rebuild')")
            await self._db.commit()
            logger.info("Índices FTS5 reconstruidos")
        except Exception as e:
            logger.debug(f"FTS rebuild (normal en BD nueva): {e}")

    async def disconnect(self):
        if self._db:
            await self._db.close()
            self._db = None
            logger.info("Base de datos desconectada")

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        sql = self._convert_query(sql)
        if self.db_type == "postgres":
            rows = await self._db.fetch(sql, *params)
            return [dict(r) for r in rows]
        else:
            async with self._db.execute(sql, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def fetch_one(self, sql: str, params: tuple = ()) -> dict:
        sql = self._convert_query(sql)
        if self.db_type == "postgres":
            row = await self._db.fetchrow(sql, *params)
            return dict(row) if row else {}
        else:
            async with self._db.execute(sql, params) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else {}

    async def execute(self, sql: str, params: tuple = ()):
        sql = self._convert_query(sql)
        if self.db_type == "postgres":
            await self._db.execute(sql, *params)
        else:
            await self._db.execute(sql, params)
            await self._db.commit()

    # ── BÚSQUEDA EXTENSIONES ───────────────────────────────────────────────────

    async def search_extension(self, query: str) -> list[dict]:
        norm_query = _normalize(query)
        logger.info(f"[SEARCH] extension='{query}'")
        if self.db_type == "postgres":
            results = await self._token_search_extensions(norm_query)
        else:
            results = await self._fts_search_extensions(norm_query)
            if not results:
                results = await self._token_search_extensions(norm_query)
        logger.info(f"[SEARCH] extension results: {len(results)}")
        return results

    async def _fts_search_extensions(self, query: str) -> list[dict]:
        try:
            fts_query = _sanitize_fts_query(query)
            if not fts_query:
                return []
            sql = """
                SELECT e.* FROM extensions e
                JOIN extensions_fts f ON e.id = f.rowid
                WHERE extensions_fts MATCH ?
                ORDER BY rank LIMIT 20
            """
            rows = await self.fetch_all(sql, (fts_query,))
            return [{
                "name": r["name"], "extension": r["extension"],
                "department": r["department"], "email": r["email"],
                "available": r["available"]
            } for r in rows]
        except Exception as e:
            logger.debug(f"FTS5 extension error (usando fallback): {e}")
            return []

    async def _token_search_extensions(self, norm_query: str) -> list[dict]:
        terms = _tokenize_query(norm_query)
        all_rows = await self.fetch_all("SELECT * FROM extensions")
        seen, results = set(), []
        for row in all_rows:
            n = _normalize(row["name"])
            d = _normalize(row["department"])
            e = _normalize(row["extension"])
            for t in terms:
                if t in n or t in d or t in e:
                    if row["id"] not in seen:
                        seen.add(row["id"])
                        results.append({
                            "name": row["name"], "extension": row["extension"],
                            "department": row["department"], "email": row["email"],
                            "available": row["available"]
                        })
                    break
        return results

    # ── BÚSQUEDA INVENTARIO ────────────────────────────────────────────────────

    async def search_inventory(self, query: str) -> list[dict]:
        norm_query = _normalize(query)
        logger.info(f"[SEARCH] inventory='{query}'")
        if self.db_type == "postgres":
            results = await self._token_search_inventory(norm_query)
        else:
            results = await self._fts_search_inventory(norm_query)
            if not results:
                results = await self._token_search_inventory(norm_query)
        logger.info(f"[SEARCH] inventory results: {len(results)}")
        return results

    async def _fts_search_inventory(self, query: str) -> list[dict]:
        try:
            fts_query = _sanitize_fts_query(query)
            if not fts_query:
                return []
            sql = """
                SELECT i.* FROM inventory i
                JOIN inventory_fts f ON i.id = f.rowid
                WHERE inventory_fts MATCH ?
                ORDER BY rank LIMIT 20
            """
            rows = await self.fetch_all(sql, (fts_query,))
            return [{
                "product_name": r["product_name"], "description": r["description"],
                "price": r["price"], "stock": r["stock"],
                "category": r["category"], "brand": r["brand"],
                "color": r["color"], "weight": r["weight"]
            } for r in rows]
        except Exception as e:
            logger.debug(f"FTS5 inventory error (usando fallback): {e}")
            return []

    async def _token_search_inventory(self, norm_query: str) -> list[dict]:
        terms = _tokenize_query(norm_query)
        all_rows = await self.fetch_all("SELECT * FROM inventory")
        seen, results = set(), []
        for row in all_rows:
            n = _normalize(row["product_name"])
            c = _normalize(row["category"])
            d = _normalize(row["description"])
            b = _normalize(row["brand"])
            for t in terms:
                if t in n or t in c or t in d or t in b:
                    if row["id"] not in seen:
                        seen.add(row["id"])
                        results.append({
                            "product_name": row["product_name"], "description": row["description"],
                            "price": row["price"], "stock": row["stock"],
                            "category": row["category"], "brand": row["brand"],
                            "color": row["color"], "weight": row["weight"]
                        })
                    break
        return results

    # ── LOGS ───────────────────────────────────────────────────────────────────

    async def log_call(self, session_id: str, caller_id: str, source: str,
                       duration: float, actions: str, transcript: str,
                       tokens_input: int = 0, tokens_output: int = 0):
        from datetime import datetime
        created_at = datetime.now()
        tokens_total = tokens_input + tokens_output
        cost_usd = (tokens_input * 0.000001) + (tokens_output * 0.000002)
        sql = """
            INSERT INTO call_logs
                (session_id, caller_id, source, duration, actions_taken, transcript,
                 tokens_input, tokens_output, tokens_total, cost_usd, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        await self.execute(sql, (
            session_id, caller_id, source, duration, actions, transcript,
            tokens_input, tokens_output, tokens_total, cost_usd, created_at
        ))
        await self._upsert_daily_usage(tokens_input, tokens_output, tokens_total, cost_usd)

    async def _upsert_daily_usage(self, tin: int, tout: int, ttotal: int, cost: float):
        from datetime import date, datetime
        today = date.today().isoformat()
        now = datetime.now()
        sql = """
            INSERT INTO token_usage_daily (date, total_calls, tokens_input, tokens_output, tokens_total, cost_usd, updated_at)
            VALUES (?, 1, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                total_calls   = token_usage_daily.total_calls + 1,
                tokens_input  = token_usage_daily.tokens_input + excluded.tokens_input,
                tokens_output = token_usage_daily.tokens_output + excluded.tokens_output,
                tokens_total  = token_usage_daily.tokens_total + excluded.tokens_total,
                cost_usd      = token_usage_daily.cost_usd + excluded.cost_usd,
                updated_at    = excluded.updated_at
        """
        await self.execute(sql, (today, tin, tout, ttotal, cost, now))

    # ── EXTENSIONES CRUD ───────────────────────────────────────────────────────

    async def get_all_extensions(self) -> list[dict]:
        return await self.fetch_all("SELECT * FROM extensions ORDER BY name")

    async def add_extension(self, name: str, extension: str, department: str = "", email: str = ""):
        sql = "INSERT INTO extensions (name, extension, department, email) VALUES (?, ?, ?, ?)"
        await self.execute(sql, (name, extension, department, email))

    async def delete_extension(self, ext_id: int):
        await self.execute("DELETE FROM extensions WHERE id = ?", (ext_id,))

    # ── INVENTARIO CRUD ────────────────────────────────────────────────────────

    async def get_all_inventory(self) -> list[dict]:
        return await self.fetch_all("SELECT * FROM inventory ORDER BY product_name")

    async def add_inventory_item(self, product_name: str, description: str,
                                 price: float, stock: int, category: str,
                                 brand: str = "", color: str = "", weight: str = ""):
        sql = """INSERT INTO inventory (product_name, description, price, stock, category, brand, color, weight)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        await self.execute(sql, (product_name, description, price, stock, category, brand, color, weight))

    async def delete_inventory_item(self, item_id: int):
        await self.execute("DELETE FROM inventory WHERE id = ?", (item_id,))

    # ── CALL LOGS ──────────────────────────────────────────────────────────────

    async def get_call_logs(self, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM call_logs ORDER BY created_at DESC LIMIT ?"
        return await self.fetch_all(sql, (limit,))

    async def get_token_stats_summary(self) -> dict:
        sql = """
            SELECT
                COUNT(*) as total_calls,
                COALESCE(SUM(tokens_input),0)  as tokens_input,
                COALESCE(SUM(tokens_output),0) as tokens_output,
                COALESCE(SUM(tokens_total),0)  as tokens_total,
                COALESCE(SUM(cost_usd),0)      as cost_usd,
                COALESCE(AVG(tokens_total),0)  as avg_tokens_per_call
            FROM call_logs
        """
        return await self.fetch_one(sql)

    async def get_token_usage_daily(self, days: int = 30) -> list[dict]:
        sql = """
            SELECT date, total_calls, tokens_input, tokens_output, tokens_total, cost_usd
            FROM token_usage_daily
            ORDER BY date DESC
            LIMIT ?
        """
        return await self.fetch_all(sql, (days,))

    async def get_top_calls_by_cost(self, limit: int = 10) -> list[dict]:
        sql = """
            SELECT session_id, caller_id, source, duration,
                   tokens_input, tokens_output, tokens_total, cost_usd, created_at
            FROM call_logs
            ORDER BY cost_usd DESC
            LIMIT ?
        """
        return await self.fetch_all(sql, (limit,))

    # ── MÉTODOS DE AUTENTICACIÓN Y SEGURIDAD ─────────────────────────────────

    async def get_user_by_username(self, username: str) -> dict:
        sql = "SELECT * FROM admin_users WHERE username = ?"
        return await self.fetch_one(sql, (username,))

    async def create_admin_user(self, username: str, password_plain: str, email: str = "", role: str = "user"):
        from auth.utils import hash_password
        password_hash = hash_password(password_plain)
        sql = "INSERT INTO admin_users (username, password_hash, email, role) VALUES (?, ?, ?, ?)"
        await self.execute(sql, (username, password_hash, email, role))

    async def create_session_token(self, user_id: int, duration_seconds: int = 24 * 3600) -> str:
        from auth.utils import generate_session_token
        from datetime import datetime, timedelta
        token = generate_session_token()
        expires_at = datetime.now() + timedelta(seconds=duration_seconds)
        sql = "INSERT INTO admin_sessions (session_token, user_id, expires_at) VALUES (?, ?, ?)"
        await self.execute(sql, (token, user_id, expires_at))
        return token

    async def validate_session_token(self, session_token: str) -> dict | None:
        from datetime import datetime
        sql = """
            SELECT s.expires_at, u.id as user_id, u.username, u.email, u.role
            FROM admin_sessions s
            JOIN admin_users u ON s.user_id = u.id
            WHERE s.session_token = ?
        """
        row = await self.fetch_one(sql, (session_token,))
        if not row:
            return None
        
        expires_at_str = row["expires_at"]
        try:
            if isinstance(expires_at_str, datetime):
                expires_at = expires_at_str
            else:
                expires_at = datetime.strptime(str(expires_at_str).split('.')[0], '%Y-%m-%d %H:%M:%S')
        except Exception:
            try:
                expires_at = datetime.fromisoformat(str(expires_at_str).replace('Z', ''))
            except Exception:
                expires_at = datetime.now()
        
        if expires_at < datetime.now():
            await self.delete_session_token(session_token)
            return None
            
        return {
            "id": row["user_id"],
            "username": row["username"],
            "email": row["email"],
            "role": row.get("role", "user")
        }

    async def delete_session_token(self, session_token: str):
        sql = "DELETE FROM admin_sessions WHERE session_token = ?"
        await self.execute(sql, (session_token,))

    # ── MÉTODOS DE PROMPTS Y AGENTES AISLADOS ───────────────────────────────

    async def get_admin_agent(self, user_id: int, agent_id: str) -> dict:
        sql = "SELECT * FROM admin_agents WHERE user_id = ? AND agent_id = ?"
        return await self.fetch_one(sql, (user_id, agent_id))

    async def save_admin_agent(self, user_id: int, agent_id: str, name: str, system_prompt: str):
        sql = """
            INSERT INTO admin_agents (user_id, agent_id, name, system_prompt)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, agent_id) DO UPDATE SET
                name = excluded.name,
                system_prompt = excluded.system_prompt
        """
        await self.execute(sql, (user_id, agent_id, name, system_prompt))

    async def get_all_admin_agents(self, user_id: int) -> list[dict]:
        sql = "SELECT * FROM admin_agents WHERE user_id = ? ORDER BY agent_id"
        return await self.fetch_all(sql, (user_id,))

