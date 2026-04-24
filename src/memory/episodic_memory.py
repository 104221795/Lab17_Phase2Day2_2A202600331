import json
import os
from typing import Any, Dict, List

from src.memory.base import BaseMemory


class EpisodicMemory(BaseMemory):
    """Episodic memory stored as structured JSON event logs."""

    def __init__(self, file_path: str = "data/episodic_memory.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _should_save_episode(self, text: str) -> bool:
        lower = text.lower()
        keywords = [
            "decided",
            "selected",
            "completed",
            "outcome",
            "lesson",
            "ta chọn",
            "đã chọn",
            "hoàn tất",
            "kết luận",
            "bài học",
            "quyết định",
        ]
        return any(keyword in lower for keyword in keywords)

    def save(self, user_id: str, conversation_id: str, item: Dict[str, Any]) -> None:
        text = item.get("text", "")

        if not self._should_save_episode(text):
            return

        data = self._load()
        data.setdefault(user_id, [])

        episode = {
            "conversation_id": conversation_id,
            "memory_type": "episodic",
            "text": text,
            "outcome": item.get("outcome", "stored_episode")
        }

        data[user_id].append(episode)
        self._save_all(data)

    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        data = self._load()
        episodes = data.get(user_id, [])
        query_words = set(query.lower().split())

        scored = []
        for episode in episodes:
            text = episode.get("text", "").lower()
            score = sum(1 for word in query_words if word in text)
            if score > 0:
                item = dict(episode)
                item["score"] = score
                scored.append(item)

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def clear(self, user_id: str) -> None:
        data = self._load()
        data[user_id] = []
        self._save_all(data)
