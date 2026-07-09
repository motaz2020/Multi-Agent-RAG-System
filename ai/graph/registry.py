import logging
from typing import Callable

logger = logging.getLogger(__name__)


class NodeRegistry:
    def __init__(self):
        self._nodes: dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self._nodes[name] = func
        logger.info(f"Registered graph node: {name}")

    def get(self, name: str) -> Callable:
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' not registered")
        return self._nodes[name]

    def list_nodes(self) -> list[str]:
        return list(self._nodes.keys())


_node_registry: NodeRegistry | None = None


def get_node_registry() -> NodeRegistry:
    global _node_registry
    if _node_registry is None:
        _node_registry = NodeRegistry()
        _register_default_nodes(_node_registry)
    return _node_registry


def _register_default_nodes(registry: NodeRegistry):
    from ai.graph.nodes.planner import planner_node
    from ai.graph.nodes.rag import rag_node
    from ai.graph.nodes.operations import operations_node
    from ai.graph.nodes.merge import merge_node
    from ai.graph.nodes.validator import validator_node
    from ai.graph.nodes.formatter import formatter_node
    from ai.graph.nodes.memory import memory_loader_node, memory_saver_node

    registry.register("planner", planner_node)
    registry.register("rag", rag_node)
    registry.register("operations", operations_node)
    registry.register("merge", merge_node)
    registry.register("validator", validator_node)
    registry.register("formatter", formatter_node)
    registry.register("memory_loader", memory_loader_node)
    registry.register("memory_saver", memory_saver_node)
