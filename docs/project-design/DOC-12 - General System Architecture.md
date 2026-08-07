# Document 12 - General System Architecture

## 1. Purpose of the document

This document defines the official general architecture of the job search automation.

Its purpose is to establish, justify, and document the structural organization of the system, including its modules, components, layers, services, integration mechanisms, and architectural principles, ensuring that all design decisions are consistent with the objectives, requirements, and constraints defined in the official project documentation.

This document constitutes the official reference for the design and implementation of the automation's architecture. Every solution developed as part of the project must respect the architecture defined herein, preserving the consistency, modularity, maintainability, and scalability of the system.

The documented architectural decisions must maintain full coherence with Documents 0 through 11, including the glossary, functional and non-functional requirements, the decision model, the data flow, the project standards, error handling, the folder architecture, strategic decisions, the research conducted, and the approved technology stack.

The architecture defined in this document will serve as the foundation for the development of Document 13 — Data Model and for the development of all subsequent phases of the project, providing a uniform technical structure upon which the different modules of the automation will be implemented.

Any modification to the general architecture must be documented, justified, and formally approved before being incorporated into the project, preserving traceability, compatibility with the rest of the official documentation, and the controlled evolution of the system.

---

## 2. Architecture objectives

The general system architecture must ensure that the job search automation can be developed, maintained, evolved, and operated consistently with the objectives, constraints, and principles defined in the official project documentation.

The objectives defined in this chapter constitute the guiding criteria of the architecture and must be considered mandatory during the design, implementation, maintenance, and evolution of the system.

Every architectural decision must contribute to the fulfillment of one or more of the following objectives.

### OA-001. Modularity

The architecture must organize the system into clearly defined modules, with specific responsibilities and well-established functional boundaries.

### OA-002. Separation of concerns

Each component must fulfill a single clearly identifiable responsibility, avoiding the concentration of functions belonging to different business processes.

### OA-003. Low coupling

Dependencies between modules must be minimized to facilitate the independent evolution of each component.

### OA-004. High cohesion

Elements belonging to the same module must be closely related to the responsibility that module performs.

### OA-005. Scalability

The architecture must allow the incorporation of new modules, functionalities, and information sources without requiring significant redesign of the system.

### OA-006. Maintainability

The organization of the system must facilitate the understanding, updating, correction, and continuous improvement of its components.

### OA-007. Reusability

Whenever appropriate, components must be designed to be reused by different modules of the system.

### OA-008. Extensibility

The architecture must facilitate the incorporation of new capabilities through the addition of components, avoiding unnecessary modification of existing ones.

### OA-009. Consistency

All modules must follow a uniform organization and respect the architectural principles established in this document.

### OA-010. Traceability

The architecture must facilitate the complete tracking of the flow of information, decisions, and processes across all components of the system.

### OA-011. Observability

The architecture must allow monitoring the operation of the system through logs, metrics, and diagnostic mechanisms.

### OA-012. Robustness

The design must minimize the impact of individual errors, preventing the failure of one component from compromising the overall operation of the automation.

### OA-013. Testability

Components must be designed so that they can be validated and verified both in isolation and as part of the complete system.

### OA-014. Configurability

The behavior of the system must be adjustable through controlled configurations, reducing the need to modify source code.

### OA-015. Technology compatibility

The architecture must be fully compatible with the official technology stack defined in Document 11.

### OA-016. Technology independence

Whenever feasible, the design must minimize unnecessary dependencies on specific technologies, platforms, or vendors.

### OA-017. Controlled evolution

The architecture must facilitate the incorporation of future changes while preserving the stability and coherence of the system.

### OA-018. Compatibility with official documentation

Every architectural decision must remain aligned with the requirements, standards, models, and constraints defined in Documents 0 through 11.

### OA-019. Simplicity

The architecture must avoid unnecessary complexity, prioritizing clear, understandable solutions that are appropriate for the real needs of the project.

### OA-020. Architectural sustainability

The organization of the system must favor its long-term maintenance and evolution, preserving the quality of the solution throughout its entire lifecycle.

---

## 3. Architectural principles

The general architecture of the automation must be designed in accordance with the principles defined in this chapter.

These principles constitute the official architectural design rules of the project and will be mandatory during the definition, implementation, maintenance, and evolution of all system components.

Every architectural decision must justify its conformity with the principles established herein.

### PA-001. Modular architecture

The solution must be organized into clearly delimited modules, each with specific responsibilities and defined functional boundaries.

### PA-002. Single responsibility

Each module, component, or service must fulfill a single main responsibility, avoiding the concentration of functions belonging to different system processes.

### PA-003. Layer separation

The architecture must maintain a clear separation between the different layers of the system, avoiding improper dependencies between them.

### PA-004. Low coupling

Dependencies between components must be minimized to promote functional independence and facilitate the evolution of the system.

### PA-005. High cohesion

The elements that make up a single component must be closely related to the responsibility that component performs.

### PA-006. Communication through defined interfaces

All interaction between modules must be carried out through clearly defined interfaces, avoiding implicit dependencies or direct access to internal implementations.

### PA-007. Centralization of shared services

Reusable functionalities must be implemented as shared services to avoid logic duplication and promote consistency.

### PA-008. Decoupled configuration

System configuration must be kept separate from implementation code, allowing behavior to be modified through controlled configuration mechanisms.

### PA-009. Controlled dependency flow

Dependencies between components must follow a clearly defined architectural direction, avoiding circular dependencies.

### PA-010. Independence between modules

Whenever possible, modules must be able to evolve, be maintained, and be tested independently.

### PA-011. Fault tolerance

The architecture must isolate errors to reduce their propagation and minimize their impact on the overall operation of the system.

### PA-012. Integrated observability

All components must facilitate the logging of events, metrics, and evidence necessary for monitoring, diagnosis, and auditing.

### PA-013. Scalability by composition

The incorporation of new capabilities must be done preferably by adding new components, avoiding modification of the existing structure.

### PA-014. Extensibility

The architecture must allow functionality to be extended without unnecessarily altering already implemented modules.

### PA-015. Structural consistency

All modules must maintain a homogeneous organization, respecting the official architectural conventions of the project.

### PA-016. Component reuse

