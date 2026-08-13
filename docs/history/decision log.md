# Decision Log

Unified, cumulative record of approved decisions affecting the job search automation. Decisions remain in effect unless superseded. This log is the authoritative reference for approved deviations between official specifications and implementation.

Format: `D<n>` — module/business decisions; `C<n>` — prompt/design alignment decisions; `PMD-<n>` — implementation deviations; `DE-LI-<n>` — LinkedIn strategic decisions (consolidated from DOC-Appendix 9A, archived 2026-08-11).

---

## Module and business decisions

### D1. `fuentes.activa` is a catalog attribute, ignored at runtime

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** The Source entity defines `activa`, which could be interpreted as a runtime filter.
- **Decision:** `activa` remains in the data model as a manually administered catalog attribute. Discovery does **not** filter sources by it at runtime.
- **Impact:** Source filtering relies on a complete and consistent source record (ficha) plus configuration content; `activa=false` neither excludes nor includes a source.

### D2. Discovery traceability tables in `job_search.db`

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** Module 1 requires run-level traceability, session audit, and concurrency control.
- **Decision:** `corridas`, `sesiones`, `eventos`, and `bloqueo` are implemented as tables in the same SQLite file (`job_search.db`), alongside `ofertas`, `fuentes`, `empresas`, `ubicaciones`, `secuencia_ids`.
- **Impact:** Every module 1 record anchors to `id_corrida` (RN-01). Prefixed sequential IDs: `COR-`, `SES-`, `EVT-`, `BLO-`.

### D3. Session record created only after successful entry; MVP keeps essential audit fields

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** The technical sheet mentions additional audit fields (e.g., `conteo_primera_pagina`, `hay_mas_paginas`, `coherencia`, `estado_auditoria`).
- **Decision:** A session record is created only after successful entry; failed attempts are reported as events, not sessions. The MVP limits the session schema to essential fields: `id_sesion`, `id_corrida`, `fuente_id`, `indice_set`, `marca_temporal`, `total_declarado`, `conteo`, `estado`.
- **Impact:** Session audit is lightweight; extended audit fields remain available in the technical sheet for future revisions.

### D4. Capture registration: dedup by `id_externo`, FK-free `fuente_id`, null catalogs

- **Date:** 2026-08-09 (extended 2026-08-10 with run-state vocabulary)
- **Status:** In effect
- **Context:** Sub-phase 4.4 capture/registration revealed that full normalized references (FK to `fuentes`/`empresas`/`ubicaciones`) are not resolvable at MVP capture time.
- **Decision:**
  - Registration deduplicates by `id_externo` via `upsert_oferta`; an existing row only refreshes `fecha_ultima_verificacion` and keeps its `id`; a missing row is inserted. Advanced two-layer dedup (strict + fuzzy) belongs to Module 2.
  - `fuente_id` stores the raw `fuente_id` string without FK constraint.
  - `empresa_id` and `ubicacion_id` are `NULL` in the MVP; raw adapter strings are kept in `empresa_nombre` and `ubicacion_nombre`.
  - Run-state vocabulary (user-specified, reconciles session 9 pending item): `en_ejecucion`, `completada`, `sin_fuentes`, `abortada` — deviations vs ficha/DOC-13A wording documented here.
- **Impact:** `ofertas` schema is FK-free for `fuente_id`/`empresa_id`/`ubicacion_id`; `corridas.estado` uses the vocabulary above; run-level `total_ofertas` counts only newly registered offers (re-seen offers become updates).

### D5. Session schema aligned with the generic writer

- **Date:** 2026-08-10
- **Status:** In effect
- **Context:** Session audit insert failed because the generic writer requires an `id` column.
- **Decision:** `sesiones` gains `id` PK (+ creation dates); migration copies legacy rows with `id = id_sesion`; session audit passes the explicit `id`. Migration is idempotent.
- **Impact:** Session audit writes through the generic writer; legacy rows survive migration.

### D6. Happy-path capture writes `ofertas_registradas`

- **Date:** 2026-08-10
- **Status:** In effect
- **Context:** Closure metrics showed 0 successes on the happy path because capture success wrote no event.
- **Decision:** On successful capture registration, write the `ofertas_registradas` success event so closure metrics reflect the run. Degraded/partial lote events remain unchanged.
- **Impact:** Run closure reports truthful `total_sucesos`/`fuentes_procesadas` (validated on COR-1957).

### D7. Spanish naming catalog for persistence fields, config keys, and discovery identifiers

