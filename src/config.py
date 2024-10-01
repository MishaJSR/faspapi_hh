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

    model_config = SettingsConfigDict(env_file=".env_dev")

    def get_database_url(self):
        return URL.create(
            drivername=f"postgresql+asyncpg",
            host=self.DB_HOST,
            password=self.DB_PASS,
            username=self.DB_USER,
            database=self.DB_NAME,
            port=self.DB_PORT,
        ).render_as_string(hide_password=False)

# DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
# DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
# DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
# DB_USER_TEST = os.environ.get("DB_USER_TEST")
# DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

# REDIS_HOST = os.environ.get("REDIS_HOST")
# REDIS_PORT = os.environ.get("REDIS_PORT")
