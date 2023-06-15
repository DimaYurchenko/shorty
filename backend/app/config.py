from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    db_url: str = "sqlite:///./shorty.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
