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
- [Morning] Spanish-to-English translation of all Python code identifiers, config keys, error messages, docstrings, and variable names
- `shared/models.py` and `shared/persistence.py`: kept entirely in Spanish (data layer, per final decision)
- `shared/errors.py`: `Severity`, typed error hierarchy, parameter/attribute names translated; error prefixes (ER-*) preserved
- `shared/decision_engine.py`: all functions, config keys, error strings, field accesses translated
- `shared/ia_service.py`: all functions, config keys (`ai_local`, `ai_cloud`, `ai_routing`), error strings, parameter names translated
- `shared/state_machine.py`, `shared/retry.py`, `shared/logging_setup.py`: functions and config keys translated
- `config/config.yaml`: `pesos` → `weights`, profile field names aligned with model
- All test files and fixtures updated to match
- [Afternoon] Architecture review executed and documented (`docs/reports/Architecture Review.md`)
- Offer lifecycle unified to the 7 implemented states (DOC-01 §12/§13 and DOC-13A §3.1 rewritten)
- Docs aligned with the cloud-primary AI strategy (DOC-11) and real names (`ai_routing`, `job_search.db`, `version_modelo`, `region`)
- MVP persistence scope and Catalog deferral formalized in DOC-13A; deviations recorded; version history created
- MVP plan corrected (EST catalog references, `discovered → prepared` initial state)
- `data/*.db` added to `.gitignore`; `job_search.db` untracked (`git rm --cached`)
- Duplicated prompt scripts removed (`test_prompt.py` deleted; `probar_prompt.py` → `prompt_tester.py`; `contextos_prompt.yaml` → `prompt_contexts.yaml`)
- `load_profile()` now warns on incomplete profile (Loguru); test added
- [Evening] C2 resolved (decision: prompts adjusted to the entity): PRM-002..005 redesigned to v2, chained, covering the 18 attributes of Detailed Evaluation
- Detailed Evaluation entity attributes renamed to Spanish in DOC-13A §2.7; catalogs 3.15/3.16 in Spanish
- `ProcessingResult` → `EvaluacionDetallada` in `shared/models.py`
- Prompt placeholder bug fixed: `{{ offer }}`/`{{ profile }}` never matched the injected `oferta`/`perfil` — data was not injected (pre-existing)
- Official Data Dictionary (DOC-13A §5.5, 13 entities) and ERD (§6.6, Mermaid + ASCII) created
- [Night] Real retest of PRM-001..005 against `gemma4:31b-cloud` (local Ollama as authenticated proxy; no API key needed)
- Variable injection confirmed working in real execution (placeholder fix validated end-to-end)
- Finding: PRM-001..004 generated content in English; mandatory Spanish output instruction added to the 5 prompts
- Final retest: 5/5 valid JSON, expected fields, Spanish content, correct catalog values
- Retest report generated; C2 resolution closed with validated retest

**Decisions:**
- Inner keys of `evaluation.weights` (experiencia, tecnologia, ubicacion, etc.) kept as-is per instruction
- Config keys `ai_routing` included in translation (`ia_routing` → `ai_routing`)
- C1: keep the 7 implemented states; EST catalog of DOC-01 is the single source of truth
- A3: Spanish for everything data-related (DB schema, `models.py`, `persistence.py`, profile/evaluation data in `config.yaml`, test fixture data); English for everything else
- C3: cloud-primary AI strategy with configurable local fallback
- A1/M1: MVP persists only `secuencia_ids`, `fuentes`, `empresas`, `ubicaciones`, `ofertas`; Catalog deferred to Modules 2-3
- C2: prompts adjusted to the entity (PRM-002..005 redesigned to v2, chained); cover letter draft and interview preparation deferred to the document generation phase
- Prompt placeholders fixed to match injected variables (Spanish names)
- All prompts must include the mandatory Spanish output instruction (generated content is stored data)
- No commit made; changes left staged in the working tree

**Status:**
- Phases 0–3 ✅, Phase 4 ⬜
- Ruff 0, mypy 0, pytest 48/48
- Branch: `modulo-1`
