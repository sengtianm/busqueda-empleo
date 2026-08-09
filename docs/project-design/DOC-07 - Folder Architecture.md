# Document 7 – Folder Architecture (Optimized)

---

## 1. Purpose

Defines the official folder and file architecture of the job search automation. Establishes a uniform structure for the physical organization of all project resources, ensuring consistency, clarity, maintainability, scalability, and ease of navigation throughout the lifecycle.

**Scope:** Mandatory for all modules, processes, components, resources, files, and directories, as well as any future extension, refactoring, or incorporation of new elements.

**Normative basis:** Complements Documents 0–6 (Glossary, Functional Requirements, Non-Functional Requirements, Decision Model, Data Flow, Project Standards, Error Handling).

---

## 2. Transversal Principles

These principles apply to **every** aspect of the folder architecture. Individual chapters reference them implicitly; only chapter-specific rules are listed per section.

| ID | Principle | Definition |
|---|---|---|
| PAC-001 | Uniform organization | Single organizational model. No alternative structures permitted. |
| PAC-002 | Single responsibility | Each directory has one clearly defined purpose. No mixed-nature storage where specific directories exist. |
| PAC-003 | Logical hierarchy | Structure reflects functional organization; navigable without technical implementation knowledge. |
| PAC-004 | Scalability | New modules/resources incorporable without major reorganization. |
| PAC-005 | Technological independence | Organization independent of language, framework, provider, or tool. Remains valid when technology changes. |
| PAC-006 | Predictable location | Every resource stored in a predefined, easily identifiable location per these rules. |
| PAC-007 | No duplication | Same resource not stored in multiple locations without documented, approved justification. |
| PAC-008 | Separation of responsibilities | Documents, configurations, data, prompts, logs, source code, temporary resources, and other elements kept in independent directories. |
| PAC-009 | Structural consistency | All modules with equivalent components respect the same internal folder organization. |
| PAC-010 | Ease of maintenance | Architecture facilitates location, modification, replacement, and deletion without unnecessary impact on other components. |
| PAC-011 | Documentary compatibility | Physical organization aligned with official documentation and Project Standards conventions. |
| PAC-012 | Controlled evolution | Any modification documented, justified, and approved before taking effect. |
| PAC-013 | Traceability | Location of each resource allows identification of its function, module, and relationships. |
| PAC-014 | Reusability | Structure favors reuse of common resources; avoids unnecessary copies or redundant structures. |
| PAC-015 | Mandatory compliance | Every folder, file, or resource must respect these rules before being considered part of the architecture. |

---

## 3. General Project Structure

Defines highest-level organization. Top-level directories differentiated by functional responsibility.

### Rules

| ID | Rule |
|---|---|
| EGP-001 | Top-level directories group resources sharing the same functional responsibility. No generic directories for mixed-nature resources. |
| EGP-002 | Official documentation completely separate from implementation resources. |
| EGP-003 | Configuration files stored independently from execution logic. |
| EGP-004 | Data kept separate from components responsible for processing it. |
| EGP-005 | Temporary resources in specific locations; cleanup/regeneration without affecting permanent information. |
| EGP-006 | Each functional module has a clearly delimited space; no unnecessary physical dependencies between modules. |
| EGP-007 | Resources used by multiple modules located in officially defined shared directories; no file duplication. |
| EGP-008 | Common configurations stored in a single location for maintenance and version control. |
| EGP-009 | All official documentation organized under a single document structure per Document 5. |
| EGP-010 | Operational logs, audits, and tracking files stored exclusively in specific locations. |

### Official Directory Tree

```
/
 ├── docs/                  # Official project documentation
 │   ├── project-design/    # Design documents (DOC-00 to DOC-13, appendices)
 │   ├── diagrams/          # Diagrams
 │   ├── plans/             # Plans
 │   ├── reports/           # Execution reports
 │   └── history/           # Session history and tracking
 │
 ├── config/                # System configuration
 │
 ├── prompts/               # Official prompts
 │
 ├── modules/               # Functional modules
 │   ├── discovery/
 │   ├── preparation/
 │   ├── evaluation/
 │   ├── processing/
 │   └── management/
 │
 ├── shared/                # Reusable resources
 │
 ├── data/                  # Persistent data
 │   ├── input/
 │   ├── processing/
 │   ├── output/
 │   └── backup/
 │
 ├── logs/                  # Logs and audit
 │
 ├── temp/                  # Temporary files
 │
 ├── scripts/               # Auxiliary scripts
 │
 ├── tests/                 # Tests
 │
 └── README.md              # General project information
```

