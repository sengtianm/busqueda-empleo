# Appendix A
# Strategic Decision Log – LinkedIn

## A.1 Objective

This appendix records the strategic decisions made during the research, analysis, and evaluation process of LinkedIn as the official job opportunity search platform for the first version (MVP) of the automation.

Each decision documents an approved conclusion reached during the preparation of Document 9 and constitutes the project's official position regarding the use of LinkedIn.

The purpose of this log is to maintain traceability between the evidence obtained during research, the conclusions reached, and the decisions that will condition the design and operation of the automation.

The decisions included in this appendix are specific to LinkedIn. If a new job platform is incorporated in the future, an independent strategic decision log must be prepared for that platform.

---

# DE-LI-001. LinkedIn as official MVP platform

## Related chapter

4. Target platforms.

## Decision

LinkedIn is established as the only official platform for job opportunity searching during the first version (MVP) of the automation.

The incorporation of other platforms is outside the scope of the MVP and will be evaluated in future stages of the project using the same research and analysis process defined in Document 9.

## Justification

The research conducted concluded that LinkedIn offers the best balance between job opportunity coverage, quality of available information, technical automation possibilities, and compatibility with the objectives defined for the project.

Although it presents technical and operational restrictions inherent to the platform, the benefits obtained outweigh the identified limitations.

## Implications for the project

- All MVP development will be carried out exclusively on LinkedIn.
- Document 9 is limited to the analysis of this platform.
- The project architecture must allow incorporating new platforms without affecting the decisions made for LinkedIn.

---

# DE-LI-002. Approval of LinkedIn as official opportunity source

## Related chapter

5. Analysis of each platform.

## Decision

LinkedIn is approved as the official source of job opportunities for the automation.

The job offers published on the platform constitute the primary source of information that will feed the project's opportunity discovery process.

The platform will be used solely to retrieve job offers, and the evaluation of their relevance will be the exclusive responsibility of the automation.

## Justification

The functional analysis showed that LinkedIn provides broad coverage of job opportunities, a sufficiently consistent offer structure, and a set of filters that allows building search strategies aligned with the user's professional profile.

The research also confirmed that the platform provides the necessary information to perform an initial evaluation of most offers.

## Implications for the project

- LinkedIn becomes the official source of opportunity discovery.
- The automation will use the retrieved information as input for subsequent stages of the process.
- LinkedIn's recommendation algorithms will not determine which offers continue within the project's evaluation flow.

---

# DE-LI-003. Official LinkedIn access mechanism

## Related chapter

6. APIs and access mechanisms.

## Decision

The automation will access LinkedIn through an authenticated session using the interaction mechanism selected during research.

Official LinkedIn APIs will not be used to obtain job opportunities because they do not provide the functionalities required by the project.

Authentication becomes part of the normal operation of the automation and is no longer considered an optional mechanism.

## Justification

During the research, the different mechanisms available to access LinkedIn Jobs information were analyzed.

Initially, working without authentication was considered viable; however, the practical validation subsequently performed demonstrated that the job search engine requires logging in to properly access the functionalities needed for the project.

Based on this evidence, the exclusively visitor-based operation strategy was discarded and an authenticated access model was adopted.

## Implications for the project

- Authenticated session management becomes part of the automation's operational flow.
- The solution design must include secure mechanisms to start, maintain, and end the user session.
- Protecting the account used by the automation becomes a priority project requirement.

# DE-LI-004. Official information extraction method

## Related chapter

7. Information extraction methods.

## Decision

Job opportunities will be obtained through a controlled extraction process, designed to retrieve only the information necessary for subsequent stages of the automation.

Extraction will be limited to the data required to evaluate each offer and build the internal opportunity record, avoiding collecting information that does not add value to the process.

The automation will obtain information directly from job offers published on LinkedIn, using the access mechanism approved for the project.

## Justification

The research showed that job offers published on LinkedIn contain, in most cases, the information needed to perform an initial evaluation of their relevance.

It also showed that collecting additional information does not provide significant benefits and unnecessarily increases complexity, execution time, and operational risk.

For this reason, an extraction method focused exclusively on information relevant to the evaluation process was adopted.

## Implications for the project

- Extraction will focus only on the information needed for the project.
- The discovery process will avoid collecting irrelevant information.
- Resource consumption during automation execution will be reduced.
- Maintenance will be simpler by limiting the amount of information dependent on LinkedIn's structure.

---

# DE-LI-005. Technical and legal restrictions

## Related chapter

8. Technical and legal restrictions.

## Decision

The automation design will incorporate the technical and operational limitations identified during the LinkedIn research as project restrictions.

It is acknowledged that LinkedIn implements mechanisms aimed at protecting the platform against automated behaviors, and that these mechanisms condition how the automation must interact with the site.

Consequently, the project adopts a conservative interaction strategy, prioritizing solution stability and user account protection over execution speed or volume of information obtained.

## Justification

The research identified restrictions related to platform access, action automation, non-human behavior detection mechanisms, and limitations inherent to LinkedIn Jobs' operation.

These restrictions do not prevent developing the automation, but they do condition how it must be implemented.

Incorporating them from the analysis stage reduces the risk of later redesigns and allows building a more stable and sustainable solution.

## Implications for the project

