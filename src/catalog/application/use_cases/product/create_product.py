import datetime
import logging
from uuid import uuid4

from catalog.application.dto.product import ProductCreateDTO, ProductResponseDTO
from catalog.application.exceptions.catalog_exception import CategoryNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC
from catalog.domain.entities.product import Product

logger = logging.getLogger("catalog")


class CreateProductUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, data: ProductCreateDTO) -> ProductResponseDTO:
        async with self._uow as uow:
            if await uow.categories.get_by_id(data.category_id) is None:
                raise CategoryNotFoundError(str(data.category_id))

            now = datetime.datetime.now(datetime.timezone.utc)
            product = Product(
                id=uuid4(),
                name=data.name,
                category_id=data.category_id,
                description=data.description,
                price=data.price,
                note_common=data.note_common,
                note_special=data.note_special,
                created_at=now,
                updated_at=now,
            )
            saved = await uow.products.save(product)

        logger.info("product_created", extra={"product_id": str(saved.id)})
        return ProductResponseDTO.from_entity(saved)