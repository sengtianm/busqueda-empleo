# MVP Tracker

> Current status of each task from the [MVP Execution Plan](MVP%20Execution%20Plan.md).

## Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Pending — not started |
| ⏳ | In progress — actively being worked on |
| ✅ | Completed — passed validation and approved |
| ❌ | Blocked — something prevents progress |

---

## Phase 0. Startup Preparation

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | Confirm MVP scope (LinkedIn single source) | DOC-01, DOC-08, DOC-09 | ✅ | No documentary contradictions. LinkedIn confirmed as MVP's only source (DOC-09 §3.10). |
| 2 | Define work rules with OpenCode | — | ✅ | Work rules documented in AGENTS.md (Workflow, Restrictions, Response Style). |
| 3 | Establish acceptance criteria per step | Execution Plan | ✅ | Acceptance criteria documented in AGENTS.md (Validation) and in the MVP Execution Plan. |
| 4 | Decide testing strategy | Execution Plan | ✅ | Testing strategy documented in AGENTS.md (Validation) and MVP Execution Plan Phase 0. |

---

## Phase 1. Common System Foundation (Infrastructure)

| Order | # | Task | Source docs | Status | Notes |
|-------|---|------|-------------|--------|-------|
| 1 | 1 | Directory structure | DOC-07 | ✅ | 19 directories + README.md created. Documentation migrated to `docs/`. 17 `.gitkeep` added. |
| 2 | 2a | Version control initialization | — | ✅ | `git init`, `.gitignore`, initial commit. Repo: `github.com/sengtianm/busqueda-empleo`. |
| 3 | 3 | venv + requirements.txt | DOC-11 | ✅ | Python 3.14.6 (3.12 unavailable). Full stack. `playwright install chromium` executed. |
| 4 | 4 | config.yaml + .env.template | DOC-05 | ✅ | config.yaml with navigation, evaluation, persistence, AI, retry, logging, profile sections. |
| 5 | 11 | pyproject.toml (Black, Ruff, mypy) | DOC-05, DOC-11 | ✅ | Black (100 chars, py312), Ruff (E/F/I/N/W), mypy (strict). |
| 6 | 5 | shared/config.py | DOC-05, DOC-11 | ✅ | Unified YAML + .env loading with cache. |
| 7 | 7 | shared/errors.py (ER hierarchy) | DOC-06, Annex 5A | ✅ | BaseError + 10 subclasses (ER-RED, ER-NAV, ER-EXT, ER-VAL, ER-LLM, ER-DAT, ER-DB, ER-CFG, ER-INT, ER-EXTS). |
| 8 | 6 | shared/logging_setup.py | DOC-06 | ✅ | Loguru with stdout + file rotation. |
| 9 | 8 | shared/retry.py (Tenacity) | DOC-06 | ✅ | retry_decorator with config-driven policies + exponential backoff. |
| 10 | 10 | shared/models.py (Pydantic) | DOC-13 | ✅ | Offer, Company, Source, Location, ProcessedOffer, Evaluation, EvaluacionDetallada. 3 Enums. |
| 11 | 9 | shared/persistence.py (SQLite) | DOC-13 | ✅ | SQLite via sqlite3. 7 tables + id_sequence. generate_id, read_table, write_row, find_by_id, update. Sequential IDs with prefix (EMP-0001). |
| 12 | 12 | tests/conftest.py + tests/fixtures/ | — | ✅ | Fixtures: clear_config_cache, example_models, temp_xlsx_file. |
| 13 | 13 | Final validation | — | ✅ | ruff → 0 errors. mypy → 0 errors. All imports OK. pytest (0 tests, infra ready). |

---

## Phase 2. Shared Services (Cross-cutting Layer)

> **Optimized order:** Phase 3 can begin after completing task 2 (`ia_service.py`).

