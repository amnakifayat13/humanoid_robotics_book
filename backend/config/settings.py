import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "https://your-cluster-url.qdrant.tech")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Google Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # OpenAI Configuration (fallback option)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Processing Configuration
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "10"))

    # Source Directory
    DOCS_DIR: str = os.getenv("DOCS_DIR", "../../book-site/docs")

    # Qdrant Collection Name
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "documentation_book")

    class Config:
        env_file = ".env"


# Create a single instance of settings
settings = Settings()