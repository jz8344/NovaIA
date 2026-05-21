import os
import uvicorn
from config.settings import get_settings

if __name__ == "__main__":
    # Establecer el módulo de configuración de Django por defecto
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

    settings = get_settings()

    logger_config = {
        "app": "django_project.asgi:application",
        "host": settings.nova_host,
        "port": settings.nova_port,
        "reload": settings.nova_debug,
        "log_level": "info",
    }

    # Iniciar el servidor asíncrono Uvicorn sirviendo Django ASGI
    uvicorn.run(
        logger_config["app"],
        host=logger_config["host"],
        port=logger_config["port"],
        reload=logger_config["reload"],
        log_level=logger_config["log_level"],
    )
