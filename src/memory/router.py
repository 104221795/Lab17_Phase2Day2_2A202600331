from typing import Any, Dict, List


class MemoryRouter:
    """Routes memory retrieval to the correct backend based on query intent."""

    def __init__(self, memories: Dict[str, Any]):
        self.memories = memories

    def classify_intent(self, query: str) -> str:
        q = query.lower()

        profile_keywords = [
            "tôi dị ứng",
            "dị ứng gì",
            "my allergy",
            "tên tôi",
            "my name",
            "prefer",
            "thích câu trả lời",
            "favorite",
            "yêu thích",
        ]

        episodic_keywords = [
            "last time",
            "previous",
            "trước đó",
            "hôm trước",
            "đã chọn",
            "quyết định",
            "bài học",
            "lesson",
            "outcome",
        ]

        recent_keywords = [
            "vừa nói",
            "just said",
            "above",
            "earlier in this conversation",
            "current conversation",
        ]

        semantic_keywords = [
            "similar",
            "semantic",
            "benchmark",
            "retrieve",
            "recall",
            "docker",
            "token",
            "context",
            "memory",
        ]

        if any(keyword in q for keyword in profile_keywords):
            return "profile_recall"

        if any(keyword in q for keyword in episodic_keywords):
            return "episodic_recall"

        if any(keyword in q for keyword in recent_keywords):
            return "recent_context"

        if any(keyword in q for keyword in semantic_keywords):
            return "semantic_recall"

        return "general"

    def route(self, query: str) -> List[str]:
        intent = self.classify_intent(query)

        routing = {
            "profile_recall": ["profile", "semantic", "buffer"],
            "episodic_recall": ["episodic", "semantic", "buffer"],
            "recent_context": ["buffer"],
            "semantic_recall": ["semantic", "episodic", "buffer"],
            "general": ["profile", "semantic", "buffer"],
        }

        return routing[intent]

    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        backends = self.route(query)
        results: List[Dict[str, Any]] = []

        for backend_name in backends:
            backend = self.memories[backend_name]
            backend_results = backend.retrieve(user_id=user_id, query=query, top_k=top_k)

            for item in backend_results:
                item = dict(item)
                item["memory_backend"] = backend_name
                results.append(item)

        return results[:top_k]

    def save_all(self, user_id: str, conversation_id: str, item: Dict[str, Any]) -> None:
        for backend in self.memories.values():
            backend.save(user_id=user_id, conversation_id=conversation_id, item=item)

    def clear_all(self, user_id: str) -> None:
        for backend in self.memories.values():
            backend.clear(user_id=user_id)
