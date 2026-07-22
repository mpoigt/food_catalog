from abc import ABC, abstractmethod
from uuid import UUID

from catalog.domain.entities.product import Product


class ProductRepositoryABC(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product: ...

    @abstractmethod
    async def update(self, product: Product) -> Product: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    async def delete_by_category(self, category_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def list_products(
        self,
        page: int,
        limit: int,
        search: str | None,
        category_id: UUID | None,
        sort_by: str | None,
        order_by: str,
    ) -> tuple[list[Product], int]: ...
