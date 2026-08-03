import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-1.5-flash"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    # Автоматически считывает переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()
