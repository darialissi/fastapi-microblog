import asyncio
from typing import AsyncGenerator, AsyncIterator

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from api.auth.schemas import TokenSchema
from api.dependencies import get_db
from config import settings
from db.db import Base
from main import app
from models.categories import Category
from schemas.comments import CommentSchemaAdd
from schemas.posts import PostSchemaAdd
from schemas.users import UserSchemaAdd
from utils.unitofwork import DBManager

engine_test = create_async_engine(settings.db.DATABASE_URL_asyncpg, poolclass=NullPool)
async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DBManager(async_session) as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def prepare_database():
    redis = aioredis.from_url(settings.db.REDIS_URL)
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


@pytest.fixture
async def ac() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
def data_user() -> UserSchemaAdd:
    return UserSchemaAdd(username="userfix", password="12345")


@pytest.fixture(scope="function")
async def register_fixture(ac: AsyncClient, data_user: UserSchemaAdd) -> None:
    await ac.post("/auth/register", data=data_user.model_dump_json())


@pytest.fixture(scope="function")
async def token_fixture(ac: AsyncClient, data_user: UserSchemaAdd, register_fixture: None) -> str:
    resp = await ac.post("/auth/token", data=data_user.model_dump_json())
    token = TokenSchema(**resp.json())
    return f"{token.token_type} {token.access_token}"


@pytest.fixture(scope="function")
def data_post() -> PostSchemaAdd:
    return PostSchemaAdd(title="design patterns", category=Category.design, body="...")


@pytest.fixture(scope="function")
async def post_fixture(ac: AsyncClient, data_post: PostSchemaAdd, token_fixture: str) -> None:
    await ac.post("/posts", data=data_post.model_dump_json(), headers={"Authorization": token_fixture})


@pytest.fixture(scope="function")
def data_comment() -> CommentSchemaAdd:
    return CommentSchemaAdd(body="some comment")


@pytest.fixture(scope="function")
async def comment_fixture(
    ac: AsyncClient, post_fixture: None, data_comment: CommentSchemaAdd, token_fixture: str
) -> None:
    await ac.post("/posts/1/comments", data=data_comment.model_dump_json(), headers={"Authorization": token_fixture})
