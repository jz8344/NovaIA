import os
import json
from pathlib import Path
import uuid
from django.http import JsonResponse, HttpResponse
from pydantic import BaseModel
from typing import Optional

_db = None
_session_manager = None
_prompt_loader = None


def _get_prompt_loader():
    global _prompt_loader
    if _prompt_loader is None:
        from ai.prompt_loader import PromptLoader
        _prompt_loader = PromptLoader()
    return _prompt_loader


def set_dependencies(db, session_manager, prompt_loader):
    global _db, _session_manager, _prompt_loader
    _db = db
    _session_manager = session_manager
    _prompt_loader = prompt_loader


class ExtensionCreate(BaseModel):
    name: str
    extension: str
    department: str = ""
    email: str = ""


class InventoryCreate(BaseModel):
    product_name: str
    description: str = ""
    price: float = 0.0
    stock: int = 0
    category: str = ""


class PromptUpdate(BaseModel):
    name: str
    content: str


# --- Extensiones ---
async def extensions_list_create(request):
    if request.method == "GET":
        data = await _db.get_all_extensions()
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            data = ExtensionCreate(**body)
            await _db.add_extension(data.name, data.extension, data.department, data.email)
            return JsonResponse({"success": True, "message": f"Extensión {data.extension} creada"})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    return HttpResponse(status=405)


async def delete_extension(request, ext_id: int):
    if request.method == "DELETE":
        await _db.delete_extension(ext_id)
        return JsonResponse({"success": True})
    return HttpResponse(status=405)


# --- Inventario ---
async def inventory_list_create(request):
    if request.method == "GET":
        data = await _db.get_all_inventory()
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            data = InventoryCreate(**body)
            await _db.add_inventory_item(
                data.product_name, data.description,
                data.price, data.stock, data.category
            )
            return JsonResponse({"success": True, "message": f"Producto '{data.product_name}' creado"})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    return HttpResponse(status=405)


async def delete_inventory_item(request, item_id: int):
    if request.method == "DELETE":
        await _db.delete_inventory_item(item_id)
        return JsonResponse({"success": True})
    return HttpResponse(status=405)


# --- Logs ---
async def list_call_logs(request):
    if request.method == "GET":
        limit = int(request.GET.get("limit", 50))
        data = await _db.get_call_logs(limit)
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)


# --- Sesiones activas ---
async def list_active_sessions(request):
    if request.method == "GET":
        from core.session import TOKEN_LIMIT_PER_SESSION
        sessions = _session_manager.active_sessions
        data = [
            {
                "session_id": s.session_id,
                "source": s.source,
                "caller_id": s.caller_id,
                "duration": round(s.duration, 1),
                "active": s.active,
                "tokens_input": s.tokens_input,
                "tokens_output": s.tokens_output,
                "tokens_total": s.tokens_total,
                "token_limit": TOKEN_LIMIT_PER_SESSION,
                "token_pct": round(s.tokens_total / TOKEN_LIMIT_PER_SESSION * 100, 1),
            }
            for s in sessions.values()
        ]
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)


# --- Estadísticas de tokens ---
async def get_token_stats(request):
    if request.method == "GET":
        data = await _db.get_token_stats_summary()
        return JsonResponse(data)
    return HttpResponse(status=405)


async def get_token_stats_daily(request):
    if request.method == "GET":
        days = int(request.GET.get("days", 30))
        data = await _db.get_token_usage_daily(days)
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)


async def get_top_calls_by_cost(request):
    if request.method == "GET":
        limit = int(request.GET.get("limit", 10))
        data = await _db.get_top_calls_by_cost(limit)
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)


# --- System Prompts ---
async def list_prompts(request):
    if request.method == "GET":
        data = _get_prompt_loader().list_prompts()
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)


async def prompt_detail(request, name: str):
    if request.method == "GET":
        content = _get_prompt_loader().load(name)
        return JsonResponse({"name": name, "content": content})
    elif request.method == "PUT":
        try:
            body = json.loads(request.body.decode("utf-8"))
            data = PromptUpdate(**body)
            loader = _get_prompt_loader()
            os.makedirs(loader.prompts_dir, exist_ok=True)
            
            filepath_md = os.path.join(loader.prompts_dir, f"{name}.md")
            with open(filepath_md, "w", encoding="utf-8") as f:
                f.write(data.content)
            
            filepath_yaml = os.path.join(loader.prompts_dir, f"{name}.yaml")
            try:
                import yaml
                yaml.safe_load(data.content)
                with open(filepath_yaml, "w", encoding="utf-8") as f:
                    f.write(data.content)
            except Exception:
                pass
            
            return JsonResponse({"success": True, "message": f"Prompt '{name}' guardado en archivos"})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    return HttpResponse(status=405)


_PROJECT_ROOT = Path(__file__).parent.parent
PROMPT_CONFIG_PATH = str(_PROJECT_ROOT / "data" / "prompt_config.json")