Whenever feasible, components must be designed to be reused by different processes or modules of the automation.

### PA-017. Incremental evolution

The architecture must facilitate the progressive incorporation of improvements without compromising the stability or compatibility of the system.

### PA-018. Technology compatibility

Every architectural decision must remain aligned with the official technology stack defined in Document 11.

### PA-019. Architectural traceability

The organization of the system must allow clear identification of the path of information, the responsibilities of each component, and the relationships between them.

### PA-020. Design simplicity

The architecture must avoid unnecessary complexity, prioritizing clear, understandable solutions proportionate to the real needs of the project.

---

## 4. General view of the architecture

The general architecture of the automation is organized into three complementary levels that together describe the functional and technical structure of the system.

This organization allows clearly separating business logic, shared services, and technological infrastructure, favoring modularity, maintainability, and controlled evolution of the solution.

### 4.1. Functional level

The functional level represents the main processes of the automation and constitutes the core of the business.

It is composed of the following modules:

- Opportunity discovery.
- Initial offer preparation.
- Initial evaluation.
- Offer processing.
- Result management.

Each module has clearly defined responsibilities and communicates with others only through the mechanisms defined by the architecture.

Functional modules will not directly implement cross-cutting services nor directly access technological infrastructure, but will use the shared components defined by this architecture.

### 4.2. Cross-cutting services level

The second level is composed of reusable services that provide common capabilities to the entire automation.

These include, among others:

- Configuration management.
- Decision engine.
- Artificial intelligence.
- Information persistence.
- Logging and auditing.
- Observability.
- Security.
- Error handling.
- Shared support services.

These services must be designed as independent, reusable components decoupled from the functional modules.

No module will re-implement functionalities that are already available through these services.

### 4.3. Infrastructure level

The third level represents the external technological resources on which the automation operates.

These include:

- Job search platform.
- Automated browser.
- Artificial intelligence models.
- Database.
- File system.
- Authorized external services.

The infrastructure must remain isolated from business logic through abstraction mechanisms that reduce technological dependencies and facilitate the future evolution of the system.

### 4.4. Relationship between levels

The architecture must maintain a strict separation between the three defined levels.

Functional modules will exclusively use the cross-cutting services necessary to execute their responsibilities.

Cross-cutting services will be the only ones responsible for interacting with the infrastructure when applicable.

This organization will allow maintaining a modular, reusable, maintainable, and scalable architecture, reducing the impact of technological changes on business logic and favoring the incorporation of new capabilities during the evolution of the project.

---

## 5. Main system components

The general architecture of the automation is composed of a set of specialized components that, in a coordinated manner, implement the functional and technical capabilities of the system.

Each component constitutes an architectural unit with clearly defined responsibilities and must maintain functional independence, explicit interfaces, and compatibility with the architectural principles established in this document.

The official components of the architecture are as follows.

### CMP-001. Opportunity discovery

Responsible for locating, collecting, and registering new job opportunities from the official sources defined for the project.

#### CMP-001 internal structure

The component is organized into the following internal elements, whose structure must be derivable one-to-one in the `modules/discovery/` package:

- `run_context.py`: maintains the context of the current run (Run), including its identifier, configuration snapshot, active session, and accumulated state during the process.
- Discovery nodes: the thirteen nodes that make up the official Discovery flow defined in the MVP Execution Plan (Phase 4) and modeled in DOC-04 (Section 15). Each node is responsible for one stage of the flow and communicates with the following nodes exclusively through the contracts defined in the technical sheet.
- `adapters/`: platform adapters that implement the `INT-001. Job search platform` interface and use the `INT-003. Automated browser` integration to interact with each official source.

The module uses the cross-cutting services of the architecture as follows:

| Internal element | Shared services it depends on |
|------------------|-------------------------------|
| Run manager | SRV-004 (Persistence) and SRV-005 (Configuration management) |
| Lock manager | SRV-004 (Persistence) |
| Platform adapters | SRV-003 (Web automation engine), SRV-006 (Logging) |

The run manager is responsible for orchestrating the execution of the official Discovery flow, and the lock manager guarantees, through the lock store, that no more than one run is in progress concurrently per source.

Official credentials used by the platform adapters must be stored in the secure credential repository defined by the architecture's Configuration Management service (SRV-005), accessed exclusively through its public interfaces and never persisted in the application database, logs, or execution records (see Section 14, Credentials and secrets).

### CMP-002. Initial offer preparation

Responsible for normalizing, structuring, and preparing the information obtained during the discovery process for subsequent evaluation stages.

### CMP-003. Initial evaluation

Responsible for performing the preliminary analysis of opportunities by applying the evaluation criteria established by the project.

### CMP-004. Offer processing

Responsible for performing the detailed analysis of opportunities approved during the initial evaluation, integrating the information necessary to support user decision-making.

### CMP-005. Result management

Responsible for consolidating, storing, and presenting the final result of the processing performed by the automation.

### CMP-006. Decision engine

Responsible for executing the official decision model defined by the project and determining the behavior of the automation according to the approved rules.

### CMP-007. Web automation engine

Responsible for controlling the automated interaction with target platforms, including navigation, information extraction, and execution of authorized actions.

### CMP-008. Artificial intelligence engine

Responsible for coordinating the use of artificial intelligence models incorporated into the project and providing capabilities for analysis, classification, generation, and information processing.

### CMP-009. Persistence

Responsible for managing the storage, retrieval, and updating of information used by the automation.

### CMP-010. Configuration management

Responsible for administering the configuration parameters that control the behavior of the system.

### CMP-011. Observability

Responsible for collecting logs, metrics, and evidence necessary for monitoring, diagnosis, and auditing of the automation's operation.

### CMP-012. Security

Responsible for implementing mechanisms to protect information, control access to resources, and preserve the integrity of the system.

### CMP-013. Error handling

Responsible for detecting, classifying, logging, and coordinating the treatment of errors and exceptions according to the official model defined by the project.

### CMP-014. Shared services

Responsible for providing reusable functionalities that can be used by multiple components without duplicating implementation logic.

### Component organization principles

All components defined in this chapter must comply with the following general rules:

