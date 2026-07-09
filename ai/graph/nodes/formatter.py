import logging

from langchain_ollama import ChatOllama

from ai.config.settings import get_settings
from ai.prompts.registry import load_prompt
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def formatter_node(state: GraphState) -> dict:
    logger.info("Formatter node executing")

    content = ""
    sources_text = ""
    tool_text = ""

    if state.merged_result:
        content = state.merged_result

    if state.rag_result and state.rag_result.sources:
        sources_text = "\n".join(f"- {s}" for s in state.rag_result.sources)

    if state.operation_result and state.operation_result.tool_name != "none":
        tool_text = f"Tool: {state.operation_result.tool_name} ({state.operation_result.status})"

    conf = state.confidence or 0.0
    srcs = state.sources or []

    if state.validation_result and not state.validation_result.passed:
        fallback = _build_fallback_response(state)
        return {
            "final_response": fallback,
            "confidence": state.validation_result.confidence,
            "sources": srcs,
        }

    settings = get_settings()
    try:
        prompt_template = load_prompt("formatter")
        prompt = prompt_template.format(
            content=content,
            sources=sources_text,
            tool_results=tool_text,
        )

        llm = ChatOllama(
            model=settings.ollama_model_name,
            base_url=settings.ollama_base_url,
            temperature=0.1,
        )

        response = llm.invoke(prompt)
        formatted = response.content
    except Exception as e:
        logger.warning(f"Formatter LLM failed, using raw content: {e}")
        formatted = content

    return {"final_response": formatted, "confidence": conf, "sources": srcs}


def _build_fallback_response(state: GraphState) -> str:
    parts = []
    if state.rag_result and state.rag_result.answer:
        parts.append(state.rag_result.answer)
    if state.operation_result and state.operation_result.status == "success":
        parts.append("The operation was completed successfully.")

    if not parts:
        return "I received your request but encountered some issues processing it. Could you please rephrase?"

    return "\n\n".join(parts)
