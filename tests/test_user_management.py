import sys
import os
import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock

# Configurar Django settings mínimas antes de realizar importaciones
from django.conf import settings
if not settings.configured:
    settings.configure(DEFAULT_CHARSET='utf-8')

import django
django.setup()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.manager import DatabaseManager
from auth.utils import hash_password, verify_password
from ai.prompt_loader import PromptLoader
from auth.middleware import AdminAuthMiddleware
import auth.middleware

class TestUserManagement(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_path = "./data/test_user_management.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass
        
        self.db = DatabaseManager()
        self.db.load_config = lambda: None
        self.db.db_type = "sqlite"
        self.db.sqlite_path = self.db_path
        await self.db.connect()

        self.prompts_dir = "./data/test_prompts"
        os.makedirs(self.prompts_dir, exist_ok=True)
        
        # Guardar valor original
        from config import settings as app_settings
        self._orig_prompts_dir = app_settings.get_settings().prompts_dir
        app_settings.get_settings().prompts_dir = self.prompts_dir

    async def asyncTearDown(self):
        await self.db.disconnect()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass
        
        import shutil
        if os.path.exists(self.prompts_dir):
            try:
                shutil.rmtree(self.prompts_dir)
            except Exception:
                pass
        
        from config import settings as app_settings
        app_settings.get_settings().prompts_dir = self._orig_prompts_dir

        # Limpiar configs de prompt temporales en data
        for f in os.listdir("./data"):
            if f.startswith("prompt_config_") or f.startswith("custom_agents_"):
                try:
                    os.remove(os.path.join("./data", f))
                except Exception:
                    pass

    async def test_roles_and_permissions(self):
        await self.db.create_admin_user("admin_user", "admin123", "admin@test.com", "admin")
        await self.db.create_admin_user("normal_user", "user123", "user@test.com", "user")

        admin = await self.db.get_user_by_username("admin_user")
        user = await self.db.get_user_by_username("normal_user")

        self.assertIsNotNone(admin)
        self.assertEqual(admin["role"], "admin")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "user")

    async def test_admin_deletion_protection(self):
        await self.db.create_admin_user("admin_to_del", "pass123", role="admin")
        user = await self.db.get_user_by_username("admin_to_del")
        self.assertIsNotNone(user)

        from api.admin import delete_user
        
        request = MagicMock()
        request.method = "DELETE"
        request.admin_user = {"id": user["id"], "role": "admin"}
        
        # Intentar auto-eliminarse
        response = await delete_user(request, user["id"])
        self.assertEqual(response.status_code, 400)
        
        body = json.loads(response.content.decode("utf-8"))
        self.assertIn("No puedes eliminar tu propia cuenta", body.get("detail", ""))

    async def test_middleware_role_based_access(self):
        from django_project import state
        orig_db = state.db
        state.db = self.db

        # Guardar async_to_sync original
        orig_async_to_sync = auth.middleware.async_to_sync

        try:
            admin_user = {"id": 1, "username": "admin", "role": "admin"}
            normal_user = {"id": 2, "username": "user", "role": "user"}

            # Simular usuario normal
            auth.middleware.async_to_sync = lambda fn: lambda token: normal_user

            middleware = AdminAuthMiddleware(get_response=lambda r: MagicMock(status_code=200))
            request = MagicMock()
            request.path = "/api/admin/users"
            request.COOKIES = {"session_token": "some_token"}
            
            res = middleware(request)
            self.assertEqual(res.status_code, 403)

            # Simular administrador
            auth.middleware.async_to_sync = lambda fn: lambda token: admin_user
            res = middleware(request)
            self.assertEqual(res.status_code, 200)
        finally:
            state.db = orig_db
            auth.middleware.async_to_sync = orig_async_to_sync

    async def test_prompt_physical_isolation(self):
        user_one_id = 101
        user_two_id = 202

        loader = PromptLoader()

        c1_path = loader._get_config_path(user_one_id)
        c2_path = loader._get_config_path(user_two_id)

        with open(c1_path, "w", encoding="utf-8") as f:
            json.dump({"mode": "raw"}, f)
        with open(c2_path, "w", encoding="utf-8") as f:
            json.dump({"mode": "raw"}, f)

        p1_path = os.path.join(self.prompts_dir, f"nova_default_{user_one_id}.yaml")
        p2_path = os.path.join(self.prompts_dir, f"nova_default_{user_two_id}.yaml")

        with open(p1_path, "w", encoding="utf-8") as f:
            f.write("system_prompt: Eres el asistente exclusivo del Usuario Uno")
        with open(p2_path, "w", encoding="utf-8") as f:
            f.write("system_prompt: Eres el asistente exclusivo del Usuario Dos")

        prompt_one = loader.load(user_id=user_one_id)
        prompt_two = loader.load(user_id=user_two_id)

        self.assertEqual(prompt_one, "Eres el asistente exclusivo del Usuario Uno")
        self.assertEqual(prompt_two, "Eres el asistente exclusivo del Usuario Dos")

if __name__ == "__main__":
    unittest.main()
