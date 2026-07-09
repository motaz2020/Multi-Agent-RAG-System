import logging

from ai.graph.builder import build_graph

logger = logging.getLogger(__name__)

_graph_instance = None


def get_graph():
    global _graph_instance
    if _graph_instance is None:
        logger.info("Building graph for first time")
        _graph_instance = build_graph()
    return _graph_instance
