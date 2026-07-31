# Execution Report — Phase 2: Shared Services (Cross-cutting Layer)

> **Date:** 24/07/2026
> **Project:** Job Search Automation
> **Objective:** Implement the shared services layer (SRV-001, SRV-002, SRV-005, SRV-009 from DOC-12) and their unit tests.

---

## 1. Executed Objective

Implement the 3 remaining shared services (`ia_service`, `decision_engine`, `state_machine`), the `Profile` model, their unit tests, and final validation, following the optimized order of the MVP execution plan.

---

## 2. Activities Performed

| Order | Task | Description |
|-------|------|-------------|
| 1 | `Profile` model + `config.yaml` section | Added `Profile(BaseModel)` class with 11 fields to `shared/models.py`. Added `profile` section with default values in `config/config.yaml`. |
| 2 | `shared/ia_service.py` | Multi-provider AI service: `load_prompt()`, `render_prompt()`, `_route_provider()`, `_send_local()` (Ollama), `_send_cloud()` (Ollama Cloud), `_validate_response()`, `analyze(purpose)`. 4 ER-LLM error codes. |
| 3 | `shared/decision_engine.py` | Rule engine: `evaluate(offer, profile)`, 6 weighted criteria with RapidFuzz, `load_profile()` from config, salary penalty, automatic company exclusion. |
| 4 | `shared/state_machine.py` | State machine: `VALID_TRANSITIONS` map with 6 transitions, `transition()` with validation, `possible_transitions()`. Raises `InternalError` ER-INT-010 if invalid. |
| 5 | Unit tests | 4 files created: `test_ia_service.py` (10), `test_decision_engine.py` (11), `test_persistence.py` (6), `test_state_machine.py` (10) = **37 tests**. Added `example_profile` fixture in `conftest.py`. |
| 6 | Final validation | `ruff check .` → 0 errors. `mypy .` → 0 errors. `pytest tests/ -v` → 37/37 passed. All modules importable OK. |

---

## 3. Files Created

| File | Approx Lines | Purpose |
|------|-------------|---------|
| `shared/ia_service.py` | ~190 | Multi-provider communication (Ollama local + Ollama Cloud), prompt loader, purpose-based routing, response validation |
| `shared/decision_engine.py` | ~120 | Weighted offer vs profile evaluation with 6 criteria |
| `shared/state_machine.py` | ~40 | Lifecycle state transition control |
| `tests/test_ia_service.py` | ~90 | 10 tests (httpx mocks, validation, ER-LLM errors) |
| `tests/test_decision_engine.py` | ~100 | 11 tests (scoring, classification, exclusion) |
| `tests/test_persistence.py` | ~50 | 6 tests (CRUD with temporary files) |
| `tests/test_state_machine.py` | ~60 | 10 tests (6 valid, 1 invalid, possible_transitions) |

---

## 4. Files Modified

| File | Change |
|------|--------|
| `shared/models.py` | +14 lines: `Profile(BaseModel)` class with 11 fields |
| `config/config.yaml` | +13 lines: `profile` section with default values |
| `tests/conftest.py` | +17 lines: `example_profile()` fixture with typical test data |
| `MVP Execution Plan.md` | Phase 2 rewritten with detailed specification of 6 tasks |
| `MVP Tracking.md` | Phase 2 table updated with ✅ status |
| `Session History.md` | Session 2 updated with evening activities |

---

## 5. Implementation Details

### 5.1. `Profile` Model

Pydantic class with 11 fields loaded from `config.yaml`:

| Field | Type | Purpose |
|-------|------|---------|
| `technologies` | `dict[str, int]` | Known technologies with proficiency level |
| `experience_years` | `int` | Years of professional experience |
| `languages` | `dict[str, str]` | Languages with level (e.g. "C1") |
| `preferred_locations` | `list[str]` | Locations where to search for jobs |
| `preferred_modalities` | `list[str]` | Accepted modalities (remote, hybrid, etc.) |
| `minimum_salary` | `float \| None` | Minimum acceptable salary |
| `seniority` | `str` | Seniority level |
| `target_companies` | `list[str]` | Companies of interest |
| `excluded_companies` | `list[str]` | Companies to avoid (automatic discard) |
| `education_level` | `str` | Educational level achieved |

### 5.2. `shared/ia_service.py`

Multi-provider service architecture:

