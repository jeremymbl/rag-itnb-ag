"""
Main entry point when running `python -m itnb_rag`
Shows usage information and available commands.
"""

import sys


def show_usage():
    """Display usage information."""
    print("""
ITNB RAG Pipeline
=================

Usage:
  python -m itnb_rag.preprocess    # Crawl and preprocess ITNB website
  python -m itnb_rag.ingest        # Ingest content to GroundX
  python -m itnb_rag.chat          # Start interactive chat

Run the commands in order:
  1. preprocess - Crawls itnb.ch and saves to data/
  2. ingest     - Uploads to GroundX vector database
  3. chat       - Interactive RAG Q&A interface

Configuration:
  Copy .env.example to .env and configure your API keys.

For more information, see README.md
""")


if __name__ == "__main__":
    show_usage()
    sys.exit(0)
