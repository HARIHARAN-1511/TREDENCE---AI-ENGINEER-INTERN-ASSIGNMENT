import asyncio
from typing import Callable, Dict, List, Any, Optional

State = Dict[str, Any]
NodeFunction = Callable[[State], State]

MAX_STEPS = 50

class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, NodeFunction] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[State], str]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: NodeFunction):
        self.nodes[name] = func

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edge(self, source: str, router: Callable[[State], str]):
        self.conditional_edges[source] = router

    def set_entry_point(self, name: str):
        self.entry_point = name

    async def run(self, initial_state: State) -> Dict[str, Any]:
        if not self.entry_point:
            raise ValueError("Graph must have an entry point")

        current_node = self.entry_point
        state = initial_state.copy()
        history = []
        
        steps = 0
        while current_node:
            steps += 1
            if steps > MAX_STEPS:
                 history.append(f"Terminated: Max steps {MAX_STEPS} reached")
                 break

            history.append(f"Running node: {current_node}")
            
            if current_node not in self.nodes:
                raise ValueError(f"Node {current_node} is not defined")
            
            func = self.nodes[current_node]
            
            if asyncio.iscoroutinefunction(func):
                state = await func(state)
            else:
                state = func(state)

            # Determine Next Node
            next_node = None
            
            if current_node in self.conditional_edges:
                router = self.conditional_edges[current_node]
                next_node = router(state)
            elif current_node in self.edges:
                next_node = self.edges[current_node]
            
            current_node = next_node

        return {
            "final_state": state,
            "history": history
        }
