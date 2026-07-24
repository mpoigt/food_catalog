from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import jwt

from auth.application.exceptions.user_exception import InvalidTokenError
from auth.application.services.token import TokenServiceJWTABC

if TYPE_CHECKING:
    from auth.infrastructure.config.settings import SettingsService


class TokenServiceJWT(TokenServiceJWTABC):
    def __init__(self, settings: SettingsService):
        self._settings = settings

    def generate_token(self, data: dict, expires: int) -> str:
        payload = dict(data)
        payload["exp"] = datetime.datetime.now(
            datetime.UTC
        ) + datetime.timedelta(minutes=expires)
        return jwt.encode(
            payload,
            self._settings.token_secret_key,
            algorithm=self._settings.jwt_config.jwt_hashing,
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self._settings.token_secret_key,
                algorithms=[self._settings.jwt_config.jwt_hashing],
            )
        except jwt.PyJWTError as exc:
            raise InvalidTokenError() from exc
