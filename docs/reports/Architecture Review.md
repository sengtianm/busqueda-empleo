# Architecture Review — Job Search Automation

> **Date:** 2026-07-30
>
> **Type:** Critical independent architecture review
>
> **Scope:** Full project — official documentation (DOC-00 to DOC-13, Annexes 5A/5B/5C/9A), MVP Execution Plan, execution reports, `shared/` implementation, tests, prompts, scripts, configuration, and git history.
>
> **Evaluated against:** Free, scalable, maintainable, modular, simple, flexible, and long-term evolvable principles. No functional code is required; the design itself is under review.

---

## Findings

### C1 · CRITICAL — Triple definition of the offer lifecycle

**Status:** ✅ **Completed** — 7 states unified as single source of truth; no pending work.

- **Description:** There are three incompatible official definitions of offer states: DOC-01 (LC-01..07 + catalog EST-001..010/999 with 11 statuses, including EST-999 Error and EST-008 Pending Decision), DOC-13A ("Offer Statuses" catalog with 12 values: Initial Evaluation, Approved for Detailed Evaluation, Documentation Generated, Applied, Closed, etc.), and the implementation (`shared/state_machine.py` with 7 states: discovered/prepared/evaluated/accepted/discarded/processed/finalized, with no error state, no pending-decision state, no classified state, and no resources-generated state).
- **Impact:** Modules 3-5 (evaluation, processing, management) will be built on a state machine that cannot represent the documented traceability: reprocessing after errors, user decisions (DU-004/DU-005), and prioritization (LC-04). This violates the AGENTS.md rule ("if documentation contains a contradiction, stop implementation and request a decision").
- **Recommendation:** Select a single source of truth (suggested: the EST catalog of DOC-01, the most complete and referenced), update DOC-13A to match it, and extend `state_machine.py` with the missing states (at minimum: error/retry) before implementing Module 3.
- **Justification:** The state trace is the central control mechanism (DOC-13 §10, DOC-04 §9, DFP-015); a contradictory catalog will invalidate any future temporal integrity validation.

### C2 · CRITICAL — Processing prompts misaligned with the Detailed Evaluation entity

**Status:** ✅ **Completed** — Prompts v2 aligned with the entity and retested against the real cloud model; no pending work.

- **Description:** DOC-13A defines Detailed Evaluation with `organizational_result`, `organizational_problem`, `profile_matches`, `xyz_logic`, `value_hypothesis`, `technical/functional/strategic_fit`, `overqualification_risk`, `final_recommendation`. The approved prompts PRM-002..005 generate different structures (`diagnostic`, `key_requirements`, `skills`, `strategic_extraction`, `application_design`, `cover_letter_draft`, etc.), and the `ProcessingResult` model reflects the prompts, not the official entity. The concepts of "fit score" and "final recommendation" do not exist anywhere in the implementation.
- **Impact:** When Module 4 is implemented (Phase 7), it will be impossible to persist the results without redefining either the official entity or the approved prompts; this blocks the entire processing flow.
- **Recommendation:** Before Phase 7, formally decide whether Detailed Evaluation is redefined to absorb the PRM-002/003 outputs (recommended) or whether the prompts are adjusted to the existing entity; update DOC-13A and the `ProcessingResult` model accordingly.
- **Justification:** DOC-13A appears to reflect an earlier cover-letter methodology (XYZ logic, value hypothesis); the current prompts have replaced it without updating the data model.

### C3 · HIGH — DOC-11 outdated against the cloud-only AI decision

**Status:** ✅ **Completed** — DOC-11 formalized; ⏳ **Future:** monitor free-plan limits and verify the local fallback works in practice.

