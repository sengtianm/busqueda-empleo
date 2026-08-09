# Appendix A
## Strategic Decision Log – LinkedIn

### A.1 Objective

This appendix records the strategic decisions from the research, analysis, and evaluation of LinkedIn as the official job opportunity search platform for the first automation version (MVP). Each decision documents an approved conclusion from Document 9 preparation and constitutes the project's official position on LinkedIn use. The log maintains traceability among research evidence, conclusions, and decisions conditioning automation design and operation. These decisions are LinkedIn-specific; each future job platform requires an independent strategic decision log.

### DE-LI-001. LinkedIn as official MVP platform

**Related chapter:** Target platforms.

**Decision:** LinkedIn is the only official platform for job opportunity searching during the automation MVP. Other platforms are outside MVP scope and will be evaluated in future stages using the same research and analysis process defined in Document 9.

**Justification:** LinkedIn offers the best balance of job opportunity coverage, information quality, technical automation possibilities, and compatibility with project objectives. Its benefits outweigh the identified technical and operational platform restrictions.

**Implications for the project:** All MVP development is carried out exclusively on LinkedIn. Document 9 is limited to LinkedIn analysis. Project architecture must allow incorporating new platforms without affecting LinkedIn decisions.

### DE-LI-002. Approval of LinkedIn as official opportunity source

**Related chapter:** Analysis of each platform.

**Decision:** LinkedIn is approved as the official source of job opportunities for the automation. Published job offers are the primary information source feeding opportunity discovery. LinkedIn is used solely to retrieve offers; relevance evaluation is exclusively the automation's responsibility.

**Justification:** LinkedIn provides broad opportunity coverage, a sufficiently consistent offer structure, and filters enabling search strategies aligned with the user's professional profile. It also provides the information needed for an initial evaluation of most offers.

**Implications for the project:** LinkedIn is the official opportunity-discovery source. Retrieved information feeds subsequent process stages. LinkedIn recommendation algorithms will not determine which offers continue in the project's evaluation flow.

### DE-LI-003. Official LinkedIn access mechanism

**Related chapter:** APIs and access mechanisms.

**Decision:** The automation will access LinkedIn through an authenticated session using the interaction mechanism selected during research. Official LinkedIn APIs will not be used to obtain job opportunities because they do not provide the functionality required by the project. Authentication is part of normal automation operation and is not optional.

**Justification:** Research analyzed the available mechanisms for accessing LinkedIn Jobs information. Unauthenticated operation initially appeared viable, but practical validation showed that the job search engine requires login to properly access the functionalities needed by the project. Visitor-only operation was discarded; authenticated access was adopted.

**Implications for the project:** Authenticated session management is part of the automation's operational flow. Solution design must securely start, maintain, and end the user session. Protecting the account used by the automation is a priority project requirement.

### DE-LI-004. Official information extraction method

**Related chapter:** Information extraction methods.

**Decision:** Job opportunities will be obtained through controlled extraction retrieving only the information necessary for subsequent automation stages. Extraction is limited to the data required to evaluate each offer and build the internal opportunity record; data that does not add value to the process is excluded. The automation obtains information directly from published LinkedIn job offers using the approved access mechanism.

**Justification:** Published LinkedIn offers usually contain the information needed for an initial relevance evaluation. Additional data provides little benefit and unnecessarily increases complexity, execution time, and operational risk. Extraction therefore focuses only on evaluation-relevant information.

**Implications for the project:** Extraction targets only project-required information. Discovery avoids irrelevant data. Resource consumption during execution is reduced. Maintenance is simpler by limiting the amount of information dependent on LinkedIn's structure.

### DE-LI-005. Technical and legal restrictions

**Related chapter:** Technical and legal restrictions.

**Decision:** Automation design incorporates the technical and operational limitations identified during LinkedIn research as project restrictions. LinkedIn implements platform-protection mechanisms against automated behavior, and these mechanisms condition interaction with the platform. The project adopts a conservative interaction strategy, prioritizing solution stability and user account protection over execution speed or volume of information obtained.

**Justification:** Research identified restrictions related to platform access, action automation, non-human behavior detection, and LinkedIn Jobs operation. These restrictions do not prevent automation but condition its implementation. Incorporating them from the analysis stage reduces later redesign risk and supports a stable, sustainable solution.

**Implications for the project:** Identified restrictions are project requirements. Architecture must consider them from the start. Future technical decisions must respect them. Stability and sustainability take priority over implementation speed.

### DE-LI-006. Terms of use and compliance criteria

**Related chapter:** Terms of use and compliance considerations.

**Decision:** The project acknowledges LinkedIn's terms of use and restrictions related to platform automation. The automation will minimize operational risk through limited, controlled interaction aligned with behavior similar to that of a legitimate user. Protecting the account used by the automation is an operational project principle.

**Justification:** The main continuity risk is not information access but potential LinkedIn account restrictions caused by behavior incompatible with normal platform use. Technical decisions must reduce this risk without compromising the automation's functional objectives.

