import sys
import os
import asyncio
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.manager import DatabaseManager
from auth.utils import hash_password, verify_password

class TestAuthIsolation(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Usamos una base de datos SQLite temporal en el directorio de pruebas
        self.db_path = "./data/test_auth_isolation.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass
        
        self.db = DatabaseManager()
        # Forzar SQLite local y desactivar carga de base de datos Postgres del entorno en pruebas
        self.db.load_config = lambda: None
        self.db.db_type = "sqlite"
        self.db.sqlite_path = self.db_path
        await self.db.connect()

    async def asyncTearDown(self):
        await self.db.disconnect()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass

    async def test_password_hashing(self):
        pwd = "super_secure_password"
        pwd_hash = hash_password(pwd)
        
        self.assertTrue(verify_password(pwd, pwd_hash))
        self.assertFalse(verify_password("wrong_password", pwd_hash))

    async def test_admin_user_creation_and_login(self):
        await self.db.create_admin_user("admin_test", "password123", "admin@test.com")
        
        user = await self.db.get_user_by_username("admin_test")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "admin_test")
        self.assertEqual(user["email"], "admin@test.com")
        self.assertTrue(verify_password("password123", user["password_hash"]))

        # Crear y validar sesión
        token = await self.db.create_session_token(user["id"])
        self.assertIsNotNone(token)

        session_user = await self.db.validate_session_token(token)
        self.assertIsNotNone(session_user)
        self.assertEqual(session_user["id"], user["id"])
        self.assertEqual(session_user["username"], "admin_test")

        # Eliminar sesión y verificar
        await self.db.delete_session_token(token)
        session_user_deleted = await self.db.validate_session_token(token)
        self.assertIsNone(session_user_deleted)

    async def test_agent_isolation(self):
        # Crear dos usuarios
        await self.db.create_admin_user("user_one", "pass123")
        await self.db.create_admin_user("user_two", "pass456")

        u1 = await self.db.get_user_by_username("user_one")
        u2 = await self.db.get_user_by_username("user_two")

        u1_id = u1["id"]
        u2_id = u2["id"]

        # Guardar agente de prueba para el usuario uno
        await self.db.save_admin_agent(
            user_id=u1_id,
            agent_id="agent_alpha",
            name="Agente Alfa U1",
            system_prompt="Tu eres el Agente Alfa para el Usuario Uno."
        )

        # Guardar agente de prueba para el usuario dos con el mismo agent_id pero diferente comportamiento
        await self.db.save_admin_agent(
            user_id=u2_id,
            agent_id="agent_alpha",
            name="Agente Alfa U2",
            system_prompt="Tu eres el Agente Alfa para el Usuario Dos."
        )

        # Validar aislamiento de lectura
        agent_u1 = await self.db.get_admin_agent(u1_id, "agent_alpha")
        agent_u2 = await self.db.get_admin_agent(u2_id, "agent_alpha")

        self.assertEqual(agent_u1["name"], "Agente Alfa U1")
        self.assertEqual(agent_u1["system_prompt"], "Tu eres el Agente Alfa para el Usuario Uno.")
        
        self.assertEqual(agent_u2["name"], "Agente Alfa U2")
        self.assertEqual(agent_u2["system_prompt"], "Tu eres el Agente Alfa para el Usuario Dos.")

        # Obtener todos los agentes por usuario y validar aislamiento
        all_u1 = await self.db.get_all_admin_agents(u1_id)
        all_u2 = await self.db.get_all_admin_agents(u2_id)

        self.assertEqual(len(all_u1), 1)
        self.assertEqual(all_u1[0]["name"], "Agente Alfa U1")

        self.assertEqual(len(all_u2), 1)
        self.assertEqual(all_u2[0]["name"], "Agente Alfa U2")

if __name__ == "__main__":
    unittest.main()
