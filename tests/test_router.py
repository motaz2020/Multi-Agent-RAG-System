from ai.graph.router import route_plan, route_after
from ai.graph.state import GraphState
from ai.models.schemas import ExecutionPlan, ExecutionMode, Task, TaskType


def _make_state(plan: ExecutionPlan) -> GraphState:
    return GraphState(execution_plan=plan)


def test_route_knowledge():
    plan = ExecutionPlan(
        tasks=[Task(type=TaskType.knowledge, priority=1)],
        execution_mode=ExecutionMode.sequential,
    )
    state = _make_state(plan)
    assert route_plan(state) == "rag"


def test_route_operations():
    plan = ExecutionPlan(
        tasks=[Task(type=TaskType.reservation, priority=1)],
        execution_mode=ExecutionMode.sequential,
    )
    state = _make_state(plan)
    assert route_plan(state) == "operations"


def test_route_clarification():
    plan = ExecutionPlan(
        tasks=[Task(type=TaskType.reservation, priority=1)],
        execution_mode=ExecutionMode.sequential,
        requires_clarification=True,
    )
    state = _make_state(plan)
    assert route_plan(state) == "clarification"


def test_route_empty_plan_defaults_rag():
    state = GraphState()
    assert route_plan(state) == "rag"


def test_route_after_always_merge():
    state = GraphState()
    assert route_after(state) == "merge"


def test_route_after_with_data():
    state = GraphState(
        rag_result={"answer": "test"},
        operation_result={"tool_name": "book_table"},
    )
    assert route_after(state) == "merge"
