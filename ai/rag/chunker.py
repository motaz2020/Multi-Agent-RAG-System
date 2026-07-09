import logging
from ai.config.settings import get_settings

logger = logging.getLogger(__name__)


def chunk_document(content: str, metadata: dict) -> list[dict]:
    settings = get_settings()
    chunk_size = settings.chunk_size
    chunk_overlap = settings.chunk_overlap

    chunks = []
    start = 0
    content_len = len(content)
    chunk_index = 0

    while start < content_len:
        end = min(start + chunk_size, content_len)
        if end < content_len:
            last_newline = content.rfind("\n", start, end)
            if last_newline > start + chunk_size // 2:
                end = last_newline

        chunk_text = content[start:end].strip()
        if chunk_text:
            chunk_meta = dict(metadata)
            chunk_meta["chunk_index"] = chunk_index
            chunk_meta["char_start"] = start
            chunk_meta["char_end"] = end
            chunks.append({"content": chunk_text, "metadata": chunk_meta})
            chunk_index += 1

        step = chunk_size - chunk_overlap
        if step <= 0:
            step = chunk_size // 2
        start += step

    logger.info(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks
