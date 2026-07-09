import json
import logging
import re

from langchain_ollama import ChatOllama

from ai.config.settings import get_settings
from ai.models.schemas import ExecutionPlan, ExecutionMode, Task, TaskType
from ai.prompts.registry import load_prompt
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def planner_node(state: GraphState) -> dict:
    plan = _detect_intent(state.user_query)
    if plan is not None:
        logger.info(f"Keyword plan: {plan.model_dump_json()}")
        return {"execution_plan": plan}

    settings = get_settings()
    history = _format_history(state.conversation_history)

    prompt_template = load_prompt("planner")
    prompt = prompt_template.format(query=state.user_query, history=history)

    llm = ChatOllama(
        model=settings.ollama_model_name,
        base_url=settings.ollama_base_url,
        temperature=0.1,
    )

    response = llm.invoke(prompt)
    plan = _parse_plan(response.content)

    logger.info(f"Plan generated: {plan.model_dump_json()}")
    return {"execution_plan": plan}


_KEYWORD_MAP = [
    (["appetizer", "menu", "ingredient", "price", "policy", "hour", 
      "open", "close", "catering", "refund", "allergen", "dietary",
      "vegan", "vegetarian", "gluten", "what.*have", "what.*serve",
      "do you have", "can i get"], TaskType.knowledge),
    (["book", "reserve", "reservation", "table for"], TaskType.reservation),
    (["available", "availability", "free table", "open table"], TaskType.availability),
    (["special", "today special", "chef special", "daily special"], TaskType.specials),
]


def _detect_intent(query: str) -> ExecutionPlan | None:
    q = query.lower().strip()
    tasks = []
    for keywords, task_type in _KEYWORD_MAP:
        for kw in keywords:
            if kw in q or re.search(kw, q):
                tasks.append(Task(type=task_type, priority=1))
                break
    if not tasks:
        return None
    return ExecutionPlan(
        tasks=tasks,
        execution_mode=ExecutionMode.parallel if len(tasks) > 1 else ExecutionMode.sequential,
        requires_clarification=False,
        clarification_fields=[],
        confidence=1.0,
    )


def _format_history(history: list) -> str:
    if not history:
        return "No previous conversation."
    lines = []
    for msg in history[-5:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        lines.append(f"{role.capitalize()}: {content}")
    return "\n".join(lines)


def _parse_plan(text: str) -> ExecutionPlan:
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if not json_match:
        logger.warning("No JSON found in planner response, using default plan")
        return ExecutionPlan(
            tasks=[Task(type=TaskType.knowledge, priority=1)],
            execution_mode=ExecutionMode.sequential,
        )

    try:
        data = json.loads(json_match.group(0))
        tasks = []
        for t in data.get("tasks", []):
            task_type = t.get("type", "knowledge")
            try:
                tt = TaskType(task_type)
            except ValueError:
                tt = TaskType.knowledge
            priority = t.get("priority", 1)
            if isinstance(priority, str):
                priority = {"high": 1, "medium": 2, "low": 3}.get(priority.lower(), 1)
            tasks.append(Task(type=tt, priority=priority))

        mode_str = data.get("execution_mode", "sequential")
        try:
            mode = ExecutionMode(mode_str)
        except ValueError:
            mode = ExecutionMode.sequential

        return ExecutionPlan(
            tasks=tasks,
            execution_mode=mode,
            requires_clarification=data.get("requires_clarification", False),
            clarification_fields=data.get("clarification_fields", []),
            confidence=data.get("confidence", 1.0),
        )
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse plan JSON: {e}")
        return ExecutionPlan(
            tasks=[Task(type=TaskType.knowledge, priority=1)],
            execution_mode=ExecutionMode.sequential,
        )
