from typing import Any, Dict, List

from src.graph.graph import MemoryGraph
from src.memory.buffer_memory import ShortTermBufferMemory
from src.memory.episodic_memory import EpisodicMemory
from src.memory.profile_memory import ProfileMemory
from src.memory.router import MemoryRouter
from src.memory.semantic_memory import SemanticMemory


class MultiMemoryAgent:
    def __init__(self, use_memory: bool = True, memory_budget: int = 500):
        self.use_memory = use_memory

        self.memories = {
            "buffer": ShortTermBufferMemory(max_turns=8),
            "profile": ProfileMemory(),
            "episodic": EpisodicMemory(),
            "semantic": SemanticMemory(),
        }

        self.router = MemoryRouter(self.memories)
        self.graph = MemoryGraph(
            router=self.router,
            use_memory=use_memory,
            memory_budget=memory_budget,
        )

        self.histories: Dict[str, List[str]] = {}

    def _history_key(self, user_id: str, conversation_id: str) -> str:
        return f"{user_id}:{conversation_id}"

    def answer(self, user_id: str, conversation_id: str, query: str) -> Dict[str, Any]:
        key = self._history_key(user_id, conversation_id)
        history = self.histories.get(key, [])

        state = self.graph.run(
            user_id=user_id,
            conversation_id=conversation_id,
            query=query,
            history=history,
        )

        response = state.get("response", "")

        self.histories.setdefault(key, [])
        self.histories[key].append(f"User: {query}")
        self.histories[key].append(f"Assistant: {response}")

        return state

    def clear_user(self, user_id: str) -> None:
        self.router.clear_all(user_id)
        for key in list(self.histories.keys()):
            if key.startswith(f"{user_id}:"):
                del self.histories[key]
