from dependency_injector import containers, providers

from auth.application.use_cases.token.refreshing import RefreshJWTTokensUseCase
from auth.application.use_cases.user.create_user import CreateUserUseCase
from auth.application.use_cases.user.delete_user import DeleteUserUseCase
from auth.application.use_cases.user.get_user_by_id import GetUserUseCase
from auth.application.use_cases.user.list_user import ListUsersUseCase
from auth.application.use_cases.user.login_user import LoginUserUseCase
from auth.application.use_cases.user.update_user_for_admin import UpdateUserByAdminUseCase
from auth.infrastructure.config.settings import SettingsService
from auth.infrastructure.db.uow.uow import AuthUnitOfWork
from auth.infrastructure.services.cache import CacheService
from auth.infrastructure.services.hashing import PasswordHasher
from auth.infrastructure.services.token import TokenServiceJWT


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "auth.presentation.api.routers.auth",
            "auth.presentation.api.routers.user",
            "auth.presentation.api.routers.token",
            "auth.presentation.dependencies.auth",
        ],
    )

    session_factory = providers.Dependency()

    settings = providers.Singleton(SettingsService)

    uow = providers.Factory(AuthUnitOfWork, session_factory=session_factory)

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


container = AuthContainer()