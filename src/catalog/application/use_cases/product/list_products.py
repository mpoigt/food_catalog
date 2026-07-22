from uuid import UUID

from catalog.application.dto.product import ProductResponseDTO
from catalog.application.repositories.uow import UnitOfWorkABC


class ListProductsUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(
        self,
        page: int = 1,
        limit: int = 30,
        search: str | None = None,
        category_id: UUID | None = None,
        sort_by: str | None = None,
        order_by: str = "asc",
    ) -> tuple[list[ProductResponseDTO], int]:
        async with self._uow as uow:
            products, total = await uow.products.list_products(
                page=page,
                limit=limit,
                search=search,
                category_id=category_id,
                sort_by=sort_by,
                order_by=order_by,
            )

        return [ProductResponseDTO.from_entity(product) for product in products], total