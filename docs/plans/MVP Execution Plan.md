# MVP Execution Plan — Job Search Automation

> **Working document.** Defines the exact build order of the MVP, step by step, based on the approved documents (DOC-00 to DOC-13, Annexes 5A, 5B, 5C, 9A).

---

## Phase 0. Startup Preparation

1. Confirm MVP scope against DOC-01, DOC-08, DOC-09 (LinkedIn as the only source).
2. Define work rules with OpenCode: one task at a time, no advancing without approval.
3. Establish acceptance criteria per step: code written, passes lint+typecheck+tests, reviewed and approved.
4. Decide testing strategy:
   - **Unit (pytest):** business logic, rules, transformations. Fixtures in `tests/fixtures/`.
   - **Real LinkedIn integration:** Playwright + real selectors (tagged `integration`).
   - **LLM:** prompts tested with local Ollama, mockable responses in unit tests.
   - **Data layer:** tests with temporary .db files (SQLite).

---

## Phase 1. Common System Foundation (Infrastructure)

#### Completed

1. **Directory structure** per DOC-07 (full root with `docs/`, `config/`, `modules/`, `shared/`, `data/`, `logs/`, `temp/`, `scripts/`, `tests/`, `prompts/`). Includes migration of `Initial Documentation/` to `docs/` and creation of `.gitkeep` in empty directories.

2. **Phase 1.2a — Version control initialization:**
   - `git init` at the project root.
   - Create `.gitignore` according to the project stack.
   - Verify that `.gitkeep` preserves empty directories.
   - First commit with base structure and migrated documentation.
   - Create remote repository on GitHub and publish.

#### Pending (execution order)

3. **venv + requirements.txt** — Initialize `venv`, create `requirements.txt` with the full stack (DOC-11), install dependencies and run `playwright install chromium`. Validate: correct venv, pip from venv, all packages installed, playwright install without errors.

4. **config.yaml + .env.template** — Create `config/config.yaml` with functional parameters + `config/.env.template`.

5. **pyproject.toml** — Configure Black, Ruff, mypy for the project.

6. **shared/config.py** — Implement unified loading of config.yaml + .env.

7. **shared/errors.py** — Exception hierarchy by category (ER-RED, ER-NAV, ER-LLM, etc., DOC-06). Attributes: code, severity (SV-1 to SV-5), source_module, offer_id, timestamp.

8. **shared/logging_setup.py** — Loguru with standard format, rotation, and `logs/` directory.

9. **shared/retry.py** — Tenacity wrapper, policies per DOC-06.

10. **shared/models.py** — Pydantic v2 models: `Offer`, `Evaluation`, `Result`, `Company`, etc. (DOC-13). IDs as sequential strings, `creation_date`/`update_date` fields in ISO 8601.

11. **shared/persistence.py** — SQLite access via sqlite3. Methods: read, write, update, find by ID, generate sequential IDs. Path from config.

