"""
ITNB RAG - Retrieval-Augmented Generation pipeline for ITNB website content.

This package provides a complete RAG pipeline:
- Web crawling and preprocessing (preprocess.py)
- Document ingestion to GroundX (ingest.py)
- Interactive RAG chat interface (chat.py)

Shared utilities:
- config: Centralized configuration management
- groundx_utils: GroundX API helpers
- text_processing: Text cleaning and formatting
"""

__version__ = "0.1.0"

from . import config
from . import groundx_utils
from . import text_processing

__all__ = ["config", "groundx_utils", "text_processing"]
