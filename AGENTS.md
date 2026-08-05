# AGENTS.md

# Job Search Automation

## Project

Automated solution that discovers, collects, prepares, evaluates, processes, and manages job opportunities, reducing the time and effort of the job search while supporting the user's decision-making.

**Current status**: MVP in progress. Phases 0-3 completed (infrastructure, shared services, prompts tested with `gemma4:31b-cloud`). Current work: Phase 4 — Module 1 (Opportunity Discovery) on branch `modulo-1`. Phases 5-9 pending. See `docs/history/tracker.md` for the authoritative status.

## Objective

Design, develop, and implement an automated job search pipeline — from discovering offers to generating the inputs for a high-quality application — keeping full traceability and minimizing manual intervention (see DOC-08).

## Architecture

Three-layer architecture:

```
Functional modules → Shared services → Infrastructure
```

General workflow:

```
Discovery → Preparation → Evaluation → Processing → Management
```

All implementations must follow this architecture (details in DOC-12).

## Technology Stack

- Python 3.12
- Playwright
- BeautifulSoup + lxml
- SQLite
- Pydantic
- httpx
- Loguru
- RapidFuzz
- Tenacity
- Ollama
- PyYAML
- python-dotenv
- pytest
- Ruff
- mypy

## Project Structure

- `docs/` — Official documentation (project-design, plans, reports, history)
- `config/` — Centralized system configuration (`config.yaml`, `.env.template`)
- `prompts/` — Official prompts (kept separate from code)
- `modules/` — Functional modules: discovery, preparation, evaluation, processing, management
- `shared/` — Reusable resources (config, errors, logging, retry, models, persistence, ia_service, decision_engine, state_machine)
- `data/` — Persistent data (input, processing, output, backup)
- `logs/` — Logs and audit
- `temp/` — Temporary files
- `scripts/` — Auxiliary scripts (e.g., prompt tester)
- `tests/` — Tests (fixtures in `tests/fixtures/`)

## Conventions

- **English** for all code, documentation, configuration, prompts, commit messages, directory and file names.
- **Spanish** for everything data-related: the SQLite database (`job_search.db`), `shared/models.py`, `shared/persistence.py`, profile and criteria in `config.yaml`, and test fixtures.
- **Spanish** for all conversations with the user.
- Configuration must be separated from business logic.
- Prompts must be separated from the code.
- No hardcoded values.
- Every transformation must preserve the original data.
- No functional module may access the database directly.
- Never include API keys, tokens, passwords, or sensitive data in repository files.

## Workflow

Work cycle: `Context → Define task → Analyze → Plan → Implement → Verify → Close`. Each user request starts a task that goes through these stages; the user defines the task and approves the plan and the close. Each stage has a mandatory check invoked as a `/check-*` command. Apply the check at its stage before moving on; the checklist and expected response format are defined in the command itself.

| Stage | Check command |
|-------|---------------|
| Context (resume project state) | `/resume` |
| Define the task | `/check-planeacion` |
| Analyze the affected area before proposing the plan | `/check-analisis` |
| Confirm the minimal plan before implementing | `/check-implementacion` |
| Verify tests, lint and typecheck after the change | `/check-tests` |
| Verify completion and close | `/check-cierre` |

For each task:

1. Resume context (apply `/resume`). The user defines the task.
2. Apply `/check-planeacion` to confirm the task is well defined; ask only the questions needed.
3. Apply `/check-analisis` (relevant files, flow, risks, minimal plan) and read only the necessary documentation.
4. Present a plan and wait for approval.
5. Apply `/check-implementacion` and implement the minimal approved change.
6. Validate (apply `/check-tests`).
7. Update AGENTS.md and docs/history/tracker.md if they changed.
8. Deliver a report applying `/check-cierre` (including the AGENTS.md and tracker.md changes).
9. Wait for approval before continuing.

Never work on more than one task at a time.

## Keep Documents Updated

- After each validated task or phase, update this file if any of its existing sections changed.
- Only update existing sections: never add new topics or sections (new topics belong in Session History).
- Keep the file short and useful: write it for a new developer, using clear headings and lists.
- Update `docs/history/tracker.md` when a task or phase changes status; add new phase tables only when defined by the MVP Execution Plan.
- Include the AGENTS.md and tracker.md diffs in the task report; they are approved together with the task.

## Restrictions

- Do not add new dependencies without authorization.
- Do not modify the architecture, data model, workflow, tech stack, or business rules without authorization.
- Do not modify official documentation without authorization.

## Commands

- `ruff check .` — Lint (E/F/I/N/W rules, line length 100)
- `mypy .` — Type check (strict)
- `pytest tests/` — Test suite (currently 47 passing)

Note: local venv runs Python 3.14.6 (3.12 unavailable).

## Validation (Definition of Done)

Before completing a task:

- Run only the validations relevant to the change: lint, type check, and tests when code changed.
- Review the official acceptance criteria in the MVP Execution Plan.
- Deliver a report with: Objective, Modified files, Validations performed, Result, Issues encountered.

Testing strategy: unit tests with fixtures in `tests/fixtures/`, integration tests tagged (Playwright), LLM responses mockable, data layer tested with temporary SQLite files.

## Response Style

- Respond in Spanish, concisely, using clear headings and lists.
- Never modify files without explaining first.

## Key Documents

| Doc | Covers |
|-----|--------|
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

Reading order: DOC-00 first, then the document related to the current task, then documents referenced by it. Do not read unnecessary documentation.

## Version Control

- Develop every phase, module, or significant change in a dedicated branch.
- Use descriptive branch names (e.g., `modulo-1`, `docs/...`).
- The branch stays active until the user explicitly asks to merge into `main`.
- Do not merge any branch without explicit authorization.

## Documentation

All official documentation lives in `docs/` and is the single source of truth.

## Session History

At the end of each session, update `docs/history/session history.md` with one entry per OpenCode session (create or update the entry for the current session number), newest first, cumulative, in three sections:

- The session number is sequential (last number + 1). Each entry includes its OpenCode session ID, obtained from the local database: `sqlite3 ~/.local/share/opencode/opencode.db "SELECT id, substr(title,1,60) FROM session ORDER BY time_updated DESC LIMIT 1;"`.
- Keep every entry short and useful for a new developer: clear keyword-style lists, one line per bullet.
- **Topics** — Keyword-style bullets, one line each. No commit hashes, file paths, or rule numbers.
- **Decisions** — Only new or modified decisions.
- **Status** — Completed/pending phases (✅/⬜), Ruff/mypy/pytest results if changes were made, active branch.
- Past detail is preserved in git; never expand old entries with new information.

## When There Is Uncertainty

Never invent a solution: stop, explain the problem, and wait for a decision.
