from abc import ABC, abstractmethod

from auth.application.repositories.user_repository import UserRepositoryABC


class UnitOfWorkABC(ABC):
    users: UserRepositoryABC

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkABC": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, traceback) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...