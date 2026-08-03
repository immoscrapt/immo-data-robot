import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "IMMO DATA ROBOT"
    secret_key: str = "dev-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 7

    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./immo_data_robot.db")
    postgres_db: str = "immo_data_robot"
    postgres_user: str = "immo"
    postgres_password: str = "change_me"


settings = Settings()
