import os
from decimal import Decimal

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from catalog.application.services.currency import UsdRate

TEST_DB_URL = os.getenv(
    "TEST_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5433/test_auth_db",
)


class FakeCache:
    def __init__(self):
        self._store: set[str] = set()

    async def add(self, key: str, expire: int) -> None:
        self._store.add(key)

    async def exists(self, key: str) -> bool:
        return key in self._store


class FakeCurrencyService:
    async def get_usd_rate(self) -> UsdRate:
        return UsdRate(rate=Decimal("3.00"), date="2026-07-22")


async def _truncate(engine) -> None:
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users, categories, products CASCADE"))


@pytest_asyncio.fixture
async def client(prepare_test_database) -> AsyncClient:
    from main import app
    from auth.presentation.dependencies.container import container as auth_container
    from catalog.presentation.dependencies.container import container as catalog_container

    engine = create_async_engine(TEST_DB_URL)
    maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    await _truncate(engine)

    auth_container.session_factory.override(maker)
    auth_container.cache_service.override(FakeCache())
    catalog_container.session_factory.override(maker)
    catalog_container.currency_service.override(FakeCurrencyService())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client

    auth_container.session_factory.reset_override()
    auth_container.cache_service.reset_override()
    catalog_container.session_factory.reset_override()
    catalog_container.currency_service.reset_override()
    await _truncate(engine)
    await engine.dispose()


@pytest_asyncio.fixture
async def make_token(client):
    from auth.infrastructure.services.hashing import PasswordHasher

    async def _make(role: str, email: str, password: str = "secret123") -> str:
        engine = create_async_engine(TEST_DB_URL)
        maker = async_sessionmaker(bind=engine, expire_on_commit=False)
        username = email.split("@")[0]
        async with maker() as session:
            await session.execute(
                text(
                    "INSERT INTO users (id, username, email, password_hash, role, is_blocked) "
                    "VALUES (gen_random_uuid(), :u, :e, :ph, :r, false)"
                ),
                {"u": username, "e": email, "ph": PasswordHasher().hash(password), "r": role},
            )
            await session.commit()
        await engine.dispose()

        response = await client.post(
            "/auth/login", json={"email": email, "password": password}
        )
        return response.json()["access_token"]

    return _make


@pytest_asyncio.fixture
async def admin_token(make_token) -> str:
    return await make_token("ADMIN", "admin@example.com", "admin12345")
