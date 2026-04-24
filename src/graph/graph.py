from typing import Any, Dict

from src.graph.nodes import (
    build_prompt_node,
    generate_response_node,
    retrieve_memory_node,
    save_memory_node,
    trim_context_node,
)
from src.graph.prompt_builder import PromptBuilder
from src.memory.context_manager import ContextWindowManager


class MemoryGraph:
    """LangGraph-style skeleton flow using explicit nodes and state passing."""

    def __init__(self, router, use_memory: bool = True, memory_budget: int = 500):
        self.router = router
        self.use_memory = use_memory
        self.prompt_builder = PromptBuilder()
        self.context_manager = ContextWindowManager(max_tokens=memory_budget)

    def initialize_state(self, query: str, history: list[str]) -> Dict[str, Any]:
        return {
            "messages": history,
            "query": query,
            "user_profile": {},
            "episodes": [],
            "semantic_hits": [],
            "recent_messages": [],
            "memory_budget": self.context_manager.max_tokens,
            "response": "",
            "retrieved_memory": [],
        }

    def run(self, user_id: str, conversation_id: str, query: str, history: list[str]) -> Dict[str, Any]:
        state = self.initialize_state(query=query, history=history)

        if self.use_memory:
            state = retrieve_memory_node(state, self.router, user_id)
        else:
            state["retrieved_memory"] = []

        state = build_prompt_node(state, self.prompt_builder)
        state = trim_context_node(state, self.context_manager)
        state = generate_response_node(state, use_memory=self.use_memory)

        if self.use_memory:
            state = save_memory_node(state, self.router, user_id, conversation_id)

        return state
