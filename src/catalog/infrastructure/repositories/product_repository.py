from uuid import UUID

from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.application.repositories.product_repository import (
    ProductListItem,
    ProductRepositoryABC,
)
from catalog.domain.entities.product import Product
from catalog.infrastructure.db.models.category import CategoryDB
from catalog.infrastructure.db.models.product import ProductDB

SORTABLE_FIELDS = frozenset({"name", "price", "created_at", "updated_at"})


class SQLAlchemyProductRepository(ProductRepositoryABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(orm: ProductDB) -> Product:
        return Product(
            id=orm.id,
            name=orm.name,
            category_id=orm.category_id,
            description=orm.description,
            price=orm.price,
            note_common=orm.note_common,
            note_special=orm.note_special,
            image_path=orm.image_path,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, product: Product) -> Product:
        orm = ProductDB(
            id=product.id,
            name=product.name,
            category_id=product.category_id,
            description=product.description,
            price=product.price,
            note_common=product.note_common,
            note_special=product.note_special,
            image_path=product.image_path,
        )
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def update(self, product: Product) -> Product:
        orm = await self._session.get(ProductDB, product.id)
        if orm is None:
            raise ValueError(f"Product {product.id} not found")

        orm.name = product.name
        orm.category_id = product.category_id
        orm.description = product.description
        orm.price = product.price
        orm.note_common = product.note_common
        orm.note_special = product.note_special
        orm.image_path = product.image_path

        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def delete(self, product_id: UUID) -> None:
        await self._session.execute(delete(ProductDB).where(ProductDB.id == product_id))

    async def delete_by_category(self, category_id: UUID) -> None:
        await self._session.execute(
            delete(ProductDB).where(ProductDB.category_id == category_id)
        )

    async def get_by_id(self, product_id: UUID) -> Product | None:
        orm = await self._session.get(ProductDB, product_id)
        return self._to_domain(orm) if orm else None

    async def list_products(
        self,
        page: int,
        limit: int,
        search: str | None,
        category_id: UUID | None,
        sort_by: str | None,
        order_by: str,
    ) -> tuple[list[ProductListItem], int]:
        query = select(ProductDB, CategoryDB.name).join(
            CategoryDB, ProductDB.category_id == CategoryDB.id
        )

        if category_id is not None:
            query = query.where(ProductDB.category_id == category_id)

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    ProductDB.name.ilike(pattern),
                    ProductDB.description.ilike(pattern),
                )
            )

        total = await self._session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        if sort_by in SORTABLE_FIELDS:
            field = getattr(ProductDB, sort_by)
            query = query.order_by(field.desc() if order_by == "desc" else field.asc())
        else:
            query = query.order_by(ProductDB.created_at.desc())

        query = query.offset((page - 1) * limit).limit(limit)
        result = await self._session.execute(query)
        items = [
            ProductListItem(product=self._to_domain(orm), category_name=name)
            for orm, name in result.all()
        ]

        return items, total or 0
