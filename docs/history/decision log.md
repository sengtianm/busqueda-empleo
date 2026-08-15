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

### D16. Persistence performance: single-connection upsert and lookup indexes (Lote 3)

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Project-wide review findings C1/C2: `upsert_oferta` opened up to 3 connections per offer (SELECT via `leer_tabla`, UPDATE via `actualizar_fila`, INSERT via `escribir_fila`; plus `generar_id` in the insert path) — hundreds of connections per capture (~90–100 offers); the DB had no indexes, so the per-offer dedup lookup (`ofertas.id_externo`) and the closure-metrics queries (`ofertas.id_corrida`, `eventos.id_corrida`) did full table scans.
- **Decision:** (1) Rewrite `upsert_oferta` internals to a single connection (SELECT → UPDATE or INSERT → one commit); same signature, same behavior; the refresh path now touches only `fecha_ultima_verificacion` (the previous implementation also updated `fecha_ultima_edicion` as a side effect — the new behavior matches D4 literally: "an existing row only refreshes `fecha_ultima_verificacion`"). (2) Create three non-unique indexes, idempotently via `CREATE INDEX IF NOT EXISTS` in `init_db` (applies to existing DBs on next run, no table rebuild, no backup): `idx_ofertas_id_externo`, `idx_ofertas_id_corrida`, `idx_eventos_id_corrida`. Indexes are intentionally NOT UNIQUE: a unique `id_externo` would enforce integrity but could fail on pre-existing duplicates and changes behavior; strict two-layer dedup belongs to Module 2 (D4).
- **Impact:** No behavior, data, or schema change (indexes are additive and reversible with `DROP INDEX`); 274 tests in ~3.4 s; capture and closure queries faster as `ofertas`/`eventos` grow; tracker sub-phase 4.12; `docs/reports/database-tables.md` index note.

### D17. Test quality and last cleanups (Lote 4): vestigial node retired, session close via contract, config and integration tests

- **Date:** 2026-08-12
- **Status:** In effect
- **Context:** Project-wide review findings E1/E2 and D1/D2: `close_session` (contract D13, documented in `adding-a-new-source.md`) was never called — the orchestrator and Finalizar Proceso closed the page with `page.close()` directly; the decision node "¿Quedan ofertas por capturar…?" always answered `no` since list-based capture (D11) — a constant decision with no flow impact, still documented in the ficha; `shared/config.py` (used by every module) had zero dedicated tests; the orchestrator was tested only with all nodes mocked (143 patches), with no end-to-end guarantee.
- **Decision:** (1) Retire the "¿Quedan ofertas por capturar…?" node from `captura.py`, the orchestrator flow, its tests, and the ficha técnica (node section replaced by an as-built removal note; successors re-wired: "Registrar ofertas…" delivers control directly to "¿Quedan sets…?"). (2) Session close goes through the adapter contract: `obtener_adaptador(fuente_id).close_session(pagina)` in `_cerrar_sesion_anterior` (orchestrator) and `_cerrar_recursos` (Finalizar Proceso), with `page.close()` fallback when no source is set — no behavior change. (3) New dedicated tests: `tests/test_config.py` (5 tests: YAML+env load, cache, reload, empty YAML, invalid YAML) and `tests/test_orquestador_integracion.py` (2 integration tests running the full flow with real nodes — only the adapter, config data and the Chromium launch are simulated — asserting corrida/ofertas/sesiones/eventos persisted, lock released, `close_session` called, and dedup on a second run).
- **Impact:** No behavior or data change; the flow now has 12 nodes (was 13); code aligns with the documented Protocol contract (D13); 278 tests in ~3.6 s; ficha as-built note; tracker sub-phase 4.13; AGENTS.md test count 278.

### D18. LinkedIn labels `f_TPR` windows with the nearest UI bucket; the filter itself works

