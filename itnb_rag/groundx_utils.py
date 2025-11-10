"""
Shared GroundX utilities for ITNB RAG pipeline.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timezone

from groundx import GroundX, Document

from .config import config


def get_client() -> GroundX:
    """
    Create and return a configured GroundX client.
    Uses API key from config.
    """
    if not config.GROUNDX_API_KEY:
        raise ValueError("GROUNDX_API_KEY not set in environment")
    return GroundX(api_key=config.GROUNDX_API_KEY)


def get_bucket_id(client: GroundX) -> int:
    """
    Get bucket ID by name, creating it if it doesn't exist.

    Args:
        client: GroundX client instance

    Returns:
        bucket_id

    Raises:
        RuntimeError: If bucket creation fails
    """
    # Try to find by name
    print(f"Looking up bucket '{config.GROUNDX_BUCKET_NAME}'...")
    resp = client.buckets.list()
    for bucket in resp.buckets:
        if bucket.name == config.GROUNDX_BUCKET_NAME:
            print(f"Found bucket: {bucket.bucket_id}")
            return bucket.bucket_id

    # Create if not found
    print(f"Bucket not found. Creating '{config.GROUNDX_BUCKET_NAME}'...")
    try:
        response = client.buckets.create(name=config.GROUNDX_BUCKET_NAME)
        bucket_id = response.bucket.bucket_id
        print(f"Created bucket: {bucket_id}")
        return bucket_id
    except Exception as e:
        raise RuntimeError(f"Failed to create bucket '{config.GROUNDX_BUCKET_NAME}': {e}")


def extract_context_and_sources(
    search_resp,
    top_k: int = None
) -> Tuple[str, List[Dict]]:
    """
    Extract combined context text and source information from search response.

    Args:
        search_resp: GroundX search response object
        top_k: Number of top results to include (uses config.TOP_K if None)

    Returns:
        Tuple of (combined_text, sources_list)
        - combined_text: Concatenated text from search results
        - sources_list: List of dicts with keys: title, sourceUrl, suggestedText, text, score
    """
    if top_k is None:
        top_k = config.TOP_K

    if search_resp is None:
        return "", []

    # Get combined text from search response
    combined_text = search_resp.search.text or ""
    if combined_text and len(combined_text) > config.MAX_CONTEXT_CHARS:
        combined_text = combined_text[:config.MAX_CONTEXT_CHARS] + "\n...[TRUNCATED CONTEXT]...\n"

    # Extract individual results for sources
    sources = []
    for result in search_resp.search.results[:top_k]:
        # search_data is a plain dict
        search_data = result.search_data or {}

        source = {
            "score": result.score,
            "searchData": search_data,
            "title": search_data.get("title"),
            "sourceUrl": search_data.get("url"),
            "suggestedText": result.suggested_text,
            "text": result.text,
        }
        sources.append(source)

    # If no combined text available, build from individual results
    if not combined_text:
        pieces = []
        for s in sources:
            if s["suggestedText"]:
                pieces.append(s["suggestedText"])
            elif s["text"]:
                pieces.append(s["text"][:3000])

        combined = "\n\n".join(pieces)
        if len(combined) > config.MAX_CONTEXT_CHARS:
            combined = combined[:config.MAX_CONTEXT_CHARS] + "\n...[TRUNCATED]...\n"
        combined_text = combined

    return combined_text, sources


def ingest_document(
    client: GroundX,
    bucket_id: int,
    url: str,
    title: str = "",
    metadata: Dict = None
) -> Tuple[bool, str]:
    """
    Ingest a single document into GroundX.
    GroundX fetches the content from the URL.

    Args:
        client: GroundX client instance
        bucket_id: Target bucket ID
        url: Source URL for the document
        title: Document title
        metadata: Additional metadata dict

    Returns:
        Tuple of (success: bool, status_message: str)
    """
    file_name = url.replace("https://", "").replace("/", "_") + ".txt"

    search_data = {
        "url": url,
        "title": title,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }

    if metadata:
        search_data.update(metadata)

    try:
        ingest_resp = client.ingest(
            documents=[
                Document(
                    bucket_id=bucket_id,
                    file_name=file_name,
                    file_path=url,
                    file_type="txt",
                    search_data=search_data,
                )
            ]
        )
        status = ingest_resp.ingest.status or "unknown"
        return True, status
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    client = get_client()
    bucket_id = get_bucket_id(client)
    print(f"Bucket ID: {bucket_id}")