from uuid import UUID

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.application.repositories.category_repository import CategoryRepositoryABC
from catalog.domain.entities.category import Category
from catalog.infrastructure.db.models.category import CategoryDB


class SQLAlchemyCategoryRepository(CategoryRepositoryABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(orm: CategoryDB) -> Category:
        return Category(
            id=orm.id,
            name=orm.name,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, category: Category) -> Category:
        orm = CategoryDB(id=category.id, name=category.name)
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def update(self, category: Category) -> Category:
        orm = await self._session.get(CategoryDB, category.id)
        if orm is None:
            raise ValueError(f"Category {category.id} not found")

        orm.name = category.name

        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def delete(self, category_id: UUID) -> None:
        await self._session.execute(delete(CategoryDB).where(CategoryDB.id == category_id))

    async def get_by_id(self, category_id: UUID) -> Category | None:
        orm = await self._session.get(CategoryDB, category_id)
        return self._to_domain(orm) if orm else None

    async def is_name_exists(self, name: str) -> bool:
        result = await self._session.execute(
            select(exists().where(CategoryDB.name == name))
        )
        return bool(result.scalar())

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(
            select(CategoryDB).order_by(CategoryDB.name.asc())
        )
        return [self._to_domain(orm) for orm in result.scalars().all()]
