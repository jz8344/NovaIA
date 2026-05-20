import re
from loguru import logger

class SecurityGuard:
    _INJECTION_PATTERNS = [
        r"(ignore|ignora|olvida).*?(instrucciones|instructions|reglas|directivas|indicaciones|system|prompt)",
        r"system\s+(override|bypass|reset)",
        r"(dame|revela|muestra|show|tell\s+me).*?(prompt|system\s+instruction|reglas\s+estrictas|instrucciones)",
        r"act(ua|úe|úa)?\s+como.*?(terminal|desarrollador|administrador|consola|shell|developer|admin|root)",
        r"act\s+as.*?(terminal|shell|developer|admin|root)",
        r"system:\s*user\s+(disconnected|hungup|left)",
        r"nueva\s+regla\s+absoluta",
    ]

    _compiled_regex = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]

    @classmethod
    def is_injection(cls, text: str) -> bool:
        if not text or not text.strip():
            return False
        
        normalized = text.strip()
        for regex in cls._compiled_regex:
            if regex.search(normalized):
                logger.warning(f"[SECURITY ALERT] Intento de Prompt Injection bloqueado en input: '{text}'")
                return True
        return False

    @classmethod
    def get_safe_response(cls) -> str:
        return "Lo siento, no puedo procesar esa solicitud. ¿En qué puedo ayudarte con respecto al directorio o el inventario?"
