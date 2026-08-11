# Decision Log

Unified, cumulative record of approved decisions affecting the job search automation. Decisions remain in effect unless superseded. This log is the authoritative reference for approved deviations between official specifications and implementation.

Format: `D<n>` — module/business decisions; `C<n>` — prompt/design alignment decisions; `PMD-<n>` — implementation deviations; `DE-LI-<n>` — LinkedIn strategic decisions (consolidated from DOC-Appendix 9A, archived 2026-08-11).

---

## Module and business decisions

### D1. `fuentes.activa` is a catalog attribute, ignored at runtime

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** The Source entity defines `active`, which could be interpreted as a runtime filter.
- **Decision:** `active` remains in the data model as a manually administered catalog attribute. Discovery does **not** filter sources by it at runtime.
- **Impact:** Source filtering relies on a complete and consistent source record (ficha) plus configuration content; `active=false` neither excludes nor includes a source.

### D2. Discovery traceability tables in `job_search.db`

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** Module 1 requires run-level traceability, session audit, and concurrency control.
- **Decision:** `corridas`, `sesiones`, `eventos`, and `bloqueo` are implemented as tables in the same SQLite file (`job_search.db`), alongside `ofertas`, `fuentes`, `empresas`, `ubicaciones`, `secuencia_ids`.
- **Impact:** Every module 1 record anchors to `run_id` (RN-01). Prefixed sequential IDs: `COR-`, `SES-`, `EVT-`, `BLO-`.

### D3. Session record created only after successful entry; MVP keeps essential audit fields

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** The technical sheet mentions additional audit fields (e.g., `conteo_primera_pagina`, `hay_mas_paginas`, `coherencia`, `estado_auditoria`).
- **Decision:** A session record is created only after successful entry; failed attempts are reported as events, not sessions. The MVP limits the session schema to essential fields: `session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`.
- **Impact:** Session audit is lightweight; extended audit fields remain available in the technical sheet for future revisions.

### D4. Capture registration: dedup by `id_externo_url`, FK-free `fuente_id`, null catalogs

- **Date:** 2026-08-09 (extended 2026-08-10 with run-state vocabulary)
- **Status:** In effect
- **Context:** Sub-phase 4.4 capture/registration revealed that full normalized references (FK to `fuentes`/`empresas`/`ubicaciones`) are not resolvable at MVP capture time.
- **Decision:**
  - Registration deduplicates by `id_externo_url` via `upsert_oferta`; an existing row only refreshes `timestamp_ultima_verificacion` and keeps its `id`; a missing row is inserted. Advanced two-layer dedup (strict + fuzzy) belongs to Module 2.
  - `fuente_id` stores the raw `source_id` string without FK constraint.
  - `empresa_id` and `ubicacion_id` are `NULL` in the MVP; raw adapter strings are kept in `empresa_nombre` and `ubicacion_nombre`.
  - Run-state vocabulary (user-specified, reconciles session 9 pending item): `en_ejecucion`, `completada`, `sin_fuentes`, `abortada` — deviations vs ficha/DOC-13A wording documented here.
- **Impact:** `ofertas` schema is FK-free for `fuente_id`/`empresa_id`/`ubicacion_id`; `corridas.estado` uses the vocabulary above; run-level `total_ofertas` counts only newly registered offers (re-seen offers become updates).

### D5. Session schema aligned with the generic writer

- **Date:** 2026-08-10
- **Status:** In effect
- **Context:** Session audit insert failed because the generic writer requires an `id` column.
- **Decision:** `sesiones` gains `id` PK (+ creation dates); migration copies legacy rows with `id = session_id`; session audit passes the explicit `id`. Migration is idempotent.
- **Impact:** Session audit writes through the generic writer; legacy rows survive migration.

### D6. Happy-path capture writes `ofertas_registradas`

- **Date:** 2026-08-10
- **Status:** In effect
- **Context:** Closure metrics showed 0 successes on the happy path because capture success wrote no event.
- **Decision:** On successful capture registration, write the `ofertas_registradas` success event so closure metrics reflect the run. Degraded/partial lote events remain unchanged.
- **Impact:** Run closure reports truthful `total_sucesos`/`fuentes_procesadas` (validated on COR-1957).

---

## Prompt/design alignment decisions

### C2. Detailed Evaluation entity uses Spanish attribute names

