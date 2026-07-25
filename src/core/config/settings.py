from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_CONFIG = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    model_config = ENV_CONFIG

    db_url: str
    test_db_url: str


class RedisSettings(BaseSettings):
    model_config = ENV_CONFIG

    host: str
    port: int
    db: int

    @property
    def redis_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"