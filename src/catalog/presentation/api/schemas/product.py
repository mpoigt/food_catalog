from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category_id: UUID
    description: str = Field(min_length=1, max_length=1000)
    price: Decimal = Field(ge=0)
    note_common: str | None = Field(default=None, max_length=255)
    note_special: str | None = Field(default=None, max_length=255)


class ProductUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    category_id: UUID | None = None
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    price: Decimal | None = Field(default=None, ge=0)
    note_common: str | None = Field(default=None, max_length=255)
    note_special: str | None = Field(default=None, max_length=255)


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category_id: UUID
    category_name: str
    description: str
    price: Decimal
    note_common: str | None
    note_special: str | None
    image_url: str | None = None


class PaginatedProductsSchema(BaseModel):
    total: int
    page: int
    limit: int
    items: list[ProductResponseSchema]


class ProductPriceUsdSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    price_byn: Decimal
    price_usd: Decimal
    rate: Decimal
    rate_date: str