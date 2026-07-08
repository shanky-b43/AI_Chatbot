from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Multi-Agent AI Chatbot"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API Auth
    JWT_SECRET: str = "supersecretkey"  # change in prod
    JWT_ALGORITHM: str = "HS256"

    # Database
    POSTGRES_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ai_chatbot"

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://11.0.0.109:9200"

    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_URL: str = "http://localhost:11434"
    ROUTER_MODEL: str = "qwen2.5:3b"
    CHAT_MODEL: str = "qwen3:8b"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
