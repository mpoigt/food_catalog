import logging
from uuid import UUID

from catalog.application.dto.product import ProductImageDTO, ProductResponseDTO
from catalog.application.exceptions.catalog_exception import ProductNotFoundError
from catalog.application.repositories.uow import UnitOfWorkABC
from catalog.application.services.file_storage import FileStorageABC

logger = logging.getLogger("catalog")


class UploadProductImageUseCase:
    def __init__(self, uow: UnitOfWorkABC, storage: FileStorageABC):
        self._uow = uow
        self._storage = storage

    async def __call__(
        self, product_id: UUID, data: ProductImageDTO
    ) -> ProductResponseDTO:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)
            if product is None:
                raise ProductNotFoundError(str(product_id))

            previous_path = product.image_path
            product.image_path = await self._storage.save(data.content, data.extension)
            updated = await uow.products.update(product)
            category = await uow.categories.get_by_id(updated.category_id)

        if previous_path:
            await self._storage.delete(previous_path)

        logger.info("product_image_uploaded", extra={"product_id": str(updated.id)})
        return ProductResponseDTO.from_entity(
            updated, category.name if category else ""
        )
