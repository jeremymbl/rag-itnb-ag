#!/usr/bin/env python3
"""
ITNB Content Ingestion to GroundX.

Reads preprocessed ITNB content from JSON and ingests into GroundX bucket.

Usage:
    python -m itnb_rag.ingest
"""

import json
import sys

from .config import config
from .groundx_utils import get_client, get_bucket_id, ingest_document


def load_documents() -> list:
    """
    Load preprocessed documents from JSON file.

    Returns:
        List of document dicts

    Raises:
        SystemExit: If JSON file doesn't exist or can't be read
    """
    try:
        with open(config.JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Loaded {len(data)} documents from {config.JSON_PATH}")
        return data
    except FileNotFoundError:
        print(f"Error: {config.JSON_PATH} not found")
        print("Run preprocessing first: python -m itnb_rag.preprocess")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading documents: {e}")
        sys.exit(1)


def ingest_all(bucket_id: str, documents: list) -> None:
    """
    Ingest all documents to GroundX bucket.

    Args:
        bucket_id: Target GroundX bucket ID
        documents: List of document dicts with url, title, content
    """
    client = get_client()
    success, fail = 0, 0

    with open(config.LOG_PATH, "w", encoding="utf-8") as log:
        for i, item in enumerate(documents, start=1):
            success_flag, status = ingest_document(
                client=client,
                bucket_id=bucket_id,
                url=item["url"],
                title=item.get("title", "")
            )

            if success_flag:
                log.write(f"{i}. {item['url']} — {status}\n")
                print(f"{i}/{len(documents)} {item['url']} — {status}")
                success += 1
            else:
                log.write(f"{i}. {item['url']} — {status}\n")
                print(f"{i}/{len(documents)} {item['url']} — {status}")
                fail += 1

    print("\nIngestion complete")
    print(f"   Success: {success}")
    print(f"   Failed:  {fail}")
    print(f"   Log:     {config.LOG_PATH}")


def main():
    """Main ingestion pipeline."""
    # Validate configuration
    config.validate()

    # Get bucket ID
    client = get_client()
    bucket_id = get_bucket_id(client)

    # Load and ingest documents
    documents = load_documents()
    ingest_all(bucket_id, documents)

    print("\nIngestion complete!")


if __name__ == "__main__":
    main()
