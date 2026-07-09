import os
import logging
from pathlib import Path
from typing import Optional

import chromadb
import chromadb.errors
from chromadb.config import Settings as ChromaSettings

from ai.config.settings import get_settings
from ai.rag.loader import load_documents, preprocess_text
from ai.rag.chunker import chunk_document
from ai.rag.embeddings import get_embedding_function

logger = logging.getLogger(__name__)


def get_chroma_client():
    settings = get_settings()
    persist_dir = Path(settings.chroma_persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(persist_dir),
        settings=ChromaSettings(anonymized_telemetry=False),
    )


def get_or_create_collection():
    client = get_chroma_client()
    settings = get_settings()
    try:
        collection = client.get_collection(settings.collection_name)
        logger.info(f"Collection '{settings.collection_name}' already exists ({collection.count()} documents)")
        return collection
    except (ValueError, chromadb.errors.NotFoundError):
        logger.info(f"Creating collection '{settings.collection_name}'")
        return client.create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"},
        )


def index_documents(data_dir: Optional[str] = None) -> int:
    settings = get_settings()
    data_dir = data_dir or settings.data_directory

    documents = load_documents(data_dir)
    if not documents:
        logger.warning("No documents found to index")
        return 0

    embedder = get_embedding_function()
    collection = get_or_create_collection()

    total_chunks = 0
    for doc in documents:
        cleaned = preprocess_text(doc["content"])
        chunks = chunk_document(cleaned, doc["metadata"])

        for chunk in chunks:
            chunk_id = f"{doc['metadata']['document']}_chunk_{chunk['metadata']['chunk_index']}"
            embedding = embedder.embed_query(chunk["content"])

            collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk["content"]],
                metadatas=[chunk["metadata"]],
            )
            total_chunks += 1

    logger.info(f"Indexed {total_chunks} chunks from {len(documents)} documents")
    return total_chunks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    count = index_documents()
    print(f"Indexed {count} chunks")
