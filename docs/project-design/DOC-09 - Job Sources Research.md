# DOC-09 – Job Sources Research

---

## 1. Purpose and Scope

This document investigates, analyzes, and documents the characteristics of job sources usable by the job search automation, providing the technical, functional, and strategic foundation for source selection decisions.

**Scope:** The current version is limited exclusively to the LinkedIn platform, approved as the sole official job source for the automation MVP. Adding new sources requires a formal update of this document and the same research process.

**Binding nature:** Decisions adopted here are mandatory for all subsequent architecture, development, and operation documents, unless modified through a formal documentation update.

**Validity condition:** Every conclusion, decision, and recommendation must be supported by prior verified analysis or research (PIF-001, PIF-007).

---

## 2. Source Research Principles

| ID | Principle | Rule |
|---|---|---|
| PIF-001 | Evidence-based research | Every conclusion must be supported by previously researched and verified information. No unsupported assumptions. |
| PIF-002 | Objectivity | Evaluation uses technical, functional, and operational criteria. No decisions based on personal preferences. |
| PIF-003 | Legal compliance | Analyze terms of use, applicable policies, and legal restrictions on information retrieval. |
| PIF-004 | User account protection | Prioritize account security. No strategies that unjustifiably increase risk of restrictions, blocks, or suspension. |
| PIF-005 | Project compatibility | The source must be compatible with objectives, scope, functional/non-functional requirements, and the decision model. |
| PIF-006 | Technological independence | Evaluation is independent of specific tools, languages, or technologies. |
| PIF-007 | Traceability | Every decision must be traceable to its evidence, analysis, and justification. |
| PIF-008 | Reproducibility | Documented information must be sufficient to reproduce the analysis and reach the same conclusions, unless the platform has changed. |
| PIF-009 | Controlled updates | When a platform modifies its operation, policies, or access mechanisms, research must be reviewed and updated before modifying the automation. |
| PIF-010 | Stability priority | Among technically viable alternatives, prioritize greater stability, maintainability, and lower operational risk. |
| PIF-011 | Controlled scope | Only LinkedIn is documented for MVP. New sources require formal document update. |
| PIF-012 | Documentary consistency | All information must remain consistent with the rest of the project's official documentation. |

---

## 3. Selection Criteria for Job Sources

A platform is evaluated on the following criteria. All apply to any current or future source.

| # | Criterion | Requirement |
|---|---|---|
| 3.1 | Opportunity coverage | Sufficient job opportunities compatible with the user's target profile. Goal: maximize relevant opportunities, not total volume. |
| 3.2 | Information quality | Listings must provide enough information to assess relevance: at minimum, responsibilities, required knowledge, and elements to compare against the user's profile. Listings with insufficient information are discarded in initial stages. |
| 3.3 | Query strategy compatibility | The platform must allow specific queries with configurable filters to reduce irrelevant listings before evaluation. |
| 3.4 | Evaluation independence | The platform is used exclusively for retrieval. Relevance determination, classification, prioritization, and continuity decisions belong solely to the automation's evaluation system. |
| 3.5 | Technical feasibility | A technically viable mechanism must exist to obtain the required information, compatible with the project's functional and technical objectives. |
| 3.6 | Interaction security | Interaction minimizes operational risk to the user account. Authentication is controlled, limited to strictly required operations, and replicates legitimate user behavior. |
| 3.7 | Maintainability | Integration maintenance must be reasonable throughout the project lifecycle. Platform modifications must be manageable without compromising overall evolution. |
| 3.8 | Cost-benefit ratio | Integration and maintenance effort must be justified by the value added to the search process. No platforms with disproportionate maintenance cost relative to actual increase in relevant opportunities. |

**Approval rule (3.9):** A platform is approved as an official source only when it simultaneously satisfies all criteria 3.1–3.8.

**MVP decision (3.10):** LinkedIn meets all criteria and is approved as the sole official source for the automation MVP.

---

## 4. Operational Recommendations

These complement the principles and criteria above with execution-level guidance.

| # | Recommendation | Detail |
|---|---|---|
| 4.1 | Validate through real testing | Do not base decisions solely on documentation, third-party research, or community information. Conduct practical tests to verify actual platform behavior before adopting decisions. |
| 4.2 | Evidence over assumptions | When research contradicts observed behavior in project tests, practical validation prevails. Document and justify any resulting update to prior decisions. |
| 4.3 | Platform independence | Platform-specific characteristics are treated as decisions for that platform, not as general automation rules. Avoid unnecessary constraints on future evolution. |
| 4.4 | Minimize operational risk | Limit actions to those strictly necessary. Avoid behaviors that increase restriction or suspension risk. |
| 4.5 | Periodic review | Review documented decisions when the platform changes its operation, access mechanisms, policies, or any aspect affecting the automation. |
| 4.6 | Maintain traceability | Every decision must be traceable to the research, evidence, or test that originated it. |
| 4.7 | Incremental evolution | New platforms are researched, documented, evaluated, and integrated individually before expanding scope. |