- The identified restrictions become part of the project requirements.
- The architecture must be designed considering these limitations from the start.
- Future technical decisions must respect these restrictions.
- Stability and sustainability will take priority over implementation speed.

---

# DE-LI-006. Terms of use and compliance criteria

## Related chapter

9. Terms of use and compliance considerations.

## Decision

The project acknowledges that LinkedIn establishes terms of use and restrictions related to the automation of its platform.

As a consequence, the automation will be designed to minimize the operational risk associated with its use through limited, controlled interaction aligned with behavior similar to that of a legitimate user.

Protecting the account used by the automation is adopted as one of the project's operational principles.

## Justification

The research identified that the main risk to project continuity is not obtaining information, but rather the potential restrictions LinkedIn could apply to an account when it detects behaviors incompatible with normal platform use.

For this reason, subsequent technical decisions must be aimed at reducing this risk without compromising the automation's functional objectives.

## Implications for the project

- Account protection will take priority during solution design.
- Aggressive or unnecessary interaction strategies will be avoided.
- Decisions related to automation must always assess their impact on operational risk.
- Continuity of automation operation will prevail over maximizing query volume.

# DE-LI-007. Risks associated with LinkedIn use

## Related chapter

10. Risks by platform.

## Decision

The main risk identified for using LinkedIn does not relate to information availability, but rather to the possibility that the platform may detect automated behavior and apply restrictions to the account used by the automation.

As a consequence, the project adopts operational risk mitigation as a design criterion over maximizing performance or execution speed.

The identified risks are classified as follows:

- Risk of temporary or permanent account restriction.
- Risk of changes to LinkedIn's interface or operation.
- Risk of modifications to platform usage policies.
- Risk of failures caused by technical changes in the job search process.
- Risk of loss of automation stability as a result of changes introduced by LinkedIn.

## Justification

The research showed that most relevant risks do not affect the technical ability to develop the automation, but rather its operational continuity.

It also concluded that these risks can be significantly reduced through design decisions adopted from the early stages of the project.

For this reason, risk management is no longer an activity that comes after development and becomes part of the fundamental principles of automation design.

## Implications for the project

- All technical decisions must consider their impact on operational risk.
- The architecture must facilitate adaptation to future platform changes.
- Automation behavior should approximate that of a legitimate user.
- Account protection will take priority over execution speed and query volume.

---

# DE-LI-008. Official query frequency

## Related chapter

11. Recommended query frequency.

## Decision

The automation will execute queries to LinkedIn at a moderate frequency, sufficient to identify new job opportunities without generating an activity pattern that unnecessarily increases risk to the user account.

The execution frequency will not be set seeking the highest possible number of queries, but rather the best balance between opportunity coverage, information freshness, and operational safety.

During the MVP, continuous queries or executions with excessively short intervals will not be performed.

## Justification

The research concluded that a higher query frequency does not guarantee a proportional improvement in the quality of opportunities obtained.

On the contrary, unnecessarily increasing the number of queries raises operational risk without providing significant benefits for the project's objectives.

A controlled execution strategy was determined to offer a more suitable balance between efficiency and sustainability.

## Implications for the project

- The execution frequency will be defined as a configurable parameter of the automation.
- The system will avoid repetitive query patterns.
- The execution strategy will prioritize project stability over constant result updates.
- Execution planning will be part of the operational risk mitigation strategy.

---

# DE-LI-009. Official opportunity prioritization strategy

## Related chapter

12. Source prioritization strategy.

## Decision

The automation will use a query strategy designed to maximize the retrieval of opportunities compatible with the user's professional profile, while simultaneously reducing the volume of irrelevant offers.

Opportunity prioritization will not depend on LinkedIn's recommendation algorithm.

The platform will be used exclusively to retrieve job offers; the decision on which ones continue within the process will be made by the evaluation system defined by the project.

The query strategy will leverage the filters available on LinkedIn to reduce the number of offers that enter the evaluation process, including, among others:

- keywords related to the professional profile;
- geographic location;
- work modality;
- publication date;
- experience level;
- other filters that add value to the discovery process.

## Justification

The research showed that LinkedIn partially personalizes results using profile and history information.

However, it also showed that a properly designed query strategy allows more consistent control over the quality of the initial set of opportunities that will be evaluated by the automation.

Delegating prioritization to LinkedIn's algorithm would reduce process transparency and limit the project's control over selection criteria.

## Implications for the project

- The query strategy becomes the first opportunity filtering mechanism.
- The evaluation system will be the sole responsible for determining the relevance of each offer.
- The quality of the discovery process will mainly depend on query design and not on LinkedIn's recommendations.
- The query strategy may evolve over time without modifying the overall automation architecture.

---

# A.2 Final observations

This log brings together the strategic decisions made during the LinkedIn analysis carried out in Document 9.

Each decision is supported by the research conducted during this stage of the project and represents the official position adopted for the first version (MVP) of the automation.

These decisions constitute the reference framework for architecture design, implementation of LinkedIn-related components, and future stages of the project.

Should LinkedIn significantly modify its operation, access mechanisms, or usage policies, the affected decisions must be reviewed using the same research methodology applied during the preparation of Document 9.

The incorporation of new job platforms will require the preparation of an independent strategic decision log for each platform, maintaining independence between analyses and preserving the traceability of the decisions made.
