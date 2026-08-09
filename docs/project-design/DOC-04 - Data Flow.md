# Document 4 – Data Flow (Optimized)

## 1. Purpose

Defines the official data flow model for the job search automation: how information is ingested, transformed, validated, stored, queried, and preserved across the entire job-posting lifecycle. Ensures consistency, integrity, traceability, and availability at every stage.

Serves as the mandatory reference for design, implementation, validation, and evolution of the project's data architecture. All components that generate, consume, transform, store, query, or update information shall comply with this document.

Cross-references: Functional Requirements, Non-Functional Requirements, Decision Model, Project Glossary.

---

## 2. Data Flow Principles

| ID | Principle | Rule |
|----|-----------|------|
| DFP-001 | Integrity | No transformation may alter, remove, or corrupt original data unless a documented business rule explicitly authorizes it. |
| DFP-002 | Complete Traceability | Every datum must be traceable from origin to final state: transformations, validations, decisions, state changes, persistence. |
| DFP-003 | Controlled Flow | Data moves only through processes defined in the functional workflow. Undocumented movements, transformations, or access are prohibited. |
| DFP-004 | Consistency | No incompatible versions, contradictory records, or unjustified differences across modules. |
| DFP-005 | Prior Validation | All data from external sources or generated during processing must pass validation before use. No component may assume validity without verification. |
| DFP-006 | Separation of Responsibilities | Acquisition, transformation, validation, evaluation, storage, and querying remain conceptually independent. Each stage performs only its own operations. |
| DFP-007 | Controlled Persistence | Information needed for operation, traceability, auditing, or reprocessing is stored via defined architectural mechanisms. Both original and derived data are preserved when applicable. |
| DFP-008 | Reproducibility | Same inputs + same rules/configurations = same outputs. The flow is deterministic. |
| DFP-009 | Technology Independence | The data flow definition is independent of language, database, provider, or tool. |
| DFP-010 | Controlled Evolution | Every modification is documented in advance and preserves compatibility with all official documentation. New elements shall not alter existing behavior without documented justification. |
| DFP-011 | Availability | Information remains available to requiring processes throughout its lifecycle, respecting access, persistence, and retention rules. |
| DFP-012 | Uniqueness | Each datum has a single source of truth. Inconsistent copies are prohibited when an official query/reconstruction mechanism exists. |
| DFP-013 | Duplicate Minimization | Avoid generating duplicates. Where functional redundancy exists, maintain synchronization and traceability between records. |
| DFP-014 | Original Data Protection | Source data is preserved unmodified. Normalization/enrichment/transformation operates on derived structures only. |
| DFP-015 | Workflow Compliance | All information movement complies with the functional workflow, job-posting lifecycle, Decision Model, and defined states. Data cannot be used in processes incompatible with its current state. |

---

## 3. Architecture

The data flow is a cross-cutting, technology-independent component used by every module. It follows a sequential workflow: **ingestion → validation → transformation → persistence → consumption → updating → preservation**.

### 3.1 Components

| ID | Component | Responsibilities |
|----|-----------|-----------------|
| DFA-001 | Data Sources | All authorized origins: job platforms, user config, professional profile, business rules, system configs, historical info, user decisions. Every datum must identify its origin before entering the flow. |
| DFA-002 | Ingestion | Receive info, identify origin, associate basic metadata, prepare for validation. **Does not modify content.** |
| DFA-003 | Validation | Verify integrity, structure, consistency, completeness, and process compatibility. **Does not transform**; only determines suitability. |
| DFA-004 | Transformation | Normalize formats, complete derived info, structure data, generate intermediates, prepare for functional processes. **Always preserves original data.** |
| DFA-005 | Persistence | Store original data, transformed data, states, decisions, events, history. |
| DFA-006 | Consumption | Retrieve info, verify availability, provide only data required per process, guarantee consistency of queried info. |
| DFA-007 | Updates | Update states, incorporate results, record evaluations, associate documents, synchronize structures. **Every update preserves history.** |
| DFA-008 | Logging & Traceability | Record at minimum: origin, transformations, validations, consuming processes, state changes, decisions, timestamps, responsible party. |

