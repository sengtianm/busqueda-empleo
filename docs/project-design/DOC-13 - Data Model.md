# Document 13 - Data Model

## 1. Purpose of the document

This document defines the official data model for the job search automation.

Its purpose is to establish, organize, and document the logical structure of the information used by the automation, ensuring that all entities, attributes, relationships, constraints, integrity rules, and persistence mechanisms are consistent with the objectives, scope, requirements, and architecture defined for the project.

This document constitutes the official reference for the design, implementation, maintenance, and evolution of the data model. No element related to information management shall be added, modified, or removed without having been previously analyzed and documented in accordance with the criteria established in this document.

The decisions documented herein must remain consistent with Documents 0 through 12, including the functional and non-functional requirements, the decision model, the data flow, the project standards, the error handling model, the folder architecture, the scope and objectives, the technology stack, and the general system architecture.

The data model must guarantee the integrity, consistency, traceability, maintainability, and scalability of the information throughout the entire lifecycle of the job offers and the processes executed by the automation.

Likewise, this document will serve as the foundation for the implementation of the persistence layer, data access, and MVP development, ensuring that all implementation decisions are supported by a previously analyzed, justified, and approved data model.

Any modification to the data model must be documented, justified, and formally approved before being incorporated into the project, preserving historical traceability and coherence with the rest of the official documentation.

---

## 2. Data model principles

The design, implementation, maintenance, and evolution of the automation's data model must be carried out in accordance with the principles defined in this chapter.

These principles constitute the official rules that must be respected during the definition of entities, attributes, relationships, constraints, validation rules, and any other component of the data model.

Every decision related to the data model must be properly justified and remain consistent with the previously approved official documentation.

The following official principles are established:

### PMD-001. Data integrity

The data model must permanently preserve the integrity of the information, avoiding inconsistent states or invalid relationships.

### PMD-002. Consistency

All stored information must remain consistent across the different modules, processes, and components of the automation.

### PMD-003. Uniqueness

Each entity must have mechanisms that allow unequivocal identification of each of its records where applicable.

### PMD-004. Normalization

The data model must minimize unnecessary information redundancy through a logical and structured organization of entities and their relationships.

### PMD-005. No data duplication

The same information must not be stored multiple times when it can be maintained through correctly defined relationships.

### PMD-006. Modularity

The data model must be organized in a modular fashion, facilitating its understanding, maintenance, and evolution.

### PMD-007. Scalability

The model structure must allow the incorporation of new entities, attributes, and relationships without requiring a significant reorganization of the existing model.

### PMD-008. Traceability

The data model must allow the reconstruction of the history of processes, decisions, and relevant changes made during the lifecycle of each job offer.

### PMD-009. Auditability

The information necessary for auditing and diagnosis must be preservable without affecting the integrity of the model.

### PMD-010. Controlled persistence

All persistent information must be stored according to clearly defined rules, avoiding orphaned, inconsistent, or unnecessary data.

### PMD-011. Technology independence

The data model must be defined independently of the database engine or any specific storage technology.

### PMD-012. Data validation

The model must facilitate the validation of data before its incorporation, modification, or use within the automation.

### PMD-013. Maintainability

The model structure must facilitate its updating, correction, and understanding throughout the entire useful life of the project.

### PMD-014. Extensibility

The model must allow the incorporation of new functional requirements through controlled extensions, preserving compatibility with existing information.

### PMD-015. Information security

The data model must facilitate the protection of the integrity, availability, and confidentiality of information in accordance with the project requirements.

### PMD-016. Separation between logical model and physical model

The conceptual and logical definition of the data must remain independent of its physical implementation in the database.

### PMD-017. Compatibility with the general architecture

The data model must be fully compatible with the general system architecture approved for the project.

### PMD-018. Compatibility with the data flow

The information structure must correctly support all transformations and movements defined in the official Data Flow.

### PMD-019. Compatibility with the decision model

The model must store all information necessary to support the approved Decision Model, preserving the traceability of each decision.

### PMD-020. Controlled evolution

Any modification to the data model must be documented, justified, and formally approved before being incorporated into the project.

---

## General principles of the data model

The data model must guarantee:

- Integrity and consistency of information.
- Elimination of unnecessary redundancies.
- Modularity and maintainability.
- Scalability and extensibility.
- Traceability and auditability.
- Technology independence.
- Compatibility with the general system architecture.
- Compatibility with the data flow and the decision model.
- Controlled evolution of the model.
- Coherence with all official project documentation.

---

## 3. Objectives of the data model

The objectives of the data model define the results that the information structure of the automation must achieve to efficiently, consistently, and traceably support all project processes.

Each objective represents a capability that must be preserved during the design, implementation, maintenance, and evolution of the data model.

---

### OMD-001. Centralize official information

Establish a data model that acts as the official source of information for all modules, processes, and components of the automation.

---

### OMD-002. Represent the project domain

Model in a structured way all entities, relationships, and attributes necessary to represent the complete process of searching and processing job opportunities.

---

### OMD-003. Guarantee information integrity

Ensure that all stored information maintains its consistency, validity, and coherence throughout its entire lifecycle.

---

### OMD-004. Support the offer lifecycle

Allow the storage and tracking of all information generated from the discovery of a job offer until the completion of its processing.

---

### OMD-005. Guarantee traceability

Preserve the information necessary to reconstruct the history of states, decisions, transformations, and operations performed on each job offer.

---

### OMD-006. Facilitate information exchange

Provide a uniform structure that allows consistent information exchange between all modules of the automation.

---

### OMD-007. Minimize redundancy

Organize information in a way that avoids unnecessary storage of duplicate data, favoring reuse through appropriate relationships.

---

### OMD-008. Facilitate auditing

Allow the recording and querying of information necessary for auditing, diagnosis, and operational monitoring of the system.

---

### OMD-009. Promote scalability

Design a model that allows the incorporation of new entities, relationships, and attributes without significantly affecting the existing structure.

---

### OMD-010. Promote maintainability

Maintain a clear, modular, and consistent organization that facilitates the evolution and understanding of the data model.

---

### OMD-011. Optimize information access

Provide a structure that facilitates the queries, searches, and operations required by the different modules of the system.

---

### OMD-012. Preserve technology independence

Define the data model independently of the database engine and any specific storage technology.

---

### OMD-013. Support project evolution

Allow the controlled incorporation of new functional requirements without compromising compatibility with previously stored information.

---

## General principles of data model objectives

The data model objectives must:

- Contribute directly to the fulfillment of the general project objectives.
- Maintain coherence with all official documentation.
- Guarantee the integrity, consistency, and traceability of information.
- Facilitate integration between automation modules.
- Promote the scalability and maintainability of the model.
- Remain independent of specific technologies.
- Serve as a reference for the design, validation, and evolution of the data model.

---

## 4. General architecture of the data model

The general architecture of the data model defines the conceptual organization of the information used by the job search automation.

Its purpose is to structure the data model in a modular, coherent way aligned with the general system architecture, the data flow, and the previously defined functional processes.

