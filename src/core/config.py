from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: SecretStr

    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file = Path(__file__).parent.parent.parent / ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )

config = Config()