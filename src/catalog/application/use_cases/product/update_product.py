import logging
from uuid import UUID

from catalog.application.dto.product import ProductResponseDTO, ProductUpdateDTO
from catalog.application.exceptions.catalog_exception import (
    CategoryNotFoundError,
    ProductNotFoundError,
)
from catalog.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("catalog")


class UpdateProductUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(
        self, product_id: UUID, data: ProductUpdateDTO
    ) -> ProductResponseDTO:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundError(str(product_id))

            changes = {key: value for key, value in vars(data).items() if value is not None}

            new_category_id = changes.get("category_id")
            if new_category_id is not None and new_category_id != product.category_id:
                if await uow.categories.get_by_id(new_category_id) is None:
                    raise CategoryNotFoundError(str(new_category_id))

            for field, value in changes.items():
                setattr(product, field, value)

            updated = await uow.products.update(product)

        logger.info("product_updated", extra={"product_id": str(updated.id)})
        return ProductResponseDTO.from_entity(updated)