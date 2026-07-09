from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TaskType(str, Enum):
    knowledge = "knowledge"
    reservation = "reservation"
    specials = "specials"
    availability = "availability"


class ExecutionMode(str, Enum):
    sequential = "sequential"
    parallel = "parallel"
    clarification = "clarification"


class Task(BaseModel):
    type: TaskType
    priority: int = 1


class ExecutionPlan(BaseModel):
    tasks: list[Task] = Field(default_factory=list)
    execution_mode: ExecutionMode = ExecutionMode.sequential
    requires_clarification: bool = False
    clarification_fields: list[str] = Field(default_factory=list)
    confidence: float = 1.0


class RAGResult(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    retrieved_chunks: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    reasoning_summary: str = ""


class OperationResult(BaseModel):
    tool_name: str
    status: str = "success"
    payload: dict = Field(default_factory=dict)
    execution_time: float = 0.0
    errors: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    passed: bool = False
    issues: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    validated_response: str = ""


class FinalResponse(BaseModel):
    content: str
    sources: list[str] = Field(default_factory=list)
    tool_calls: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class ConversationMessage(BaseModel):
    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    thread_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list[str] = Field(default_factory=list)
    tool_calls: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    execution_time: float = 0.0
