import asyncio
import datetime
import os
from uuid import uuid4

from auth.domain.entities.user import User
from auth.domain.enums.role import Role
from auth.presentation.dependencies.container import container
from core.container import CoreContainer

container.session_factory.override(CoreContainer().session_factory)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin12345")


async def seed() -> None:
    hasher = container.password_hasher()
    uow = container.uow()

    async with uow:
        if await uow.users.get_by_email(ADMIN_EMAIL) is not None:
            print(f"Admin already exists: {ADMIN_EMAIL}")
            return

        now = datetime.datetime.now(datetime.UTC)
        await uow.users.save(
            User(
                id=uuid4(),
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password_hash=hasher.hash(ADMIN_PASSWORD),
                role=Role.ADMIN,
                is_blocked=False,
                created_at=now,
                updated_at=now,
            )
        )

    print(f"Admin created: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
