# Document 9 - Job Sources Research

## 1. Purpose of the document

This document aims to objectively investigate, analyze, and document the characteristics of job sources that may be used by the job search automation.

Its purpose is to provide a technical, functional, and strategic foundation that allows determining the feasibility of using a platform as an official source of information for the project, considering its access mechanisms, restrictions, risks, stability, automation possibilities, and compatibility with the objectives defined in the official documentation.

The conclusions contained in this document will serve as the basis for architecture, implementation, and evolution decisions of the automation, preventing such decisions from being based on assumptions or unverified information.

For the current version of the project, the scope of this document is limited exclusively to the analysis of the **LinkedIn** platform, which constitutes the only job source that will be evaluated and documented for the first version (MVP) of the automation.

Any conclusion, decision, or recommendation included in this document must be supported by prior analysis and, where applicable, by research of the technical, functional, or legal information necessary to ensure its validity.

Decisions adopted in this document shall be mandatory for subsequent documents related to the architecture, development, and operation of the automation, unless modified through a formal update of the project documentation.

---

## 2. Principles of source research

The following principles establish the rules that shall govern the investigation, evaluation, selection, and documentation of job sources used by the job search automation.

Their purpose is to ensure that all decisions related to an information source are based on objective, verifiable criteria aligned with the project's official documentation.

---

### PIF-001. Evidence-based research

Every conclusion incorporated into this document must be supported by previously researched and verified information.

No unsupported assumptions or claims shall be documented.

---

### PIF-002. Objectivity

The evaluation of a job source shall be carried out using technical, functional, and operational criteria, avoiding decisions based on personal preferences.

---

### PIF-003. Legal compliance

Every job source shall be analyzed considering its terms of use, applicable policies, and legal restrictions related to information retrieval.

---

### PIF-004. User account protection

Decisions adopted shall prioritize the security and preservation of the account used by the user during interaction with the platform.

No strategies that unjustifiably increase the risk of restrictions, blocks, or account suspension shall be accepted.

---

### PIF-005. Project compatibility

The evaluated source shall be compatible with the objectives, scope, functional requirements, non-functional requirements, and the decision model defined for the automation.

---

### PIF-006. Technological independence

The evaluation of a source shall be conducted without depending on a specific tool, programming language, or technology.

---

### PIF-007. Traceability

Every decision made during the research must be traceable to the corresponding evidence, analysis, and justification.

---

### PIF-008. Reproducibility

The documented information shall be sufficient for a future review to reproduce the analysis and reach the same conclusions, unless the platform has changed.

---

### PIF-009. Controlled updates

When a platform modifies its operation, policies, or access mechanisms, the research shall be reviewed and updated before modifying the automation.

---

### PIF-010. Stability priority

Among several technically viable alternatives, the one offering greater stability, maintainability, and lower operational risk for the automation shall be prioritized.

---

### PIF-011. Controlled scope

This document shall only document the LinkedIn platform for the first version of the automation.

The addition of new sources will require a formal update of the document.

---

### PIF-012. Documentary consistency

All documented information shall remain consistent with the rest of the project's official documentation.

---

## General principles of source research

Source research shall ensure:

- Evidence-based decisions.
- Objective and verifiable evaluations.
- Compliance with legal and usage restrictions.
- Protection of the user account.
- Compatibility with project objectives.
- Traceability of all decisions.
- Ease of updating the research.
- Controlled evolution of the project's official sources.

---

## 3. Criteria for selecting job sources

The selection of a job source for the automation shall be based on objective, verifiable criteria aligned with the overall objectives of the project. The inclusion of a platform will depend not only on its popularity or the volume of available listings, but on its ability to be sustainably integrated within the automation's architecture.

The criteria defined in this chapter shall apply to any platform evaluated in the future, ensuring that all decisions related to the incorporation of new sources maintain the same standard of quality, security, maintainability, and traceability.

### 3.1 Opportunity coverage

The platform shall offer a sufficient number of job opportunities compatible with the user's target professional profile.

The goal is not to obtain the largest possible number of listings, but to maximize the availability of potentially relevant opportunities.

### 3.2 Information quality

Published listings shall provide sufficient information to allow an objective assessment of their relevance.

A listing will be considered suitable to continue in the process only when its content allows understanding, at minimum, the responsibilities of the position, the required knowledge, and the elements necessary to compare it with the user's professional profile.

Listings with insufficient information shall be discarded during the initial stages of the process.

### 3.3 Compatibility with the query strategy

The platform shall allow building sufficiently specific query strategies to reduce the volume of irrelevant listings before the evaluation process.

The automation shall design and execute such queries using configurable filters and criteria oriented to the user's professional profile.

### 3.4 Independence of the evaluation system

