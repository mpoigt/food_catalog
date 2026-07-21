from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, status

from application.dto.user import UserCreateDTO, UserUpdateAdminDTO
from application.use_cases.user.create_user import CreateUserUseCase
from application.use_cases.user.delete_user import DeleteUserUseCase
from application.use_cases.user.get_user_by_id import GetUserUseCase
from application.use_cases.user.list_user import ListUsersUseCase
from application.use_cases.user.update_user_for_admin import UpdateUserByAdminUseCase
from domain.enums.role import Role
from presentation.api.schemas.user import (
    AdminCreateUserSchema,
    PaginatedUsersSchema,
    UserResponseSchema,
    UserUpdateAdminSchema,
)
from presentation.dependencies.auth import require_roles
from presentation.dependencies.container import Container

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_roles(Role.ADMIN))],
)


@router.get("/", response_model=PaginatedUsersSchema)
@inject
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    sort_by: str | None = Query(None),
    order_by: str = Query("asc", pattern=r"^(asc|desc)$"),
    use_case: ListUsersUseCase = Depends(Provide[Container.list_users_use_case]),
) -> PaginatedUsersSchema:
    items, total = await use_case(
        page=page, limit=limit, sort_by=sort_by, order_by=order_by
    )
    return PaginatedUsersSchema(
        total=total,
        page=page,
        limit=limit,
        items=[UserResponseSchema.model_validate(item) for item in items],
    )


@router.post(
    "/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
@inject
async def create_user(
    data: AdminCreateUserSchema,
    use_case: CreateUserUseCase = Depends(Provide[Container.create_user_use_case]),
) -> UserResponseSchema:
    dto = await use_case(
        UserCreateDTO(
            username=data.username,
            email=data.email,
            password=data.password,
            role=data.role,
        )
    )
    return UserResponseSchema.model_validate(dto)


@router.get("/{user_id}", response_model=UserResponseSchema)
@inject
async def get_user(
    user_id: UUID = Path(...),
    use_case: GetUserUseCase = Depends(Provide[Container.get_user_use_case]),
) -> UserResponseSchema:
    dto = await use_case(user_id)
    return UserResponseSchema.model_validate(dto)


@router.patch("/{user_id}", response_model=UserResponseSchema)
@inject
async def update_user(
    data: UserUpdateAdminSchema,
    user_id: UUID = Path(...),
    use_case: UpdateUserByAdminUseCase = Depends(
        Provide[Container.update_user_admin_use_case]
    ),
) -> UserResponseSchema:
    dto = await use_case(
        user_id,
        UserUpdateAdminDTO(
            username=data.username,
            email=data.email,
            role=data.role,
            is_blocked=data.is_blocked,
            password=data.password,
        ),
    )
    return UserResponseSchema.model_validate(dto)


@router.patch("/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: UUID = Path(...),
    use_case: DeleteUserUseCase = Depends(Provide[Container.delete_user_use_case]),
) -> None:
    await use_case(user_id)
