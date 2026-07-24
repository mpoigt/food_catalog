from catalog.application.exceptions.catalog_exception import (
    CurrencyRateUnavailableError,
)
from catalog.application.services.currency import CurrencyServiceABC, UsdRate


class GetUsdRateUseCase:
    def __init__(self, currency_service: CurrencyServiceABC):
        self._currency_service = currency_service

    async def __call__(self) -> UsdRate:
        rate = await self._currency_service.get_usd_rate()
        if rate.rate <= 0:
            raise CurrencyRateUnavailableError()
        return rate
