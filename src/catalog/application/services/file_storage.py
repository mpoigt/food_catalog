from abc import ABC, abstractmethod


class FileStorageABC(ABC):
    @abstractmethod
    async def save(self, content: bytes, extension: str) -> str: ...

    @abstractmethod
    async def delete(self, relative_path: str) -> None: ...
