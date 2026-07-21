from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.dto.user import CurrentUserDTO
from application.exceptions.user_exception import (
    AccessDeniedError,
    InvalidTokenError,
    UserBlockedError,
)
from application.repositories.uow import UnitOfWorkABC
from application.services.token import TokenServiceJWTABC
from domain.enums.role import Role
from presentation.dependencies.container import Container

_bearer = HTTPBearer(auto_error=False)


@inject
async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    token_service: TokenServiceJWTABC = Depends(Provide[Container.token_service_jwt]),
    uow: UnitOfWorkABC = Depends(Provide[Container.uow]),
) -> CurrentUserDTO:
    if credentials is None:
        raise InvalidTokenError("Missing bearer token")

    payload = token_service.decode_token(credentials.credentials)
    if payload.get("token_type") != "access":
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
