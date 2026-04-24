from typing import Any, Dict


class PromptBuilder:
    """Builds the final prompt with explicit memory injection sections."""

    def build(self, state: Dict[str, Any]) -> str:
        return f"""You are a memory-enabled assistant. Use the memory only when relevant.

[USER PROFILE MEMORY]
{state.get("user_profile", {})}

[EPISODIC MEMORY]
{state.get("episodes", [])}

[SEMANTIC MEMORY]
{state.get("semantic_hits", [])}

[RECENT CONVERSATION]
{state.get("recent_messages", [])}

[USER QUERY]
{state.get("query", "")}

Answer using the most relevant memory. If memory is missing, say you do not know.
"""
