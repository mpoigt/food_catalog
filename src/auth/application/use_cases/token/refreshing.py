import datetime
from uuid import UUID

from auth.application.dto.token_pair import TokenPair
from auth.domain.enums.token_type import TOKEN_TYPE_CLAIM, TokenType
from auth.application.services.cache import CacheServiceABC
from auth.application.config.settings import SettingsServiceABC
from auth.application.services.token import TokenServiceJWTABC
from auth.application.repositories.uow import UnitOfWorkABC
from auth.application.exceptions.user_exception import (
    InvalidTokenError,
    UserBlockedError,
)


class RefreshJWTTokensUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
        token_service: TokenServiceJWTABC,
        cache: CacheServiceABC,
        settings: SettingsServiceABC,
    ):
        self._uow = uow
        self._token_service = token_service
        self._cache = cache
        self._settings = settings

    async def __call__(self, refresh_token: str) -> TokenPair:
        if await self._cache.exists(refresh_token):
            raise InvalidTokenError("Token revoked")

        payload = self._token_service.decode_token(refresh_token)
        if payload.get(TOKEN_TYPE_CLAIM) != TokenType.REFRESH.value:
            raise InvalidTokenError("Not a refresh token")

        async with self._uow as uow:
            user = await uow.users.get_by_id(UUID(payload["id"]))

        if user is None:
            raise InvalidTokenError("User no longer exists")
        if user.is_blocked:
            raise UserBlockedError()

        identity = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
        }
        access_token = self._token_service.generate_token(
            {**identity, TOKEN_TYPE_CLAIM: TokenType.ACCESS.value},
            self._settings.access_token_expire,
        )
        refresh = self._token_service.generate_token(
            {**identity, TOKEN_TYPE_CLAIM: TokenType.REFRESH.value},
            self._settings.refresh_token_expire,
        )

        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        ttl = max(payload["exp"] - now, 0)
        await self._cache.add(refresh_token, ttl)

        return TokenPair(access_token=access_token, refresh_token=refresh)