The organization established in this chapter constitutes the official model that must be respected during the design of all entities, relationships, attributes, and other components of the data model.

---

### 4.1. Architectural model

The data model adopts an architecture organized by functional domains, where each set of entities represents a specific responsibility within the automation.

This organization facilitates domain understanding, reduces coupling between entities, and promotes the independent evolution of each functional area of the system.

---

### 4.2. Opportunity discovery domain

Groups the entities responsible for representing the information obtained during the process of identifying and collecting job offers.

Entities belonging to this domain must store only the information corresponding to this stage of the operational flow.

---

### 4.3. Initial preparation domain

Groups the entities related to normalization, initial validation, and preparation of information before its evaluation.

This domain will be responsible for representing the data generated during the offer preparation stage.

---

### 4.4. Initial evaluation domain

Groups the entities responsible for representing the results obtained during the automatic evaluation of job offers.

Includes the information necessary to support the decision model and the initial classification of opportunities.

---

### 4.5. Offer processing domain

Groups the entities that represent the information generated during the deep processing of selected offers.

This domain will contain data related to diagnoses, analyses, document generation, results, and other specialized processes.

---

### 4.6. Shared services domain

Groups the entities reused by several modules of the automation.

Its purpose is to avoid data duplication and centralize common information used by different system processes.

---

### 4.7. Configuration domain

Groups the entities responsible for storing parameters, configurations, preferences, and other information used to control the behavior of the automation.

---

### 4.8. Audit and operation domain

Groups the entities intended for the operational monitoring of the system.

Includes the information necessary for auditing, traceability, error handling, execution logs, relevant events, and monitoring of the automation.

---

### 4.9. Relationships between domains

Each domain must maintain relationships only when there is a clearly identified functional need.

Relationships must minimize coupling between domains and preserve the functional independence of each one.

Any interaction between domains must respect the official data flow defined for the automation.

---

### 4.10. Principles of data model architecture

The general architecture of the data model must permanently preserve the following principles:

- Organization by functional domains.
- Low coupling between domains.
- High cohesion within each domain.
- Modularity.
- Scalability.
- Information reuse.
- Data integrity and consistency.
- Complete information traceability.
- Compatibility with the general system architecture.
- Controlled evolution of the model.

---

### 4.11. Architecture evolution

Any incorporation, modification, or deletion of entities must respect the general architecture defined in this document.

Any structural change must be documented, justified, and formally approved before its implementation, guaranteeing compatibility with the rest of the data model and with the official project documentation.

---

## 5. System entities

System entities represent the fundamental elements that make up the official data model of the job search automation.

Each entity must model a unique concept of the project domain, have a clearly defined responsibility, and maintain coherence with the data model principles, the general system architecture, the data flow, and the decision model.

Official entities are classified into the following categories:

---

### 5.1. Main entities

Correspond to the central elements of the automation's business domain.

These entities represent the main information on which the functional processes of the system are executed.

Every main entity must:

- Represent a concept specific to the project domain.
- Have a clearly defined lifecycle.
- Be able to relate to other entities through explicit rules.
- Maintain independence from its physical implementation.

---

### 5.2. Supporting entities

Correspond to entities used to complement, parameterize, or enrich the information of the main entities.

Their purpose is to avoid redundancy, promote information reuse, and facilitate the evolution of the model.

Supporting entities may be shared by multiple automation modules.

---

### 5.3. Operational entities

Correspond to entities used to represent the internal functioning of the automation.

They include the information necessary for:

- State management.
- Internal processing.
- Auditing.
- Error handling.
- Operational logs.
- Executions.
- Events.
- Configuration.
- Traceability.

These entities do not represent business concepts, but rather aspects of the system's own operation.

---

### 5.4. Official entity inventory

The official entity inventory of the project must be derived exclusively from previously approved official documentation.

Each entity incorporated into the data model must meet, at a minimum, the following conditions:

- Have a clearly identified functional need.
- Be supported by one or more functional requirements.
- Be compatible with the official data flow.
- Maintain coherence with the decision model.
- Respect the general system architecture.
- Not duplicate responsibilities of another existing entity.
- Be integrable with the rest of the data model without generating inconsistencies.

Entities that are not properly justified from a functional or architectural standpoint may not be incorporated.

---

### 5.5. Entity inventory evolution

Any incorporation, modification, unification, or deletion of entities must be documented and formally justified before becoming part of the official data model.

Modifications must preserve compatibility with existing information, historical traceability, and coherence with the rest of the official project documentation.

---

## 6. Relationships between entities

Relationships between entities define how the different elements of the data model interact with each other to coherently represent the functional domain of the automation.

Every relationship must respond to a clearly identified functional need, respect the general system architecture, and maintain the integrity of the data model.

The relationships defined in this document constitute the normative framework that must be respected during the construction of the logical model and the physical implementation of the database.

---

### 6.1. General principles of relationships

Every relationship between entities must comply with the following principles:

- Respond to a functional requirement of the project.
- Maintain referential integrity.
- Avoid unnecessary redundancies.
- Minimize coupling between domains.
- Facilitate information traceability.
- Maintain coherence with the official data flow.
- Respect the modular architecture of the system.
- Allow controlled evolution of the data model.

---

### 6.2. Intra-domain relationships

Entities belonging to the same functional domain may establish relationships when such relationships are necessary to correctly represent the behavior of that domain.

These relationships must maintain high cohesion and avoid unnecessary dependencies with other domains.

---

### 6.3. Inter-domain relationships

Relationships between entities belonging to different domains may only be established when there is a clearly documented functional need.

These relationships must be designed seeking the lowest possible level of coupling between domains.

---

### 6.4. Relationship cardinality

Every relationship must explicitly define its cardinality during the construction of the logical data model.

At a minimum, the following types of relationship must be identified where applicable:

- One-to-one (1:1).
- One-to-many (1:N).
- Many-to-many (N:M).

The selection of cardinality must be justified according to the functional needs of the project.

---

### 6.5. Referential integrity

Relationships must permanently preserve the referential integrity of the information.

Relationships that generate orphaned records, inconsistencies, or invalid dependencies between entities are not permitted.

Specific update and deletion rules will be defined during the logical model design and physical implementation.

---

### 6.6. Dependencies between entities

Dependencies between entities must be kept to the minimum necessary to correctly represent the project domain.

Every dependency must be properly justified and documented.

---

### 6.7. Prevention of unnecessary relationships

Relationships that do any of the following are not permitted:

- Duplicate information already represented by other relationships.
- Introduce unjustified circular dependencies.
- Unnecessarily increase the complexity of the model.
- Contradict the general system architecture or the official data flow.

---

### 6.8. Compatibility with the data flow

Relationships between entities must facilitate the exchange of information between the different modules of the automation according to the official processing flow.

The relational structure must not hinder the execution of any process stage.

---

### 6.9. Evolution of relationships

Any incorporation, modification, or deletion of relationships must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve compatibility with existing information, model integrity, and coherence with the rest of the official project documentation.

---

## 7. Entity attributes

Entity attributes represent the properties that describe the information stored by each element of the data model.