- **Date:** 2026-08-14
- **Status:** In effect
- **Context:** The user reported that the LinkedIn jobs search UI showed "Data Engineer · Últimas 24 horas" while `config.yaml` set `fecha_publicacion: "r18000"` (5 h), and the modality filter seemed unapplied. A controlled empirical test (2026-08-14, authenticated session, 5 URL variants, evidence in HTML/screenshots) established: totals 11 (r18000/5 h), 17 (r43200/12 h), 58 (r86400/24 h), 368 (no date) with `f_WT=2` — the date window and modality filters ARE applied by LinkedIn (cards all "Hace ≤4 h" for r18000; pill "En remoto" selected; 19→11 offers when `f_WT=2` is added). However the UI labels ANY non-named `f_TPR` window as "Últimas 24 horas" (`aria-label="...Se ha aplicado el filtro «Últimas 24 horas»..."`), even r43200 (12 h), and every job card embeds a hardcoded accessible text "En las últimas 24 horas" while showing "Hace N horas".
- **Decision:** Keep arbitrary `r<N>` windows in `fecha_publicacion` (r18000 = 5 h filters correctly; the label is cosmetic and cannot be changed — platform limitation). The flow was verified correct end-to-end (URL construction, parameter mapping, effective filtering); no code change was required for the filters themselves.
- **Impact:** Config remains `r18000` (5 h); the UI label stays "Últimas 24 horas" (cosmetic); future investigations must not treat the label as evidence of a broken filter — verify via result totals and card timestamps.

### D19. Search observability: successful `SearchResult` carries the applied URL + declared total

- **Date:** 2026-08-14
- **Status:** In effect
- **Context:** During the D18 investigation, no run logged the applied search URL or the declared total, so real runs could not be diagnosed (e.g., whether a run used a 5 h or 24 h window).
- **Decision:** `LinkedInAdapter._parsear_resultados` sets `evidencia_acotada = "url: <search url>" (+ " | total: <declared total>" when present)` on successful results, and `apply_filters` logs INFO "Busqueda aplicada | url=... | total_declarado=... | ofertas_primera_pagina=N". The generic event node (`registrar_evento`) already persists `evidencia_acotada`, so each successful search event in `eventos` now records URL + total + attempts.
- **Impact:** Real runs become diagnosable from `logs/execution_*.log` and the `eventos` table without re-investigation; no behavior change; 1 new adapter test (evidence url + total); 282 tests total.

### D20. `fecha_publicacion` format validation in the adapter (`r<N>`), not a UI-bucket catalog

- **Date:** 2026-08-14
- **Status:** In effect
- **Context:** The D18 test proved arbitrary `r<N>` windows (e.g. `r18000` = 5 h) filter correctly even though LinkedIn labels them with the nearest UI bucket (D18). A catalog of "UI-supported" values would therefore wrongly reject working configs (e.g. `r18000`).
- **Decision:** `_construir_url_busqueda` validates the FORMAT of `fecha_publicacion` as `r<N>` (regex `^r\d+$`); malformed values (e.g. "24h", "5 horas") raise `FlowError("filtros_no_aplicables")` — the existing official mechanism (ficha ERR-02, set discarded, never retried). Validation lives in the adapter because the value format is platform-specific (RN-04/RN-09: filter applicability belongs to the search node/adapter, not INICIO).
- **Impact:** Malformed date values fail fast with the official code instead of being silently discarded by LinkedIn; `r18000` (and any `r<N>`) keeps working; 2 new adapter tests (malformed format rejected, `r<N>` accepted).

### D21. Login fallback tolerant to slow form detach

- **Date:** 2026-08-14
- **Status:** In effect
- **Context:** During the D18 test run, `_autenticar`'s fallback failed a REAL successful login: after Enter, the username field detached slower than the 15 s wait; the fallback `page.click("button:visible:text-is('Iniciar sesión')", timeout=15000)` then raised because the submit button was already gone (form detached mid-login), turning a successful login into `autenticacion_rechazada`.
- **Decision:** The fallback click becomes best-effort: `click(..., timeout=5000)` wrapped in try/except (button may already be gone), followed by the existing 30 s detached wait. A slow detach now ends in the 30 s wait instead of an exception; invalid credentials still fail downstream via the entry criterion (`criterio_no_cumplido`), as before.
- **Impact:** Intermittent false `autenticacion_rechazada` failures on slow logins eliminated; behavior otherwise unchanged; 1 new adapter test (detach-lento fake page).