---

## 4. Directory Organization

| ID | Rule |
|---|---|
| ODR-001 | Entire project contained within a single root directory (entry point). No resource stored outside this structure. |
| ODR-002 | Only officially defined top-level directories may exist. Each represents a clearly differentiated functional category. |
| ODR-003 | Logical hierarchy: each level specializes the upper level. Depth kept reasonable for navigation. |
| ODR-004 | Each directory stores only resources related to its purpose. No generic storage for unclassified files. |
| ODR-005 | Shared resources in officially defined shared directories. No independent copies per module. |
| ODR-006 | Each functional module has its own space. Module-exclusive resources remain within its directory. |
| ODR-007 | Temporary resources, intermediate files, and execution data in directories independent from permanent resources. Cleanup without affecting official information. |
| ODR-008 | Equivalent structures across modules maintain the same internal directory organization. |
| ODR-009 | Directory names comply with Project Standards conventions. No ambiguous, duplicate, or technology-specific names. |
| ODR-010 | New directories respond to clearly identified functional need. No preventive folders for non-existent functionality. |
| ODR-011 | Deletion/reorganization requires prior verification that no active component depends on contained resources. |
| ODR-012 | Organization facilitates version control; automatically generated resources that can be rebuilt are not permanently stored. |

---

## 5. File Organization

| ID | Rule |
|---|---|
| OAR-001 | Every file stored in a single official directory. No multiple copies without documented, approved justification. |
| OAR-002 | Each file fulfills a single clearly defined function. No concentrated independent responsibilities when logically separable. |
| OAR-003 | Files grouped by nature. Minimum categories: Documentation, Configuration, Prompts, Data, Logs, Shared resources, Temporary resources, Scripts, System components. |
| OAR-004 | All files respect official naming conventions (Project Standards Document). |
| OAR-005 | Equivalent modules maintain the same internal file organization. |
| OAR-006 | Manually maintained files stored separately from automatically generated files. |
| OAR-007 | Files used by multiple modules kept in officially defined shared locations. No local copies per module. |
| OAR-008 | Temporary files stored only in designated directories; permanence exclusively transitory. |
| OAR-009 | System configuration centralized. No unnecessarily distributed configurations. |
| OAR-010 | Official documentation organized per the document architecture. |
| OAR-011 | Data files (processed information) kept separate from implementation files. |
| OAR-012 | Automatically generated files that can be rebuilt are not part of permanent project content. |
| OAR-013 | No file depends on ambiguous or changing physical paths. References between files remain consistent throughout evolution. |

---

## 6. Resource Location Conventions

| ID | Rule |
|---|---|
| CUR-001 | Every resource stored in the directory whose functional responsibility matches its nature. Location never defined by temporary convenience. |
| CUR-002 | Resources used by only one module remain within that module's structure. Not stored in shared locations. |
| CUR-003 | Resources reused by several modules located exclusively in shared-resource directories. No independent copies. |
| CUR-004 | Official documentation kept separate from resources used during execution. |
| CUR-005 | Configuration files grouped in official locations. Not distributed among modules without documented technical justification. |
| CUR-006 | Temporary resources stored only in transient-file locations. Not considered permanent architecture. |
| CUR-007 | Resources requiring preservation between executions located exclusively in permanent-storage directories. |
| CUR-008 | Automatically generated resources stored according to their nature, clearly distinguished from manually maintained resources. |
| CUR-009 | Logs, evidence, metrics, and audit resources grouped in specific locations for consultation. |
| CUR-010 | Test resources completely separate from normal-operation resources. |
| CUR-011 | Resources from external platforms/services/sources identified and organized independently from project-owned resources. |
| CUR-012 | Obsolete resources not mixed with active resources. Treatment follows official maintenance, archiving, or deletion policies. |
| CUR-013 | Location assigned to a resource remains stable throughout its lifecycle unless officially approved reorganization. |

---

## 7. Documentation Organization

