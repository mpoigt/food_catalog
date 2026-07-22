from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from catalog.domain.entities.product import Product


@dataclass
class ProductCreateDTO:
    name: str
    category_id: UUID
    description: str
    price: Decimal
    note_common: str | None = None
    note_special: str | None = None


@dataclass
class ProductUpdateDTO:
    name: str | None = None
    category_id: UUID | None = None
    description: str | None = None
    price: Decimal | None = None
    note_common: str | None = None
    note_special: str | None = None


@dataclass
class ProductResponseDTO:
    id: UUID
    name: str
    category_id: UUID
    description: str
    price: Decimal
    note_common: str | None
    note_special: str | None

    @classmethod
    def from_entity(cls, product: Product) -> "ProductResponseDTO":
        return cls(
            id=product.id,
            name=product.name,
            category_id=product.category_id,
            description=product.description,
            price=product.price,
            note_common=product.note_common,
            note_special=product.note_special,
        )


@dataclass
class ProductPriceUsdDTO:
    product_id: UUID
    price_byn: Decimal
    price_usd: Decimal
    rate: Decimal
    rate_date: str