- **Description:** DOC-11 §9.3/9.7.1/9.10 documents a hybrid strategy (local `qwen3.5:4b` for evaluation, mandatory offline operation in Module 3) and a routing section named `ia_routing`. The reality is `ai_routing: evaluation=cloud, processing=cloud` with `gemma4:31b-cloud` through a local proxy (a decision recorded only in the Phase 3 report). `scripts/README-tests.md` still instructs testing PRM-001 with the local model.
- **Impact:** The official documentation contradicts the current implementation; a future maintainer will not know which is the source of truth. In addition, the free Ollama Cloud plan as the only route is an operational risk (usage limits, availability, term changes) for a project whose principle is technological independence (PST-014).
- **Recommendation:** Update DOC-11 (strategy, `ai_routing`, remove or replace the offline restriction with a configurable fallback), align `scripts/README-tests.md`, and monitor the free plan limits with a contingency plan (configurable local fallback).
- **Justification:** RAR-014 requires alignment with Documents 0-12; keeping the document outdated invalidates the architectural acceptance mechanism (CA-001..013).

### A1 · HIGH — Gap between the official data model and the implemented persistence

**Status:** ✅ **Completed** — Scope cut formalized; ⏳ **Future:** incremental table migration per module (Module 3 → Modules 4-5).

- **Description:** DOC-13A defines 13 entities; DOC-11 §10.6 defines 7 tables; the implementation has 4 (`fuentes`, `empresas`, `ubicaciones`, `ofertas` + `secuencia_ids`). Tables for ProcessedOffer, Evaluation, and ProcessingResult are missing, as is the entire trace layer (Event, Decision) — entities that DOC-04/DFP-002 and DOC-12/ROA-003 declare mandatory. The commit "dejar solo tablas del Modulo 1 en la BD" shows this was a scoping decision, but it has not been formalized in any document.
- **Impact:** Complete traceability (Event/Decision) is not implementable today; each future module will require schema expansion with a risk of accumulating undocumented deviations.
- **Recommendation:** Formally document the scope cut (MVP scope decision), plan incremental migration per module (`ofertas_procesadas` + `evaluaciones` in Module 3, results + documents + events in Modules 4-5), and prioritize a minimal events table for transition logging.
- **Justification:** PMD-008/010 and RP-005 are mandatory; without them the system cannot be audited.

### A2 · HIGH — Personal data committed to git

**Status:** ✅ **Completed** — Untracked + history verified (DB copy empty, no personal data); no pending work.

- **Description:** `data/job_search.db` is tracked in git (not in `.gitignore`; confirmed via `git ls-files`). It will contain the professional profile, offers, evaluations, and cover letter drafts.
- **Impact:** Risk of exposing personal information if the repository is made public or shared; violates RSA-003/005 (isolation of confidential information).
- **Recommendation:** Add `data/*.db` (and `data/backup/*`) to `.gitignore`, run `git rm --cached data/job_search.db`, and verify that the current database contains no sensitive data in history.
- **Justification:** The security principles (DOC-12 §14) are mandatory (RSA-005).

### A3 · HIGH — Mixed languages in code and schema

**Status:** ✅ **Completed** — Language convention decided (English code/docs; Spanish data layer) and applied; no pending work.

- **Description:** AGENTS.md requires English for all code and Spanish only for natural-language data. The reality: Pydantic fields in Spanish (`nombre`, `titulo`, `descripcion_original`, `version_modelo`) mixed with English (`creation_date`, `id`), SQL tables in Spanish (`fuentes`, `ofertas`), while DOC-13A defines attributes in English (`name`, `title`) and DOC-11 defines tables in Spanish. The commit "full project translation to English + directory restructure" was left incomplete.
- **Impact:** Hinders maintenance and layer mapping; any new contributor will not know which convention to follow.
- **Recommendation:** Decide on a single norm (recommended: identifiers/code in English, natural content in Spanish), migrate models and schema, and update DOC-11 accordingly.
- **Justification:** PA-015 (structural consistency) and the official project conventions.

### A4 · HIGH — Duplicated scripts and hardcoded prompt metadata

**Status:** ✅ **Completed** — Duplicate removed; ⬜ **Optional (future):** move the prompt catalog to a metadata file (RAI-004).

