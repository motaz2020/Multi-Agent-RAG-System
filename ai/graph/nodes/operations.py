import logging
import json
import re


from ai.config.settings import get_settings
from ai.models.schemas import OperationResult
from ai.tools.registry import get_registry
from ai.graph.state import GraphState

logger = logging.getLogger(__name__)


def operations_node(state: GraphState) -> dict:
    logger.info(f"Operations node executing for: {state.user_query[:50]}...")

    plan = state.execution_plan
    if not plan or not plan.tasks:
        logger.warning("No tasks in execution plan")
        return {"operation_result": OperationResult(
            tool_name="none", status="error", errors=["No tasks to execute"]
        )}

    registry = get_registry()
    results = []

    for task in plan.tasks:
        tool_name = _task_to_tool(task.type.value)
        if not tool_name:
            continue

        params = _extract_params(state.user_query, tool_name)
        result = registry.execute(tool_name, **params)
        results.append(result)

    if not results:
        return {"operation_result": OperationResult(
            tool_name="none", status="skipped", errors=["No operation tasks"]
        )}

    merged = _merge_operation_results(results)
    return {"operation_result": merged, "tool_calls": [r.tool_name for r in results if r.status == "success"]}


def _task_to_tool(task_type: str) -> str | None:
    mapping = {
        "reservation": "book_table",
        "availability": "check_table_availability",
        "specials": "get_today_special",
    }
    return mapping.get(task_type)


def _extract_params(query: str, tool_name: str) -> dict:
    params = {}
    if tool_name == "check_table_availability":
        params.update(_extract_branch(query))
        params.update(_extract_date_time(query))
    elif tool_name == "book_table":
        params["customer_name"] = _extract_name(query) or "Guest"
        params.update(_extract_branch(query))
        params.update(_extract_date_time(query))
    elif tool_name == "get_today_special":
        params.update(_extract_branch(query))
    return params


def _extract_branch(text: str) -> dict:
    text_lower = text.lower()
    branches = {"downtown": "downtown", "uptown": "uptown", "riverside": "riverside"}
    for keyword, branch in branches.items():
        if keyword in text_lower:
            return {"branch": branch}
    return {"branch": "downtown"}


def _extract_date_time(text: str) -> dict:
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    time_match = re.search(r"(\d{1,2}):(\d{2})", text)

    import datetime
    result = {}
    if date_match:
        result["date_str"] = date_match.group(1)
    else:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        result["date_str"] = tomorrow.isoformat()

    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        result["time_str"] = f"{hour:02d}:{minute:02d}"
    else:
        result["time_str"] = "19:00"

    return result


def _extract_name(text: str) -> str | None:
    patterns = [
        r"(?:name is|for|under)\s+(\w+\s+\w+)",
        r"(?:book|reserve)\s+(?:for\s+)?(\w+\s+\w+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _merge_operation_results(results: list[OperationResult]) -> OperationResult:
    if len(results) == 1:
        return results[0]

    tool_names = [r.tool_name for r in results]
    status = "success" if all(r.status == "success" for r in results) else "partial"
    errors = [e for r in results for e in r.errors]

    merged_payload = {}
    for r in results:
        merged_payload.update(r.payload)

    return OperationResult(
        tool_name=",".join(tool_names),
        status=status,
        payload=merged_payload,
        execution_time=sum(r.execution_time for r in results),
        errors=errors,
    )
