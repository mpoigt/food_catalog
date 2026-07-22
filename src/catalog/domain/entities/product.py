from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class Product:
    id: UUID
    name: str
    category_id: UUID
    description: str
    price: Decimal
    note_common: str | None
    note_special: str | None
    created_at: datetime
    updated_at: datetime