import datetime
import uuid
from decimal import Decimal

import pytest

from catalog.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO
from catalog.application.dto.product import ProductCreateDTO, ProductUpdateDTO
from catalog.application.exceptions.catalog_exception import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    CurrencyRateUnavailableError,
    ProductNotFoundError,
)
from catalog.application.repositories.product_repository import ProductListItem
from catalog.application.services.currency import UsdRate
from catalog.application.use_cases.category.create_category import CreateCategoryUseCase
from catalog.application.use_cases.category.delete_category import DeleteCategoryUseCase
from catalog.application.use_cases.category.update_category import UpdateCategoryUseCase
from catalog.application.use_cases.currency.get_product_price_usd import (
    GetProductPriceUsdUseCase,
)
from catalog.application.use_cases.product.create_product import CreateProductUseCase
from catalog.application.use_cases.product.update_product import UpdateProductUseCase
from catalog.domain.entities.category import Category
from catalog.domain.entities.product import Product

_NOW = datetime.datetime.now(datetime.UTC)


def _category(name: str = "Еда") -> Category:
    return Category(id=uuid.uuid4(), name=name, created_at=_NOW, updated_at=_NOW)


def _product(category_id: uuid.UUID, **overrides) -> Product:
    data = {
        "id": uuid.uuid4(),
        "name": "Селедка",
        "category_id": category_id,
        "description": "Селедка соленая",
        "price": Decimal("10.00"),
        "note_common": "Акция",
        "note_special": "Пересоленая",
        "image_path": None,
        "created_at": _NOW,
        "updated_at": _NOW,
    }
    data.update(overrides)
    return Product(**data)


class _FakeCategoryRepo:
    def __init__(self):
        self.items: dict[uuid.UUID, Category] = {}

    async def save(self, category):
        self.items[category.id] = category
        return category

    async def update(self, category):
        self.items[category.id] = category
        return category

    async def delete(self, category_id):
        self.items.pop(category_id, None)

    async def get_by_id(self, category_id):
        return self.items.get(category_id)

    async def is_name_exists(self, name):
        return any(c.name == name for c in self.items.values())

    async def list_all(self):
        return list(self.items.values())


class _FakeProductRepo:
    def __init__(self):
        self.items: dict[uuid.UUID, Product] = {}
        self.cascade_calls: list[uuid.UUID] = []

    async def save(self, product):
        self.items[product.id] = product
        return product

    async def update(self, product):
        self.items[product.id] = product
        return product

    async def delete(self, product_id):
        self.items.pop(product_id, None)

    async def delete_by_category(self, category_id):
        self.cascade_calls.append(category_id)
        for pid in [p.id for p in self.items.values() if p.category_id == category_id]:
            self.items.pop(pid)

    async def get_by_id(self, product_id):
        return self.items.get(product_id)

    async def list_products(self, **kwargs):
        items = [
            ProductListItem(product=product, category_name="")
            for product in self.items.values()
        ]
        return items, len(items)


class _FakeUow:
    def __init__(self, categories=None, products=None):
        self.categories = categories or _FakeCategoryRepo()
        self.products = products or _FakeProductRepo()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def commit(self):
        ...

    async def rollback(self):
        ...


class _FakeCurrency:
    def __init__(self, rate):
        self._rate = rate

    async def get_usd_rate(self):
        return UsdRate(rate=self._rate, date="2026-07-22")


async def test_create_category_success():
    uow = _FakeUow()
    dto = await CreateCategoryUseCase(uow)(CategoryCreateDTO(name="Вода"))
    assert dto.name == "Вода"
    assert len(uow.categories.items) == 1


async def test_create_category_duplicate_raises():
    repo = _FakeCategoryRepo()
    await repo.save(_category("Еда"))
    uow = _FakeUow(categories=repo)
    with pytest.raises(CategoryAlreadyExistsError):
        await CreateCategoryUseCase(uow)(CategoryCreateDTO(name="Еда"))