### D22. Batch persistence and retry in one connection; Playwright resource closure reused (Lote A)

- **Date:** 2026-08-14
- **Status:** In effect
- **Context:** Capture persisted offers with one connection per offer (`upsert_oferta`, D16): ~90–100 connections per capture run. A leak review also found `finalizar.py` closed Playwright resources only on the happy path; when the orchestrator switched sources it opened a new session (`ingreso`) without closing the previous one, leaking the previous browser context between sources. Closure metrics (`consultar_metricas`) read whole tables into Python to count rows (`leer_tabla`), increasingly expensive as tables grow.
- **Decision:** (1) Persistence by batch: `upsert_lote_ofertas(filas) -> (registradas, fallidas)` writes the whole lot in one connection (core `_upsert_ofertas_en`; dedup by `id_externo` per D4, including intra-lot duplicates; a row-level failure logs `id_externo`/`id_corrida` and does not abort the lot; `upsert_oferta` becomes a thin wrapper that raises a descriptive `PersistenceError` on invalid rows instead of an `IndexError`). Batch retry policy: 2 attempts of the WHOLE lot, only on connection/transaction exceptions (`should_retry`); per-row failures are row-data errors and are NOT retried. `_generar_id_en(conn, tabla)` captures generated ids via `RETURNING` (no extra SELECT); `generar_id` updated; the D16 non-unique index makes the dedup lookup a single SELECT. (2) Closure metrics by SQL: new `contar_filas(tabla, filtros)` / `contar_distintos(tabla, columna, filtros)` (empty column values excluded); `consultar_metricas` uses them, dropping the full-table `leer_tabla` reads. (3) Playwright leak fix: `RunContext` gains typed `browser`/`playwright_instance` fields; `ingreso` assigns them on success and clears them on definitive failure/reset; `finalizar.cerrar_recursos(contexto)` is now public (page → browser → instance, resets the three fields, idempotent) and the orchestrator reuses it on source switch (`_cerrar_sesion_anterior`) — the adapter `close_session` contract (D17) is unchanged.
- **Impact:** One connection per lot (~10× fewer connections per capture) with identical dedup semantics (D4); closure metrics stop scanning whole tables; no more browser-context leak between sources. Derogates the ficha NOTA 4.4 ("persistencia por oferta"): batch persistence is now the as-built mode and RN-06/VAL-03 of "Registrar ofertas capturadas" were updated accordingly. 10 new tests; 292 total; ruff/mypy clean.

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
| 1.7 | 2026-08-14 | Added D18 (LinkedIn labels any `f_TPR` window with the nearest UI bucket; filter itself verified working), D19 (search observability: successful `SearchResult` carries URL + declared total; INFO log in `apply_filters`), D20 (`fecha_publicacion` format validation `r<N>` in the adapter, not a UI-bucket catalog), D21 (login fallback tolerant to slow form detach). |
| 1.6 | 2026-08-12 | Added D17 (Lote 4 test quality + cleanups: vestigial "¿Quedan ofertas…?" node retired, session close via `close_session` contract, config tests, orchestrator integration tests). |
| 1.5 | 2026-08-12 | Added D16 (persistence performance: single-connection upsert, 3 non-unique indexes). |
| 1.4 | 2026-08-12 | Added D15 (Spanish catalog completed for persistence function names; `indice_set DEFAULT ''` known inert issue, not migrated). |
| 1.3 | 2026-08-12 | Added D14 (Lote 1 quick-win cleanup: write-only context state removed, dead params/fixtures, single metrics query, fast suite). |
| 1.2 | 2026-08-12 | Added D9 (MainFeed entry criterion), D10 (visible-only blocked detection), D11 (list-based capture), D12 (24h filters) and D13 (adapter registry + `fuente_no_soportada`); DE-LI-010 updated to D9. |
| 1.1 | 2026-08-11 | Added D7 (Spanish naming catalog) and D8 (Spanish state/timeout vocabulary); identifier references in prior decisions updated to the current catalog. |
| 1.0 | 2026-08-11 | Initial unified log: consolidated D1–D6, C2, C5, PMD-020/021, DE-LI-001..010 (9A archived). |