| Order | # | Task | Source docs | Status | Notes |
|-------|---|------|-------------|--------|-------|
| 1 | 1 | `Profile` model in `shared/models.py` + `profile` section in `config.yaml` | DOC-10, DOC-03 | ✅ | Loaded from config.yaml as a value model (not a persistent entity). |
| 2 | 2 | `shared/ia_service.py` (multi-provider local + cloud) | DOC-11, DOC-12 | ✅ | Hybrid architecture: `_send_local` (Ollama + qwen3.5:4b) + `_send_cloud` (Ollama Cloud + Gemma 4 31B). Purpose-based routing from config. 4 ER-LLM error codes. |
| 3 | 3 | `shared/decision_engine.py` (rules + scoring) | DOC-03, DOC-10 | ✅ | `evaluate(offer, profile)`. 6 weighted criteria. RapidFuzz. Salary penalty. Auto-exclusion. |
| 4 | 4 | `shared/state_machine.py` (states + transitions) | DOC-03, DOC-04 | ✅ | 6 transitions defined in immutable map. Raises ER-INT-010 if invalid. |
| 5 | 5 | Tests: ia_service, decision_engine, persistence, state_machine | — | ✅ | 37 tests (11 decision_engine, 10 ia_service, 6 persistence, 10 state_machine). Fixture `example_profile`. |
| 6 | 6 | Validation: ruff → mypy → pytest | — | ✅ | ruff 0 errors, mypy 0 errors, 37/37 tests passed. All modules importable. |

---

## Phase 3. Initial Prompts

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | prompts/initial_evaluation/ | DOC-03, DOC-12 | ✅ | Created PRM-001 compatibility.md with Annex 5C structure. |
| 2 | prompts/processing/ | DOC-12 | ✅ | Created PRM-002 to PRM-005: diagnosis, strategic_extraction, application_design, inputs. |
| 3 | PRM-XXX identifiers + Annex 5C template | Annex 5A, 5C | ✅ | All 5 prompts follow official template C.9 (Objective, Inputs, Variables, Instructions, Output, Notes, Version). |
| 4 | Manual test with AI (local + cloud) | — | ✅ | All 5 prompts tested against `gemma4:31b-cloud` via local Ollama as proxy. All return valid JSON with coherent content. Local model `qwen3.5:4b` discarded due to timeout (60s+). Routing changed to cloud for evaluation and processing. |
| 5 | Version 1 approved | — | ✅ | All 5 prompts (PRM-001 to PRM-005) work correctly with `gemma4:31b-cloud`. Pending formal Architect review. |
| 6 | Alignment with Detailed Evaluation (decision C2) | DOC-13A §2.7 | ✅ | PRM-002..005 redesigned to v2: each produces exactly the entity fields (resultado_organizacional, problema_organizacional, perfil_profesional_requerido / coincidencias_perfil, logica_xyz, hipotesis_valor, informacion_descartada / ajuste_tecnico, ajuste_funcional, ajuste_estrategico + justifications / riesgo_sobrecalificacion, recomendacion_final + justifications, insumos_carta_presentacion). Chained execution. `ProcessingResult` → `EvaluacionDetallada`. Retest 2026-07-30 against `gemma4:31b-cloud`: 5/5 valid JSON with expected fields and coherent content; Spanish output instruction added to the 5 prompts (see `Prompt Retest Report.md`). |

---

## ⚙ Pre-migration (before Phase 4)

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| — | Migrate persistence: Excel/openpyxl → SQLite + sequential IDs | — | ✅ | shared/models.py: UUID→str, ISO dates. shared/persistence.py: SQLite with sequences. config.yaml: persistence to db_file. Tests adapted. Validation: ruff 0, mypy 0, pytest 47/47. Branch `modulo-1`. |

## Phase 4. Module 1 — Opportunity Discovery

> Build strategy: functional sub-phases grouping nodes by testable unit. Each sub-phase goes through its own work cycle. See the MVP Execution Plan Phase 4.

| # | Sub-phase (nodes) | Source docs | Status | Notes |
|---|---|---|---|---|
| 0 | Prerequisite: preparation plan (7 phases) completed | Análisis comparativo M1, Plan de Preparación | ✅ | DOC-13/13A, DOC-04, DOC-06, DOC-01, DOC-12, DOC-09/9A, DOC-00/5A, config.yaml, models.py, persistence.py, errors.py, retry.py, conftest.py, discovery/ scaffold, linkedin adapter. 102 tests passing. |
| 4.1 | Startup and source control (INICIO + 3 nodes) | Ficha técnica | ✅ | INICIO + 3 control nodes implemented and validated: run instantiation, config (ERR-02..04/11), DB probe (ERR-05), concurrency lock (ERR-06..09), source validation with ERR-12 discard, run state (ERR-10), existence decision, iteration decision, source selection. 136 tests passing. |
| 4.2 | Platform entry (2 nodes) | Ficha técnica, DOC-09, Annex 9A | ⬜ | LinkedIn login, credentials, conditional retries, entry_result. |
| 4.3 | Filter search (2 nodes) | Ficha técnica, DOC-09 | ⬜ | Set iterator, adapter search, search_result. |
| 4.4 | Capture and registration (4 nodes) | Ficha técnica, DOC-09, DOC-13, DOC-04 | ⬜ | Capture policies, batch write, Grupo A/B, pagination loop. |
| 4.5 | Closure and orchestrator (2 nodes) | Ficha técnica | ⬜ | Termination, lock release, full flow integration. |

