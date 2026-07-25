from auth.application.dto.user import UserResponseDTO
from auth.application.repositories.uow import UnitOfWorkABC


class ListUsersUseCase:
    def __init__(self, uow: UnitOfWorkABC):
        self._uow = uow

    async def __call__(
        self,
        page: int = 1,
        limit: int = 30,
        sort_by: str | None = None,
        order_by: str = "asc",
    ) -> tuple[list[UserResponseDTO], int]:
        async with self._uow as uow:
            users, total = await uow.users.list_users(
                page=page,
                limit=limit,
                filters={},
                sort_by=sort_by,
                order_by=order_by,
            )

        items = [UserResponseDTO.from_entity(user) for user in users]
        return items, total
