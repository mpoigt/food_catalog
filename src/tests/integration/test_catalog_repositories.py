import uuid
from datetime import datetime, timezone
from decimal import Decimal

from catalog.domain.entities.category import Category
from catalog.domain.entities.product import Product
from catalog.infrastructure.repositories.category_repository import (
    SQLAlchemyCategoryRepository,
)
from catalog.infrastructure.repositories.product_repository import (
    SQLAlchemyProductRepository,
)

_NOW = datetime.now(timezone.utc)


def _category(name: str) -> Category:
    return Category(id=uuid.uuid4(), name=name, created_at=_NOW, updated_at=_NOW)


def _product(category_id: uuid.UUID, **overrides) -> Product:
    data = dict(
        id=uuid.uuid4(),
        name="Селедка",
        category_id=category_id,
        description="Селедка соленая",
        price=Decimal("10.00"),
        note_common="Акция",
        note_special="Пересоленая",
        created_at=_NOW,
        updated_at=_NOW,
    )
    data.update(overrides)
    return Product(**data)


async def test_category_save_and_get(db_session):
    repo = SQLAlchemyCategoryRepository(db_session)
    cat = _category("Еда")

    saved = await repo.save(cat)
    assert saved.id == cat.id

    fetched = await repo.get_by_id(cat.id)
    assert fetched is not None
    assert fetched.name == "Еда"


async def test_category_is_name_exists(db_session):
    repo = SQLAlchemyCategoryRepository(db_session)
    await repo.save(_category("Вода"))

    assert await repo.is_name_exists("Вода") is True
    assert await repo.is_name_exists("Отсутствует") is False


async def test_category_update(db_session):
    repo = SQLAlchemyCategoryRepository(db_session)
    cat = _category("Едаа")
    await repo.save(cat)

    cat.name = "Еда"
    updated = await repo.update(cat)
    assert updated.name == "Еда"


async def test_category_list_all_ordered_by_name(db_session):
    repo = SQLAlchemyCategoryRepository(db_session)
    await repo.save(_category("Вода"))
    await repo.save(_category("Еда"))
    await repo.save(_category("Вкусности"))

    names = [c.name for c in await repo.list_all()]
    assert names == sorted(names)


async def test_product_save_get_update_delete(db_session):
    cat = await SQLAlchemyCategoryRepository(db_session).save(_category("Еда"))
    repo = SQLAlchemyProductRepository(db_session)
    product = _product(cat.id)

    saved = await repo.save(product)
    assert saved.price == Decimal("10.00")

    got = await repo.get_by_id(product.id)
    assert got is not None
    assert got.name == "Селедка"

    product.price = Decimal("12.00")
    updated = await repo.update(product)
    assert updated.price == Decimal("12.00")

    await repo.delete(product.id)
    assert await repo.get_by_id(product.id) is None


async def test_product_search_and_filter_by_category(db_session):
    cat_repo = SQLAlchemyCategoryRepository(db_session)
    food = await cat_repo.save(_category("Еда"))
    water = await cat_repo.save(_category("Вода"))
    repo = SQLAlchemyProductRepository(db_session)
    await repo.save(_product(food.id, name="Селедка", description="Селедка соленая"))
    await repo.save(_product(food.id, name="Тушенка", description="Тушенка говяжья"))
    await repo.save(_product(water.id, name="Квас", description="В бутылках"))

    _, total_all = await repo.list_products(
        page=1, limit=30, search=None, category_id=None, sort_by=None, order_by="asc"
    )
    assert total_all == 3

    found, total_found = await repo.list_products(
        page=1, limit=30, search="Тушен", category_id=None, sort_by=None, order_by="asc"
    )
    assert total_found == 1
    assert found[0].name == "Тушенка"

    _, total_food = await repo.list_products(
        page=1, limit=30, search=None, category_id=food.id, sort_by=None, order_by="asc"
    )
    assert total_food == 2


async def test_product_pagination(db_session):
    cat = await SQLAlchemyCategoryRepository(db_session).save(_category("Еда"))
    repo = SQLAlchemyProductRepository(db_session)
    for i in range(3):
        await repo.save(_product(cat.id, name=f"p{i}"))

    items, total = await repo.list_products(
        page=1, limit=2, search=None, category_id=None, sort_by="name", order_by="asc"
    )
    assert total == 3
    assert len(items) == 2


async def test_delete_by_category(db_session):
    cat = await SQLAlchemyCategoryRepository(db_session).save(_category("Еда"))
    repo = SQLAlchemyProductRepository(db_session)
    await repo.save(_product(cat.id))
    await repo.save(_product(cat.id))

    await repo.delete_by_category(cat.id)

    _, total = await repo.list_products(
        page=1, limit=30, search=None, category_id=cat.id, sort_by=None, order_by="asc"
    )
    assert total == 0


async def test_fk_cascade_deletes_products(db_session):
    cat_repo = SQLAlchemyCategoryRepository(db_session)
    cat = await cat_repo.save(_category("Еда"))
    prod_repo = SQLAlchemyProductRepository(db_session)
    product = _product(cat.id)
    await prod_repo.save(product)

    await cat_repo.delete(cat.id)
    db_session.expire_all()

    assert await prod_repo.get_by_id(product.id) is None
