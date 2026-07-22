import logging

from auth.application.dto.token_pair import TokenPair
from auth.domain.enums.token_type import TOKEN_TYPE_CLAIM, TokenType
from auth.application.services.hashing import PasswordHasherABC
from auth.application.config.settings import SettingsServiceABC
from auth.application.services.token import TokenServiceJWTABC
from auth.application.repositories.uow import UnitOfWorkABC
from auth.application.exceptions.user_exception import (
    InvalidPasswordError,
    UserBlockedError,
    UserNotFoundError,
)

logger = logging.getLogger("auth")


class LoginUserUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
        token_service: TokenServiceJWTABC,
        hashing: PasswordHasherABC,
        settings: SettingsServiceABC,
    ):
        self._uow = uow
        self._token_service = token_service
        self._hashing = hashing
        self._settings = settings

    async def __call__(self, email: str, password: str) -> TokenPair:
        async with self._uow as uow:
            user = await uow.users.get_by_email(email)

        if user is None:
            logger.warning(
                "login_failed", extra={"email": email, "reason": "not_found"}
            )
            raise UserNotFoundError(email)
        if user.is_blocked:
            logger.warning("login_failed", extra={"email": email, "reason": "blocked"})
            raise UserBlockedError()
        if not self._hashing.verify(password, user.password_hash):
            logger.warning(
                "login_failed", extra={"email": email, "reason": "bad_password"}
            )
            raise InvalidPasswordError()

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
        refresh_token = self._token_service.generate_token(
            {**identity, TOKEN_TYPE_CLAIM: TokenType.REFRESH.value},
            self._settings.refresh_token_expire,
        )
        logger.info("user_login", extra={"user_id": str(user.id)})
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
