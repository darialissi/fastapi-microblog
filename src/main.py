from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api.routers import all_routers
from config import settings
from db.db import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.db.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_tables()
    yield
    await drop_tables()


app = FastAPI(title="Microblog", prefix="/api", lifespan=lifespan)

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