| ID | Rule |
|---|---|
| ORD-001 | All official documentation within a single document structure. Not distributed across multiple locations without approved justification. |
| ORD-002 | Documents organized by purpose. Minimum categories: Strategic, Functional, Technical, Architecture, Standards, Annexes, Diagrams, Manuals, Histories, References. |
| ORD-003 | Official documents completely separate from files used during execution. |
| ORD-004 | Every document stored in a location predefined by the document architecture. Location independent of author or creation time. |
| ORD-005 | Each official document exists in only one current version within active documentation. No multiple active copies. |
| ORD-006 | Annexes organized independently from main documents. Each annex explicitly references the document it complements. |
| ORD-007 | Official diagrams grouped by process, module, or document they belong to. |
| ORD-008 | Historical versions, change logs, and construction conversations kept separate from current documentation. Preserved for audit and traceability. |
| ORD-009 | Documents generated by automated processes clearly identified to differentiate from manually maintained ones. |
| ORD-010 | Inter-document dependencies established through official references, avoiding content duplication. |
| ORD-011 | Historical documentation not deleted while it provides value for audits, decision reconstruction, or project evolution. |

---

## 8. System Configuration Organization

| ID | Rule |
|---|---|
| OCS-001 | All configuration centralized within official architecture. No equivalent configurations distributed among modules without documented technical justification. |
| OCS-002 | Configuration completely separate from business logic and implementation. No hardcoded configurable values. |
| OCS-003 | Configurations organized by component, process, or functional scope. Each has a clearly defined purpose. |
| OCS-004 | Configurations used by multiple modules defined once and shared through official mechanisms. |
| OCS-005 | Each configuration identified by a unique, descriptive name indicating its purpose. |
| OCS-006 | Every modification identifiable, documentable, and justifiable. |
| OCS-007 | When multiple execution environments exist, environment-specific configurations clearly differentiated without altering general structure. |
| OCS-008 | Configurations containing sensitive information managed through secure mechanisms defined by system architecture. |
| OCS-009 | Obsolete configurations not deleted without verifying no active component depends on them. |

---

## 9. Prompt Organization

| ID | Rule |
|---|---|
| ORP-001 | All official prompts stored within a single structure exclusively for their administration. Not distributed among system components. |
| ORP-002 | Prompts completely separate from implementation logic. No prompt text embedded in system components. |
| ORP-003 | Prompts organized by process, module, or functional responsibility. |
| ORP-004 | Prompts usable by multiple modules: single shared official version. No independent copies. |
| ORP-005 | Every prompt has a unique identifier per Project Standards conventions. |
| ORP-006 | Every modification allows clear version identification and history preservation. |
| ORP-007 | Prompts classified by operational purpose. Minimum: Classification, Extraction, Evaluation, Generation, Validation, Correction, Verification, Operational support. |
| ORP-008 | Variables used by a prompt clearly defined and documented, following official conventions. |
| ORP-009 | Prompts designed for compatibility with future automation modifications. New modules don't require redesigning existing prompts without technical justification. |
| ORP-010 | Prompt usage identifiable during execution for audit and analysis. |
| ORP-011 | All prompts maintain uniform structure per official templates and standards. |

---

## 10. Data Organization

| ID | Rule |
|---|---|
| ODT-001 | Data organized by purpose. Minimum differentiation: Input, In processing, Persistent, Historical, Temporary, Backup. |
| ODT-002 | Data completely separate from components responsible for processing it. Organization independent of technical implementation. |
| ODT-003 | When necessary, data organized by functional module with uniform structure throughout. |
| ODT-004 | Data used by multiple modules managed through centralized mechanisms. No independent copies compromising consistency. |
| ODT-005 | Data requiring preservation between executions stored using official mechanisms. |
| ODT-006 | Temporary data completely separate from persistent data. Permanence limited to necessary execution time. |
| ODT-007 | Information for audit, analysis, traceability, or reconstruction kept separate from operational data. |
| ODT-008 | Organization permanently preserves integrity, consistency, and reliability of information. |
| ODT-009 | Data structure changes identifiable and under control when project evolution requires it. |
| ODT-010 | Data requiring preservation per project policies kept available per official storage and audit rules. |

---

## 11. Log Organization

