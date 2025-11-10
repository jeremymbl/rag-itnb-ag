"""
Text processing utilities for ITNB RAG pipeline.
Converts markdown to plain text for ingestion.
"""

import re
import mistune
from bs4 import BeautifulSoup


def md_to_text(md: str) -> str:
    """
    Convert Markdown to plain text suitable for ingestion.

    Uses mistune to parse markdown to HTML, then BeautifulSoup to extract
    clean text.

    Args:
        md: Markdown text

    Returns:
        Cleaned plain text with normalized whitespace
    """
    if not md:
        return ""

    # Parse markdown to HTML using mistune
    html = mistune.html(md)

    # Extract text from HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


