from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Path, Query, UploadFile, status

from auth.application.dto.user import CurrentUserDTO
from auth.domain.enums.role import Role
from auth.presentation.dependencies.auth import get_current_user, require_roles
from catalog.application.dto.product import (
    ProductCreateDTO,
    ProductImageDTO,
    ProductUpdateDTO,
)
from catalog.application.exceptions.catalog_exception import InvalidImageError
from catalog.application.use_cases.currency.get_product_price_usd import (
    GetProductPriceUsdUseCase,
)
from catalog.application.use_cases.product.create_product import CreateProductUseCase
from catalog.application.use_cases.product.delete_product import DeleteProductUseCase
from catalog.application.use_cases.product.get_product import GetProductUseCase
from catalog.application.use_cases.product.list_products import ListProductsUseCase
from catalog.application.use_cases.product.update_product import UpdateProductUseCase
from catalog.application.use_cases.product.upload_product_image import (
    UploadProductImageUseCase,
)
from catalog.presentation.api.schemas.product import (
    PaginatedProductsSchema,
    ProductCreateSchema,
    ProductPriceUsdSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
)
from catalog.presentation.dependencies.container import CatalogContainer

router = APIRouter(prefix="/products", tags=["Products"])

_manage = Depends(require_roles(Role.ADVANCED, Role.ADMIN))

MEDIA_URL_PREFIX = "/media"
MAX_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _to_response(dto, role: Role) -> ProductResponseSchema:
    schema = ProductResponseSchema.model_validate(dto)
    if dto.image_path:
        schema.image_url = f"{MEDIA_URL_PREFIX}/{dto.image_path}"
    if role == Role.USER:
        schema.note_special = None
    return schema


def _writable_note_special(role: Role, value: str | None) -> str | None:
    # USER can neither see nor set the special note; ignore whatever was sent.
    return None if role == Role.USER else value


@router.get("/", response_model=PaginatedProductsSchema)
@inject
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    search: str | None = Query(None),
    category_id: UUID | None = Query(None),
    sort_by: str | None = Query(None),
    order_by: str = Query("asc", pattern=r"^(asc|desc)$"),
    user: CurrentUserDTO = Depends(get_current_user),
    use_case: ListProductsUseCase = Depends(
        Provide[CatalogContainer.list_products_use_case]
    ),
) -> PaginatedProductsSchema:
    items, total = await use_case(
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        sort_by=sort_by,
        order_by=order_by,
    )
    return PaginatedProductsSchema(
        total=total,
        page=page,
        limit=limit,
        items=[_to_response(item, user.role) for item in items],
    )


@router.get("/{product_id}", response_model=ProductResponseSchema)
@inject
async def get_product(
    product_id: UUID = Path(...),
    user: CurrentUserDTO = Depends(get_current_user),
    use_case: GetProductUseCase = Depends(
        Provide[CatalogContainer.get_product_use_case]
    ),
) -> ProductResponseSchema:
    dto = await use_case(product_id)
    return _to_response(dto, user.role)


@router.get("/{product_id}/price-usd", response_model=ProductPriceUsdSchema)
@inject
async def get_product_price_usd(
    product_id: UUID = Path(...),
    _: CurrentUserDTO = Depends(get_current_user),
    use_case: GetProductPriceUsdUseCase = Depends(
        Provide[CatalogContainer.get_product_price_usd_use_case]
    ),
) -> ProductPriceUsdSchema:
    dto = await use_case(product_id)
    return ProductPriceUsdSchema.model_validate(dto)


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_product(
    data: ProductCreateSchema,
    user: CurrentUserDTO = Depends(get_current_user),
    use_case: CreateProductUseCase = Depends(
        Provide[CatalogContainer.create_product_use_case]
    ),
) -> ProductResponseSchema:
    dto = await use_case(
        ProductCreateDTO(
            name=data.name,
            category_id=data.category_id,
            description=data.description,
            price=data.price,
            note_common=data.note_common,
            note_special=_writable_note_special(user.role, data.note_special),
        )
    )
    return _to_response(dto, user.role)


@router.patch("/{product_id}", response_model=ProductResponseSchema)
@inject
async def update_product(
    data: ProductUpdateSchema,
    product_id: UUID = Path(...),
    user: CurrentUserDTO = Depends(get_current_user),
    use_case: UpdateProductUseCase = Depends(
        Provide[CatalogContainer.update_product_use_case]
    ),
) -> ProductResponseSchema:
    dto = await use_case(
        product_id,
        ProductUpdateDTO(
            name=data.name,
            category_id=data.category_id,
            description=data.description,
            price=data.price,
            note_common=data.note_common,
            note_special=_writable_note_special(user.role, data.note_special),
        ),
    )
    return _to_response(dto, user.role)


@router.post("/{product_id}/image", response_model=ProductResponseSchema)
@inject
async def upload_product_image(
    product_id: UUID = Path(...),
    file: UploadFile = File(...),
    user: CurrentUserDTO = Depends(get_current_user),
    use_case: UploadProductImageUseCase = Depends(
        Provide[CatalogContainer.upload_product_image_use_case]
    ),
) -> ProductResponseSchema:
    extension = ALLOWED_IMAGE_TYPES.get(file.content_type or "")
    if extension is None:
        raise InvalidImageError("Разрешены только JPEG, PNG и WEBP")

    content = await file.read()
    if len(content) > MAX_IMAGE_BYTES:
        raise InvalidImageError("Файл больше 5 МБ")

    dto = await use_case(product_id, ProductImageDTO(content=content, extension=extension))
    return _to_response(dto, user.role)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[_manage],
)
@inject
async def delete_product(
    product_id: UUID = Path(...),
    use_case: DeleteProductUseCase = Depends(
        Provide[CatalogContainer.delete_product_use_case]
    ),
) -> None:
    await use_case(product_id)