Every attribute must provide a clear functional meaning, maintain coherence with the domain it represents, and comply with the principles established for the data model.

The detailed definition of individual attributes will be carried out in the Official Data Dictionary. This chapter only establishes the general rules that all model attributes must comply with.

---

### 7.1. General principles of attributes

Every attribute must comply with the following principles:

- Represent a single property of the domain.
- Have a clear and unambiguous meaning.
- Be supported by a functional need.
- Maintain coherence with the entity to which it belongs.
- Comply with the official project naming standards.
- Be validable according to objective rules.
- Avoid unnecessary redundancies.
- Maintain independence from physical implementation.

---

### 7.2. Attribute classification

Data model attributes are officially classified into the following categories:

#### Identification attributes

Allow the unique identification of an instance of an entity.

These attributes constitute the basis for the logical identification of records within the model.

---

#### Business attributes

Represent the information specific to the functional domain of the entity.

They describe the main characteristics of the modeled concept and constitute most of the information used by the automation.

---

#### Relationship attributes

Allow establishing links between entities and representing the associations defined by the data model.

Their use must preserve referential integrity and minimize coupling between entities.

---

#### Control attributes

Represent information used to manage the lifecycle of records.

They include, among others, states, version indicators, operational dates, and other elements necessary to control the behavior of the information.

---

#### Audit attributes

Allow recording the information necessary to guarantee traceability and historical tracking of records.

Their use must facilitate diagnosis, auditing, and analysis of information evolution.

---

### 7.3. Attribute typing

Every attribute must define a data type compatible with the nature of the information it represents.

The selection of the data type must prioritize:

- Precision.
- Consistency.
- Efficiency.
- Ease of validation.
- Compatibility with the logical model.

Specific data types will be defined during the logical model design and documented in the Official Data Dictionary.

---

### 7.4. Attribute mandatory status

Each attribute must be classified as mandatory or optional according to the functional requirements of the project.

Mandatory status must be functionally justified and remain consistent throughout the evolution of the model.

---

### 7.5. Attribute validation

Every attribute must have validation rules that guarantee the quality and integrity of the information.

Validation rules may include, where applicable:

- Length.
- Format.
- Value domain.
- Allowed ranges.
- Uniqueness.
- Mandatory status.
- Consistency with other attributes.

Specific rules will be documented in the Official Data Dictionary.

---

### 7.6. Derived attributes

Information that can be obtained deterministically from other attributes shall not be stored, unless there is a duly documented technical or functional justification.

When a derived attribute is persisted, mechanisms must be established that permanently guarantee its consistency with the source information.

---

### 7.7. Attribute evolution

Any incorporation, modification, or deletion of attributes must be documented, justified, and formally approved before becoming part of the official data model.

Modifications must preserve compatibility with existing information, model integrity, and coherence with the rest of the official project documentation.

---

## 8. Data integrity rules

Data integrity rules establish the official criteria that must guarantee the consistency, validity, reliability, and coherence of all information managed by the automation.

These rules shall be mandatory during data model design, database implementation, validation processes, information exchange between modules, and any operation involving creation, modification, deletion, or querying of data.

---

### 8.1. Entity integrity

Every entity must have a mechanism that allows the unique identification of each of its records.

The existence of ambiguous records or records that cannot be unequivocally identified within the data model is not permitted.

---

### 8.2. Referential integrity

Every relationship between entities must preserve the coherence between related records.

References to non-existent entities or relationships that generate orphaned or inconsistent records are not allowed.

Specific update and deletion rules will be defined during the logical model design.

---

### 8.3. Domain integrity

Each attribute may only admit values compatible with its nature, meaning, and functional purpose.

Valid domains must be defined through clearly documented validation rules.

---

### 8.4. Functional integrity

All stored information must comply with the functional rules established in the project requirements, the decision model, and the official processing flow.

Information that contradicts the expected behavior of the automation shall not be stored.

---

### 8.5. Temporal integrity

The evolution of information must respect the logical and chronological order defined for the lifecycle of each job offer and associated processes.

Transitions, states, or temporal sequences incompatible with the official automation flow may not occur.

---

### 8.6. Audit integrity

Every relevant operation that modifies information must be reconstructable through the official audit and traceability mechanisms of the project.

The deletion or modification of information must not compromise the reconstruction of the history when it must be preserved.

---

### 8.7. Operational integrity

The automation must prevent execution errors, processing interruptions, or recoverable failures from generating inconsistent states within the data model.

Recovery mechanisms must preserve information coherence throughout the entire processing cycle.

---

### 8.8. Semantic integrity

Information generated by automatic processes or through artificial intelligence must be validated before being incorporated into the data model where applicable.

Validation must guarantee that such information is coherent with the functional context, project rules, and the rest of the previously stored information.

The incorporation of automatically generated information must not compromise the consistency or reliability of the data model.

---

### 8.9. Integrity validation

Validation mechanisms must be executed before, during, or after data operations, as appropriate to the nature of each integrity rule.

Any violation of an integrity rule must be managed according to the Error Handling Model approved for the project.

---

### 8.10. Evolution of integrity rules

Any incorporation, modification, or deletion of integrity rules must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve compatibility with existing information, model coherence, and compliance with all official project documentation.

---

## 9. Catalogs and reference tables

Catalogs and reference tables constitute the official mechanism for centralizing reusable information used by the job search automation.

Their purpose is to guarantee data consistency, reduce information duplication, and facilitate the administration of values shared by the different system modules.

The incorporation of a catalog must always respond to a clearly identified functional need and respect the data model principles defined in this document.

---

### 9.1. Purpose of catalogs

Catalogs must provide a single source of information for those sets of values used recurrently within the automation.

Their use must promote:

- Information normalization.
- Data reuse.
- Consistency between modules.
- Simplified maintenance.
- Controlled evolution of the data model.

---

### 9.2. Criteria for catalog creation

A set of values may only be modeled as a catalog when it meets one or more of the following criteria:

- Is reused by multiple entities.
- Is used by different automation modules.
- Requires centralized administration.
- Can be modified without altering system logic.
- Represents a stable concept of the project domain.
- Is necessary for validation or normalization processes.
- Contributes to reducing information redundancy.

The creation of catalogs that do not provide a functional or architectural benefit should be avoided.

---

### 9.3. Catalog classification

Official project catalogs may be classified into the following categories:

#### Functional catalogs

Represent concepts specific to the business domain used during job offer processing.

---

#### Geographic catalogs

Represent information related to geographic locations used by the automation.

---

#### Technical catalogs

Represent information used for the internal functioning of the system, including states, types, classifications, and other technical elements.

---

#### Configuration catalogs

Represent values used to parameterize the behavior of the automation without requiring modifications to system logic.

---

### 9.4. Catalog reuse

Any entity that requires information represented by an official catalog must reuse that catalog instead of storing the same information again.

Duplicate catalogs representing the same functional concept are not permitted.

---

### 9.5. Catalog integrity

The values contained in catalogs must remain consistent, complete, and compatible with the rest of the data model.

