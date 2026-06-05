import asyncio
from loguru import logger

from config.settings import get_settings
from core.session import SessionManager
from ai.gemini_live import GeminiLiveClient
from ai.function_registry import FunctionRegistry
from ai.prompt_loader import PromptLoader
from database.manager import DatabaseManager
from database.seed import seed_database
from telephony.audiosocket_server import AudioSocketServer
from telephony.ami_client import AMIClient

from actions.lookup_extension import (
    handle_lookup_extension,
    set_db as set_lookup_ext_db,
)
from actions.lookup_inventory import (
    handle_lookup_inventory,
    set_worker as set_lookup_inv_worker,
    set_db as set_lookup_inv_db,
)
from ai.inventory_worker import InventoryWorker
from actions.transfer_call import (
    handle_transfer_call,
    set_dependencies as set_transfer_deps,
)
from actions.end_call import handle_end_call
from actions.create_odoo_order import handle_create_odoo_order
from actions.search_odoo_contacts import handle_search_odoo_contacts
from actions.create_odoo_mailing import handle_create_odoo_mailing
from api.admin import set_dependencies as set_admin_deps

from core.exchange_updater import ExchangeRateUpdater

# Instancias globales
settings = get_settings()
db = DatabaseManager()
session_manager = SessionManager()
prompt_loader = PromptLoader()
function_registry = FunctionRegistry()
ami_client = AMIClient()
gemini_client: GeminiLiveClient | None = None
audiosocket_server: AudioSocketServer | None = None
exchange_updater: ExchangeRateUpdater | None = None

async def init_resources():
    global gemini_client, audiosocket_server, exchange_updater

    logger.info("=" * 60)
    logger.info("  Nova Voice Agent (Django) — Iniciando...")
    logger.info("=" * 60)

    exchange_updater = ExchangeRateUpdater()
    exchange_updater.start()

    await db.connect()
    await seed_database(db)

    set_lookup_ext_db(db)
    set_lookup_inv_db(db)
    worker = InventoryWorker(db)
    set_lookup_inv_worker(worker)
    set_transfer_deps(db, ami_client)
    set_admin_deps(db, session_manager, prompt_loader)

    function_registry.register("transfer_call", handle_transfer_call)
    function_registry.register("lookup_extension", handle_lookup_extension)
    function_registry.register("lookup_inventory", handle_lookup_inventory)
    function_registry.register("end_call", handle_end_call)
    function_registry.register("create_odoo_order", handle_create_odoo_order)
    function_registry.register("search_odoo_contacts", handle_search_odoo_contacts)
    function_registry.register("create_odoo_mailing", handle_create_odoo_mailing)
    logger.info(f"Funciones registradas: {function_registry.registered_functions}")

    await ami_client.connect()

    gemini_client = GeminiLiveClient(function_registry, prompt_loader)

    audiosocket_server = AudioSocketServer(session_manager)
    await audiosocket_server.start()

    logger.info("=" * 60)
    logger.info(f"  Nova lista en http://{settings.nova_host}:{settings.nova_port}")
    logger.info(f"  AudioSocket en {settings.audiosocket_host}:{settings.audiosocket_port}")
    logger.info(f"  Panel Admin: http://{settings.nova_host}:{settings.nova_port}/admin")
    logger.info("=" * 60)

async def close_resources():
    global audiosocket_server, exchange_updater
    logger.info("Nova Voice Agent (Django) — Cerrando...")
    if exchange_updater:
        try:
            exchange_updater.stop()
        except Exception as e:
            logger.error(f"Error deteniendo actualizador de divisas: {e}")
    if audiosocket_server:
        try:
            await audiosocket_server.stop()
        except Exception as e:
            logger.error(f"Error apagando AudioSocket: {e}")
    try:
        await ami_client.disconnect()
    except Exception as e:
        logger.error(f"Error desconectando AMI Client: {e}")
    try:
        await db.disconnect()
    except Exception as e:
        logger.error(f"Error desconectando Base de Datos: {e}")
    logger.info("Nova Voice Agent (Django) — Cerrado.")
