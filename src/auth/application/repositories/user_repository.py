from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user import User


class UserRepositoryABC(ABC):
    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def is_email_exists(self, email: str) -> bool: ...

    @abstractmethod
    async def is_username_exists(self, username: str) -> bool: ...

    @abstractmethod
    async def list_users(
        self,
        page: int,
        limit: int,
        filters: dict,
        sort_by: str | None,
        order_by: str,
    ) -> tuple[list[User], int]: ...
