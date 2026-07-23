from pydantic_settings import BaseSettings, SettingsConfigDict

from auth.application.config.settings import SettingsServiceABC
from core.config.settings import DatabaseSettings, RedisSettings

_ENV = SettingsConfigDict(env_file=".env", extra="ignore")


class JWTTokensSettings(BaseSettings):
    model_config = _ENV

    access_token_expire: int
    refresh_token_expire: int
    jwt_hashing: str
    token_secret_key: str


class SettingsService(SettingsServiceABC):
    jwt_config: JWTTokensSettings = JWTTokensSettings()
    db_settings: DatabaseSettings = DatabaseSettings()
    redis_config: RedisSettings = RedisSettings()

    @property
    def token_secret_key(self) -> str:
        return self.jwt_config.token_secret_key

    @property
    def access_token_expire(self) -> int:
        return self.jwt_config.access_token_expire

    @property
    def refresh_token_expire(self) -> int:
        return self.jwt_config.refresh_token_expire


settings = SettingsService()
