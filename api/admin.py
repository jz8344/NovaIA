from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/admin", tags=["Admin"])

_db = None
_session_manager = None
_prompt_loader = None


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
@router.get("/extensions")
async def list_extensions():
    return await _db.get_all_extensions()


@router.post("/extensions")
async def create_extension(data: ExtensionCreate):
    try:
        await _db.add_extension(data.name, data.extension, data.department, data.email)
        return {"success": True, "message": f"Extensión {data.extension} creada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/extensions/{ext_id}")
async def delete_extension(ext_id: int):
    await _db.delete_extension(ext_id)
    return {"success": True}


# --- Inventario ---
@router.get("/inventory")
async def list_inventory():
    return await _db.get_all_inventory()


@router.post("/inventory")
async def create_inventory_item(data: InventoryCreate):
    try:
        await _db.add_inventory_item(
            data.product_name, data.description,
            data.price, data.stock, data.category
        )
        return {"success": True, "message": f"Producto '{data.product_name}' creado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/inventory/{item_id}")
async def delete_inventory_item(item_id: int):
    await _db.delete_inventory_item(item_id)
    return {"success": True}


# --- Logs ---
@router.get("/logs")
async def list_call_logs(limit: int = 50):
    return await _db.get_call_logs(limit)


# --- Sesiones activas ---
@router.get("/sessions")
async def list_active_sessions():
    sessions = _session_manager.active_sessions
    return [
        {
            "session_id": s.session_id,
            "source": s.source,
            "caller_id": s.caller_id,
            "duration": round(s.duration, 1),
            "active": s.active
        }
        for s in sessions.values()
    ]


# --- System Prompts ---
@router.get("/prompts")
async def list_prompts():
    return _prompt_loader.list_prompts()


@router.get("/prompts/{name}")
async def get_prompt(name: str):
    content = _prompt_loader.load(name)
    return {"name": name, "content": content}


@router.put("/prompts/{name}")
async def update_prompt(name: str, data: PromptUpdate):
    import os
    filepath = os.path.join(_prompt_loader.prompts_dir, f"{name}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data.content)
    return {"success": True, "message": f"Prompt '{name}' actualizado"}
