# Session History
Chronological record of OpenCode sessions (newest first, one entry per session, ID-identified). Sessions 1–5 detail preserved in git.
Unless noted, decisions from previous sessions remain in effect.

## Sessions index
| № | Date | Session ID | Summary |
|---|---|---|---|
| 18 | 11/08/2026 | `ses_011dd31a8ffe0sUJfx0l66OpUJ` | Documentation depuration: only primary docs kept, all non-primary deleted physically; docs-reviewer optimized (single skill, git-diff scope, primary-only checks, conditional output) |
| 17 | 10/08/2026 | `ses_0133020ecffeN4R4bi4Y7MXDAF` | LinkedIn 2026 SSR login fixed (direct login, `voyager` criterion, multi-variant parsing) + `sesiones` schema migration + closure-metrics success event (240 tests) |
| 16 | 10/08/2026 | `ses_0133020ecffeN4R4bi4Y7MXDAF` | Sub-fase 4.5: terminal closure node + full-flow orchestrator implemented, validated, and audited CONFORME (229 tests) |
| 15 | 09/08/2026 | `ses_01823c05affeFQbFrKubp332mC` | Skills inventory reviewed; review-against-documentation fully rewritten; /save authorized full commit of worktree |
| 14 | 09/08/2026 | `ses_01bcc78adffemcqFEiZxT52Eli` | Sub-fase 4.4: capture/registration nodes implemented, audited, and post-audit fixes applied (FK-free schema, name columns, upsert tests) |
| 13 | 08/08/2026 | `ses_01be77680ffeuyoKct4Qrfx1GG` | Repo sync to `fase-4`; new `/save` section with general git commit and push guidance |
| 12 | 08/08/2026 | `ses_01c089ce2ffe9MvQT4F1pC0MJN` | Sub-fase 4.2 deep audit + post-audit fixes (credentials mapping, playwright lifecycle) |
| 11 | 08/08/2026 | `ses_01c312689ffewPDBUxLcQIRb5L` | Sub-fase 4.3: Filter search + generic register implemented and validated (171 tests) |
| 10 | 08/08/2026 | `ses_01d9bc3d2ffe0OwXiVc3Mw8NWO` | Sub-fase 4.2: Ingreso flow implemented (3 nodes) and validated (152 tests) |
| 9 | 08/08/2026 | `ses_01ebcd885ffe7UB5IsfCrylV90` | Sub-fase 4.1: INICIO node implemented and validated (123 tests), reviewer fixes applied, branch `fase-4` created |
| 8 | 07/08/2026 | `ses_021c087e1ffePrh0h4O4Zzb4BY` | Module 1 preparation: discovery scaffold (run context + LinkedIn adapter), full validation passed, build ready |
| 7 | 07/08/2026 | `ses_0234a5a0effeWIUu0hsOpfvx3L` | Module 1 (Discovery): build strategy decided node-by-node; MVP Plan Phase 4 redefined as 13-node plan |
| 6 | 01/08/2026 | `ses_041587944ffe8Ve6EeplEa9Huo` | Session History restructured; custom sub-agents created |
| 1–5 | 23–30/07/2026 | — | Project foundation, Phases 0–3, SQLite migration, prompts retested |

## Session 18 — 11/08/2026
`ses_011dd31a8ffe0sUJfx0l66OpUJ` · `fase-4`

**Topics**
- Documentation authority clarified: only primary docs are consultable when building (module ficha, decision log, data model, prefix catalog, plan, tracker, AGENTS.md)
- Docs-reviewer inefficiency diagnosed: two heavy skills loaded, full-implementation inspection, checks against retired docs, inflated output template
- Physical deletion of all non-primary documentation: design docs and retired docs removed from the repo (history preserved in git)
- Authority model simplified in AGENTS.md: single consultable category; generic close gate against primary docs replaces the DOC-01 sync gate
- Docs-reviewer optimized: one lightweight skill, git-diff scoped inspection, primary-docs-only checks, CONFORME output in ≤5 lines when no findings
- Review skill streamlined: precedence = primary docs, 3-step workflow, conditional report template
- README links updated to living documents only
- Functional inputs (requirements, decision model, data flow, error catalog, user profile) removed: future module fichas will be rebuilt from module-1 ficha + decision log + data model
- Workflow audit (checks, implementation, documentation, closure skills): read/update scope verified aligned with primary docs only; project-documentation skill adjusted to forbid consulting deleted docs and over-reading

**Decisions**
- Only primary documentation remains consultable; all non-primary docs deleted physically, never to be consulted again
- Future module fichas (2–5) are built from module-1 ficha + decision log + data model, without prior functional inputs
- Closure documentation review limited to changed files and primary documents, with conditional output
- Documentation consultation across all workflow skills scoped to primary documents only, minimum required by the task

**Status**
- Documentation depuration + reviewer optimization + workflow alignment ✅ (no code changes: ruff/mypy/pytest n/a)
- Branch: `fase-4` · /save single commit + push, no merge

## Session 17 — 10/08/2026
`ses_0133020ecffeN4R4bi4Y7MXDAF` · `fase-4`

**Topics**
- Deep-debug of LinkedIn 2026 login: page renders two copies of the form — invisible SSR residual (`autocomplete="username"`, 0×0) vs real React one (`autocomplete="username webauthn"`, visible); exact-attribute CSS selector matched only the residual → 30s fill timeout; authwall/modal hypothesis was a false lead
- Direct login: authenticated sources go straight to the Spanish login URL (search URL no longer visited first); selectors `[autocomplete^='username']:visible` + Enter submit with click fallback; form-detach wait; entry criterion verified by HTML polling tolerant to in-flight navigation
- Entry criterion switched from `global-nav` to `voyager` (feed no longer renders `global-nav`; SSR shell arrives first, `voyager` ~3.5s later)
- Multi-variant listing/detail parsing: per-page exclusive CSS variants (2026 job-card → generic anchor → classic base-search-card), href dedup, title/description fallbacks; new fixtures + adapter tests
- Two pre-existing findings fixed: session-audit insert (generic writer requires `id` column; schema migrated idempotently with id=session_id) and closure metrics (happy path wrote no events, so finalize counts showed 0/0)
- Capture success now writes `ofertas_registradas` success event; functional run COR-1957: session audit persisted, events traceable, closure `total_sucesos=2 | fuentes_procesadas=1`
- Re-visit dedup verified: re-seen offers become UPDATEs, so run-level `total_ofertas` counts only newly registered offers (7/7 of COR-1839 duplicated in COR-1957 → 0 new by design)
- Tests: 240 passing (persistence migration, `write_row` on sesiones, register-success event tests added)

**Decisions**
- LinkedIn 2026 login selectors: prefix match + `:visible`, Enter submit with click fallback — never exact-attribute match on username
- Entry success for authenticated sources: HTML polling for `voyager` on the feed, tolerant to navigation; direct login URL instead of visiting search first
- Parsing variants resolved per page by exclusivity (one variant per page, selectors never mixed)
- `sesiones` schema aligned with the generic writer (`id` PK + creation dates); migration copies legacy rows with id=session_id; session audit passes the explicit id
- Happy-path capture writes `ofertas_registradas` so closure metrics reflect the run; degraded/partial lote events unchanged
- Run `total_ofertas` counts only newly registered offers by design (upsert dedup); no semantic change

**Status**
- Login SSR fix + multi-variant parsing + both pre-existing findings ✅ (validated on real DB via COR-1957)
- Ruff 0 · mypy 0 (46 files) · pytest 240/240
- Branch: `fase-4` · /save single commit + push, no merge

## Session 16 — 10/08/2026
`ses_0133020ecffeN4R4bi4Y7MXDAF` · `fase-4`

