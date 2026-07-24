from pydantic_settings import BaseSettings

from core.config.settings import ENV_CONFIG


class MediaSettings(BaseSettings):
    model_config = ENV_CONFIG

    media_root: str = "media"
    media_url: str = "/media"
