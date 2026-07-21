from redis.asyncio import Redis  # type: ignore[import-untyped]

from application.services.cache import CacheServiceABC
from infrastructure.config.settings import settings


class CacheService(CacheServiceABC):
    def __init__(self):
        self._redis = Redis(
            host=settings.redis_config.host,
            port=settings.redis_config.port,
            db=settings.redis_config.db,
        )

    async def add(self, jwt: str, expire: int) -> None:
        await self._redis.setex(jwt, time=expire, value="1")

    async def exists(self, jwt: str) -> bool:
        return await self._redis.exists(jwt) == 1
