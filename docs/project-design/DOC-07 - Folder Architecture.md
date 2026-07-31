# DOC-07 - Folder Architecture

## 1. Purpose of the document

This document defines the official folder and file architecture of the job search automation.

Its purpose is to establish a uniform structure for the physical organization of all resources that make up the project, ensuring consistency, clarity, maintainability, scalability, and ease of navigation throughout its lifecycle.

This document constitutes the official reference for the location, organization, and distribution of documents, modules, configurations, data, prompts, logs, scripts, auxiliary resources, and other elements that integrate the automation, regardless of the technology used for its implementation.

Likewise, it defines the necessary guidelines to ensure that all project components are stored following a predictable structure, avoiding duplicities, unnecessary dependencies, and disorganization as the automation evolves.

The provisions contained in this document shall be mandatory for all modules, processes, components, resources, files, and directories of the project, as well as for any future extension, refactoring, or incorporation of new elements to the architecture.

---

## 2. Principles of the folder architecture

The following principles establish the general rules that shall govern the design, organization, maintenance, and evolution of the folder architecture of the job search automation.

These principles complement the Project Glossary, the Functional Requirements, the Non-Functional Requirements, the Decision Model, the Data Flow, the Project Standards, and the Error Handling Model, constituting the normative basis to guarantee a uniform organization of all project resources.

---

### PAC-001. Uniform organization

The entire folder structure shall follow a single organizational model defined by this document.

No alternative structures that generate inconsistencies within the project shall be permitted.

---

### PAC-002. Single responsibility

Each directory shall have a single clearly defined purpose.

Storing resources of a different nature when a specific directory exists for them shall not be permitted.

---

### PAC-003. Logical hierarchy

The folder structure shall reflect the functional organization of the automation, facilitating understanding of the project without relying on knowledge of its technical implementation.

---

### PAC-004. Scalability

The architecture shall allow the incorporation of new modules, resources, and components without requiring major reorganizations of the existing structure.

---

### PAC-005. Technological independence

The folder organization shall not depend on a specific programming language, framework, provider, or tool.

The structure shall remain valid even when the technologies used change.

---

### PAC-006. Predictable location

Every resource shall be stored in a predefined and easily identifiable location according to the rules established in this document.

---

### PAC-007. Avoid duplication

The same resource shall not be stored in multiple locations unless there is a documented and approved justification.

---

### PAC-008. Separation of responsibilities

Documents, configurations, data, prompts, logs, source code, temporary resources, and other elements shall be kept separated in independent directories.

---

### PAC-009. Structural consistency

All automation modules shall respect the same internal folder organization when the nature of their components is equivalent.

---

### PAC-010. Ease of maintenance

The architecture shall facilitate the location, modification, replacement, and deletion of any resource without unnecessarily affecting other project components.

---

### PAC-011. Documentary compatibility

The physical organization of the project shall remain aligned with the official documentation and with the conventions established in the Project Standards Document.

---

### PAC-012. Controlled evolution

Any modification to the folder architecture shall be documented, justified, and approved before coming into effect.

---

### PAC-013. Traceability

The location of each resource shall allow easy identification of its function, its module, and its relationship with the rest of the automation.

---

### PAC-014. Reusability

The structure shall favor the reuse of common resources, avoiding the unnecessary creation of copies or redundant structures.

---

### PAC-015. Mandatory compliance

Every folder, file, or resource incorporated into the project shall respect the rules defined in this document before being considered an official part of the architecture.

---

## General principles of the folder architecture

The folder architecture shall comply with the following principles:

- Maintain a uniform organization throughout the project.
- Facilitate navigation and location of resources.
- Favor the scalability of the automation.
- Avoid duplicities and unnecessary dependencies.
- Clearly separate the responsibilities of each directory.
- Maintain technological independence.
- Ensure traceability of resources.
- Facilitate maintenance and evolution of the project.
- Remain aligned with all official documentation.
- Serve as the single reference for the physical organization of the project.

---

## 3. General project structure

The general project structure defines the highest-level organization of the job search automation.

Its purpose is to establish a uniform physical architecture that facilitates resource location, reduces project complexity, and allows the incorporation of new components without altering the existing organization.

The entire structure shall be organized using clearly differentiated top-level directories according to their responsibility within the automation.

---

### EGP-001. Organization by responsibility

Top-level directories shall group resources that share the same functional responsibility.

Generic directories shall not be permitted for storing resources of a different nature.

---

### EGP-002. Separation between documentation and implementation

The official project documentation shall be kept completely separate from the resources used for the automation implementation.

---

### EGP-003. Separation between configuration and logic

Configuration files shall be stored in directories independent from those containing execution logic.

---

### EGP-004. Separation between data and processes

Data generated, processed, or stored by the automation shall be kept separate from the components responsible for its processing.

---

### EGP-005. Separation between permanent and temporary resources

Temporary resources shall be stored in specific locations that allow their cleanup or regeneration without affecting the permanent project information.

---

### EGP-006. Modular organization

Each functional module of the automation shall have a clearly delimited space within the general structure, avoiding unnecessary physical dependencies between modules.

---

### EGP-007. Shared resources

Resources used by multiple modules shall be located in officially defined shared directories, avoiding file duplication.

---

### EGP-008. Centralization of configurations

Common automation configurations shall be stored in a single location, facilitating their maintenance and version control.

---

### EGP-009. Centralization of documentation

All official project documentation shall be organized under a single document structure, respecting the standards defined in Document 5.

---

### EGP-010. Centralization of logs

Operational logs, audits, and tracking files shall be stored in specific locations exclusively intended for that purpose.

---

### EGP-011. Structural scalability

The incorporation of new modules, components, or resources shall not require reorganizing the main project structure.

The architecture shall support the progressive growth of the automation.

---

### EGP-012. Technological independence

The general structure shall not depend on specific tools, programming languages, or technologies.

The physical organization shall remain valid even when the technical implementation changes.

---

### EGP-013. Traceability

The physical location of any resource shall facilitate the identification of its function, its module, and its relationship with the rest of the project.

---

### EGP-014. Consistency

All components shall respect the official structure defined in this document.

No alternative directories that contradict the approved architecture may be created.

---

### EGP-015. Single source of organization

The architecture defined in this document shall constitute the only official reference for the physical organization of the project.

