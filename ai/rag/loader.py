import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_documents(data_dir: str) -> list[dict]:
    documents = []
    data_path = Path(data_dir)
    if not data_path.exists():
        logger.warning(f"Data directory not found: {data_dir}")
        return documents

    for file_path in data_path.glob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8")
            doc = {
                "content": content,
                "metadata": {
                    "document": file_path.stem,
                    "file_name": file_path.name,
                    "source": str(file_path),
                },
            }
            documents.append(doc)
            logger.info(f"Loaded document: {file_path.name} ({len(content)} chars)")
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")

    return documents


def preprocess_text(text: str) -> str:
    import re

    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text
