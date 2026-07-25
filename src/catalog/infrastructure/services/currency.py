import json
from datetime import UTC, datetime
from decimal import Decimal

import httpx

from catalog.application.exceptions.catalog_exception import (
    CurrencyRateUnavailableError,
)
from catalog.application.services.cache import CacheServiceABC
from catalog.application.services.currency import CurrencyServiceABC, UsdRate

_NBRB_USD_URL = "https://api.nbrb.by/exrates/rates/USD"
_CACHE_TTL_SECONDS = 86400


class NBRBCurrencyService(CurrencyServiceABC):
    def __init__(self, cache: CacheServiceABC):
        self._cache = cache

    async def get_usd_rate(self) -> UsdRate:
        key = f"catalog:nbrb:usd:{datetime.now(UTC).date().isoformat()}"

        cached = await self._cache.get(key)
        if cached:
            data = json.loads(cached)
            return UsdRate(rate=Decimal(data["rate"]), date=data["date"])

        rate = await self._fetch_rate()
        await self._cache.set(
            key,
            json.dumps({"rate": str(rate.rate), "date": rate.date}),
            _CACHE_TTL_SECONDS,
        )
        return rate

    @staticmethod
    async def _fetch_rate() -> UsdRate:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(_NBRB_USD_URL, params={"parammode": 2})
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            raise CurrencyRateUnavailableError() from exc

        return UsdRate(
            rate=Decimal(str(payload["Cur_OfficialRate"])),
            date=str(payload["Date"])[:10],
        )