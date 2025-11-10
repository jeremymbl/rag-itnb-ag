#!/usr/bin/env python3
"""
ITNB Website Crawler and Preprocessor.

Crawls the ITNB website using crawl4ai, extracts and cleans content,
then saves results to JSON and TXT formats for ingestion.

Usage:
    python -m itnb_rag.preprocess
"""

import asyncio
import json
import os
from typing import List, Dict

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter, ContentTypeFilter

from .config import config
from .text_processing import md_to_text


async def crawl_itnb() -> List[Dict]:
    """
    Crawl ITNB website and extract content.

    Returns:
        List of dicts with keys: url, title, content
    """
    # Filters: only /en pages on itnb.ch, only text/html
    filter_chain = FilterChain([
        URLPatternFilter(patterns=[
            "https://www.itnb.ch/en*",
            "*itnb.ch/en*"
        ]),
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=config.CRAWL_MAX_DEPTH,
            include_external=False,
            filter_chain=filter_chain,
            max_pages=config.CRAWL_MAX_PAGES
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    results = []
    print(f"Starting crawl from: {config.CRAWL_START_URL}")
    print(f"Max depth: {config.CRAWL_MAX_DEPTH}, Max pages: {config.CRAWL_MAX_PAGES}")

    async with AsyncWebCrawler() as crawler:
        crawl_results = await crawler.arun(url=config.CRAWL_START_URL, config=run_conf)

        for r in crawl_results:
            # Prefer "fit_markdown" if present; else raw markdown
            md = r.markdown.fit_markdown or r.markdown.raw_markdown or r.markdown
            text = md_to_text(md)

            results.append({
                "url": r.url,
                "title": (r.metadata.get("title") if r.metadata else "") or "",
                "content": text
            })

    print(f"Crawled {len(results)} pages")
    return results


def persist(pages: List[Dict]) -> None:
    """
    Save crawled pages to JSON and TXT files.

    Args:
        pages: List of page dicts (url, title, content)
    """
    os.makedirs(config.DATA_DIR, exist_ok=True)

    # Save as structured JSON
    with open(config.JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    # Save as flat corpus file (useful for embeddings)
    with open(config.TXT_PATH, "w", encoding="utf-8") as f:
        for p in pages:
            if not p["content"]:
                continue
            f.write(f"### {p['url']}\n{p['title']}\n{p['content']}\n\n")

    print(f"Saved {len(pages)} pages")
    print(f"JSON: {config.JSON_PATH}")
    print(f"TXT:  {config.TXT_PATH}")


async def main():
    """Main preprocessing pipeline."""
    pages = await crawl_itnb()
    persist(pages)
    print("\nPreprocessing complete!")


if __name__ == "__main__":
    asyncio.run(main())