Any modification to a catalog must preserve the referential integrity of the entities that depend on it.

---

### 9.6. Catalog administration

The incorporation, modification, deactivation, or deletion of values belonging to a catalog must be carried out through controlled procedures that guarantee the consistency of the data model.

Specific rules for the administration of each catalog will be defined during the logical model design and documented in the Official Data Dictionary.

---

### 9.7. Alternatives to catalogs

When a set of values does not meet the established criteria to become an official catalog, it may be represented through other implementation mechanisms, provided that such decision is technically justified and does not compromise the maintainability, consistency, or evolution of the data model.

The selection of the most appropriate mechanism must be made during the logical model design and kept documented according to the project architecture.

---

### 9.8. Catalog evolution

Any incorporation, modification, or deletion of an official catalog must be documented, justified, and formally approved before being incorporated into the data model.

Modifications must preserve compatibility with existing information, model integrity, and coherence with the rest of the official project documentation.

---

## 10. System states

System states represent the functional or operational situation of the entities that make up the data model during their lifecycle within the automation.

Their purpose is to control the evolution of information, guarantee processing consistency, and allow complete tracking of each entity from its creation until the end of its participation in the system.

Every entity whose behavior evolves through different stages must manage its lifecycle through clearly defined states.

---

### 10.1. General principles of states

System states must comply with the following principles:

- Represent real situations of the domain or of the internal functioning of the system.
- Maintain coherence with the official data flow.
- Respect the project's Decision Model.
- Facilitate processing traceability.
- Allow auditing of transitions.
- Promote controlled recovery from errors.
- Maintain independence from technological implementation.

---

### 10.2. State classification

Official data model states may be classified into the following categories:

#### Business states

Represent the functional progress of entities within the job opportunity search and processing process.

---

#### Operational states

Represent the execution status of internal automation processes.

---

#### Control states

Represent administrative, technical, or temporal conditions necessary to control the behavior of the system.

---

### 10.3. State machine-based model

Every entity that has a lifecycle must be conceptually modeled as a state machine.

Each state machine must define, at a minimum:

- The initial state.
- The allowed states.
- The valid transitions.
- The conditions necessary for each transition.
- The final states, where applicable.

Transitions that have not been defined as valid for the corresponding entity are not permitted.

---

### 10.4. State transitions

Every transition must respond to a clearly identified functional or operational event.

Transitions must:

- Maintain coherence with the official processing flow.
- Respect the rules of the Decision Model.
- Preserve the integrity of the information.
- Prevent sequences incompatible with the entity's lifecycle.

---

### 10.5. Transition recording

Every relevant transition between states must be recorded through the official traceability and audit mechanisms defined for the project.

The record must allow the reconstruction of the complete evolution history of the entity when necessary.

---

### 10.6. State validation

Before performing a transition, the system must verify that:

- The entity is in a valid state.
- The requested transition is allowed.
- The necessary functional conditions are met.
- The integrity of the data model is not compromised.

Specific validations will be defined during the logical model design and system implementation.

---

### 10.7. Recovery from inconsistent states

When an automation process detects an invalid transition or an inconsistent state, it must apply the strategies defined in the Error Handling Model.

Recovery must not compromise the integrity, traceability, or consistency of the stored information.

---

### 10.8. State model evolution

Any incorporation, modification, or deletion of states or transitions must be documented, justified, and formally approved before becoming part of the official data model.

Modifications must preserve compatibility with existing information, entity history, and coherence with the rest of the official project documentation.

---

## 11. Identifiers and keys

Identifiers and keys constitute the official mechanisms for guaranteeing the unique identification of entities and the correct representation of relationships within the data model.

Their purpose is to preserve referential integrity, facilitate information traceability, and maintain model stability throughout the evolution of the automation.

Every entity in the data model must have identification mechanisms defined according to the principles established in this chapter.

---

### 11.1. General principles

Identifiers and keys must comply with the following principles:

- Guarantee the unique identification of each record.
- Maintain stability throughout the entire lifecycle of the entity.
- Preserve the referential integrity of the data model.
- Maintain independence from changes in business information.
- Facilitate the evolution and maintainability of the system.
- Avoid ambiguities in relationships between entities.

---

### 11.2. Technical identifiers

Every persistent entity must have a stable technical identifier that represents its identity within the system.

Technical identifiers must:

- Be unique.
- Remain immutable throughout the entire existence of the record.
- Not depend on information subject to modification.
- Not be reused once assigned.
- Be used as the primary identification mechanism within the data model.

The specific strategy for generating these identifiers will be defined during the logical model design.

---

### 11.3. Primary keys

Every entity must have a primary key that allows the unequivocal identification of each of its records.

The primary key must be built using the official technical identifier of the entity, unless there is a documented architectural justification to adopt a different strategy.

---

### 11.4. Alternate keys

When an entity has one or more identifiers specific to the functional domain, these may be defined as alternate keys.

Alternate keys must:

- Maintain uniqueness where applicable.
- Not replace the primary key.
- Be modifiable when the nature of the business so requires.
- Maintain consistency with the functional rules of the project.

---

### 11.5. Foreign keys

Relationships between entities must be implemented using foreign keys that preserve the referential integrity of the data model.

Every foreign key must:

- Reference an existing entity.
- Maintain coherence with the relationships defined in the logical model.
- Comply with the update and deletion rules established for each relationship.

---

### 11.6. Uniqueness constraints

When the functional nature of the information so requires, the data model must establish additional uniqueness constraints on one or more attributes.

These constraints will complement the technical identification of entities and guarantee the consistency of business information.

---

### 11.7. Identifier reuse

Technical identifiers belonging to previously existing records shall not be reused, even when such records have been deleted, archived, or deactivated.

This principle guarantees the preservation of historical traceability and avoids ambiguities during system evolution.

---

### 11.8. Evolution of identifiers and keys

Any modification related to identification mechanisms or data model keys must be documented, justified, and formally approved before being incorporated into the official model.

Modifications must preserve referential integrity, compatibility with existing information, and coherence with the rest of the official project documentation.

---

## 12. Logical data model

The logical data model constitutes the official representation of the logical structure of the information managed by the job search automation.

Its purpose is to consolidate the organization of entities, their relationships, identification mechanisms, and structural rules, providing a representation independent of any specific storage technology.

The logical model will serve as a direct reference for the implementation of the physical data model and must maintain coherence with all official project documentation.

---

### 12.1. Purpose of the logical model

The logical model must represent completely, consistently, and structurally all the components that make up the automation's data model.

Its design must guarantee:

- Structural coherence.
- Information integrity.
- Technology independence.
- Scalability.
- Traceability.
- Compatibility with the general system architecture.

---

### 12.2. Scope of the logical model

The logical model must integrate, at a minimum:

- The official system entities.
- The relationships between entities.
- The cardinalities.
- The identification mechanisms.
- The primary keys.
- The alternate keys.
- The foreign keys.
- The related catalogs.
- The applicable state machines.
- The logical constraints necessary to preserve the integrity of the model.

