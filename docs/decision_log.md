# Architecture Decision Records (ADR) & Design Log

> [!IMPORTANT]
> **To All Agents:** This is the collective memory of the project's evolution.
> Whenever you make a significant architectural choice (e.g., adding a new tool, changing the prompt strategy, modifying the data flow), you **MUST** append a new entry here.
> 
> **Format:**
> - Keep it concise (bullet points preferred).
> - Focus on the **"Why"** (Rationale), not just the "What".
> - Note any alternatives considered and why they were rejected.

---

## 001. Project Initialization & Framework Choice
*   **Date**: 2026-01-03
*   **Decision**: Use `google-adk` framework with `uv` package manager and `gemini-3-flash-preview` model.
*   **Rationale**:
    *   `google-adk` provides structured Agent/Tool primitives and observability.
    *   `uv` ensures fast, reproducible environments.
    *   `gemini-3-flash` is the current optimal balance of speed and reasoning capability for search tasks.

## 002. Tooling: Strict "Anthropic-Style" Docstrings
*   **Date**: 2026-01-04
*   **Decision**: Adopt verbose, scenario-based docstrings for all tools (`app/tools/*.py`).
*   **Context**: Agent needs to know *when* to use a tool, not just how.
*   **Rationale**:
    *   Docstrings act as the system prompt for tool usage.
    *   Explicit "Use this tool when..." sections reduce hallucinations and misuse.
    *   See `docs/tooling_standards.md` for the full specification.

## 003. Semantic Binding for Data Flow
*   **Date**: 2026-01-05
*   **Decision**: Rely on LLM Semantic Understanding for cross-tool data passing (e.g., Search `link` -> Browse `url`).
*   **Context**: `search.py` returns `"link"`, but `browse.py` expects `"url"`.
*   **Rationale**:
    *   Instead of writing rigid glue code (middleware), we trust the Agent to map fields based on value characteristics (e.g., looks like a URL) and context.
    *   **Insight**: "Natural Language Programming" allows for fuzzy, resilient interfaces relative to traditional strict variable matching.
    *   **Constraint**: Requires high-quality, descriptive field names in tool returns.

## 004. [Next Decision Title]
*   **Date**: [YYYY-MM-DD]
*   **Decision**: [What did we decide?]
*   **Rationale**: [Why? What alternatives were rejected?]
