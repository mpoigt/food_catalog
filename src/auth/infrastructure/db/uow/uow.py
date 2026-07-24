from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.repositories.uow import UnitOfWorkABC
from auth.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from core.db.uow import BaseUnitOfWork


class AuthUnitOfWork(BaseUnitOfWork, UnitOfWorkABC):
    def _init_repositories(self, session: AsyncSession) -> None:
        self.users = SQLAlchemyUserRepository(session)