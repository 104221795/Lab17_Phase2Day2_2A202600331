from typing import Any, Dict, List


class ContextWindowManager:
    """Priority-based context trimming with real token counting via tiktoken."""

    def __init__(self, max_tokens: int = 500, encoding_name: str = "cl100k_base"):
        self.max_tokens = max_tokens
        self.encoding_name = encoding_name
        self.encoder = self._load_encoder()

    def _load_encoder(self):
        try:
            import tiktoken
            return tiktoken.get_encoding(self.encoding_name)
        except Exception:
            return None

    def estimate_tokens(self, text: str) -> int:
        text = str(text)

        if self.encoder:
            return max(1, len(self.encoder.encode(text)))

        # fallback if tiktoken is unavailable
        return max(1, len(text.split()) * 2)

    def trim(self, state: Dict[str, Any]) -> Dict[str, Any]:
        context_items: List[Dict[str, Any]] = []

        context_items.append({
            "priority": 1,
            "section": "query",
            "text": state.get("query", "")
        })

        if state.get("user_profile"):
            context_items.append({
                "priority": 2,
                "section": "profile",
                "text": str(state.get("user_profile"))
            })

        for episode in state.get("episodes", []):
            context_items.append({
                "priority": 3,
                "section": "episodic",
                "text": episode.get("text", str(episode))
            })

        for hit in state.get("semantic_hits", []):
            context_items.append({
                "priority": 3,
                "section": "semantic",
                "text": hit
            })

        for message in state.get("messages", []):
            context_items.append({
                "priority": 4,
                "section": "recent",
                "text": message
            })

        context_items.sort(key=lambda item: item["priority"])

        selected = []
        total_tokens = 0

        for item in context_items:
            token_count = self.estimate_tokens(item["text"])

            if total_tokens + token_count <= self.max_tokens:
                selected.append({**item, "tokens": token_count})
                total_tokens += token_count

        state["selected_context"] = selected
        state["context_tokens"] = total_tokens
        state["evicted_count"] = len(context_items) - len(selected)
        state["memory_budget"] = self.max_tokens
        state["token_counter"] = "tiktoken" if self.encoder else "word_count_fallback"

        return state