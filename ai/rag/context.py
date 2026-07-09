import logging
from typing import Optional

logger = logging.getLogger(__name__)


def build_context(chunks: list[dict], max_tokens: int = 2000) -> str:
    if not chunks:
        return ""

    seen = set()
    unique_chunks = []
    for chunk in chunks:
        content = chunk.get("content", "").strip()
        if content and content not in seen:
            seen.add(content)
            unique_chunks.append(chunk)

    parts = []
    total_chars = 0
    chars_per_token = 4

    for chunk in unique_chunks:
        content = chunk.get("content", "")
        chunk_cost = len(content) + 100
        if total_chars + chunk_cost > max_tokens * chars_per_token:
            break

        doc_name = chunk.get("metadata", {}).get("document", "unknown")
        parts.append(f"[Source: {doc_name}]\n{content}")
        total_chars += chunk_cost

    return "\n\n".join(parts)


def build_rag_result(
    answer: str,
    chunks: list[dict],
    confidence: Optional[float] = None,
) -> dict:
    sources = list(set(
        c.get("metadata", {}).get("document", "unknown")
        for c in chunks
        if c.get("metadata", {}).get("document")
    ))

    retrieved = [c.get("content", "") for c in chunks if c.get("content")]

    if confidence is None and chunks:
        scores = [1.0 - c.get("distance", 0) for c in chunks if c.get("distance") is not None]
        confidence = sum(scores) / len(scores) if scores else 0.0
    elif confidence is None:
        confidence = 0.0

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved,
        "confidence": round(confidence, 2),
        "reasoning_summary": f"Retrieved from {len(sources)} sources: {', '.join(sources)}" if sources else "No sources retrieved",
    }
