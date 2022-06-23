from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug_mode = True
    server_url = "http://localhost:8000"
    sqlalchemy_database_url = "sqlite:///webrtc-360.sqlite3"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
