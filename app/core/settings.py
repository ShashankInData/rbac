import secrets
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional



class Settings(BaseSettings):
    # ── JWT Settings ──
    # In production, omit a default so that missing both env and .env raises an error.
    JWT_SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Signing secret for JWTs. "
                    "If not provided via env/.env, a random one is generated."
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ── Database Settings ──
    CHROMA_PERSIST_DIRECTORY: str = "data/chroma"

    # ── API Settings ──
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RBAC Chatbot"
    PROJECT_VERSION: str = "0.1.0"

    # ── LLM / Groq Settings ──
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ── HuggingFace Settings ──
    HUGGINGFACE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
