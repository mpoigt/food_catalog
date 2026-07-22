from dataclasses import dataclass
from uuid import UUID

from auth.domain.enums.role import Role


@dataclass
class UserCreateDTO:
    username: str
    email: str
    password: str
    role: Role


@dataclass
class UserResponseDTO:
    id: UUID
    username: str
    email: str
    role: Role
    is_blocked: bool


@dataclass
class UserUpdateAdminDTO:
    username: str | None = None
    email: str | None = None
    role: Role | None = None
    is_blocked: bool | None = None
    password: str | None = None


@dataclass
class CurrentUserDTO:
    id: UUID
    username: str
    email: str
    role: Role
