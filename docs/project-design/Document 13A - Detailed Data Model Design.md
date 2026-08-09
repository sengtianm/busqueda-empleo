# Document 13A - Detailed Data Model Design

## 1. Official Entity Inventory

Official record of all persistent entities in the job search automation data model.

| Entity | Category | Functional Domain | Description |
| --- | --- | --- | --- |
| Offer | Main | Opportunity Discovery | Job offer identified by the automation during search. |
| Source | Main | Opportunity Discovery | Origin from which a job offer is obtained. |
| Company | Main | Opportunity Discovery | Organization that publishes the job offer. |
| Location | Support | Opportunity Discovery | Geographic information associated with a job offer. |
| Processed Offer | Main | Offer Processing | Structured and normalized version of an offer after processing. |
| Initial Evaluation | Main | Initial Evaluation | Result of the initial evaluation of a job offer. |
| Detailed Evaluation | Main | Detailed Evaluation | Complete evaluation of an offer that passed the initial evaluation. |
| Generated Document | Operational | Document Generation | Documents automatically generated for an offer. |
| Application | Main | Application Management | Application process carried out for a job offer. |
| Event | Operational | Traceability | Relevant events occurring during automation processing. |
| Decision | Operational | Decision Model | Functional decisions made by the automation during offer processing. |
| Configuration | Support | Configuration | Configuration parameters used during execution. |
| Catalog | Support | References | Controlled values used by model entities. |
| Corrida | Operational | Traceability | Discovery module execution instance (run); all module records anchor to its `run_id` (RN-01). |
| Sesion | Operational | Traceability | Audit of each platform session used by the Discovery module during a run. |
| Bloqueo | Operational | Concurrency | Persistent lock guaranteeing a single active Discovery module run. |

**Scope of implemented persistence** — decisions 2026-07-30 and 2026-08-07:  
The MVP database (`job_search.db`) persists only: `secuencia_ids`, `fuentes`, `empresas`, `ubicaciones`, and `ofertas`. The Discovery module additionally defines `eventos`, `sesiones`, `corridas`, and `bloqueo` as tables in the same SQLite file (decision D2, 2026-08-07). Remaining entities are deferred to later modules. This note formalizes the implemented scope; the full inventory remains the target model.

## 2. Detailed Specification of Entities

Each entity is specified with: description/purpose, attributes, primary key, alternate keys, foreign keys, relationships, constraints, state machine, and observations. Full attribute metadata — type, requirement, defaults, domains, sensitivity, persistence, actual implementation names — is in §5.

Specification order: Offer, Source, Company, Location, Processed Offer, Initial Evaluation, Detailed Evaluation, Generated Document, Application, Event, Decision, Configuration, Catalog, Corrida, Sesion, Bloqueo.

### 2.1. Entity: Offer

**Description/purpose:** Represents each job opportunity identified during discovery. Main entity of the model. Stores original offer information before normalization, evaluation, or document generation, and preserves the official reference throughout its lifecycle.

**Attributes:** `id`, `source_id`, `company_id`, `location_id`, `company_name`, `location_name`, `source_identifier`, `run_id`, `session_id`, `set_indice`, `id_externo_url`, `timestamp_ultima_verificacion`, `url`, `title`, `original_description`, `publication_date`, `discovery_date`, `status`, `active`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `source_id → Source`; `company_id → Company`; `location_id → Location`; `run_id → Corrida`; `status → Catalog`.  
MVP capture deviation (D4, 2026-08-09): `fuente_id` is stored as a raw `source_id` string without FK constraint; `empresa_id` and `ubicacion_id` may be `NULL`.

**Relationships:** belongs to Source N:1; captured by Corrida N:1; published by Company N:1; located in Location N:1; generates Processed Offer 1:1; evaluated by Initial Evaluation 1:1; may generate Detailed Evaluation 1:0..1; may generate Generated Document 1:N; may originate Application 1:0..1; records Event 1:N; records Decision 1:N.

**Constraints:**
- Every offer belongs to a single source.
- Every offer is associated with a single company.
- The offer URL is preserved throughout its lifecycle.
- Original offer content must not be overwritten after discovery.
- Offer status follows the official state machine.
- Discovery module records new offers with status `discovered` (decision C5, 2026-08-07); other transitions belong to Processing module 2.
- `company_name` and `location_name` store raw adapter strings as `empresa_nombre` and `ubicacion_nombre` (D4).
- `id_externo_url` is an external source identifier, alias of `source_identifier`, best effort.
- Registration deduplicates by `id_externo_url` via upsert; each dedup hit refreshes `timestamp_ultima_verificacion` (D4).

**State machine:** Official offer state machine applies; detailed specification is documented in the corresponding section.

**Observations:** Entry point of the data model and main reference for all derived processing, evaluation, and application entities.

### 2.2. Entity: Source

**Description/purpose:** Represents each origin from which offers are discovered: platform, website, job portal, corporate page, or authorized means. Centralizes origin information, provenance, and source-specific characteristics.

**Attributes:** `id`, `name`, `type`, `main_url`, `description`, `active`, `query_frequency`, `last_query`, `last_update`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `type → Catalog`; `query_frequency → Catalog`.

**Relationships:** publishes Offer 1:N.

**Constraints:**
- Source name is unique.
- `main_url` uniquely identifies the source.
- `active` is a catalog attribute for external administration; Discovery does not filter sources by it at runtime (decision D1, 2026-08-07).
- Source type must be a valid official catalog value.

**State machine:** Not applicable.

**Observations:** Represents only the origin of offers; it does not store individual offer data.

### 2.3. Entity: Company

**Description/purpose:** Represents the organization responsible for publishing one or more offers. Centralizes company information and avoids duplication when the same organization publishes multiple offers or uses different sources.

**Attributes:** `id`, `name`, `normalized_name`, `website`, `linkedin`, `sector`, `size`, `description`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `sector → Catalog`; `size → Catalog`.

**Relationships:** publishes Offer 1:N.

**Constraints:**
- `normalized_name` is used to minimize duplicate companies.
- A company may be associated with multiple offers.
- A company may appear in multiple sources without generating duplicate records.
- Sector and size must use official catalog values when used.

**State machine:** Not applicable.

**Observations:** Represents only the organization offering the vacancy. The same company may publish multiple offers over time and through different sources while maintaining a single record.

### 2.4. Entity: Location

**Description/purpose:** Represents the geographic location associated with a job offer. Stores normalized location information to avoid duplication when multiple offers share the same place.

**Attributes:** `id`, `country`, `region`, `city`, `address`, `modality`, `location_type`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `modality → Catalog`; `location_type → Catalog`.

**Relationships:** is used by Offer 1:N.

**Constraints:**
- At least `country` is mandatory.
- `modality` must be a valid official catalog value.
- `location_type` must be a valid official catalog value.
- Geographic coordinates may be stored only when available and consistent with the registered location.

