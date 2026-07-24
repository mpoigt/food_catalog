import uuid
from types import SimpleNamespace

import pytest

from auth.application.exceptions.user_exception import (
    InvalidPasswordError,
    UserBlockedError,
    UserNotFoundError,
)
from auth.application.use_cases.user.login_user import LoginUserUseCase
from auth.domain.entities.user import User
from auth.domain.enums.role import Role


class _FakeUsers:
    def __init__(self, user):
        self._user = user

    async def get_by_email(self, email):
        return self._user


class _FakeUow:
    def __init__(self, user):
        self.users = _FakeUsers(user)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False


class _FakeHasher:
    def __init__(self, ok):
        self._ok = ok

    def verify(self, plain, hashed):
        return self._ok


class _FakeToken:
    def generate_token(self, data, expires):
        return f"token-{data['token_type']}"


def _settings():
    return SimpleNamespace(access_token_expire=15, refresh_token_expire=10080)


def _user(**overrides):
    data = {
        "id": uuid.uuid4(),
        "username": "user",
        "email": "user@example.com",
        "password_hash": "hash",
        "role": Role.USER,
        "is_blocked": False,
        "created_at": None,
        "updated_at": None,
    }
    data.update(overrides)
    return User(**data)


async def test_login_success_returns_typed_token_pair():
    use_case = LoginUserUseCase(
        _FakeUow(_user()), _FakeToken(), _FakeHasher(True), _settings()
    )
    tokens = await use_case("user@example.com", "pw")
    assert tokens.access_token == "token-access"
    assert tokens.refresh_token == "token-refresh"


async def test_login_unknown_user_raises():
    use_case = LoginUserUseCase(
        _FakeUow(None), _FakeToken(), _FakeHasher(True), _settings()
    )
    with pytest.raises(UserNotFoundError):
        await use_case("ghost@example.com", "pw")


async def test_login_blocked_user_raises():
    use_case = LoginUserUseCase(
        _FakeUow(_user(is_blocked=True)), _FakeToken(), _FakeHasher(True), _settings()
    )
    with pytest.raises(UserBlockedError):
        await use_case("user@example.com", "pw")


async def test_login_wrong_password_raises():
    use_case = LoginUserUseCase(
        _FakeUow(_user()), _FakeToken(), _FakeHasher(False), _settings()
    )
    with pytest.raises(InvalidPasswordError):
        await use_case("user@example.com", "pw")