- Maintain clearly defined responsibilities.
- Communicate only through mechanisms defined by the architecture.
- Avoid unnecessary dependencies between components.
- Favor the reuse of common functionalities.
- Allow their independent evolution when technically feasible.
- Maintain compatibility with the official technology stack and with the rest of the project documentation.


---

## 6. Organization by modules

The architecture of the automation will be organized through independent modules, each with clearly defined responsibilities and a structure that facilitates the development, maintenance, and evolution of the system.

Modular organization constitutes one of the fundamental principles of the architecture and aims to reduce coupling between components, favor reuse, and allow the incorporation of new capabilities without affecting the stability of the system.

The architecture will be organized into the following module groups.

### 6.1. Business modules

Business modules implement the main functional flow of the automation and represent the processes directly related to the management of job opportunities.

This group is composed of:

- Opportunity discovery.
- Initial offer preparation.
- Initial evaluation.
- Offer processing.
- Result management.

Each of these modules must execute only the responsibilities specific to the business process it represents.

### 6.2. Platform modules

Platform modules provide reusable technical capabilities necessary to support the operation of business processes.

This group includes, among others:

- Decision engine.
- Web automation engine.
- Artificial intelligence engine.
- Persistence.

These modules must offer reusable services without incorporating specific business process logic.

### 6.3. Infrastructure modules

Infrastructure modules provide capabilities necessary for the operation, administration, and supervision of the system.

This group includes, among others:

- Configuration management.
- Observability.
- Security.
- Error handling.
- Shared services.

These modules must remain decoupled from functional logic and provide common services to the rest of the architecture.

### 6.4. Relationships between modules

Interaction between modules must respect the following general rules:

- Each module must maintain a clearly defined responsibility.
- Business modules may use services provided by platform and infrastructure modules.
- Platform modules must not depend on specific business processes.
- Infrastructure modules must not incorporate functional logic specific to business processes.
- All communication between modules must be carried out through the mechanisms defined by the architecture.

### 6.5. Modular evolution

The incorporation of new modules must be done preserving the organization defined in this chapter.

Every new module must be classified within one of the established architectural groups or, when strictly necessary, the creation of a new group must be formally justified without affecting the overall coherence of the architecture.

---

## 7. Layered architecture

All modules that make up the architecture of the automation must maintain a uniform internal organization based on functional layers and technical layers.

The purpose of this organization is to guarantee a clear separation of responsibilities, reduce coupling between components, facilitate system maintenance, and allow the independent evolution of each module.

The layered architecture defined in this chapter will be mandatory for all modules developed as part of the project.

### 7.1. Functional layers

Functional layers implement the logic specific to the module and represent the business behavior.

#### Interface layer

Responsible for receiving requests, delivering results, and acting as the entry and exit point of the module.

It must not implement business logic.

#### Orchestration layer

Responsible for coordinating the internal execution flow of the module.

Its function is to organize the sequence of operations necessary to complete a process, delegating specific work to the corresponding services.

#### Service layer

Responsible for implementing the functional logic of the module through specialized services.

Each service must maintain a clearly defined responsibility.

#### Domain layer

Responsible for representing the business rules, conceptual entities, and models specific to the module.

Domain rules must remain independent of technological or infrastructure aspects.

### 7.2. Technical layers

Technical layers provide capabilities necessary for the operation of the module without being part of the business logic.

#### Integrations layer

Responsible for managing communication with other modules, internal services, and authorized external resources.

#### Persistence layer

Responsible for storing, retrieving, and updating the information required by the module.

#### Configuration layer

Responsible for administering the specific configuration parameters of the module.

#### Observability layer

Responsible for generating logs, metrics, and evidence necessary for monitoring and diagnosis of the module's operation.

#### Error handling layer

Responsible for detecting, classifying, logging, and managing errors and exceptions according to the official project model.

### 7.3. Dependencies between layers

Relationships between layers must respect the following general rules:

- Each layer must fulfill a single clearly defined responsibility.
- Functional layers must not depend directly on specific technologies.
- Technical layers must not contain business-specific rules.
- All communication between layers must be carried out through clearly defined interfaces.
- Circular dependencies between layers must be avoided.

### 7.4. Architectural uniformity

All modules must implement the same layer organization defined in this chapter.

Only those layers whose responsibility is not necessary for a specific module may be omitted, provided such omission does not affect the coherence of the general architecture.

The incorporation of new layers must be formally justified and maintain compatibility with the architectural principles established in this document.

---

## 8. General flow of interaction between modules

Interaction between the modules of the architecture must be carried out in a controlled, explicit manner consistent with the architectural principles defined in this document.

The objective of this chapter is to establish the official rules of communication between modules, guaranteeing a decoupled, maintainable architecture prepared to evolve without introducing unnecessary dependencies.

### 8.1. General execution flow

The main functional flow of the automation will follow this sequence:

1. Opportunity discovery.
2. Initial offer preparation.
3. Initial evaluation.
4. Offer processing.
5. Result management.

Each module will be exclusively responsible for the activities corresponding to its stage of the process.

### 8.2. Use of cross-cutting services

During their execution, functional modules may use the services provided by platform and infrastructure components when necessary to fulfill their responsibilities.

The use of such services will not alter the main functional flow of the automation.

### 8.3. Official communication rules

#### RCM-001. Communication through public interfaces

Every module must interact with other modules exclusively through the official interfaces defined by the architecture.

#### RCM-002. Prohibition of internal access

No module may directly access internal components belonging to another module.

#### RCM-003. Unidirectional dependencies

Dependencies between modules must maintain a single direction of communication.

Circular dependencies are not permitted.

#### RCM-004. Use of shared services

Any reusable functionality must be obtained through the shared services defined by the architecture.

Logic already existing in other components must not be duplicated.

#### RCM-005. Functional independence

Functional modules must not depend on the internal operation of the technical services used during their execution.

#### RCM-006. Explicit communication

All interaction between modules must be clearly defined, documented, and controlled.

There must be no implicit dependencies.

#### RCM-007. Error isolation

Each module will be responsible for managing errors generated during the execution of its own responsibilities before propagating any result to other modules.

#### RCM-008. Respect for the official flow

All interaction between modules must respect the official processing flow defined for the automation.

Exceptions to this flow may only occur when expressly authorized by the project rules.

### 8.4. Interaction principles

