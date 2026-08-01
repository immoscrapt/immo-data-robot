from pathlib import Path
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "IMMO DATA ROBOT"
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 7

    database_url: str = Field(..., env="DATABASE_URL")
    postgres_db: str = Field("immo_data_robot", env="POSTGRES_DB")
    postgres_user: str = Field("immo", env="POSTGRES_USER")
    postgres_password: str = Field("change_me", env="POSTGRES_PASSWORD")

    class Config:
        env_file = BASE_DIR.parent.parent / ".env"


settings = Settings()
