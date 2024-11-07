from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Settings(BaseSettings):
    REDISHOST: str
    REDISPORT: int
    REDISPASSWORD: str
    USE_REDIS: bool
    TG_KEY: str
    GRPC_HOST: str
    AMPQ_HOST: str

    def get_redis_storage(self):
        if self.REDISPASSWORD:
            return f"redis://:{self.REDISPASSWORD}@{self.REDISHOST}:{self.REDISPORT}/0"
        else:
            return f"redis://{self.REDISHOST}:{self.REDISPORT}/0"

    def is_use_redis(self):
        return True if self.USE_REDIS else False

    def get_token(self):
        return self.TG_KEY

    def get_grpc_host(self):
        return self.GRPC_HOST

    def get_ampq_host(self):
        return self.AMPQ_HOST


base_settings = Settings(_env_file=".env_dev", _env_file_encoding="utf-8")
