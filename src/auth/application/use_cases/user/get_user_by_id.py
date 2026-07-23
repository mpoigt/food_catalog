from uuid import UUID

from auth.application.dto.user import UserResponseDTO
from auth.application.exceptions.user_exception import UserNotFoundError
from auth.application.repositories.uow import UnitOfWorkABC


class GetUserUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, user_id: UUID) -> UserResponseDTO:
        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(str(user_id))

        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_blocked=user.is_blocked,
        )
