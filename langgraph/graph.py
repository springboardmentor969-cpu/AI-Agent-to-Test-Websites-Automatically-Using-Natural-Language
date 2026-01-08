from typing import Callable, Dict, Any

START = "__start__"
END = "__end__"


class StateGraph:
    def __init__(self, state_type=None):
        self.nodes: Dict[str, Callable[[Any], Any]] = {}
        self.edges: Dict[str, str] = {}

    def add_node(self, name: str, fn: Callable[[Any], Any]):
        self.nodes[name] = fn

    def add_edge(self, src: str, dst: str):
        # Only support single outgoing edge per node for simplicity
        self.edges[src] = dst

    def compile(self):
        graph = self

        class Runner:
            def __init__(self, graph: StateGraph):
                self._graph = graph

            def invoke(self, initial_state: Any):
                state = initial_state
                current = START
                # traverse until END or no next
                while True:
                    # if current is END, stop
                    if current == END:
                        break
                    nxt = self._graph.edges.get(current)
                    # if there's no next node, stop
                    if nxt is None:
                        break
                    # if next is END marker, stop without trying to call a node
                    if nxt == END:
                        break
                    fn = self._graph.nodes.get(nxt)
                    if fn is None:
                        raise RuntimeError(f"No node function for {nxt}")
                    state = fn(state)
                    current = nxt
                return state

        return Runner(graph)