**Topics**
- Sub-fase 4.5 implemented: terminal node Finalizar Proceso + orchestrator connecting the 13 nodes + module entry point (python -m)
- Persistence additions only (no other files touched): `actualizar_corrida`, `liberar_bloqueo` alias, 6 closure columns on `corridas`, idempotent migration
- Closure semantics: state mapping by motivo, metrics query with zero fallback, single-retry on update, best-effort event/resource-close/lock-release
- Custom Playwright closing (page/browser/instance attributes) without touching existing adapters
- Orchestrator loops: sources × filter sets, session close between sources, abort with motivo on any node error; INICIO non-ok exits without Finalizar
- Unit tests: 17 node + 13 orchestrator (mocks, temp DB end-to-end, order-of-calls tracking); full suite 229
- Read-only audit by user request: CONFORME with minor findings (metric query duplicated on close, user-specified deviations vs ficha pending D4 documentation)
- Reviewer sub-agents: code-reviewer returned empty twice; docs-reviewer flagged ficha deviations later confirmed as user-specified

**Decisions**
- Estado vocabulary defined by user: completada/sin_fuentes/abortada (reconciles the session 9 pending item; deviations vs ficha/doc to be documented as D4 in a later session)
- Termination event: tipo suceso only on completada, error otherwise; INICIO non-ok (error/concurrencia) prints and returns without Finalizar — both per user spec
- Documentation updates (tracker/ficha/DOC-13A) deferred by user during implementation; /save applies only session history + tracker status
- No commit was made during implementation; /save authorizes the single closing commit and push on `fase-4`

**Status**
- Sub-fase 4.5 ✅: closure node + orchestrator implemented and audited CONFORME
- Ruff 0, mypy 0 (44 files), pytest 229/229
- Branch: `fase-4` · committed & pushed via /save, no merge
`ses_01823c05affeFQbFrKubp332mC` · `fase-4`

**Topics**
- Skills inventory: project skills (implementation, docs, debugging, review, testing) vs global skills (design, SEO, data validation)
- Reviewed review-against-documentation skill: purpose, workflow, review categories, output format
- Use scope of the skill: closure/verification stage via the documentation reviewer agent
- Full rewrite of the skill: applicability, required inputs, documentation precedence hierarchy, 7-step workflow, finding categories, severity levels, mandatory rules, review output template
- /save detection of unexpected worktree changes (report deletions, DOC edits) — user authorized committing everything

**Decisions**
- Review skill now defines documentation precedence order, structured findings/severity taxonomies, and a fixed review report template
- Restricting the skill to the docs-reviewer agent only: discussed, investigated, pending user confirmation (not applied)
- /save session: full worktree commit authorized by user

**Status**
- Session: skill rewritten ✅ · no code changes (ruff/mypy/pytest n/a)
- Skill-agent restriction: ⬜ pending decision
- Branch: `fase-4` · /save full commit authorized

## Session 14 — 09/08/2026
`ses_01bcc78adffemcqFEiZxT52Eli` · `fase-4`

**Topics**
- Context recovery: AGENTS.md, MVP Plan, tracker, session history
- Sub-fase 4.4 implementation: capture nodes (`capturar_ofertas`, `registrar_ofertas`, `quedan_ofertas_por_capturar`, `quedan_sets_por_aplicar`)
- `upsert_oferta` by `id_externo_url` + `timestamp_ultima_verificacion` (+ `read_table` filters + migration)
- First upsert commit reverted on request; reimplemented with full test coverage (22 node tests)
- Second audit: FK constraint failed on capture (empty `empresa_id`/`ubicacion_id` referencing missing catalogs)
- Post-audit fixes: FK-free `ofertas` schema, `empresa_nombre`/`ubicacion_nombre` columns, idempotent migration, 5 upsert integration tests
- Docs aligned: ficha técnica NOTA + RN-02/03, DOC-13 decision D4, DOC-13A v1.4, tracker 4.4 ✅, AGENTS.md update
- Fixed pre-existing migration bug on real DB (obsolete Spanish columns)

