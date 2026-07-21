import datetime

from application.dto.token_pair import TokenPair
from domain.enums.token_type import TOKEN_TYPE_CLAIM, TokenType
from application.services.cache import CacheServiceABC
from application.config.settings import SettingsServiceABC
from application.services.token import TokenServiceJWTABC
from application.exceptions.user_exception import InvalidTokenError


class RefreshJWTTokensUseCase:
    def __init__(
        self,
        token_service: TokenServiceJWTABC,
        cache: CacheServiceABC,
        settings: SettingsServiceABC,
    ):
        self._token_service = token_service
        self._cache = cache
        self._settings = settings

    async def __call__(self, refresh_token: str) -> TokenPair:
        if await self._cache.exists(refresh_token):
            raise InvalidTokenError("Token revoked")

        payload = self._token_service.decode_token(refresh_token)
        if payload.get(TOKEN_TYPE_CLAIM) != TokenType.REFRESH.value:
            raise InvalidTokenError("Not a refresh token")

        identity = {
            "id": payload["id"],
            "username": payload["username"],
            "email": payload["email"],
            "role": payload["role"],
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
