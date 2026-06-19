import os
import uvicorn
import django
from config.settings import get_settings

if __name__ == "__main__":
    # Inicializar Django para tener acceso al ORM y base de datos
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    django.setup()

    settings = get_settings()
    
    # El puerto del microservicio de tiempo real por defecto es 8001
    port = int(os.environ.get("REALTIME_PORT", 8001))
    host = os.environ.get("REALTIME_HOST", settings.nova_host)
    
    is_production = "PORT" in os.environ or "RAILWAY_STATIC_URL" in os.environ
    reload_app = settings.nova_debug if not is_production else False

    print("\n" + "=" * 80)
    print(" [*] INICIANDO NOVA VOICE AGENT — MOTOR DE TIEMPO REAL (MICROSERVICIO)")
    print(f" [*] Escuchando conexiones en: ws://{host}:{port}/ws/voice")
    print(f" [*] AudioSocket escuchando en: {settings.audiosocket_host}:{settings.audiosocket_port}")
    print("=" * 80 + "\n")

    uvicorn.run(
        "realtime.app:fastapi_app",
        host=host,
        port=port,
        reload=reload_app,
        log_level="info",
    )