**Decisions**
- Dedup by `id_externo_url` stays in Module 1 (upsert); documented as approved deviation over 1.0 spec
- `empresa_id`/`ubicacion_id` stored NULL in MVP; raw adapter strings kept in `empresa_nombre`/`ubicacion_nombre`; `fuente_id` stores `source_id` with no FK constraint (decision D4 2026-08-09)
- Schema migrations copy only columns present in target schema (intersection) to survive legacy DBs

**Status**
- Sub-fase 4.4 ✅: capture/registration nodes validated with audit fixes
- Ruff 0, mypy 0 (39 files), pytest 199/199
- Branch: `fase-4` · committed, no merge

## Session 13 — 08/08/2026
`ses_01be77680ffeuyoKct4Qrfx1GG` · `fase-4`

**Topics**
- Context recovery and current status summary
- Remote sync of last commit on `fase-4`
- Investigation: no documented rules for commit/push from `/save`
- Drafted general, phase-independent git commit + push section for `/save` command
- Added section to `/save` command file and pushed to `fase-4`

**Decisions**
- Place general git commit + push guidance in `/save` command (not AGENTS.md/elsewhere), close to action it governs
- Keep merges and branch pushes out of `/save`; governed by AGENTS.md Version Control rules
- Section covers: scope verification, excluded files, explicit staging, review of staged diff, conventional English commit message ≤ 72 chars, single commit per closing, push of commit with no force-push

**Status**
- Branch: `fase-4` · `/save` section added, committed & pushed (no merge); no code changes (ruff/mypy/pytest n/a)

## Session 12 — 08/08/2026
`ses_01c089ce2ffe9MvQT4F1pC0MJN` · `fase-4`

**Topics**
- Context recovery: AGENTS.md, MVP Plan, tracker, session history
- Deep audit of Sub-fase 4.2 across 11 verification sections (structure, resource lifecycle, credentials, session_id, retries, decision node, event registration, tests, cleanliness, suite, commit/tracker)
- Critical finding: credential key mismatch between node and adapter (refs vs canonical keys)
- Minor finding: playwright `finally` guard depended on shared context state (multi-source leak risk)
- Post-audit fixes implemented and validated

**Decisions**
- Credential mapping convention (MVP): `credenciales_referencia[0] → username`, `[1] → password`
- Adapter consumes canonical keys; node performs mapping (Option A over changing adapter)
- Playwright lifecycle tracked by local `playwright_activo` flag instead of context state, preventing multi-source leaks
- On success, local flag reset so `finally` does not close session intended for subsequent nodes

**Status**
- Sub-fase 4.2 post-audit fixes applied and validated
- Ruff 0, mypy 0 (37 files), pytest 172/172
- Branch: `fase-4` · committed, no merge

## Session 11 — 08/08/2026
`ses_01c312689ffewPDBUxLcQIRb5L` · `fase-4`

**Topics**
- Sub-fase 4.3 complete: search nodes ("Aplicar filtros básicos", "¿Se encontraron ofertas?", "Registrar suceso/error")
- Set iteration (indices) with reset and marking as processed when source changes
- Adapter search with filters
- Conditional retries (source unavailable / timeouts) and retry counts
- Search_result contract fixing (`exito` vs `ok` literal)
- Generic event node that reads search_result or entry_result, typed to suceso/error, via shared/persistence
- Event logging of failures/successes not aborted
- Discovery of errors in the reviewer and final tests

**Decisions**
- Search filters unsupported (`filtros_no_aplicables`) fail set completely instead of silently continuing without filters
- Success path of retries validated: successful retries count against actual attempts (`numero_de_intentos`)
- Event search scoped to current source (search_result of previous source inhibited)
- Logging of a write failure must still continue (registered node)
- Playwright mocked in node tests to avoid async/event-loop issues

