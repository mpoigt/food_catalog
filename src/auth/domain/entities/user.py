from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.enums.role import Role


@dataclass
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    role: Role
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
