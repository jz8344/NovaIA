import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def serve_index(request):
    """
    Sirve index.html del directorio web asegurando que la cookie
    csrftoken esté configurada en el cliente.
    """
    filepath = os.path.join(settings.BASE_DIR, 'web', 'index.html')
    if not os.path.exists(filepath):
        raise Http404("Index HTML no encontrado")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')

@ensure_csrf_cookie
def serve_admin(request):
    """
    Sirve admin.html del directorio web asegurando que la cookie
    csrftoken esté configurada en el cliente.
    """
    filepath = os.path.join(settings.BASE_DIR, 'web', 'admin.html')
    if not os.path.exists(filepath):
        raise Http404("Admin HTML no encontrado")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/html')
