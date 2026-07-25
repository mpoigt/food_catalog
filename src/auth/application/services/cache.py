from abc import ABC, abstractmethod


class CacheServiceABC(ABC):
    @abstractmethod
    async def add(self, jwt: str, expire: int) -> None: ...

    @abstractmethod
    async def exists(self, jwt: str) -> bool: ...
