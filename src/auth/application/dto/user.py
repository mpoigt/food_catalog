from dataclasses import dataclass
from uuid import UUID

from auth.domain.entities.user import User
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

    @classmethod
    def from_entity(cls, user: User) -> "UserResponseDTO":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_blocked=user.is_blocked,
        )


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
