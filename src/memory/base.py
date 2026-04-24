from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseMemory(ABC):
    """Common interface for all memory backends."""

    @abstractmethod
    def save(self, user_id: str, conversation_id: str, item: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def clear(self, user_id: str) -> None:
        raise NotImplementedError
