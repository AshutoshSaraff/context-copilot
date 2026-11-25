
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = PROJECT_ROOT / "backend"


class Settings(BaseSettings):
    gemini_api_key: str = ""

    gemini_model: str = "gemini-3.8-flash"
    embedding_model: str = "gemini-embedding-001"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5

    chroma_persist_dir: Path = (
        BACKEND_DIR / "storage" / "chroma"
    )

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
