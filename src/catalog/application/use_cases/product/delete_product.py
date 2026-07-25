import logging
from uuid import UUID

from catalog.application.exceptions.catalog_exception import ProductNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("catalog")


class DeleteProductUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, product_id: UUID) -> None:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundError(str(product_id))

            await uow.products.delete(product_id)

        logger.info("product_deleted", extra={"product_id": str(product_id)})