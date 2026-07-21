from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.repositories.uow import UnitOfWorkABC
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository


class UnitOfWork(UnitOfWorkABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.users = SQLAlchemyUserRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self._session is not None:
                await self._session.close()
            self._session = None

    async def commit(self) -> None:
        if self._session is not None:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session is not None:
            await self._session.rollback()
