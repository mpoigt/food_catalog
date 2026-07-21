import asyncio
import os

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.db.models import Base

TEST_DB_URL = os.getenv(
    "TEST_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5433/test_auth_db",
)


async def _create_database_if_missing() -> None:
    url = make_url(TEST_DB_URL)
    conn = await asyncpg.connect(
        host=url.host,
        port=url.port,
        user=url.username,
        password=url.password,
        database="postgres",
    )
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", url.database
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{url.database}"')
    finally:
        await conn.close()


async def _create_tables() -> None:
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    asyncio.run(_create_database_if_missing())
    asyncio.run(_create_tables())
    yield


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(TEST_DB_URL)
    async with engine.connect() as conn:
        transaction = await conn.begin()
        maker = async_sessionmaker(
            bind=conn, class_=AsyncSession, expire_on_commit=False
        )
        session = maker()
        await session.execute(text("TRUNCATE TABLE users CASCADE"))
        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
    await engine.dispose()