- **Description:** `scripts/probar_prompt.py` and `scripts/test_prompt.py` are almost identical duplicates (163 lines each; they differ only in identifier names). The PRM-001..005 → path/purpose/variables mapping is duplicated in both scripts.
- **Impact:** Double maintenance; any change to prompts or routing requires editing two files; risk of divergence.
- **Recommendation:** Keep a single script (`probar_prompt.py`) and remove the other; consider moving the prompt catalog to a metadata file (config) to comply with RAI-004 (centralized instruction management).
- **Justification:** RCM-004 prohibits duplicating existing logic.

### M1 · MEDIUM — Official catalogs not implemented

**Status:** ✅ **Completed** — Deferral formalized; ⏳ **Future:** Catalog entity adoption in Modules 2-3.

- **Description:** DOC-13A defines Catalog as a central entity with foreign keys (modality, sector, type, statuses, etc.); the implementation uses free text in models and tables.
- **Impact:** Risk of inconsistent values (synonyms, spelling) as volume grows; deviation from the official model without a formal decision.
- **Recommendation:** Either defer explicitly with a documented decision or introduce enum/Literal (Pydantic) validation as a bridge until the Catalog table is defined.
- **Justification:** PMD-004/005 (normalization, no duplication).

### M2 · MEDIUM — Empty default profile produces silent degenerate evaluations

**Status:** ✅ **Completed** — Warning implemented in `load_profile()` + test; no pending work.

- **Description:** The `profile` section in `config.yaml` is empty (`tecnologias: {}`, `experience_years: 0`, `seniority: ""`). With that profile, the decision engine will score 0 and discard all offers without warning.
- **Impact:** Confusing and useless first execution for the user.
- **Recommendation:** Validate profile completeness on load (warning/error in `load_profile` or configuration validation, RCF-003) and document it as an initial configuration requirement.
- **Justification:** RCF-003 requires configuration validation before use.

### M3 · MEDIUM — Minor naming inconsistencies

**Status:** ✅ **Completed** — Real names officialized in DOC-11/DOC-13A; no pending work.

- **Description:** `job_search.db` (config) vs `busqueda_empleo.db` (DOC-11 §10.8); `ai_routing` (config) vs `ia_routing` (DOC-11 §9.5 and plan); `version_modelo` (model) vs `model_version` (DOC-13A); `region` (model) vs `state_province` (DOC-13A).
- **Impact:** Friction when searching documentation; risk of configuration errors.
- **Recommendation:** Make the actual names official and correct DOC-11/13A.
- **Justification:** Documentation consistency (PST-006).

### M4 · MEDIUM — MVP plan references non-existent codes

**Status:** ✅ **Completed** — Plan corrected to reference the EST catalog; no pending work.

- **Description:** Phase 2, Task 4 cites "DOC-03 RTD-001..RTD-010 and DOC-04 EPD-001..EPD-010" — codes that do not exist (DOC-04 defines DS-xxx); Phase 5 assigns a `received` state that is not an official offer status (it is a data state, DS-001).
- **Impact:** Reinforces C1: the state machine was built on incorrect references.
- **Recommendation:** Correct the plan to reference the EST catalog of DOC-01 as the only source.
- **Justification:** Plans are working documents, but they must point to the correct official documentation.

### B1 · LOW — Undocumented attribute deviations

**Status:** ✅ **Completed** — Deviation recorded in DOC-13A §2.6; no pending work.

- **Description:** `requisitos`/`tecnologias`/`idiomas` as JSON lists (a real improvement) vs `Long Text` in DOC-13A; ProcessedOffer lacks the `technical_skills`/`soft_skills`/`summary` fields of DOC-13A.
- **Impact:** Minimal; but PMD-020 requires every deviation to be recorded.
- **Recommendation:** Annotate the deviation in DOC-13A.
- **Justification:** PMD-020.

### B2 · LOW — Required artifacts not created

**Status:** ✅ **Completed** — Versioning, Data Dictionary (§5.5) and ERD (§6.6) created; ⬜ **Pending:** formal Architect review.

