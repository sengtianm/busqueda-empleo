# AGENTS.md

## Project
Automated job search pipeline: discovers, collects, prepares, evaluates, processes, and manages opportunities to reduce search time/effort and support decision-making. Objective: from discovery to high-quality application inputs with full traceability and minimal manual intervention (DOC-08).

**Status:** MVP in progress — Phases 0–3 done (infrastructure, shared services, prompts tested with `gemma4:31b-cloud`); Phase 4 (Module 1 — Opportunity Discovery, branch `fase-4`) active with sub-phases 4.1–4.4 implemented & validated (INICIO + control nodes, platform entry, filter search + generic register, capture/registration with dedup by `id_externo_url`); Phases 5–9 pending. Authoritative status: `docs/history/tracker.md`.

## Architecture
Three layers: Functional modules → Shared services → Infrastructure.
Workflow: Discovery → Preparation → Evaluation → Processing → Management.
All implementations must follow this architecture (DOC-12).

## Technology Stack
Python 3.12 · Playwright · BeautifulSoup + lxml · SQLite · Pydantic · httpx · Loguru · RapidFuzz · Tenacity · Ollama · PyYAML · python-dotenv · pytest · Ruff · mypy

## Project Structure
- `docs/` — official documentation (project-design, plans, reports, history)
- `config/` — centralized configuration (`config.yaml`, `.env.template`)
- `prompts/` — official prompts (separate from code)
- `modules/` — functional modules: discovery, preparation, evaluation, processing, management
- `shared/` — reusable resources (config, errors, logging, retry, models, persistence, ia_service, decision_engine, state_machine)
- `data/` — persistent data (input, processing, output, backup)
- `logs/` — logs and audit
- `temp/` — temporary files
- `scripts/` — auxiliary scripts (e.g., prompt tester)
- `tests/` — tests (fixtures in `tests/fixtures/`)

## Conventions
- English: code, documentation, configuration, prompts, commit messages, directory/file names.
- Spanish: data-related — SQLite DB (`job_search.db`), `shared/models.py`, `shared/persistence.py`, profile/criteria in `config.yaml`, test fixtures.
- Exception: `modules/discovery/` (node files and tests) uses Spanish identifiers for domain concepts (e.g., `ejecutar_inicio`, `ResultadoInicio`, `fuentes_filtradas`), consistent with `run_context.py` and the Spanish data layer; Spanish docstrings/error-evidence strings allowed here only.
- Spanish for all conversations with the user.
- Configuration must be separated from business logic; prompts from code; no hardcoded values.
- Every transformation must preserve original data.
- No functional module may access the database directly.
- Never include API keys, tokens, passwords, or sensitive data in repository files.
- Response style: Spanish, concise, clear headings/lists; never modify files without explaining first.

## Workflow
Work cycle: Context → Define task → Analyze → Plan → Implement → Verify → Close → Save. Every user request is a task; the user defines it and approves plan/implementation. Stage gates are `/check` commands.

| Command | Stage | Who and when |
|---|---|---|
| `/resume` | Context | User-invoked |
| — | Define task | User request itself |
| `/check-analisis` | Analyze | Automatic: agent applies right after each request, before anything else |
| `/check-planeacion` | Plan | User-invoked: agent creates plan and waits approval |
| `/check-implementacion` | Implement | User-invoked: approves plan and authorizes implementation |
| `/check-tests` | Verify | Only when request requires tests; otherwise skipped |
| `/check-cierre` | Close | Automatic: agent self-verifies after implementation, including reviewers |
| `/save` | Save | User-invoked when closing session; never automatic or anticipated |

Task rules:
1. User invokes `/resume`, then sends request (task definition).
2. Apply `/check-analisis` automatically (task readiness, gap, impact, risks, viable approaches); read only necessary docs. Never skip, even for simple inspections or read-only requests.
3. Create plan only on `/check-planeacion`.
4. Implement only after `/check-implementacion` approval; minimal approved change.
5. Validate after change: lint + typecheck always when code changed; `/check-tests` only when required.
6. Apply `/check-cierre` automatically: verify acceptance criteria, review diff, run reviewers (code-reviewer, docs-reviewer), update AGENTS.md/tracker.md if changed.
7. Deliver closing report and wait approval before continuing.
8. User invokes `/save` at session end to update session history.
9. Never work on more than one task at a time.

## Keep Documents Updated
- After each validated task/phase, update AGENTS.md if existing sections changed; only update existing sections (new topics → Session History).
- Keep AGENTS.md short and useful for a new developer: clear headings/lists.
- Update `docs/history/tracker.md` when task/phase status changes; add new phase tables only when defined by MVP Execution Plan.
- Include AGENTS.md and tracker.md diffs in task report; approved together with task.
- All official documentation lives in `docs/` and is the single source of truth.

## Restrictions
- No new dependencies without authorization.
- No modifications to architecture, data model, workflow, tech stack, or business rules without authorization.
- No modifications to official documentation without authorization.

## Validation & Commands
- `ruff check .` — lint (E/F/I/N/W, line length 100)
- `mypy .` — typecheck (strict)
- `pytest tests/` — test suite (currently 199 passing)
- Local venv runs Python 3.14.6 (3.12 unavailable).

Definition of Done:
- Run only relevant validations: lint + typecheck always when code changed; pytest only when change requires tests.
- Review official acceptance criteria in MVP Execution Plan.
- Deliver report: Objective, Modified files, Validations performed, Result, Issues encountered.
- Testing strategy: unit tests with fixtures in `tests/fixtures/`; integration tests tagged (Playwright); LLM responses mockable; data layer tested with temporary SQLite files.

## Key Documents
| Doc | Covers |
|---|---|
| DOC-00 | Glossary |
| DOC-01 | Functional requirements |
| DOC-03 | Decision model |
| DOC-04 | Data flow |
| DOC-05 | Project standards (naming, formats) |
| DOC-06 | Error handling |
| DOC-07 | Folder architecture |
| DOC-08 | Scope and objectives |
| DOC-09 | Job sources research (LinkedIn) |
| DOC-11 | Technology stack |
| DOC-12 | General system architecture |
| DOC-13 | Data model |
| MVP Execution Plan | Build order and acceptance criteria per task |
| tracker.md | Current status of each phase and task |

Reading order: DOC-00 first → document related to current task → documents referenced by it. Do not read unnecessary documentation.

## Version Control
- Develop each phase/module/significant change in a dedicated branch; use descriptive names (e.g., `modulo-1`, `docs/...`).
- Branch stays active until user explicitly requests merge to `main`; never merge without explicit authorization.

## Session History
- `/save` is the only command that updates session history, tracker, and their commit/push; runs only on user invocation — agent never executes or anticipates it.
- At session end, update `docs/history/session history.md`: one entry per OpenCode session (create/update current session number), newest first, cumulative.
- Session number is sequential (last + 1); each entry includes OpenCode session ID from local DB:
  ```bash
  sqlite3 ~/.local/share/opencode/opencode.db "SELECT id, substr(title,1,60) FROM session ORDER BY time_updated DESC LIMIT 1;"
  ```
- Entry format — three sections, short and useful for a new developer, keyword-style bullets, one line per bullet:
  - **Topics** — keyword bullets; no commit hashes, file paths, or rule numbers.
  - **Decisions** — only new or modified decisions.
  - **Status** — completed/pending phases (✅/⬜); Ruff/mypy/pytest results if changes made; active branch.
- Past detail preserved in git; never expand old entries with new information.

## Uncertainty
Never invent a solution: stop, explain the problem, and wait for a decision.
