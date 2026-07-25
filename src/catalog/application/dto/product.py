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
class ProductImageDTO:
    content: bytes
    extension: str


@dataclass
class ProductResponseDTO:
    id: UUID
    name: str
    category_id: UUID
    category_name: str
    description: str
    price: Decimal
    note_common: str | None
    note_special: str | None
    image_path: str | None

    @classmethod
    def from_entity(cls, product: Product, category_name: str) -> "ProductResponseDTO":
        return cls(
            id=product.id,
            name=product.name,
            category_id=product.category_id,
            category_name=category_name,
            description=product.description,
            price=product.price,
            note_common=product.note_common,
            note_special=product.note_special,
            image_path=product.image_path,
        )


@dataclass
class ProductPriceUsdDTO:
    product_id: UUID
    price_byn: Decimal
    price_usd: Decimal
    rate: Decimal
    rate_date: str