**State machine:** Not applicable.

**Observations:** Work modality belongs to Location because it relates to how the vacancy is performed — on-site, remote, hybrid — and enables reuse across offers.

### 2.5. Entity: Processed Offer

**Description/purpose:** Structured, normalized, and enriched version of an offer after processing. Enables evaluation, comparison, document generation, and decision-making while preserving the original offer unchanged.

**Attributes:** `id`, `offer_id`, `normalized_position`, `processed_description`, `summary`, `technical_skills`, `soft_skills`, `technologies`, `experience_level`, `education_level`, `contract_type`, `work_modality`, `salary_range`, `languages`, `benefits`, `requirements`, `responsibilities`, `processing_date`, `processing_version`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** `offer_id`.  
**Foreign keys:** `offer_id → Offer`; `experience_level → Catalog`; `education_level → Catalog`; `contract_type → Catalog`; `work_modality → Catalog`.

**Relationships:** generated from Offer 1:1; used by Initial Evaluation 1:1; may be used by Detailed Evaluation 1:0..1; serves as input for Generated Document 1:N.

**Constraints:**
- Each processed offer is associated with a single original offer.
- At most one processed offer exists per offer.
- Processed information must not replace or modify original Offer content.
- Catalog-classified values must use official project values.

**State machine:** Not applicable.

**Observations:** Basis for evaluation and document generation. Recorded deviations (PMD-020): `requisitos`, `tecnologias`, and `idiomas` are implemented as JSON lists instead of `Long Text`; `summary`, `technical_skills`, and `soft_skills` are not implemented in `shared/models.py`.

### 2.6. Entity: Initial Evaluation

**Description/purpose:** Result of the first evaluation performed on a processed offer. Determines whether the offer proceeds to detailed evaluation or is discarded, preserving decision traceability.

**Attributes:** `id`, `processed_offer_id`, `result`, `score`, `pass_threshold`, `decision`, `justification`, `evaluated_criteria`, `observations`, `evaluation_date`, `version_modelo`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** `processed_offer_id`.  
**Foreign keys:** `processed_offer_id → Processed Offer`; `result → Catalog`; `decision → Catalog`.

**Relationships:** evaluates Processed Offer 1:1; may generate Detailed Evaluation 1:0..1; records Decision 1:N; records Event 1:N.

**Constraints:**
- Each initial evaluation is associated with a single processed offer.
- At most one initial evaluation exists per processed offer.
- `result` must be a valid official catalog value.
- `decision` must correspond to the evaluation result.
- Score, threshold, and justification used for decision-making must be preserved.

**State machine:** Not applicable.

**Observations:** First objective filter. Its result determines continuation or termination of processing while preserving decision traceability.

### 2.7. Entity: Detailed Evaluation

**Description/purpose:** Result of the in-depth diagnosis performed on an offer that passed initial evaluation. Corresponds to Phase 1 — Diagnosis of the vacancy for cover letter construction. Records the analysis and the fit between the organization’s needs and the user’s professional profile.

**Attributes:** `id`, `processed_offer_id`, `resultado_organizacional`, `problema_organizacional`, `perfil_profesional_requerido`, `coincidencias_perfil`, `logica_xyz`, `hipotesis_valor`, `informacion_descartada`, `ajuste_tecnico`, `justificacion_ajuste_tecnico`, `ajuste_funcional`, `justificacion_ajuste_funcional`, `ajuste_estrategico`, `justificacion_ajuste_estrategico`, `riesgo_sobrecalificacion`, `justificacion_riesgo`, `recomendacion_final`, `justificacion_recomendacion`, `insumos_carta_presentacion`, `evaluation_date`, `version_metodologia`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** `processed_offer_id`.  
**Foreign keys:** `processed_offer_id → Processed Offer`; `riesgo_sobrecalificacion → Catalog`; `recomendacion_final → Catalog`.

**Relationships:** evaluates Processed Offer 1:1; provides inputs for Generated Document 1:N; may originate Application 1:0..1; records Decision 1:N; records Event 1:N.

**Constraints:**
- Each detailed evaluation is associated with a single processed offer.
- At most one detailed evaluation exists per processed offer.
- Only offers that passed initial evaluation may undergo detailed evaluation.
- Fit scores use a 0–10 scale.
- `riesgo_sobrecalificacion` must be an official catalog value.
- `recomendacion_final` must be an official catalog value.
- Every recorded conclusion must maintain traceability with evidence from the job offer, resume, and professional portfolio.

**State machine:** Not applicable.

**Observations:** Stores the complete Phase 1 diagnosis deliverables so later phases can consume the analysis without reconstructing it.

### 2.8. Entity: Generated Document

**Description/purpose:** Represents each document automatically produced from processing and evaluating an offer. Controls lifecycle, version history, and later retrieval.

**Attributes:** `id`, `offer_id`, `detailed_evaluation_id`, `document_type`, `document_name`, `version`, `content`, `format`, `status`, `generation_date`, `last_modified_date`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `offer_id → Offer`; `detailed_evaluation_id → Detailed Evaluation`; `document_type → Catalog`; `format → Catalog`; `status → Catalog`.

**Relationships:** generated for Offer N:1; based on Detailed Evaluation N:1; may be used in Application 1:N.

**Constraints:**
- Every document is associated with a single offer.
- Every document requires a previously completed detailed evaluation.
- Document type, format, and status must be valid official catalog values.
- Each document version must preserve traceability.

**State machine:** Official document-management state machine applies; detailed specification is documented in the corresponding section.

**Observations:** Manages all documents independently of type, supporting future document types without structural changes.

### 2.9. Entity: Application

**Description/purpose:** Represents the process through which the user applies to an offer using generated documents. Records and manages the complete application lifecycle up to the final selection result.

**Attributes:** `id`, `offer_id`, `main_document_id`, `application_date`, `application_channel`, `status`, `company_response`, `response_date`, `next_action`, `next_action_date`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `offer_id → Offer`; `main_document_id → Generated Document`; `application_channel → Catalog`; `status → Catalog`.

**Relationships:** corresponds to Offer N:1; uses Generated Document N:1; records Event 1:N; may record Decision 1:N.

**Constraints:**
- Every application is associated with a single offer.
- Every application uses at least one automation-generated document.
- Application channel and status must be valid official catalog values.
- Every application status modification must preserve traceability.

**State machine:** Official application-process state machine applies; detailed specification is documented in the corresponding section.

**Observations:** Tracks the complete application process, not only submission, including evolution and closure.

### 2.10. Entity: Event

**Description/purpose:** Represents each relevant fact occurring during automation execution: action, state change, process execution, error, or occurrence preserved for traceability, auditing, and diagnostics.