- **Date:** 2026-08-11
- **Status:** In effect
- **Context:** DB columns, config keys, models, and Discovery code mixed English and Spanish identifiers (e.g., `run_id`, `source_id`, `session_id`, `set_indice`, `id_externo_url`, `creation_date`, `last_edit_date`, `url_base`, `normalized_name`, `experience_years`).
- **Decision:** Approved word-boundary English→Spanish catalog applied mechanically to `shared/models.py`, `shared/persistence.py`, `shared/state_machine.py`, `shared/retry.py`, `shared/decision_engine.py`, `config/config.yaml`, `modules/discovery/**`, and tests. Main mappings: `run_id`→`id_corrida`, `source_id`→`fuente_id`, `session_id`→`id_sesion`, `set_indice`→`indice_set`, `offer_id`→`id_oferta`, `processed_offer_id`→`id_oferta_procesada`, `id_externo_url`→`id_externo`, `timestamp_ultima_verificacion`→`fecha_ultima_verificacion`, `creation_date`→`fecha_creacion`, `last_edit_date`→`fecha_ultima_edicion`, `url_base`→`enlace_base`, `normalized_name`→`nombre_normalizado`, `clean_title`→`titulo_limpio`, `clean_description`→`descripcion_limpia`, `processing_date`→`fecha_procesamiento`, `approval_threshold`→`umbral_aprobacion`, `evaluated_criteria`→`criterios_evaluados`, `evaluation_date`→`fecha_evaluacion`, `experience_years`→`anos_experiencia`, `discovery_date`→`fecha_descubrimiento`, `source_identifier`→`identificador_origen`, `url`→`enlace`, `timestamp`→`marca_temporal`. Exceptions: `shared/errors.py` keeps English attribute names (`run_id`, `source_id`, `session_id`, `set_indice`, `offer_id`, `source_module`, `timestamp`) — error-context fields, not DB columns; `linkedin`→`perfil_linkedin` and `size`→`tamano` applied manually only (unsafe for blind replacement).
- **Impact:** `job_search.db` migrated via `_migrar_espanol_total` in `shared/persistence.py` (rebuild per table with explicit old→new column mapping, `CASE` translation of `ofertas.estado`, `sesiones.id` backfill, idempotent, runs before legacy migrations); data preserved (7 offers); backup `data/backup/job_search_pre_espanol_20260811_073632.db`. DOC-13A, module 1 ficha técnica, and MVP plan updated to the Spanish catalog. Identifier references in prior decisions (D1–D6, C5, PMD-020) updated here to the current naming.

### D8. Spanish vocabulary for offer states and retry timeout codes

- **Date:** 2026-08-11
- **Status:** In effect
- **Context:** Offer states used English values (`discovered`…`finalized`); retry timeout codes used English (`timeout_ingreso`, `timeout_consulta`, `timeout_captura`).
- **Decision:** `OfferState` members and DB values are now Spanish lowercase: `descubierta`, `preparada`, `evaluada`, `aceptada`, `descartada`, `procesada`, `finalizada` (supersedes the C5 `discovered` value); timeout codes renamed to `tiempo_agotado_ingreso`, `tiempo_agotado_consulta`, `tiempo_agotado_captura` in retry policies and tests.
- **Impact:** `ofertas.estado` CHECK constraint in Spanish; existing rows migrated via `CASE`; DOC-13A §3.1 catalog values in Spanish; ficha técnica error tables updated.

### D9. Entry criterion is the `MainFeed` string in visible HTML

- **Date:** 2026-08-12 (verified live on the 2026-08-12 session; implementation had already switched)
- **Status:** In effect (supersedes the `voyager` polling wording of DE-LI-010)
- **Context:** `config/config.yaml` defines `criterio_exito: "MainFeed"` and the adapter checks the criterion as a plain text substring of the page HTML. The older `voyager` feed criterion (DE-LI-010, 2026-08-10) no longer matches the live page. Note: "MainFeed" also appears in login-page bundles, so the criterion is evaluated only after the username field is detached (successful login flow).
- **Decision:** Keep `criterio_exito: "MainFeed"` as the official entry criterion; adapter checks `ficha.criterio_exito in html` on the authenticated feed.
- **Impact:** DE-LI-010 updated; criterion stays config-driven (config `criterio_exito`), so a future platform change only adjusts the config value.

### D10. Blocked-detection heuristics only on visible content

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** A false positive occurred: `_revisar_bloqueo_html` flagged login pages as blocked because "challenge"/"authwall" appeared inside inline scripts, and the global-nav criterion made feeds fail.
- **Decision:** The detector analyzes only visible content signals (`show captcha`, `complete the captcha`, `verify your identity`, `verifica tu identidad`, `verificacion de identidad`, `introduce el codigo`, `challenge-login`, `id="challenge"`, `no soy un robot`, `i'm not a robot`, authwall only in visible content); script/JSON payloads are ignored.
- **Impact:** 5 regression tests added; blocked detection triggers only on real visible signals.