### 3.2 Conceptual Flow (mandatory sequence)

1. Receive from authorized source → 2. Identify origin → 3. Validate → 4. Transform/normalize → 5. Store → 6. Make available to authorized modules → 7. Update during processing → 8. Record every operation for traceability/auditing.

### 3.3 Scope

**In scope:** Incorporating, validating, transforming, storing, making available, maintaining consistency, recording history, preserving traceability, facilitating authorized reprocessing.

**Out of scope:** Functional/strategic decisions, Decision Model business rules, modifying the user's profile, determining priorities/classifications, executing non-information-management processes.

---

## 4. Inputs

Every input must: originate from an authorized source; be uniquely identifiable; preserve origin info; pass validation before use; preserve integrity; be compatible with the current workflow state; remain available for audits/reprocessing; comply with security, traceability, and persistence rules.

| ID | Input | Contents (non-exhaustive) |
|----|-------|--------------------------|
| DFI-001 | Job Posting Info *(primary input)* | Title, company, description, responsibilities, requirements, benefits, salary, work arrangement, location, employment type, publication date, source platform, URL, identifiers. |
| DFI-002 | Professional Profile | Experience, technical/professional skills, education, certifications, languages, preferences, salary expectations, work arrangement, location, target/restricted companies. |
| DFI-003 | System Configuration | General settings, execution parameters, module configs, processing frequencies, workflow configs, operational variables. |
| DFI-004 | Business Rules | Evaluation, acceptance, rejection, prioritization rules; thresholds; constraints; special cases; exceptions. |
| DFI-005 | Historical Info | Posting/evaluation/decision/state history, generated documents, execution logs, metrics. |
| DFI-006 | User Decisions | Approvals, manual rejections, authorized reprocessing, priority changes, profile updates, config/rule modifications. |
| DFI-007 | Automation-Generated Data | Intermediate results, normalized data, classifications, scores, analyses, documents, processing/operational states. May become input for subsequent processes. |

---

## 5. Transformations

All transformations execute only after successful validation.

| ID | Rule |
|----|------|
| DTF-001 | Original data fully preserved. Modifications occur on derived structures only. |
| DTF-002 | Normalize: dates, times, locations, work arrangements, employment types, salaries, currencies, identifiers, text structures. |
| DTF-003 | Organize into uniform internal structures, consistent regardless of source. |
| DTF-004 | Enrichment (derived fields, preliminary classifications, internal IDs, metadata, relationships) is permitted when allowed by project rules. Never replaces original info. |
| DTF-005 | Remove functional redundancies only when no relevant info or traceability is lost. |
| DTF-006 | Associate metadata: timestamp, source, internal ID, processing version, initial state, traceability info. |
| DTF-007 | Generate derived structures for evaluations, analyses, reports, history, auditing, processing management. Maintain relationship with origin data. |
| DTF-008 | Output must be compatible with consuming modules and official interfaces. |
| DTF-009 | Deterministic and fully reproducible. |
| DTF-010 | Log every transformation: data ID, transformation applied, timestamp, responsible party, result, relationship to original. |

---

## 6. Validations

No data advances to the next stage without passing validation, unless a documented rule authorizes handling as a special case/exception.

