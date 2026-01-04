# Tooling & Skills Standards
> **Philosophy**: Built on Anthropic's "Building Effective Agents" principles & Google ADK patterns.

## 1. The "Junior Developer" Principle (Documentation)
**Rule**: Write docstrings as if you are explaining the function to a **junior developer** who just joined the team.
*   **BAD**: `Search Google.`
*   **GOOD**: `Searches Google for the given query. Returns the top 5 snippets with URLs. Use this tool when the user asks about current events, facts, or live data that is not in your internal knowledge base.`

**Why?** LLMs are not telepathic. They need context on *when* and *why* to use a tool, not just *how*.

## 2. Poka-yoke Design (Error Proofing)
**Rule**: Design tool arguments to make it impossible (or very hard) to invalid inputs.
*   **Use Enums**: Instead of `str` for status, use `Literal['open', 'closed']`.
*   **Fuzzy Matching**: Do not demand exact IDs if a name search can work.
*   **Validation**: Use Pydantic `Field` constraints (e.g., `min_length`, `regex`) to catch bad data *before* the tool runs.

## 3. Rich Returns (Verbose Output)
**Rule**: Never return just a boolean or a raw string. Return a structured `dict` or Pydantic model.
*   **BAD**: `return True`
*   **GOOD**:
    ```python
    return {
        "status": "success",
        "action": "deleted_file",
        "file_name": "report.pdf",
        "remaining_storage": "10.5GB",
        "note": "File moved to trash bin, can be recovered within 30 days."
    }
    ```

**Why?** The Agent needs "State Awareness". Knowing *what happened* (side effects) and *current state* helps it plan the next step.

## 4. Separation of Concerns (File Structure)
*   **New Tools**: Must be created in `app/tools/`.
*   **One File per Domain**: e.g., `app/tools/search.py`, `app/tools/calculator.py`.
*   **No Global Pollution**: Do not dump everything into `agent.py`.
