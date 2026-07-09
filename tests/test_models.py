from ai.models.schemas import (
    TaskType, ExecutionMode, Task, ExecutionPlan,
    RAGResult, OperationResult, ValidationResult,
    ChatRequest, ChatResponse, ConversationMessage, MessageRole,
)


def test_task_type_values():
    assert TaskType.knowledge.value == "knowledge"
    assert TaskType.reservation.value == "reservation"


def test_execution_mode_values():
    assert ExecutionMode.sequential.value == "sequential"
    assert ExecutionMode.parallel.value == "parallel"
    assert ExecutionMode.clarification.value == "clarification"


def test_execution_plan_defaults():
    plan = ExecutionPlan()
    assert plan.tasks == []
    assert plan.execution_mode == ExecutionMode.sequential
    assert plan.requires_clarification is False


def test_rag_result_defaults():
    result = RAGResult(answer="Test")
    assert result.sources == []
    assert result.retrieved_chunks == []
    assert result.confidence == 0.0


def test_operation_result():
    result = OperationResult(
        tool_name="book_table",
        status="success",
        payload={"reservation_id": "RES-123"},
    )
    assert result.tool_name == "book_table"
    assert result.payload["reservation_id"] == "RES-123"


def test_validation_result_defaults():
    result = ValidationResult()
    assert result.passed is False
    assert result.issues == []


def test_chat_request():
    req = ChatRequest(thread_id="thread-1", message="Hello")
    assert req.thread_id == "thread-1"
    assert req.message == "Hello"


def test_chat_response():
    resp = ChatResponse(response="Hello!", sources=["menu"], confidence=0.95)
    assert resp.response == "Hello!"
    assert resp.sources == ["menu"]


def test_conversation_message():
    msg = ConversationMessage(role=MessageRole.user, content="Hi")
    assert msg.role == MessageRole.user
    assert msg.content == "Hi"


def test_message_role_values():
    assert MessageRole.user.value == "user"
    assert MessageRole.assistant.value == "assistant"
