import asyncio
import json
from typing import Callable, Any
from collections import defaultdict
from loguru import logger


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._pubsub_task: asyncio.Task | None = None

    def on(self, event: str, handler: Callable):
        self._handlers[event].append(handler)
        logger.debug(f"Handler registrado para evento: {event}")

    def off(self, event: str, handler: Callable):
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    async def emit(self, event: str, **kwargs: Any):
        await self._emit_local(event, **kwargs)

        from django_project import state
        if state.redis_client is not None:
            try:
                serializable_kwargs = {}
                for k, v in kwargs.items():
                    if k == "session":
                        serializable_kwargs["session_id"] = v.session_id
                    else:
                        try:
                            json.dumps(v)
                            serializable_kwargs[k] = v
                        except Exception:
                            pass

                payload = {
                    "event": event,
                    "kwargs": serializable_kwargs,
                    "origin": id(self),
                }
                await state.redis_client.publish("nova_events", json.dumps(payload))
            except Exception as e:
                logger.error(f"Error publicando evento {event} en Redis: {e}")

    async def _emit_local(self, event: str, **kwargs: Any):
        for handler in self._handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(**kwargs)
                else:
                    handler(**kwargs)
            except Exception as e:
                logger.error(f"Error en handler de evento '{event}': {e}")

    def start_listener(self):
        from django_project import state
        if state.redis_client is not None and self._pubsub_task is None:
            self._pubsub_task = asyncio.create_task(self._listen_loop())
            logger.info("Redis Pub/Sub EventBus listener iniciado.")

    async def stop_listener(self):
        if self._pubsub_task:
            self._pubsub_task.cancel()
            try:
                await self._pubsub_task
            except (asyncio.CancelledError, Exception):
                pass
            self._pubsub_task = None
            logger.info("Redis Pub/Sub EventBus listener detenido.")

    async def _listen_loop(self):
        from django_project import state
        pubsub = state.redis_client.pubsub()
        try:
            await pubsub.subscribe("nova_events")
            while True:
                try:
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if message and message.get("type") == "message":
                        data = json.loads(message["data"])
                        if data.get("origin") == id(self):
                            continue

                        event = data.get("event")
                        kwargs = data.get("kwargs", {})

                        if "session_id" in kwargs:
                            session_id = kwargs["session_id"]
                            if event == "session_kill_request":
                                s = await state.session_manager.get_session(session_id)
                                if s:
                                    logger.info(f"Kill request recibida vía Pub/Sub para sesión local: {session_id}")
                                    await state.session_manager.end_session(session_id, reason="new_session_override")
                                continue

                            s = await state.session_manager.get_session(session_id)
                            if s:
                                kwargs["session"] = s

                        await self._emit_local(event, **kwargs)
                except asyncio.CancelledError:
                    break
                except Exception as loop_err:
                    logger.error(f"Error en bucle de eventos de Pub/Sub: {loop_err}")
                    await asyncio.sleep(1.0)
        except Exception as e:
            logger.error(f"Error en inicialización de suscripción Pub/Sub: {e}")
        finally:
            try:
                await pubsub.unsubscribe("nova_events")
            except Exception:
                pass


event_bus = EventBus()
