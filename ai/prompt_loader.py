import os
from loguru import logger
from config.settings import get_settings


class PromptLoader:
    def __init__(self):
        self.prompts_dir = get_settings().prompts_dir

    def load(self, prompt_name: str = "nova_default") -> str:
        filepath_yaml = os.path.join(self.prompts_dir, f"{prompt_name}.yaml")
        filepath_md = os.path.join(self.prompts_dir, f"{prompt_name}.md")
        
        filepath = filepath_yaml if os.path.exists(filepath_yaml) else filepath_md
        
        if not os.path.exists(filepath):
            logger.warning(f"Prompt no encontrado: {filepath}, usando prompt vacío")
            return "Eres un asistente de voz profesional. Responde en español."

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(f"System prompt cargado: {filepath} ({len(content)} chars)")
        return content

    def list_prompts(self) -> list[str]:
        if not os.path.exists(self.prompts_dir):
            return []
        return [f.replace(".yaml", "").replace(".md", "") for f in os.listdir(self.prompts_dir) if f.endswith((".md", ".yaml"))]
