"""PRACTICE: settings from environment variables.
Reference answer: ../../../fastapi-app/app/config.py  (look only after trying)

Shape:
  1. import BaseSettings, SettingsConfigDict (pydantic_settings) and lru_cache
  2. class Settings(BaseSettings): app_name, debug, database_url (with defaults)
  3. model_config -> read .env, ignore extra vars
  4. get_settings() cached with @lru_cache
  5. settings = get_settings()
"""
# TODO
