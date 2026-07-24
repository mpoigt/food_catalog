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

            if data.category_id is not None and data.category_id != product.category_id:
                if await uow.categories.get_by_id(data.category_id) is None:
                    raise CategoryNotFoundError(str(data.category_id))
                product.category_id = data.category_id

            if data.name is not None:
                product.name = data.name
            if data.description is not None:
                product.description = data.description
            if data.price is not None:
                product.price = data.price
            if data.note_common is not None:
                product.note_common = data.note_common
            if data.note_special is not None:
                product.note_special = data.note_special

            updated = await uow.products.update(product)
            category = await uow.categories.get_by_id(updated.category_id)

        logger.info("product_updated", extra={"product_id": str(updated.id)})
        return ProductResponseDTO.from_entity(
            updated, category.name if category else ""
        )