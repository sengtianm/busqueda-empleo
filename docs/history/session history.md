# Session History

> Chronological record of OpenCode work sessions.

---

## Session 1 — 23/07/2026

**Topics:**
- MVP execution plan (9 phases)
- MVP Tracking.md and session persistence system (`/save`, `/resume`)
- LinkedIn confirmed as the only source for the MVP
- 17 RT rules, 11 ACs, and EP strategy documented in AGENTS.md
- Directory structure, documentation migration, git init, GitHub
- Phase 1 completed: `shared/*`, configuration, tests, validation
- Lint/typecheck cleanup (N818 ignored, `ErrorBase` → `BaseError`)

**Decisions:**
- 9-phase plan approved
- LinkedIn as the only source
- N818 ignored due to Spanish naming convention
- Remote repository created
- Session rules adopted (one session per day, automatic save, DD/MM/YYYY)

**Status:**
- Phase 0 ✅, Phase 1 ✅
- Ruff 0, mypy 0
- Approval pending for Phase 2

---

## Session 2 — 24/07/2026

**Topics:**
- [Morning] Review of session history saving rules
- RT-018 to RT-021 formalized in AGENTS.md
- Session history consolidated (5 entries → 1)
- [Afternoon] Phase 2 planning: Profile model (Pydantic, no database)
- Phase 2 completed: `ia_service`, `decision_engine` (RapidFuzz), `state_machine`, tests
- Weight validation in `decision_engine`
- [Evening] Phase 3 completed: 5 prompts (PRM-001 to PRM-005) using Annex 5C template
- Manual Ollama test pending (timeout caused by the "thinking" model)

**Decisions:**
- RapidFuzz selected for fuzzy matching
- Profile implemented as a Pydantic value model loaded from `config.yaml`
- Prompts released as v1, pending manual testing
- Phase 4 not blocked by the pending Phase 3 manual test

**Status:**
- Phase 0 ✅, Phase 1 ✅, Phase 2 ✅
- Phase 3: Tasks 1–3 ✅, Task 4 ⏳, Task 5 ⬜
- Ruff 0, mypy 0, pytest 39/39

---

## Session 4 — 29/07/2026

**Topics:**
- [Morning] Rollback of the previous Phase 4 implementation
- Destructive reset to the post–Phase 3 commit
- Removed the `experiment/scroll-inventario` branch and cleaned the database and `pycache`
- [Afternoon] Persistence migration: Excel/openpyxl → SQLite
- 7 normalized tables + `sequence_ids` with prefixes
- Models updated: UUID → `str`, creation/update timestamps
- `persistence.py` rewritten using SQLite, tests updated
- Documentation updated (DOC-11, Annex 5A, AGENTS, README, plan, tracking)
- `modulo-1` branch, not merged into `main`

**Decisions:**
- Previous Phase 4 implementation discarded
- SQLite replaces openpyxl as the persistence layer
- IDs use the `{PREFIX}-{NUM:04d}` format

**Status:**
- SQLite persistence ✅
- Phases 0–3 ✅, Phase 4 ⬜
- Ruff 0, mypy 0, pytest 47/47
- Branch: `modulo-1`

---

## Session 5 — 30/07/2026

**Topics:**
- Spanish-to-English translation of all Python code identifiers, config keys, error messages, docstrings, and variable names
- `shared/models.py`: enums (`OfferState`, `EvaluationResult`, `DecisionEvaluation`), model classes (`Profile`, `Evaluation`, `ProcessedOffer`, etc.), and field names updated
- `shared/config.py`: renamed internal variables, `load`/`reload_config` functions
- `shared/errors.py`: `Severity`, `ConfigurationError`, parameter/attribute names translated
- `shared/decision_engine.py`: all functions, config keys, error strings, field accesses translated
- `shared/ia_service.py`: all functions, config keys (`ai_local`, `ai_cloud`, `ai_routing`), error strings, parameter names translated
- `shared/persistence.py`: functions, SQL columns, CHECK constraint, error strings translated
- `shared/state_machine.py`, `shared/retry.py`, `shared/logging_setup.py`: functions and config keys translated
- `config/config.yaml`: `pesos` → `weights`, profile field names aligned with model
- All test files and fixtures updated to match
- Ruff and mypy pass clean

**Decisions:**
- Inner keys of `evaluation.weights` (experiencia, tecnologia, ubicacion, etc.) kept as-is per instruction
- Config keys `ai_routing` included in translation (`ia_routing` → `ai_routing`)

**Status:**
- Phases 0–3 ✅, Phase 4 ⬜
- Ruff 0, mypy 0, pytest 47/47
- Branch: `modulo-1`