Communications between modules must permanently comply with the following principles:

- Maintain low coupling.
- Favor service reuse.
- Preserve functional independence.
- Facilitate information traceability.
- Minimize the impact of architectural changes.
- Maintain coherence with the official decision model and the data flow of the project.


---

## 9. Shared services

Shared services constitute the set of reusable capabilities that may be used by multiple modules of the automation without duplicating implementation logic.

Their purpose is to centralize common functionalities, maintain architectural consistency, and reduce coupling between the different components of the system.

Every shared service must maintain a clearly defined responsibility, a public usage interface, and compatibility with the architectural principles established in this document.

### 9.1. Domain services

Domain services provide capabilities directly related to the operation of the automation business.

#### SRV-001. Decision engine

**Purpose**

Execute the official decision model of the project.

**Responsibility**

Apply the approved decision rules to determine the behavior of the automation.

---

#### SRV-002. Artificial intelligence engine

**Purpose**

Provide capabilities for analysis, classification, generation, and processing of information through artificial intelligence models.

**Responsibility**

Centralize all interaction with the AI models used by the automation.

---

#### SRV-003. Web automation engine

**Purpose**

Manage automated interaction with target platforms.

**Responsibility**

Control navigation, information extraction, and execution of authorized actions.

### 9.2. Infrastructure services

Infrastructure services provide common technical capabilities necessary for the operation of the entire architecture.

#### SRV-004. Persistence

**Purpose**

Manage the storage and retrieval of system information.

**Responsibility**

Guarantee the availability and integrity of the data used by the automation.

---

#### SRV-005. Configuration management

**Purpose**

Manage the configuration parameters of the system.

**Responsibility**

Allow adjusting the behavior of the automation without modifying the implementation.

**Credentials storage**

Credentials and secrets used by the integrations must be stored in a secure repository managed by this service. For the first version (MVP) of the automation, such a repository is implemented as an environment variable file (`.env`) loaded exclusively through an official environment loader, and its values must be referenced in the system configuration without being embedded in the configuration itself.

Credentials must never be included in version-controlled files, application database, logs, or execution records.

---

#### SRV-006. Logging and auditing

**Purpose**

Centralize the generation of logs and evidence of the system's operation.

**Responsibility**

Facilitate traceability, auditing, and diagnosis of the automation.

---

#### SRV-007. Observability

**Purpose**

Provide metrics, indicators, and monitoring mechanisms.

**Responsibility**

Facilitate continuous supervision of the system's behavior.

---

#### SRV-008. Security

**Purpose**

Protect information and control access to system resources.

**Responsibility**

Implement the protection mechanisms defined by the architecture.

---

#### SRV-009. Error handling

**Purpose**

Centrally manage errors and exceptions produced during system execution.

**Responsibility**

Apply the official error handling model of the project.

---

#### SRV-010. File system management

**Purpose**

Manage access to resources stored in the file system.

**Responsibility**

Centralize operations related to reading, writing, and organizing files used by the automation.

### 9.3. General rules for shared services

All services defined in this chapter must comply with the following rules:

- Maintain a single clearly defined responsibility.
- Be reusable by multiple modules.
- Expose only clearly documented public interfaces.
- Remain decoupled from specific business processes when applicable.
- Avoid circular dependencies with other services.
- Maintain compatibility with the official technology stack.
- Facilitate the independent evolution of their implementation.

---

## 10. Integration architecture with external systems

The architecture of the automation must maintain a strict separation between the internal components of the system and the external resources with which it interacts during its execution.

All integration with external systems must be carried out through abstraction mechanisms that isolate business logic from the technological particularities of each resource, favoring maintainability, scalability, and independent evolution of the architecture.

No functional module should communicate directly with an external system.

### 10.1. Integration model

Every integration must be implemented through an architectural adapter responsible for:

- Receiving requests from internal modules.
- Validating the exchanged information.
- Translating data into the format required by the external system.
- Normalizing received responses.
- Managing communication errors.
- Logging relevant integration events.
- Isolating changes produced by modifications in the external system.

This model must be applied uniformly to all integrations incorporated into the project.

### 10.2. Official integration catalog

#### INT-001. Job search platform

**Purpose**

Provide access to job opportunities published on the target platform defined for the project.

**Responsibility**

Allow obtaining information and executing authorized actions during the automation process.

---

#### INT-002. Artificial intelligence model provider

**Purpose**

Provide access to the artificial intelligence models used by the automation.

**Responsibility**

Execute processing requests made by the Artificial Intelligence Engine without exposing implementation details to consuming modules.

---

#### INT-003. Automated browser

**Purpose**

Provide the execution environment necessary for automating interaction with web platforms.

**Responsibility**

Allow automated navigation and controlled execution of actions on web resources according to the policies defined by the project.

### 10.3. General integration rules

All integrations must comply with the following rules:

- Maintain clearly defined interfaces.
- Remain decoupled from business logic.
- Centralize communication error management.
- Normalize information exchanged with external systems.
- Facilitate substitution of the external resource when necessary.
- Log relevant events for auditing and diagnostic purposes.
- Maintain compatibility with the architectural principles defined in this document.

### 10.4. Internal technological resources

Technological resources used exclusively by the internal architecture of the system, such as the database and file system, are not part of the external integration catalog.

Their use must be carried out through the corresponding shared services and will be documented in the specific chapters on persistence and infrastructure of this architecture.


---

## 11. Persistence architecture

The persistence architecture defines the principles and rules that will govern the management of all information used by the automation during its lifecycle.

Its purpose is to ensure that information is stored, retrieved, protected, and managed consistently, preserving its integrity, traceability, and availability.

The implementation of these capabilities will be the responsibility of the shared Persistence service (SRV-004), while this chapter establishes the architectural rules that must be respected for the organization of information.

### 11.1. Organization of information

The information managed by the automation must be organized according to its nature and purpose.

#### Operational information

Corresponds to information generated during the normal execution of the automation.

Includes, among others:

- Discovered job opportunities.
- Information prepared for evaluation.
- Evaluation results.
- Processed information.
- Execution states.

#### Configuration information

Corresponds to the parameters that determine the behavior of the system.

Includes, among others:

- General parameters.
- Module configuration.
- Thresholds.
- Operation variables.
- System preferences.

