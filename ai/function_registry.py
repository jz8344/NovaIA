import json
import os
from typing import Callable, Any
from loguru import logger
from google.genai import types
from config.settings import get_settings


class FunctionRegistry:
    def __init__(self):
        self._functions: dict[str, Callable] = {}
        self._schemas: list[dict] = []
        self.tools_dir = get_settings().tools_dir

    def register(self, name: str, handler: Callable):
        self._functions[name] = handler
        logger.debug(f"Función registrada: {name}")

    def load_schemas(self, config_name: str = "default_tools") -> list[types.Tool]:
        filepath = os.path.join(self.tools_dir, f"{config_name}.json")
        if not os.path.exists(filepath):
            logger.warning(f"Archivo de tools no encontrado: {filepath}")
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            config = json.load(f)

        tool_defs = config.get("tools", [])

        declarations = []
        for tool_def in tool_defs:
            declarations.append(
                types.FunctionDeclaration(
                    name=tool_def["name"],
                    description=tool_def["description"],
                    parameters=tool_def.get("parameters")
                )
            )

        logger.info(f"Cargadas {len(declarations)} herramientas desde {filepath}")
        return [types.Tool(function_declarations=declarations)]

    async def execute(self, function_name: str, arguments: dict) -> Any:
        handler = self._functions.get(function_name)
        if not handler:
            logger.error(f"Función no registrada: {function_name}")
            return {"error": f"Función '{function_name}' no encontrada"}

        logger.info(f"Ejecutando función: {function_name}({arguments})")
        try:
            import asyncio
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**arguments)
            else:
                result = handler(**arguments)
            logger.info(f"Resultado de {function_name}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error ejecutando {function_name}: {e}")
            return {"error": str(e)}

    @property
    def registered_functions(self) -> list[str]:
        return list(self._functions.keys())