The complete detail of individual attributes will remain documented exclusively in the Official Data Dictionary.

---

### 12.3. Uniform entity structure

Every entity incorporated into the logical model must be documented using a uniform structure that facilitates its understanding, maintenance, and evolution.

At a minimum, each entity must include:

- Official name.
- Functional domain.
- Entity type.
- Functional description.
- Main responsibility.
- Relevant relationships.
- Cardinalities.
- Technical identifier.
- Alternate keys, where they exist.
- Foreign keys, where applicable.
- Associated catalogs.
- State machine, where applicable.
- Relevant architectural observations.

---

### 12.4. Structural coherence

Every entity and relationship incorporated into the logical model must maintain coherence with:

- The functional and non-functional requirements.
- The official data flow.
- The Decision Model.
- The General System Architecture.
- The data model principles.
- The integrity rules.
- The official identification mechanisms.

Elements that contradict the approved project architecture may not be incorporated.

---

### 12.5. Independence from the physical model

The logical model must remain independent of any database engine, persistence technology, or specific implementation decision.

Decisions related to physical data types, indexes, storage optimizations, or database management system-specific configurations will be part of the physical model and not the logical model.

---

### 12.6. Logical model validation

Before approving the logical model, it must be verified that:

- All official entities are represented.
- All relationships are consistent.
- Cardinalities are correctly defined.
- The identification mechanisms are coherent.
- The integrity rules can be correctly applied.
- The model fully supports the functional flow of the automation.

---

### 12.7. Logical model evolution

Any modification to the logical model must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve compatibility with existing information, the general system architecture, and the rest of the official project documentation.


---

## 13. Persistence and storage

Persistence and storage define the official principles for the conservation, administration, and availability of information used by the job search automation.

Their purpose is to guarantee that all information managed by the system maintains its integrity, consistency, traceability, and availability for as long as necessary, regardless of the technology used for its storage.

Decisions related to the physical implementation of persistence must respect the principles established in this chapter and remain aligned with the Technology Stack approved for the project.

---

### 13.1. General principles of persistence

All information persisted by the automation must comply with the following principles:

- Maintain integrity and consistency throughout its entire lifecycle.
- Preserve information traceability where applicable.
- Avoid unnecessary redundancies.
- Promote recovery from errors.
- Maintain independence from the physical storage mechanism.
- Guarantee compatibility with the official data model.
- Facilitate the future evolution of the system.

---

### 13.2. Information classification according to persistence

Information managed by the system shall be officially classified according to its lifecycle.

#### Permanent information

Corresponds to information that constitutes the main knowledge of the system and whose preservation is necessary throughout the entire useful life of the project.

Its deletion may only be carried out through formally authorized procedures.

---

#### Historical information

Corresponds to information used to preserve traceability, auditing, and reconstruction of the history of processes executed by the automation.

Its preservation must guarantee the possibility of performing historical analysis when necessary.

---

#### Temporary information

Corresponds to information used only during certain processing stages and whose permanence is no longer necessary once its function is completed.

Its lifecycle must be managed through controlled cleanup and deletion policies.

---

#### Configuration information

Corresponds to information used to control the behavior of the automation.

Its persistence must guarantee the reproducibility of executions and the operational stability of the system.

---

### 13.3. Information retention

Any retention policy must be established considering:

- The functional nature of the information.
- The audit and traceability requirements.
- The operational needs of the system.
- The project maintenance criteria.

Information whose preservation is necessary to guarantee the integrity or traceability of the system should not be deleted.

---

### 13.4. Information deletion

The deletion of information must be carried out only through controlled procedures that preserve the consistency of the data model.

Every deletion must respect:

- The referential integrity rules.
- The existing dependencies between entities.
- The audit needs.
- The official retention policies.

---

### 13.5. Information availability

Persistence must guarantee that information remains available for authorized automation processes when needed.

Specific access mechanisms will be defined during the physical implementation of the system.

---

### 13.6. Technology independence

The persistence rules established in this document must remain independent of the database engine, storage mechanism, or any specific technology used during implementation.

Corresponding technology decisions will be governed by the official Technology Stack of the project.

---

### 13.7. Evolution of the persistence strategy

Any modification related to persistence or storage of information must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve the integrity, compatibility, and coherence with the rest of the official project documentation.

---

### 13.8. Discovery module (module 1) — 2026-08-07

The Opportunity Discovery module defines the following persistence decisions:

- **D1 — `active` of the Source entity:** catalog attribute for external (manual) administration; the module's runtime does not filter sources by it.
- **D2 — single store:** all logical stores of the module — offers (`ofertas`), events (`eventos`), sessions (`sesiones`), runs (`corridas`), and lock (`bloqueo`) — persist as tables of the same single SQLite database (`job_search.db`), in accordance with section 13.6 (technology independence) and the Technology Stack decision that set SQLite as the MVP single store.
- **D3 — session audit (minimal viable):** the session audit table registers successful sessions only and contains the essential fields: `session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`. Failed attempts are reported as events, never as sessions. Credentials, tokens, and cookies are never stored (per the technical sheet).

---

## 14. Versioning and evolution of the data model

The data model constitutes a strategic component of the automation architecture and must evolve in a controlled manner throughout the entire lifecycle of the project.

Every modification must preserve the integrity of the model, guarantee compatibility with existing information, and maintain coherence with the official project documentation.

The evolution process of the data model must be fully documented, justified, and traceable.

---

### 14.1. General principles of evolution

Every evolution of the data model must comply with the following principles:

- Maintain the structural integrity of the model.
- Preserve the consistency of existing information.
- Minimize the impact on system modules.
- Maintain compatibility with the general architecture.
- Promote project scalability.
- Guarantee traceability of all modifications.
- Allow recovery of previous versions when necessary.

---

### 14.2. Data model versioning

The data model must maintain a formal versioning scheme that allows clearly identifying each of its official revisions.

Each version must be associated, at a minimum, with:

- A version identifier.
- The approval date.
- The description of the changes made.
- The corresponding functional or architectural justification.
- The impact analysis performed.
- The formal approval of the change.

---

### 14.3. Change classification

Modifications made to the data model may be officially classified as:

#### Evolutionary changes

Incorporate new capabilities or expand the existing model without altering its general purpose.

---

#### Corrective changes

Correct errors, inconsistencies, or improvements identified during the evolution of the project.

---

#### Structural changes

Modify the general organization of the data model and require an exhaustive impact analysis before their incorporation.

---

### 14.4. Change compatibility

Every modification must also be classified according to its impact on the existing model.

#### Compatible changes

Are those that preserve compatibility with existing information and do not require significant modifications in the components that use the data model.

As a general criterion, this type of change may include:

- Incorporation of new independent entities.
- Addition of optional attributes.
- Incorporation of new catalogs.
- Compatible extensions with the existing architecture.

---

#### Incompatible changes

Are those that may affect the structure of the model, the stored information, or the operation of the automation modules.

As a general criterion, this type of change may include:

- Deletion of entities.
- Modification of identification mechanisms.
- Changes in cardinalities.
- Deletion of attributes used by other components.
- Alterations that compromise compatibility with previous versions.