- **Description:** DOC-13A requires a Data Dictionary, an ERD, and versioning (v1.0 "Pending"); none exist. Phase reports are written in Spanish while the convention requires English.
- **Impact:** Low today; will grow with module implementation.
- **Recommendation:** Create the versioning and prioritize the dictionary before Module 3.
- **Justification:** DOC-13A §5-7.

---

## Verified strengths

- Three-level architecture (DOC-12) is solid and consistent with AGENTS.md; the real folder structure respects DOC-07, and the module layers are correctly empty.
- Shared services quality: Pydantic v2, typed error hierarchy with codes (ER-*), tenacity, loguru, isolated fixtures; 37/37 tests green, ruff and mypy at 0 errors.
- Free, mature stack without frameworks; SQLite and Playwright decisions well justified (PST methodology of DOC-11).
- Correct configuration/code and prompts/code separation; `.env` well managed (ignored, no history).
- Branch workflow, reports, and Session History working (active branch: `modulo-1`).

---

## Final scores (1-10)

| Category | Score |
|---|---|
| Documentation consistency (docs↔docs, docs↔code) | 4 |
| General architecture design (DOC-12) | 9 |
| Technology stack | 9 |
| Data model (design) | 7 |
| AI strategy | 6 |
| Implementation quality (shared/) | 8 |
| Testability | 8 |
| Scalability/extensibility | 8 |
| Long-term sustainability | 6 |

## Verdict

**YES, I would continue with this architecture.** The fundamental design (layers, modules, stack, shared services) is solid, mature, and well grounded; the issues found are about **documentation consistency and decisions pending formalization** (offer states, prompt↔entity alignment, AI strategy, code language, database cleanup in git), not structural design. This is a small, personal project in an early phase: fixing these today costs hours; letting them accumulate will cost redesigns in modules 3-5.

---

## Resolution (2026-07-30)

Decisions adopted to close each finding:

| Finding | Status | Resolution |
|---|---|---|
| C1 | ✅ Completed | **Keep the 7 implemented states** (`shared/state_machine.py`): discovered, prepared, evaluated, accepted, discarded, processed, finalized. The EST catalog of DOC-01 §13 and DOC-13A §3.1 were rewritten to match the implementation (single source of truth). LC-04..07 of DOC-01 §12 aligned. |
| C2 | ✅ Completed | **Resolved 2026-07-30 — prompts adjusted to the entity.** PRM-002..005 redesigned (v2) to produce exactly the 18 attributes of the Detailed Evaluation entity (renamed to Spanish: `resultado_organizacional`, `problema_organizacional`, `perfil_profesional_requerido`, `coincidencias_perfil`, `logica_xyz`, `hipotesis_valor`, `informacion_descartada`, `ajuste_tecnico`/`ajuste_funcional`/`ajuste_estrategico` + justifications, `riesgo_sobrecalificacion` + justification, `recomendacion_final` + justification, `insumos_carta_presentacion`). Chained execution: PRM-002 → PRM-003 → PRM-004 → PRM-005. `ProcessingResult` replaced by `EvaluacionDetallada` (`shared/models.py`). Cover letter draft and interview preparation are deferred to the document generation phase (Generated Document entity). Prompts pending manual retest against the cloud model (requires API key). **Bonus fix:** the 5 prompts documented their variables as `{{ offer }}`/`{{ profile }}` while the tester injects `oferta`/`perfil` — the offer and profile data were never injected into the rendered prompt (pre-existing bug); placeholders corrected in all 5 prompts. **Retest completed 2026-07-30** against `gemma4:31b-cloud` (see `Prompt Retest Report.md`): 5/5 valid JSON with the expected fields, variable injection confirmed, and a new fix — mandatory Spanish output instruction added to the 5 prompts (PRM-001..004 generated English content). |
| C3 | ✅ Completed | **Cloud-primary strategy formalized.** DOC-11 §9.3/9.5/9.7.1/9.10 updated: `ai_routing: evaluation=cloud, processing=cloud`, local model as optional fallback, offline restriction replaced by configurable fallback. `scripts/README-tests.md` aligned. |
| A1 | ✅ Completed | **Scope cut formalized** in DOC-13A §1 note: MVP persists `secuencia_ids`, `fuentes`, `empresas`, `ubicaciones`, `ofertas`. Remaining entities are deferred per module (`ofertas_procesadas` + `evaluaciones` in Module 3, results + documents + events in Modules 4-5). |
| A2 | ✅ Completed | `data/*.db` added to `.gitignore`; `data/job_search.db` untracked via `git rm --cached` (file kept locally). **History verified 2026-07-30:** the copy of `job_search.db` committed in `84c662f` was extracted and inspected — all tables are empty (0 rows), no personal data in git history. |
| A3 | ✅ Completed | **User decision:** English for all code, docs, config, and prompts; **Spanish for everything data-related**: the SQLite schema, `shared/models.py` + `shared/persistence.py`, profile/evaluation criteria data in `config.yaml`, and test fixture data. Translation of `shared/` (except models/persistence), `scripts/prompt_tester.py`, and `tests/` completed; AGENTS.md conventions updated. |
| A4 | ✅ Completed | Duplicate removed: `scripts/test_prompt.py` deleted; `scripts/probar_prompt.py` → `scripts/prompt_tester.py`; `tests/fixtures/contextos_prompt.yaml` → `prompt_contexts.yaml`; `README-tests.md` updated. |
| M1 | ✅ Completed | **Deferral formalized** in DOC-13A §3: Catalog entity not implemented in MVP (free text in models); adoption deferred to Modules 2-3. Only Offer Statuses enforced in MVP via `state_machine.py`. |
| M2 | ✅ Completed | **Implemented:** `load_profile()` in `shared/decision_engine.py` warns via Loguru when the profile is incomplete; test added (`test_load_profile_warns_if_incomplete`). |
| M3 | ✅ Completed | Names made official: `ai_routing`, `job_search.db`, `version_modelo`, `region` in DOC-11/DOC-13A (real names in code are the source of truth). |
| M4 | ✅ Completed | MVP Execution Plan corrected: Task 4 references the EST catalog (DOC-01 §13) instead of non-existent RTD/EPD codes; Phase 5 initial state uses `discovered → prepared` (EST-001 → EST-002) instead of `received`. |
| B1 | ✅ Completed | **Recorded** in DOC-13A §2.6 (Processed Offer): `requisitos`/`tecnologias`/`idiomas` as JSON lists; `summary`/`technical_skills`/`soft_skills` not implemented. |
| B2 | ✅ Completed | **Completed 2026-07-30.** DOC-13A version history created (v1.0, v1.1, v1.2). **Official Data Dictionary (§5.5) created for the 13 entities** with sensitivity classification per DOC-12 §14.2; **ERD (§6.6) created in Mermaid + ASCII** with cardinality legend. Historical Phase 2/3 reports keep their original language (historical record). |

---

## Outstanding work (as of 2026-07-30)

> Status legend: ✅ Completed — ⏳ In progress — ⬜ Pending / future.

| Finding | Pending item | When |
|---|---|---|
| B2 | Formal Architect review of PRM-001..005 (v2), Data Dictionary and ERD (DOC-13A v1.2) | Before Module 3 |
| M1 | Adopt the Catalog entity (replace free text with FK-referenced values) | Modules 2-3 |
| A1 | Incremental schema migration: `ofertas_procesadas` + `evaluaciones` tables (Module 3); results, documents, events tables (Modules 4-5) | Module 3 → Modules 4-5 |
| C3 | Verify the local fallback (`qwen3.5:4b`) works in practice; monitor Ollama Cloud free-plan limits | Before relying on fallback; ongoing |
| A4 | (Optional) Move the prompt catalog (PRM-001..005 → path/purpose/variables) to a metadata file per RAI-004 | Any time |
| — | Keep documentation consistency score (4/10) improving: any code change must keep DOC-01/11/13A synced | Ongoing |