12. **tests/conftest.py + tests/fixtures/** — Basic fixtures (test config, mock logger, temp persistence) and `tests/fixtures/` directory with `.gitkeep`.

13. **Final validation:**
    - `ruff check .` with no errors.
    - `mypy .` with no errors.
    - `python -c "import shared.config, shared.errors, shared.logging_setup, shared.retry, shared.models, shared.persistence"` — all modules importable without error.
    - `pytest tests/` — all tests pass.

---

## Phase 2. Shared Services (Cross-cutting Layer)

### Optimized Execution Order

> Phase 3 (prompts) can begin immediately after completing **Task 2** (`ia_service.py`). The remaining tasks (3, 4, 5, 6) do not block Phase 3.

| Order | Task | Depends on | Blocks Phase 3? |
|-------|------|------------|------------------|
| 1 | Add `Profile` model to `shared/models.py` + `profile` section in `config.yaml` | Nothing | No |
| 2 | `shared/ia_service.py` (Ollama + prompt loader) | Task 1 (weak) | **Yes** |
| 3 | `shared/decision_engine.py` (rules + scoring) | Task 1 (strong) | No |
| 4 | `shared/state_machine.py` (states + transitions) | Nothing (independent) | No |
| 5 | Unit tests (ia_service, decision_engine, persistence, state_machine) | Tasks 2-4 | No |
| 6 | Final validation (ruff → mypy → pytest) | Task 5 | No |

---

#### Task 1 — `Profile` model + config section

**Files:** modify `shared/models.py` and `config/config.yaml`.

**Objective:** Create the Pydantic `Profile` model representing the user's professional profile, required for the decision engine to evaluate offers against the profile. Its values are loaded from a new `profile` section in `config.yaml`.

**`Profile` model** (add to `shared/models.py`):

```python
class Profile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    technologies: dict[str, int] = Field(default_factory=dict)
    experience_years: int = 0
    languages: dict[str, str] = Field(default_factory=dict)
    preferred_locations: list[str] = Field(default_factory=list)
    preferred_modalities: list[str] = Field(default_factory=list)
    minimum_salary: float | None = None
    seniority: str = ""
    target_companies: list[str] = Field(default_factory=list)
    excluded_companies: list[str] = Field(default_factory=list)
    education_level: str = ""
```

**`profile` section** (add to `config/config.yaml`):

```yaml
profile:
  technologies: {}
  experience_years: 0
  seniority: ""
  languages: {}
  preferred_locations: []
  preferred_modalities: []
  minimum_salary: null
  target_companies: []
  excluded_companies: []
  education_level: ""
```

**Rationale:** Based on DOC-10 (technologies, experience, languages, job preferences) and criteria CE-001 through CE-012 from DOC-03. `Profile` is a value model (not a persistent entity), consistent with DOC-13/13A which does not define it as an entity.

---

#### Task 2 — `shared/ia_service.py`

**File to create:** `shared/ia_service.py`

**Objective:** Implement the AI service with multi-provider support (SRV-002 per DOC-12), capable of routing requests to local or cloud models depending on the purpose.

**Components:**

| Component | Description |
|---|---|
| `load_prompt(prompt_id: str) -> str` | Loads template from `prompts/{category}/{prompt_id}.md`. Raises `ConfigError` if not found. |
| `render_prompt(template: str, context: dict) -> str` | Replaces `{{ variable }}` with values from context. |
| `_route_provider(purpose: str) -> str` | Determines which provider to use based on `config.yaml` → `ia_routing`. |
| `_send_local(prompt: str) -> str` | httpx POST to local Ollama (`http://{host}:{port}/api/generate`). |
| `_send_cloud(prompt: str) -> str` | httpx POST to Ollama Cloud with API Key and endpoint from config. |
| `_validate_response(raw_response: str) -> dict` | JSON parsing, minimum expected structure validation. |
| `analyze(prompt_id: str, context: dict, purpose: str = "evaluation") -> dict` | Orchestrates: load → render → route → send → validate → return dict. |

**Error handling:** `LLMError` with codes ER-LLM-001 (connection), ER-LLM-002 (timeout), ER-LLM-003 (invalid response), ER-LLM-004 (unexpected format).

**Retries:** Use `retry_decorator` from `shared/retry.py` with policy from `config.yaml` → `retries` (global block).

**Routing:** Defined in `config.yaml` → `ia_routing`. Default: evaluation → local, processing → cloud.

**Prompt loader:** Searches in `prompts/{category}/{prompt_id}.md`. Supports subdirectories. Each interaction is logged with Loguru.

---

#### Task 3 — `shared/decision_engine.py`

**File to create:** `shared/decision_engine.py`

**Objective:** Implement the rule-based evaluation engine (SRV-001 per DOC-12).

**Components:**

| Component | Description |
|---|---|
| `load_profile() -> Profile` | Builds a `Profile` from the `profile` section of `config.yaml`. |
| `evaluate(offer: ProcessedOffer, profile: Profile) -> Evaluation` | Evaluates offer vs profile compatibility using weighted criteria. |
| `_calculate_score(offer, profile, weights) -> float` | Calculates 0-100 score by applying configured weights. |
| `_classify(score: float) -> EvaluationResult` | Uses thresholds from config: ≥80 → HIGH, ≥50 → MEDIUM, <50 → LOW. |
| `_decide(result: EvaluationResult) -> EvaluationDecision` | HIGH/MEDIUM → CONTINUE, LOW → DISCARD. |
| `_justify(offer, profile, partial_scores) -> str` | Generates text with score breakdown. |

**Evaluated criteria** (weights from `config.yaml` → `evaluation.weights`):

| Criterion | Configurable weight | Matching |
|---|---|---|
| Experience | 0.30 | `profile.experience_years` vs offer |
| Technology | 0.25 | RapidFuzz between `profile.technologies` and `offer.technologies` |
| Location | 0.15 | RapidFuzz between `profile.preferred_locations` and offer |
| Modality | 0.10 | Exact match against `profile.preferred_modalities` |
| Languages | 0.10 | Level match between `profile.languages` and `offer.languages` |
| Seniority | 0.10 | Match between `profile.seniority` and offer |

**Business rules:**
- Companies in `profile.excluded_companies` → automatic discard (score = 0).
- `profile.minimum_salary` not met → penalized score.
- Justification includes per-criterion breakdown.

---

#### Task 4 — `shared/state_machine.py`

**File to create:** `shared/state_machine.py`

**Objective:** Implement the state machine for the offer lifecycle (based on DOC-03 RTD-001 to RTD-010 and DOC-04 EPD-001 to EPD-010).

**Components:**

| Component | Description |
|---|---|
| `VALID_TRANSITIONS: dict[OfferState, list[OfferState]]` | Map of allowed transitions. |
| `transition(current_state: OfferState, target_state: OfferState) -> OfferState` | Validates and executes transition. Raises `InternalError` (ER-INT-010) if invalid. |
| `possible_transitions(state: OfferState) -> list[OfferState]` | Returns valid destinations from a state. |

**Defined transitions:**

```
DISCOVERED  → PREPARED
PREPARED    → EVALUATED
EVALUATED   → ACCEPTED | DISCARDED
ACCEPTED    → PROCESSED
DISCARDED   → FINALIZED
PROCESSED   → FINALIZED
```

**Validations:** Applies RTD-001 to RTD-010: only defined transitions, no skipping stages, no going back.

---

#### Task 5 — Unit tests

**Files to create:**

| File | Content |
|---|---|
| `tests/test_ia_service.py` | Tests with httpx mock (simulated Ollama response), prompt loading, error if prompt does not exist. |
| `tests/test_decision_engine.py` | Tests with `example_processed_offer` fixture + new `example_profile`. Verify scores and classifications. |
| `tests/test_persistence.py` | CRUD tests with `temp_db_file`: generate_id, read_table, write_row, find_by_id, update. |
| `tests/test_state_machine.py` | Tests for valid and invalid transitions. |

**Additional fixture in `conftest.py`:** `example_profile() -> Profile`

---

#### Task 6 — Final validation

```bash
ruff check .
mypy .
pytest tests/ -v
```

**Criteria:** 0 errors in ruff, 0 errors in mypy, all tests green.

---

## Phase 3. Initial Prompts

1. Create `prompts/initial_evaluation/` — prompt to analyze offer/profile compatibility.
2. Create `prompts/processing/` — prompts for strategic extraction and input generation.
3. Each prompt: file with identifier (PRM-XXX), instructions section, `{{ }}` variables, expected output format.
4. Test each prompt manually with Ollama + a real offer.
5. Adjust and leave approved version 1.

---

## Phase 4. Module 1 — Opportunity Discovery

1. Create `modules/discovery/` with layers (interface, orchestration, services).
2. Implement with Playwright:
   - LinkedIn login/logout (reusable session).
   - Search with filters from config.
   - Result navigation (pagination).
3. Extract raw HTML → pass to `shared/models.py` (BeautifulSoup4 + lxml).
4. Save discovered offers via `shared/persistence.py`.
5. Log events.
6. Error handling: ER-NAV, ER-RED, ER-EXT with retries (Tenacity).
7. Tests:
   - Unit: simulated HTML parsing.
   - Integration: real LinkedIn (tagged `integration`).
8. **Validation:** lint → typecheck → pytest → run against LinkedIn and review results.

---

## Phase 5. Module 2 — Offer Preparation

1. Create `modules/preparation/`.
2. Read raw offers from persistence.
3. Clean fields (spaces, line breaks, residual HTML).
4. Normalize: dates (ISO 8601), salaries (number + currency), locations, modality.
5. Validate required fields, integrity, consistency.
6. Detect duplicates (RapidFuzz on title + company).
7. Assign initial state (`received` / `prepared`).
8. Save prepared version + transformation log.
9. Error handling: ER-VAL, ER-DAT.
10. Tests:
    - Unit with anonymized real offers as fixtures.
    - Edge cases: empty fields, unusual formats, duplicate offers.
11. **Validation.**

---

## Phase 6. Module 3 — Initial Evaluation

1. Create `modules/evaluation/`.
2. Load prepared offers + user's professional profile.
3. Invoke `shared/decision_engine.py`:
   - Apply DOC-03 criteria, configurable weights.
   - Calculate compatibility score.
4. Optional: call LLM (evaluation prompt) for non-deterministic items.
5. Classify: High / Medium / Low.
6. Decide: continue or discard (with justification).
7. Save results + traceability.
8. Error handling: ER-LLM, ER-DAT, ER-INT.
9. Tests:
   - Unit: rules applied to mock profiles.
   - Mocked LLM for deterministic tests.
10. **Validation.**

---

## Phase 7. Module 4 — Deep Processing

1. Create `modules/processing/`.
2. Load accepted offers from evaluation.
3. Invoke LLM with prompts from `prompts/processing/`:
   - Vacancy diagnosis.
   - Strategic extraction (key requirements, culture, differentiators).
   - Application design (strengths to highlight, gaps to mitigate).
   - Input generation (draft cover letter, interview preparation).
4. Validate result consistency (Pydantic).
5. Save products in persistence + `data/output/`.
6. Log full history.
7. Error handling: ER-LLM, ER-INT.
8. Tests:
   - With real prompts + real offer → inspect quality.
   - With mock responses → validate parsing and structures.
9. **Validation.**

---

## Phase 8. Module 5 — Results Management

1. Create `modules/management/`.
2. Implement: full per-offer history, state management, tracking.
3. Reports:
   - Offer summary (processed, discarded, pending).
   - Export to compatible format (`data/output/`).
4. Validate complete traceability (each decision → its justification → log).
5. Error handling: ER-DB, ER-DAT.
6. Tests:
   - Unit: queries, filters, export.
   - Integration: real data → generated report.
7. **Validation.**

---

## Phase 9. MVP Integration

1. Create `scripts/run_mvp.py` — orchestrator that runs all 5 phases in sequence.
2. Test full end-to-end flow with a small set of real offers.
3. Verify: logs, errors, states, persistence, generated files.
4. Fix broken dependencies and adjust sequence.
5. Run pytest regression (lint → typecheck → tests).
6. Review coverage: any functionality from DOC-01 not implemented? Any inconsistent documentation?
7. **Final MVP approval.**

---

## Validation Criteria per Step

Each numbered step in the phases above is considered complete when:

1. The code is written and placed according to DOC-07.
2. `ruff check .` passes with no errors.
3. `mypy .` passes with no errors.
4. `pytest tests/` passes (relevant tests for the step exist and are green).
5. The result is reviewed and approved before moving to the next step.

---

## References

| Document | Purpose |
|----------|---------|
| DOC-01 | Functional requirements |
| DOC-03 | Decision model |
| DOC-04 | Data flow |
| DOC-05 | Project standards |
| DOC-06 | Error handling |
| DOC-07 | Folder architecture |
| DOC-08 | Scope and objectives |
| DOC-09 | Source research (LinkedIn) |
| DOC-11 | Technology stack |
| DOC-12 | General system architecture |
| DOC-13 | Data model |
| Annex 5A | Prefix catalog |
| Annex 5B | Official technical standards |
| Annex 9A | LinkedIn strategic decisions |
