import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

from asgiref.sync import async_to_sync
from django_project.state import db

@ensure_csrf_cookie
def serve_index(request):
    """
    Sirve index.html del directorio web asegurando que la cookie
    csrftoken esté configurada en el cliente.
    """
    filepath = os.path.join(settings.BASE_DIR, 'templates', 'index.html')
    if not os.path.exists(filepath):
        raise Http404("Index HTML no encontrado")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')

@ensure_csrf_cookie
def serve_admin(request):
    """
    Sirve admin.html si el administrador está autenticado, de lo contrario sirve login.html.
    """
    token = request.COOKIES.get("session_token")
    user = None
    if token:
        try:
            user = async_to_sync(db.validate_session_token)(token)
        except Exception:
            pass

    filename = 'admin.html' if user else 'login.html'
    filepath = os.path.join(settings.BASE_DIR, 'templates', filename)
    if not os.path.exists(filepath):
        raise Http404(f"{filename} no encontrado")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')

