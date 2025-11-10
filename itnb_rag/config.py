"""
Centralized configuration management for ITNB RAG pipeline.
Loads configuration from environment variables.
"""

import sys
from os import getenv
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Config:
    """Centralized configuration for ITNB RAG pipeline."""

    # GroundX Configuration (from .env)
    GROUNDX_API_KEY: str = getenv("GROUNDX_API_KEY", "")
    GROUNDX_BUCKET_NAME: str = getenv("GROUNDX_BUCKET_NAME", "itnb_website")

    # OpenAI-compatible LLM Configuration (from .env)
    OPENAI_API_KEY: str = getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = getenv("OPENAI_API_BASE", "")
    OPENAI_MODEL_NAME: str = getenv("OPENAI_MODEL_NAME", "inference-llama4-maverick")

    # LLM Parameters (hardcoded defaults)
    LLM_MAX_TOKENS: int = 512
    LLM_TEMPERATURE: float = 0.0
    REQUEST_TIMEOUT: int = 60

    # RAG Parameters (hardcoded defaults)
    TOP_K: int = 3
    MAX_CONTEXT_CHARS: int = 100000

    # Preprocessing Configuration (hardcoded defaults)
    CRAWL_START_URL: str = "https://www.itnb.ch/en"
    CRAWL_MAX_DEPTH: int = 2
    CRAWL_MAX_PAGES: int = 100

    # Data Paths (hardcoded defaults)
    DATA_DIR: str = "data"
    JSON_PATH: str = "data/itnb_texts.json"
    TXT_PATH: str = "data/itnb_corpus.txt"
    LOG_PATH: str = "data/ingest_log.txt"

    @classmethod
    def validate(cls) -> None:
        """
        Validate required configuration.
        Raises SystemExit if critical config is missing.
        """
        missing = []

        if not cls.GROUNDX_API_KEY:
            missing.append("GROUNDX_API_KEY")
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.OPENAI_API_BASE:
            missing.append("OPENAI_API_BASE")

        if missing:
            print("Missing required environment variables:", ", ".join(missing))
            print("Put them in a .env file or export them in your shell.")
            print("See .env.example for required variables.")
            sys.exit(1)

    @classmethod
    def display_config(cls) -> None:
        """Display current configuration (without exposing secrets)."""
        print("Current Configuration:")
        print(f"  GroundX Bucket: {cls.GROUNDX_BUCKET_NAME}")
        print(f"  LLM Model: {cls.OPENAI_MODEL_NAME}")
        print(f"  LLM API Base: {cls.OPENAI_API_BASE}")
        print(f"  TOP_K: {cls.TOP_K}")
        print(f"  Max Context: {cls.MAX_CONTEXT_CHARS:,} chars")
        print(f"  Temperature: {cls.LLM_TEMPERATURE}")
        print(f"  Max Tokens: {cls.LLM_MAX_TOKENS}")


# Convenience instance
config = Config()
