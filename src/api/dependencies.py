from typing import Annotated, AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import async_session, redis_client
from utils.unitofwork import DBManager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DBManager(async_session) as db:
        yield db


async def get_redis():
    async with redis_client as redis:
        yield redis


UOW_db = Annotated[DBManager, Depends(get_db)]
Redis_db = Annotated[Redis, Depends(get_redis)]
