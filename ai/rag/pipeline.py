import logging
from pathlib import Path

from ai.config.settings import get_settings
from ai.rag.retriever import retrieve
from ai.rag.context import build_context, build_rag_result
from ai.prompts.registry import load_prompt

logger = logging.getLogger(__name__)


def execute_rag(query: str, history: list = None, filter_dict: dict = None) -> dict:
    settings = get_settings()

    chunks = retrieve(query, filter_dict)
    context = build_context(chunks, max_tokens=2000)
    history_text = _format_history(history or [])

    rag_prompt = load_prompt("rag")
    prompt = rag_prompt.format(context=context, history=history_text, question=query)

    answer = _call_llm(prompt)

    result = build_rag_result(answer, chunks)
    logger.info(f"RAG executed | confidence={result['confidence']} | sources={result['sources']}")
    return result


def _format_history(history: list) -> str:
    if not history:
        return "No previous conversation."
    lines = []
    for msg in history[-5:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        lines.append(f"{role.capitalize()}: {content}")
    return "\n".join(lines)


def _call_llm(prompt: str) -> str:
    from langchain_ollama import ChatOllama
    settings = get_settings()
    llm = ChatOllama(
        model=settings.ollama_model_name,
        base_url=settings.ollama_base_url,
        temperature=0.1,
    )
    response = llm.invoke(prompt)
    return response.content