**Status**
- Phase 4.3 ✅: Filter search + generic register nodes done and validated
- Ruff 0, mypy 0 (37 files), pytest 171/171
- Branch: `fase-4` · committed

## Session 10 — 08/08/2026
`ses_01d9bc5d2ffe0OwXiVc3MrXgBo` · `fase-4`

**Topics**
- Sub-fase 4.2 complete: "Entrar a la fuente", "¿Ingreso exitoso?" and "Registrar evento" nodes
- Integration with LinkedInAdapter (navigation, auth, success criteria)
- Conditional retry logic for source unavailability and timeouts
- session_id generation (SES-NNNN) and handle_sesion management (Playwright page)
- Event logging for both successes and failures in persistence layer
- Validation of entry result consistency

**Decisions**
- Browser instance created per attempt to ensure clean state
- Playwright instance started manually to prevent page closure on successful node exit

**Status**
- Phase 4.2 ✅: Platform entry nodes done and validated
- Ruff 0, mypy clean (logic), pytest 152/152
- Branch: `fase-4`

## Session 9 — 08/08/2026
`ses_01ebcd885ffe7UB5IsfCrylV90` · `fase-4`

**Topics**
- Sub-fase 4.1 complete: INICIO node + 3 control nodes (existence, iteration, selection) of Discovery flow (technical sheet v1.0/v1.3)
- Branch `fase-4` created from `main`; Phase 4 work restricted to it, no merge without authorization
- `run_context.py`: `permitir_vacio` parameter; new context fields (`fuente_corriente`, `posicion_fuente_corriente`, `motivo_terminacion`, `timestamp_terminacion`)
- `shared/persistence.py`: atomic lock acquisition (`BEGIN IMMEDIATE`), `forzar` overwrite with CAS, `probe_write`, `write_corrida`, `write_evento`, public `umbral_obsolescencia_minutos`
- `control_fuentes.py`: 3 nodes, pure context evaluation, ERR-01..03 local codes, termination reasons fixed on context (sin_fuentes/corrida_completada), traceability run_id+source_id
- Reviewer cycle: blockers resolved, minors fixed (iterador range validation, run_id empty → Loguru-only, atomic mutation docs)
- Validation: 136 tests passing, ruff 0, mypy 0

**Decisions**
- INICIO validates `source_id`/`nombre` required to discard with ERR-12 instead of aborting with ERR-10
- `acquire_lock` rework: `BEGIN IMMEDIATE` for atomic first acquisition; CAS (`UPDATE ... WHERE run_id`) for `forzar` branch
- Authorities exception in AGENTS.md: `modules/discovery/` uses Spanish identifiers for domain concepts (consistent with `run_context.py` precedent)
- `corridas.estado` 5 values vs DOC-13A termination-reason reconciliation pending before Finalizar Proceso node (documented, not resolved)

**Status**
- Phase 4.1 ✅: INICIO + 3 control nodes done and validated
- Ruff 0, mypy 0 (31 files), pytest 136/136
- Branch: `fase-4`

## Session 8 — 07/08/2026
`ses_021c087e1ffePrh0h4O4Zzb4BY` · `modulo-1`

**Topics**
- Context recovery: preparation plan phases 1–5 completed and committed, phase 6 scaffolded (run context + LinkedIn adapter)
- Fase 6 of preparation plan: discovery scaffold with 4 methods, 8 new conftest fixtures, 20 new tests, HTML fixtures
- Code-review fixes from reviewers: entry criterion enforced as mandatory in validated config and base URL derived from source URL
- Documentation correction: `credenciales_no_disponibles` registered in official `codigo_motivo` catalog as non-retryable config error, outside retry groups A/B
- Fase 7 validation finished: full checklist vs docs + suite green (102/102), verdict "READY TO BUILD PHASE 4"
- Git state verified: working tree clean at session start, all phase work already committed and pushed
- Session history updated (this entry)