#### Operational evidence

Corresponds to information used for monitoring, auditing, and diagnosis.

Includes, among others:

- Event logs.
- Errors.
- Audits.
- Metrics.
- Execution evidence.

#### Documentary resources

Corresponds to documents used by the automation as part of its operation.

Includes, among others:

- Resume.
- Professional portfolio.
- Templates.
- Official project documentation.

### 11.2. Official persistence rules

#### RP-001. Organization by information type

All persisted information must be classified according to the categories defined in this chapter.

#### RP-002. Access through the Persistence service

Architecture modules may only access persisted information using the shared Persistence service (SRV-004).

#### RP-003. Prohibition of direct storage access

No functional module may interact directly with physical storage mechanisms.

#### RP-004. Information integrity

The architecture must preserve the consistency and integrity of information during all storage and retrieval operations.

#### RP-005. Traceability

Every relevant modification to persisted information must be identifiable and traceable according to the policies defined by the project.

#### RP-006. Business decoupling

Persistence rules must remain independent of the functional logic implemented by the system modules.

#### RP-007. Compatibility with the data model

The organization of information must remain aligned with the official Data Model of the project.

#### RP-008. Controlled evolution

The incorporation of new types of information or storage mechanisms must preserve compatibility with the architecture defined in this document.

### 11.3. General persistence principles

The persistence architecture must guarantee:

- Clear separation between business logic and storage.
- Consistent organization of information.
- Traceability of data managed by the system.
- Reuse of the Persistence service by all modules.
- Compatibility with the official technology stack.
- Preparation for the future evolution of the automation.


---

## 12. Artificial intelligence architecture

The artificial intelligence architecture defines the rules that govern the use of artificial intelligence models within the automation.

Its purpose is to ensure that artificial intelligence capabilities are used in a consistent, controlled manner decoupled from business logic, preserving the maintainability, traceability, and evolution of the architecture.

The use of artificial intelligence will be the exclusive responsibility of the shared service Artificial Intelligence Engine (SRV-002), while this chapter establishes the architectural rules that must be followed during its use.

### 12.1. Role of artificial intelligence

Artificial intelligence constitutes a specialized information processing mechanism.

Its function is to execute tasks of analysis, extraction, classification, transformation, and content generation when such capabilities are required by business processes.

Artificial intelligence does not constitute a mechanism for controlling the execution flow nor does it implement business rules.

### 12.2. Authorized responsibilities

Artificial intelligence may be used for activities such as:

- Structured information extraction.
- Content classification.
- Information summarization.
- Text analysis.
- Content generation when the process requires it.
- Transformation of information between formats compatible with the automation.

Every use must be aligned with the officially defined responsibilities for each module of the system.

### 12.3. Unauthorized responsibilities

Artificial intelligence must not:

- Implement business rules.
- Replace the Decision Engine (SRV-001).
- Control the execution flow of the automation.
- Directly modify persisted information.
- Alter system configurations.
- Execute actions outside the scope authorized by the project processes.

### 12.4. Official rules for the use of artificial intelligence

#### RAI-001. Access through the official service

All use of artificial intelligence models must be carried out exclusively through the Artificial Intelligence Engine (SRV-002).

#### RAI-002. Separation of responsibilities

Artificial intelligence will only perform information processing tasks.

Functional decisions will remain under the responsibility of the Decision Engine (SRV-001).

#### RAI-003. Business independence

Artificial intelligence models must not contain specific knowledge about the business rules of the automation.

#### RAI-004. Centralized instruction management

The instructions used to interact with the models must be managed centrally, allowing their controlled evolution.

#### RAI-005. Input validation

All information sent to the models must be previously validated according to the rules defined by the architecture.

#### RAI-006. Response normalization

Responses generated by the models must be transformed into formats compatible with the internal processes of the automation before being used by other modules.

#### RAI-007. Traceability

All interaction with artificial intelligence models must be recordable and auditable when applicable.

#### RAI-008. Uniform error handling

Errors produced during the use of artificial intelligence must be managed through the official error handling mechanisms defined by the architecture.

#### RAI-009. Vendor independence

The architecture must minimize specific dependencies on a particular artificial intelligence provider or model, facilitating its replacement when necessary.

#### RAI-010. Controlled evolution

The incorporation of new models, capabilities, or usage strategies must preserve compatibility with the general architecture of the system.

### 12.5. General principles

The artificial intelligence architecture must guarantee:

- Separation between intelligent processing and business logic.
- Consistent use of artificial intelligence models.
- Independence from the technology vendor.
- Traceability of requests made.
- Compatibility with the Decision Engine.
- Controlled evolution of artificial intelligence capabilities incorporated into the project.


---

## 13. Configuration management

The configuration management architecture defines the principles and rules that govern the administration of all parameters used by the automation.

Its purpose is to ensure that the behavior of the system can be adjusted in a controlled, consistent, and maintainable manner, without requiring modifications to the implementation of components.

Configuration administration will be the exclusive responsibility of the shared service Configuration Management (SRV-005), while this chapter establishes the architectural rules that must be respected throughout the entire lifecycle of the system.

### 13.1. Configuration organization

The system configuration must be organized according to its scope of application.

#### Global configuration

Corresponds to parameters that affect the general operation of the automation.

Includes, among others:

- General system parameters.
- Execution environment configuration.
- Main directories.
- Global operation options.

#### Module configuration

Corresponds to the specific parameters used by each module of the architecture.

Includes, among others:

- Opportunity Discovery parameters.
- Initial Preparation parameters.
- Initial Evaluation parameters.
- Offer Processing parameters.
- Result Management parameters.

#### Integration configuration

Corresponds to parameters necessary for interaction with external resources.

Includes, among others:

- Automated browser configuration.
- Target platform configuration.
- Artificial intelligence provider configuration.

#### Operational configuration

Corresponds to parameters used by the technical services of the architecture.

Includes, among others:

- Observability.
- Logging and auditing.
- Persistence.
- Security.
- Error handling.

### 13.2. Official configuration rules

#### RCF-001. Centralized configuration

All system configuration must be managed through the official Configuration Management service (SRV-005).

#### RCF-002. Prohibition of embedded configuration

