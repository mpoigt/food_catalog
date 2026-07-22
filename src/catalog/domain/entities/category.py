from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Category:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime