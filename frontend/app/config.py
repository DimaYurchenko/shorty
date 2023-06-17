from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8001
    api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
