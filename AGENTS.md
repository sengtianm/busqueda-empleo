# AGENTS.md

## Project
Automated job search pipeline: discovers, collects, prepares, evaluates, processes, and manages opportunities to reduce search time/effort and support decision-making. Objective: from discovery to high-quality application inputs with full traceability and minimal manual intervention.

**Status:** MVP in progress — Phases 0–3 done (infrastructure, shared services, prompts tested with `gemma4:31b-cloud`); Phase 4 (Module 1 — Opportunity Discovery, branch `fase-4`) complete & recorded as-built (INICIO + control nodes, platform entry, filter search + generic register, capture/registration with dedup by `id_externo`, closure node + full-flow orchestrator; ficha técnica closed v1.1, decision log v1.0 created); Spanish naming catalog implemented and documented (decisions D7/D8, 2026-08-11: DB fields, states, and timeout codes in Spanish; `job_search.db` migrated with backup; DOC-13A v1.5, decision log v1.1, tracker Phase 4.7); filter investigation + observability hardening closed (decisions D18–D21, 2026-08-14: LinkedIn `f_TPR`/`f_WT` verified working — UI labels cosmetic; search evidence URL+total; `fecha_publicacion` format validation `r<N>` in adapter; login fallback robust to slow detach; decision log v1.7, tracker 4.14, 282 tests); Lote A closed (decision D22, 2026-08-14: batch persistence in one connection `upsert_lote_ofertas` derogating ficha NOTA 4.4, SQL closure metrics `contar_filas`/`contar_distintos`, `RETURNING` ids, Playwright leak fix with public `cerrar_recursos` reused by the orchestrator; decision log v1.8, tracker 4.15, 292 tests); Lote B closed (decision D23, 2026-08-14: unified retry helper `ejecutar_con_reintento` in `shared/retry.py` replacing the 3 node loops + test-only `retry_conditional`, `escribir_lote` deleted, Pydantic validation on writes `EventoAlmacen`/`Corrida`/`AuditoriaSesion`; decision log v1.9, tracker 4.16, 300 tests); Lote C closed (decision D24, 2026-08-14: P3 duplication unifications — `ahora()`/`FORMATO_TIMESTAMP`/`TIPOS_ACCESO` in `shared/utilidades.py`, `escribir_evento_seguro` in persistence, `_enviar` in ia_service, merged capture policies in run_context, unified `_revisar_estado` in the adapter, `_resultado_fallo` in busqueda; decision log v1.10, tracker 4.17, 302 tests); Lote D closed (decision D25, 2026-08-14: P4 improvement plan items 13–18 — `EstadoCorrida` aligned to D4 (`en_ejecucion`/`completada`/`sin_fuentes`/`abortada`) + `Corrida` closure fields with `extra="forbid"`, `actualizar_corrida` validated; value validation replacing dead `hasattr` checks; `marcar_cambio_de_fuente` in run_context; `_ejecutar_nodo` + `_ResultadoNodo` Protocol in orchestrator; `_resolver_credenciales` single read; `logging.logs_path`; decision log v1.11, tracker 4.18, 307 tests); search entry optimized (decision D26, 2026-08-14: `apply_filters` navigates straight to the `/jobs/search-results` SDUi list with `wait_until="commit"` — removes the transient post-login `fuente_inalcanzable` retry duplication and the unreliable-total `/jobs/search` intermediate; one search load + direct pagination, verified by COR-2140; decision log v1.12, tracker 4.19, 308 tests); SDUi filters verified + hardened (decision D27, 2026-08-17: new UI drops `f_WT`/`location` — remote-only via `f_SAL=f_SA_id_225001:272001`, canonical date buckets only (`r86400`/`r604800`/`r2592000`, config now `r86400`), post-load DOM chip verification (remote radio `aria-checked='true'`, date via `label[for]` + sibling checkbox) + best-effort UI click fallback for missing filters + `filtros_no_aplicables` on failure, total from plain text "N resultados", pagination from the applied URL; supersedes D18/D20/D26; verified by COR-0344, 0 errors; decision log v1.13, tracker 4.20, 318 tests); card field extraction closed (decision D28, 2026-08-17: SDUi card text parsing for `empresa_nombre`/`ubicacion_nombre`/`fecha_publicacion` — hashed CSS classes, `<p>` classification with fixed noise exclusion (Exp 9: 75/75 cards); `fecha_publicacion` as approximate timestamp from "Publicado hace N <unidad>" (±1 h, month = 30 days) with raw text preserved in `observaciones` (approved RN-03 deviation); total only from visible DOM text (excludes script/style/HTML comments); verified COR-0001 on clean DB: 89 offers, 0 errors, 89/89 fields populated; decision log v1.14, DOC-13A v1.6, tracker 4.21, 323 tests); company/location extraction reverted (decision D29, 2026-08-17: user rejected raw strings in `ofertas` — the offer's relation to `empresas`/`ubicaciones` should be the catalog ids, out of scope; adapter keeps only enlace/título/fecha relativa + visible total; `empresa_nombre`/`ubicacion_nombre` columns dropped from `ofertas` (schema + live DB, idempotent migration); `empresa_id`/`ubicacion_id` stay NULL (D4), catalogs unpopulated (PMD-021); live DB reset with backup `data/backup/job_search_pre_d29_20260817_211232.db`, no run; decision log v1.15, DOC-13A v1.7, tracker 4.22, 322 tests); success-event traceability + observability closed (decision D30, 2026-08-17: `ingreso_exitoso`/`consulta_exitosa` emitted by the entry/search nodes aligning the ficha contracts — one event per search result (success-with-offers from the node, zero-offers/failures via the register node); `duracion_s` in `captura_completada` evidence; `total_sucesos` semantics documented (success events prior to closure, termination event never counted); default log level INFO with `LOG_LEVEL=DEBUG` override; verified fresh run COR-0001: 98 offers, 0 errors, trace complete, `total_sucesos=4`; decision log v1.16, DOC-13A v1.8, tracker 4.23, 327 tests); schema cleanup + no-empty-field rule closed (decision D31, 2026-08-18: `eventos.id_oferta` and `ofertas.identificador_origen` columns dropped, `fuentes` table + `FNT-` prefix removed (config-driven sources, never populated), fundamental rule "no empty fields" — `N/A`/`N/R` placeholders enforced at the persistence boundary (`escribir_evento`/`_upsert_ofertas_en` normalization + `DEFAULT 'N/A'`), `empresa_id`/`ubicacion_id` NULL → `'N/A'` (supersedes D4/D29 on those columns), `id_externo` excluded (dedup) and `fecha_ultima_verificacion` exempted (user instruction), `contar_distintos` excludes `'N/A'`; live DB migrated 9→8 tables with backup, 62 offers preserved; decision log v1.17, DOC-13A v1.9, database-tables.md updated, tracker 4.24, 329 tests); table rename closed (decision D32, 2026-08-19: physical table `ofertas` renamed to `ofertas_descubiertas` in schema, `secuencia_ids`, queries, discovery nodes, tests and docs; idempotent migration `_migrate_ofertas_descubiertas` first in `init_db`; prefix `OFE`, index and function names unchanged; live DB migrated in place via `init_db()`, no backup, 62 offers preserved; decision log v1.18, DOC-13A v1.10, database-tables.md and ficha as-built note updated; tracker 4.25, 331 tests); Phases 5–9 pending. **Phase 5 documentation closed (decisions D33/D34, 2026-08-20):** Module 2 (Preparation) and transversal orchestrator fichas técnicas created as authoritative construction bases; project docs aligned (decision log v1.19, DOC-13A v1.11, database-tables.md, Appendix 5A, ficha M1 as-built note on dual semantics, plan fase 5 pointers, adding-a-new-source.md, README); tracker 4.26; implementation pending approval. **Phase 5 in progress (branch `fase-5`):** sub-phase 5.1 foundations closed (2026-08-21, D33 dependencies): schema to the M2 state (`estado` CHECK with `duplicada`; `id_duplicidad`/`ubicacion_nombre`/`modalidad` on offers; `corridas.total_preparadas`/`total_duplicadas`; `eventos.id_oferta` re-added — supersedes D31 D-1 on that column; `ubicaciones` = `(ciudad, region, pais)` tuple), models/state machine extended, `normalizar_texto` utility, config `preparacion:` + `ai_routing.preparacion: local` (`gpt-oss:20b-cloud`, user choice), PRM-006 location prompt manually verified; live DB migrated with backup (136 offers preserved); decision D35 registered (location-classification routing, decision log v1.20). **Sub-phase 5.2 closed (2026-08-21):** Module 2 INICIO + candidate decision in new `modules/preparation/` (mirror of M1; Spanish identifiers exception extended to this module) — `RunContext` with FIFO candidates/counters/closure-motive slots, full `preparacion:` section validation (VAL-02), shared global lock with M1, `sin_pendientes` controlled termination fixed on the context for Finalizar Proceso (5.5); additive `leer_candidatas_descubiertas()` FIFO read in persistence. Authoritative status: `docs/history/tracker.md`.

## Architecture
Three layers: Functional modules → Shared services → Infrastructure.
Workflow: Discovery → Preparation → Evaluation → Processing → Management.
All implementations must follow this architecture (see decision log v1.0).

## Technology Stack
Python 3.12 · Playwright · BeautifulSoup + lxml · SQLite · Pydantic · httpx · Loguru · RapidFuzz · Tenacity · Ollama · PyYAML · python-dotenv · pytest · Ruff · mypy

## Project Structure
- `docs/` — official documentation (project-design, plans, reports, history)
- `config/` — centralized configuration (`config.yaml`, `.env.template`)
- `prompts/` — official prompts (separate from code)
- `modules/` — functional modules: discovery, preparation, evaluation, processing, management
- `shared/` — reusable resources (config, errors, logging, retry, models, persistence, ia_service, decision_engine, state_machine)
- `data/` — persistent data (input, processing, output, backup)
- `logs/` — logs and audit
- `temp/` — temporary files
- `scripts/` — auxiliary scripts (e.g., prompt tester)
- `tests/` — tests (fixtures in `tests/fixtures/`)

## Conventions
- English: code, documentation, configuration, prompts, commit messages, directory/file names.
- Spanish: data-related — SQLite DB (`job_search.db`), `shared/models.py`, `shared/persistence.py`, `shared/utilidades.py`, profile/criteria in `config.yaml`, test fixtures.
- Exception: `modules/discovery/` and `modules/preparation/` (node files and tests) use Spanish identifiers for domain concepts (e.g., `ejecutar_inicio`, `ResultadoInicio`, `fuentes_filtradas`, `quedan_ofertas_por_preparar`), consistent with `run_context.py` and the Spanish data layer; Spanish docstrings/error-evidence strings allowed here only.
- Spanish for all conversations with the user.
- Configuration must be separated from business logic; prompts from code; no hardcoded values.
- Every transformation must preserve original data.
- No functional module may access the database directly.
- Data rule (decision D31): no empty fields — persisted values that are not applicable/available use `N/A`/`N/R`, never `''`/NULL (exceptions: `ofertas_descubiertas.id_externo` to protect dedup, `ofertas_descubiertas.fecha_ultima_verificacion` by user instruction). `contar_distintos` treats `N/A` as empty.
- Never include API keys, tokens, passwords, or sensitive data in repository files.
- Response style: Spanish, concise, clear headings/lists; never modify files without explaining first.

## Workflow
Work cycle: Context → Define task → Analyze → Plan → Implement → Verify → Close → Save. Every user request is a task; the user defines it and approves plan/implementation. Stage gates are `/check` commands.

| Command | Stage | Who and when |
|---|---|---|
| `/resume` | Context | User-invoked |
| — | Define task | User request itself |
| `/check-analisis` | Analyze | Automatic: agent applies right after each request, before anything else |
| `/check-planeacion` | Plan | User-invoked: agent creates plan and waits approval |
| `/check-implementacion` | Implement | User-invoked: approves plan and authorizes implementation |
| `/check-tests` | Verify | Only when request requires tests; otherwise skipped |
| `/check-cierre` | Close | Automatic: agent self-verifies after implementation, including reviewers |
| `/save` | Save | User-invoked when closing session; never automatic or anticipated |

Task rules:
1. User invokes `/resume`, then sends request (task definition).
2. Apply `/check-analisis` automatically (task readiness, gap, impact, risks, viable approaches); read only necessary docs. Never skip, even for simple inspections or read-only requests.
3. Create plan only on `/check-planeacion`.
4. Implement only after `/check-implementacion` approval; minimal approved change.
5. Validate after change: lint + typecheck always when code changed; `/check-tests` only when required.
6. Apply `/check-cierre` automatically: verify acceptance criteria, review diff, run reviewers (code-reviewer, docs-reviewer), update AGENTS.md/tracker.md if changed.
7. Deliver closing report and wait approval before continuing.
8. User invokes `/save` at session end to update session history.
9. Never work on more than one task at a time.

## Keep Documents Updated
- After each validated task/phase, update AGENTS.md if existing sections changed; only update existing sections (new topics → Session History).
- Keep AGENTS.md short and useful for a new developer: clear headings/lists.
- Update `docs/history/tracker.md` when task/phase status changes; add new phase tables only when defined by MVP Execution Plan.
- Include AGENTS.md and tracker.md diffs in task report; approved together with task.
- All official documentation lives in `docs/` and is the single source of truth.

## Restrictions
- No new dependencies without authorization.
- No modifications to architecture, data model, workflow, tech stack, or business rules without authorization.
- No modifications to official documentation without authorization.

## Validation & Commands
- `ruff check .` — lint (E/F/I/N/W, line length 100)
- `mypy .` — typecheck (strict)
- `pytest tests/` — test suite (currently 381 passing)
- Local venv runs Python 3.14.6 (3.12 unavailable).

Definition of Done:
- Run only relevant validations: lint + typecheck always when code changed; pytest only when change requires tests.
- Review official acceptance criteria in MVP Execution Plan.
- Deliver report: Objective, Modified files, Validations performed, Result, Issues encountered.
- Testing strategy: unit tests with fixtures in `tests/fixtures/`; integration tests tagged (Playwright); LLM responses mockable; data layer tested with temporary SQLite files.

## Key Documents
Documentation authority model: only **primary construction docs** are consultable (authoritative, always current). All non-primary docs were removed from the repository; never rely on deleted documentation (only git history).

| Category | Doc | Covers |
|---|---|---|
| **Primary** | Ficha técnica (per module) | Node-level module spec: flow, business rules, error codes, states — authoritative for building (`docs/diagrams/`) |
| **Primary** | DOC-13A | Detailed data model: entities, attributes, catalogs, ERD — aligned with implementation deviations |
| **Primary** | Appendix 5A | Official prefix catalog (IDs, codes) |
| **Primary** | Decision log | Approved decisions and deviations D1–D6, C2/C5, PMD-020/021, DE-LI (`docs/history/decision log.md`) |
| **Primary** | MVP Execution Plan | Build order and acceptance criteria per task |
| **Primary** | tracker.md | Current status of each phase and task |
| **Primary** | AGENTS.md (this file) | Operating contract, conventions, validation |
| **Operational** | session history.md | Per-session record, updated only by `/save` (`docs/history/session history.md`) |

Reading order: AGENTS.md → decision log → current module ficha → DOC-13A → docs referenced by the task. Do not read unnecessary documentation.

## Close gate
At every closure, run the `docs-reviewer` agent: verify the implemented changes against the primary documents (decision log, current module ficha, DOC-13A, MVP Execution Plan acceptance criteria, tracker, AGENTS.md) and detect documentation drift before validation.

## Version Control
- Develop each phase/module/significant change in a dedicated branch; use descriptive names (e.g., `modulo-1`, `docs/...`).
- Branch stays active until user explicitly requests merge to `main`; never merge without explicit authorization.

## Session History
- `/save` is the only command that updates session history, tracker, and their commit/push; runs only on user invocation — agent never executes or anticipates it.
- At session end, update `docs/history/session history.md`: one entry per OpenCode session (create/update current session number), newest first, cumulative.
- Session number is sequential (last + 1); each entry includes OpenCode session ID from local DB:
  ```bash
  sqlite3 ~/.local/share/opencode/opencode.db "SELECT id, substr(title,1,60) FROM session ORDER BY time_updated DESC LIMIT 1;"
  ```
- Entry format — three sections, short and useful for a new developer, keyword-style bullets, one line per bullet:
  - **Topics** — keyword bullets; no commit hashes, file paths, or rule numbers.
  - **Decisions** — only new or modified decisions.
  - **Status** — completed/pending phases (✅/⬜); Ruff/mypy/pytest results if changes made; active branch.
- Past detail preserved in git; never expand old entries with new information.

## Uncertainty
Never invent a solution: stop, explain the problem, and wait for a decision.