| ID | Validation |
|----|-----------|
| DV-001 | **Source:** Origin must be authorized and verifiable. Unidentified data is rejected. |
| DV-002 | **Integrity:** No loss, alteration, or corruption during incorporation. |
| DV-003 | **Structure:** Must match expected structure per info type. Incompatible structures follow exception-handling rules. |
| DV-004 | **Required Info:** All mandatory fields present when required. Missing fields follow defined business rules. |
| DV-005 | **Consistency:** No contradictory data preventing reliable interpretation. |
| DV-006 | **Compatibility:** Data must match current lifecycle state and the intended functional process. Incompatible-stage data is rejected. |
| DV-007 | **Duplicates:** Detect per equivalent-posting management rules. |
| DV-008 | **Relationships:** Verify Posting ↔ History, Evaluations, States, Documents, Decisions remain valid. |
| DV-009 | **Pre-Consumption:** Before use, verify info remains valid. Obsolete/incomplete/incompatible data triggers defined rules. |
| DV-010 | **Logging:** Record data ID, validation executed, result, timestamp, responsible party, action on failure. |

---

## 7. Outputs

Every output maintains its relationship with origin data and complies with integrity, traceability, and persistence rules.

| ID | Output | Contents |
|----|--------|----------|
| DFO-001 | Structured Job Posting | Validated info, normalized fields, internal IDs, metadata, internal relationships. Primary source for subsequent processes. |
| DFO-002 | Evaluation Results | Scores, compatibility levels, priorities, classifications, partial/final results, justifications. |
| DFO-003 | Derived Information | Enriched data, calculated fields, relationships, indicators, metadata. Always linked to original. |
| DFO-004 | Processing States | Lifecycle state, operational state, update date, responsible party, transition history. |
| DFO-005 | Application Resources | Strategic analyses, organized info, documents, resources. Each linked to its posting. |
| DFO-006 | Query Information | Full history, current state, evaluation results, documents, decisions, metrics. |
| DFO-007 | Operational Records | Events, logs, validations, transformations, errors, warnings, metrics, automated/user decisions. |

---

## 8. Persistence

| ID | Rule |
|----|------|
| DP-001 | Original source data preserved in full. Never deleted or overwritten by transformations. |
| DP-002 | Derived info stored when needed for operation, traceability, auditing, or reprocessing. Always linked to origin. |
| DP-003 | Complete posting history preserved: state changes, validations, transformations, evaluations, decisions, reprocessing, relevant events. |
| DP-004 | Configurations stored to reproduce behavior. Critical config changes preserve history. |
| DP-005 | Documents/analyses/resources linked to posting; origin, version, and generation time identifiable. |
| DP-006 | Operational records (events, errors, warnings, metrics, validations, transformations, decisions) stored for full execution reconstruction. |
| DP-007 | All relationships preserved: Posting ↔ History, Evaluations, States, Documents, Decisions, Records. No relationship lost during storage. |
| DP-008 | Stored info available to authorized processes during retention period. Queries do not alter content. |
| DP-009 | Reuse previously persisted valid info before regenerating. Reduces unnecessary processing and duplication. |
| DP-010 | Log every significant storage/update: data ID, operation, timestamp, responsible party, result, final state. |

---

## 9. Data States

States describe the condition of *information itself* (not the posting lifecycle/operational states defined elsewhere). A datum exists in only one active state at a time. Every transition is logged. No data may be used in a process incompatible with its state.

| ID | State | Characteristics |
|----|-------|----------------|
| DS-001 | **Received** | Origin identified; original preserved; pending validation; unavailable for functional processes. |
| DS-002 | **Validated** | Integrity, structure, consistency verified; available for transformation. |
| DS-003 | **Transformed** | Standardized format; derived info generated; original preserved; available for functional processes. |
| DS-004 | **Persisted** | Available for querying, auditing, reprocessing; history preserved. |
| DS-005 | **In Use** | Associated with a functional process; controlled consumption; protected against incompatible modifications. |
| DS-006 | **Updated** | History updated; relationships preserved; new version recorded; available for subsequent processes. |
| DS-007 | **Historical** | Not current version; not deleted; linked to current version; available for historical queries and authorized reprocessing. |
| DS-008 | **Archived** | Processing completed; queryable; no operational modifications; preserved per retention policies. |
| DS-009 | **Inconsistent** | Integrity/structure/consistency/compatibility issues; processing suspended; pending resolution; unavailable for consumption. |
| DS-010 | **Obsolete** | Replaced by newer version; not used as current source; preserved for traceability; linked to replacing version. |

