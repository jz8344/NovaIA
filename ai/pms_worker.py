import httpx
import asyncio
from datetime import datetime, timedelta
from loguru import logger


# Caché global para compartir tokens JWT entre múltiples instancias de PmsWorker
# Clave: (base_url, username) -> Valor: (token, expires_datetime)
_token_cache: dict[tuple[str, str], tuple[str, datetime]] = {}
_token_cache_lock = asyncio.Lock()


def _invalidate_token_cache(base_url: str, username: str):
    cache_key = (base_url.rstrip("/"), username)
    _token_cache.pop(cache_key, None)


class PmsWorker:
    """
    Cliente asíncrono para el PMS Hotel (FastAPI + SQLite con JWT).
    Autenticación: POST /login → Bearer token (24h de validez).
    """

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self._token: str | None = None
        self._token_expires: datetime | None = None

    # ── Auth ─────────────────────────────────────────────────────────────────

    async def _authenticate(self) -> bool:
        url = f"{self.base_url}/api/login"
        payload = {"username": self.username, "password": self.password}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    self._token = data.get("access_token")
                    self._token_expires = datetime.now() + timedelta(hours=23)
                    logger.info(f"PmsWorker: Autenticado exitosamente como '{self.username}'")
                    return True
                logger.error(f"PmsWorker: Login fallido HTTP {resp.status_code}: {resp.text[:200]}")
                return False
        except httpx.TimeoutException:
            logger.error("PmsWorker: Timeout al intentar login en PMS")
            return False
        except Exception as e:
            logger.error(f"PmsWorker: Error en autenticación: {e}")
            return False

    async def _get_token(self) -> str | None:
        async with _token_cache_lock:
            cache_key = (self.base_url, self.username)
            cached = _token_cache.get(cache_key)
            if cached:
                token, expires = cached
                if datetime.now() < expires:
                    self._token = token
                    self._token_expires = expires
                    return token

            # Si no hay token o ya expiró
            ok = await self._authenticate()
            if ok and self._token and self._token_expires:
                _token_cache[cache_key] = (self._token, self._token_expires)
                return self._token
        return None

    def _headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    # ── HTTP helpers ─────────────────────────────────────────────────────────

    async def _get(self, path: str, params: dict | None = None) -> dict | list | None:
        token = await self._get_token()
        if not token:
            return None
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.get(url, headers=self._headers(token), params=params or {})
                if resp.status_code == 401:
                    _invalidate_token_cache(self.base_url, self.username)
                    self._token = None
                    logger.warning("PmsWorker: Token expirado, reintentando...")
                    token = await self._get_token()
                    if not token:
                        return None
                    resp = await client.get(url, headers=self._headers(token), params=params or {})
                if resp.status_code == 200:
                    return resp.json()
                logger.error(f"PmsWorker GET {path} → HTTP {resp.status_code}: {resp.text[:200]}")
                return None
        except httpx.TimeoutException:
            logger.error(f"PmsWorker: Timeout en GET {path}")
            return None
        except Exception as e:
            logger.error(f"PmsWorker GET {path} error: {e}")
            return None

    async def _post(self, path: str, body: dict) -> dict | None:
        token = await self._get_token()
        if not token:
            return None
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.post(url, headers=self._headers(token), json=body)
                if resp.status_code == 401:
                    _invalidate_token_cache(self.base_url, self.username)
                    self._token = None
                    token = await self._get_token()
                    if not token:
                        return None
                    resp = await client.post(url, headers=self._headers(token), json=body)
                if resp.status_code in (200, 201):
                    return resp.json()
                logger.error(f"PmsWorker POST {path} → HTTP {resp.status_code}: {resp.text[:300]}")
                return None
        except httpx.TimeoutException:
            logger.error(f"PmsWorker: Timeout en POST {path}")
            return None
        except Exception as e:
            logger.error(f"PmsWorker POST {path} error: {e}")
            return None

    async def _patch(self, path: str, body: dict) -> dict | None:
        token = await self._get_token()
        if not token:
            return None
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.patch(url, headers=self._headers(token), json=body)
                if resp.status_code == 401:
                    _invalidate_token_cache(self.base_url, self.username)
                    self._token = None
                    token = await self._get_token()
                    if not token:
                        return None
                    resp = await client.patch(url, headers=self._headers(token), json=body)
                if resp.status_code in (200, 201):
                    return resp.json()
                logger.error(f"PmsWorker PATCH {path} → HTTP {resp.status_code}: {resp.text[:300]}")
                return None
        except httpx.TimeoutException:
            logger.error(f"PmsWorker: Timeout en PATCH {path}")
            return None
        except Exception as e:
            logger.error(f"PmsWorker PATCH {path} error: {e}")
            return None

    async def _put(self, path: str, body: dict) -> dict | None:
        token = await self._get_token()
        if not token:
            return None
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.put(url, headers=self._headers(token), json=body)
                if resp.status_code == 401:
                    _invalidate_token_cache(self.base_url, self.username)
                    self._token = None
                    token = await self._get_token()
                    if not token:
                        return None
                    resp = await client.put(url, headers=self._headers(token), json=body)
                if resp.status_code in (200, 201):
                    return resp.json()
                logger.error(f"PmsWorker PUT {path} → HTTP {resp.status_code}: {resp.text[:300]}")
                return None
        except httpx.TimeoutException:
            logger.error(f"PmsWorker: Timeout en PUT {path}")
            return None
        except Exception as e:
            logger.error(f"PmsWorker PUT {path} error: {e}")
            return None

    # ── PMS Operations ────────────────────────────────────────────────────────

    async def get_available_rooms(self, room_type: str | None = None) -> str:
        data = await self._get("/api/rooms")
        if data is None:
            return "No se pudo conectar al sistema hotelero. Por favor intenta más tarde."

        rooms = data if isinstance(data, list) else data.get("rooms", [])
        available = [r for r in rooms if r.get("status", "").lower() in ("disponible", "available", "libre")]

        if room_type:
            t = room_type.lower()
            available = [r for r in available if t in r.get("type", "").lower()]

        if not available:
            msg = f"No hay habitaciones disponibles"
            if room_type:
                msg += f" de tipo '{room_type}'"
            return msg + " en este momento."

        lines = ["=== HABITACIONES DISPONIBLES ==="]
        for r in available[:10]:
            num = r.get("number", "?")
            rtype = r.get("type", "?")
            floor = r.get("floor", "?")
            price = r.get("price", 0)
            lines.append(f"  Hab. {num} — {rtype} (Piso {floor}) — ${price:,.2f}/noche")

        if len(available) > 10:
            lines.append(f"  ... y {len(available) - 10} más disponibles.")

        return "\n".join(lines)

    async def check_room_status(self, room_number: str) -> str:
        data = await self._get("/api/rooms")
        if data is None:
            return "No se pudo consultar el estado de la habitación."

        rooms = data if isinstance(data, list) else data.get("rooms", [])
        for r in rooms:
            if str(r.get("number", "")).strip() == str(room_number).strip():
                status = r.get("status", "desconocido")
                guest = r.get("guest", r.get("currentGuest", ""))
                rtype = r.get("type", "")
                price = r.get("price", 0)
                pbx = r.get("pbx_status", "Idle")
                lines = [f"Habitación {room_number} ({rtype}):"]
                lines.append(f"  Estado: {status}")
                if guest:
                    lines.append(f"  Huésped: {guest}")
                lines.append(f"  Precio: ${price:,.2f}/noche")
                lines.append(f"  Estado telefónico: {pbx}")
                return "\n".join(lines)

        return f"No encontré la habitación {room_number} en el sistema."

    async def get_reservations(self, guest_name: str | None = None) -> str:
        """
        El PMS no tiene endpoint de reservas separado.
        Usamos /api/rooms para listar habitaciones ocupadas (status = Ocupada)
        filtrando por el nombre del huésped si se provee.
        """
        data = await self._get("/api/rooms")
        if data is None:
            return "No se pudo consultar las habitaciones en este momento."

        rooms = data if isinstance(data, list) else data.get("rooms", [])
        occupied = [r for r in rooms if r.get("status", "").lower() in ("ocupada", "ocupado", "occupied")]

        if guest_name:
            g = guest_name.lower()
            occupied = [
                r for r in occupied
                if g in r.get("guest", r.get("currentGuest", "")).lower()
            ]

        if not occupied:
            msg = "No se encontraron habitaciones ocupadas"
            if guest_name:
                msg += f" para '{guest_name}'"
            return msg + "."

        lines = ["=== HABITACIONES OCUPADAS ==="]
        for r in occupied[:10]:
            num = r.get("number", "?")
            rtype = r.get("type", "?")
            guest = r.get("guest", r.get("currentGuest", "Sin registro"))
            price = r.get("price", 0)
            lines.append(f"  Hab. {num} ({rtype}) | Huésped: {guest} | ${price:,.2f}/noche")

        return "\n".join(lines)

    async def create_reservation(self, guest_name: str, room_number: str,
                                  check_in: str, check_out: str,
                                  adults: int = 1) -> str:
        """
        El PMS gestiona ocupación actualizando el status de la habitación.
        Usamos PUT /api/rooms/{room_id} para marcarla como Ocupada con el huésped.
        """
        rooms_data = await self._get("/api/rooms")
        if rooms_data is None:
            return "No se pudo verificar disponibilidad de habitaciones."

        rooms = rooms_data if isinstance(rooms_data, list) else rooms_data.get("rooms", [])
        room = next((r for r in rooms if str(r.get("number", "")) == str(room_number)), None)
        if not room:
            return f"No encontré la habitación {room_number} en el sistema."

        if room.get("status", "").lower() not in ("disponible", "available", "libre"):
            return f"La habitación {room_number} no está disponible (Estado: {room.get('status', 'desconocido')})."

        room_id = room.get("id")
        update_body = {
            **room,
            "status": "Ocupada",
            "guest": guest_name,
            "currentGuest": guest_name,
        }
        update_body.pop("id", None)

        result = await self._put(f"/api/rooms/{room_id}", update_body)

        if result is None:
            return f"No se pudo registrar a {guest_name} en la habitación {room_number}."

        logger.info(f"PmsWorker: Habitación {room_number} asignada a '{guest_name}'")
        return (
            f"¡Habitación {room_number} asignada a {guest_name}! "
            f"Check-in: {check_in} | Check-out: {check_out}. "
            f"El registro quedó guardado en el sistema hotelero."
        )

    async def process(self, query: str, session=None) -> str:
        q = query.lower()

        if any(kw in q for kw in ["disponible", "libre", "desocupada", "hay habitacion", "tienes cuarto"]):
            room_type = None
            for rtype in ["suite", "doble", "estándar", "estandar", "familiar", "presidencial", "junior"]:
                if rtype in q:
                    room_type = rtype
                    break
            return await self.get_available_rooms(room_type)

        if any(kw in q for kw in ["estado", "estatus", "habitacion", "cuarto", "número", "numero"]):
            import re
            nums = re.findall(r'\b\d{1,4}\b', query)
            if nums:
                return await self.check_room_status(nums[0])

        if any(kw in q for kw in ["reserva", "reservacion", "booking", "reservado"]):
            return await self.get_reservations()

        return await self.get_available_rooms()

    async def test_connection(self) -> dict:
        ok = await self._authenticate()
        if ok:
            data = await self._get("/api/rooms")
            count = len(data) if isinstance(data, list) else len(data.get("rooms", [])) if data else 0
            return {"success": True, "message": f"Conexión al PMS exitosa. {count} habitaciones encontradas."}
        return {"success": False, "message": "No se pudo autenticar en el PMS. Verifica URL, usuario y contraseña."}


_pms_instances: dict[int, PmsWorker] = {}


def get_pms_worker(base_url: str, username: str, password: str, user_id: int | None = None) -> PmsWorker:
    key = user_id if user_id is not None else 0
    existing = _pms_instances.get(key)
    if (existing is None
            or existing.base_url != base_url.rstrip("/")
            or existing.username != username):
        _pms_instances[key] = PmsWorker(base_url, username, password)
    return _pms_instances[key]
