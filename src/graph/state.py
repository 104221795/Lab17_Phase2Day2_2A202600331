from typing import Any, Dict, List, TypedDict


class MemoryState(TypedDict, total=False):
    messages: List[str]
    user_profile: Dict[str, Any]
    episodes: List[Dict[str, Any]]
    semantic_hits: List[str]
    recent_messages: List[str]
    selected_context: List[Dict[str, Any]]
    memory_budget: int
    context_tokens: int
    evicted_count: int
    query: str
    prompt: str
    response: str
    retrieved_memory: List[Dict[str, Any]]
    used_memory_count: int