**Attributes:** `id`, `run_id`, `source_id`, `session_id`, `set_indice`, `offer_id`, `tipo`, `codigo`, `evidencia`, `event_type`, `affected_entity`, `entity_id`, `action`, `description`, `result`, `origin`, `context`, `event_date`, `creation_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `offer_id → Offer`; `run_id → Corrida`; `source_id → Source`; `event_type → Catalog`; `tipo → Catalog`; `action → Catalog`; `result → Catalog`; `origin → Catalog`.

**Relationships:** records events of Offer N:1; anchored to Corrida N:1; may be associated with Decision N:0..1; may record Application N:0..1.

**Constraints:**
- In module 1, every event must be associated with a `run_id`.
- `offer_id` is required only when the event belongs to a specific offer.
- Every event must record the exact moment it occurred.
- Every module 1 event must record `tipo` — `error` or `suceso` — and, when applicable, `codigo` from the Discovery module technical sheet.
- `event_type`, `action`, `result`, and `origin` must use valid official catalog values.
- Events cannot be deleted once recorded.
- Events must be preserved to guarantee traceability.

**State machine:** Not applicable.

**Observations:** Chronological history of the automation. In Discovery module 1, events additionally record origin run `run_id`, typology `tipo`, and business `codigo` (`ERR-nn`, `EVT-nn`).

### 2.11. Entity: Decision

**Description/purpose:** Represents each decision made by the automation during offer processing after applying business rules, evaluation criteria, or analysis processes. Preserves reasoning and traceability.

**Attributes:** `id`, `offer_id`, `stage`, `decision_type`, `decision`, `justification`, `evidence`, `confidence`, `origin_component`, `decision_date`, `observations`, `creation_date`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `offer_id → Offer`; `stage → Catalog`; `decision_type → Catalog`; `origin_component → Catalog`.

**Relationships:** records decisions of Offer N:1; may originate Event 1:N; may be associated with Initial Evaluation N:0..1; may be associated with Detailed Evaluation N:0..1; may influence Application N:0..1.

**Constraints:**
- Every decision is associated with an offer.
- Justification is mandatory.
- Evidence used to support the decision must be preserved.
- Stage, decision type, and origin component must use valid official catalog values.
- Decisions cannot be deleted once recorded.

**State machine:** Not applicable.

**Observations:** Formal record of automation decisions: what was decided, why, with what evidence, and at what stage.

### 2.12. Entity: Configuration

**Description/purpose:** Represents parameters controlling automation behavior during execution without modifying implementation.

**Attributes:** `id`, `category`, `name`, `description`, `value`, `data_type`, `default_value`, `required`, `editable`, `active`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** `name`.  
**Foreign keys:** `category → Catalog`; `data_type → Catalog`.

**Relationships:** uses values from Catalog N:1.

**Constraints:**
- Parameter name is unique within the system.
- Every parameter belongs to a catalog-defined category.
- `data_type` must be a valid catalog value.
- Stored value must be compatible with the defined data type.
- Required parameters must always have a valid value.

**State machine:** Not applicable.

**Observations:** Decouples automation logic from operational values, enabling adaptation without changing the data model or code.

### 2.13. Entity: Catalog

**Description/purpose:** Represents controlled value sets used by model entities to normalize information, prevent inconsistent values, and maintain reference lists.

**Attributes:** `id`, `catalog_name`, `code`, `name`, `description`, `order`, `active`, `observations`, `creation_date`, `update_date`.

**Primary key:** `id`.  
**Alternate keys:** `catalog_name + code`.  
**Foreign keys:** Not applicable.

**Relationships:** used by Offer, Source, Company, Location, Processed Offer, Initial Evaluation, Detailed Evaluation, Generated Document, Application, Event, Decision, and Configuration — 1:N each.

**Constraints:**
- Each `catalog_name + code` combination is unique.
- Inactive values cannot be used in new records.
- Codes must remain stable to preserve compatibility.
- Physical deletion of values used by other entities is not permitted.

**State machine:** Not applicable.

**Observations:** Central repository for controlled values, including but not limited to: offer statuses, source types, work modalities, contract types, experience levels, education levels, business sectors, company sizes, document types, document statuses, application statuses, event types, decision types, configuration categories, and future controlled value sets.

### 2.14. Entity: Corrida

**Description/purpose:** Execution instance (run) of the Discovery module. Created at startup, acquires the persistent lock, processes sources, and ends with a termination motive. Every module record anchors to its `run_id`.

**Attributes:** `id`, `run_id`, `start_timestamp`, `end_timestamp`, `estado`.

**Primary key:** `id`.  
**Alternate keys:** `run_id` — unique.  
**Foreign keys:** `estado → Catalog`.

**Relationships:** captures Offer 1:N; anchors Event 1:N; registers Sesion 1:N; protected by Bloqueo 1:0..1.

**Constraints:**
- `run_id` is unique within the system.
- Every record generated by the module — errors, success events, sessions, offers — must reference its `run_id`.

**State machine:** Run statuses and transitions are defined by the Discovery module technical sheet — INICIO and FINALIZAR PROCESO nodes.

**Observations:** Physical table: `corridas` (decision D2, 2026-08-07).

### 2.15. Entity: Sesion

**Description/purpose:** Audit record of a platform session successfully established by the Discovery module. Records essential audit data only; it does not store credentials, tokens, or cookies.

**Attributes:** `id`, `session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`.

**Primary key:** `id`.  
**Alternate keys:** `(session_id, set_indice)` per source.  
**Foreign keys:** `run_id → Corrida`; `source_id → Source`.

**Relationships:** registered by Corrida N:1; established on Source N:1.

**Constraints:**
- A session record is created only after successful entry (decision D3); failed attempts are reported as events, not sessions.
- Sessions record only essential audit fields.

**State machine:** Not applicable.

**Observations:** The technical sheet mentions additional audit fields — e.g., `conteo_primera_pagina`, `hay_mas_paginas`, `coherencia`, `estado_auditoria`; the MVP limits itself to essential fields per decision D3.

### 2.16. Entity: Bloqueo

**Description/purpose:** Persistent concurrency lock for the Discovery module: at most one active run at a time.

**Attributes:** `id`, `run_id`, `timestamp`, `umbral_obsolescencia`, `estado`.

**Primary key:** `id`.  
**Alternate keys:** None.  
**Foreign keys:** `run_id → Corrida`.

**Relationships:** protects Corrida 1:0..1.

**Constraints:**
- At most one record with `estado = activo` per module.
- If an active lock’s `timestamp` is older than `umbral_obsolescencia`, a new run may take over the lock as obsolete.

**State machine:** Not applicable.

**Observations:** `umbral_obsolescencia` is centralized in the system configuration file; no hardcoded values.

## 3. Catalogs and Reference Tables

Catalogs are controlled value sets used through foreign keys to guarantee consistency, integrity, and normalization.

**Deferral** — decision 2026-07-30: the Catalog entity is not implemented in the MVP. Current implementation — `shared/models.py`, `shared/persistence.py` — stores catalog values as free text. Formal Catalog entity adoption is deferred to modules introducing traceability — Modules 2–3 onward. Only Offer Statuses catalog, §3.1, is enforced in the MVP via `shared/state_machine.py`.

| § | Catalog | Purpose | Initial values and notes |
| --- | --- | --- | --- |
| 3.1 | Offer Statuses | Define offer lifecycle states. | `Discovered`, `Prepared`, `Evaluated`, `Accepted`, `Discarded`, `Processed`, `Finalized`. Official 7-status source of truth, aligned with `shared/state_machine.py` and DOC-01 §13; previous 12-value versions are superseded. |
| 3.2 | Source Types | Classify offer origins. | `Job portal`, `Corporate page`, `LinkedIn`, `Recruitment agency`, `Referral`, `Other`. |
| 3.3 | Work Modalities | Classify vacancy execution modality. | `On-site`, `Remote`, `Hybrid`. |
| 3.4 | Contract Types | Classify contractual modality. | `Permanent`, `Fixed term`, `Temporary`, `Service provision`, `Freelance`, `Internship`, `Not specified`. |
| 3.5 | Experience Level | Classify required experience. | `No experience`, `Junior`, `Mid-Senior`, `Senior`, `Lead`, `Managerial`, `Not specified`. |
| 3.6 | Education Level | Classify required academic level. | `High school`, `Technical`, `Associate`, `Bachelor's`, `Specialization`, `Master's`, `Doctorate`, `Not specified`. |
| 3.7 | Business Sectors | Classify company economic sector. | `Technology`, `Manufacturing`, `Healthcare`, `Education`, `Financial`, `Retail`, `Consulting`, `Government`, `Other`. |
| 3.8 | Company Size | Classify organization size. | `Micro-enterprise`, `Small`, `Medium`, `Large`, `Multinational`, `Not specified`. |
| 3.9 | Document Types | Classify generated documents. | `Cover Letter`, `Resume`, `Application email`, `Supporting document`, `Other`. |
| 3.10 | Document Statuses | Control document lifecycle. | `Generated`, `Reviewed`, `Approved`, `Used`, `Archived`. |
| 3.11 | Application Channels | Classify application means. | `Job portal`, `Corporate page`, `LinkedIn`, `Email`, `Other`. |
| 3.12 | Application Statuses | Record application evolution. | `Pending`, `Sent`, `Under review`, `Interview`, `Technical test`, `Offer received`, `Rejected`, `Withdrawn`, `Completed`. |
| 3.13 | Event Types | Classify recorded events. | `Discovery`, `Processing`, `Evaluation`, `Document generation`, `Application`, `Update`, `Error`, `Warning`, `Information`. In Discovery module 1, each event is additionally classified by Event.`tipo`: `error` or `suceso` — decision 2026-08-07. |
| 3.14 | Decision Types | Classify automation decisions. | `Approval`, `Rejection`, `Continue processing`, `Stop processing`, `Generate document`, `Apply`, `Archive`. |
| 3.15 | Overqualification Risk | Classify detailed-evaluation overqualification risk. | `Bajo`, `Medio`, `Alto`. |
| 3.16 | Final Recommendation | Record detailed-evaluation final recommendation. | `Aplicar`, `Aplicar con reservas`, `No aplicar`. |

## 4. Logical Data Model

Defines entities, relationships, and organization rules independently of implementation technology.

### 4.1. Main entities

Offer, Source, Company, Location, Processed Offer, Initial Evaluation, Detailed Evaluation, Generated Document, Application, Event, Decision, Configuration, Catalog, Corrida, Sesion, Bloqueo.

### 4.2–4.3. Relationships and cardinalities

| Relationship | Cardinality |
| --- | --- |
| Source → Offer | 1:N |
| Company → Offer | 1:N |
| Location → Offer | 1:N |
| Offer → Processed Offer | 1:1 |
| Processed Offer → Initial Evaluation | 1:1 |
| Processed Offer → Detailed Evaluation | 1:0..1 |
| Detailed Evaluation → Generated Document | 1:N |
| Offer → Event | 1:N |
| Offer → Decision | 1:N |
| Offer → Application | 1:0..1 |
| Generated Document → Application | 1:N |
| Corrida → Offer | 1:N |
| Corrida → Event | 1:N |
| Corrida → Sesion | 1:N |
| Corrida → Bloqueo | 1:0..1 |
| Source → Sesion | 1:N |

### 4.4. Logical flow

Main information flow:

`Source → Offer → Processed Offer → Initial Evaluation → Detailed Evaluation → Generated Document → Application`

Event and Decision record traceability throughout the process. Catalog and Configuration provide supporting controlled values and operational parameters. During Discovery — module 1 — each Corrida anchors Offers, Events, and Sesiones via `run_id`, and is protected by Bloqueo while active.

### 4.5. Model integrity

The model must guarantee:
- Referential integrity across all relationships.
- No orphan entities.
- Every main entity is traceable to the originating offer.
- Every Discovery-module record — offers, events, sessions — is traceable to its run via `run_id` — RN-01.
- Original offer information remains unchanged throughout processing.
- Processing traceability is fully reconstructible from entity relationships.

### 4.6. Model evolution

Any Logical Data Model modification must:
- Maintain compatibility with official project versions.
- Update the Official Data Dictionary.
- Update the Entity–Relationship Diagram.
- Maintain consistency with Document 13 architecture.

## 5. Official Data Dictionary

Official technical reference for all model attributes.

### 5.1. Dictionary structure

Each attribute documents, at minimum: Entity, Attribute, Description, Logical type, Required, Primary key, Alternate key, Foreign key, Default value, Domain, Constraints, Sensitivity, Persistence, Observations.

### 5.2. Coverage

The dictionary includes all attributes of: Offer, Source, Company, Location, Processed Offer, Initial Evaluation, Detailed Evaluation, Generated Document, Application, Event, Decision, Configuration, Catalog, Corrida, Sesion, Bloqueo. Implemented attributes not documented here are not permitted.

**Common audit fields:**  
For entities §5.5.1–5.5.13, unless otherwise specified:
- `creation_date` — Record creation timestamp. Date/Time; required. Sensitivity Internal; Persistence Permanent.
- `update_date` — Last record update timestamp. Date/Time; required. Sensitivity Internal; Persistence Permanent. Actual name is `last_edit_date` for Offer, Source, Company, Location, Processed Offer, and Initial Evaluation; no actual name is noted for Detailed Evaluation, Generated Document, Application, Configuration, and Catalog.

Event and Decision include only `creation_date`. Corrida, Sesion, and Bloqueo use only their listed temporal fields.

### 5.3. Consistency

Any attribute modification must be reflected consistently in:
- Entity specification.
- Logical Data Model.
- ERD, if structure is affected.

The Official Data Dictionary is the technical reference for database implementation.

### 5.4. Change control

Any addition, modification, or deletion of attributes must update this dictionary before being considered an official model version. Documented information must remain synchronized with project technical documentation.

### 5.5. Attribute catalog

#### 5.5.1. Offer

- `id` — Unique identifier. UUID; required; PK. Sensitivity Internal; Permanent. Actual name: `id`.
- `source_id` — Reference to the source where the offer was discovered. UUID; required; FK Source. Constraint: mandatory source. Internal; Permanent. Actual name: `fuente_id`; MVP stores raw `source_id` string without FK constraint — D4.
- `company_id` — Reference to the company publishing the offer. UUID; logically mandatory association; FK Company. Constraint: mandatory company. Internal; Permanent. Actual name: `empresa_id`; MVP capture may be `NULL` — D4.
- `location_id` — Reference to the location associated with the offer. UUID; optional; FK Location. Public; Permanent. Actual name: `ubicacion_id`; MVP capture may be `NULL` — D4.
- `source_identifier` — Identifier used by the source of origin. Text; optional. Public; Permanent.
- `run_id` — Run that discovered the offer. UUID; optional; FK Corrida. Discovery traceability — RN-01. Internal; Permanent. Actual name: `run_id`.
- `session_id` — Platform session used to discover the offer. UUID; optional; module 1. Internal; Permanent. Actual name: `session_id`.
- `set_indice` — Index of the filter set that produced the offer. Integer; optional; module 1. Internal; Permanent. Actual name: `set_indice`.
- `id_externo_url` — External identifier of the offer in the source of origin; alias of `source_identifier`; best effort. Text; optional. Public; Permanent. Actual name: `id_externo_url`.
- `url` — Original offer link. Text; required. Constraint: preserved throughout lifecycle. Public; Permanent.
- `title` — Original offer title. Text; required. Public; Permanent. Actual name: `titulo`.
- `original_description` — Original content obtained during discovery. Long Text; required. Constraint: must not be overwritten after discovery. Public; Permanent. Actual name: `descripcion_original`.
- `publication_date` — Publication date indicated by the source. Date/Time; optional. Public; Permanent.
- `discovery_date` — Date/time when automation discovered the offer. Date/Time; required. Internal; Permanent.
- `status` — Current offer status in the processing flow. Catalog; required; FK Catalog. Default: `discovered`. Domain: Offer Statuses — 7 values. Constraint: follows official state machine. Internal; Permanent. Actual name: `estado`.
- `active` — Indicates whether the offer remains valid. Boolean; required; default `true`. Internal; Permanent.
- `observations` — Additional relevant offer information. Long Text; optional. Internal; Permanent. Actual name: `observaciones`.

#### 5.5.2. Source

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `name` — Official source name. Text; required. Constraint: unique name. Internal; Permanent. Actual name: `nombre`.
- `type` — Source type. Catalog; required; FK Catalog. Domain: Source Types. Constraint: valid catalog value. Internal; Permanent. Actual name: `tipo`.
- `main_url` — Main source URL. Text; required. Constraint: unique URL. Public; Permanent. Actual name: `url_base`.
- `description` — General source description. Long Text; optional. Internal; Permanent.
- `active` — Indicates whether source is enabled for discovery. Boolean; required; default `true`. Constraint: catalog attribute for external administration; Discovery does not filter by it at runtime — D1. Internal; Permanent.
- `query_frequency` — Configured query frequency. Catalog; optional; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `last_query` — Last query date/time. Date/Time; optional. Internal; Permanent.
- `last_update` — Last detected source update date/time, when determinable. Date/Time; optional. Internal; Permanent.
- `observations` — Additional relevant information. Long Text; optional. Internal; Permanent.

#### 5.5.3. Company

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `name` — Official company name. Text; required. Public; Permanent. Actual name: `nombre`.
- `normalized_name` — Standardized name used to avoid duplicates. Text; required. Internal; Permanent.
- `website` — Official website. Text; optional. Public; Permanent. Actual name: `sitio_web`.
- `linkedin` — Official LinkedIn profile URL. Text; optional. Public; Permanent.
- `sector` — Economic sector. Catalog; optional; FK Catalog. Domain: Business Sectors. Constraint: valid catalog value. Internal; Permanent.
- `size` — Company size classification. Catalog; optional; FK Catalog. Domain: Company Size. Constraint: valid catalog value. Internal; Permanent.
- `description` — General company description. Long Text; optional. Public; Permanent. Actual name: `descripcion`.
- `observations` — Additional relevant information. Long Text; optional. Internal; Permanent.

#### 5.5.4. Location

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `country` — Country where the vacancy is offered. Text; required. Constraint: at least country is mandatory. Public; Permanent. Actual name: `pais`.
- `region` — State, province, or department. Text; optional. Public; Permanent.
- `city` — City of the vacancy. Text; optional. Public; Permanent. Actual name: `ciudad`.
- `address` — Specific address when available. Text; optional. Public; Permanent.
- `modality` — Work modality associated with the location. Catalog; required; FK Catalog. Domain: Work Modalities. Constraint: valid catalog value. Public; Permanent. Actual name: `modalidad`.
- `location_type` — Classification of offer location. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `observations` — Additional location information. Long Text; optional. Internal; Permanent.

#### 5.5.5. Processed Offer

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `offer_id` — Reference to original offer. UUID; required; AK; FK Offer. Constraint: unique per offer. Internal; Permanent.
- `normalized_position` — Normalized position name. Text; required. Public; Permanent. Actual name: `clean_title`.
- `processed_description` — Structured offer description. Long Text; required. Public; Permanent. Actual name: `clean_description`.
- `summary` — Generated summary. Long Text; optional. Internal; Permanent. Not implemented — PMD-020.
- `technical_skills` — Identified technical skills. Long Text; optional. Internal; Permanent. Not implemented — PMD-020.
- `soft_skills` — Identified soft skills. Long Text; optional. Internal; Permanent. Not implemented — PMD-020.
- `technologies` — Technologies identified during processing. Long Text; optional. Internal; Permanent. Implemented as JSON list — PMD-020. Actual name: `tecnologias`.
- `experience_level` — Required experience level. Catalog; optional; FK Catalog. Domain: Experience Level. Constraint: valid catalog value. Internal; Permanent.
- `education_level` — Identified education level. Catalog; optional; FK Catalog. Domain: Education Level. Constraint: valid catalog value. Internal; Permanent.
- `contract_type` — Identified contract type. Catalog; optional; FK Catalog. Domain: Contract Types. Constraint: valid catalog value. Internal; Permanent.
- `work_modality` — Identified work modality. Catalog; optional; FK Catalog. Domain: Work Modalities. Constraint: valid catalog value. Internal; Permanent.
- `salary_range` — Normalized salary information when available. Text; optional. Internal; Permanent. Implemented as `salario_min`, `salario_max`, `moneda`.
- `languages` — Required or desirable languages. Long Text; optional. Internal; Permanent. Implemented as JSON list — PMD-020. Actual name: `idiomas`.
- `benefits` — Identified benefits. Long Text; optional. Public; Permanent.
- `requirements` — Main requirements extracted from the offer. Long Text; optional. Public; Permanent. Implemented as JSON list — PMD-020. Actual name: `requisitos`.
- `responsibilities` — Identified main responsibilities. Long Text; optional. Public; Permanent.
- `processing_date` — Processing completion date/time. Date/Time; required. Internal; Permanent.
- `processing_version` — Version of the processing process used. Text; required. Internal; Permanent.
- `observations` — Additional processing information. Long Text; optional. Internal; Permanent.

#### 5.5.6. Initial Evaluation

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `processed_offer_id` — Reference to evaluated processed offer. UUID; required; AK; FK Processed Offer. Constraint: unique per processed offer. Internal; Permanent.
- `result` — Initial evaluation result. Catalog; required; FK Catalog. Domain: Evaluation Result. Constraint: valid catalog value. Internal; Permanent. Actual name: `resultado`.
- `score` — Total evaluation score. Decimal; required. Domain: 0–100. Internal; Permanent.
- `pass_threshold` — Minimum score required to pass. Decimal; required; default `50`. Internal; Permanent. Actual name: `approval_threshold`.
- `decision` — Decision generated from result. Catalog; required; FK Catalog. Domain: Decision Evaluation. Constraint: must match result. Internal; Permanent.
- `justification` — Justification for decision. Long Text; required. Confidential; Permanent.
- `evaluated_criteria` — Summary of applied criteria. Long Text; required. Internal; Permanent.
- `observations` — Additional evaluation information. Long Text; optional. Internal; Permanent.
- `evaluation_date` — Evaluation execution date/time. Date/Time; required. Internal; Permanent.
- `version_modelo` — Version of model, rules, or configuration used. Text; required; default `v1`. Internal; Permanent. Actual name is official.

#### 5.5.7. Detailed Evaluation

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `processed_offer_id` — Reference to evaluated processed offer. UUID; required; AK; FK Processed Offer. Constraint: unique per processed offer. Internal; Permanent.
- `resultado_organizacional` — Main and secondary organizational results identified. Long Text; required. Confidential; Permanent.
- `problema_organizacional` — Main, explicit, inferred, and non-determinable organizational problems. Long Text; required. Confidential; Permanent.
- `perfil_profesional_requerido` — Critical capabilities, way of thinking, experiences, and competencies required. Long Text; required. Confidential; Permanent.
- `coincidencias_perfil` — Main and complementary evidence of profile-vacancy match. Long Text; required. Constraint: evidence must be truthful. Confidential; Permanent.
- `logica_xyz` — X → Y → Z logic constructed during diagnosis. Long Text; required. Confidential; Permanent.
- `hipotesis_valor` — Value hypothesis supporting the candidacy. Long Text; required. Confidential; Permanent.
- `informacion_descartada` — Profile information determined not to add value for this vacancy. Long Text; optional. Confidential; Permanent.
- `ajuste_tecnico` — Technical fit score. Decimal; required. Domain: 0–10. Constraint: must be justified. Internal; Permanent.
- `justificacion_ajuste_tecnico` — Technical fit justification. Long Text; required. Confidential; Permanent.
- `ajuste_funcional` — Functional fit score. Decimal; required. Domain: 0–10. Constraint: must be justified. Internal; Permanent.
- `justificacion_ajuste_funcional` — Functional fit justification. Long Text; required. Confidential; Permanent.
- `ajuste_estrategico` — Strategic fit score. Decimal; required. Domain: 0–10. Constraint: must be justified. Internal; Permanent.
- `justificacion_ajuste_estrategico` — Strategic fit justification. Long Text; required. Confidential; Permanent.
- `riesgo_sobrecalificacion` — Overqualification risk level. Catalog; required; FK Catalog. Domain: Overqualification Risk — `Bajo`, `Medio`, `Alto`. Constraint: valid catalog value. Confidential; Permanent.
- `justificacion_riesgo` — Justification for risk level. Long Text; required. Confidential; Permanent.
- `recomendacion_final` — Final recommendation on applying. Catalog; required; FK Catalog. Domain: Final Recommendation — `Aplicar`, `Aplicar con reservas`, `No aplicar`. Constraint: valid catalog value. Confidential; Permanent.
- `justificacion_recomendacion` — Justification for final recommendation. Long Text; required. Confidential; Permanent.
- `insumos_carta_presentacion` — Strategic inputs for cover letter construction. Long Text; required. Confidential; Permanent.
- `evaluation_date` — Evaluation completion date/time. Date/Time; required. Internal; Permanent.
- `version_metodologia` — Methodology version used. Text; required; default `v1`. Internal; Permanent.

#### 5.5.8. Generated Document

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `offer_id` — Offer for which the document was generated. UUID; required; FK Offer. Confidential; Permanent.
- `detailed_evaluation_id` — Detailed evaluation used as basis. UUID; required; FK Detailed Evaluation. Constraint: requires completed evaluation. Confidential; Permanent.
- `document_type` — Type of generated document. Catalog; required; FK Catalog. Domain: Document Types. Constraint: valid catalog value. Internal; Permanent.
- `document_name` — Assigned document name. Text; required. Confidential; Permanent.
- `version` — Document version. Text; required. Constraint: traceability per version. Internal; Permanent.
- `content` — Complete document content. Long Text; required. Confidential; Permanent.
- `format` — Document format. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `status` — Current document status. Catalog; required; FK Catalog. Domain: Document Statuses. Constraint: valid catalog value. Internal; Permanent.
- `generation_date` — Generation date/time. Date/Time; required. Internal; Permanent.
- `last_modified_date` — Last modification date/time, when applicable. Date/Time; optional. Internal; Permanent.
- `observations` — Additional document information. Long Text; optional. Internal; Permanent.

#### 5.5.9. Application

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `offer_id` — Offer to which application is made. UUID; required; FK Offer. Confidential; Permanent.
- `main_document_id` — Main document used for application. UUID; required; FK Generated Document. Constraint: at least one document required. Confidential; Permanent.
- `application_date` — Application submission date/time. Date/Time; optional. Internal; Permanent.
- `application_channel` — Means used to apply. Catalog; required; FK Catalog. Domain: Application Channels. Constraint: valid catalog value. Internal; Permanent.
- `status` — Current application status. Catalog; required; FK Catalog. Domain: Application Statuses. Constraint: valid catalog value. Internal; Permanent.
- `company_response` — Response received from company. Long Text; optional. Confidential; Permanent.
- `response_date` — Company response date/time. Date/Time; optional. Internal; Permanent.
- `next_action` — Next planned action in selection process. Text; optional. Confidential; Permanent.
- `next_action_date` — Scheduled date for next action. Date/Time; optional. Internal; Permanent.
- `observations` — Additional application information. Long Text; optional. Confidential; Permanent.

#### 5.5.10. Event

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `run_id` — Run that generated the event. UUID; required; FK Corrida. Constraint: mandatory in module 1 — RN-01. Internal; Permanent. Actual name: `run_id`.
- `source_id` — Source on which the event occurred. UUID; optional; FK Source. Module 1 traceability. Internal; Permanent.
- `session_id` — Platform session in which the event occurred. UUID; optional; module 1. Internal; Permanent.
- `set_indice` — Filter-set index where the event occurred. Integer; optional; module 1. Internal; Permanent.
- `offer_id` — Offer related to the event. UUID; optional; FK Offer. Constraint: required only when event belongs to a specific offer. Internal; Permanent.
- `tipo` — Event classification: `error` or `suceso`. Catalog; required; FK Catalog. Domain: `error`, `suceso`. Module 1 typology — decision 2026-08-07. Internal; Permanent.
- `codigo` — Business code — e.g., `ERR-01`, `EVT-01`. Text; optional. Per Discovery module technical sheet. Internal; Permanent.
- `evidencia` — Evidence — screenshots, traces, raw snippets. Long Text; optional. Constraint: never credentials or session tokens. Internal; Permanent. Actual name: `evidencia`.
- `event_type` — Type of event recorded. Catalog; required; FK Catalog. Domain: Event Types. Constraint: valid catalog value. Internal; Permanent.
- `affected_entity` — Name of entity affected. Text; required. Internal; Permanent.
- `entity_id` — Identifier of record affected. UUID; required. For run-level events, use `run_id`. Internal; Permanent.
- `action` — Executed action. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `description` — Detailed event description. Long Text; required. Internal; Permanent.
- `result` — Result of associated operation. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `origin` — Automation component that generated the event. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `context` — Additional contextual information. Long Text; optional. Internal; Permanent.
- `event_date` — Date/time when event occurred. Date/Time; required. Constraint: exact moment required. Internal; Permanent.
- `creation_date` — Record creation date/time. Date/Time; required. Internal; Permanent.
- Deletion constraint: events cannot be deleted once recorded; audit trail.

#### 5.5.11. Decision

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `offer_id` — Offer related to the decision. UUID; required; FK Offer. Constraint: mandatory. Internal; Permanent.
- `stage` — Process stage where decision was made. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `decision_type` — Decision classification. Catalog; required; FK Catalog. Domain: Decision Types. Constraint: valid catalog value. Internal; Permanent.
- `decision` — Decision adopted. Text; required. Internal; Permanent.
- `justification` — Explanation supporting decision. Long Text; required. Constraint: mandatory. Confidential; Permanent.
- `evidence` — Evidence supporting decision. Long Text; required. Constraint: mandatory. Confidential; Permanent.
- `confidence` — Confidence level, when applicable. Decimal; optional. Internal; Permanent.
- `origin_component` — Component that generated the decision. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `decision_date` — Decision date/time. Date/Time; required. Internal; Permanent.
- `observations` — Additional decision information. Long Text; optional. Internal; Permanent.
- `creation_date` — Record creation date/time. Date/Time; required. Internal; Permanent.
- Deletion constraint: decisions cannot be deleted once recorded; audit trail.

#### 5.5.12. Configuration

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `category` — Parameter category. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `name` — Unique parameter name. Text; required; AK. Constraint: unique within system. Internal; Permanent.
- `description` — Parameter purpose. Long Text; required. Internal; Permanent.
- `value` — Assigned parameter value. Long Text; required. Constraint: compatible with data type. Sensitivity Secret — secret for credential parameters; Permanent.
- `data_type` — Expected value data type. Catalog; required; FK Catalog. Domain: Catalog. Constraint: valid catalog value. Internal; Permanent.
- `default_value` — Default value. Long Text; optional. Internal; Permanent.
- `required` — Indicates whether parameter is required. Boolean; required. Constraint: required parameters always have a value. Internal; Permanent.
- `editable` — Indicates whether parameter can be modified without altering implementation. Boolean; required. Internal; Permanent.
- `active` — Indicates whether parameter is enabled. Boolean; required; default `true`. Internal; Permanent.
- `observations` — Additional parameter information. Long Text; optional. Internal; Permanent.

#### 5.5.13. Catalog

- `id` — Unique identifier. UUID; required; PK. Internal; Permanent.
- `catalog_name` — Catalog to which record belongs. Text; required; AK. Internal; Permanent.
- `code` — Unique value code within catalog. Text; required; AK. Constraint: codes remain stable. Internal; Permanent.
- `name` — Display name of value. Text; required. Internal; Permanent.
- `description` — Catalog value description. Long Text; optional. Internal; Permanent.
- `order` — Presentation order. Integer; optional. Internal; Permanent.
- `active` — Indicates whether value can be used. Boolean; required; default `true`. Constraint: inactive values not used in new records. Internal; Permanent.
- `observations` — Additional value information. Long Text; optional. Internal; Permanent.

#### 5.5.14. Corrida

- `id` — Unique identifier of run record. UUID; required; PK. Internal; Permanent.
- `run_id` — Public unique run identifier. UUID; required; AK. Constraint: referenced by every module record — RN-01. Internal; Permanent. Actual name: `run_id`.
- `start_timestamp` — Run start date/time. Date/Time; required. Internal; Permanent.
- `end_timestamp` — Run end date/time. Date/Time; optional. Applies to normal, concurrency, or failure termination. Internal; Permanent.
- `estado` — Run status. Catalog; required; FK Catalog. Default: `en_ejecucion`. Domain: `en_ejecucion`, `corrida_completada`, `sin_fuentes`, `error`, `concurrencia`. Constraint: follows Discovery technical sheet. Internal; Permanent. Actual name: `estado`.

#### 5.5.15. Sesion

- `id` — Unique identifier of session record. UUID; required; PK. Internal; Permanent.
- `session_id` — Platform session identifier assigned by source. UUID; optional; AK. Constraint: unique per source. Internal; Permanent.
- `run_id` — Run under which session was established. UUID; required; FK Corrida. Internal; Permanent.
- `source_id` — Source on which session was established. UUID; required; FK Source. Internal; Permanent.
- `set_indice` — Filter-set index for session. Integer; optional; AK with `session_id`. Internal; Permanent.
- `timestamp` — Session establishment date/time. Date/Time; required. Internal; Permanent.
- `total_declarado` — Total offers declared by source, when exposed. Integer; optional. Internal; Permanent.
- `conteo` — Offers captured during session. Integer; required. Internal; Permanent.
- `estado` — Final session state. Catalog; required; FK Catalog. Domain: `activa`, `cerrada`, `expirada`. Internal; Permanent.

#### 5.5.16. Bloqueo

- `id` — Unique identifier of lock record. UUID; required; PK. Internal; Permanent.
- `run_id` — Run owning the lock. UUID; required; FK Corrida. Internal; Permanent.
- `timestamp` — Lock acquisition date/time. Date/Time; required. Internal; Permanent.
- `umbral_obsolescencia` — Seconds after which lock may become obsolete. Integer; required. Constraint: from configuration; no hardcoded values; defined in configuration file. Internal; Permanent.
- `estado` — Lock state. Catalog; required; FK Catalog. Default: `activo`. Domain: `activo`, `obsoleto`, `liberado`. Constraint: single active lock per run. Internal; Permanent.

## 6. Entity–Relationship Diagram

The ERD is the official graphical representation of the Logical Data Model. It must represent official entities, relationships, and cardinalities; remain consistent with entity specifications, Logical Data Model, and Data Dictionary; avoid ambiguous or duplicate relationships; and maintain readable layout. No differences are permitted among these four artifacts.

Entities represented: all entities in §1.  
Relationships represented: all official relationships in §4.3, including Catalog controlled-value support and Configuration support relationships.

### 6.1. Entity–Relationship Diagram — Mermaid

```mermaid
erDiagram
     SOURCE ||--o{ OFFER : "publishes"
     COMPANY ||--o{ OFFER : "publishes"
     LOCATION ||--o{ OFFER : "is associated with"
     OFFER ||--|| PROCESSED_OFFER : "generates"
     PROCESSED_OFFER ||--|| INITIAL_EVALUATION : "is evaluated by"
     PROCESSED_OFFER ||--o| DETAILED_EVALUATION : "may have"
     DETAILED_EVALUATION ||--o{ GENERATED_DOCUMENT : "provides inputs for"
     OFFER ||--o{ EVENT : "records events"
     OFFER ||--o{ DECISION : "records decisions"
     OFFER ||--o| APPLICATION : "may originate"
     GENERATED_DOCUMENT ||--o{ APPLICATION : "is used in"
     CORRIDA ||--o{ OFFER : "captures under"
     CORRIDA ||--o{ EVENT : "anchors"
     CORRIDA ||--o{ SESION : "registers"
     CORRIDA ||--o| BLOQUEO : "is protected by"
     SESION }o--|| SOURCE : "is established on"
     CONFIGURATION }o--|| CATALOG : "category, data_type / provides values"
     CATALOG ||--o{ OFFER : "provides values"
     CATALOG ||--o{ SOURCE : "provides values"
     CATALOG ||--o{ COMPANY : "provides values"
     CATALOG ||--o{ LOCATION : "provides values"
     CATALOG ||--o{ PROCESSED_OFFER : "provides values"
     CATALOG ||--o{ INITIAL_EVALUATION : "provides values"
     CATALOG ||--o{ DETAILED_EVALUATION : "provides values"
     CATALOG ||--o{ GENERATED_DOCUMENT : "provides values"
     CATALOG ||--o{ APPLICATION : "provides values"
     CATALOG ||--o{ EVENT : "provides values"
     CATALOG ||--o{ DECISION : "provides values"
```

### 6.2. Main flow — ASCII

```text
SOURCE ──1:N──> OFFER ──1:1──> PROCESSED_OFFER ──1:1──> INITIAL_EVALUATION
COMPANY ──1:N──> OFFER                                             │
LOCATION ──1:N──> OFFER                                       1:0..1
                                                                   ▼
OFFER ──1:N──> EVENT ─────────────────────────────────────> DETAILED_EVALUATION
OFFER ──1:N──> DECISION                                             │
OFFER ──1:0..1──> APPLICATION <──1:N── GENERATED_DOCUMENT <──1:N────┘

CORRIDA ──1:N──> OFFER / EVENT / SESION   — module 1 traceability, run_id
CORRIDA ──1:0..1──> BLOQUEO
SESION ──N:1──> SOURCE
CATALOG ──1:N──> all entities using controlled values — support
CONFIGURATION ──N:1──> CATALOG — support
```

### 6.3. Cardinality legend

| Symbol | Meaning |
| --- | --- |
| 1:1 | Exactly one on each side. |
| 1:0..1 | One on the left; zero or one on the right. |
| 1:N | One on the left; many on the right. |
| N:1 | Many on the left; one on the right. |

## 7. Version History

Every data-model modification must be recorded before becoming official. Each version records number, date, author, and change description. Structural changes require updating: entity inventory, entity specifications, catalogs, Logical Data Model, Official Data Dictionary, and ERD. A version with inconsistencies among these components is not official.

| Version | Date | Author | Change description |
| --- | --- | --- | --- |
| 1.0 | 2026-07-30 | System | Initial creation of Document 13A — Detailed Data Model Design. |
| 1.1 | 2026-07-30 | System | Alignment with implementation: official Offer Statuses catalog reduced to the 7 states of `shared/state_machine.py`; attribute names aligned with `shared/models.py` — `version_modelo`, `region`; recorded Processed Offer deviations — PMD-020; implemented-persistence scope note. |
| 1.2 | 2026-07-30 | System | Detailed Evaluation entity redefined with Spanish attribute names — decision C2: prompts adjusted to the entity; Overqualification Risk and Final Recommendation catalog values in Spanish; Official Data Dictionary §5.5 for the 13 entities; ERD §6.6 in Mermaid + ASCII; sensitivity classification per DOC-12 §14.2. |
| 1.3 | 2026-08-07 | System | Discovery module — module 1: traceability fields added to Offer — `run_id`, `session_id`, `set_indice`, `id_externo_url`; Source.`active` redefined as catalog attribute — decision D1; Event formalized — mandatory `run_id`, typology `tipo` error/suceso, `codigo`, `evidencia`, optional `offer_id`; new entities Corrida, Sesion, Bloqueo — decisions D2 and D3; inventory, Logical Data Model, Data Dictionary, and ERD updated. |
| 1.4 | 2026-08-09 | System | Sub-phase 4.4 capture registration — decision D4: Offer gains `empresa_nombre`, `ubicacion_nombre`, and `timestamp_ultima_verificacion`; `empresa_id` / `ubicacion_id` optional — `NULL` in MVP; `fuente_id` stored as raw string without FK constraint; registration deduplicates by `id_externo_url` via upsert. Data Dictionary updated. |