Configurable parameters must not be hard-coded directly in the implementation of modules.

#### RCF-003. Configuration validation

All configuration must be validated before being used by any component of the system.

#### RCF-004. Access through the official service

Modules may only access configuration through the public interfaces provided by SRV-005.

#### RCF-005. Versioning

Relevant configuration modifications must allow their identification and control according to the strategy defined by the project.

#### RCF-006. Separation between configuration and data

System configuration must be kept separate from the operational information managed by the persistence architecture.

#### RCF-007. Reuse

Common parameters must be centralized to avoid duplication and guarantee uniform behavior.

#### RCF-008. Controlled evolution

The incorporation of new parameters must preserve compatibility with the existing architecture and remain aligned with the official project documentation.

### 13.3. Configuration restrictions

Configuration must not:

- Implement business rules.
- Control the functional flow of the automation.
- Replace the responsibilities of the Decision Engine.
- Contain processing logic.
- Modify the architectural structure of the system.

Its purpose will be exclusively to parameterize the behavior of previously defined components of the architecture.

### 13.4. General principles

The configuration management architecture must guarantee:

- Centralization of configuration.
- Separation between configuration and business logic.
- Consistency between modules.
- Ease of maintenance.
- Traceability of changes.
- Compatibility with the official technology stack.
- Controlled evolution of the system configuration.


---

## 14. Security architecture

The security architecture defines the principles and rules that govern the protection of information, components, and resources used by the automation.

Its purpose is to preserve the confidentiality, integrity, and availability of system assets, ensuring that security is part of the architectural design and does not depend exclusively on technological implementation.

Security capabilities will be provided by the shared service Security (SRV-008), while this chapter establishes the architectural rules that must be followed throughout the automation.

### 14.1. Protected assets

The architecture must protect, at a minimum, the following assets:

#### Information

All information managed by the automation, including operational data, configurations, documents, and processing results.

#### Configuration

The parameters that control the behavior of the system and its modules.

#### Credentials and secrets

All information used for authentication, authorization, or access to protected resources.

#### External integrations

Communications between the automation and authorized external resources.

#### System execution

The normal operation of the modules, services, and processes that make up the architecture.

### 14.2. Information sensitivity classification

The information used by the automation must be classified according to its sensitivity level.

#### Public

Information whose disclosure does not represent a risk to the project.

#### Internal

Information intended exclusively for the internal operation of the automation.

#### Confidential

Personal, operational, or strategic information whose unauthorized disclosure may affect the operation of the system or the privacy of the user.

#### Secret

Information whose access must be restricted to the maximum level permitted by the architecture.

Includes, among others:

- Credentials.
- Tokens.
- Access keys.
- Secrets used by integrations.

### 14.3. Official security rules

#### RSA-001. Principle of least privilege

Each component must access only the resources strictly necessary to fulfill its responsibilities.

#### RSA-002. Mandatory input validation

All information received by any component must be validated before being processed.

#### RSA-003. Credential protection

Credentials and secrets must not be stored or exposed outside the mechanisms authorized by the architecture.

#### RSA-004. Secure secrets management

Secrets used by the automation must be managed through centralized and controlled mechanisms.

#### RSA-005. Isolation of sensitive information

Information classified as confidential or secret must be kept isolated from other information when necessary.

#### RSA-006. Auditing of critical actions

Every operation considered critical for system security must be recordable and auditable.

#### RSA-007. Protection of external integrations

All communication with external resources must be carried out through the integration mechanisms defined by the architecture.

#### RSA-008. Information integrity

The architecture must preserve the integrity of information throughout its entire lifecycle.

#### RSA-009. Controlled recovery

Security-related incidents must be managed in a controlled manner to minimize their impact on the operation of the system.

#### RSA-010. Controlled evolution

The incorporation of new security mechanisms must preserve compatibility with the general architecture of the system.

### 14.4. General security principles

The security architecture must guarantee:

- Protection proportional to the sensitivity level of the information.
- Separation between business logic and security mechanisms.
- Protection of credentials and secrets.
- Integrity of information managed by the system.
- Traceability of critical actions.
- Compatibility with the official technology stack.
- Controlled evolution of the security architecture.


---

## 15. Observability architecture

The observability architecture defines the principles and rules that allow monitoring, understanding, and diagnosing the behavior of the automation throughout its entire execution cycle.

Its purpose is to provide sufficient information to evaluate the operation of the system, detect anomalies, facilitate incident diagnosis, and support the continuous evolution of the architecture.

Observability capabilities will be provided by the shared service Observability (SRV-007), while this chapter establishes the architectural rules that must be followed for the generation, organization, and use of observational information.

### 15.1. Organization of observability

The information generated by the architecture must be organized according to its purpose.

#### Operational evidence

Corresponds to events generated during the execution of the automation.

Includes, among others:

- Process start and completion.
- State changes.
- Relevant execution events.
- Warnings.
- Errors.

#### Operational metrics

Corresponds to indicators used to evaluate the behavior of the system.

Includes, among others:

- Execution time.
- Number of opportunities processed.
- Integration response time.
- Utilization of shared services.
- Requests made to artificial intelligence.

#### Process traceability

Corresponds to information necessary to reconstruct the complete path of an operation within the architecture.

Includes, among others:

- Flow followed by each process.
- Components involved.
- Services used.
- Integrations invoked.
- Decisions executed.

### 15.2. Official observability rules

#### ROA-001. Uniform event logging

All components must generate events using a consistent format defined by the architecture.

#### ROA-002. Metric generation

Components must produce the metrics necessary to evaluate their behavior and performance.

#### ROA-003. Process traceability

The architecture must allow reconstructing the complete path of relevant operations executed by the system.

#### ROA-004. Decoupled observability

The generation of evidence must not modify or interfere with the functional logic of the modules.

#### ROA-005. Component identification

Every piece of evidence generated must allow identifying the component responsible for its origin.

#### ROA-006. Event correlation

Evidence related to the same operation must be associable with each other to facilitate analysis.

#### ROA-007. Error logging

Errors must be logged according to the official error handling model defined by the architecture.

#### ROA-008. Controlled evolution

The incorporation of new evidence, metrics, or observability mechanisms must preserve compatibility with the general architecture of the system.