**Implications for the project:** Account protection is prioritized during solution design. Aggressive or unnecessary interaction strategies are avoided. Automation decisions must assess their operational-risk impact. Operational continuity prevails over query-volume maximization.

### DE-LI-007. Risks associated with LinkedIn use

**Related chapter:** Risks by platform.

**Decision:** The main LinkedIn risk is platform detection of automated behavior and restriction of the account used by the automation, not information availability. Operational risk mitigation is therefore a design criterion over maximizing performance or execution speed. Identified risks:

- Temporary or permanent account restriction.
- Changes to LinkedIn's interface or operation.
- Modifications to platform usage policies.
- Failures caused by technical changes in the job search process.
- Loss of automation stability due to LinkedIn changes.

**Justification:** Most relevant risks affect operational continuity, not the technical ability to develop the automation. Early design decisions can significantly reduce them. Risk management is therefore a fundamental automation-design principle, not a post-development activity.

**Implications for the project:** All technical decisions must consider their impact on operational risk. Architecture must facilitate adaptation to future platform changes. Automation behavior should approximate that of a legitimate user. Account protection takes priority over execution speed and query volume.

### DE-LI-008. Official query frequency

**Related chapter:** Recommended query frequency.

**Decision:** The automation will query LinkedIn at a moderate frequency sufficient to identify new job opportunities without generating an activity pattern that unnecessarily increases account risk. Frequency seeks the best balance among opportunity coverage, information freshness, and operational safety, not the maximum number of queries. The MVP will not perform continuous queries or executions with excessively short intervals.

**Justification:** Higher query frequency does not proportionally improve the quality of obtained opportunities; it raises operational risk without significant benefit. Controlled execution balances efficiency and sustainability.

**Implications for the project:** Execution frequency is a configurable automation parameter. The system avoids repetitive query patterns. Stability takes priority over constant result updates. Execution planning is part of operational-risk mitigation.

### DE-LI-009. Official opportunity prioritization strategy

**Related chapter:** Source prioritization strategy.

**Decision:** The automation will use a query strategy maximizing retrieval of opportunities compatible with the user's professional profile while reducing the volume of irrelevant offers. Prioritization will not depend on LinkedIn's recommendation algorithm. LinkedIn is used exclusively to retrieve job offers; the project's evaluation system decides which offers continue in the process. The query strategy uses LinkedIn filters, including:

- Keywords related to the professional profile.
- Geographic location.
- Work modality.
- Publication date.
- Experience level.
- Other filters that add value to discovery.

**Justification:** LinkedIn partially personalizes results using profile and history information. A properly designed query strategy provides more consistent control over the quality of the initial opportunities evaluated. Delegating prioritization to LinkedIn's algorithm would reduce transparency and limit project control over selection criteria.

**Implications for the project:** The query strategy is the first opportunity filtering mechanism. The evaluation system alone determines offer relevance. Discovery quality depends mainly on query design, not LinkedIn recommendations. The query strategy can evolve without modifying the overall automation architecture.

### DE-LI-010. Implementation criteria for Module 1

**Related chapter:** LinkedIn implementation specification (DOC-09, Section 6).

**Decision:** The "Enter the source", "Apply filters", and "Capture offers" nodes of the Opportunity Discovery module (Module 1) shall follow DOC-09, Section 6. Official implementation criteria:

- Entry succeeds only when a verifiable authenticated-session DOM criterion is met within `timeout_ingreso`, using LinkedIn `global-nav` as official authenticated-session evidence.
- Queries are composed from official filter sets defined in system configuration, mapping each field to the corresponding LinkedIn search parameter.
- Capture respects configured default policies: `max_paginas`, `max_ofertas_por_corrida`, `pausa_entre_lotes`, `estrategia_anti_bloqueo`.
- Captcha or platform-blocking evidence terminates the run with `bloqueo_plataforma` (Group A, no retry); session expiration uses `sesion_expirada` with controlled re-entry.

**Justification:** Account protection takes priority over execution volume or speed (DE-LI-006, DE-LI-007); therefore entry verification, controlled interaction, and explicit prohibition of captcha retry are mandatory. Converting platform behavior into verifiable criteria and official codes allows implementing the module nodes using only documented information.

**Implications for the project:** Module 1 requires a verifiable entry criterion per source. Filter mapping is configuration-defined, not hardcoded. Capture limits and pauses follow global configuration default policies. Captcha/blocking handling is governed by the DOC-06, Section 11 error catalog.

### A.2 Final observations

This log gathers the strategic decisions from Document 9's LinkedIn analysis. Each decision is supported by the research conducted during this stage and represents the official position adopted for the first automation version (MVP). These decisions are the reference framework for architecture design, LinkedIn component implementation, and future project stages. If LinkedIn significantly modifies its operation, access mechanisms, or usage policies, affected decisions must be reviewed using the same research methodology applied in Document 9. New job platforms require independent strategic decision logs, preserving independent analysis and decision traceability.
