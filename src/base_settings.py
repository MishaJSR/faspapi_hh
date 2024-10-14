import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    TG_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_database_url(self):
        return URL.create(
            drivername=f"postgresql+asyncpg",
            host=self.DB_HOST,
            password=self.DB_PASS,
            username=self.DB_USER,
            database=self.DB_NAME,
            port=self.DB_PORT,
        ).render_as_string(hide_password=False)

    def get_api_token(self):
        return self.TG_KEY


base_settings = Settings()