The platform shall be used exclusively as a source for retrieving job opportunities.

Determining the relevance of each listing shall be the sole responsibility of the automation's evaluation system, which will apply its own criteria to classify, prioritize, and decide the continuity of each opportunity.

### 3.5 Technical feasibility

A technically viable mechanism must exist to obtain the information required for the automation.

The platform shall allow an integration that is compatible with the functional and technical objectives of the project.

### 3.6 Interaction security

Interaction with the platform shall be carried out through mechanisms that minimize operational risk to the user account.

When the platform requires authentication to access the necessary functionalities, this shall be implemented in a controlled manner, limited to strictly required operations and seeking to replicate the expected behavior of a legitimate user.

### 3.7 Maintainability

The platform shall allow an integration whose maintenance is reasonable throughout the project lifecycle.

Modifications the platform may undergo over time shall be manageable without compromising the overall evolution of the automation.

### 3.8 Cost-benefit ratio

The effort required to integrate and maintain a platform shall be justified by the value it brings to the job opportunity search process.

No platforms whose maintenance cost is disproportionate to the actual increase in relevant opportunities shall be incorporated.

### 3.9 Approval principles

A platform may be approved as an official source of the project only when it simultaneously meets the following principles:

- It provides relevant job opportunities for the target professional profile.
- Listings contain sufficient information to be objectively evaluated.
- A technically viable mechanism exists to obtain the required information.
- It allows secure interaction with an acceptable operational risk for the user account.
- Its maintenance is sustainable throughout the project lifecycle.
- The benefit obtained justifies the integration and maintenance effort.

### 3.10 Application to the MVP

As a result of the research process carried out for the first version of the project, it is determined that LinkedIn meets the criteria established in this chapter and is approved as the sole official source of job opportunities for the automation MVP.

Future additions of new platforms shall undergo the same research, analysis, and evaluation process before being approved as official sources of the project.

---

## 4. General recommendations

The following recommendations shall be considered during the analysis, selection, and integration of any job platform within the project.

### 4.1 Always validate through real testing

Decisions related to a platform shall not be based solely on documentation, third-party research, or information published by the community.

Whenever possible, practical tests should be conducted to verify the actual behavior of the platform before adopting a decision that affects the design or operation of the automation.

### 4.2 Prioritize evidence over assumptions

When there is a contradiction between research and the behavior observed during tests carried out by the project, the evidence obtained through practical validation shall prevail.

Any modification derived from new evidence shall be documented and justify the update of previously adopted decisions.

### 4.3 Maintain independence from the platform

Decisions made during the analysis of a platform shall not unnecessarily constrain the future evolution of the project.

Whenever possible, the particular characteristics of a platform shall be treated as specific decisions for that platform and not as general rules of the automation.

### 4.4 Minimize operational risk

Interaction with any platform shall be designed to reduce risk to the user account.

The automation shall limit its actions to those strictly necessary to fulfill the objectives defined by the project and avoid behaviors that may increase the risk of restrictions or suspensions.

### 4.5 Periodically review adopted decisions

Job platforms evolve constantly.

For this reason, documented decisions shall be reviewed when there are relevant changes in the platform's operation, its access mechanisms, its policies, or any other aspect that may affect the automation.

### 4.6 Maintain traceability

Every relevant decision shall be traceable to the research, evidence, or practical test that originated it.

Traceability will facilitate updating the project when a platform modifies its behavior or when new job sources are incorporated.

### 4.7 Favor incremental evolution

The incorporation of new platforms shall be carried out gradually.

Each new source shall be researched, documented, evaluated, and integrated individually before expanding the scope of the automation.

---

## 5. Acceptance criteria

The research and analysis process for a job platform shall be considered finalized only when the following criteria have been met.

### 5.1 Research completed

The necessary information to understand the platform's operation in aspects relevant to the automation shall have been collected and analyzed.

### 5.2 Practical validation performed

The most relevant conclusions shall have been verified through practical tests whenever possible.

When experimental validation is not possible, such limitation shall be documented.

### 5.3 Risks identified

The main technical, operational, and functional risks associated with using the platform shall have been identified.

Each risk shall have a clear description and, where applicable, a mitigation strategy.

### 5.4 Access mechanisms documented

The mechanisms available to access the information required for the automation shall be documented, including their main characteristics, limitations, and known restrictions.

### 5.5 Restrictions documented

Technical, functional, and usage restrictions identified during the research process shall be documented.

### 5.6 Feasibility determined

The research shall explicitly conclude whether the platform is viable or not to be part of the automation, justifying said decision based on the evidence gathered.

### 5.7 Decisions documented

All relevant decisions derived from the analysis shall be documented and justified, allowing understanding of the reasons supporting the inclusion, rejection, or particular treatment of the platform.

