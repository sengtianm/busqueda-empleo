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
| 4.2 | Platform entry (2 nodes) | Ficha técnica, DOC-09, Annex 9A | ✅ | LinkedIn login, credentials, conditional retries, entry_result. 152 tests passing. |
| 4.3 | Filter search (2 nodes) | Ficha técnica, DOC-09 | ✅ | Set iterator (reset on source switch), adapter search (`filtros_no_aplicables`, empty values skipped), `search_result` contract (`exito`/`fallo`), conditional retries, generic register node scoped to current source (`TipoEvento` enum, write failure tolerated). 171 tests passing. |
| 4.4 | Capture and registration (4 nodes) | Ficha técnica, DOC-09, DOC-13, DOC-04 | ✅ | Capture policies, batch write, dedup by `id_externo` (upsert, decision D4 2026-08-09; column name per D7 2026-08-11), Grupo A/B, pagination loop. 199 tests passing. |
| 4.5 | Closure and orchestrator (2 nodes) | Ficha técnica | ✅ | Terminal node Finalizar Proceso (closure metrics with zero fallback, single-retry update, exit event, Playwright resource close, lock release) + full-flow orchestrator (`ejecutar_flujo`, 13 nodes, source/set loops, abort with motivo, INICIO non-ok exits without Finalizar). 229 tests passing. Audited CONFORME (minor finding "duplicated metrics query" — resolved in sub-phase 4.10). |
| 4.6 | Documentation closure and authority model | Ficha técnica, decision log | ✅ | Module 1 closed as-built: ficha técnica v1.1 (`estado_captura.indice_set` per D7), unified decision log v1.0 (`docs/history/decision log.md`, D1–D6/C2/C5/PMD-020/021/DE-LI), DOC-01 reconciled (D4 dedup, RF-M1-009), authority model in AGENTS.md (primary construction docs vs derived living DOC-01 vs ficha inputs vs archive), retired design docs moved to `docs/history/archive/`, `browser.headless` reverted to `true`. |
| 4.7 | Spanish naming catalog (decisions D7/D8) | Decision log, DOC-13A, ficha técnica | ✅ | English→Spanish word-boundary rename across persistence, config, discovery code, and tests (main: `run_id`→`id_corrida`, `source_id`→`fuente_id`, `session_id`→`id_sesion`, `set_indice`→`indice_set`, `offer_id`→`id_oferta`, `id_externo_url`→`id_externo`, `creation_date`→`fecha_creacion`, `timestamp_ultima_verificacion`→`fecha_ultima_verificacion`); states `descubierta`…`finalizada`; timeout codes `tiempo_agotado_*`; `shared/errors.py` exempt (error-context attributes). `job_search.db` migrated via `_migrar_espanol_total` (rebuild + explicit column map + `CASE` estado + `sesiones.id` backfill; idempotent; backup `job_search_pre_espanol_20260811_073632.db`; 7 offers preserved). Docs aligned: DOC-13A v1.5, ficha técnica as-built note, decision log v1.1 (D7/D8), MVP plan. 243 tests passing; ruff/mypy clean. |
| 4.8 | Post-closure fixes from functional test (COR-2303 findings) | Ficha técnica, AGENTS.md | ✅ | Functional E2E run on 2026-08-11 exposed two gaps, fixed: (1) `logging_setup.setup()` was never invoked → `modules/discovery/__main__.py` now calls it before `ejecutar_flujo()`, restoring file persistence (`logs/execution_*.log`) and config-driven level/rotation/retention; new unit test `tests/test_logging_setup.py`. (2) pytest contaminated the real DB (events/sessions referencing fictional run ids — e.g. EVT-0062/0063 and SES-0264/0265 for COR-2249/2253/2262, plus COR-9001 from unit tests — none present in the `corridas` table) → `temp_db_file` fixture is now `autouse` in `tests/conftest.py`, isolating the whole suite. Dev DB wiped with backup `data/backup/job_search_db_pre_limpieza_20260811_112013.db` (state after a prior partial cleanup) and re-verified clean after full suite. 244 tests passing; ruff/mypy clean; E2E re-run terminates `corrida_completada` with file logging active (LinkedIn still challenges headless: `bloqueo_plataforma` handled per ficha). |
| 4.9 | Capture optimization, search scope, and adapter registry (decisions D9–D13) | Ficha técnica, decision log | ✅ | (1) LinkedIn filters narrowed per user: `Data Engineer` / `Colombia` / `remoto` / 24 h (`r86400`) — COR-0792: 97→93 new, 0 errors. (2) List-based capture (D11): direct `/jobs/search-results/` navigation with `wait_until="commit"`, page-1 reuse, end by missing pagination button, `tope_espera_paginas_sucesivas_segundos` (10 s, min with ficha timeout), `pausa_entre_lotes` 10→5 s, success event `captura_completada` "páginas=N \| ofertas=M" replacing `captura_exitosa` — COR-0864: 5 pages, 98 offers, 10 new in 58 s (was 1m51s), 0 errors. (3) Adapter registry (D13): `modules/discovery/adapters/registry.py` with `AdaptadorPlataforma` Protocol, `REGISTRO_ADAPTADORES={"linkedin": LinkedInAdapter}`, `obtener_adaptador(fuente_id)`; the 3 flow nodes resolve adapters via registry; unknown source → `fuente_no_soportada` (never retried). (4) Blocked-detector visible-only (D10): 5 regression tests. (5) Entry criterion `MainFeed` formalized (D9, DE-LI-010 updated). Docs closed: ficha técnica "Capturar ofertas" v1.2 (as-built), decision log v1.2 (D9–D13), guide `docs/adding-a-new-source.md` (+README link). 273 tests passing; ruff/mypy clean. |
| 4.10 | Quick-win cleanup — Lote 1 (project-wide review, findings A1–A5; decision D14) | Ficha técnica, decision log | ✅ | (1) Test suite ~10× faster: retry sleeps neutralized (autouse fixture `_sin_esperas_de_reintento` in test_ia_service.py + `patch("time.sleep")` in test_node_busqueda.py; tenacity binds sleep at import) — 273 tests in ~3.4 s (was ~35 s). (2) Six write-only `RunContext` fields removed (capture progress only in `estado_captura`; termination reason passed by orchestrator param; DB column `motivo_terminacion` unchanged) — resolves 4.5's "duplicated metrics query" finding. (3) Dead fixtures deleted: `authwall_linkedin.html`, `detalle_linkedin_sesion.html`, 9 unused conftest fixtures (kept `example_offer`/`example_profile` + deps). (4) Single `consultar_metricas` call in Finalizar Proceso. (5) Dead params/fields removed: `_fallo_nodo(resultado)`, `ResultadoInicio.motivo`, `eventos_declarados`. Docs: decision log v1.3 (D14), ficha as-built note, AGENTS.md test count 273. 273 tests passing; ruff/mypy clean. |
| 4.11 | Spanish catalog completed for persistence function names (Lote 2; decision D15) | Ficha técnica, decision log | ✅ | (1) `shared/persistence.py` renamed to Spanish, English aliases dropped: `generate_id`→`generar_id`, `read_table`→`leer_tabla`, `write_row`→`escribir_fila`, `write_batch`→`escribir_lote`, `find_by_id`→`buscar_por_id`, `update`→`actualizar_fila`, `acquire_lock`→`adquirir_bloqueo`, `release_lock` merged into `liberar_bloqueo`, `check_lock`→`consultar_bloqueo`, `probe_write`→`sondear_escritura`, `write_corrida`→`registrar_corrida`, `write_evento`→`escribir_evento` (~210 refs across shared/persistence.py, 7 discovery files + 5 test files; D7/D8 catalog now complete). (2) Known inert issue documented, NOT migrated: `indice_set INTEGER DEFAULT ''` in `ofertas`/`eventos`/`sesiones` (SQLite cannot alter a column default; harmless). Docs: decision log v1.4 (D15), ficha as-built note, `docs/reports/database-tables.md` updated to new names. 273 tests passing; ruff/mypy clean. |
| 4.12 | Persistence performance (Lote 3; decision D16) | Ficha técnica, decision log | ✅ | (1) `upsert_oferta` rewritten to a single connection (was 3 per offer: SELECT + UPDATE/INSERT) — same signature/behavior, ~270–300 connections per capture reduced to ~90–100. (2) Three non-unique indexes created idempotently in `init_db` (apply to existing DBs on next run, no rebuild/backup, reversible with `DROP INDEX`): `idx_ofertas_id_externo` (dedup lookup), `idx_ofertas_id_corrida` + `idx_eventos_id_corrida` (closure metrics). NOT UNIQUE on purpose: strict dedup is Module 2 (D4). Docs: decision log v1.5 (D16), `docs/reports/database-tables.md` index note. 274 tests passing; ruff/mypy clean. |
| 4.13 | Test quality + last cleanups (Lote 4; decision D17) | Ficha técnica, decision log | ✅ | (1) Vestigial decision node "¿Quedan ofertas por capturar…?" retired (constant `no` since list-based capture D11): removed from `captura.py`, orchestrator flow (now 12 nodes) and 12 tests; ficha re-edited — node section replaced by an as-built removal note, successors re-wired to "¿Quedan sets…?". (2) Session close delegated to the adapter contract: `obtener_adaptador(...).close_session(page)` in orchestrator and Finalizar Proceso (was `page.close()` direct; `page.close()` fallback when no source set). (3) New `tests/test_config.py` (5 tests: YAML+env load, cache, reload, empty/invalid YAML). (4) New `tests/test_orquestador_integracion.py` (2 integration tests: full flow with real nodes, simulated adapter/config/Chromium launch; asserts corrida completada, 2 ofertas persisted with `id_externo`, sesiones audit, `captura_completada` event, lock released, `close_session` called; second run dedups). Docs: decision log v1.6 (D17), ficha as-built note, AGENTS.md test count 278. 278 tests passing (~3.6 s); ruff/mypy clean. |
| 4.14 | Filter investigation + observability hardening (decisions D18–D21) | Ficha técnica, decision log | ✅ | (1) Filter issue investigated empirically (2026-08-14, authenticated session, 5 URL variants): LinkedIn DOES apply `f_TPR` (totals 11/17/58/368 for r18000/r43200/r86400/none) and `f_WT=2` (19→11 offers); the UI merely labels any `r<N>` window as "Últimas 24 horas" and cards embed hardcoded accessible text — cosmetic platform limitation (D18). Config `r18000` (5 h) confirmed correct and kept. (2) Observability (D19): successful `SearchResult` now carries `evidencia_acotada = "url: <URL> | total: <N>"` (persisted by the generic event node) and `apply_filters` logs INFO "Busqueda aplicada". (3) Format validation (D20): `_construir_url_busqueda` rejects `fecha_publicacion` not matching `^r\d+$` with official `filtros_no_aplicables` (adapter-level, RN-04/09); `r<N>` values keep working. (4) Login fallback hardened (D21): fallback click best-effort (5 s try/except) + 30 s detached wait — slow detach no longer turns a real successful login into `autenticacion_rechazada`. Docs: decision log v1.7 (D18–D21). 282 tests passing; ruff/mypy clean. |
| 4.15 | Playwright leak fix + batch persistence & SQL metrics (Lote A; decision D22) | Ficha técnica, decision log | ✅ | (1) Playwright resource leak fixed: `RunContext` gains typed `browser`/`playwright_instance` (assigned on successful "Ingresar a la plataforma", cleared on definitive failure/reset); `finalizar.cerrar_recursos` is now public (page→browser→instance, resets the three fields, idempotent) and the orchestrator reuses it on source switch (`_cerrar_sesion_anterior`) — switching sources no longer leaks the previous browser context; adapter `close_session` contract unchanged. (2) Batch persistence (D22, derogates ficha NOTA 4.4 "persistencia por oferta"): `upsert_lote_ofertas(filas) -> (registradas, fallidas)` writes the whole lot in one connection (core `_upsert_ofertas_en`, dedup by `id_externo` incl. intra-lot duplicates, per-row errors logged with `id_externo`/`id_corrida` without aborting; `upsert_oferta` becomes a thin wrapper raising a descriptive `PersistenceError` on invalid rows); `_generar_id_en` captures ids via `RETURNING` (no extra SELECT). Retry policy: 2 attempts of the whole lot on connection/transaction exceptions only (`_registrar_lote_con_reintento` in `captura.py`). (3) Closure metrics by SQL: `contar_filas`/`contar_distintos` (empty values excluded) replace full-table `leer_tabla` reads in `consultar_metricas`. Docs: decision log v1.8 (D22), ficha as-built notes (nodo "Registrar ofertas" + D22), AGENTS.md test count 292. 292 tests passing; ruff/mypy clean. |
| 4.16 | Retry unification, dead code removal, Pydantic validation on writes (Lote B; decision D23) | Ficha técnica, decision log | ✅ | (1) Unified retry helper `ejecutar_con_reintento` in `shared/retry.py` replaces the 3 duplicated loops (ingreso/busqueda/captura) and the test-only `retry_conditional` (deleted; 5 tests migrated + 8 new: callbacks receive (exc, intentos), backoff exponential + `max_wait` cap asserted, `max_attempts<1` both routes). Callbacks: `al_fallo_final` (FlowError, node fallo result), `al_error_interno` (ERR-07/ERR-09 branch), `al_reintento` (ingreso closes page/browser between attempts; Playwright instance reused, stopped only on definitive failure). Dispatch exclusively by `codigo_motivo` — non-flow exceptions fall to error interno exactly like the old `except Exception`. Config-driven via `_policies()` (nodes no longer read `retries` inline; `_config_reintentos` removed). (2) `escribir_lote` deleted (no production callers; 2 tests removed). (3) Pydantic validation before writes: `EventoAlmacen.model_validate` in `escribir_evento`, `Corrida.model_validate` in `registrar_corrida` (single caller INICIO `en_ejecucion`), `AuditoriaSesion.model_validate` in the session audit (non-aborting); `registro.py` passes `fuente_id=""` (None rejected by the model); 2 validation tests added. Edge preserved: `max_attempts=0` keeps `ERR-09` "Sin intentos configurados" in captura. Docs: decision log v1.9 (D23, v1.8 row repaired), `docs/reports/database-tables.md` updated (`escribir_lote` mention removed), AGENTS.md test count 300. 300 tests passing; ruff/mypy clean. |
| 4.18 | Final P4 lot: run-state catalog, value validation, context encapsulation, orchestrator helper, single credential resolution, config-driven log path (Lote D; decision D25) | Ficha técnica, decision log | ✅ | (1) `EstadoCorrida` reduced to the D4 vocabulary (`en_ejecucion`/`completada`/`sin_fuentes`/`abortada`; `error`/`concurrencia` removed — no production callers, only tests); `Corrida` extended with closure fields `fecha_fin`, `motivo_terminacion`, `total_ofertas`, `total_sucesos`, `total_errores`, `fuentes_procesadas` (defaults) + `extra="forbid"`; `actualizar_corrida` now validates the update dict with the `Corrida` model before writing (D23 deferred P4-13 closed; `registrar_corrida` callers unaffected). (2) Dead `hasattr` structural checks replaced by value validation `estado not in ("exito","fallo")` → ERR-02 in ingreso/busqueda (error contract preserved). (3) `RunContext.marcar_cambio_de_fuente(fuente_id)` public, idempotent within a source; busqueda no longer mutates privates. (4) Orchestrator `_ejecutar_nodo` helper + `_ResultadoNodo` Protocol (estado/descripcion/decision); 11 call sites unified; `ResultadoRegistro` gained `decision: str = ""`; flow order/motivos unchanged (orchestrator integration tests pass). (5) `_resolver_credenciales` single config read (was 1 per attempt); `_obtener_credenciales` deleted. (6) `json`/`loguru` imports to top of `shared/ia_service.py`; `logging.logs_path: "logs"` in config consumed by `_logs_path()` with fallback. Docs: decision log v1.11 (D25), ficha + DOC-13A as-built notes (F-001/F-002 corrected; F-003 kept as known drift), AGENTS.md test count 307. 307 tests passing; ruff/mypy clean. |

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
