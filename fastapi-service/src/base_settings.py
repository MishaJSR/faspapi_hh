from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    def get_database_url(self):
        return URL.create(
            drivername=f"postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            password=self.POSTGRES_PASSWORD,
            username=self.POSTGRES_USER,
            database=self.POSTGRES_DB,
            port=self.POSTGRES_PORT,
        ).render_as_string(hide_password=False)



base_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
