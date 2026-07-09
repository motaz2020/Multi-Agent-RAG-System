from pydantic import BaseModel, Field
from typing import Optional, Any

from ai.models.schemas import ExecutionPlan, RAGResult, OperationResult, ValidationResult


class GraphState(BaseModel):
    thread_id: str = ""
    user_query: str = ""
    conversation_history: list = Field(default_factory=list)
    execution_plan: Optional[ExecutionPlan] = None
    rag_result: Optional[RAGResult] = None
    operation_result: Optional[OperationResult] = None
    merged_result: Optional[str] = None
    validation_result: Optional[ValidationResult] = None
    final_response: Optional[str] = None
    sources: list = Field(default_factory=list)
    tool_calls: list = Field(default_factory=list)
    confidence: float = 0.0
    error: Optional[str] = None
