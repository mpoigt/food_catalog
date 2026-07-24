from uuid import UUID

from catalog.application.dto.product import ProductResponseDTO
from catalog.application.exceptions.catalog_exception import ProductNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC


class GetProductUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, product_id: UUID) -> ProductResponseDTO:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundError(str(product_id))
            category = await uow.categories.get_by_id(product.category_id)

        return ProductResponseDTO.from_entity(
            product, category.name if category else ""
        )