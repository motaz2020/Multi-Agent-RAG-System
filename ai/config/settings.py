from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ollama_model_name: str = "qwen2.5:3b-instruct-q3_K_S"
    ollama_base_url: str = "http://localhost:11434"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    collection_name: str = "restaurant_documents"
    chroma_persist_dir: str = "data/chroma"

    top_k: int = 4
    chunk_size: int = 500
    chunk_overlap: int = 100

    confidence_threshold: float = 0.7

    sqlite_database: str = "data/checkpointer.db"

    log_level: str = "INFO"

    host: str = "0.0.0.0"
    port: int = 8000

    data_directory: str = "data"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