Every incompatible change must be supported by a specific impact analysis before its approval.

---

### 14.5. Change history management

The evolution history of the data model must remain available throughout the entire useful life of the project.

Each modification must record:

- The affected version.
- The modified elements.
- The nature of the change.
- The corresponding justification.
- The related architectural decisions.

---

### 14.6. Impact assessment

Before approving any modification to the data model, an impact assessment must be carried out that considers, at a minimum:

- The compatibility with existing information.
- The integrity of the model.
- The general system architecture.
- The official data flow.
- The Decision Model.
- The persistence mechanisms.
- The audit and traceability processes.

---

### 14.7. Change approval

Every modification to the data model must be documented, justified, and formally approved before being incorporated into a new official version.

Changes whose functional or architectural need has not been duly demonstrated may not be incorporated.

---

### 14.8. Controlled evolution

The evolution of the data model must be carried out in a planned manner, guaranteeing at all times the stability of the system, the maintainability of the project, and the coherence with the rest of the official documentation.

Every new version must preserve the architectural principles established in this document.


---

## 15. Traceability and auditing

Traceability and auditing constitute the official mechanisms for guaranteeing complete tracking of the information managed by the automation and the operations performed throughout its entire lifecycle.

Their purpose is to allow process reconstruction, facilitate incident diagnosis, support the decision model, and preserve the reliability of stored information.

The entire data model architecture must be designed so that relevant information can be traced, audited, and analyzed when necessary.

---

### 15.1. General principles of traceability and auditing

Traceability and auditing must comply with the following principles:

- Preserve the historical integrity of information.
- Allow the reconstruction of relevant processes.
- Maintain coherence with the official data flow.
- Promote incident diagnosis.
- Support the Decision Model.
- Facilitate the evolution and maintenance of the system.
- Maintain independence from technological implementation.

---

### 15.2. Scope of traceability

Traceability must cover, at a minimum:

- The lifecycle of main entities.
- The transitions between states.
- The relevant operations performed on the information.
- The functional decisions that affect processing.
- The operational events necessary to understand the evolution of the system.

The recorded information must be sufficient to reconstruct the processes when necessary.

---

### 15.3. Audit classification

The official project audit may be classified into the following categories.

#### Functional audit

Records events related to the functional behavior of the automation and the processing of job offers.

---

#### Technical audit

Records events related to the internal operation of the system, process execution, and the functioning of technical components.

---

#### Change audit

Records modifications made to persistent information and to relevant elements of the data model.

---

### 15.4. Traceability of decision context

Every relevant decision generated during automation must be contextualizable when necessary.

The traceability information must allow identifying, at a minimum:

- The process that originated the decision.
- The moment when it was made.
- The information used as input.
- The result obtained.
- The component responsible for execution.
- The version of the applicable rules, configurations, or models where applicable.

The level of detail recorded must be sufficient to explain the functional context of the decision without compromising the efficiency or maintainability of the system.

---

### 15.5. Audit integrity

Audit records must remain protected against unauthorized modifications that compromise the reliability of historical information.

Any alteration to audit information must be duly documented and authorized.

---

### 15.6. Audit information retention

Audit information must be preserved according to the official persistence policies defined for the project.

Its deletion may only be carried out through controlled procedures that do not compromise the traceability of relevant processes.

---

### 15.7. Access to audit information

Access to audit information must be carried out only for functional, operational, diagnostic, maintenance, or analysis purposes authorized by the system architecture.

The organization of the information must facilitate its consultation without affecting the integrity of the data model.

---

### 15.8. Evolution of traceability mechanisms

Any modification related to traceability or auditing must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve compatibility with existing information, historical integrity, and coherence with the rest of the official project documentation.

---

## 16. Data security and protection

Data security and protection establish the official principles for preserving the confidentiality, integrity, availability, and proper use of information managed by the job search automation.

Their purpose is to guarantee that information is managed securely throughout its entire lifecycle, maintaining coherence with the general system architecture, the data model, and the principles established for the project.

Decisions related to specific technological protection mechanisms must be governed by the Technology Stack and by the system implementation, without altering the principles defined in this document.

---

### 16.1. General security principles

Information management must comply, at a minimum, with the following principles:

- Preserve the confidentiality of information.
- Guarantee data integrity.
- Maintain information availability when necessary.
- Promote traceability of relevant operations.
- Protect information against unauthorized modifications.
- Maintain coherence with the Error Handling Model.
- Preserve the stability of the data model.

---

### 16.2. Information classification according to sensitivity

All information managed by the automation must be classified according to the level of protection it requires.

#### Public information

Corresponds to information whose disclosure does not represent a significant impact for the project or the user.

Its use does not require special protection measures other than those defined by the general architecture.

---

#### Internal use information

Corresponds to information used exclusively by the automation for the operation of its internal processes.

Its access must be limited to authorized components of the system architecture.

---

#### Sensitive information

Corresponds to information whose disclosure, modification, loss, or improper use could affect the user, the operation of the automation, or the integrity of the project.

This type of information must receive a level of protection commensurate with its criticality during system implementation.

---

### 16.3. Data integrity protection

Every operation on information must preserve the consistency of the data model and respect the official integrity rules defined for the project.

Mechanisms that compromise the reliability of stored information may not be incorporated.

---

### 16.4. Protection during the information lifecycle

Protection measures must cover all stages of the information lifecycle, including:

- Creation.
- Processing.
- Storage.
- Query.
- Modification.
- Archiving.
- Deletion.

The protection strategy must remain consistent throughout all these stages.

---

### 16.5. Access to information

Access to information must be limited exclusively to the processes, components, and mechanisms authorized by the system architecture.

The organization of the data model must facilitate the application of access controls during implementation, without depending on a specific technological mechanism.

---

### 16.6. Protection of historical information

Information used for auditing, traceability, and history must be protected in a way that permanently preserves its integrity and reliability.

Any modification to historical information must be duly justified, documented, and authorized.

---

### 16.7. Compatibility with the security architecture

The rules established in this chapter must remain compatible with:

- The General System Architecture.
- The official Technology Stack.
- The Error Handling Model.
- The official persistence policies.
- The audit and traceability mechanisms.

---

### 16.8. Evolution of protection policies

Any modification related to the security or protection of information must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve the integrity of the model, compatibility with existing information, and coherence with the rest of the official project documentation.

---

## 17. Data validation rules

Data validation rules establish the official principles that must guarantee that all information incorporated into the data model is consistent, complete, valid, and compatible with the automation architecture.

Their purpose is to prevent the incorporation of incorrect information, preserve the integrity of the data model, and ensure that all information used by the automation complies with the functional and architectural rules of the project.

Validations must be applied throughout the entire information lifecycle, regardless of the technological mechanism used for their implementation.

---

### 17.1. General validation principles

Every data validation must comply with the following principles:

- Verify information consistency before its incorporation into the data model.
- Maintain coherence with the integrity rules defined for the project.
- Be objective, reproducible, and verifiable.
- Maintain independence from the technology used for its implementation.
- Promote information quality.
- Reduce the incorporation of inconsistent data.
- Maintain compatibility with the Decision Model and the official processing flow.

