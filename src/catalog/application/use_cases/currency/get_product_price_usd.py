from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from catalog.application.dto.product import ProductPriceUsdDTO
from catalog.application.exceptions.catalog_exception import (
    CurrencyRateUnavailableError,
    ProductNotFoundError,
)
from catalog.application.repositories.uow import UnitOfWorkABC
from catalog.application.services.currency import CurrencyServiceABC


class GetProductPriceUsdUseCase:
    def __init__(self, uow: UnitOfWorkABC, currency_service: CurrencyServiceABC):
        self._uow = uow
        self._currency_service = currency_service

    async def __call__(self, product_id: UUID) -> ProductPriceUsdDTO:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(str(product_id))

        usd_rate = await self._currency_service.get_usd_rate()
        if usd_rate.rate <= 0:
            raise CurrencyRateUnavailableError()

        price_usd = (product.price / usd_rate.rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return ProductPriceUsdDTO(
            product_id=product.id,
            price_byn=product.price,
            price_usd=price_usd,
            rate=usd_rate.rate,
            rate_date=usd_rate.date,
        )