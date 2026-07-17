import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Multi-Agent AI Chatbot"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API Auth
    JWT_SECRET: str = "supersecretkey"  # change in prod
    JWT_ALGORITHM: str = "HS256"

    # Database
    MONGO_URI: str = "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = "ai_chatbot"

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://11.0.0.109:9200"
    
    # PostgreSQL
    POSTGRESQL_URL: Optional[str] = None

    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    OLLAMA_URL: str = "http://localhost:11434"
    ROUTER_MODEL: str = "qwen3:8b"
    CHAT_MODEL: str = "qwen3:8b"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