---

## 10. Traceability

All info managed by the data flow must maintain evidence to completely reconstruct its history.

| ID | Requirement |
|----|------------|
| DFT-001 | Unique, immutable identifier per datum, unchanged across transformations, updates, reprocessing. |
| DFT-002 | Record origin: source, timestamp, source ID (if available), incorporating process. |
| DFT-003 | Log every transformation: original info, transformation applied, result, timestamp, responsible party. |
| DFT-004 | Log every validation: validation applied, result, rule used, action taken, timestamp. |
| DFT-005 | Log data consumption: which components consumed what and for what purpose. |
| DFT-006 | Log every update: previous state, resulting state, modified info, timestamp, responsible party, justification. |
| DFT-007 | Complete history preserved; never deleted or overwritten during posting lifecycle. |
| DFT-008 | Recorded info sufficient for full reconstruction: entry, validations, transformations, consuming processes, updates, final state. |
| DFT-009 | Audit info available throughout retention period. Audit queries do not modify data or affect operations. |
| DFT-010 | Associate info with current version of rules, configs, and processes to enable historical reproduction after evolution. |

---

## 11. Integrity & Consistency

Preserved from incorporation through final retention.

| ID | Rule |
|----|------|
| DIC-001 | No process may alter, remove, or corrupt info unless a documented rule authorizes it. |
| DIC-002 | Cross-module consistency: no incompatible differences in data representing the same info. |
| DIC-003 | Single official representation per datum. Derived/functional copies linked to official source. |
| DIC-004 | Preserve all relationships: Posting ↔ Original, Transformed, History, Evaluations, Decisions, Documents, Operational Records. |
| DIC-005 | Temporal consistency: every update recorded chronologically. |
| DIC-006 | Inconsistent info halts processing until validation/special-case/exception rules are applied. No results from unverified info. |
| DIC-007 | Updates preserve history; no loss of previously recorded data. |
| DIC-008 | Reprocessing maintains consistency with existing history; no contradictions between versions. |
| DIC-009 | Integrity/consistency checks may execute at any stage without altering data content. |
| DIC-010 | Log every integrity/consistency incident: data ID, type, description, timestamp, action, result, responsible party. |

---

## 12. Reprocessing

Every reprocessing requires a documented business rule or explicit user authorization (per Decision Model). Arbitrary reprocessing is prohibited.

| ID | Rule |
|----|------|
| RM-001 | Authorization mandatory (documented rule or user decision). |
| RM-002 | Never delete, overwrite, or alter existing info. New info preserves existing history. |
| RM-003 | Reuse valid persisted data before regenerating. |
| RM-004 | Revalidate info under current system conditions. |
| RM-005 | Recalculate only affected derived elements; preserve valid ones. |
| RM-006 | Update all relationships (original, derived, documents, evaluations, history). |
| RM-007 | Log as new event; preserve all previous executions fully. |
| RM-008 | Post-reprocessing consistency check against: workflow, Decision Model, business rules, current posting state, previously recorded info. |
| RM-009 | Log: posting ID, reason, reused info, recalculated info, timestamp, responsible party, result. |
| RM-010 | Resulting info re-enters the data flow complying with all validation, persistence, traceability, and consistency rules. |

---

## 13. Constraints

