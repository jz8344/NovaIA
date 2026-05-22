import asyncio
import json
import os
import aiohttp
from loguru import logger
from config.settings import get_settings

EXCHANGE_RATES_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "exchange_rates.json"
)

FALLBACK_RATES = {
    "USD": 1.0,
    "MXN": 17.37,
    "ARS": 900.0,
    "BOB": 6.91,
    "GBP": 0.79,
    "RUB": 90.0,
    "CNY": 7.24,
    "KRW": 1360.0
}

class ExchangeRateUpdater:
    def __init__(self):
        self._task = None
        self._running = False
        settings = get_settings()
        self._fallback_mxn = settings.usd_exchange_rate

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run_loop())
            logger.info("Servicio de actualización de divisas iniciado.")

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            logger.info("Servicio de actualización de divisas detenido.")

    async def _run_loop(self):
        while self._running:
            await self.update_rates()
            try:
                await asyncio.sleep(2 * 3600)
            except asyncio.CancelledError:
                break

    async def update_rates(self):
        url = "https://open.er-api.com/v6/latest/USD"
        rates_data = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates = data.get("rates", {})
                        
                        target_currencies = ["USD", "MXN", "ARS", "BOB", "GBP", "RUB", "CNY", "KRW"]
                        for currency in target_currencies:
                            if currency in rates:
                                rates_data[currency] = float(rates[currency])
                            else:
                                rates_data[currency] = FALLBACK_RATES[currency]
                                
                        if "MXN" not in rates_data or rates_data["MXN"] <= 0:
                            rates_data["MXN"] = self._fallback_mxn

                        os.makedirs(os.path.dirname(EXCHANGE_RATES_FILE), exist_ok=True)
                        with open(EXCHANGE_RATES_FILE, "w", encoding="utf-8") as f:
                            json.dump(rates_data, f, indent=4)
                        logger.info(f"Tipos de cambio actualizados en JSON: MXN={rates_data.get('MXN')}")
                        return
                    else:
                        logger.warning(f"Error de API de divisas, status: {response.status}")
        except Exception as e:
            logger.error(f"Error actualizando divisas: {e}")

        if not os.path.exists(EXCHANGE_RATES_FILE):
            fallback = FALLBACK_RATES.copy()
            fallback["MXN"] = self._fallback_mxn
            os.makedirs(os.path.dirname(EXCHANGE_RATES_FILE), exist_ok=True)
            with open(EXCHANGE_RATES_FILE, "w", encoding="utf-8") as f:
                json.dump(fallback, f, indent=4)
            logger.info("Valores por defecto de divisas escritos por fallo de API.")
