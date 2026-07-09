import logging

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from ai.graph.state import GraphState
from ai.graph.router import route_plan, route_after
from ai.graph.registry import get_node_registry

logger = logging.getLogger(__name__)


def build_graph():
    registry = get_node_registry()

    graph = StateGraph(GraphState)

    graph.add_node("memory_loader", registry.get("memory_loader"))
    graph.add_node("planner", registry.get("planner"))
    graph.add_node("rag", registry.get("rag"))
    graph.add_node("operations", registry.get("operations"))
    graph.add_node("merge", registry.get("merge"))
    graph.add_node("validator", registry.get("validator"))
    graph.add_node("formatter", registry.get("formatter"))
    graph.add_node("memory_saver", registry.get("memory_saver"))

    graph.add_edge(START, "memory_loader")
    graph.add_edge("memory_loader", "planner")

    graph.add_conditional_edges(
        "planner",
        route_plan,
        {
            "rag": "rag",
            "operations": "operations",
            "clarification": "formatter",
        },
    )

    graph.add_edge("rag", "merge")
    graph.add_edge("operations", "merge")

    graph.add_edge("merge", "validator")
    graph.add_edge("validator", "formatter")
    graph.add_edge("formatter", "memory_saver")
    graph.add_edge("memory_saver", END)

    checkpointer = MemorySaver()

    compiled = graph.compile(checkpointer=checkpointer)
    logger.info("Graph compiled successfully")
    return compiled