Any modification to the structure shall be documented and approved beforehand.

---

## Objectives of the general structure

The general project structure shall guarantee:

- Uniform organization of all resources.
- Clear separation of responsibilities.
- Ease of navigation.
- Project scalability.
- Technological independence.
- Reuse of common resources.
- Ease of maintenance.
- Compatibility with official documentation.
- Traceability of all components.
- Controlled evolution of the architecture.

---

## 4. Directory organization

The directory organization defines the official folder structure of the job search automation.

Its purpose is to establish a uniform distribution of all project resources, ensuring that each directory has a single responsibility and a predictable location within the general architecture.

The structure defined in this chapter shall be mandatory for all modules and resources that are part of the automation.

---

### ODR-001. Root directory

The entire project shall be contained within a single root directory that will act as the entry point of the architecture.

No resource belonging to the project shall be stored outside this structure.

---

### ODR-002. Top-level directories

Only top-level directories officially defined by this document may exist.

Each one shall represent a clearly differentiated functional category.

---

### ODR-003. Hierarchical organization

Directories shall be organized using a logical hierarchy, where each level represents a specialization of the upper level.

The depth of the structure shall be kept reasonable to facilitate navigation.

---

### ODR-004. Exclusive responsibility

Each directory shall store only resources related to its purpose.

Using a folder as generic storage for unclassified files shall not be permitted.

---

### ODR-005. Shared directories

Resources reused by multiple modules shall be stored in officially defined shared directories.

No module shall maintain independent copies of common resources.

---

### ODR-006. Module-specific directories

Each functional module of the automation shall have its own space within the project structure.

Resources exclusive to a module shall remain within its own directory.

---

### ODR-007. Separation between permanent and temporary resources

Temporary resources, intermediate files, and execution data shall be stored in directories independent from permanent resources.

This will allow their cleanup without affecting the official project information.

---

### ODR-008. Uniform organization

When multiple modules use equivalent structures, they shall maintain the same internal directory organization.

---

### ODR-009. Consistent names

Directory names shall comply with the official conventions defined in the Project Standards Document.

Ambiguous, duplicate, or technology-specific names shall not be permitted.

---

### ODR-010. Controlled growth

The incorporation of new directories shall respond to a clearly identified functional need.

Preventive folders for functionalities that do not yet exist may not be created.

---

### ODR-011. Controlled deletion

The deletion or reorganization of a directory shall ensure beforehand that no active component depends on the resources contained within it.

---

### ODR-012. Compatibility with versioning

The directory organization shall facilitate version control, avoiding storing automatically generated resources when they can be rebuilt during execution.

---

### ODR-013. Traceability

The physical location of any resource shall allow immediate identification of its function and the component it belongs to.

---

### ODR-014. Controlled evolution

Any modification to the official directory structure shall be documented, justified, and approved before being incorporated into the project.

---

### ODR-015. Single architecture

The directory structure defined by this document shall constitute the only official architecture of the project.

No parallel variants or alternative structures shall be permitted.

---

## Objectives of the directory organization

The official directory organization shall guarantee:

- Easy navigation through the project.
- Clear separation of responsibilities.
- Uniformity between modules.
- Reuse of common resources.
- Scalability of the structure.
- Ease of maintenance.
- Compatibility with version control.
- Technological independence.
- Controlled evolution.
- Complete traceability of all resources.

---

## 5. File organization

The file organization defines the official structure of the files that make up the job search automation and their distribution within the directories defined by the project architecture.

Its purpose is to ensure that each file has a unique location, a clearly defined responsibility, and a uniform organization that facilitates navigation, maintenance, and evolution of the automation.

---

### OAR-001. Unique location

Every file shall be stored in a single official directory according to the rules established in this document.

Keeping multiple copies of the same file shall not be permitted unless there is a documented and approved justification.

---

### OAR-002. Single responsibility

Each file shall fulfill a single clearly defined function.

Concentrating independent responsibilities within the same file when they can be logically separated shall not be permitted.

---

### OAR-003. Organization by category

Files shall be grouped according to their nature.

At a minimum, independent categories shall exist for:

- Documentation.
- Configuration.
- Prompts.
- Data.
- Logs.
- Shared resources.
- Temporary resources.
- Scripts.
- System components.

---

### OAR-004. Naming conventions

All files shall respect the official naming conventions defined in the Project Standards Document.

---

### OAR-005. Consistency between modules

Equivalent modules shall maintain the same internal file organization to facilitate maintenance and understanding.

---

### OAR-006. Separation between editable and generated files

Manually maintained files shall be stored separately from those automatically generated by the automation.

---

### OAR-007. Shared files

Files used by multiple modules shall be kept in officially defined shared locations.

There shall be no local copies within each module.

---

### OAR-008. Temporary files

Temporary files shall be stored only in the directories intended for that purpose.

Their permanence shall be exclusively transitory.

---

### OAR-009. Configuration files

All system configuration shall be centralized.

Unnecessarily distributed configurations among different components shall not be permitted.

---

### OAR-010. Documentation files

All official project documentation shall be kept organized according to the document architecture defined by the project.

---

### OAR-011. Data files

Files containing information processed by the automation shall be kept separate from files used for system implementation.

---

### OAR-012. Compatibility with version control

The file organization shall facilitate version control.

Automatically generated files that can be rebuilt shall not form part of the permanent project content.

---

### OAR-013. Integrity

No file shall depend on ambiguous or changing physical paths for its operation.

References between files shall remain consistent throughout the evolution of the project.

---

### OAR-014. Controlled evolution

The creation, modification, relocation, or deletion of official files shall respect the architecture defined in this document.

Any significant modification shall be documented.

---

### OAR-015. Official source

The structure defined in this document shall constitute the only official file organization of the project.

No parallel structures that contradict these rules shall be permitted.

---

## Official project structure

The following structure represents the official directory and file architecture of the automation:

