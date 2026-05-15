import os
from loguru import logger
from config.settings import get_settings


class PromptLoader:
    def __init__(self, db=None):
        self.prompts_dir = get_settings().prompts_dir
        self.db = db

    def set_db(self, db):
        """Inyectar la BD después de inicializar"""
        self.db = db

    async def load(self, prompt_name: str = "nova_default") -> str:
        # Primero intenta cargar de BD si está disponible
        if self.db:
            try:
                prompt_data = await self.db.get_prompt(prompt_name)
                if prompt_data:
                    logger.info(f"System prompt cargado desde BD: {prompt_name} ({len(prompt_data['system_prompt'])} chars)")
                    return prompt_data["system_prompt"]
            except Exception as e:
                logger.warning(f"Error al cargar prompt de BD: {e}, usando archivo por defecto")

        # Fallback a archivos
        filepath_yaml = os.path.join(self.prompts_dir, f"{prompt_name}.yaml")
        filepath_md = os.path.join(self.prompts_dir, f"{prompt_name}.md")
        
        filepath = filepath_yaml if os.path.exists(filepath_yaml) else filepath_md
        
        if not os.path.exists(filepath):
            logger.warning(f"Prompt no encontrado: {filepath}, usando prompt vacío")
            return "Eres un asistente de voz profesional. Responde en español."

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(f"System prompt cargado desde archivo: {filepath} ({len(content)} chars)")
        return content

    def list_prompts(self) -> list[str]:
        if not os.path.exists(self.prompts_dir):
            return []
        return [f.replace(".yaml", "").replace(".md", "") for f in os.listdir(self.prompts_dir) if f.endswith((".md", ".yaml"))]
