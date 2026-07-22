import logging
from uuid import UUID

from auth.application.dto.user import UserResponseDTO, UserUpdateAdminDTO
from auth.application.exceptions.user_exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.application.services.hashing import PasswordHasherABC
from auth.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("auth")


class UpdateUserByAdminUseCase:
    def __init__(self, uow: UnitOfWorkABC, hashing: PasswordHasherABC):
        self._uow = uow
        self._hashing = hashing

    async def __call__(
        self, user_id: UUID, data: UserUpdateAdminDTO
    ) -> UserResponseDTO:
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError(str(user_id))

            if data.email is not None and data.email != user.email:
                if await uow.users.is_email_exists(data.email):
                    raise UserAlreadyExistsError(data.email)
                user.email = data.email

            if data.username is not None and data.username != user.username:
                if await uow.users.is_username_exists(data.username):
                    raise UserAlreadyExistsError(data.username)
                user.username = data.username

            if data.role is not None:
                user.role = data.role
            if data.is_blocked is not None:
                user.is_blocked = data.is_blocked
            if data.password is not None:
                user.password_hash = self._hashing.hash(data.password)

            updated = await uow.users.update(user)

        logger.info(
            "user_updated_by_admin",
            extra={
                "user_id": str(updated.id),
                "blocked": data.is_blocked,
                "role": data.role.value if data.role else None,
                "password_changed": data.password is not None,
            },
        )
        return UserResponseDTO(
            id=updated.id,
            username=updated.username,
            email=updated.email,
            role=updated.role,
            is_blocked=updated.is_blocked,
        )
