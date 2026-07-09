import logging

from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def merge_node(state: GraphState) -> dict:
    logger.info("Merge node executing")

    parts = []

    if state.rag_result and state.rag_result.answer:
        parts.append(state.rag_result.answer)

    if state.operation_result and state.operation_result.status == "success":
        op_output = _format_operation_result(state.operation_result)
        if op_output:
            parts.append(op_output)

    if not parts:
        return {"merged_result": "", "confidence": 0.0}

    merged = "\n\n".join(parts)
    confidence = _compute_confidence(state)

    return {"merged_result": merged, "confidence": confidence, "sources": _collect_sources(state)}


def _format_operation_result(op_result) -> str:
    if op_result.tool_name == "book_table":
        payload = op_result.payload
        if payload.get("status") == "confirmed":
            return f"Reservation confirmed! Your reservation ID is {payload.get('reservation_id')}. We look forward to serving you at our {payload.get('branch', '')} branch on {payload.get('date', '')} at {payload.get('time', '')}."
        else:
            return f"Reservation could not be completed: {payload.get('error', 'Unknown error')}"

    if op_result.tool_name == "check_table_availability":
        payload = op_result.payload
        if payload.get("available"):
            return f"Tables are available at {payload.get('branch', '')} on {payload.get('date', '')} at {payload.get('time', '')}. {payload.get('remaining_tables', 0)} table(s) remaining."
        else:
            return f"Sorry, no tables are available at {payload.get('branch', '')} on {payload.get('date', '')} at {payload.get('time', '')}."

    if op_result.tool_name == "get_today_special":
        payload = op_result.payload
        return f"Today's special at {payload.get('branch', '')}: {payload.get('meal', '')} - ${payload.get('price', '')}\n{payload.get('description', '')}"

    return str(op_result.payload) if op_result.payload else ""


def _compute_confidence(state: GraphState) -> float:
    confidence = 1.0
    if state.rag_result:
        confidence = min(confidence, state.rag_result.confidence)
    if state.operation_result and state.operation_result.status != "success":
        confidence *= 0.8
    return round(confidence, 2)


def _collect_sources(state: GraphState) -> list:
    sources = []
    if state.rag_result:
        sources.extend(state.rag_result.sources)
    if state.operation_result and state.operation_result.tool_name:
        sources.append(f"tool:{state.operation_result.tool_name}")
    return list(set(sources))
