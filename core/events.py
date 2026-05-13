import asyncio
from typing import Callable, Any
from collections import defaultdict
from loguru import logger


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, handler: Callable):
        self._handlers[event].append(handler)
        logger.debug(f"Handler registrado para evento: {event}")

    def off(self, event: str, handler: Callable):
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    async def emit(self, event: str, **kwargs: Any):
        for handler in self._handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(**kwargs)
                else:
                    handler(**kwargs)
            except Exception as e:
                logger.error(f"Error en handler de evento '{event}': {e}")


event_bus = EventBus()
