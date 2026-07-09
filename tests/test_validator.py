from ai.graph.state import GraphState
from ai.graph.nodes.validator import validator_node
from ai.models.schemas import RAGResult, OperationResult, ValidationResult


def test_validator_passes_with_valid_data():
    state = GraphState(
        merged_result="This is a valid response.",
        confidence=0.95,
    )
    result = validator_node(state)
    assert result["validation_result"].passed is True
    assert result["validation_result"].issues == []


def test_validator_fails_empty_response():
    state = GraphState(merged_result="")
    result = validator_node(state)
    assert result["validation_result"].passed is False
    assert "Empty response content" in result["validation_result"].issues


def test_validator_fails_low_confidence():
    state = GraphState(
        merged_result="Some response",
        confidence=0.1,
    )
    result = validator_node(state)
    assert result["validation_result"].passed is False


def test_validator_detects_missing_knowledge():
    state = GraphState(
        merged_result="I don't know the answer",
        confidence=0.8,
        rag_result=RAGResult(
            answer="I don't have information about that.",
        ),
    )
    result = validator_node(state)
    assert result["validation_result"].confidence == 0.8


def test_validator_with_error():
    state = GraphState(
        merged_result="Response",
        error="Something went wrong",
        confidence=0.9,
    )
    result = validator_node(state)
    assert result["validation_result"].passed is False
    assert any("error" in i.lower() for i in result["validation_result"].issues)
