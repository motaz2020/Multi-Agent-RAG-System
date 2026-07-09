from ai.graph.nodes.merge import merge_node
from ai.graph.state import GraphState
from ai.models.schemas import RAGResult, OperationResult


def test_merge_with_rag_only():
    state = GraphState(
        rag_result=RAGResult(
            answer="Grilled chicken is available for $15.99.",
            sources=["restaurant_menu"],
            confidence=0.95,
        ),
    )
    result = merge_node(state)
    assert "Grilled chicken" in result["merged_result"]
    assert result["confidence"] > 0


def test_merge_with_operation_only():
    state = GraphState(
        operation_result=OperationResult(
            tool_name="book_table",
            status="success",
            payload={
                "reservation_id": "RES-ABC123",
                "status": "confirmed",
                "branch": "downtown",
                "date": "2026-07-10",
                "time": "19:00",
            },
        ),
    )
    result = merge_node(state)
    assert "RES-ABC123" in result["merged_result"]
    assert result["confidence"] == 1.0


def test_merge_with_both():
    state = GraphState(
        rag_result=RAGResult(
            answer="Yes, we have vegan pasta.",
            sources=["restaurant_menu"],
            confidence=0.95,
        ),
        operation_result=OperationResult(
            tool_name="book_table",
            status="success",
            payload={
                "reservation_id": "RES-ABC",
                "status": "confirmed",
                "branch": "downtown",
                "date": "2026-07-10",
                "time": "19:00",
            },
        ),
    )
    result = merge_node(state)
    assert "vegan pasta" in result["merged_result"]
    assert "RES-ABC" in result["merged_result"]
    assert result["confidence"] == 0.95


def test_merge_empty_state():
    state = GraphState()
    result = merge_node(state)
    assert result["merged_result"] == ""
    assert result["confidence"] == 0.0