**Decisions**
- `credenciales_no_disponibles` → ER-CFG, non-retryable, belongs neither to retry Group A nor B (occurs before channel opens, deterministic at step 2 of "Entrar a la fuente")
- Node construction of Phase 4 starts only after explicit user confirmation
- Reviewer minor findings stay documented as-is pending future authorization (adapter error class outside BaseError hierarchy)

**Status**
- Phases 0–3 ✅; Module 1 preparation plan phases 1–7 ✅ (validation verdict "ready to build"); Phase 4 node construction ⬜ pending approval
- Ruff 0, mypy 0 (27 files), pytest 102/102
- Branch: `modulo-1`

## Session 7 — 07/08/2026
`ses_0234a5a0effeWIUu0hsOpfvx3L` · `modulo-1`

**Topics**
- Context recovery: AGENTS.md, MVP Plan, tracker, session history
- Analysis of Module 1 flow diagram + technical sheet (13 canonical node specs)
- Build strategy discussion: node-by-node vs. vertical-phase A-E approach
- Chosen node-by-node build for Phase 4 (13 nodes, flow order, one validated node per step)
- MVP Execution Plan Phase 4 rewritten: generic 8-step plan replaced by 13-node build plan
- Gaps identified vs. current infra: rework risk contained via per-node work cycle

**Decisions**
- Phase 4 (Module 1) built node-by-node, strictly in flow order, each node through its own full work cycle (analysis → plan → implementation → validation → close)
- The 6 decision nodes act as contract validators of their immediate predecessor
- Closed/open gap decisions pending user approval before execution (no implementation done)

**Status**
- Phases 0–3 ✅, Phase 4 ⬜ (plan redefined as 13 nodes; no implementation yet)
- No code changes this session → Ruff/mypy/pytest n/a
- Branch: `modulo-1`

## Session 6 — 01/08/2026
`ses_041587944ffe8Ve6EeplEa9Huo` · `modulo-1`

**Topics**
- Session identification via OpenCode local database
- Session History restructured: managed by session number, newest first
- Past sessions (1–5) consolidated into a single entry; detail preserved in git
- 5 custom sub-agents created: docs-reviewer, code-reviewer, docs-updater, test-writer, playwright-debugger

**Decisions**
- Session History managed by session number, newest first
- Sessions 1–5 consolidated; old format remains recoverable in git
- One entry per OpenCode session (not per calendar day)
- Sub-agents have a single specific function; reviewers are read-only; they support project construction, not the product automation

**Status**
- Phases 0–3 ✅, Phase 4 ⬜
- Ruff 0, mypy 0, pytest 48/48
- Branch: `modulo-1`

## Sessions 1–5 — 23–30/07/2026 (consolidated)

**Topics**
- Project foundation: repository, directory structure, config, git + GitHub, MVP plan (9 phases)
- Phases 0–3 completed: shared services, profile model, AI service, decision engine, state machine, 5 prompts (PRM-001..005)
- Persistence migrated from Excel to SQLite (7 tables + ID sequences)
- Code fully translated to English; data layer kept in Spanish
- Architecture review: 7 offer states, cloud-primary AI strategy, MVP persistence scope, data dictionary + ERD
- Prompts retested end-to-end against `gemma4:31b-cloud`; mandatory Spanish output enforced
- Branch `modulo-1` created for Phase 4 (Opportunity Discovery)

**Decisions still in effect**
- LinkedIn is the only source for the MVP
- SQLite persistence; data layer (models, persistence, DB) in Spanish
- Cloud-primary AI strategy with configurable local fallback
- Offer lifecycle unified to 7 states
- Prompts must always instruct Spanish output (generated content is stored data)

**Status (end of 30/07/2026)**
- Phases 0–3 ✅, Phase 4 ⬜
- Ruff 0, mypy 0, pytest 48/48
- Branch: `modulo-1`