---

### 17.2. Structural validations

Structural validations will verify that the information meets the basic requirements defined for each element of the data model.

They may include, among others:

- Mandatory status.
- Data type.
- Length.
- Format.
- Value domain.
- Uniqueness constraints.

Specific rules will be documented in the Official Data Dictionary.

---

### 17.3. Functional validations

Functional validations will verify that the information complies with the business rules established for the automation.

Their purpose will be to guarantee that the information correctly represents the expected behavior of the project's functional domain.

---

### 17.4. Relational validations

Relational validations will verify the existing coherence between related entities.

These validations must preserve referential integrity and guarantee the consistency of the relationships defined by the data model.

---

### 17.5. Temporal validations

Temporal validations will verify the chronological coherence of information throughout the entire lifecycle of entities.

Temporal sequences incompatible with the official processing flow may not be recorded.

---

### 17.6. Semantic validations

Semantic validations will verify, where applicable, that information generated automatically or through artificial intelligence is coherent with the functional context of the project before being incorporated into the data model.

These validations must guarantee that the information:

- Is consistent with the represented domain.
- Respects the functional rules of the project.
- Maintains coherence with previously stored information.
- Does not compromise the semantic integrity of the data model.

Semantic validations complement the semantic integrity rules defined for the project and must be applied when the nature of the information so requires.

---

### 17.7. Validation error management

Every failed validation must be managed according to the Error Handling Model approved for the project.

The incorporation of information into the data model must not continue when the non-compliance of a validation rule compromises the integrity, consistency, or reliability of the information.

---

### 17.8. Evolution of validation rules

Any incorporation, modification, or deletion of validation rules must be documented, justified, and formally approved before becoming part of the official data model.

Modifications must preserve compatibility with existing information, coherence with the rest of the architecture, and compliance with all official project documentation.

---

## 18. Migration strategy

The migration strategy establishes the official principles for managing the structural evolution of the data model throughout the entire lifecycle of the automation.

Its purpose is to guarantee that any modification made to the persistent structure of the system preserves the integrity of the information, maintains compatibility with the approved architecture, and allows a controlled evolution of the project.

Decisions related to specific migration tools must be governed by the official Technology Stack and are not part of this document.

---

### 18.1. General principles of migrations

Every data model migration must comply with the following principles:

- Maintain information integrity.
- Preserve data model consistency.
- Guarantee traceability of modifications.
- Maintain compatibility with the general system architecture.
- Be reproducible and verifiable.
- Promote controlled evolution of the project.
- Minimize the risk of information loss or corruption.

---

### 18.2. Scope of migrations

Migrations must be used to manage any structural modification that affects the persistent data model, including, where applicable:

- Incorporation of new entities.
- Modification of existing entities.
- Changes in relationships.
- Updating of constraints.
- Incorporation or modification of catalogs.
- Adjustments derived from the evolution of the data model.

---

### 18.3. Migration classification

Official migrations may be classified as:

#### Evolutionary migrations

Incorporate new capabilities to the data model while preserving compatibility with the existing structure.

---

#### Corrective migrations

Correct errors, inconsistencies, or deficiencies identified during the evolution of the project.

---

#### Structural migrations

Introduce significant modifications to the organization of the data model and require an impact analysis prior to execution.

---

### 18.4. Migration versioning

Every migration must be associated with an official version of the data model.

Each migration must record, at a minimum:

- Migration identifier.
- Data model version.
- Description of the modification.
- Functional or architectural justification.
- Date of incorporation.
- Execution result.

---

### 18.5. Pre-migration validation

Before executing a migration, it must be verified, at a minimum:

- The consistency of the data model.
- The compatibility with the previous version.
- The impact on existing information.
- The compliance with integrity rules.
- The compatibility with the general system architecture.

Every migration must have a documented impact analysis before its approval.

---

### 18.6. Migration reversibility

Whenever technically feasible, every migration must be designed in a way that allows reverting the changes made and restoring the previous state of the data model.

When a migration cannot be reversed due to technical limitations or the nature of the transformation performed, this condition must be documented in advance along with its justification.

In such cases, measures must be established that minimize the risk to the integrity and availability of the information.

---

### 18.7. Migration traceability

Every migration must be part of the official evolution history of the data model.

The corresponding documentation must allow reconstructing:

- The source version.
- The target version.
- The changes made.
- The justification for the modification.
- The identified impact.
- The evidence of approval.

---

### 18.8. Evolution of the migration strategy

Any modification related to the official migration strategy must be documented, justified, and formally approved before being incorporated into the official data model.

Modifications must preserve compatibility with the general architecture, the project evolution history, and the rest of the official documentation.

---

## 19. Acceptance criteria

The acceptance criteria establish the official conditions that the data model must meet to be considered complete, consistent, and conformant with the approved project architecture.

Their purpose is to provide a set of objective criteria that allow verifying the quality of the data model before its official approval or the incorporation of new versions.

Compliance with these criteria shall be mandatory for every official version of the data model.

---

### 19.1. Structural integrity

The data model must comply, at a minimum, with the following conditions:

- All official entities must be represented.
- All relationships must be properly defined and justified.
- The official identification mechanisms must be documented.
- The integrity rules must be correctly applicable.
- There must be no structural inconsistencies within the model.

---

### 19.2. Functional coherence

The data model must correctly represent the functional domain of the automation.

At a minimum, it must be verified that:

- The model fully supports the official processing flow.
- The entities correctly represent the domain concepts.
- The relationships reflect the functional needs of the project.
- The state machines are compatible with the lifecycle of the corresponding entities.

---

### 19.3. Data model quality

The model must demonstrate that:

- Information can be maintained consistently.
- Unnecessary redundancy is minimized.
- The organization of entities promotes maintainability.
- The architecture allows controlled evolution of the system.
- The model is scalable and extensible.

---

### 19.4. Compliance with model rules

Before approval, it must be verified that the model complies with:

- The data model principles.
- The model objectives.
- The integrity rules.
- The validation rules.
- The persistence policies.
- The security principles.
- The traceability and audit mechanisms.

---

### 19.5. Documentary coherence

The data model must remain fully aligned with the official project documentation.

At a minimum, compatibility must be verified with:

- The functional and non-functional requirements.
- The project strategic documentation.
- The official data flow.
- The Decision Model.
- The General System Architecture.
- The approved Technology Stack.
- The Error Handling Model.
- The rest of the official documents related to the project architecture.

There must be no contradictions between the data model and the current official documentation.

---

### 19.6. Documentation completeness

Before approving an official version of the data model, it must be verified that all associated documentation is complete.

At a minimum, the following must be available:

- The Logical Data Model.
- The Official Data Dictionary.
- The Official Data Model Diagram.
- The corresponding version history.
- The documentation of approved changes.

---

### 19.7. Model approval

The data model may only be considered officially approved when all the criteria defined in this chapter have been satisfactorily verified.

