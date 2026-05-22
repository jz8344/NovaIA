from django.http import JsonResponse
from asgiref.sync import async_to_sync
from django_project.state import db

class AdminAuthMiddleware:
    """
    Middleware de Django para validar la sesión de administradores.
    Protege todos los endpoints bajo /api/admin/ validando la cookie 'session_token'.
    Inyecta el diccionario del usuario autenticado en request.admin_user.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Endpoints excluidos del middleware de autenticación
        if path in ["/api/auth/login", "/api/auth/logout"]:
            return self.get_response(request)

        # Validar cookies en rutas de API administrativas
        if path.startswith("/api/admin"):
            token = request.COOKIES.get("session_token")
            if not token:
                return JsonResponse({"detail": "No autorizado. Sesión no iniciada."}, status=401)

            user = async_to_sync(db.validate_session_token)(token)
            if not user:
                response = JsonResponse({"detail": "Sesión inválida o expirada."}, status=401)
                response.delete_cookie("session_token", path="/")
                return response

            # Adjuntar usuario a la petición
            request.admin_user = user

        return self.get_response(request)

