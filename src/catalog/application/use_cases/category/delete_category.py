import logging
from uuid import UUID

from catalog.application.exceptions.catalog_exception import CategoryNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("catalog")


class DeleteCategoryUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, category_id: UUID) -> None:
        async with self._uow as uow:
            category = await uow.categories.get_by_id(category_id)
            if category is None:
                raise CategoryNotFoundError(str(category_id))

            await uow.products.delete_by_category(category_id)
            await uow.categories.delete(category_id)

        logger.info("category_deleted", extra={"category_id": str(category_id)})