Any exception must be documented, justified, and formally approved before the release of a new official version.

---

### 19.8. Model revalidation

Any modification made to the data model must lead to a new evaluation of the acceptance criteria defined in this chapter.

A new version of the model may not be approved while any acceptance criterion remains unfulfilled.

---

## 20. Official Data Dictionary

The Official Data Dictionary constitutes the official technical specification of the data model of the job search automation.

Its purpose is to document in a complete, uniform, and traceable manner all the elements that make up the data model, providing a single official source of information for the design, implementation, maintenance, and evolution of the system.

Every entity, attribute, relationship, catalog, and component of the data model must be documented according to the structure established in this chapter.

---

### 20.1. Objectives of the Official Data Dictionary

The dictionary must:

- Centralize the technical documentation of the data model.
- Guarantee uniformity in the definition of model elements.
- Facilitate the implementation of the database.
- Promote system maintainability.
- Serve as an official reference for the development and evolution of the project.
- Maintain traceability with the rest of the official documentation.

---

### 20.2. Scope of the dictionary

The Official Data Dictionary must document, at a minimum:

- Entities.
- Attributes.
- Relationships.
- Primary keys.
- Alternate keys.
- Foreign keys.
- Catalogs.
- Constraints.
- Validation rules.
- State machines where applicable.
- Relevant architectural observations.

There must be no persistent element of the data model that is not documented in this dictionary.

---

### 20.3. Official template for entities

Every entity must be documented using a uniform structure.

At a minimum, it must include:

#### General information

- Official name.
- Functional domain.
- Entity type.
- Functional description.
- Main responsibility.

---

#### Identification

- Technical identifier.
- Primary key.
- Alternate keys.

---

#### Relationships

- Related entities.
- Cardinalities.
- Foreign keys.
- Relevant dependencies.

---

#### Lifecycle

- State machine, where applicable.
- Main states.
- Observations related to the lifecycle.

---

#### Associated catalogs

List of catalogs used by the entity.

---

#### Architectural observations

Information relevant to understanding the role of the entity within the data model.

---

### 20.4. Official template for attributes

Every attribute must be documented using a uniform structure.

At a minimum, it must include:

- Official name.
- Functional description.
- Logical type.
- Physical type, where applicable during implementation.
- Attribute category.
- Mandatory status.
- Default value, where applicable.
- Value domain.
- Constraints.
- Validation rules.
- Uniqueness constraints, where they exist.
- Sensitivity level.
- Classification according to persistence.
- Relevant observations.

---

### 20.5. Documentary traceability

The Official Data Dictionary must maintain traceability with the rest of the official project documentation.

Where applicable, each entity must indicate its relationship with:

- The associated functional requirements.
- The architectural domain to which it belongs.
- The official data flow.
- The Decision Model.
- The corresponding state machines.
- The catalogs used.
- The applicable integrity rules.
- The related validation rules.

Likewise, where pertinent, each attribute may document:

- The corresponding validation rule.
- The associated integrity rule.
- Its classification according to sensitivity.
- Its classification according to persistence.
- Relevant architectural observations.

---

### 20.6. Dictionary consistency

All information documented in the Official Data Dictionary must remain consistent with:

- The Logical Data Model.
- The Official Data Model Diagram.
- The data model principles.
- The general system architecture.
- The rest of the official project documentation.

Contradictions between the dictionary and other official artifacts are not permitted.

---

### 20.7. Dictionary maintenance

Any incorporation, modification, or deletion of information documented in the Official Data Dictionary must be carried out in a controlled manner.

Modifications must:

- Maintain documentary traceability.
- Preserve model consistency.
- Update related documentation where applicable.
- Keep the Logical Data Model and the Official Data Model Diagram synchronized.

---

### 20.8. Dictionary evolution

The Official Data Dictionary must evolve together with the data model.

Any modification must be documented, justified, and formally approved before being incorporated into a new official version of the project.

The dictionary constitutes the official source of reference for the detailed definition of data model elements and must remain permanently updated.


---

## 21. Official Data Model Diagram

The Official Data Model Diagram constitutes the official graphical representation of the logical structure of the information used by the job search automation.

Its purpose is to facilitate understanding of the general organization of the data model, visually showing entities, their relationships, and the general structure of the system, maintaining coherence with the Logical Data Model and the Official Data Dictionary.

The diagram must remain permanently synchronized with these artifacts and will not constitute the official source for the definition of the data model.

---

### 21.1. Purpose of the diagram

The Official Data Model Diagram must:

- Graphically represent the logical structure of the data model.
- Facilitate understanding of the relationships between entities.
- Promote architectural analysis of the system.
- Serve as support for the development and maintenance of the project.
- Maintain coherence with all official documentation.

---

### 21.2. Scope of the diagram

The diagram must represent, at a minimum:

- The official entities of the data model.
- The existing relationships between entities.
- The corresponding cardinalities.
- The functional domains when convenient for understanding the model.
- The classification of entities according to the project architecture.
- The official catalogs when they form part of the logical model.
- The relevant structural dependencies.

The inclusion of additional information must be justified by its usefulness for understanding the model architecture.

---

### 21.3. Graphical representation

The graphical representation must facilitate understanding of the data model avoiding unnecessary complexity.

The diagram must:

- Maintain a clear and uniform organization.
- Minimize unnecessary crosses between relationships.
- Promote readability.
- Maintain consistency in the symbology used.
- Facilitate its evolution as the data model grows.

The specific graphical notation will be defined during the implementation phase and must remain uniform across all versions of the diagram.

---

### 21.4. Relationship with the Logical Data Model

The Official Data Model Diagram must be derived directly from the Logical Data Model.

Any structural modification made to the logical model must subsequently be reflected in the official diagram.

The diagram may not contain elements that do not exist in the Logical Data Model.

---

### 21.5. Relationship with the Official Data Dictionary

Every entity represented in the diagram must be documented in the Official Data Dictionary.

Relationships, identification mechanisms, and other graphically represented elements must maintain coherence with the corresponding technical documentation.

The diagram constitutes a visual representation of the model and does not replace the detailed specification contained in the dictionary.

---

### 21.6. Diagram versioning

The Official Data Model Diagram must be versioned consistently with the official versions of the data model.

Each version must be associated with the corresponding Logical Data Model and the Official Data Dictionary.

Any modification must be documented within the official model evolution history.

---

### 21.7. Diagram maintenance

Any modification incorporated into the data model must be reflected promptly in the Official Data Model Diagram.

Synchronization between the diagram, the logical model, and the dictionary must be permanently preserved.

Inconsistent versions between these artifacts are not permitted.

---

### 21.8. Nature of the diagram

The Official Data Model Diagram constitutes a graphical support artifact for understanding the system architecture.

The official source for the definition of the data model shall be comprised of:

- The Logical Data Model.
- The Official Data Dictionary.

In case of discrepancy between the diagram and these artifacts, the information documented in the Logical Data Model and the Official Data Dictionary shall always prevail.

The diagram must be considered a visual representation derived from these documents and remain permanently updated with respect to them.
