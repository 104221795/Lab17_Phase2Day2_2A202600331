from collections import defaultdict, deque
from typing import Any, Deque, Dict, List

from src.memory.base import BaseMemory


class ShortTermBufferMemory(BaseMemory):
    """Short-term memory using a sliding conversation window."""

    def __init__(self, max_turns: int = 8):
        self.max_turns = max_turns
        self.store: Dict[str, Deque[Dict[str, Any]]] = defaultdict(lambda: deque(maxlen=max_turns))

    def _key(self, user_id: str, conversation_id: str) -> str:
        return f"{user_id}:{conversation_id}"

    def save(self, user_id: str, conversation_id: str, item: Dict[str, Any]) -> None:
        key = self._key(user_id, conversation_id)
        saved_item = dict(item)
        saved_item["memory_type"] = "short_term"
        saved_item["conversation_id"] = conversation_id
        self.store[key].append(saved_item)

    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        prefix = f"{user_id}:"

        for key, messages in self.store.items():
            if key.startswith(prefix):
                results.extend(list(messages))

        return results[-top_k:]

    def clear(self, user_id: str) -> None:
        prefix = f"{user_id}:"
        for key in list(self.store.keys()):
            if key.startswith(prefix):
                del self.store[key]
