from datetime import timedelta

from redis.asyncio import Redis

from config import settings


class RedisStorage:

    @classmethod
    async def add_token(
        cls,
        redis_client: Redis,
        key: str,
        value: str,
        expire: timedelta = timedelta(days=settings.jwt.refresh_token_expire_days),
    ) -> None:
        await redis_client.set(key, value, ex=expire)

    @classmethod
    async def get_token(cls, redis_client: Redis, key: str) -> str:
        token = await redis_client.get(key)
        return token.decode()

    @classmethod
    async def revoke_token(cls, redis_client: Redis, key: str) -> None:
        await redis_client.delete(key)