| ID | Constraint |
|----|-----------|
| DFC-001 | Only authorized, identifiable sources. |
| DFC-002 | Original source data never modified, deleted, or overwritten. Transformations on derived structures only. |
| DFC-003 | No information loss. Any authorized deletion is documented with history preserved. |
| DFC-004 | Modules use only validated info (or info authorized via special-case/exception rules). |
| DFC-005 | All movement follows the official functional workflow. No out-of-sequence or incompatible-stage processing. |
| DFC-006 | Every operation preserves evidence for full data-journey reconstruction. |
| DFC-007 | Avoid unnecessary duplication. Functional copies maintain synchronization with official source. |
| DFC-008 | Centralized configuration management. No incompatible or distributed configs. |
| DFC-009 | Behavior independent of language, database, provider, service, or tool. |
| DFC-010 | Every modification preserves compatibility with: Glossary, Functional/Non-Functional Requirements, Decision Model, Functional Workflow, Posting Lifecycle, all official docs. Breaking changes require prior documentation and approval. |

---

## 14. Acceptance Criteria

The data flow is approved when objective evidence (testing, documentation review, operational evidence) demonstrates compliance with all criteria below.

| ID | Criterion |
|----|----------|
| DAC-001 | Info incorporated only from authorized, identified sources. |
| DAC-002 | All info passes validations or is handled per documented special-case/exception rules. |
| DAC-003 | Transformations produce consistent, reproducible, compatible structures. Original data intact. |
| DAC-004 | All required info persisted per this document's rules. |
| DAC-005 | States transition only per workflow and project rules. No inconsistent/incompatible states. |
| DAC-006 | No unauthorized loss, alteration, or corruption of data. |
| DAC-007 | Cross-module consistency; no incompatible shared-data differences. |
| DAC-008 | Reprocessing preserves history, reuses valid info, maintains consistency. |
| DAC-009 | Full traceability: origin, validations, transformations, consuming processes, updates, final state. |
| DAC-010 | Every significant operation justifiable through recorded evidence. Sufficient for technical and functional audits. |
| DAC-011 | Same inputs + same rules/configs/version = same results. |
| DAC-012 | Full alignment with Glossary, Functional/Non-Functional Requirements, Decision Model, Workflow, Lifecycle, all official docs. |
| DAC-013 | New sources/transformations/validations/processes incorporable without affecting existing components (unless documented and approved). |
| DAC-014 | Technology replacement does not modify data flow rules. |
| DAC-015 | Full compliance = all above criteria verifiable. |

**General acceptance:** All managed information must be complete, consistent, reproducible, traceable, auditable, sourced from authorized origins, and compatible with all official project documentation.

---

## 15. Module 1: Opportunity Discovery – Data Flow

### DFT-M1-001. Run Orchestration

Each execution is a **run** (`corrida`) with a unique `run_id`. The run moves linearly through 13 nodes within a single execution context (the only interface between nodes; see INICIO §1.12). Every record is anchored to `run_id` (RN-01).

| # | Node | Type | Delivered Contract |
|---|------|------|--------------------|
| 1 | INICIO | Process | Instantiated run + full execution context (`run_id`, raw config, validated global config, opened connections, acquired lock, filtered source list) |
| 2 | ¿Existe al menos una fuente/plataforma configurada? | Decision | `lista_fuentes` non-empty, or termination motive `sin_fuentes` |
| 3 | ¿Quedan fuentes por procesar en esta corrida? | Decision | `fuente_pendiente` exists, or termination motive `corrida_completada` |
| 4 | Seleccionar la siguiente fuente pendiente | Process | Current `source_id` + access parameters + filter sets |
| 5 | Entrar a la fuente seleccionada | Process | `entry_result` (+ `session_id` on success) |
| 6 | ¿El ingreso fue exitoso? | Decision | Branch by `entry_result.estado` |
| 7 | Aplicar los filtros básicos | Process | `search_result` (one per filter set) |
| 8 | ¿Se encontraron ofertas? | Decision | Branch by `search_result.estado` + `conteo` |
| 9 | Capturar ofertas | Process | `capture_batch` + `estado_captura` + session audit write |
| 10 | Registrar ofertas capturadas en "Ofertas Totales" | Process | Transactional raw insert of the batch |
| 11 | ¿Quedan ofertas por capturar en la búsqueda actual? | Decision | `capture_batch` and `estado_captura` of next page |
| 12 | ¿Quedan sets de filtros por aplicar en esta fuente? | Decision | `set_indice` of next set, or next source |
| 13 | Finalizar Proceso | Terminal | Termination event + lock release + resources close |

