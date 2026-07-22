from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class CategoryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str