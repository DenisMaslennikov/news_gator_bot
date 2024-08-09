from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    # Настройки подключения к базе данных
    postgres_db: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_port: str

    # URL RabbitMQ
    rabbitmq_url: str

    # Telegram
    telegram_token: str

    # Корневая директория проекта
    base_dir: Path = Field(default=Path(__file__).resolve().parent.parent)

    model_config = SettingsConfigDict()

    @property
    def async_database_uri(self) -> str:
        """Получение асинхронного uri для подключения к базе данных."""
        return (
            f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:'
            f'{self.postgres_port}/{self.postgres_db}'
        )
    @property
    def database_uri(self) -> str:
        """Получение синхронного uri для подключения к базе данных."""
        return (
            f'postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:'
            f'{self.postgres_port}/{self.postgres_db}'
        )


settings = Settings()
