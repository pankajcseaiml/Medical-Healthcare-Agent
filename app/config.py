"""
Application Configuration and Environment Settings.
Loads and validates settings from environment variables or .env file.
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    app_name: str = "Medical Healthcare Multi-Agent Assistant"
    app_version: str = "1.0.0"

    # Groq API Configuration
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    request_timeout: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    @property
    def is_groq_configured(self) -> bool:
        """Check if Groq API key is present and not a dummy placeholder."""
        if not self.groq_api_key:
            return False
        stripped = self.groq_api_key.strip()
        if not stripped or stripped.startswith("gsk_your_actual"):
            return False
        return True


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
