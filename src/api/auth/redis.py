from datetime import timedelta
from redis.asyncio import Redis


async def add_token_to_redis(
    redis_client: Redis,
    key: int,
    value: str,
    expire: timedelta
    ):
    await redis_client.set(key, value)
    await redis_client.expire(key, expire)