async def test_update_category_not_found_raises():
    uow = _FakeUow()
    with pytest.raises(CategoryNotFoundError):
        await UpdateCategoryUseCase(uow)(uuid.uuid4(), CategoryUpdateDTO(name="X"))


async def test_delete_category_cascades_products():
    cat = _category("Еда")
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    prod_repo = _FakeProductRepo()
    await prod_repo.save(_product(cat.id))
    await prod_repo.save(_product(cat.id))
    uow = _FakeUow(categories=cat_repo, products=prod_repo)

    await DeleteCategoryUseCase(uow)(cat.id)

    assert cat.id in prod_repo.cascade_calls
    assert prod_repo.items == {}
    assert cat_repo.items == {}


async def test_delete_category_not_found_raises():
    uow = _FakeUow()
    with pytest.raises(CategoryNotFoundError):
        await DeleteCategoryUseCase(uow)(uuid.uuid4())


async def test_create_product_unknown_category_raises():
    uow = _FakeUow()
    data = ProductCreateDTO(
        name="Квас",
        category_id=uuid.uuid4(),
        description="В бутылках",
        price=Decimal("15.00"),
    )
    with pytest.raises(CategoryNotFoundError):
        await CreateProductUseCase(uow)(data)


async def test_create_product_success():
    cat = _category("Вода")
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    uow = _FakeUow(categories=cat_repo)

    dto = await CreateProductUseCase(uow)(
        ProductCreateDTO(
            name="Квас",
            category_id=cat.id,
            description="В бутылках",
            price=Decimal("15.00"),
            note_common="Вятский",
            note_special="Теплый",
        )
    )
    assert dto.name == "Квас"
    assert dto.note_special == "Теплый"
    assert len(uow.products.items) == 1


async def test_update_product_changes_only_provided_fields():
    cat = _category()
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    prod_repo = _FakeProductRepo()
    product = _product(cat.id, name="Селедка", price=Decimal("10.00"))
    await prod_repo.save(product)
    uow = _FakeUow(categories=cat_repo, products=prod_repo)

    dto = await UpdateProductUseCase(uow)(
        product.id, ProductUpdateDTO(price=Decimal("12.50"))
    )
    assert dto.price == Decimal("12.50")
    assert dto.name == "Селедка"


async def test_update_product_unknown_new_category_raises():
    cat = _category()
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    prod_repo = _FakeProductRepo()
    product = _product(cat.id)
    await prod_repo.save(product)
    uow = _FakeUow(categories=cat_repo, products=prod_repo)

    with pytest.raises(CategoryNotFoundError):
        await UpdateProductUseCase(uow)(
            product.id, ProductUpdateDTO(category_id=uuid.uuid4())
        )


async def test_get_product_price_usd_conversion():
    cat = _category()
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    prod_repo = _FakeProductRepo()
    product = _product(cat.id, price=Decimal("30.00"))
    await prod_repo.save(product)
    uow = _FakeUow(categories=cat_repo, products=prod_repo)

    dto = await GetProductPriceUsdUseCase(uow, _FakeCurrency(Decimal("3.00")))(product.id)
    assert dto.price_byn == Decimal("30.00")
    assert dto.price_usd == Decimal("10.00")
    assert dto.rate == Decimal("3.00")


async def test_get_product_price_usd_zero_rate_raises():
    cat = _category()
    cat_repo = _FakeCategoryRepo()
    await cat_repo.save(cat)
    prod_repo = _FakeProductRepo()
    product = _product(cat.id)
    await prod_repo.save(product)
    uow = _FakeUow(categories=cat_repo, products=prod_repo)

    with pytest.raises(CurrencyRateUnavailableError):
        await GetProductPriceUsdUseCase(uow, _FakeCurrency(Decimal(0)))(product.id)


async def test_get_product_price_usd_product_not_found_raises():
    uow = _FakeUow()
    with pytest.raises(ProductNotFoundError):
        await GetProductPriceUsdUseCase(uow, _FakeCurrency(Decimal("3.00")))(uuid.uuid4())
