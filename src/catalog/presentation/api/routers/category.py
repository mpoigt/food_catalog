from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status

from auth.domain.enums.role import Role
from auth.presentation.dependencies.auth import get_current_user, require_roles
from catalog.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO
from catalog.application.use_cases.category.create_category import CreateCategoryUseCase
from catalog.application.use_cases.category.delete_category import DeleteCategoryUseCase
from catalog.application.use_cases.category.get_category import GetCategoryUseCase
from catalog.application.use_cases.category.list_categories import ListCategoriesUseCase
from catalog.application.use_cases.category.update_category import UpdateCategoryUseCase
from catalog.presentation.api.schemas.category import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CategoryUpdateSchema,
)
from catalog.presentation.dependencies.container import CatalogContainer

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],
)

_manage = Depends(require_roles(Role.ADVANCED, Role.ADMIN))


@router.get("/", response_model=list[CategoryResponseSchema])
@inject
async def list_categories(
    use_case: ListCategoriesUseCase = Depends(
        Provide[CatalogContainer.list_categories_use_case]
    ),
) -> list[CategoryResponseSchema]:
    items = await use_case()
    return [CategoryResponseSchema.model_validate(item) for item in items]


@router.get("/{category_id}", response_model=CategoryResponseSchema)
@inject
async def get_category(
    category_id: UUID = Path(...),
    use_case: GetCategoryUseCase = Depends(
        Provide[CatalogContainer.get_category_use_case]
    ),
) -> CategoryResponseSchema:
    dto = await use_case(category_id)
    return CategoryResponseSchema.model_validate(dto)


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[_manage],
)
@inject
async def create_category(
    data: CategoryCreateSchema,
    use_case: CreateCategoryUseCase = Depends(
        Provide[CatalogContainer.create_category_use_case]
    ),
) -> CategoryResponseSchema:
    dto = await use_case(CategoryCreateDTO(name=data.name))
    return CategoryResponseSchema.model_validate(dto)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponseSchema,
    dependencies=[_manage],
)
@inject
async def update_category(
    data: CategoryUpdateSchema,
    category_id: UUID = Path(...),
    use_case: UpdateCategoryUseCase = Depends(
        Provide[CatalogContainer.update_category_use_case]
    ),
) -> CategoryResponseSchema:
    dto = await use_case(category_id, CategoryUpdateDTO(name=data.name))
    return CategoryResponseSchema.model_validate(dto)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[_manage],
)
@inject
async def delete_category(
    category_id: UUID = Path(...),
    use_case: DeleteCategoryUseCase = Depends(
        Provide[CatalogContainer.delete_category_use_case]
    ),
) -> None:
    await use_case(category_id)