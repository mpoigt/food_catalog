import logging
from uuid import UUID

from auth.application.exceptions.user_exception import (
    SelfActionForbiddenError,
    UserNotFoundError,
)
from auth.application.repositories.uow import UnitOfWorkABC

logger = logging.getLogger("auth")


class DeleteUserUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(self, user_id: UUID, actor_id: UUID) -> None:
        if user_id == actor_id:
            raise SelfActionForbiddenError()

        async with self._uow as uow:
            user = await uow.users.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError(str(user_id))
            await uow.users.delete(user_id)

        logger.info("user_deleted", extra={"user_id": str(user_id)})
