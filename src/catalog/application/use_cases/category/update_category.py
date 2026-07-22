import logging
from uuid import UUID

from catalog.application.dto.category import CategoryResponseDTO, CategoryUpdateDTO
from catalog.application.exceptions.catalog_exception import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
)
from catalog.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("catalog")


class UpdateCategoryUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(
        self, category_id: UUID, data: CategoryUpdateDTO
    ) -> CategoryResponseDTO:
        async with self._uow as uow:
            category = await uow.categories.get_by_id(category_id)
            if category is None:
                raise CategoryNotFoundError(str(category_id))

            if data.name is not None and data.name != category.name:
                if await uow.categories.is_name_exists(data.name):
                    raise CategoryAlreadyExistsError(data.name)
                category.name = data.name

            updated = await uow.categories.update(category)

        logger.info("category_updated", extra={"category_id": str(updated.id)})
        return CategoryResponseDTO.from_entity(updated)