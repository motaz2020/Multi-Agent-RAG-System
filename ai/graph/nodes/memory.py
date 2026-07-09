import logging

from ai.models.schemas import ConversationMessage, MessageRole
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def memory_loader_node(state: GraphState) -> dict:
    logger.info(f"Memory loader for thread: {state.thread_id}")
    return {}


def memory_saver_node(state: GraphState) -> dict:
    logger.info(f"Memory saver for thread: {state.thread_id}")

    history = list(state.conversation_history) if state.conversation_history else []

    history.append(ConversationMessage(
        role=MessageRole.user,
        content=state.user_query,
    ).model_dump())

    if state.final_response:
        history.append(ConversationMessage(
            role=MessageRole.assistant,
            content=state.final_response,
        ).model_dump())

    if len(history) > 50:
        history = history[-50:]

    return {"conversation_history": history}
