from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from auth.application.dto.user import UserCreateDTO
from auth.application.use_cases.user.create_user import CreateUserUseCase
from auth.application.use_cases.user.login_user import LoginUserUseCase
from auth.domain.enums.role import Role
from auth.presentation.api.schemas.token_pair import TokenPairSchema
from auth.presentation.api.schemas.user import (
    LoginSchema,
    RegisterSchema,
    UserResponseSchema,
)
from auth.presentation.dependencies.container import AuthContainer

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    data: RegisterSchema,
    use_case: CreateUserUseCase = Depends(Provide[AuthContainer.create_user_use_case]),
) -> UserResponseSchema:
    dto = await use_case(
        UserCreateDTO(
            username=data.username,
            email=data.email,
            password=data.password,
            role=Role.USER,
        )
    )
    return UserResponseSchema.model_validate(dto)


@router.post("/login", response_model=TokenPairSchema)
@inject
async def login(
    data: LoginSchema,
    use_case: LoginUserUseCase = Depends(Provide[AuthContainer.login_user_use_case]),
) -> TokenPairSchema:
    tokens = await use_case(email=data.email, password=data.password)
    return TokenPairSchema(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )
