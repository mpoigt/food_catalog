import datetime
import logging
from uuid import uuid4

from auth.application.dto.user import UserCreateDTO, UserResponseDTO
from auth.application.exceptions.user_exception import UserAlreadyExistsError
from auth.application.services.hashing import PasswordHasherABC
from auth.application.repositories.uow import UnitOfWorkABC
from auth.domain.entities.user import User

logger = logging.getLogger("auth")


class CreateUserUseCase:
    def __init__(self, uow: UnitOfWorkABC, hashing: PasswordHasherABC):
        self._uow = uow
        self._hashing = hashing

    async def __call__(self, data: UserCreateDTO) -> UserResponseDTO:
        async with self._uow as uow:
            if await uow.users.is_email_exists(data.email):
                raise UserAlreadyExistsError(data.email)
            if await uow.users.is_username_exists(data.username):
                raise UserAlreadyExistsError(data.username)

            now = datetime.datetime.now(datetime.timezone.utc)
            user = User(
                id=uuid4(),
                username=data.username,
                email=data.email,
                password_hash=self._hashing.hash(data.password),
                role=data.role,
                is_blocked=False,
                created_at=now,
                updated_at=now,
            )
            saved = await uow.users.save(user)

        logger.info(
            "user_created", extra={"user_id": str(saved.id), "role": saved.role.value}
        )
        return UserResponseDTO.from_entity(saved)