### 15.3. General observability principles

The observability architecture must guarantee:

- Understanding of the system's behavior.
- Incident diagnosis.
- Objective performance measurement.
- Process traceability.
- Compatibility with the official error handling model.
- Separation between observability and business logic.
- Controlled evolution of monitoring capabilities.


---

## 16. Scalability strategy

The scalability strategy defines the principles and rules that will allow expanding the capabilities of the automation progressively, preserving the stability, coherence, and maintainability of the architecture.

Its purpose is to ensure that the incorporation of new functionalities, modules, services, and integrations can be carried out without requiring significant redesign of the existing architecture.

Scalability must be achieved primarily through the evolution of the architecture and not exclusively through the increase of technological resources.

### 16.1. Functional scalability

The architecture must allow the incorporation of new business processes without affecting the operation of existing modules.

Among others, it must facilitate the incorporation of:

- New functional modules.
- New processing flow stages.
- New analysis criteria.
- New automation processes.

### 16.2. Service scalability

The architecture must allow incorporating new reusable shared services without modifying existing services.

Every new service must respect the architectural principles defined in this document.

### 16.3. Integration scalability

The architecture must allow incorporating new external integrations while maintaining the official integration model established in Chapter 10.

The incorporation of new platforms or providers must not affect the operation of consuming modules.

### 16.4. Information scalability

The architecture must allow managing a progressive growth in the volume of persisted information without modifying the architectural organization of the system.

The evolution of the data model must remain compatible with the persistence architecture defined in this document.

### 16.5. Operational scalability

The architecture must allow increasing the execution frequency, the number of automated processes, and the processing volume while preserving the stability of the system.

### 16.6. Official scalability rules

#### REA-001. Scalability through composition

The evolution of the system should be done preferably by incorporating new components, avoiding modification of existing ones.

#### REA-002. Compatible evolution

Every expansion must maintain compatibility with the general architecture of the system.

#### REA-003. Service reuse

Whenever possible, new capabilities should reuse existing shared services.

#### REA-004. Controlled incorporation of integrations

Every new integration must conform to the official integration model defined by the architecture.

#### REA-005. Module independence

The incorporation of new modules must not create unnecessary dependencies on existing modules.

#### REA-006. Documentary compatibility

Every expansion must remain aligned with the official project documentation.

#### REA-007. Progressive scalability

The architecture must allow incorporating new capabilities incrementally, avoiding structural redesigns.

#### REA-008. Documented evolution

Every modification related to scalability must be documented and formally justified before being incorporated into the project.

### 16.7. General scalability principles

The scalability strategy must guarantee:

- Progressive growth of the architecture.
- Controlled incorporation of new capabilities.
- Preservation of modularity.
- Reuse of components and services.
- Compatibility with the official technology stack.
- Sustainable evolution throughout the entire project lifecycle.

---

## 17. Extensibility strategy

The extensibility strategy defines the principles and rules that will allow incorporating new capabilities into the automation without unnecessarily altering existing components.

Its purpose is to ensure that the architecture can evolve in a controlled manner, maintaining the stability, compatibility, and coherence of the system throughout its entire lifecycle.

Extensibility must be achieved through the incorporation of new architectural elements that respect the interfaces, principles, and rules defined in this document.

### 17.1. Functional extensibility

The architecture must allow incorporating new business processes without modifying the behavior of existing modules.

New functional capabilities must be implemented through new modules or extensions compatible with the official architectural organization.

### 17.2. Component extensibility

The architecture must allow incorporating new components when it is necessary to expand the capabilities of the system.

Every new component must comply with the architectural principles, modular organization, and layered architecture established in this document.

### 17.3. Service extensibility

The incorporation of new shared services must be done preserving the independence of existing services.

New services must be integrated through public interfaces and maintain compatibility with the official catalog of shared services.

### 17.4. Integration extensibility

The architecture must allow incorporating new platforms, providers, or external resources while respecting the official integration model defined for the project.

New integrations must not require modifications to consuming modules.

### 17.5. Artificial intelligence extensibility

The architecture must allow incorporating new models, processing strategies, instructions, or artificial intelligence capabilities without affecting the operation of modules that use the official artificial intelligence service.

The evolution of these capabilities must remain decoupled from business logic.

### 17.6. Official extensibility rules

#### REX-001. Extension through incorporation

Every new capability should be implemented preferably by incorporating new components, modules, or services.

#### REX-002. Preservation of existing components

Whenever technically feasible, extensions must not require modifications to previously stabilized components.

#### REX-003. Compatibility with public interfaces

New capabilities must exclusively use the public interfaces defined by the architecture.

#### REX-004. Reuse of shared services

Every extension must reuse existing shared services when they satisfy the required functional needs.

#### REX-005. Documentary compatibility

Every expansion must remain aligned with the official project documentation.

#### REX-006. Decoupling of extensions

New capabilities must be designed in a way that minimizes dependencies on existing components.

#### REX-007. Incremental evolution

Extensions must be incorporable progressively without affecting the stability of the architecture.

#### REX-008. Mandatory documentation

Every new extension must be documented and formally justified before being incorporated into the project.

### 17.7. General extensibility principles

The extensibility strategy must guarantee:

- Controlled incorporation of new capabilities.
- Preservation of architectural stability.
- Reuse of existing components and services.
- Low coupling between extensions and existing components.
- Compatibility with the official technology stack.
- Sustainable evolution of the architecture throughout the entire project lifecycle.


---

## 18. Architectural constraints

Architectural constraints constitute the set of mandatory conditions that must be respected during the design, implementation, maintenance, and evolution of the automation.

Their purpose is to preserve the coherence of the official project architecture, avoiding deviations that compromise the modularity, maintainability, scalability, or compatibility of the system.

The constraints defined in this chapter consolidate the principles, objectives, and rules established in the previous chapters and do not introduce new architectural requirements.

### 18.1. Structural constraints

#### RAR-001. Mandatory use of the official architecture

Every implementation must respect the architectural organization defined in this document.

#### RAR-002. Respect for modular organization

Components must be organized according to the modular structure established by the architecture.

#### RAR-003. Respect for layered architecture

Every module must implement the layer organization defined in Chapter 7.

#### RAR-004. Communication through public interfaces

