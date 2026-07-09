from ai.models.schemas import ExecutionPlan, ExecutionMode, Task, TaskType


def test_default_plan_sequential():
    plan = ExecutionPlan()
    assert plan.execution_mode == ExecutionMode.sequential
    assert plan.tasks == []
    assert plan.requires_clarification is False


def test_plan_with_single_knowledge_task():
    plan = ExecutionPlan(
        tasks=[Task(type=TaskType.knowledge, priority=1)],
        execution_mode=ExecutionMode.sequential,
    )
    assert len(plan.tasks) == 1
    assert plan.tasks[0].type == TaskType.knowledge
    assert plan.execution_mode == ExecutionMode.sequential


def test_plan_with_parallel_mode():
    plan = ExecutionPlan(
        tasks=[
            Task(type=TaskType.knowledge, priority=1),
            Task(type=TaskType.reservation, priority=2),
        ],
        execution_mode=ExecutionMode.parallel,
    )
    assert len(plan.tasks) == 2
    assert plan.execution_mode == ExecutionMode.parallel


def test_plan_with_clarification():
    plan = ExecutionPlan(
        tasks=[Task(type=TaskType.reservation, priority=1)],
        execution_mode=ExecutionMode.sequential,
        requires_clarification=True,
        clarification_fields=["branch", "date", "time"],
    )
    assert plan.requires_clarification
    assert len(plan.clarification_fields) == 3
