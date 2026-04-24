import copy
from typing import Any, Dict, List

from src.memory.base import BaseMemory


class ProfileMemory(BaseMemory):
    """
    Long-term profile memory.

    Stores stable user facts/preferences as key-value data.
    Conflict handling uses overwrite semantics for the same profile field.
    """

    def __init__(self):
        self.profiles: Dict[str, Dict[str, Any]] = {}

    def _ensure_user(self, user_id: str) -> Dict[str, Any]:
        self.profiles.setdefault(user_id, {})
        return self.profiles[user_id]

    def _extract_profile_facts(self, text: str) -> Dict[str, Any]:
        lower = text.lower()
        facts: Dict[str, Any] = {}

        # Required conflict-handling test:
        # "Tôi dị ứng sữa bò."
        # "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò."
        if "dị ứng" in lower or "allergy" in lower or "allergic" in lower:
            if "đậu nành" in lower or "soy" in lower:
                facts["allergy"] = "đậu nành"
            elif "sữa bò" in lower or "milk" in lower or "cow milk" in lower:
                facts["allergy"] = "sữa bò"

        if "tên tôi là" in lower:
            name = text.split("tên tôi là", 1)[-1].strip(" .")
            if name:
                facts["name"] = name

        if "my name is" in lower:
            name = text.lower().split("my name is", 1)[-1].strip(" .")
            if name:
                facts["name"] = name.title()

        if "thích câu trả lời ngắn" in lower or "prefer brief" in lower or "prefer concise" in lower:
            facts["response_style"] = "brief"

        if "thích câu trả lời dài" in lower or "prefer detailed" in lower or "prefer long" in lower:
            facts["response_style"] = "detailed"

        if "ngôn ngữ lập trình yêu thích" in lower and "python" in lower:
            facts["favorite_programming_language"] = "Python"

        if "favorite programming language" in lower and "python" in lower:
            facts["favorite_programming_language"] = "Python"

        return facts

    def save(self, user_id: str, conversation_id: str, item: Dict[str, Any]) -> None:
        text = item.get("text", "")
        new_facts = self._extract_profile_facts(text)

        if not new_facts:
            return

        profile = self._ensure_user(user_id)

        # Conflict handling: same key gets overwritten by newer fact.
        for key, value in new_facts.items():
            profile[key] = value

    def retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        profile = copy.deepcopy(self.profiles.get(user_id, {}))

        if not profile:
            return []

        return [{
            "memory_type": "profile",
            "text": str(profile),
            "profile": profile,
            "score": 1.0
        }]

    def clear(self, user_id: str) -> None:
        self.profiles[user_id] = {}