Components may only communicate using the official interfaces defined by the architecture.

#### RAR-005. Prohibition of circular dependencies

Circular dependencies between modules, components, or services are not permitted.

### 18.2. Functional constraints

#### RAR-006. Respect for the official flow

The implementation must maintain the functional flow defined for the automation.

#### RAR-007. Separation between intelligent processing and business logic

Artificial intelligence must not replace the responsibilities of the Decision Engine nor implement business rules.

#### RAR-008. Use of shared services

Any reusable functionality must be implemented through the shared services defined by the architecture.

#### RAR-009. Separation between business and infrastructure

Functional logic must remain decoupled from technological infrastructure and integration mechanisms.

### 18.3. Technological constraints

#### RAR-010. Compatibility with the technology stack

Every implementation must use the official technology stack approved for the project.

#### RAR-011. Controlled integrations

All communication with external resources must be carried out through the official integration model defined by the architecture.

#### RAR-012. Decoupled persistence

Functional modules must not directly access storage mechanisms.

All interaction with persisted information must be carried out through the official Persistence service.

#### RAR-013. Centralized configuration

System configuration must be managed exclusively through the official Configuration Management service.

### 18.4. Documentary constraints

#### RAR-014. Compatibility with official documentation

Every implementation must remain aligned with Documents 0 through 12 and with the officially approved decisions for the project.

#### RAR-015. Traceability of changes

Every architectural modification must be documented, justified, and remain traceable with respect to the previous version.

#### RAR-016. Controlled evolution

Every expansion of the architecture must preserve compatibility with the objectives, principles, and constraints defined in this document.

### 18.5. Compliance principles

Every implementation of the architecture must demonstrate compliance with the constraints established in this chapter before being considered compatible with the official project architecture.

Non-compliance with any of these constraints must be treated as an architectural deviation and will require its corresponding analysis, justification, and formal approval before its incorporation into the project.


---

## 19. Acceptance criteria

The acceptance criteria define the official mechanism for verifying that an implementation, modification, or expansion of the automation complies with the architecture established in this document.

Their purpose is to provide an objective, uniform, and traceable validation process that allows determining the architectural conformity of the system before its incorporation into the project.

The criteria defined in this chapter consolidate all the objectives, principles, rules, and constraints previously established, without introducing new architectural requirements.

### 19.1. Scope of validation

The acceptance criteria must be applied, at a minimum, in the following cases:

- Implementation of new modules.
- Incorporation of new components.
- Development of new shared services.
- Incorporation of new integrations.
- Architectural modifications.
- Refactorings with structural impact.
- MVP validation.
- Validation of subsequent versions of the automation.

### 19.2. Architectural conformity matrix

Every validation must verify compliance with the following groups of criteria:

#### CA-001. Architectural objectives

The implementation must comply with the Architectural Objectives (OA) defined in this document.

#### CA-002. Architectural principles

The implementation must respect the Architectural Principles (PA).

#### CA-003. Official components

The implementation must correctly use the Architectural Components (CMP) defined by the architecture.

#### CA-004. Shared services

The implementation must use the Shared Services (SRV) according to the officially defined responsibilities.

#### CA-005. Communication between modules

The implementation must respect the Communication Rules between Modules (RCM).

#### CA-006. Persistence architecture

The implementation must comply with the Persistence Rules (RP).

#### CA-007. Artificial intelligence architecture

The implementation must comply with the Artificial Intelligence Architecture Rules (RAI).

#### CA-008. Configuration management

The implementation must respect the Configuration Rules (RCF).

#### CA-009. Security architecture

The implementation must comply with the Architectural Security Rules (RSA).

#### CA-010. Observability architecture

The implementation must comply with the Architectural Observability Rules (ROA).

#### CA-011. Scalability strategy

The implementation must respect the Architectural Scalability Rules (REA).

#### CA-012. Extensibility strategy

The implementation must comply with the Architectural Extensibility Rules (REX).

#### CA-013. Architectural constraints

The implementation must comply with all Official Architectural Constraints (RAR).

### 19.3. Validation result

Each acceptance criterion must be evaluated using exclusively one of the following outcomes:

- **Compliant:** The criterion is fully satisfied.
- **Non-compliant:** The criterion is not satisfied.
- **Not applicable:** The criterion is not applicable to the element being evaluated.

No intermediate states or subjective interpretations should be used during the validation process.

### 19.4. Approval criteria

An implementation may be considered compatible with the official architecture only when:

- It complies with all applicable criteria.
- It does not violate any architectural constraint.
- It maintains compatibility with the official project documentation.
- It preserves the structural coherence of the architecture.

Every deviation identified during validation must be documented, justified, and resolved before approving its incorporation into the project.

### 19.5. General validation principles

The architectural validation process must guarantee:

- Objectivity in evaluation.
- Traceability of results.
- Uniformity of criteria.
- Repeatability of the validation process.
- Compatibility with all official project documentation.
- Controlled evolution of the architecture throughout the entire system lifecycle.


---

## 20. Consolidated architectural view

The Consolidated Architectural View constitutes the official representation of the general architecture of the job search automation.

Its purpose is to integrate, in a single coherent representation, all architectural elements defined in this document, providing a high-level view that facilitates understanding of the system organization and the relationships between its main components.

The consolidated view synthesizes the official architecture through the integration of:

- The general organization of the architecture.
- The business modules.
- The main components.
- The shared services.
- The external integrations.
- The layered architecture.
- The general flow of interaction between modules.
- The specialized architectures defined for persistence, artificial intelligence, configuration, security, and observability.
- The scalability and extensibility strategies.
- The architectural constraints and the official acceptance criteria.

The Consolidated Architectural View constitutes the main reference point for understanding the structural organization of the system and must remain permanently synchronized with the architectural decisions officially approved for the project.

Every modification that affects the general architecture must be reflected both in the corresponding chapters of this document and in the consolidated architectural representation, preserving coherence between the documentation and the current architecture.

The official graphical representation of the architecture is an integral part of this document and constitutes the authorized visual reference for interpreting the general structure of the system.

> **Note:** The official diagram of the Consolidated Architectural View will be created and maintained as part of the architectural documentation of the project, and must faithfully reflect all decisions approved in this document.
