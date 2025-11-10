#!/usr/bin/env python3
"""
ITNB RAG Chat CLI.

Interactive chat interface that queries GroundX for relevant context,
then calls an OpenAI-compatible LLM for final answers.

Usage:
    python -m itnb_rag.chat
"""

import sys
import textwrap
from typing import Optional, Tuple

import requests

from .config import config
from .groundx_utils import get_client, get_bucket_id, extract_context_and_sources


def build_system_instruction(context_text: str) -> str:
    """
    Build system message with embedded context for LLM.

    Args:
        context_text: Retrieved context from GroundX

    Returns:
        System message with instructions and context
    """
    system_instruction = textwrap.dedent(
        """You are a highly knowledgeable assistant. Your primary role is to answer user questions using the provided document context.
- If the context contains the answer, respond concisely and include a short 'Sources:' section listing titles and URLs used.
- If the context does not contain the answer, say you don't know and avoid hallucinating.
- Be technical, precise, and concise for a developer audience.
"""
    )
    system_with_context = system_instruction + "\n===\n" + context_text + "\n===\n"

    # Ensure system message isn't too large
    max_sys_len = 20000
    if len(system_with_context) > max_sys_len:
        system_with_context = system_with_context[:max_sys_len] + "\n...[TRUNCATED CONTEXT]...\n"

    return system_with_context


def call_llm(system_message: str, user_message: str) -> Tuple[Optional[str], dict]:
    """
    Call OpenAI-compatible LLM endpoint.

    Args:
        system_message: System prompt with context
        user_message: User's question

    Returns:
        Tuple of (content_text or None, raw_response_dict)
    """
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    url_chat = config.OPENAI_API_BASE.rstrip("/") + "/v1/chat/completions"

    payload = {
        "model": config.OPENAI_MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": config.LLM_MAX_TOKENS,
        "temperature": config.LLM_TEMPERATURE,
    }

    try:
        r = requests.post(
            url_chat,
            headers=headers,
            json=payload,
            timeout=config.REQUEST_TIMEOUT
        )
    except Exception as e:
        debug = {"error": f"HTTP exception when calling chat endpoint: {e}"}
        return None, debug

    if r.status_code == 200:
        try:
            j = r.json()
            content = j["choices"][0]["message"]["content"]
            return content, j
        except Exception:
            return None, {"error": "unexpected JSON shape", "response_text": r.text}
    else:
        debug = {"status_code": r.status_code, "response_text": r.text}
        return None, debug


def print_sources(sources: list):
    """
    Display source citations from GroundX results.

    Args:
        sources: List of source dicts
    """
    if not sources:
        print("\n(Sources: none returned)\n")
        return

    print("\nSources used:")
    for i, s in enumerate(sources, start=1):
        title = s.get("title") or "(no title)"
        url = s.get("sourceUrl") or "(no url)"
        score = s.get("score")
        print(f" [{i}] {title} — {url} (score={score})")


def interactive_loop(bucket_id: str):
    """
    Main interactive chat loop.

    Args:
        bucket_id: GroundX bucket to search
    """
    client = get_client()

    print("ITNB RAG CLI — ask questions about the ingested ITNB content.")
    print("Commands: /help /exit /quit /raw (shows raw combined context)")
    print()

    while True:
        try:
            q = input("itnb> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return

        if not q:
            continue

        if q.lower() in ("/exit", "/quit"):
            print("Bye.")
            return

        if q.lower() == "/help":
            print("Ask any question about ITNB content.")
            print("Example: 'What cloud services do they offer for healthcare?'")
            continue

        # Perform GroundX search
        try:
            search_resp = client.search.content(id=bucket_id, query=q)
            combined_text, sources = extract_context_and_sources(search_resp, top_k=config.TOP_K)
        except Exception as e:
            print(f"Search error: {e}")
            continue

        # Debug command to show raw context
        if q.lower() == "/raw":
            print("\n--- RAW COMBINED CONTEXT ---\n")
            display_text = combined_text[:20000]
            if len(combined_text) > 20000:
                display_text += "\n...[TRUNCATED]"
            print(display_text)
            print("\n--- END ---\n")
            continue

        if not combined_text:
            print("No context was retrieved for that query. I'll still try to answer, but I may be less precise.\n")

        system_msg = build_system_instruction(combined_text)
        user_msg = q + "\n\nPlease answer using only the provided document context. At the end, include a short 'Sources:' list."

        print(f"\n[1/2] Retrieved context length: {len(combined_text):,} chars")
        print("[2/2] Sending to LLM... (this may take a few seconds)")

        answer, raw = call_llm(system_msg, user_msg)

        if answer is None:
            print("\nLLM call failed. Debug info:")
            print(raw)
            print("\nYou can try reducing context size or checking your OPENAI_MODEL_NAME and OPENAI_API_BASE.")
            continue

        print("\n--- Answer ---\n")
        print(answer.strip())
        print("\n--- End Answer ---")
        print_sources(sources)


def main():
    """Main chat application entry point."""
    # Validate configuration
    config.validate()

    # Get bucket
    client = get_client()
    try:
        bucket_id = get_bucket_id(client)
    except RuntimeError as e:
        print(f"Error: {e}")
        print("   Make sure ingestion completed and bucket exists.")
        print("   Run: python -m itnb_rag.ingest")
        sys.exit(1)

    print(f"Using bucket id: {bucket_id}")
    print(f"Using LLM model: {config.OPENAI_MODEL_NAME} @ {config.OPENAI_API_BASE}")
    print()

    interactive_loop(bucket_id)


if __name__ == "__main__":
    main()