### D11. List-based capture without detail navigation

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Detail-per-offer navigation was slow (double page load via `/jobs/search` → `/jobs/search-results` redirect) and unnecessary at capture time: the list card already carries title + canonical link (`id_externo`); description enrichment belongs to the Preparation module.
- **Decision:** `capture_batch` traverses the search-results list via `?start=N` without opening each offer; ends when the pagination button ("Siguiente"/"Página N" in Spanish and English) is absent or a page yields no cards; navigates directly to `/jobs/search-results/` with `goto(wait_until="commit")` and reuses page 1 already loaded after `apply_filters`; successive-page waits capped by new policy `tope_espera_paginas_sucesivas_segundos` (min with ficha timeout); `pausa_entre_lotes_segundos` reduced 10→5; new success event `captura_completada` with evidence "páginas=N | ofertas=M" replaces `captura_exitosa` in the node's code contract.
- **Impact:** Capture time 1m51s → 58s (COR-0864: 5 pages, 98 offers, 10 new, 0 errors); ficha técnica "Capturar ofertas" re-edited to v1.2 (as-built); descriptions stay empty at discovery (enrichment in Preparation).

### D12. LinkedIn search filters narrowed to 24-hour window

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Initial config was too broad (no location, no modality, 3 keywords) and repeated re-discovery flooded the run.
- **Decision:** LinkedIn filters set to `keywords: ["Data Engineer"]`, `ubicacion: "Colombia"`, `modalidad: "remoto"` (`f_WT=2`), `fecha_publicacion: "r86400"` (last 24 h, `f_TPR`).
- **Impact:** COR-0792: 97 results → 93 new (4 dupes) in 1m51s; COR-0864: 98 offers, 10 new. Verified URL: `?keywords=Data+Engineer&location=Colombia&f_WT=2&f_TPR=r86400`.

### D13. Adapter registry per `fuente_id` with `fuente_no_soportada`

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** The three flow nodes instantiated `LinkedInAdapter()` directly, coupling the flow to a concrete class; adding a source would require editing the nodes.
- **Decision:** New `modules/discovery/adapters/registry.py` defines the `AdaptadorPlataforma` Protocol (enter_source, apply_filters, capture_batch, close_session — structurally checked by mypy strict), `REGISTRO_ADAPTADORES = {"linkedin": LinkedInAdapter}` and `obtener_adaptador(fuente_id)`; nodes resolve the adapter by `fuente_id`. Unknown sources raise `FlowError("fuente_no_soportada")` (never retried, `should_retry` only retries `fuente_inalcanzable`/`tiempo_agotado_*`) — new official DOC-06-style code documented in the ficha.
- **Impact:** A new source = adapter file + one registry line + config block, no node changes; unknown sources fail cleanly without pointless retries; operational guide `docs/adding-a-new-source.md` created and linked from README.

### D14. Write-only context state removed (Lote 1 quick-win cleanup)

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Project-wide review (findings A1–A5) found dead state and slow tests in Module 1: `RunContext` carried six fields that were written but never read in production (`paginas_consumidas`, `capturadas_acumuladas_fuente`, `limite_alcanzado`, `motivo_terminacion`, `fecha_terminacion`, `posicion_fuente_corriente`); `ResultadoInicio.motivo`, `eventos_declarados` (LinkedInAdapter) and `_fallo_nodo`'s `resultado` param were unused; `finalizar_proceso` queried metrics twice; retry sleeps made the suite take ~35 s; 2 fixture HTMLs and 9 conftest fixtures were dead.
- **Decision:** Remove the six write-only fields (capture progress lives only in `estado_captura`; the termination reason is passed to Finalizar Proceso by the orchestrator parameter, `motivo_terminacion` DB column unchanged); remove `ResultadoInicio.motivo`, `eventos_declarados` and `_fallo_nodo(resultado=...)`; single `consultar_metricas` call reused for the termination event and run closure; retry sleeps neutralized in tests (`patch("time.sleep")`, tenacity binds sleep at import); dead fixtures deleted (kept `example_offer`, `example_profile` and their dependencies).
- **Impact:** No behavior or DB-schema change; suite 273 tests in ~3.4 s (was ~35 s); tracker sub-phase 4.10; ficha técnica as-built note (no node re-edition, contract intact).

