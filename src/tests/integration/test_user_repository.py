import datetime
import uuid

from domain.entities.user import User
from domain.enums.role import Role
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository


def _user(**overrides) -> User:
    now = datetime.datetime.now(datetime.timezone.utc)
    data = dict(
        id=uuid.uuid4(),
        username="user",
        email="user@example.com",
        password_hash="hash",
        role=Role.USER,
        is_blocked=False,
        created_at=now,
        updated_at=now,
    )
    data.update(overrides)
    return User(**data)


async def test_save_and_get_by_email(db_session):
    repo = SQLAlchemyUserRepository(db_session)
    user = _user(username="a", email="a@example.com")

    saved = await repo.save(user)
    assert saved.id == user.id

    fetched = await repo.get_by_email("a@example.com")
    assert fetched is not None
    assert fetched.username == "a"


async def test_is_email_exists(db_session):
    repo = SQLAlchemyUserRepository(db_session)
    await repo.save(_user(username="b", email="b@example.com"))

    assert await repo.is_email_exists("b@example.com") is True
    assert await repo.is_email_exists("missing@example.com") is False


async def test_update_changes_fields(db_session):
    repo = SQLAlchemyUserRepository(db_session)
    user = _user(username="c", email="c@example.com")
    await repo.save(user)

    user.role = Role.ADMIN
    user.is_blocked = True
    updated = await repo.update(user)

    assert updated.role == Role.ADMIN
    assert updated.is_blocked is True


async def test_delete_removes_user(db_session):
    repo = SQLAlchemyUserRepository(db_session)
    user = _user(username="d", email="d@example.com")
    await repo.save(user)

    await repo.delete(user.id)
    assert await repo.get_by_id(user.id) is None


async def test_list_users_pagination(db_session):
    repo = SQLAlchemyUserRepository(db_session)
    for i in range(3):
        await repo.save(_user(username=f"u{i}", email=f"u{i}@example.com"))

    users, total = await repo.list_users(
        page=1, limit=2, filters={}, sort_by="username", order_by="asc"
    )
    assert total == 3
    assert len(users) == 2
