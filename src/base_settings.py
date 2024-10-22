from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    TG_KEY: str

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


base_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