| ID | Rule |
|---|---|
| ORL-001 | All official logs stored within a single structure. No distribution among modules without documented technical justification. |
| ORL-002 | Logs organized by purpose. Minimum: Operational, Audit, Error, Event, Execution, Diagnostic. |
| ORL-003 | Logs completely separate from components generating them. System logic does not depend on log physical location. |
| ORL-004 | All modules record information following a uniform structure per official standards. |
| ORL-005 | Every log identifies at minimum: date/time, responsible module, associated process, event type, operation result, related identifier (when applicable). |
| ORL-006 | Logs kept intact once generated. No modification except through officially authorized procedures. |
| ORL-007 | Active (daily operation) logs separate from historical/audit logs. |
| ORL-008 | Log organization compatible with Document 6 (Error Handling) and Document 5 (Project Standards). |
| ORL-009 | Logs organized for easy consultation, analysis, and retrieval. |
| ORL-010 | Multiple components generating equivalent logs use the same organizational structure. |
| ORL-011 | Classification and organization uniform throughout project evolution. No alternative structures for same log type. |

---

## 12. Temporary Resource Organization

| ID | Rule |
|---|---|
| ORT-001 | All temporary resources stored exclusively in designated locations. Never mixed with permanent resources. |
| ORT-002 | Every temporary resource exists only for the time necessary for the process requiring it. |
| ORT-003 | When preservation during execution is necessary, organized by generating process/module. |
| ORT-004 | Temporary resources never become permanent dependencies. Normal execution does not depend on previously stored temporary information. |
| ORT-005 | Every temporary resource regenerable automatically. Loss does not compromise project continuity. |
| ORT-006 | Deletion/reuse through controlled mechanisms. No indefinite accumulation. |
| ORT-007 | Temporary resources not used as permanent mechanism for audit, traceability, or historical storage. |
| ORT-008 | Organization compatible with error handling, recovery, and traceability policies. |
| ORT-009 | Existence, modification, or deletion of temporary resources does not affect permanent data or official documentation. |
| ORT-010 | Every temporary resource relatable to: generating process, module, associated execution, operational purpose. |
| ORT-011 | Reuse during same execution permitted only when system consistency is not compromised. |
| ORT-012 | All modules follow the same rules for generation, use, and deletion of temporary resources. |

---

## 13. Script and Utility Organization

| ID | Rule |
|---|---|
| OSU-001 | Scripts/utilities completely separate from functional modules. Their existence does not alter main system component organization. |
| OSU-002 | Each script/utility fulfills a single clearly defined responsibility. No grouped independent functions when separable. |
| OSU-003 | Organized by operational purpose. Minimum: Automation, Maintenance, Migration, Conversion, Validation, Diagnosis, Administration, Development support. |
| OSU-004 | Scripts usable by multiple processes kept as reusable resources. No independent copies. |
| OSU-005 | Automation can execute main processes without depending on auxiliary scripts for maintenance/administration. |
| OSU-006 | Every script/utility has clear identification for immediate purpose recognition. |
| OSU-007 | Scripts remain compatible with Project Standards conventions and general architecture. |
| OSU-008 | Every significant modification identifiable, documentable, justifiable. |
| OSU-009 | Every script/utility relatable to: supported process, module (if applicable), operational purpose, modification history. |
| OSU-010 | Scripts for administrative/maintenance tasks designed to avoid affecting information integrity or automation stability. |
| OSU-011 | No redundant utilities duplicating existing functionalities. |
| OSU-012 | Unused scripts removed in controlled manner after verifying no active process depends on them. |

---

## 14. Directory Dependency Rules

| ID | Rule |
|---|---|
| RDD-001 | Every dependency between directories responds to a clearly identified functional need. No convenience-only dependencies. |
| RDD-002 | Architecture minimizes dependencies. Each component maintains highest possible independence. |
| RDD-003 | Dependencies do not modify a directory's main responsibility. Each retains a single function. |
| RDD-004 | Dependencies kept unidirectional whenever possible. Circular dependencies avoided. |
| RDD-005 | Resources needed by several directories located in officially defined shared structure. No dependencies through resource copies. |
| RDD-006 | Each functional module independent from other modules' internal structure. Inter-module interaction only through mechanisms defined by architecture. |
| RDD-007 | Configuration directories may be used by multiple components, but configurations do not depend on consuming modules. |
| RDD-008 | Documentation may reference any component without generating operational dependencies between directories. |
| RDD-009 | Temporary resources never become permanent dependencies of any directory. |
| RDD-010 | New directories do not break previously defined dependencies or unnecessarily affect existing components. |
| RDD-011 | Before deleting a directory, verify no other component maintains active dependencies toward it. |
| RDD-012 | Every dependency identifiable, justifiable, and documentable. |
| RDD-013 | Dependency rules applied uniformly. No undocumented exceptions. |

---

## 15. Incorporating New Modules

