from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from application.use_cases.token.refreshing import RefreshJWTTokensUseCase
from application.use_cases.user.create_user import CreateUserUseCase
from application.use_cases.user.delete_user import DeleteUserUseCase
from application.use_cases.user.get_user_by_id import GetUserUseCase
from application.use_cases.user.list_user import ListUsersUseCase
from application.use_cases.user.login_user import LoginUserUseCase
from application.use_cases.user.update_user_for_admin import UpdateUserByAdminUseCase
from infrastructure.db.uow.uow import UnitOfWork
from infrastructure.services.hashing import PasswordHasher
from infrastructure.services.cache import CacheService
from infrastructure.services.token import TokenServiceJWT
from infrastructure.config.settings import SettingsService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "presentation.api.routers.auth",
            "presentation.api.routers.user",
            "presentation.api.routers.token",
            "presentation.dependencies.auth",
        ],
    )

    settings = providers.Singleton(SettingsService)

    engine = providers.Singleton(
        create_async_engine, settings.provided.db_settings.db_url
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    uow = providers.Factory(UnitOfWork, session_factory=session_factory)

    password_hasher = providers.Factory(PasswordHasher)
    token_service_jwt = providers.Factory(TokenServiceJWT, settings=settings)
    cache_service = providers.Singleton(CacheService)

    create_user_use_case = providers.Factory(
        CreateUserUseCase, uow=uow, hashing=password_hasher
    )
    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        uow=uow,
        token_service=token_service_jwt,
        hashing=password_hasher,
        settings=settings,
    )
    refresh_tokens_use_case = providers.Factory(
        RefreshJWTTokensUseCase,
        token_service=token_service_jwt,
        cache=cache_service,
        settings=settings,
    )
    get_user_use_case = providers.Factory(GetUserUseCase, uow=uow)
    list_users_use_case = providers.Factory(ListUsersUseCase, uow=uow)
    delete_user_use_case = providers.Factory(DeleteUserUseCase, uow=uow)
    update_user_admin_use_case = providers.Factory(
        UpdateUserByAdminUseCase, uow=uow, hashing=password_hasher
    )


container = Container()
