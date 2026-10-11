"""TEMPLATE: settings from environment variables (12-factor config).

Shape: one Settings class -> read once -> import `settings` everywhere.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Each field = one env var (case-insensitive). Default is used if the var is missing.
    app_name: str = "items-api"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"

    # Also read a local .env file (handy in dev; in K8s, real env vars win).
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache  # build Settings once, reuse the same object (cheap + consistent)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