- **Date:** 2026-07-30
- **Status:** In effect
- **Context:** Prompts PRM-002..005 originally produced English/mixed outcomes.
- **Decision:** Detailed Evaluation entity fields are Spanish (e.g., `resultado_organizacional`, `logica_xyz`, `insumos_carta_presentacion`); prompts redesigned to v2 producing exactly those fields; chained execution; `ProcessingResult` → `EvaluacionDetallada`. Catalogs Overqualification Risk and Final Recommendation use Spanish values (`Bajo/Medio/Alto`, `Aplicar/Aplicar con reservas/No aplicar`).
- **Impact:** DOC-13A §2.7 and §3.15–3.16 reflect this; prompts emit Spanish output.

### C5. Module 1 registers offers with `estado='discovered'`

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** Offer state machine has 7 states; discovery is the entry point.
- **Decision:** Module 1 inserts discovered offers with `estado='discovered'` (default assignment, no normalization/dedup beyond D4 upsert; those belong to Module 2).
- **Impact:** Every newly registered offer enters the pipeline in `discovered`.

---

## Implementation deviations

### PMD-020. Processed Offer attribute deviations

- **Date:** 2026-07-30
- **Status:** In effect
- **Context:** Document 13A Processed Offer spec vs `shared/models.py`.
- **Decision:** `requisitos`, `tecnologias`, and `idiomas` are implemented as JSON lists instead of Long Text; `summary`, `technical_skills`, and `soft_skills` are not implemented in `shared/models.py`; `salary_range` implemented as `salario_min`/`salario_max`/`moneda`; `normalized_position` → `clean_title`; `processed_description` → `clean_description`.
- **Impact:** DOC-13A §2.5 and §5.5.5 record these deviations.

### PMD-021. MVP persistence scope

- **Date:** 2026-07-30 / 2026-08-07
- **Status:** In effect
- **Context:** The full logical model includes 16 entities; the MVP cannot persist all.
- **Decision:** `job_search.db` persists only `secuencia_ids`, `fuentes`, `empresas`, `ubicaciones`, `ofertas` plus module 1 tables (`eventos`, `sesiones`, `corridas`, `bloqueo`). Remaining entities (Processed Offer, Evaluations, Documents, Application, Decision, Configuration, Catalog) are deferred to later modules. Catalog values are free text in the MVP; only Offer Statuses is enforced via `shared/state_machine.py`.
- **Impact:** DOC-13A §1 (scope note) and §3 (deferral note) formalize this.

---

## LinkedIn strategic decisions (consolidated from DOC-Appendix 9A)

Source: DOC-APPENDIX 9A — archived 2026-08-11; content consolidated here unchanged except where annotated. Full research justification: DOC-09, archived 2026-08-11.

| ID | Decision (summary) |
|---|---|
| DE-LI-001 | LinkedIn is the only official MVP platform; other platforms evaluated later with the same research process. |
| DE-LI-002 | LinkedIn approved as official opportunity source; extraction is used solely to retrieve offers; relevance evaluation is exclusively the automation's. |
| DE-LI-003 | Access through an authenticated session; official LinkedIn APIs are not used; authentication is part of normal operation. |
| DE-LI-004 | Controlled extraction of only the information required by subsequent stages. |
| DE-LI-005 | Technical/legal restrictions are project requirements; conservative interaction strategy; account protection over speed/volume. |
| DE-LI-006 | Minimize operational risk via limited, controlled, legitimate-user-like interaction; account protection is an operational principle. |
| DE-LI-007 | Main risk is account restriction by automated-behavior detection; risk mitigation is a design criterion. |
| DE-LI-008 | Moderate query frequency balancing coverage, freshness, and safety; never continuous runs or excessively short intervals. |
| DE-LI-009 | Query strategy maximizes compatible opportunities via LinkedIn filters; prioritization never delegated to LinkedIn's recommendation algorithm. |
| DE-LI-010 | Module 1 implementation criteria per DOC-09 §6: verifiable entry criterion, config-defined filter mapping, capture policies, `bloqueo_plataforma` (Group A, no retry), `sesion_expirada` with controlled re-entry. **Updated 2026-08-10:** entry criterion for authenticated sources is HTML polling for `voyager` on the feed (global-nav no longer renders); direct login URL flow; selectors use prefix match + `:visible` with Enter submit and click fallback; per-page parsing variants resolved by exclusivity. |

---

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-11 | Initial unified log: consolidated D1–D6, C2, C5, PMD-020/021, DE-LI-001..010 (9A archived). |