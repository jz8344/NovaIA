import os
import socket
import uvicorn
from config.settings import get_settings

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

    settings = get_settings()
    port = int(os.environ.get("PORT", settings.nova_port))

    if settings.nova_host == "0.0.0.0":
        local_ip = get_local_ip()
        print("\n" + "=" * 80)
        print(" [*] SERVIDOR HABILITADO EN TU RED LOCAL")
        print(f" [*] Accede localmente en: http://localhost:{port}/")
        print(f" [*] Accede desde otros dispositivos (celular/otra PC): http://{local_ip}:{port}/")
        print("=" * 80 + "\n")

    is_production = "PORT" in os.environ or "RAILWAY_STATIC_URL" in os.environ
    reload_app = settings.nova_debug if not is_production else False

    logger_config = {
        "app": "django_project.asgi:application",
        "host": settings.nova_host,
        "port": port,
        "reload": reload_app,
        "log_level": "info",
    }

    uvicorn.run(
        logger_config["app"],
        host=logger_config["host"],
        port=logger_config["port"],
        reload=logger_config["reload"],
        log_level=logger_config["log_level"],
    )