### D15. Spanish catalog completed for `shared/persistence.py` function names (Lote 2)

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Decisions D7/D8 (2026-08-11) set Spanish for persistence fields, config keys, and discovery identifiers, but `shared/persistence.py` kept 11 English function names with a duplicated alias pair (`release_lock`/`liberar_bloqueo`); the catalog was half-applied. Also found: `indice_set INTEGER DEFAULT ''` (text default in an INTEGER column) in `ofertas`, `eventos` and `sesiones` — inert (SQLite tolerates it; code always writes the column explicitly).
- **Decision:** Rename the 11 functions to Spanish and drop the English aliases: `generate_id`→`generar_id`, `read_table`→`leer_tabla`, `write_row`→`escribir_fila`, `write_batch`→`escribir_lote`, `find_by_id`→`buscar_por_id`, `update`→`actualizar_fila`, `acquire_lock`→`adquirir_bloqueo`, `release_lock` merged into `liberar_bloqueo` (single implementation), `check_lock`→`consultar_bloqueo`, `probe_write`→`sondear_escritura`, `write_corrida`→`registrar_corrida`, `write_evento`→`escribir_evento` (~210 references across persistence, discovery nodes and tests). `indice_set DEFAULT ''` is NOT migrated: SQLite cannot alter a column default (table rebuild required) and the wart is inert — documented here as a known issue for any future schema migration.
- **Impact:** No behavior or DB-schema change (column `motivo_terminacion` and all tables untouched); 273 tests in ~3.4 s; consistency with D7/D8 completed; operational doc `docs/reports/database-tables.md` updated to the new names; tracker sub-phase 4.11; ficha técnica as-built note. Historical mentions in tracker Phase 1 and MVP Execution Plan kept as record of the time.

---

## Prompt/design alignment decisions

### C2. Detailed Evaluation entity uses Spanish attribute names

- **Date:** 2026-07-30
- **Status:** In effect
- **Context:** Prompts PRM-002..005 originally produced English/mixed outcomes.
- **Decision:** Detailed Evaluation entity fields are Spanish (e.g., `resultado_organizacional`, `logica_xyz`, `insumos_carta_presentacion`); prompts redesigned to v2 producing exactly those fields; chained execution; `ProcessingResult` → `EvaluacionDetallada`. Catalogs Overqualification Risk and Final Recommendation use Spanish values (`Bajo/Medio/Alto`, `Aplicar/Aplicar con reservas/No aplicar`).
- **Impact:** DOC-13A §2.7 and §3.15–3.16 reflect this; prompts emit Spanish output.

### C5. Module 1 registers offers with `estado='descubierta'`

- **Date:** 2026-08-07
- **Status:** In effect
- **Context:** Offer state machine has 7 states; discovery is the entry point.
- **Decision:** Module 1 inserts discovered offers with `estado='descubierta'` (default assignment, no normalization/dedup beyond D4 upsert; those belong to Module 2).
- **Impact:** Every newly registered offer enters the pipeline in `descubierta`.

---

## Implementation deviations

### PMD-020. Processed Offer attribute deviations

- **Date:** 2026-07-30
- **Status:** In effect
- **Context:** Document 13A Processed Offer spec vs `shared/models.py`.
- **Decision:** `requisitos`, `tecnologias`, and `idiomas` are implemented as JSON lists instead of Long Text; `summary`, `technical_skills`, and `soft_skills` are not implemented in `shared/models.py`; `salary_range` implemented as `salario_min`/`salario_max`/`moneda`; `normalized_position` → `titulo_limpio`; `processed_description` → `descripcion_limpia`.
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
| DE-LI-010 | Module 1 implementation criteria per DOC-09 §6: verifiable entry criterion, config-defined filter mapping, capture policies, `bloqueo_plataforma` (Group A, no retry), `sesion_expirada` with controlled re-entry. **Updated 2026-08-10:** entry criterion for authenticated sources is HTML polling for `voyager` on the feed (global-nav no longer renders); direct login URL flow; selectors use prefix match + `:visible` with Enter submit and click fallback; per-page parsing variants resolved by exclusivity. **Updated 2026-08-12 (D9):** entry criterion is HTML polling for the `MainFeed` string (config `criterio_exito`), superseding `voyager`; evaluated only after the username field is detached; login flow unchanged. |

---

## Version history

| Version | Date | Change |
|---|---|---|
| 1.4 | 2026-08-12 | Added D15 (Spanish catalog completed for persistence function names; `indice_set DEFAULT ''` known inert issue, not migrated). |
| 1.3 | 2026-08-12 | Added D14 (Lote 1 quick-win cleanup: write-only context state removed, dead params/fixtures, single metrics query, fast suite). |
| 1.2 | 2026-08-12 | Added D9 (MainFeed entry criterion), D10 (visible-only blocked detection), D11 (list-based capture), D12 (24h filters) and D13 (adapter registry + `fuente_no_soportada`); DE-LI-010 updated to D9. |
| 1.1 | 2026-08-11 | Added D7 (Spanish naming catalog) and D8 (Spanish state/timeout vocabulary); identifier references in prior decisions updated to the current catalog. |
| 1.0 | 2026-08-11 | Initial unified log: consolidated D1–D6, C2, C5, PMD-020/021, DE-LI-001..010 (9A archived). |