The six decision nodes act as contract validators of their predecessor: consume the contract, validate structure, route the flow. They do **not** re-read the store or probe the platform.

### DFT-M1-002. Contracts Between Nodes

| Contract | Producer | Consumer | Contents |
|----------|----------|----------|----------|
| `entry_result` | Node 5 | Node 6 | `{estado: exito\|fallo, codigo_motivo, evidencia_acotada, numero_de_intentos}` — no sensitive data (RN-06) |
| `search_result` | Node 7 | Nodes 8, 12 | `{estado, codigo_motivo, evidencia_acotada, ofertas_primera_pagina, estado_paginacion, total_declarado, set_indice, numero_de_intentos}` (RN-09) |
| `capture_batch` | Node 9 | Node 10 | `{lote_ofertas, paginas_consumidas, capturadas_acumuladas_fuente, limite_alcanzado}` |
| `estado_captura` | Node 9 | Node 11 | `{estado, paginas, capturadas_acumuladas_fuente, limite_alcanzado}`; with `estado_paginacion` of `search_result` |

Absent or corrupt contract → run proceeds to Finalizar Proceso with state `error` (abort).

### DFT-M1-003. Logical Stores (single SQLite, D2)

All stores in `job_search.db`:

| Store | Table | Written by | Purpose |
|-------|-------|-----------|---------|
| Corrida | `corridas` | INICIO / Finalizar | Run instance + termination record, by `run_id` |
| Sesión | `sesiones` | Node 9 | Session audit (success only), by `(session_id, set_indice)` |
| Evento | `eventos` | All critical/error/success events | Events with `run_id`, `tipo` (error/suceso), `codigo`, `evidencia` |
| Bloqueo | `bloqueo` | INICIO / Finalizar | Persistable concurrency lock with obsolescence threshold |
| Oferta | `ofertas` ("Ofertas Totales") | Node 10 | Raw offer rows, full traceability, **no deduplication** (Module 2) |

### DFT-M1-004. Traceability Chain

| Field | Semantics |
|-------|-----------|
| `run_id` | Run that produced the record; mandatory in every record |
| `source_id` | Platform; present in source-related records |
| `session_id` | Platform session; present when source entry succeeded |
| `set_indice` | Filter set; present in search/capture records |

Guarantees traceability of every offer, event, session audit, and run record back to its origin run, source, session, and filter set.

---

## 16. Identifier Index

Identifiers are unique, immutable, and shall not be reused, modified, or reassigned after approval.

| Range | Category |
|-------|----------|
| DFP-001 – DFP-015 | Data Flow Principles |
| DFA-001 – DFA-008 | Architecture Components |
| DFI-001 – DFI-007 | Inputs |
| DTF-001 – DTF-010 | Transformations |
| DV-001 – DV-010 | Validations |
| DFO-001 – DFO-007 | Outputs |
| DP-001 – DP-010 | Persistence |
| DS-001 – DS-010 | Data States |
| DFT-001 – DFT-010 | Traceability |
| DIC-001 – DIC-010 | Integrity & Consistency |
| RM-001 – RM-010 | Reprocessing Management |
| DFC-001 – DFC-010 | Constraints |
| DAC-001 – DAC-015 | Acceptance Criteria |
| DFT-M1-001 – DFT-M1-004 | Module 1 Data Flow |

> **Note:** DTF prefix is used by both Data Transformations (ch. 5) and Data Flow Traceability (ch. 10). Use full identifier (chapter + code) or adopt a distinct prefix during implementation to avoid ambiguity.