```text
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

## Objectives of the file organization

The official file organization shall guarantee:

- A unique location for each file.
- Clearly defined responsibility.
- Uniformity between modules.
- Ease of navigation.
- Separation between permanent and temporary files.
- Reuse of common resources.
- Compatibility with version control.
- Scalability of the architecture.
- Ease of maintenance.
- Complete traceability of all resources.

---

## 6. Resource location conventions

The resource location conventions establish the official rules for determining where each resource belonging to the job search automation shall be stored.

Their purpose is to guarantee a uniform organization, eliminate ambiguities, facilitate resource location, and preserve the coherence of the project architecture throughout its evolution.

Every resource shall have a unique location defined according to the rules established in this chapter.

---

### CUR-001. Location by responsibility

Every resource shall be stored in the directory whose functional responsibility corresponds to the nature of the resource.

The location shall never be defined by temporary convenience.

---

### CUR-002. Exclusive resources

Resources used only by one module shall remain within the structure corresponding to that module.

They shall not be stored in shared locations.

---

### CUR-003. Shared resources

Resources reused by several modules shall be located exclusively in directories intended for shared resources.

No module shall maintain independent copies.

---

### CUR-004. Documentary separation

All official documentation shall be kept separate from the resources used during the execution of the automation.

---

### CUR-005. Separation of configurations

Configuration files shall be kept grouped in the official locations defined for this purpose.

They shall not be distributed among different modules unless there is a documented technical justification.

---

### CUR-006. Temporary resources

Temporary resources shall be stored only in locations intended for transient files.

They may not be considered a permanent part of the architecture.

---

### CUR-007. Persistent resources

Resources whose information must be preserved between executions shall be located exclusively in directories intended for permanent storage.

---

### CUR-008. Automatically generated resources

Every resource generated by the automation shall be stored according to its nature, clearly distinguishing it from manually maintained resources.

---

### CUR-009. Audit resources

Logs, evidence, metrics, and other resources used for audit and traceability shall be kept grouped in specific locations to facilitate their consultation.

---

### CUR-010. Test resources

Resources used for testing shall be kept completely separate from those used by the normal operation of the automation.

---

### CUR-011. External resources

Resources obtained from external platforms, services, or sources shall be kept identified and organized independently from the project's own resources.

---

### CUR-012. Obsolete resources

Resources that are no longer used shall not remain mixed with active resources.

Their treatment shall follow the official maintenance, archiving, or deletion policies defined by the project.

---

### CUR-013. Consistency

The location assigned to a resource shall remain stable throughout its entire lifecycle, unless there is an officially approved reorganization.

---

### CUR-014. Traceability

The physical location of a resource shall allow easy identification of:

- Its purpose.
- The module it belongs to.
- Its level of reuse.
- Its relationship with other project components.

---

### CUR-015. Mandatory compliance

Every new resource incorporated into the project shall respect these conventions before becoming an official part of the architecture.

---

## Objectives of the location conventions

The location conventions shall guarantee:

- A unique location for each resource.
- Uniform organization.
- Clear separation of responsibilities.
- Ease of navigation.
- Reuse of shared resources.
- Separation between permanent and temporary resources.
- Compatibility with the general architecture.
- Ease of maintenance.
- Complete traceability.
- Controlled evolution of the project structure.

---

## 7. Documentation organization

The documentation organization defines the official rules for the structure, location, and administration of all documentation belonging to the job search automation.

Its purpose is to ensure that the documentation remains organized, accessible, consistent, and aligned with the evolution of the project, facilitating its consultation, maintenance, and traceability.

All official documentation shall comply with the provisions established in this chapter, regardless of its nature or format.

---

### ORD-001. Single document repository

All official project documentation shall be kept within a single document structure.

Official documentation shall not be kept distributed across multiple locations without an approved justification.

---

### ORD-002. Documentary classification

Documents shall be organized according to their purpose.

At a minimum, the following categories shall be differentiated:

- Strategic documentation.
- Functional documentation.
- Technical documentation.
- Architecture.
- Standards.
- Annexes.
- Diagrams.
- Manuals.
- Histories.
- References.

---

### ORD-003. Separation of documentation and operation

Official documents shall be kept completely separate from the files used during the execution of the automation.

---

### ORD-004. Predictable location

Every document shall be stored in a location previously defined by the project's document architecture.

Its location shall not depend on the author or the time of creation.

---

### ORD-005. Documentary uniqueness

Each official document shall exist only in one current version within the active documentation.

Keeping multiple active copies of the same document shall not be permitted.

---

### ORD-006. Organization of annexes

Annexes shall be kept organized independently from the main documents.

Each annex shall explicitly reference the document it complements.

---

### ORD-007. Organization of diagrams

Official diagrams shall be stored grouped according to the process, module, or document they belong to.

---

### ORD-008. Document history

Historical versions, change logs, and conversations used to build the documentation shall be kept separate from the current documentation.

Their preservation shall serve audit and traceability purposes.

---

### ORD-009. Automatically generated documentation

Documents generated by automated processes shall be clearly identified to differentiate them from those maintained manually.

---

### ORD-010. Cross-references

When a document depends on another, the relationship shall be established through official document references, avoiding content duplication.

---

### ORD-011. Controlled evolution

Any incorporation, reorganization, or deletion of official documentation shall be previously documented according to the project's policies.

---

### ORD-012. Compatibility

The document organization shall remain compatible with the conventions established in the Project Standards Document.

---

### ORD-013. Traceability

Every document shall be relatable to:

- The main document it belongs to.
- The associated annexes.
- The decisions it documents.
- The affected modules.
- The corresponding change history.

---

### ORD-014. Preservation

Historical documentation shall not be deleted while it can provide value for audits, decision reconstruction, or project evolution.

---

### ORD-015. Official source

Documentation organized according to this document shall constitute the only official source of project information.

Any external documentation shall have only informative value until it is officially incorporated.

---

## Objectives of the document organization

The documentation organization shall guarantee:

- A single official source of information.
- Uniform organization of all documents.
- Separation between current and historical documentation.
- Clear classification by categories.
- Ease of consultation.
- Compatibility with project standards.
- Reuse through cross-references.
- Complete document traceability.
- Preservation of project history.
- Controlled evolution of all documentation.

---

## 8. System configuration organization

The system configuration organization establishes the official rules for the administration, storage, and organization of all configurations used by the job search automation.

Its purpose is to ensure that the configuration remains centralized, consistent, controlled, and decoupled from the implementation logic, facilitating its maintenance, evolution, and reuse.

All configuration used by the automation shall comply with the provisions established in this chapter.

---

### OCS-001. Centralization

All system configuration shall be kept centralized within the official project architecture.

Distributing equivalent configurations among different modules without a documented technical justification shall not be permitted.

---

### OCS-002. Separation from logic

Configuration shall be kept completely separate from the business logic and module implementation.

Configurable values shall not be hardcoded directly within system components.

---

### OCS-003. Organization by responsibility

Configurations shall be organized according to the component, process, or functional scope they belong to.

Each configuration shall have a clearly defined purpose.

---

### OCS-004. Reuse

Configurations used by multiple modules shall be defined once and shared through the official mechanisms established by the architecture.

---

### OCS-005. Consistency

Every configuration shall maintain a uniform structure compatible with the conventions defined in the Project Standards Document.

---

### OCS-006. Identification

Each configuration shall be clearly identified by a unique and descriptive name that allows easy recognition of its purpose.

---

### OCS-007. Technological independence

The organization of configurations shall not depend on a specific format, language, or tool.

The rules established in this document shall remain valid regardless of the technology used.

---

### OCS-008. Change control

Every modification made to an official configuration shall be identifiable, documentable, and justifiable.

---

### OCS-009. Separation by environment

When the automation requires specific configurations for different execution environments, these shall be kept clearly differentiated without altering the general project structure.

---

### OCS-010. Sensitive values

Configurations containing sensitive information shall be managed through secure mechanisms defined by the system architecture.

Their handling shall not compromise the security or traceability of the project.

---

### OCS-011. Controlled deletion

Obsolete configurations shall not be deleted without first verifying that no active component depends on them.

---

### OCS-012. Compatibility

Every new configuration incorporated into the project shall maintain compatibility with the organizational structure defined by this document.

---

### OCS-013. Traceability

Each configuration shall be relatable to:

- The module that uses it.
- The process it belongs to.
- The affected resources.
- Its modification history.

---

### OCS-014. Controlled evolution

The incorporation of new configurations shall respond to clearly justified and documented functional needs.

---

### OCS-015. Official source

The configuration architecture defined in this document shall constitute the only official reference for the administration of project configurations.

No parallel mechanisms that contradict these rules shall be permitted.

---

## Objectives of the configuration organization

The system configuration organization shall guarantee:

- Centralization of all configurations.
- Separation between configuration and business logic.
- Reuse of common configurations.
- Structural consistency.
- Technological independence.
- Change control.
- Ease of maintenance.
- Scalability of the architecture.
- Complete traceability.
- Controlled evolution of the system.

---

## 9. Prompt organization

The prompt organization establishes the official rules for the administration, location, classification, and maintenance of all prompts used by the job search automation.

Its purpose is to ensure that prompts remain organized, reusable, versionable, and decoupled from the implementation logic, facilitating their evolution and ensuring consistent behavior of components that interact with language models.

Every official project prompt shall comply with the provisions established in this chapter.

---

### ORP-001. Single repository

All official prompts shall be stored within a single structure exclusively intended for their administration.

Keeping official prompts distributed among different system components shall not be permitted.

---

### ORP-002. Separation from logic

Prompts shall be kept completely separate from the implementation logic.

Texts used to interact with language models shall not be embedded directly within system components.

---

### ORP-003. Functional organization

Prompts shall be organized according to the process, module, or functional responsibility for which they were designed.

---

### ORP-004. Reuse

When the same prompt can be used by multiple modules, a single shared official version shall exist.

Independent copies shall not be maintained.

---

### ORP-005. Identification

Every prompt shall have a unique identifier according to the conventions established in the Project Standards Document.

---

### ORP-006. Versioning

Every modification made to an official prompt shall allow clear identification of its version and preservation of the corresponding history.

---

### ORP-007. Technological independence

The organization of prompts shall remain independent of the language model provider, API, tool, or technology used to execute them.

---

### ORP-008. Classification

Prompts shall be classified according to their operational purpose.

At a minimum, they may be differentiated between:

- Classification.
- Extraction.
- Evaluation.
- Generation.
- Validation.
- Correction.
- Verification.
- Operational support.

---

### ORP-009. Variables

Variables used by a prompt shall be kept clearly defined and documented.

Their incorporation shall follow the official project conventions.

---

### ORP-010. Compatibility

Every prompt shall be designed to maintain compatibility with future modifications of the automation.

The incorporation of new modules shall not require redesigning existing prompts unless there is a technical justification.

---

### ORP-011. Traceability

Each prompt shall be relatable to:

- The module that uses it.
- The process where it intervenes.
- The required inputs.
- The expected outputs.
- Its modification history.

---

### ORP-012. Controlled evolution

The incorporation, modification, or deletion of prompts shall be previously documented and remain aligned with the general project architecture.

---

### ORP-013. Consistency

All official prompts shall maintain a uniform structure according to the templates and standards defined by the project.

---

### ORP-014. Audit

The use of prompts shall be identifiable during the execution of the automation to facilitate audit and subsequent analysis.

---

### ORP-015. Official source

The architecture defined in this document shall constitute the only official reference for the organization of project prompts.

Official prompts stored outside the authorized structure shall not be permitted.

---

## Objectives of the prompt organization

The prompt organization shall guarantee:

- Centralization of all official prompts.
- Separation between prompts and implementation logic.
- Reuse of common prompts.
- Controlled versioning.
- Uniform classification.
- Technological independence.
- Compatibility with project evolution.
- Complete traceability.
- Ease of maintenance.
- Consistency with official project standards.

---

## 10. Data organization

The data organization establishes the official rules for the administration, storage, and organization of all information used, generated, or processed by the job search automation.

Its purpose is to ensure that data remains organized, integral, traceable, and decoupled from the implementation logic, facilitating its maintenance, evolution, and reuse throughout the project lifecycle.

All data managed by the automation shall comply with the provisions established in this chapter.

---

### ODT-001. Separation by purpose

Data shall be organized according to its purpose within the automation.

At a minimum, differentiation shall be made between:

- Input data.
- Data in processing.
- Persistent data.
- Historical data.
- Temporary data.
- Backup data.

---

### ODT-002. Separation from implementation

Data shall be kept completely separate from the components responsible for processing it.

The organization of data shall not depend on the technical implementation used.

---

### ODT-003. Organization by module

When necessary, data may be organized by functional module, always maintaining a uniform structure throughout the automation.

---

### ODT-004. Shared data

Data used by multiple modules shall be managed through centralized mechanisms defined by the system architecture.

Independent copies that compromise consistency shall not be maintained.

---

### ODT-005. Persistence

Data whose preservation is necessary between different executions shall be stored using the official mechanisms defined by the project.

---

### ODT-006. Temporary data

Temporary data shall be kept completely separate from persistent data.

Its permanence shall be limited exclusively to the time necessary for the corresponding execution.

---

### ODT-007. Historical data

Information used for audit, analysis, traceability, or process reconstruction shall be kept separate from operational data.

---

### ODT-008. Integrity

The data organization shall permanently preserve the integrity, consistency, and reliability of the information managed by the automation.

---

### ODT-009. Versioning

When the evolution of the project requires it, changes to data structures shall be identifiable and kept under control.

---

### ODT-010. Technological independence

The rules defined in this document shall remain independent of the storage engine, format, or technology used.

---

### ODT-011. Traceability

Every data set shall be relatable to:

- The module that generates it.
- The process that uses it.
- Its origin.
- Its destination.
- Its processing history.

---

### ODT-012. Compatibility

The data organization shall facilitate the incorporation of new modules and new types of information without requiring significant reorganizations.

---

### ODT-013. Preservation

Data whose preservation is required by the project policies shall be kept available according to the official storage and audit rules.

---

### ODT-014. Controlled evolution

Every significant modification to the data organization shall be previously documented and remain aligned with the rest of the project architecture.

---

### ODT-015. Official source

The organization defined in this document shall constitute the only official reference for the administration and organization of project data.

No parallel structures that contradict these provisions shall be permitted.

---

## Objectives of the data organization

The data organization shall guarantee:

- Clear separation between different types of data.
- Independence from technical implementation.
- Integrity and consistency of information.
- Reuse of shared data.
- Scalability of the architecture.
- Compatibility with new modules.
- Complete traceability of the data lifecycle.
- Ease of maintenance.
- Proper preservation of information.
- Controlled evolution of the data architecture.

---

## 11. Log organization

The log organization establishes the official rules for the administration, storage, and classification of all logs generated by the job search automation.

Its purpose is to ensure that logs remain organized, accessible, traceable, and consistent, facilitating monitoring, auditing, error diagnosis, operational analysis, and system evolution.

Every log generated by the automation shall comply with the provisions established in this chapter.

---

### ORL-001. Centralization

All official automation logs shall be stored within a single structure intended for that purpose.

Distributing operational logs among different modules without a documented technical justification shall not be permitted.

---

### ORL-002. Separation by purpose

Logs shall be organized according to their purpose.

At a minimum, differentiation shall be made between:

- Operational logs.
- Audit logs.
- Error logs.
- Event logs.
- Execution logs.
- Diagnostic logs.

---

### ORL-003. Separation from implementation

Logs shall be kept completely separate from the components responsible for generating them.

The system logic shall not depend on the physical location of logs.

---

### ORL-004. Uniform organization

All automation modules shall record information following a uniform structure according to the official project standards.

---

### ORL-005. Traceability

Every log shall allow identification of, at a minimum:

- Date and time of the event.
- Responsible module.
- Associated process.
- Event type.
- Operation result.
- Related identifier when applicable.

---

### ORL-006. Integrity

Logs shall be kept intact once generated.

They may not be modified afterwards except through officially authorized procedures.

---

### ORL-007. Separation between active and historical logs

Logs used for daily operation shall be kept separate from those preserved exclusively for historical or audit purposes.

---

### ORL-008. Compatibility

The log organization shall remain compatible with Document 6 — Error Handling and with the conventions defined in Document 5 — Project Standards.

---

### ORL-009. Technological independence

The rules established in this chapter shall remain independent of any monitoring tool, storage engine, or technology used to implement the logs.

---

### ORL-010. Preservation

Logs whose preservation is required for audit, diagnosis, or historical analysis shall be kept available according to the official project policies.

---

### ORL-011. Accessibility

Logs shall be organized in a way that facilitates their consultation, analysis, and retrieval when required for operational or audit tasks.

---

### ORL-012. Controlled evolution

Every modification to the log organization shall be previously documented and remain aligned with the rest of the project architecture.

---

### ORL-013. Reuse

When multiple components generate equivalent logs, they shall use the same officially defined organizational structure.

---

### ORL-014. Consistency

The classification and organization of logs shall remain uniform throughout the evolution of the project.

Alternative structures for the same type of log may not coexist.

---

### ORL-015. Official source

The organization defined in this document shall constitute the only official reference for the administration of automation logs.

No parallel mechanisms that contradict these provisions shall be permitted.

---

## Objectives of the log organization

The log organization shall guarantee:

- Centralization of all official logs.
- Separation between different types of logs.
- Compatibility with audit and error handling.
- Integrity of recorded information.
- Ease of consultation and diagnosis.
- Technological independence.
- Complete traceability of operations.
- Scalability of the architecture.
- Ease of maintenance.
- Controlled evolution of the system.

---

## 12. Temporary resource organization

The temporary resource organization establishes the official rules for the administration, storage, and treatment of all transient resources generated during the execution of the job search automation.

Its purpose is to ensure that temporary resources remain isolated from permanent resources, avoiding affecting the integrity, organization, and maintainability of the project.

Every temporary resource shall comply with the provisions established in this chapter.

---

### ORT-001. Physical separation

All temporary resources shall be stored exclusively in the locations intended for that purpose.

They may not be mixed with permanent project resources.

---

### ORT-002. Transient nature

Every temporary resource shall exist only for the time necessary for the execution of the process that requires it.

---

### ORT-003. Organization by process

When it is necessary to preserve temporary resources during an execution, these shall be organized according to the process or module that generated them.

---

### ORT-004. Independence

Temporary resources shall not become permanent dependencies of any automation component.

The normal execution of the system shall not depend on previously stored temporary information.

---

### ORT-005. Regeneration

Every temporary resource shall be able to regenerate automatically when necessary.

The loss of a temporary resource shall not compromise the continuity of the project.

---

### ORT-006. Controlled cleanup

Temporary resources shall be deleted or reused through controlled mechanisms defined by the system architecture.

They shall not accumulate indefinitely.

---

### ORT-007. Separation from audit

Temporary resources shall not be used as a permanent mechanism for audit, traceability, or historical storage.

---

### ORT-008. Compatibility

The organization of temporary resources shall remain compatible with the error handling, recovery, and traceability policies defined by the project.

---

### ORT-009. Integrity

The existence, modification, or deletion of temporary resources shall not affect the integrity of permanent data or official documentation.

---

### ORT-010. Technological independence

The rules established in this chapter shall remain independent of specific tools, formats, or technologies.

---

### ORT-011. Identification

Every temporary resource shall be relatable to:

- The process that generated it.
- The corresponding module.
- The associated execution when applicable.
- Its operational purpose.

---

### ORT-012. Reusable resources

When a temporary resource can be reused during the same execution without compromising system consistency, the architecture may allow its controlled reuse.

---

### ORT-013. Controlled evolution

Every significant modification to the organization of temporary resources shall be previously documented and remain aligned with the rest of the project architecture.

---

### ORT-014. Consistency

All modules shall follow the same rules for the generation, use, and deletion of temporary resources.

---

### ORT-015. Official source

The provisions established in this document shall constitute the only official reference for the organization of temporary resources within the automation.

No alternative mechanisms that contradict these rules may be implemented.

---

## Objectives of the temporary resource organization

The temporary resource organization shall guarantee:

- Complete separation between temporary and permanent resources.
- Controlled deletion of transient resources.
- Independence from technical implementation.
- Ease of maintenance.
- Compatibility with error recovery.
- Integrity of permanent information.
- Scalability of the architecture.
- Uniform organization across modules.
- Traceability of temporary resources when necessary.
- Controlled evolution of the project architecture.

---

## 13. Script and utility organization

The script and utility organization establishes the official rules for the administration, storage, and maintenance of all resources intended to support the development, operation, testing, maintenance, and administration of the job search automation.

Its purpose is to ensure that scripts and utilities remain organized, reusable, independent of the main system logic, and aligned with the official project architecture.

Every script or utility belonging to the project shall comply with the provisions established in this chapter.

---

### OSU-001. Functional separation

Scripts and utilities shall be kept completely separate from the functional modules of the automation.

Their existence shall not alter the organization of the main system components.

---

### OSU-002. Specific purpose

Each script or utility shall fulfill a single clearly defined responsibility.

Grouping independent functions within the same resource when they can be kept separately shall not be permitted.

---

### OSU-003. Organization by purpose

Scripts and utilities shall be organized according to their operational purpose.

At a minimum, they may be differentiated between:

- Automation.
- Maintenance.
- Migration.
- Conversion.
- Validation.
- Diagnosis.
- Administration.
- Development support.

---

### OSU-004. Reuse

Every script that can be used by multiple processes shall be kept as a reusable resource.

Independent copies of the same utility shall not exist.

---

### OSU-005. Independence from operation

The automation shall be able to execute its main processes without necessarily depending on auxiliary scripts intended exclusively for maintenance or administration.

---

### OSU-006. Identification

Every script or utility shall have a clear identification that allows immediate recognition of its purpose.

---

### OSU-007. Compatibility

Scripts shall remain compatible with the conventions established by the Project Standards Document and with the general architecture defined in this document.

---

### OSU-008. Technological independence

The organization rules established in this chapter shall remain independent of the programming language or tool used to implement the scripts.

---

### OSU-009. Change control

Every significant modification made to an official script shall be identifiable, documentable, and justifiable.

---

### OSU-010. Traceability

Every script or utility shall be relatable to:

- The process it supports.
- The corresponding module when applicable.
- Its operational purpose.
- Its modification history.

---

### OSU-011. Security

Scripts used for administrative or maintenance tasks shall be designed avoiding affecting the integrity of the information or the stability of the automation.

---

### OSU-012. Controlled evolution

The incorporation of new scripts shall respond to a clearly identified and documented need.

Creating redundant utilities that duplicate existing functionalities shall not be permitted.

---

### OSU-013. Consistency

All official scripts shall maintain a uniform organization according to the conventions established by the project.

---

### OSU-014. Controlled deletion

Scripts that are no longer used shall be removed in a controlled manner, previously verifying that no active process depends on them.

---

### OSU-015. Official source

The organization defined in this document shall constitute the only official reference for the administration of project scripts and utilities.

No parallel structures that contradict these provisions may be maintained.

---

## Objectives of the script and utility organization

The script and utility organization shall guarantee:

- Separation between main logic and auxiliary resources.
- Uniform organization by purpose.
- Reuse of common utilities.
- Technological independence.
- Compatibility with the general architecture.
- Ease of maintenance.
- Change control.
- Complete traceability.
- Scalability of the architecture.
- Controlled evolution of auxiliary resources.

---

## 14. Directory dependency rules

The directory dependency rules establish the official model for controlling the permitted relationships between the different directories that make up the architecture of the job search automation.

Their purpose is to avoid unnecessary dependencies, reduce coupling between components, and ensure that the evolution of the project structure can be carried out in a controlled and maintainable manner.

Every directory belonging to the official architecture shall comply with the provisions established in this chapter.

---

### RDD-001. Justified dependencies

Every dependency between directories shall respond to a clearly identified functional need.

Dependencies created solely for implementation convenience shall not be permitted.

---

### RDD-002. Low coupling

The architecture shall minimize dependencies between directories.

Each component shall maintain the highest possible level of independence from the others.

---

### RDD-003. Independent responsibility

The existence of a dependency shall not modify the main responsibility of a directory.

Each directory shall retain a single clearly defined function.

---

### RDD-004. Unidirectional dependencies

Whenever possible, dependencies shall be kept in a single direction.

Circular dependencies between directories shall be avoided.

---

### RDD-005. Shared resources

When several directories require using the same resource, it shall be located in an officially defined shared structure.

Dependencies through resource copies shall not be established.

---

### RDD-006. Modular isolation

Each functional module shall maintain independence from the internal structure of the other modules.

Interaction between modules shall occur only through the mechanisms defined by the project architecture.

---

### RDD-007. Configuration dependencies

Directories responsible for configuration may be used by multiple components, but configurations shall not depend on the consuming modules.

---

### RDD-008. Documentary dependencies

Documentation may reference any project component without generating operational dependencies between directories.

---

### RDD-009. Temporary resources

Temporary resources may not become permanent dependencies of any project directory.

---

### RDD-010. Technological independence

The dependency rules shall remain independent of the programming language, framework, or tool used to implement the automation.

---

### RDD-011. Compatible evolution

The incorporation of new directories shall not break previously defined dependencies nor unnecessarily affect existing components.

---

### RDD-012. Controlled deletion

Before deleting a directory, it shall be verified that no other component maintains active dependencies toward it.

---

### RDD-013. Traceability

Every dependency between directories shall be identifiable, justifiable, and documentable.

---

### RDD-014. Consistency

The dependency rules shall be applied uniformly throughout the project architecture.

No undocumented exceptions shall be permitted.

---

### RDD-015. Official source

The rules defined in this document shall constitute the only official reference for the administration of dependencies between project directories.

No relationships that contradict these provisions may be established.

---

## Objectives of the dependency rules

The directory dependency rules shall guarantee:

- Low coupling between components.
- Independence of responsibilities.
- Elimination of circular dependencies.
- Proper reuse of shared resources.
- Scalability of the architecture.
- Compatibility with new modules.
- Ease of maintenance.
- Controlled evolution of the project.
- Traceability of relationships between directories.
- Structural consistency of the entire architecture.

---

## 15. Rules for incorporating new modules

The rules for incorporating new modules establish the official procedure that any functional component added to the job search automation shall follow.

Their purpose is to ensure that the evolution of the project preserves the coherence of the architecture, avoiding organizational inconsistencies, duplication of responsibilities, and unnecessary dependencies.

Every new module shall comply with the provisions established in this chapter before becoming part of the official project architecture.

---

### RIM-001. Functional justification

Every new module shall respond to a clearly identified and documented functional need.

Modules whose responsibility is already covered by another existing component may not be incorporated.

---

### RIM-002. Single responsibility

Each module shall have a single clearly defined purpose.

Modules with multiple or ambiguous responsibilities shall not be permitted.

---

### RIM-003. Architectural compatibility

Every new module shall be integrated respecting the folder architecture, organizational conventions, and standards defined by the project.

---

### RIM-004. Uniform organization

New modules shall adopt the same organizational structure used by existing modules when the nature of their components is equivalent.

---

### RIM-005. Reuse

Before creating new resources, it shall be verified whether reusable components exist within the architecture.

Functionalities already available shall not be duplicated.

---

### RIM-006. Controlled dependencies

Dependencies introduced by a new module shall be kept to the necessary minimum and respect the official dependency rules defined by this document.

---

### RIM-007. Documentary compatibility

Every new module shall be incorporated together with the update of the corresponding official documentation.

The physical architecture and documentation shall remain synchronized.

---

### RIM-008. Compatibility with standards

The incorporation of a new module shall respect the naming, identifier, documentation, configuration, logging, and other official project standard conventions.

---

### RIM-009. Compatibility with the data model

The incorporation of new resources shall not compromise the integrity, consistency, or traceability of data managed by the automation.

---

### RIM-010. Compatibility with error handling

Every new module shall implement the official policies for error detection, logging, recovery, and treatment defined in Document 6.

---

### RIM-011. Scalability

The incorporation of new modules shall not require significantly reorganizing the existing architecture.

The structure shall allow the progressive growth of the project.

---

### RIM-012. Prior validation

Before approving a new module, it shall be verified that its incorporation complies with all architectural rules defined by the official documentation.

---

### RIM-013. Traceability

Every incorporation of a new module shall document:

- Its purpose.
- Its scope.
- Its responsibilities.
- Its dependencies.
- The affected documents.
- The incorporation date.

---

### RIM-014. Controlled evolution

Every incorporation shall be formally approved before being integrated into the official project architecture.

Subsequent modifications shall follow the same procedure.

---

### RIM-015. Official source

The rules established in this document shall constitute the only official procedure for incorporating new modules into the automation.

Components that contradict these provisions may not be added.

---

## Objectives of new module incorporation

The rules for incorporating new modules shall guarantee:

- Ordered growth of the architecture.
- Compatibility with all official documentation.
- Organizational uniformity.
- Reuse of existing components.
- Low coupling between modules.
- Project scalability.
- Ease of maintenance.
- Integrity of the architecture.
- Traceability of incorporations.
- Controlled evolution of the automation.

---

## 16. Folder architecture restrictions

The following restrictions establish the official limits that shall be respected during the design, implementation, maintenance, and evolution of the folder architecture of the job search automation.

Their purpose is to preserve the consistency of the project organization, avoid architectural deviations, and ensure that any future modification maintains compatibility with the official documentation.

All restrictions defined in this chapter shall be mandatory for any component, module, resource, or extension of the project.

---

### RAP-001. Single architecture

No more than one official folder architecture may coexist for the same project.

The entire organization shall conform to the structure defined by this document.

---

### RAP-002. Directories without purpose

No directories whose responsibility is not clearly defined and documented may be created.

---

### RAP-003. Organizational duplication

Multiple directories intended to store the same type of resource may not exist when a single location is sufficient.

---

### RAP-004. Mixing of responsibilities

Storing resources belonging to different functional categories within the same directory when specific locations exist for each one shall not be permitted.

---

### RAP-005. Circular dependencies

Circular dependencies between modules, directories, or architecture components may not be established.

---

### RAP-006. Implicit dependencies

The architecture may not depend on undocumented folder structures or those created dynamically without being part of the official project organization.

---

### RAP-007. Undocumented modifications

No significant modification to the architecture may be made without the corresponding update of the official documentation.

---

### RAP-008. Resources outside the architecture

Resources belonging to the project may not be stored outside the official structure defined by this architecture, except in exceptional cases previously approved and documented.

---

### RAP-009. Excessive coupling

The architecture organization may not force a module to know the internal structure of other modules to fulfill its responsibilities.

---

### RAP-010. Technological dependency

The folder organization may not be designed based on specific tools, frameworks, languages, or providers.

The architecture shall retain its validity even when the technological implementation changes.

---

### RAP-011. Distributed configuration

Maintaining equivalent configurations unnecessarily distributed among different project components shall not be permitted.

---

### RAP-012. Permanent temporary resources

Temporary resources may not become permanent storage nor form part of the stable project structure.

---

### RAP-013. Deletion without validation

No directory, file, or official resource may be deleted without first verifying that there are no active dependencies toward it.

---

### RAP-014. Documentary inconsistency

The physical architecture and official documentation may not evolve independently.

Any modification shall remain synchronized between both.

---

### RAP-015. Non-compliance with standards

No resource, module, or component that fails to comply with the conventions established by the Project Standards Document and the provisions defined in this document may be incorporated.

---

## General restrictions

The folder architecture shall respect the following general restrictions:

- There shall be a single official architecture.
- Duplication of responsibilities shall not be permitted.
- There shall be no circular dependencies.
- Every modification shall be documented.
- The architecture shall remain independent of the technology used.
- Resources shall be kept within the official structure.
- Documentation and architecture shall evolve together.
- Temporary resources shall remain separate from permanent ones.
- Every new component shall respect the official architectural rules.
- No exception may be applied without the corresponding justification and documentary approval.

---

## 17. Acceptance criteria

The present acceptance criteria establish the conditions that the folder architecture must meet to be considered compliant with the official project documentation.

Their purpose is to provide a uniform set of verifications that allow validating the correct organization of the physical structure of the automation before its approval, implementation, or modification.

Compliance with these criteria shall be mandatory for all modules, components, and resources incorporated into the project.

---

### CAP-001. Uniform organization

The architecture shall maintain a consistent organization in all its directories and resources, according to the rules defined in this document.

---

### CAP-002. Clearly defined responsibilities

Each directory and resource shall have a single clearly identifiable responsibility.

There shall be no functional ambiguities.

---

### CAP-003. Separation of responsibilities

The architecture shall maintain a clear separation between:

- Documentation.
- Configuration.
- Prompts.
- Data.
- Logs.
- Temporary resources.
- Scripts and utilities.
- Functional components.

---

### CAP-004. Compliance with standards

The entire architecture shall respect the conventions established by the Project Standards Document.

---

### CAP-005. Documentary compatibility

The physical structure shall remain fully aligned with the official project documentation.

There shall be no differences between the two.

---

### CAP-006. Scalability

The architecture shall allow incorporating new modules without requiring significant reorganizations of the existing structure.

---

### CAP-007. Technological independence

The architecture organization shall not depend on specific technologies, tools, or providers.

---

### CAP-008. Low coupling

Dependencies between directories shall be kept to the necessary minimum and respect the official architecture rules.

---

### CAP-009. Traceability

The location of each resource shall allow easy identification of:

- Its purpose.
- The corresponding module.
- Its relationship with other components.
- The associated documentation.

---

### CAP-010. Integrity

The architecture shall preserve the organizational integrity of the project, avoiding duplicities, inconsistencies, or unauthorized dependencies.

---

### CAP-011. Controlled evolution

Every modification shall be previously documented, justified, and approved before being officially incorporated into the architecture.

---

### CAP-012. Compatibility with new components

Every new module, resource, or directory shall be incorporable while fully respecting the rules established in this document.

---

### CAP-013. Global consistency

The architecture shall maintain organizational uniformity across all automation modules.

---

### CAP-014. Auditability

The architecture organization shall facilitate the review, audit, and verification of any resource belonging to the project.

---

### CAP-015. Comprehensive compliance

The architecture may only be considered approved when it simultaneously meets all the criteria established in this chapter.

---

## Acceptance verification

The folder architecture shall be considered compliant when:

- It maintains a uniform organization.
- There is a single responsibility per directory.
- Resource separation is respected.
- It complies with official project standards.
- It maintains technological independence.
- It allows orderly growth of the automation.
- It avoids unnecessary dependencies.
- It facilitates traceability of all resources.
- It maintains coherence with official documentation.
- It fully complies with the provisions defined in this document.

---

## 18. Folder architecture index

This index constitutes the official structure of **Document 7 – Folder Architecture**.

Its purpose is to facilitate consultation, navigation, maintenance, and traceability of all sections that make up the organizational architecture of the project.

---

# Index

## 1. Purpose of the document

Defines the objective, scope, and mandatory nature of the folder architecture.

---

## 2. Principles of the folder architecture

Establishes the general principles that shall govern the entire physical organization of the project.

---

## 3. General project structure

Defines the conceptual organization of the architecture and the separation of responsibilities.

---

## 4. Directory organization

Establishes the official rules for the hierarchical organization of project directories.

---

## 5. File organization

Defines the rules for the organization of files and the conceptual architecture of the project.

---

## 6. Resource location conventions

Establishes the official criteria for determining the location of all automation resources.

---

## 7. Documentation organization

Defines the official structure for the administration and organization of all project documentation.

---

## 8. System configuration organization

Establishes the rules for organizing and administering all automation configurations.

---

## 9. Prompt organization

Defines the official architecture for the organization, reuse, and maintenance of prompts.

---

## 10. Data organization

Establishes the rules for organizing the information used and generated by the automation.

---

## 11. Log organization

Defines the architecture for the organization of operational logs, audit, events, and diagnosis.

---

## 12. Temporary resource organization

Establishes the rules for the administration of transient resources generated during execution.

---

## 13. Script and utility organization

Defines the official organization of auxiliary resources used for the development, maintenance, and administration of the project.

---

## 14. Directory dependency rules

Establishes the rules that control the permitted relationships between the different directories of the architecture.

---

## 15. Rules for incorporating new modules

Defines the official procedure for incorporating new modules without affecting the consistency of the architecture.

---

## 16. Folder architecture restrictions

Establishes the limits and prohibitions that shall be respected throughout the evolution of the project.

---

## 17. Acceptance criteria

Defines the objective conditions that the architecture must meet to be considered compliant with the official documentation.

---

## 18. Folder architecture index

Presents the official structure of the document and facilitates its consultation as a normative reference.

---

# Normative references

The folder architecture shall remain permanently aligned with the following official project documents:

- Document 0 — Project Glossary.
- Document 1 — Functional Requirements.
- Document 2 — Non-Functional Requirements.
- Document 3 — Decision Model.
- Document 4 — Data Flow.
- Document 5 — Project Standards.
- Document 6 — Error Handling.

Any modification made to the architecture shall maintain compatibility with these documents and with any subsequently approved official update.
