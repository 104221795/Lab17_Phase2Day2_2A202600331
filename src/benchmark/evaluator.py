from typing import Any, Dict, List


def contains_keyword(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower()


def response_relevance(response: str, expected_keywords: List[str]) -> float:
    if not expected_keywords:
        return 0.0

    hits = sum(1 for keyword in expected_keywords if contains_keyword(response, keyword))
    return round((hits / len(expected_keywords)) * 5, 2)


def memory_hit_rate(retrieved_memory: List[Dict[str, Any]], expected_keywords: List[str]) -> float:
    if not expected_keywords:
        return 0.0

    memory_text = " ".join(item.get("text", str(item)) for item in retrieved_memory)
    memory_text += " " + " ".join(str(item.get("profile", "")) for item in retrieved_memory)

    hits = sum(1 for keyword in expected_keywords if contains_keyword(memory_text, keyword))
    return round(hits / len(expected_keywords), 2)


def context_utilization(response: str, retrieved_memory: List[Dict[str, Any]]) -> float:
    if not retrieved_memory:
        return 0.0

    response_lower = response.lower()
    used = 0

    for item in retrieved_memory:
        text = item.get("text", str(item)).lower()
        profile = str(item.get("profile", "")).lower()
        sample = (text + " " + profile).split()[:12]

        if any(word in response_lower for word in sample):
            used += 1

    return round((used / len(retrieved_memory)) * 5, 2)


def token_efficiency(state: Dict[str, Any]) -> float:
    total_tokens = max(1, state.get("context_tokens", 1))
    useful_tokens = 0

    for item in state.get("selected_context", []):
        if item.get("section") in {"query", "profile", "episodic", "semantic"}:
            useful_tokens += item.get("tokens", 0)

    return round(useful_tokens / total_tokens, 2)


def pass_case(response: str, expected_keywords: List[str]) -> bool:
    return all(contains_keyword(response, keyword) for keyword in expected_keywords)
