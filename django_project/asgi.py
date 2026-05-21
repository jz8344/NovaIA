import os
import django
from django.core.asgi import get_asgi_application

# Configurar variables de entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Inicializar Django antes de importar componentes que dependan de settings
django.setup()
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from loguru import logger

from django_project.consumers import VoiceConsumer
from django_project.state import init_resources, close_resources

# Router principal de protocolos para Daphne / Channels
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path("ws/voice", VoiceConsumer.as_asgi()),
    ]),
})

# Middleware ASGI para interceptar y gestionar el ciclo de vida (Lifespan) de la aplicación
class LifespanMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    try:
                        logger.info("ASGI Lifespan: Inicializando recursos globales...")
                        await init_resources()
                        await send({'type': 'lifespan.startup.complete'})
                        logger.info("ASGI Lifespan: Inicialización completada exitosamente.")
                    except Exception as e:
                        logger.error(f"ASGI Lifespan: Falló el inicio de recursos: {e}")
                        await send({'type': 'lifespan.startup.failed', 'message': str(e)})
                elif message['type'] == 'lifespan.shutdown':
                    try:
                        logger.info("ASGI Lifespan: Liberando recursos globales...")
                        await close_resources()
                        await send({'type': 'lifespan.shutdown.complete'})
                        logger.info("ASGI Lifespan: Recursos liberados.")
                    except Exception as e:
                        logger.error(f"ASGI Lifespan: Falló el apagado de recursos: {e}")
                        await send({'type': 'lifespan.shutdown.failed', 'message': str(e)})
                    break
        else:
            await self.app(scope, receive, send)

application = LifespanMiddleware(application)
