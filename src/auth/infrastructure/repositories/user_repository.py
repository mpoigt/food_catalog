from uuid import UUID

from sqlalchemy import delete, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.repositories.user_repository import UserRepositoryABC
from auth.domain.entities.user import User
from auth.infrastructure.db.models.user import UserDB


class SQLAlchemyUserRepository(UserRepositoryABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(orm: UserDB) -> User:
        return User(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            password_hash=orm.password_hash,
            role=orm.role,
            is_blocked=orm.is_blocked,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, user: User) -> User:
        orm = UserDB(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            is_blocked=user.is_blocked,
        )
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def update(self, user: User) -> User:
        orm = await self._session.get(UserDB, user.id)
        if orm is None:
            raise ValueError(f"User {user.id} not found")

        orm.username = user.username
        orm.email = user.email
        orm.password_hash = user.password_hash
        orm.role = user.role
        orm.is_blocked = user.is_blocked

        await self._session.flush()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def delete(self, user_id: UUID) -> None:
        await self._session.execute(delete(UserDB).where(UserDB.id == user_id))

    async def get_by_id(self, user_id: UUID) -> User | None:
        orm = await self._session.get(UserDB, user_id)
        return self._to_domain(orm) if orm else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserDB).where(UserDB.email == email)
        )
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(UserDB).where(UserDB.username == username)
        )
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def is_email_exists(self, email: str) -> bool:
        result = await self._session.execute(
            select(exists().where(UserDB.email == email))
        )
        return bool(result.scalar())

    async def is_username_exists(self, username: str) -> bool:
        result = await self._session.execute(
            select(exists().where(UserDB.username == username))
        )
        return bool(result.scalar())

    async def list_users(
        self,
        page: int,
        limit: int,
        filters: dict,
        sort_by: str | None,
        order_by: str,
    ) -> tuple[list[User], int]:
        query = select(UserDB)

        for key, value in filters.items():
            if hasattr(UserDB, key):
                query = query.where(getattr(UserDB, key) == value)

        if sort_by and hasattr(UserDB, sort_by):
            field = getattr(UserDB, sort_by)
            query = query.order_by(field.desc() if order_by == "desc" else field.asc())

        total = await self._session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset((page - 1) * limit).limit(limit)
        result = await self._session.execute(query)
        users = [self._to_domain(orm) for orm in result.scalars().all()]

        return users, total or 0
