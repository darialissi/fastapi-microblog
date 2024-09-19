from datetime import timedelta

from redis.asyncio import Redis


class RedisStorage:

    @staticmethod
    async def add_token(redis_client: Redis, key: int, value: str, expire: timedelta):
        await redis_client.set(key, value)
        await redis_client.expire(key, expire)

    @staticmethod
    async def revoke_token(redis_client: Redis, key: int):
        await redis_client.delete(key)
