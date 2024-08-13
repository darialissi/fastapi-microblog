import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from db.db import Base
from src.config import settings
from src.main import app
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


engine_test = create_async_engine(settings.DATABASE_URL_asyncpg, poolclass=NullPool)
async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

transport = ASGITransport(app=app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# objects for foreign key relationship

@pytest.fixture
async def add_user(ac: AsyncClient):
    await ac.post("/users", json={
        "username": "userfix",
        "password": "12345",
    })

@pytest.fixture
async def add_post(ac: AsyncClient, add_user):
    await ac.post("/posts", json={
        "user_id": 1,
        "title": "postfix",
        "category": "development",
        "body": "test post",
    })