---

## 5. Acceptance Criteria

The research process for a platform is considered finalized only when all of the following are met:

| # | Criterion | Condition |
|---|---|---|
| 5.1 | Research completed | Necessary information on platform operation relevant to the automation has been collected and analyzed. |
| 5.2 | Practical validation performed | Most relevant conclusions verified through practical tests. If experimental validation is not possible, the limitation is documented. |
| 5.3 | Risks identified | Main technical, operational, and functional risks identified, each with a clear description and, where applicable, a mitigation strategy. |
| 5.4 | Access mechanisms documented | Available mechanisms to access required information documented, including characteristics, limitations, and known restrictions. |
| 5.5 | Restrictions documented | Technical, functional, and usage restrictions identified during research are documented. |
| 5.6 | Feasibility determined | Explicit conclusion on whether the platform is viable, justified by gathered evidence. |
| 5.7 | Decisions documented | All relevant decisions documented and justified, enabling understanding of inclusion, rejection, or particular treatment reasons. |
| 5.8 | Traceability guaranteed | Conclusions, decisions, and recommendations are traceable to supporting evidence. Documentation allows review or update when the platform changes or new evidence emerges. |
| 5.9 | Complete documentation | All chapters of this document completed, reviewed, and approved per project objectives. |

---

## 6. LinkedIn Implementation Specification – Module 1 (Opportunity Discovery)

Official specification for integrating LinkedIn within the Opportunity Discovery module (Module 1) of the automation MVP. Governs the nodes **"Enter the source"**, **"Apply filters"**, and **"Capture offers"** of the official Discovery flow (MVP Execution Plan; DOC-04, Section 15).

### 6.1 Verifiable Entry Criteria

Entry is successful only when, after executing the session accreditation process, **all** of the following are verified:

- The authenticated LinkedIn session displays the navigation bar element `global-nav` (confirms authenticated session).
- The element is visible within the timeout configured as `timeout_ingreso` in the source access configuration.

If criteria are not met: abort entry, return the corresponding `codigo_motivo` from the error catalog (DOC-06, Section 11). **No retry.**

### 6.2 Official Filter Sets

Search uses official filter sets defined per source. Fields:

| Set field | LinkedIn parameter | Typical value |
|---|---|---|
| `keywords` | `keywords` | Professional profile terms |
| `ubicacion` | `location` | Geographic location |
| `modalidad` | `f_WT` | Work type: `2` (Remote), `3` (Hybrid), etc. |
| `fecha_publicacion` | `f_TPR` | Publication period: `r86400` (24 h), `r604800` (7 days), etc. |
| `nivel_experiencia` | `f_JT` | Experience level: `1` (internship), `2` (entry), `3` (associate), etc. |

- Set order is defined by `set_indice` (starting at 0). An empty set (`keywords` not defined) means the base search.
- The complete list of official filter sets per source is defined in `config.yaml`, section `fuentes`. Modification requires official documentation update.

### 6.3 Capture Policies (Defaults)

| Policy | Default | Scope |
|---|---|---|
| `max_paginas` | Configured globally | Pagination consumption per set |
| `max_ofertas_por_corrida` | Configured globally | Total captured offers per run |
| `pausa_entre_lotes` | Configured globally | Minimum interval between batches |
| `estrategia_anti_bloqueo` | `pausa_aleatoria` | Mitigation strategy: `pausa_aleatoria` / `retraso_fijo` / `none` |

These are **not hardcoded**: actual values are resolved from `config/config.yaml`, section `captura`, applying the global default unless the source defines specific values in `politicas_de_captura`.

### 6.4 Captcha / Blocking Treatment

| Evidence | `codigo_motivo` | Result |
|---|---|---|
| Challenge/captcha shown | `bloqueo_plataforma` | Abort run. Group A (no retry). |
| Session expired | `sesion_expirada` | Abort batch. Controlled re-entry permitted. |

**Retry after captcha is expressly prohibited** (increases account blocking risk; DE-LI-006, DE-LI-007). Abort the current run and log evidence without preserving credentials.

---

## 7. Document Index

**Main body:** 1 Purpose and Scope · 2 Source Research Principles · 3 Selection Criteria · 4 Operational Recommendations · 5 Acceptance Criteria · 6 LinkedIn Implementation Specification (Module 1) · 7 Document Index.

**Annexes** (supporting documentation, one set per platform):

- **Annex A – Decisions:** Strategic decisions adopted for the analyzed platform, with justifications.
- **Annex B – Research:** Research, comparative analyses, experimental results, and evidence gathered during evaluation.

Each new platform incorporated into the project shall have its own Annexes A and B, maintaining independence between sources.