---

## Phase 5. Module 2 — Offer Preparation

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | Structure modules/preparation/ | DOC-07 | ⬜ | |
| 2 | Load raw offers from persistence | DOC-04 | ⬜ | |
| 3 | Field cleaning (spaces, residual HTML) | DOC-05 | ⬜ | |
| 4 | Normalization (dates, salaries, location, modality) | DOC-05, DOC-13 | ⬜ | |
| 5 | Integrity and required field validation | DOC-01 | ⬜ | |
| 6 | Duplicate detection (RapidFuzz) | DOC-01 | ⬜ | |
| 7 | Initial state assignment | DOC-03 | ⬜ | |
| 8 | Persistence of prepared version + log | DOC-04 | ⬜ | |
| 9 | Error handling (ER-VAL, ER-DAT) | DOC-06 | ⬜ | |
| 10 | Tests | — | ⬜ | |
| 11 | Validation | — | ⬜ | |

---

## Phase 6. Module 3 — Initial Evaluation

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | Structure modules/evaluation/ | DOC-07 | ⬜ | |
| 2 | Load prepared offers + profile | DOC-04 | ⬜ | |
| 3 | Rule engine (decision_engine) | DOC-03 | ⬜ | |
| 4 | Optional LLM invocation | DOC-12 | ⬜ | |
| 5 | Classification (High / Medium / Low) | DOC-01 | ⬜ | |
| 6 | Continue/discard decision + justification | DOC-03 | ⬜ | |
| 7 | Persistence of results + traceability | DOC-04 | ⬜ | |
| 8 | Error handling (ER-LLM, ER-DAT, ER-INT) | DOC-06 | ⬜ | |
| 9 | Tests | — | ⬜ | |
| 10 | Validation | — | ⬜ | |

---

## Phase 7. Module 4 — Deep Processing

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | Structure modules/processing/ | DOC-07 | ⬜ | |
| 2 | Load accepted offers | DOC-04 | ⬜ | |
| 3 | LLM: vacancy diagnosis | DOC-01 | ⬜ | |
| 4 | LLM: strategic extraction | DOC-01 | ⬜ | |
| 5 | LLM: application design | DOC-01 | ⬜ | |
| 6 | LLM: inputs (cover letter, interview prep) | DOC-01 | ⬜ | |
| 7 | Result validation (Pydantic) | DOC-13 | ⬜ | |
| 8 | Persistence in data/output/ | DOC-04 | ⬜ | |
| 9 | Error handling (ER-LLM, ER-INT) | DOC-06 | ⬜ | |
| 10 | Tests | — | ⬜ | |
| 11 | Validation | — | ⬜ | |

---

## Phase 8. Module 5 — Results Management

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | Structure modules/management/ | DOC-07 | ⬜ | |
| 2 | Per-offer history + state management | DOC-01, DOC-03 | ⬜ | |
| 3 | Offer summary report | DOC-01 | ⬜ | |
| 4 | Export to formatted .xlsx | DOC-01 | ⬜ | |
| 5 | Traceability validation | DOC-04 | ⬜ | |
| 6 | Error handling (ER-DB, ER-DAT) | DOC-06 | ⬜ | |
| 7 | Tests | — | ⬜ | |
| 8 | Validation | — | ⬜ | |

---

## Phase 9. MVP Integration

| # | Task | Source docs | Status | Notes |
|---|------|-------------|--------|-------|
| 1 | scripts/run_mvp.py (orchestrator) | DOC-12 | ⬜ | |
| 2 | E2E test with small set of real offers | DOC-01 | ⬜ | |
| 3 | Verification: logs, errors, persistence | — | ⬜ | |
| 4 | Fix dependencies and sequence | — | ⬜ | |
| 5 | Regression: lint → typecheck → pytest | — | ⬜ | |
| 6 | Coverage review vs DOC-01 | — | ⬜ | |
| 7 | Final MVP approval | — | ⬜ | |
