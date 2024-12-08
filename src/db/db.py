from typing import AsyncGenerator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from config import settings

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(settings.db.DATABASE_URL_asyncpg, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


redis_client = aioredis.from_url(settings.db.REDIS_URL)


async def init_cache():
    return FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
