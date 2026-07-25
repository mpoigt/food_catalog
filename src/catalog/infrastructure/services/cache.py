from redis.asyncio import Redis  # type: ignore[import-untyped]

from catalog.application.services.cache import CacheServiceABC


class RedisCacheService(CacheServiceABC):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str) -> str | None:
        value = await self._redis.get(key)
        if isinstance(value, bytes):
            return value.decode()
        return value

    async def set(self, key: str, value: str, ttl_seconds: int) -> None:
        await self._redis.set(key, value, ex=ttl_seconds)