async def prompt_config_handler(request):
    if request.method == "GET":
        if os.path.exists(PROMPT_CONFIG_PATH):
            with open(PROMPT_CONFIG_PATH, "r", encoding="utf-8") as f:
                return JsonResponse(json.load(f))
        return JsonResponse({"use_custom": False, "mode": "builder", "raw_content": "", "builder": {}})
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            os.makedirs(str(_PROJECT_ROOT / "data"), exist_ok=True)
            
            existing_config = {}
            if os.path.exists(PROMPT_CONFIG_PATH):
                try:
                    with open(PROMPT_CONFIG_PATH, "r", encoding="utf-8") as f:
                        existing_config = json.load(f)
                except Exception:
                    pass
                    
            mode = data.get("mode", "builder")
            loader = _get_prompt_loader()
            os.makedirs(loader.prompts_dir, exist_ok=True)
            
            existing_config["mode"] = mode
            if "use_custom" in data:
                existing_config["use_custom"] = data["use_custom"]
            if "voice" in data:
                existing_config["voice"] = data["voice"]
            
            if mode == "builder":
                builder = data.get("builder", {})
                if builder:
                    existing_config["builder"] = builder
                    compiled = loader._build_from_config(builder)
                    filepath_md = os.path.join(loader.prompts_dir, "nova_builder.md")
                    with open(filepath_md, "w", encoding="utf-8") as f:
                        f.write(compiled)
                        
            elif mode == "raw":
                raw_content = data.get("raw_content", "").strip()
                existing_config["raw_content"] = raw_content
                filepath_yaml = os.path.join(loader.prompts_dir, "nova_default.yaml")
                with open(filepath_yaml, "w", encoding="utf-8") as f:
                    f.write(raw_content)
                    
            elif mode == "agent":
                agent_id = data.get("agent_id")
                agent_source = data.get("agent_source", "preset")
                agent_builder = data.get("agent_builder") or data.get("builder", {})
                
                existing_config["agent_id"] = agent_id
                existing_config["agent_source"] = agent_source
                if agent_builder:
                    existing_config["agent_builder"] = agent_builder
                    compiled = loader._build_from_config(agent_builder)
                    
                    if agent_source == "custom" and agent_id:
                        filepath_md = os.path.join(loader.prompts_dir, f"nova_custom_{agent_id}.md")
                        with open(filepath_md, "w", encoding="utf-8") as f:
                            f.write(compiled)
                    else:
                        filepath_md = os.path.join(loader.prompts_dir, "nova_agent.md")
                        with open(filepath_md, "w", encoding="utf-8") as f:
                            f.write(compiled)
                        
                        if agent_id:
                            import yaml
                            filepath_yaml = os.path.join(loader.prompts_dir, f"nova_{agent_id}.yaml")
                            preset_data = {
                                "name": agent_builder.get("identity", {}).get("name", "Nova"),
                                "company": agent_builder.get("identity", {}).get("company", "la empresa"),
                                "role": agent_builder.get("identity", {}).get("role", "asistente"),
                                "greeting": agent_builder.get("greeting", ""),
                                "language": agent_builder.get("language", "es"),
                                "tone": agent_builder.get("tone", "friendly"),
                                "personality": agent_builder.get("personality", []),
                                "capabilities": agent_builder.get("capabilities", []),
                                "rules": agent_builder.get("rules", []),
                                "custom_instructions": agent_builder.get("custom_instructions", ""),
                                "system_prompt": compiled
                            }
                            with open(filepath_yaml, "w", encoding="utf-8") as f:
                                yaml.safe_dump(preset_data, f, allow_unicode=True, default_flow_style=False)

            with open(PROMPT_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(existing_config, f, ensure_ascii=False, indent=2)
                
            return JsonResponse({"success": True, "message": "Configuración de prompt guardada e implementada físicamente"})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
            
    return HttpResponse(status=405)


async def get_active_prompt_preview(request):
    if request.method == "GET":
        from ai.prompt_loader import PromptLoader
        loader = PromptLoader()
        text = loader.load()
        return JsonResponse({
            "prompt_preview": text[:500] + "..." if len(text) > 500 else text,
            "total_chars": len(text),
            "config_path": PROMPT_CONFIG_PATH,
            "config_exists": os.path.exists(PROMPT_CONFIG_PATH)
        })
    return HttpResponse(status=405)


CUSTOM_AGENTS_PATH = str(_PROJECT_ROOT / "data" / "custom_agents.json")


def _load_custom_agents() -> list:
    if os.path.exists(CUSTOM_AGENTS_PATH):
        with open(CUSTOM_AGENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_custom_agents(agents: list):
    os.makedirs(str(_PROJECT_ROOT / "data"), exist_ok=True)
    with open(CUSTOM_AGENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)


async def custom_agents_handler(request):
    if request.method == "GET":
        return JsonResponse(_load_custom_agents(), safe=False)
        
    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            agents = _load_custom_agents()
            
            agent_id = str(uuid.uuid4())[:8]
            data["id"] = agent_id
            
            builder = data.get("builder", {})
            if builder:
                loader = _get_prompt_loader()
                compiled = loader._build_from_config(builder)
                os.makedirs(loader.prompts_dir, exist_ok=True)
                filepath_md = os.path.join(loader.prompts_dir, f"nova_custom_{agent_id}.md")
                with open(filepath_md, "w", encoding="utf-8") as f:
                    f.write(compiled)
                    
            agents.append(data)
            _save_custom_agents(agents)
            return JsonResponse({"success": True, "id": agent_id, "message": f"Agente '{data.get('profile_name', '')}' guardado físicamente"})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
            
    return HttpResponse(status=405)


async def delete_custom_agent(request, agent_id: str):
    if request.method == "DELETE":
        agents = _load_custom_agents()
        agents = [a for a in agents if a.get("id") != agent_id]
        _save_custom_agents(agents)
        
        loader = _get_prompt_loader()
        filepath_md = os.path.join(loader.prompts_dir, f"nova_custom_{agent_id}.md")
        if os.path.exists(filepath_md):
            try:
                os.remove(filepath_md)
            except Exception:
                pass
                
        return JsonResponse({"success": True})
    return HttpResponse(status=405)
