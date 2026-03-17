from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://localhost/interviewos"

    # JWT Authentication
    JWT_SECRET: str = "super-secret-local-jwt-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # AI
    OPENAI_API_KEY: str = "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"
    GEMINI_API_KEY: str = "AIzaSyD60Hcgbs7fgWvWLmWFGEMceEVBb51wokY"
    AI_PROVIDER: str = "anthropic"  # openai | anthropic

    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "http://localhost:8080,http://localhost:5173,http://localhost:3000,http://localhost:8081,http://localhost:8082"

    # Code sandbox
    SANDBOX_TIMEOUT: int = 10

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
