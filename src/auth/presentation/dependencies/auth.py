from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.application.dto.user import CurrentUserDTO
from auth.domain.enums.token_type import TOKEN_TYPE_CLAIM, TokenType
from auth.application.exceptions.user_exception import (
    AccessDeniedError,
    InvalidTokenError,
    UserBlockedError,
)
from auth.application.repositories.uow import UnitOfWorkABC
from auth.application.services.token import TokenServiceJWTABC
from auth.domain.enums.role import Role
from auth.presentation.dependencies.container import AuthContainer

_bearer = HTTPBearer(auto_error=False)


@inject
async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    token_service: TokenServiceJWTABC = Depends(Provide[AuthContainer.token_service_jwt]),
    uow: UnitOfWorkABC = Depends(Provide[AuthContainer.uow]),
) -> CurrentUserDTO:
    if credentials is None:
        raise InvalidTokenError("Missing bearer token")

    payload = token_service.decode_token(credentials.credentials)
    if payload.get(TOKEN_TYPE_CLAIM) != TokenType.ACCESS.value:
        raise InvalidTokenError("Not an access token")

    try:
        user_id = UUID(payload["id"])
    except (KeyError, ValueError) as exc:
        raise InvalidTokenError() from exc

    async with uow:
        user = await uow.users.get_by_id(user_id)

    if user is None:
        raise InvalidTokenError("User no longer exists")
    if user.is_blocked:
        raise UserBlockedError()

    return CurrentUserDTO(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
    )


def require_roles(*roles: Role):
    def guard(
        user: CurrentUserDTO = Depends(get_current_user),
    ) -> CurrentUserDTO:
        if user.role not in roles:
            raise AccessDeniedError()
        return user

    return guard
