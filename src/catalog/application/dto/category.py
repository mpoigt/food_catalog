from dataclasses import dataclass
from uuid import UUID

from catalog.domain.entities.category import Category


@dataclass
class CategoryCreateDTO:
    name: str


@dataclass
class CategoryUpdateDTO:
    name: str | None = None


@dataclass
class CategoryResponseDTO:
    id: UUID
    name: str

    @classmethod
    def from_entity(cls, category: Category) -> "CategoryResponseDTO":
        return cls(id=category.id, name=category.name)