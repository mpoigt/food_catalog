from abc import ABC, abstractmethod
from uuid import UUID

from catalog.domain.entities.category import Category


class CategoryRepositoryABC(ABC):
    @abstractmethod
    async def save(self, category: Category) -> Category: ...

    @abstractmethod
    async def update(self, category: Category) -> Category: ...

    @abstractmethod
    async def delete(self, category_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category | None: ...

    @abstractmethod
    async def is_name_exists(self, name: str) -> bool: ...

    @abstractmethod
    async def list_all(self) -> list[Category]: ...
