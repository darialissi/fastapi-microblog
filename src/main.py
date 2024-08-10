from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

from db.db import create_tables, drop_tables
from api.routers import all_routers

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from redis import asyncio as aioredis
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_tables()
    yield
    await drop_tables()


app = FastAPI(
    title='Microblog',
    prefix='/api',
    lifespan=lifespan
    )

for router in all_routers:
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        reload=True,
    )