| ID | Rule |
|---|---|
| RIM-001 | Every new module responds to a clearly identified, documented functional need. No modules whose responsibility is already covered. |
| RIM-002 | Each module has a single clearly defined purpose. No multiple or ambiguous responsibilities. |
| RIM-003 | New modules respect folder architecture, organizational conventions, and project standards. |
| RIM-004 | New modules adopt the same organizational structure as existing modules when component nature is equivalent. |
| RIM-005 | Before creating new resources, verify reusable components exist. No duplication of available functionality. |
| RIM-006 | Dependencies kept to necessary minimum, respecting official dependency rules. |
| RIM-007 | Incorporation accompanied by update of corresponding official documentation. Physical architecture and documentation synchronized. |
| RIM-008 | Incorporation respects naming, identifier, documentation, configuration, logging, and other official conventions. |
| RIM-009 | New resources do not compromise integrity, consistency, or traceability of managed data. |
| RIM-010 | New modules implement official error detection, logging, recovery, and treatment policies (Document 6). |
| RIM-011 | Incorporation does not require significantly reorganizing existing architecture. |
| RIM-012 | Before approval, verify compliance with all architectural rules in official documentation. |
| RIM-013 | Every incorporation documents: purpose, scope, responsibilities, dependencies, affected documents, incorporation date. |
| RIM-014 | Every incorporation formally approved before integration. Subsequent modifications follow the same procedure. |

---

## 16. Restrictions

| ID | Restriction |
|---|---|
| RAP-001 | No more than one official folder architecture per project. |
| RAP-002 | No directories without clearly defined, documented responsibility. |
| RAP-003 | No multiple directories for the same resource type when a single location suffices. |
| RAP-004 | No mixing resources of different functional categories in the same directory when specific locations exist. |
| RAP-005 | No circular dependencies between modules, directories, or architecture components. |
| RAP-006 | No dependence on undocumented or dynamically created folder structures outside official organization. |
| RAP-007 | No significant modification without corresponding official documentation update. |
| RAP-008 | No project resources stored outside official structure except in exceptional, approved, documented cases. |
| RAP-009 | No module forced to know another module's internal structure to fulfill its responsibilities. |
| RAP-010 | Folder organization not designed based on specific tools, frameworks, languages, or providers. |
| RAP-011 | No equivalent configurations unnecessarily distributed among different components. |
| RAP-012 | No temporary resources becoming permanent storage or part of stable structure. |
| RAP-013 | No deletion of directory, file, or official resource without prior dependency verification. |
| RAP-014 | Physical architecture and official documentation must not evolve independently. Modifications synchronized. |
| RAP-015 | No resource, module, or component failing Project Standards conventions or this document's provisions may be incorporated. |

---

## 17. Acceptance Criteria

The architecture is compliant only when **all** of the following are simultaneously met:

| ID | Criterion |
|---|---|
| CAP-001 | Consistent organization in all directories and resources per these rules. |
| CAP-002 | Each directory and resource has a single clearly identifiable responsibility. No functional ambiguities. |
| CAP-003 | Clear separation between: Documentation, Configuration, Prompts, Data, Logs, Temporary resources, Scripts/utilities, Functional components. |
| CAP-004 | Entire architecture respects Project Standards conventions. |
| CAP-005 | Physical structure fully aligned with official documentation. No differences. |
| CAP-006 | New modules incorporable without significant reorganization. |
| CAP-007 | Organization independent of specific technologies, tools, or providers. |
| CAP-008 | Dependencies between directories at necessary minimum, respecting official rules. |
| CAP-009 | Location of each resource allows identification of: purpose, module, relationships, associated documentation. |
| CAP-010 | No duplicities, inconsistencies, or unauthorized dependencies. |
| CAP-011 | Every modification previously documented, justified, and approved. |
| CAP-012 | Every new module, resource, or directory incorporable while fully respecting these rules. |
| CAP-013 | Organizational uniformity across all automation modules. |
| CAP-014 | Organization facilitates review, audit, and verification of any resource. |
| CAP-015 | **All** criteria met simultaneously for approval. |

---

## 18. Normative References

This architecture shall remain permanently aligned with:
- Document 0 — Project Glossary
- Document 1 — Functional Requirements
- Document 2 — Non-Functional Requirements
- Document 3 — Decision Model
- Document 4 — Data Flow
- Document 5 — Project Standards
- Document 6 — Error Handling

Any modification shall maintain compatibility with these documents and any subsequently approved official update.
