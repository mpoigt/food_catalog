from catalog.application.dto.category import CategoryResponseDTO
from catalog.application.repositories.uow import UnitOfWorkABC


class ListCategoriesUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self) -> list[CategoryResponseDTO]:
        async with self._uow as uow:
            categories = await uow.categories.list_all()

        return [CategoryResponseDTO.from_entity(category) for category in categories]