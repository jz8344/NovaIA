from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django_project.views import serve_index, serve_admin
from api.health import health_check
from api.admin import (
    extensions_list_create,
    delete_extension,
    inventory_list_create,
    delete_inventory_item,
    list_call_logs,
    list_active_sessions,
    get_token_stats,
    get_token_stats_daily,
    get_top_calls_by_cost,
    list_prompts,
    prompt_detail,
    prompt_config_handler,
    get_active_prompt_preview,
    custom_agents_handler,
    delete_custom_agent
)

urlpatterns = [
    # Páginas principales del frontend
    path('', serve_index),
    path('admin', serve_admin),
    path('admin/', serve_admin),
    
    # Endpoint de salud
    path('health', health_check),
    path('health/', health_check),
    
    # Endpoints de API de Administración
    path('api/admin/extensions', extensions_list_create),
    path('api/admin/extensions/<int:ext_id>', delete_extension),
    path('api/admin/inventory', inventory_list_create),
    path('api/admin/inventory/<int:item_id>', delete_inventory_item),
    path('api/admin/logs', list_call_logs),
    path('api/admin/sessions', list_active_sessions),
    path('api/admin/token-stats', get_token_stats),
    path('api/admin/token-stats/daily', get_token_stats_daily),
    path('api/admin/token-stats/top', get_top_calls_by_cost),
    path('api/admin/prompts', list_prompts),
    path('api/admin/prompts/<str:name>', prompt_detail),
    path('api/admin/prompt-config', prompt_config_handler),
    path('api/admin/prompt-config/active', get_active_prompt_preview),
    path('api/admin/custom-agents', custom_agents_handler),
    path('api/admin/custom-agents/<str:agent_id>', delete_custom_agent),
] + static('/static/', document_root=settings.STATICFILES_DIRS[0])
