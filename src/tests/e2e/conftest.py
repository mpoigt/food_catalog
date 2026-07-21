import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DB_URL = os.getenv(
    "TEST_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5433/test_auth_db",
)


class FakeCache:
    """In-memory замена Redis, чтобы e2e не зависели от него."""

    def __init__(self):
        self._store: set[str] = set()

    async def add(self, key: str, expire: int) -> None:
        self._store.add(key)

    async def exists(self, key: str) -> bool:
        return key in self._store


@pytest_asyncio.fixture
async def client(prepare_test_database) -> AsyncClient:
    from main import app
    from presentation.dependencies.container import container

    engine = create_async_engine(TEST_DB_URL)
    maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users CASCADE"))

    container.session_factory.override(maker)
    container.cache_service.override(FakeCache())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client

    container.session_factory.reset_override()
    container.cache_service.reset_override()
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users CASCADE"))
    await engine.dispose()


@pytest_asyncio.fixture
async def admin_token(client) -> str:
    from infrastructure.services.hashing import PasswordHasher

    engine = create_async_engine(TEST_DB_URL)
    maker = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with maker() as session:
        await session.execute(
            text(
                "INSERT INTO users (id, username, email, password_hash, role, is_blocked) "
                "VALUES (gen_random_uuid(), 'admin', 'admin@example.com', :ph, 'ADMIN', false)"
            ),
            {"ph": PasswordHasher().hash("admin12345")},
        )
        await session.commit()
    await engine.dispose()

    response = await client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "admin12345"},
    )
    return response.json()["access_token"]
