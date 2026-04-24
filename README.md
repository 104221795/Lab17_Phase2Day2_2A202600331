# Lab 17 – Multi-Memory Agent with LangGraph-style Flow

## Objective

This project implements a multi-memory AI agent architecture for Lab 17.

It includes:

- 4 memory types:
  - Short-term memory
  - Long-term profile memory
  - Episodic memory
  - Semantic memory
- LangGraph-style state, nodes, router, and graph flow
- Prompt injection with clear memory sections
- Profile update and conflict handling
- Context window trimming and memory budget control
- Benchmark comparing no-memory vs with-memory over 10 multi-turn conversations
- BENCHMARK.md with results, privacy reflection, and limitations

## Project Structure

```txt
src/
  app/
    agent.py

  benchmark/
    conversations.py
    evaluator.py
    run_benchmark.py

  graph/
    graph.py
    nodes.py
    prompt_builder.py
    state.py

  memory/
    base.py
    buffer_memory.py
    profile_memory.py
    episodic_memory.py
    semantic_memory.py
    router.py
    context_manager.py

reports/
  BENCHMARK.md
  lab17_results.json

data/
  episodic_memory.json
  semantic_memory.json
```

## Installation

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Benchmark

```bash
python -m src.benchmark.run_benchmark
```

Generated outputs:

```txt
reports/BENCHMARK.md
reports/lab17_results.json
```

## Design Summary

### Memory Types

| Memory Type | Implementation | Purpose |
|---|---|---|
| Short-term | Sliding conversation buffer | Recent turns |
| Long-term profile | Key-value profile store | Stable user facts/preferences |
| Episodic | JSON event log | Past task outcomes/decisions |
| Semantic | Keyword semantic fallback / optional Chroma-style interface | Relevant past knowledge |

### LangGraph-style Flow

```txt
initialize_state
    ↓
retrieve_memory_node
    ↓
build_prompt_node
    ↓
trim_context_node
    ↓
generate_response_node
    ↓
save_memory_node
```

### Prompt Injection Sections

```txt
[USER PROFILE MEMORY]
[EPISODIC MEMORY]
[SEMANTIC MEMORY]
[RECENT CONVERSATION]
[USER QUERY]
```

## Notes

This implementation uses deterministic mock generation for stable grading. The architecture is designed so a real LLM can replace the mock generation node later.

## Bonus Readiness

This project includes real token counting through `tiktoken` when available. If `tiktoken` cannot be loaded, the system falls back to word-count approximation.

The semantic memory backend currently uses deterministic keyword-overlap retrieval for stable benchmark results. However, the memory interface is designed to be easily replaced with:

- Chroma
- FAISS
- Ollama embeddings
- OpenAI-compatible embedding APIs

The extraction and generation layer can also be extended with Ollama or another cloud/local LLM. For grading stability, the benchmark uses deterministic mock generation so results are reproducible.
