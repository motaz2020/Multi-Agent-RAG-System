import logging
import time
from typing import Any, Callable

from ai.models.schemas import OperationResult

logger = logging.getLogger(__name__)


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self._tools[name] = func
        logger.info(f"Registered tool: {name}")

    def execute(self, name: str, **kwargs) -> OperationResult:
        start = time.time()
        if name not in self._tools:
            error_msg = f"Tool '{name}' not found"
            logger.error(error_msg)
            return OperationResult(
                tool_name=name,
                status="error",
                errors=[error_msg],
                execution_time=time.time() - start,
            )

        try:
            logger.info(f"Executing tool: {name} | args={kwargs}")
            result = self._tools[name](**kwargs)
            execution_time = time.time() - start
            logger.info(f"Tool completed: {name} | time={execution_time:.2f}s")

            if isinstance(result, OperationResult):
                return result

            return OperationResult(
                tool_name=name,
                status="success",
                payload=result if isinstance(result, dict) else {"result": str(result)},
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start
            logger.error(f"Tool failed: {name} | error={e}")
            return OperationResult(
                tool_name=name,
                status="error",
                errors=[str(e)],
                execution_time=execution_time,
            )

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def get_tool(self, name: str) -> Callable | None:
        return self._tools.get(name)


_registry: ToolRegistry | None = None


def get_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
        _register_default_tools(_registry)
    return _registry


def _register_default_tools(registry: ToolRegistry):
    from ai.tools.restaurant_tools import check_table_availability, book_table, get_today_special
    registry.register("check_table_availability", check_table_availability)
    registry.register("book_table", book_table)
    registry.register("get_today_special", get_today_special)
