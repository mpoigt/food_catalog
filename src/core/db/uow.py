from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class BaseUnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    def _init_repositories(self, session: AsyncSession) -> None: ...

    async def __aenter__(self):
        self._session = self._session_factory()
        self._init_repositories(self._session)
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