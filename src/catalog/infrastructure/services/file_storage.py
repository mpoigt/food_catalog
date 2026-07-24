from pathlib import Path
from uuid import uuid4

import anyio

from catalog.application.services.file_storage import FileStorageABC

PRODUCTS_DIR = "products"


class LocalFileStorage(FileStorageABC):
    def __init__(self, media_root: str):
        self._root = Path(media_root)

    async def save(self, content: bytes, extension: str) -> str:
        relative_path = f"{PRODUCTS_DIR}/{uuid4().hex}{extension}"
        target = self._root / relative_path

        def write() -> None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

        await anyio.to_thread.run_sync(write)
        return relative_path

    async def delete(self, relative_path: str) -> None:
        target = self._root / relative_path

        def remove() -> None:
            target.unlink(missing_ok=True)

        await anyio.to_thread.run_sync(remove)
