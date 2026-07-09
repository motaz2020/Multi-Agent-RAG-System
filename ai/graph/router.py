import logging
from typing import Union

from langgraph.types import Send

from ai.models.schemas import ExecutionPlan, ExecutionMode, TaskType
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def route_plan(state: GraphState) -> Union[str, list[Send]]:
    plan = state.execution_plan
    if not plan:
        logger.warning("No execution plan, defaulting to knowledge")
        return "rag"

    if plan.requires_clarification:
        logger.info("Routing to: clarification")
        return "clarification"

    if plan.execution_mode == ExecutionMode.parallel and len(plan.tasks) > 1:
        logger.info(f"Routing to: parallel ({[t.type.value for t in plan.tasks]})")
        sends = []
        for task in plan.tasks:
            if task.type == TaskType.knowledge:
                sends.append(Send("rag", state))
            else:
                sends.append(Send("operations", state))
        return sends

    if not plan.tasks:
        logger.warning("Empty task list, defaulting to rag")
        return "rag"

    task_types = [t.type for t in plan.tasks]
    primary = task_types[0]

    if primary == TaskType.knowledge:
        logger.info("Routing to: rag")
        return "rag"
    elif primary in (TaskType.reservation, TaskType.availability, TaskType.specials):
        logger.info("Routing to: operations")
        return "operations"

    logger.info(f"Routing to: knowledge (default for {primary})")
    return "rag"


def route_after(state: GraphState) -> str:
    return "merge"
