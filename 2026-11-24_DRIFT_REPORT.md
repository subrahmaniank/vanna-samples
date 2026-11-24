# Drift Report: 2026-11-24

Comparison of README specifications vs current codebase. Only divergences are listed.

## Remediation (2026-11-24 follow-up)

Addressed in code/docs: root README tagline, shared-components list (`chroma_agent_memory`, env loader, `sample.env` path), `pyproject.toml` description, `store_analyzer/README.md` auth wording, and LLM docstrings in three `agent_factory.py` files. Still open: dedicated `adventureworks/README.md` and `portfolio_analyzer/README.md`; documenting or removing stub `main.py`.

## README.md (Root)

- Opening tagline (line 3) names **Snowflake**, **Qdrant**, and **Azure OpenAI** only; configuration and `shared/llm_factory.py` also support **OpenRouter**, **Bedrock Mantle**, **standard OpenAI**, and **custom** OpenAI Chat Completions endpoints.
- Shared components list (line 64) references `shared/chroma_agent_memory.py`; that file **does not exist**. ChromaDB is provided via `vanna.integrations.chromadb.ChromaAgentMemory` inside `shared/vector_store_factory.py`.
- Shared components list (line 65) states `shared/env_loader.py` supports **root and module-level** `.env`; `EnvironmentLoader` loads **only** `{module_path}/.env` (see docstring and `load_dotenv` at `shared/env_loader.py:26–29`).
- Configuration section (lines 76–79) instructs `cp sample.env .env` at the **project root**; there is **no** root-level `sample.env`—templates live under each module (`adventureworks/`, `store_analyzer/`, etc.).
- Shared components section does not mention `shared/test_llm_factory.py` or `shared/llm_factory.py` helpers `_normalize_openai_v1_base_url` / `_parse_truthy_env_flag` (factory behavior is documented only indirectly via env vars).
- `pyproject.toml` `description` still lists **AWS Bedrock Mantle / Azure OpenAI** only and omits OpenRouter, custom endpoint, and standard OpenAI called out in README LLM selector.

## auto_finance/README.md

- No drift detected for custom LLM: setup correctly defers to module `.env` / Qdrant.
- Root README lists Auto Finance **entry points** as server + MCP only; this README matches (no `auto_finance_app.py` / `auto_finance_api.py` in repo—consistent with code).

## store_analyzer/README.md

- Legacy section claims `simple_authorization.py` is **used for** `/auth/login` migration; `store_analyzer_server.py` implements login/logout routes **inline** and does **not** import `simple_authorization.py` (grep shows no Python references to that module).
- Setup does not document **custom** / **OpenRouter** LLM options present in `store_analyzer/sample.env` (minor doc gap vs module template, not vs factory).

## adventureworks/README.md

- No drift detected (file absent).

- **Missing design surface:** Root README documents the AdventureWorks module (ports, seeders, entry points) but **`adventureworks/README.md` does not exist** (unlike `auto_finance/` and `store_analyzer/`).

## portfolio_analyzer/README.md

- No drift detected (file absent).

- **Missing design surface:** Root README documents Portfolio Analyzer; **`portfolio_analyzer/README.md` does not exist**.

## Module agent_factory.py docstrings (vs README + llm_factory)

- `adventureworks/agent_factory.py`, `store_analyzer/agent_factory.py`, and `portfolio_analyzer/agent_factory.py` module docstrings still state LLM support as **Bedrock Mantle / Azure / OpenAI** only; they omit **OpenRouter** and **custom** providers implemented in `shared/llm_factory.py` and documented in README/sample.env.

## shared/llm_factory.py (vs README)

- No drift detected for **custom** provider: `CUSTOM_LLM_*` env vars, aliases (`custom`, `openai_compatible`, `custom_endpoint`, `custom_llm`), and `CUSTOM_LLM_APPEND_V1` match README and module `sample.env` files.

## Undocumented / unreferenced implementation (no README link)

- `main.py` — placeholder `Hello from vanna-samples!` entry point; not referenced in any README.
- `shared/test_llm_factory.py` — unit tests for custom LLM factory; not referenced in README or CI configuration in `pyproject.toml`.