from uuid import UUID

from catalog.application.dto.category import CategoryResponseDTO
from catalog.application.exceptions.catalog_exception import CategoryNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC


class GetCategoryUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, category_id: UUID) -> CategoryResponseDTO:
        async with self._uow as uow:
            category = await uow.categories.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(str(category_id))
        return CategoryResponseDTO.from_entity(category)