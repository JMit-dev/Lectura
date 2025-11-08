"""Configuration settings"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # OpenRouter API Configuration
    openrouter_api_key: str = ""  # Loaded from environment
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    gemini_model: str = "google/gemini-flash-1.5"

    # App Configuration
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"
    max_file_size: int = 10485760  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()  # type: ignore[call-arg]
