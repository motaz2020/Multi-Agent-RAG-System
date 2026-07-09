import logging
from functools import lru_cache

from ai.config.settings import get_settings
from ai.rag.embeddings import get_embedding_function
from ai.rag.indexer import get_chroma_client

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_retrieval_components():
    settings = get_settings()
    client = get_chroma_client()
    collection = client.get_collection(settings.collection_name)
    embedder = get_embedding_function()
    return collection, embedder, settings.top_k


def retrieve(query: str, filter_dict: dict = None) -> list[dict]:
    try:
        collection, embedder, top_k = _get_retrieval_components()
        query_embedding = embedder.embed_query(query)

        where = filter_dict if filter_dict else None

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        chunks = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                chunks.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0,
                })

        logger.info(f"Retrieved {len(chunks)} chunks for query: {query[:50]}...")
        return chunks

    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return []
