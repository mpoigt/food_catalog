from sqlalchemy.ext.asyncio import AsyncSession

from core.db.uow import BaseUnitOfWork

from catalog.application.repositories.uow import UnitOfWorkABC
from catalog.infrastructure.repositories.category_repository import (
    SQLAlchemyCategoryRepository,
)
from catalog.infrastructure.repositories.product_repository import (
    SQLAlchemyProductRepository,
)


class CatalogUnitOfWork(BaseUnitOfWork, UnitOfWorkABC):
    def _init_repositories(self, session: AsyncSession) -> None:
        self.categories = SQLAlchemyCategoryRepository(session)
        self.products = SQLAlchemyProductRepository(session)