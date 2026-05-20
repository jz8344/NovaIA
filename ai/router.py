import re
import unicodedata
from loguru import logger

class IntelligentRouter:
    # ── TIER 0: REGEX DE SALUDOS Y DESPEDIDAS ────────────────────────────────
    _GREETINGS = [
        r"\b(hola|buenos\s+dias|buenas\s+tardes|buenas\s+noches|alo|saludos|buen\s+dia)\b"
    ]
    _FAREWELLS = [
        r"\b(adios|chao|hasta\s+luego|hasta\s+pronto|nos\s+vemos|bye|finalizar\s+llamada|terminar\s+llamada)\b"
    ]
    _THANKS = [
        r"\b(gracias|muchas\s+gracias|excelente|entendido|ok|perfecto|muy\s+amable)\b"
    ]

    _greeting_regexes = [re.compile(p, re.IGNORECASE) for p in _GREETINGS]
    _farewell_regexes = [re.compile(p, re.IGNORECASE) for p in _FAREWELLS]
    _thanks_regexes   = [re.compile(p, re.IGNORECASE) for p in _THANKS]

    # ── TIER 1: PREGUNTAS FRECUENTES (FAQ) SEMÁNTICA LOCAL ───────────────────
    _FAQ_DATA = [
        {
            "keys": {"horario", "horarios", "atencion", "abren", "cierran", "hora", "abierto", "cerrado", "dias"},
            "response": "Nuestros horarios de atención son de lunes a viernes, de 9:00 AM a 6:00 PM."
        },
        {
            "keys": {"ubicacion", "ubicados", "ubicada", "direccion", "oficina", "donde", "queda", "fisica", "llegar", "mapa"},
            "response": "Estamos ubicados en la Avenida Central 100, Torre Empresarial, Piso 5."
        },
        {
            "keys": {"soporte", "tecnico", "ayuda", "falla", "problema", "ayudar", "asistencia"},
            "response": "Puedes contactar a soporte técnico solicitando que te transfiera a la extensión 102 de Soporte o enviando un correo a soporte@techsolutions.com."
        },
        {
            "keys": {"ventas", "comprar", "cotizar", "compras", "precio", "cotizacion", "adquirir", "costo"},
            "response": "Para compras y cotizaciones, te recomiendo solicitar la extensión 101 de Ventas o enviar un correo a ventas@techsolutions.com."
        }
    ]

    _STOPWORDS = {
        "de", "la", "el", "en", "y", "a", "que", "un", "una", "los", "las", "por",
        "para", "con", "es", "son", "se", "del", "al", "cual", "cuales", "como",
        "mi", "tu", "su", "nos", "me", "te", "le", "lo", "la", "os", "les"
    }

    @classmethod
    def _normalize(cls, text: str) -> str:
        nfd = unicodedata.normalize('NFD', text)
        cleaned = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn').lower()
        return re.sub(r'[^\w\s]', ' ', cleaned)

    @classmethod
    def _get_words(cls, text: str) -> set[str]:
        norm = cls._normalize(text)
        words = norm.split()
        return {w for w in words if w not in cls._STOPWORDS and len(w) >= 3}

    @classmethod
    def route(cls, text: str) -> dict | None:
        """
        Analiza el texto de entrada.
        Retorna un dict con {"tier": int, "response": str, "action": str} si es procesado localmente,
        o None si debe pasarse al Tier superior (Gemini Flash/Live).
        """
        if not text or not text.strip():
            return None

        normalized = text.strip()

        # ── EVALUAR TIER 0 ───────────────────────────────────────────────────
        for regex in cls._farewell_regexes:
            if regex.search(normalized):
                logger.info(f"[ROUTER] Match Tier 0 (Despedida): '{text}'")
                return {
                    "tier": 0,
                    "response": "Muchas gracias por comunicarte con Tech Solutions. ¡Que tengas un excelente día, adiós!",
                    "action": "hangup"
                }

        for regex in cls._greeting_regexes:
            if regex.search(normalized):
                # Validar que no sea parte de una consulta más larga (e.g. "Hola, quiero saber...")
                words = cls._get_words(normalized)
                if len(words) <= 1:
                    logger.info(f"[ROUTER] Match Tier 0 (Saludo): '{text}'")
                    return {
                        "tier": 0,
                        "response": "¡Hola! Bienvenido a Tech Solutions. ¿En qué puedo ayudarte hoy?",
                        "action": "greet"
                    }

        for regex in cls._thanks_regexes:
            if regex.search(normalized):
                words = cls._get_words(normalized)
                if len(words) <= 1:
                    logger.info(f"[ROUTER] Match Tier 0 (Agradecimiento): '{text}'")
                    return {
                        "tier": 0,
                        "response": "De nada. Es un placer ayudarte. ¿Hay algo más en lo que pueda colaborar?",
                        "action": "acknowledge"
                    }

        # ── EVALUAR TIER 1 ───────────────────────────────────────────────────
        input_words = cls._get_words(normalized)
        if not input_words:
            return None

        best_match = None
        highest_score = 0.0

        for faq in cls._FAQ_DATA:
            intersection = input_words.intersection(faq["keys"])
            if intersection:
                # Puntuación basada en proporción de palabras significativas de la consulta
                score = len(intersection) / len(input_words)
                if score > highest_score:
                    highest_score = score
                    best_match = faq

        # Si supera el umbral de similitud semántica (0.25 sobre la consulta), responde FAQ local
        if best_match and highest_score >= 0.25:
            logger.info(f"[ROUTER] Match Tier 1 (FAQ, confianza={highest_score:.2f}): '{text}'")
            return {
                "tier": 1,
                "response": best_match["response"],
                "action": "faq"
            }

        return None