### 5.8 Traceability guaranteed

Conclusions, decisions, and recommendations shall be traceable to the evidence, research, or tests that support them.

The documentation shall allow reviewing or updating decisions when the platform modifies its operation or new evidence is obtained.

### 5.9 Complete documentation

The platform analysis shall be considered accepted only when all chapters defined in this document have been completed, reviewed, and approved in accordance with the project objectives.

---

## 6. LinkedIn implementation specification for Module 1

This chapter establishes the official specifications for the implementation of the integration with LinkedIn within the Opportunity Discovery module (Module 1) of the automation MVP.

Its purpose is to provide the register of rules and contracts necessary to implement the nodes "Enter the source", "Apply filters", and "Capture offers" of the official Discovery flow, defined in the MVP Execution Plan and the reference data flow (DOC-04, Section 15), using exclusively the information documented in this chapter together with the technical sheet of the module.

### 6.1. Verifiable entry criteria

Entry to the platform shall be considered successful only when, after executing the accreditation process (user account) of the session, all of the following criteria are verified:

- The authenticated LinkedIn session shows the navigation bar element that confirms the authenticated session (DOM element `global-nav`).
- The element is visible within the timeout configured as `timeout_ingreso` in the source access configuration.

The automation shall proceed with the capture only when the criteria are met; otherwise, it shall abort the entry returning the corresponding `codigo_motivo` established in the error catalog (DOC-06, Section 11) without retrying.

### 6.2. Official filter sets

The search strategy shall use the official filter sets defined for the source, composed of the following fields:

| Set field | LinkedIn search parameter | Typical value |
|-----------|--------------------------|---------------|
| `keywords` | `keywords` | Professional profile terms |
| `ubicacion` | `location` | Geographic location |
| `modalidad` | `f_WT` | Work type: `2` (Remote), `3` (Hybrid), etc. |
| `fecha_publicacion` | `f_TPR` | Publication period: `r86400` (24 hours), `r604800` (7 days), etc. |
| `nivel_experiencia` | `f_JT` | Experience level: `1` (internship), `2` (entry), `3` (associate), etc. |

The set order is defined by the value `set_indice` (starting at 0); an empty set (`keywords` not defined) means the base search.

The complete list of official filter sets per source is defined in the system configuration (`config.yaml`, section `fuentes`) and cannot be modified without updating the official documentation.

### 6.3. Capture policies (defaults)

The capture limits and pauses shall use the following default policies, defined in the system configuration and applicable when the source does not define its own values:

| Policy | Default | Scope |
|---------------------------|-------------------------------------|--------------------------------------|
| `max_paginas` | Configured globally | Pagination consumption of a set |
| `max_ofertas_por_corrida` | Configured globally | Total captured offers per run |
| `pausa_entre_lotes` | Configured globally | Minimum interval between batches |
| `estrategia_anti_bloqueo` | `pausa_aleatoria` | Mitigation strategy (`pausa_aleatoria` / `retraso_fijo` / `none`) |

The defaults above are not hardcoded values: the actual values are defined in `config/config.yaml` (section `captura`) and are resolved applying the global default unless the source defines specific values (see `politicas_de_captura` per source).

---

### 6.4. Treatment of captcha/blocking

When the platform shows a captcha or blocking evidence during entry or search, the run shall be terminated with the corresponding status defined in the error catalog (DOC-06, Section 11):

| Evidence | `codigo_motivo` | Result |
|---------------------------|------------------|--------------------------------|
| Challenge/captcha shown | `bloqueo_plataforma` | Abort, Group A (no retry) |
| Session expired | `sesion_expirada` | Abort the batch, controlled re-entry permitted |

Retrying after a captcha is expressly prohibited: it increases the account blocking risk (DE-LI-006, DE-LI-007). The current run shall be aborted and the evidence must be logged without preserving credentials.

---

## 7. Document index

### Document structure

1. Purpose of the document.
2. Principles of source research.
3. Criteria for selecting job sources.
4. General recommendations.
5. Acceptance criteria.
6. LinkedIn implementation specification for Module 1.
7. Document index.

---

### Annexes

The following annexes are part of the supporting documentation for this document and aim to preserve the traceability of the research, analysis, and decision-making process carried out during the selection of job platforms.

**Annex A.** Decisions derived from the platform analysis.

It shall contain the strategic decisions adopted specifically for the analyzed platform, including the justifications that gave rise to each of them.

**Annex B.** Research conducted.

It shall contain the research, comparative analyses, experimental results, and other evidence gathered during the platform evaluation process.

Each new platform incorporated into the project shall have its own annexes of decisions and research, maintaining independence between the specific documentation for each job source.