```
analyze(prompt_id, context, purpose="evaluation")
  ├── load_prompt(prompt_id) → str
  │     └── Reads prompts/{category}/{prompt_id}.md
  │     └── ConfigurationError if not found
  ├── render_prompt(template, context) → str
  │     └── Replaces {{ variable }} with values
  ├── _route_provider(purpose) → "local" | "cloud"
  │     └── Routing from config.yaml → ia_routing
  │     └── ConfigurationError if invalid provider
  ├── _send_local(prompt) → str  [@retry_decorator]
  │     └── httpx POST to http://{host}:{port}/api/generate
  │     └── ER-LLM-001 (connection), ER-LLM-002 (timeout), ER-LLM-003 (HTTP)
  ├── _send_cloud(prompt) → str  [@retry_decorator]
  │     └── httpx POST to {endpoint}/api/generate with API Key
  │     └── ER-LLM-001 (connection), ER-LLM-002 (timeout), ER-LLM-003 (HTTP)
  └── _validate_response(raw) → dict
        └── ER-LLM-003 (not JSON), ER-LLM-004 (not dict)
```

### 5.3. `shared/decision_engine.py`

Evaluation criteria with weights from `config.yaml`:

| Criterion | Weight | Matching Algorithm |
|-----------|--------|-------------------|
| Experience | 0.30 | Year comparison (`min(100, profile / offer * 100)`) |
| Technology | 0.25 | RapidFuzz `token_sort_ratio` average |
| Location | 0.15 | RapidFuzz `partial_ratio` against preferences |
| Modality | 0.10 | Exact match (case-insensitive) |
| Languages | 0.10 | Proportion of languages covered |
| Seniority | 0.10 | Level match (with 1-level tolerance) |

Additional business rules:
- Company in `excluded_companies` → **automatic discard** (score = 0)
- Offer salary < `minimum_salary` → **penalty** of up to 30 points
- Classification: ≥80 → HIGH, ≥50 → MEDIUM, <50 → LOW
- Decision: HIGH/MEDIUM → CONTINUE, LOW → DISCARD

### 5.4. `shared/state_machine.py`

Valid transitions defined:

```
DISCOVERED  → PREPARED
PREPARED    → EVALUATED
EVALUATED   → ACCEPTED | DISCARDED
ACCEPTED    → PROCESSED
DISCARDED   → FINALIZED
PROCESSED   → FINALIZED
```

Any other transition raises `InternalError` (ER-INT-010).

---

## 6. Validations Executed

| Tool | Command | Result |
|------|---------|--------|
| Ruff | `ruff check .` | 0 errors |
| MyPy | `mypy .` | 0 errors (16 files) |
| Pytest | `pytest tests/ -v` | 37/37 passed (12.53s) |
| Importability | `python -c "import shared.ia_service, shared.decision_engine, shared.state_machine"` | OK |

---

## 7. Problems Found and Fixes

| Problem | File | Fix |
|---------|------|-----|
| `typing.Any` imported but unused | `shared/decision_engine.py` | Removed the import |
| 43 mypy errors due to missing `-> None` | 4 test files | Added type annotations to all functions |
| `type: ignore` not used | `tests/test_decision_engine.py` | Replaced with direct `uuid4()` |
| Untyped mock parameters | `tests/test_ia_service.py` | Added `MagicMock` type to 4 parameters |

---

## 8. Identified Risks

- `ia_service.py` supports two providers: Ollama local (for evaluation) and Ollama Cloud (for processing). Tests use httpx mocks for both.
- The cloud provider requires an Internet connection and an Ollama Cloud API Key configured in `.env`. Without it, deep processing (Phase 7) will not work.
- The Ollama Cloud free tier has usage limits that must be monitored during Phase 7.
- Evaluation weights in `config.yaml` (`evaluation.weights`) represent initial values and may require fine-tuning during Phase 6 (Initial Evaluation) with real offers.
- The `ia_service` prompt loader reads from the `prompts/` directory which currently only contains `.gitkeep`. Prompts will be created in Phase 3.
- The `git add` command incorrectly omitted `.opencode/commands/save.md` and `AGENTS.md` in previous commits; they were included in the final commit of this phase.

---

## 9. Current Project Status

| Phase | Status |
|-------|--------|
| Phase 0 — Startup Preparation | ✅ Completed |
| Phase 1 — Common System Foundation | ✅ Completed |
| **Phase 2 — Shared Services** | **✅ Completed** |
| Phase 3 — Initial Prompts | ⬜ Pending |
| Phase 4 — Module 1: Discovery | ⬜ Pending |
| Phase 5 — Module 2: Preparation | ⬜ Pending |
| Phase 6 — Module 3: Initial Evaluation | ⬜ Pending |
| Phase 7 — Module 4: Deep Processing | ⬜ Pending |
| Phase 8 — Module 5: Results Management | ⬜ Pending |
| Phase 9 — MVP Integration | ⬜ Pending |

---

## 10. Commit and Deployment

| Aspect | Detail |
|--------|--------|
| Hash | `32b2723` |
| Message | `feat: complete Fase 2 — shared services layer` |
| Files in commit | 15 (7 created, 8 modified) |
| Lines added | +1009 |
| Push | `main → origin/main` (GitHub) |

---

*End of report*
