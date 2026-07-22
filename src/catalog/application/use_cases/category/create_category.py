import datetime
import logging
from uuid import uuid4

from catalog.application.dto.category import CategoryCreateDTO, CategoryResponseDTO
from catalog.application.exceptions.catalog_exception import CategoryAlreadyExistsError
from catalog.application.repositories.uow import UnitOfWorkABC
from catalog.domain.entities.category import Category

logger = logging.getLogger("catalog")


class CreateCategoryUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, data: CategoryCreateDTO) -> CategoryResponseDTO:
        async with self._uow as uow:
            if await uow.categories.is_name_exists(data.name):
                raise CategoryAlreadyExistsError(data.name)

            now = datetime.datetime.now(datetime.timezone.utc)
            category = Category(
                id=uuid4(),
                name=data.name,
                created_at=now,
                updated_at=now,
            )
            saved = await uow.categories.save(category)

        logger.info("category_created", extra={"category_id": str(saved.id)})
        return CategoryResponseDTO.from_entity(saved)