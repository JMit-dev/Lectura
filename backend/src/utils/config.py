"""Configuration settings"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    gemini_api_key: str
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"
    max_file_size: int = 10485760  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
