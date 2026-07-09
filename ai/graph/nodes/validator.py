import logging

from ai.config.settings import get_settings
from ai.models.schemas import ValidationResult
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def validator_node(state: GraphState) -> dict:
    logger.info("Validation node executing")

    issues = []

    if not state.merged_result or not state.merged_result.strip():
        issues.append("Empty response content")

    confidence = state.confidence or 0.0
    threshold = get_settings().confidence_threshold

    if confidence < threshold:
        issues.append(f"Low confidence: {confidence} < {threshold}")

    if state.error:
        issues.append(f"Execution error: {state.error}")

    if state.rag_result and state.rag_result.answer:
        if "I don't have" in state.rag_result.answer.lower() and "don't know" in state.rag_result.answer.lower():
            issues.append("Response indicates missing knowledge")

    passed = len(issues) == 0
    validated = state.merged_result or ""

    result = ValidationResult(
        passed=passed,
        issues=issues,
        confidence=confidence,
        validated_response=validated,
    )

    logger.info(f"Validation {'passed' if passed else 'failed'}: {issues}")
    return {"validation_result": result}
