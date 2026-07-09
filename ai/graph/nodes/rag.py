import logging

from ai.rag.pipeline import execute_rag
from ai.models.schemas import RAGResult
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def rag_node(state: GraphState) -> dict:
    logger.info(f"RAG node executing for: {state.user_query[:50]}...")

    history = state.conversation_history
    result = execute_rag(state.user_query, history)

    rag_result = RAGResult(
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
        retrieved_chunks=result.get("retrieved_chunks", []),
        confidence=result.get("confidence", 0.0),
        reasoning_summary=result.get("reasoning_summary", ""),
    )

    return {"rag_result": rag_result}
