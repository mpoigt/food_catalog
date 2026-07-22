from abc import ABC, abstractmethod

from catalog.application.repositories.category_repository import CategoryRepositoryABC
from catalog.application.repositories.product_repository import ProductRepositoryABC


class UnitOfWorkABC(ABC):
    categories: CategoryRepositoryABC
    products: ProductRepositoryABC

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkABC": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, traceback) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...