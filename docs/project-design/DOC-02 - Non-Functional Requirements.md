# Document 2

# Non-Functional Requirements

## 1. Purpose of the Document

This document defines the non-functional requirements of the job search automation.

Its purpose is to establish the quality characteristics, constraints, and technical criteria that all system components must satisfy throughout their design, implementation, operation, and evolution.

Unlike the functional requirements, which describe **what** the automation does, the non-functional requirements define **how** it must do it, ensuring attributes such as performance, reliability, maintainability, scalability, security, and portability.

The requirements defined in this document are mandatory for all project modules and components and shall serve as a reference for architectural decisions, tool selection, implementation, and system validation.

---

## 2. System Quality Principles

The following principles establish the quality attributes that all automation components must satisfy throughout their design, development, implementation, operation, and maintenance.

These principles complement the functional requirements and shall serve as criteria for evaluating any architectural decision, implementation, or incorporation of new functionality.

---

### QP-001. Reliability

The automation shall execute its processes consistently and predictably, producing reproducible results under the same input conditions.

Failures shall be detected, recorded, and handled using the recovery mechanisms defined by the system.

---

### QP-002. Scalability

The architecture shall allow the incorporation of new job sources, modules, business rules, and functionalities with minimal impact on existing components.

Expanding the system shall not require significant architectural redesign.

---

### QP-003. Modularity

Each component shall have a clearly defined responsibility and maintain the lowest possible level of dependency on other components.

Modifying or replacing a module shall not affect the operation of the remaining modules, except through previously defined interfaces.

---

### QP-004. Maintainability

The automation shall be designed to facilitate bug fixes, enhancements, and component updates while minimizing maintenance effort.

Any modification shall be performed without compromising the overall stability of the system.

---

### QP-005. Traceability

Every action, decision, status change, processing activity, and generated piece of information shall be reconstructable through verifiable records.

Traceability shall be maintained throughout the entire lifecycle of every job posting.

---

### QP-006. Consistency

Data generated, stored, and processed shall remain consistent across all system modules.

Conflicting states, records, or results shall not exist.

---

### QP-007. Availability

The automation shall be ready to execute whenever requested by the user or according to the defined schedule, provided that external dependencies are available.

Temporary interruptions shall be handled through predefined recovery strategies.

---

### QP-008. Efficiency

Computational resources shall be used efficiently, avoiding unnecessary processing, redundant queries, and excessive consumption of memory, storage, or execution time.

---

### QP-009. Security

The information used by the automation shall be protected against unauthorized access, modification, or disclosure.

Credentials, sensitive configurations, and personal data shall be stored using appropriate protection mechanisms.

---

### QP-010. Portability

The automation shall be designed so that it can be moved across different execution environments with the minimum possible number of changes.

Platform-specific dependencies shall remain isolated whenever technically feasible.

---

### QP-011. Extensibility

The system shall allow new capabilities to be incorporated without altering the expected behavior of existing functionality.

All extensions shall comply with the interfaces, standards, and rules defined by the project.

---

### QP-012. Auditability

Every automated decision shall be justifiable through objective evidence recorded by the system.

Records shall be sufficient to determine what happened, when it happened, why it happened, and what result was obtained.

---

### QP-013. Simplicity

Implemented solutions shall favor simplicity over unnecessary complexity.

Whenever multiple technically viable alternatives exist, priority shall be given to the one that improves system understanding, maintenance, and evolution.

---

### QP-014. Use of Free Technologies

The selection of tools, services, and components shall prioritize free alternatives that satisfy the project's functional and non-functional requirements.

Paid technologies or services shall only be considered when there is documented technical justification and their adoption has been explicitly approved by the user.

---

### QP-015. Continuous Documentation

Every significant decision related to architecture, business rules, operation, implementation, or system evolution shall be documented before being incorporated into the project.

No critical component shall depend solely on implicit or undocumented knowledge.

---

## 3. Performance

The following requirements establish the expected behavior of the automation in terms of efficiency, response times, and resource utilization during operation.

The objective is to ensure that the system processes job postings in a timely, consistent, and efficient manner without compromising the stability of the remaining components.

---

### NFR-001. Overall Performance

The automation shall execute each process using only the resources required to complete its tasks, avoiding redundant or unnecessary operations.

---

### NFR-002. Module Response Time

Each module shall complete its processing within a reasonable time for the volume of information received.

Specific maximum response times shall be defined in the corresponding technical documents once the implementation of each module is known.

---

### NFR-003. Incremental Processing

The automation shall process only new job postings or those requiring reprocessing, avoiding repeated execution on information that is already current and validated.

---

### NFR-004. Query Optimization

Queries to job sources, databases, and other external dependencies shall minimize repeated and unnecessary requests.

Whenever possible, previously retrieved information shall be reused.

---

### NFR-005. Processing Optimization

Modules shall execute only the tasks required for the current state of each job posting.

Processes that do not provide additional value to the functional workflow shall not be executed.

---

### NFR-006. Efficient Resource Usage

The automation shall optimize memory, storage, processing, and bandwidth consumption throughout its execution.

---

### NFR-007. Independent Execution

The execution of one module shall not significantly degrade the performance of other modules.

Each component shall manage its own resources in a controlled manner.

---

### NFR-008. Performance Scalability

As the number of processed job postings increases, execution times shall grow in a controlled manner, avoiding disproportionate performance degradation.

---

### NFR-009. Performance Monitoring

The automation shall record metrics including, at a minimum:

- Execution time per module.
- Total execution time.
- Number of processed job postings.
- Number of discarded job postings.
- Number of errors.
- Number of retries.
- Approximate resource consumption, whenever possible.

These metrics shall be used to identify optimization opportunities and verify compliance with performance requirements.

---

### NFR-010. Controlled Degradation

When an external dependency becomes slow or partially unavailable, the automation shall degrade its performance in a controlled manner, prioritizing processing continuity over complete system interruption whenever permitted by the business rules.

---

## 4. Scalability

The following requirements establish the automation's ability to grow in a controlled manner, allowing the incorporation of new functionality, job sources, business rules, and components without compromising system stability, performance, or maintainability.

Scalability shall be treated as a cross-cutting principle throughout the entire project lifecycle.

---

### NFR-011. Modular Scalability

The automation shall consist of independent modules with clearly defined responsibilities, allowing components to be added, replaced, or extended without affecting the operation of the rest of the system.

---

### NFR-012. Addition of New Job Sources

The system shall allow new job sources to be added without requiring significant modifications to the processing, evaluation, management, or resource-generation modules.

Each new source shall be integrated through standardized mechanisms defined by the project architecture.

---

### NFR-013. Business Rule Scalability

Evaluation, rejection, classification, and prioritization rules shall be managed centrally, allowing them to be extended or modified without changing the overall process logic.

---

### NFR-014. Functional Scalability

New functionality shall be incorporated through additional modules or components, avoiding unnecessary modifications to functionality that has already been implemented and approved.

---

### NFR-015. Processing Scalability

The automation shall maintain stable behavior as the number of job postings, job sources, business rules, or executed processes increases.

Growth in processing volume shall not require structural redesign of the solution.

---

### NFR-016. Data Scalability

The architecture shall support the progressive growth of stored information while preserving data integrity, traceability, and efficient access to historical records.

---

### NFR-017. Configuration Scalability

System configurations shall be managed centrally, allowing new parameters to be incorporated without affecting existing configurations or requiring changes across multiple components.

---

### NFR-018. Compatibility with Future Integrations

The architecture shall facilitate the future integration of new services, tools, artificial intelligence models, or external components through clearly defined and loosely coupled interfaces.

---

### NFR-019. Maintenance Scalability

As the project grows, maintenance complexity shall not increase disproportionately.

The organization of the codebase, documentation, and architecture shall support controlled and progressive system evolution.

---

### NFR-020. Controlled Evolution

Every system enhancement shall comply with the project's architecture, standards, conventions, and documented rules, ensuring compatibility with existing components while avoiding unnecessary dependencies.

---

## 5. Availability

The following requirements establish the conditions under which the automation shall be ready to execute its processes and recover from interruptions that may affect its operation.

Availability shall ensure operational continuity within the limitations imposed by external dependencies and the underlying infrastructure.

---

### NFR-021. Operational Availability

The automation shall be ready to start and execute its processes whenever requested by the user or according to the defined schedule, provided that the required dependencies are available.

---

### NFR-022. Tolerance to External Unavailability

The temporary unavailability of a job source, external service, artificial intelligence model, or any other dependency shall not compromise the overall operation of the automation.

The system shall isolate the affected component and continue execution whenever permitted by the process rules.

---

### NFR-023. Processing Resumption

When a process is interrupted by a recoverable event, the automation shall be capable of resuming execution from the most appropriate point, avoiding unnecessary repetition of already completed tasks.

---

### NFR-024. Controlled Recovery

Failure recovery shall follow predefined and documented strategies, prioritizing information integrity and processing consistency.

---

### NFR-025. State Preservation

In the event of an interruption, the automation shall preserve both the operational state and the lifecycle state of every job posting, allowing processing to continue without loss of traceability.

---

### NFR-026. Module Independence

The unavailability of one module shall not prevent the operation of other modules unless an explicit functional dependency has been documented.

---

### NFR-027. Protection Against Unexpected Interruptions

The automation shall minimize the impact of unexpected shutdowns, system restarts, or execution interruptions by preserving the information required to resume processing later.

---

### NFR-028. External Dependency Management

The availability of each external dependency shall be verified before initiating operations that require it.

When a dependency is unavailable, the system shall apply the corresponding strategy before marking the process as failed.

---

### NFR-029. Service Continuity

Whenever technically feasible, processes unaffected by a failure shall continue executing normally, avoiding global interruptions of the automation.

---

### NFR-030. Unavailability Logging

Every interruption, service degradation, or detected unavailability shall be recorded to facilitate auditing, diagnostics, and continuous system improvement.

---

## 6. Security

The following requirements establish the conditions necessary to protect the information, configurations, and resources used by the automation throughout its entire lifecycle.

Security shall be applied as a cross-cutting concern across all system modules, preserving the confidentiality, integrity, and availability of information.

---

### NFR-031. Information Protection

All information managed by the automation shall be stored and processed using mechanisms that reduce the risk of loss, alteration, or unauthorized access.

---

### NFR-032. Credential Protection

Credentials, access keys, tokens, secrets, and any other sensitive data shall be kept separate from the source code and stored using appropriate protection mechanisms.

Under no circumstances shall they be embedded directly in the automation's source code.

---

### NFR-033. Protection of Sensitive Configurations

Configurations that may affect the security or operation of the system shall be managed centrally and protected against accidental or unauthorized modifications.

---

### NFR-034. Information Integrity

The automation shall preserve the integrity of the original data obtained from job sources.

Any transformation performed during processing shall be applied only to derived information or normalized structures, while keeping the original information available whenever necessary.

---

### NFR-035. Personal Data Protection

The user's personal information shall be used solely for the purposes defined by the automation and limited to the processes that genuinely require it.

The system shall minimize unnecessary exposure of personal data during processing and storage.

---

### NFR-036. Input Validation

All information originating from external sources, user configurations, or integrated services shall be validated before being used by the automation.

No external data shall be assumed to be valid without prior verification.

---

### NFR-037. Principle of Least Access

Each automation component shall access only the information and resources strictly necessary to fulfill its functional responsibility.

---

### NFR-038. Security Event Logging

Any event that may compromise the security of the automation shall be recorded to facilitate analysis, auditing, and subsequent remediation.

---

### NFR-039. Secure Recovery

Error recovery processes shall not compromise information integrity or bypass the validations defined by the system.

Every recovery operation shall preserve data consistency and processing traceability.

---

### NFR-040. Secure Evolution

The incorporation of new modules, services, dependencies, or functionalities shall not reduce the level of security previously achieved by the automation.

Every modification shall comply with the security requirements defined in this document.

---

## 7. Reliability

The following requirements establish the conditions necessary to ensure that the automation operates consistently, predictably, and reliably throughout its entire lifecycle.

Reliability shall ensure that results are reproducible, processing integrity is maintained, and any abnormal situation can be identified, recorded, and properly managed.

---

### NFR-041. Execution Consistency

The automation shall produce consistent results when processing the same information under the same input conditions and configuration.

---

### NFR-042. Processing Integrity

Each job posting shall complete only the stages of the functional workflow corresponding to its current state, preventing omissions, duplications, or out-of-sequence execution.

---

### NFR-043. Data Corruption Prevention

The system shall protect information against partial, inconsistent, or incomplete modifications that could compromise processing integrity.

---

### NFR-044. Anomaly Detection

The automation shall identify anomalous behavior during process execution and record it for later analysis, regardless of whether it results in an error.

---

### NFR-045. Tolerance to Recoverable Failures

Whenever a recoverable failure occurs, the automation shall apply the defined mechanisms to continue processing without compromising information consistency.

---

### NFR-046. Reproducibility

Automated decisions and generated results shall be reproducible using the same inputs, configurations, and business rules that were in effect at the time of execution.

---

### NFR-047. Functional Workflow Protection

No job posting shall skip mandatory stages, revert to incompatible states, or advance through undefined transitions unless explicitly authorized by a documented rule.

---

### NFR-048. Operational Stability

The automation shall maintain stable behavior during prolonged or repetitive executions, preventing degradation that could affect processing reliability.

---

### NFR-049. Result Verification

Upon completion of each process, the automation shall verify that the expected results have been correctly generated before continuing to the next stage of the functional workflow.

---

### NFR-050. Preservation of Traceability

Every action performed by the automation shall preserve the information necessary to reconstruct the processing carried out later, ensuring reliable audits, reviews, and reprocessing.

---

## 8. Maintainability

The following requirements establish the conditions necessary for the automation to be corrected, updated, extended, and maintained easily throughout its entire lifecycle.

Maintainability shall minimize the effort required to incorporate improvements, fix defects, replace components, or adapt the automation to new requirements.

---

### NFR-051. Modular Architecture

The automation shall be organized into modules with clearly defined responsibilities and low coupling, facilitating independent maintenance and evolution.

---

### NFR-052. Separation of Responsibilities

Each component shall fulfill a single, clearly identified functional responsibility.

Business logic, configuration, data access, and external service integration shall remain decoupled whenever technically feasible.

---

### NFR-053. Centralized Configuration

Business rules, operational parameters, general configurations, and other modifiable elements shall be managed from centralized locations, avoiding duplicated configurations.

---

### NFR-054. Up-to-Date Documentation

Every functional, technical, or architectural modification shall be reflected in the project's official documentation before being considered complete.

Documentation shall remain synchronized with the actual behavior of the automation.

---

### NFR-055. Ease of Updates

Enhancements, corrections, or new functionality shall be incorporated with the least possible impact on existing components.

Updates shall not require unnecessary modifications to unrelated modules.

---

### NFR-056. Component Replacement

The architecture shall facilitate the replacement of tools, libraries, external services, or internal components without significantly affecting the overall operation of the system.

---

### NFR-057. Reusability

Common components, functions, rules, and resources shall be designed to encourage reuse and avoid duplicated logic throughout the project.

---

### NFR-058. Implementation Consistency

All modules shall comply with the project's conventions, standards, and guidelines, ensuring consistency in organization and behavior.

---

### NFR-059. Ease of Diagnosis

The structure of the automation shall facilitate the identification of the source of errors, unexpected behavior, or performance issues through appropriate traceability mechanisms and logging.

---

### NFR-060. Controlled Evolution

Every modification made to the automation shall preserve compatibility with the architecture, functional requirements, non-functional requirements, and documented project rules, while avoiding unnecessary technical debt.

---

## 9. Portability

The following requirements establish the conditions necessary for the automation to be moved, installed, and executed across different environments with minimal effort while preserving its expected behavior and functionality.

Portability shall reduce dependence on specific platforms, tools, and infrastructures, facilitating the future evolution of the project.

---

### NFR-061. Environment Independence

The automation shall be designed so that its operation depends as little as possible on environment-specific characteristics.

Differences between environments shall be resolved through configuration mechanisms rather than modifications to system logic.

---

### NFR-062. Decoupled Configuration

Paths, environment variables, credentials, execution parameters, and all other configurations shall remain completely separate from the source code.

Migration between environments shall not require changes to functional components.

---

### NFR-063. Infrastructure Independence

The architecture shall minimize dependencies on specific infrastructure, hardware, or services whenever technically viable alternatives exist that satisfy the project requirements.

---

### NFR-064. Multi-Environment Compatibility

The automation shall be designed to facilitate execution in different compatible environments, such as development, testing, or production, while maintaining consistent behavior.

---

### NFR-065. Dependency Replacement

Libraries, tools, external services, or internal components shall be replaceable with minimal impact on the rest of the automation.

---

### NFR-066. Centralized Dependency Management

System dependencies shall be clearly identified, documented, and managed centrally to simplify installation, updates, and replacement.

---

### NFR-067. Data Portability

Data generated by the automation shall be stored using open, widely supported, and easily portable formats, avoiding unnecessary dependence on proprietary technologies.

---

### NFR-068. Documentation Portability

All functional, technical, and configuration documentation shall be maintained in open and widely compatible formats, facilitating access and maintenance using different tools.

---

### NFR-069. Environment Reproducibility

Project documentation shall enable a fully functional environment to be recreated by following only the documented procedures, without relying on undocumented knowledge.

---

### NFR-070. Technological Evolution

The architecture shall facilitate the future incorporation of new technologies or the replacement of existing components without requiring significant reconstruction of the automation.

---

## 10. Compatibility

The following requirements establish the conditions necessary to ensure that the different automation components can interact correctly with one another and with the external dependencies planned during project development.

Compatibility shall facilitate integration, technological evolution, and the incorporation of new components without compromising the overall operation of the system.

---

### NFR-071. Inter-Module Compatibility

All automation modules shall communicate through clearly defined interfaces that are compatible with the system architecture.

No module shall depend on the internal implementation details of other components.

---

### NFR-072. Compatibility with External Dependencies

The automation shall use integration mechanisms compatible with the platforms, services, and tools approved for the project, respecting the technical and operational constraints of each.

---

### NFR-073. Data Format Compatibility

Information exchanged between modules and external dependencies shall use standardized, consistent, and widely supported formats.

Any required transformations shall be performed without affecting information integrity.

---

### NFR-074. Configuration Compatibility

System configurations shall remain compatible across the different execution environments, preventing differences that alter the expected behavior of the automation.

---

### NFR-075. Compatibility with Future Extensions

The incorporation of new modules, job sources, artificial intelligence models, or external services shall not require significant modifications to the interfaces already established.

---

### NFR-076. Version Compatibility

Whenever a component depends on specific versions of tools, libraries, or external services, those dependencies shall be documented to ensure system stability.

---

### NFR-077. Documentation Compatibility

Functional, technical, and architectural documentation shall remain aligned with the current version of the automation, avoiding inconsistencies between implemented behavior and official documentation.

---

### NFR-078. Data Model Compatibility

Changes made to data structures shall preserve compatibility with the components that use them or include predefined migration mechanisms.

---

### NFR-079. Evolutionary Compatibility

Enhancements incorporated into the system shall maintain compatibility with existing functionality unless an incompatible modification has been previously documented, justified, and approved.

---

### NFR-080. Architectural Compatibility

Every new component shall comply with the principles, standards, conventions, and interfaces defined by the project's official architecture before being integrated into the automation.

---

## 11. Usability

The following requirements establish the conditions necessary for the automation to be easy for the user to understand, configure, operate, and monitor.

Usability shall reduce the operational complexity of the system, making it easier to manage without requiring unnecessary technical knowledge for routine activities.

---

### NFR-081. Simple Configuration

The automation's common configuration settings shall be organized in a clear and structured manner, allowing them to be understood and modified without affecting the rest of the system.

---

### NFR-082. Understandable Information

All information presented to the user shall use terminology consistent with the project's official documentation and clearly describe the corresponding status, result, or action.

---

### NFR-083. Interface Consistency

The mechanisms used to query information, review results, manage configurations, or make decisions shall maintain consistent behavior throughout the automation.

---

### NFR-084. User Traceability

The user shall be able to easily identify the current status of each job posting, the actions performed, the decisions made, and the outcome of every processing stage.

---

### NFR-085. Ease of Administration

Routine administrative tasks, such as updating configurations, reviewing results, consulting logs, or modifying rules, shall be performed through clearly defined and documented procedures.

---

### NFR-086. Informative Messages

The automation shall provide clear messages during process execution, indicating progress, warnings, errors, and any actions required from the user whenever applicable.

---

### NFR-087. Reduced Manual Intervention

The automation shall minimize the number of repetitive actions requiring user intervention, reserving user participation exclusively for the predefined strategic decisions.

---

### NFR-088. Ease of Learning

The organization of the automation, its documentation, and its configurations shall enable new users to progressively understand its operation without relying on implicit knowledge.

---

### NFR-089. Information Accessibility

Relevant information about each job posting, execution, analysis, or decision shall be organized and readily available for quick and structured consultation.

---

### NFR-090. Documentation Consistency

The terminology used by the automation shall remain aligned with the Project Glossary and the rest of the project's official documentation, ensuring a consistent user experience during system administration and monitoring.

---

## 12. Technological Constraints

The following requirements establish the technological limitations and criteria that shall be respected during the design, development, implementation, and evolution of the automation.

These constraints are intended to ensure technical consistency throughout the project, reduce maintenance complexity, and comply with the principles established during project planning.

---

### NFR-091. Priority for Free Tools

The automation shall be built using free tools, libraries, services, and technologies whenever they satisfy the project's functional and non-functional requirements.

---

### NFR-092. Adoption of Paid Technologies

No paid technology, service, or tool shall be incorporated into the project without documented technical justification and the user's explicit approval.

---

### NFR-093. Widely Supported Technologies

Priority shall be given to technologies that provide sufficient documentation, active maintenance, established communities, and broad support, reducing the risk of obsolescence or abandonment.

---

### NFR-094. Use of Open Standards

Whenever technically feasible, the automation shall use open standards for data formats, communication protocols, and information exchange.

---

### NFR-095. Minimization of Dependencies

The incorporation of unnecessary external dependencies shall be avoided.

Every new dependency shall provide a clearly justified benefit relative to its maintenance cost and added complexity.

---

### NFR-096. Vendor Independence

The architecture shall minimize coupling to specific vendors, platforms, or services, facilitating their replacement whenever necessary.

---

### NFR-097. Architectural Compatibility

Every technology incorporated into the project shall comply with the architecture, design principles, and standards defined in the official documentation.

---

### NFR-098. Version Management

The versions of all tools, libraries, and components used shall be documented to ensure environment reproducibility and facilitate future updates.

---

### NFR-099. Prior Evaluation of New Technologies

Before incorporating any new tool, service, or dependency, its compatibility with the architecture, maintenance impact, scalability, and long-term continuity shall be evaluated.

---

### NFR-100. Restriction on Technological Changes

The replacement of core technologies during project development shall only be allowed when supported by documented technical justification and approved by the user.

---

## 13. Expected Resource Consumption

The following requirements establish the criteria for the efficient use of computational resources during automation execution.

The objective is to ensure that the system operates efficiently and consistently while avoiding unnecessary resource consumption and supporting execution in resource-constrained environments.

---

### NFR-101. Efficient Resource Usage

The automation shall use only the resources necessary to execute each process, avoiding unnecessary consumption of memory, processing power, storage, and bandwidth.

---

### NFR-102. Processing Optimization

Modules shall execute only the operations required for the current state of each job posting, avoiding redundant calculations, queries, or analyses.

---

### NFR-103. Memory Management

The automation shall promptly release memory resources used during each process, preventing unnecessary accumulation that could degrade system performance.

---

### NFR-104. Storage Management

Stored information shall be organized efficiently, avoiding unnecessary duplication while retaining only the data required to ensure traceability, auditing, and proper system operation.

---

### NFR-105. Query Optimization

Queries made to databases, job sources, and other external dependencies shall minimize repeated and unnecessary access through appropriate organization and information reuse strategies.

---

### NFR-106. Responsible Bandwidth Usage

The automation shall minimize unnecessary data transfers to and from external services, downloading only the information required for each process.

---

### NFR-107. Concurrent Process Control

The number of processes executed simultaneously shall remain within limits that guarantee the stability of both the system and the external dependencies it uses.

---

### NFR-108. Historical Storage Optimization

Growth in the history of job postings, logs, metrics, and documents shall not significantly affect the overall performance of the automation.

The organization of stored information shall facilitate long-term management and retrieval.

---

### NFR-109. Resource Consumption Monitoring

The automation shall record metrics that allow approximate resource consumption during execution to be identified, facilitating the detection of optimization opportunities.

---

### NFR-110. Resource Consumption Scalability

As the volume of processed job postings increases, resource consumption shall grow proportionally and in a controlled manner, avoiding disproportionate increases relative to the work performed.

---

## 14. Maximum Execution Times

The following requirements establish the criteria for controlling the duration of processes executed by the automation.

The objective is to ensure that execution remains within reasonable limits, detect abnormal processes in a timely manner, and facilitate recovery whenever an operation exceeds the expected duration.

Specific maximum execution times shall be defined during architectural design and module implementation, once the technologies, dependencies, and actual execution conditions are known.

---

### NFR-111. Maximum Execution Time per Process

Every process executed by the automation shall have a predefined maximum execution time.

When this limit is exceeded, the system shall apply the corresponding management strategy.

---

### NFR-112. Long-Running Process Monitoring

The automation shall identify processes whose execution time exceeds expected behavior and record them for subsequent analysis.

---

### NFR-113. Controlled Termination

When a process exceeds the maximum allowed execution time and cannot be completed safely, the automation shall terminate it in a controlled manner while preserving information integrity and processing traceability.

---

### NFR-114. Timeout Management

Operations that depend on external services shall use configurable timeout values to prevent indefinite blocking during execution.

---

### NFR-115. Temporal Independence Between Modules

Delays in one module shall not permanently block other independent processes unless an explicit functional dependency has been documented.

---

### NFR-116. Resumption After Interruption

When a process is stopped because it exceeded the maximum allowed execution time and a recovery strategy exists, the automation shall allow it to resume without unnecessarily repeating completed tasks.

---

### NFR-117. Centralized Time Configuration

Time limits used by the automation shall be managed through centralized configurations, avoiding values distributed throughout module logic.

---

### NFR-118. Logging of Time Exceedances

Every execution that exceeds the expected time shall be recorded with at least the following information:

- Affected process.
- Date and time.
- Observed duration.
- Configured limit.
- Action performed by the automation.

---

### NFR-119. Continuous Optimization

Information collected about execution times shall be used to identify processes that can be optimized during the project's evolution.

---

### NFR-120. Adaptability of Time Limits

Maximum execution times shall be adjustable as the architecture, processing volume, and characteristics of external dependencies evolve, without requiring modifications to the system's functional logic.

---

## 15. Failure Recovery

The following requirements establish the conditions necessary for the automation to detect, manage, and recover from failures without compromising information integrity, processing traceability, or overall system stability.

Failure recovery shall prioritize operational continuity whenever technically feasible and compatible with the defined business rules.

---

### NFR-121. Failure Detection

The automation shall promptly identify any failure that prevents or compromises the normal execution of a process and initiate the corresponding recovery strategy.

---

### NFR-122. Controlled Recovery

Every recovery operation shall follow predefined and documented procedures, avoiding improvised actions or non-deterministic behavior.

---

### NFR-123. State Preservation

Whenever a failure occurs, the system shall preserve the operational state, lifecycle state, and the information required to resume processing at a later time.

---

### NFR-124. Controlled Retries

Processes that support automatic recovery shall use predefined retry mechanisms, avoiding infinite loops or unnecessary repeated executions.

---

### NFR-125. Failure Isolation

A failure occurring in one module shall not automatically propagate to other independent components unless an explicit functional dependency has been documented.

---

### NFR-126. Integrity Protection

No recovery process shall compromise data integrity, generate inconsistencies, or alter the traceability of processing completed before the failure occurred.

---

### NFR-127. Incident Escalation

When a failure cannot be resolved through the defined automatic mechanisms, the automation shall record the situation and mark the process for user intervention whenever appropriate.

---

### NFR-128. Recovery Logging

Every executed recovery strategy shall record, at a minimum:

- Affected process.
- Cause of the failure.
- Applied strategy.
- Number of retries performed.
- Obtained result.
- Final process status.

---

### NFR-129. Safe Resumption

When recovery is successful, the automation shall resume processing from the most appropriate point, avoiding unnecessary repetition of correctly completed tasks.

---

### NFR-130. Reproducible Recovery

Recovery mechanisms shall produce consistent and predictable behavior when handling equivalent failures, ensuring that identical situations result in the same recovery strategy under the same conditions.

---

## 16. Observability (Logs and Metrics)

The following requirements establish the conditions necessary for the automation to make its behavior understandable, measurable, and auditable throughout the execution of all its processes.

Observability shall provide sufficient information to monitor system operation, diagnose problems, measure performance, and support the continuous improvement of the automation.

---

### NFR-131. Comprehensive Event Logging

The automation shall record all relevant events that occur during execution, allowing the complete behavior of the system to be reconstructed.

---

### NFR-132. Process Logging

Every executed process shall generate records containing at least the following information:

- Execution identifier.
- Responsible module.
- Start date and time.
- End date and time.
- Obtained result.
- Final status.

---

### NFR-133. Decision Logging

Every automated decision shall be recorded together with the information necessary to understand:

- The applied rule.
- The evaluated data.
- The decision made.
- The obtained result.

---

### NFR-134. Error and Exception Logging

Every error, exception, or unexpected behavior shall be recorded together with the information required to facilitate diagnosis, recovery, and subsequent analysis.

---

### NFR-135. State Transition Logging

Every lifecycle and operational state transition of a job posting shall be recorded, including the time of the change and the entity responsible for the transition (system or user).

---

### NFR-136. Execution Metrics

The automation shall collect metrics that make it possible to evaluate its operational behavior, including at least:

- Number of discovered job postings.
- Number of processed job postings.
- Number of discarded job postings.
- Number of executed processes.
- Number of errors.
- Number of retries.
- Execution duration.

---

### NFR-137. Performance Metrics

The system shall record indicators that enable the efficiency of each module to be analyzed and optimization opportunities to be identified throughout the project's evolution.

---

### NFR-138. Log Retention

Logs generated by the automation shall be retained for the period defined by the project's management strategy, enabling audits, historical analysis, and reprocessing whenever required.

---

### NFR-139. Operational Information Access

Recorded information shall be organized in a way that facilitates querying, searching, and analyzing processes, job postings, decisions, errors, and metrics without affecting the operation of the automation.

---

### NFR-140. Complete Traceability

The combination of logs, metrics, and events shall make it possible to fully reconstruct the journey of a job posting from its discovery through the completion of its processing, including every generated action, decision, state, and result throughout its lifecycle.

---

## 17. Acceptance Criteria

The automation shall satisfy the non-functional requirements when it can be verified that it meets the following acceptance criteria during testing, validation, and system operation.

---

### NAC-001. Performance

The automation executes its processes within the performance limits defined for each module, without significant degradation during normal operation.

---

### NAC-002. Scalability

New job sources, business rules, modules, or functionalities can be incorporated without requiring significant modifications to existing components.

---

### NAC-003. Availability

The automation can start and execute its processes whenever the required dependencies are available and properly manages temporary interruptions of external services.

---

### NAC-004. Security

Credentials, sensitive configurations, and personal data remain protected and separate from the automation logic, complying with the defined security mechanisms.

---

### NAC-005. Reliability

The automation produces consistent and reproducible results under the same input conditions while preserving processing integrity throughout the entire lifecycle of job postings.

---

### NAC-006. Maintainability

Modifications, corrections, and extensions can be implemented without unnecessarily affecting other components and while respecting the project's architecture and official documentation.

---

### NAC-007. Portability

The automation can be installed and executed in the intended environments using only the documented procedures and configurations.

---

### NAC-008. Compatibility

Modules, services, and external dependencies interact correctly through the defined interfaces while preserving the consistency of information exchange.

---

### NAC-009. Usability

The user can configure, manage, review results, and monitor the automation using the documentation and mechanisms provided by the system.

---

### NAC-010. Technological Constraints

The technologies used comply with the project's defined constraints, prioritizing free tools, open standards, and components compatible with the system architecture.

---

### NAC-011. Resource Consumption

The automation uses computational resources efficiently and maintains stable behavior as the processing volume increases.

---

### NAC-012. Execution Times

Processes comply with the configured maximum execution times or correctly apply the defined strategies whenever those limits are exceeded.

---

### NAC-013. Failure Recovery

The automation detects, records, and recovers from failures according to the documented strategies while preserving information integrity and processing continuity whenever possible.

---

### NAC-014. Observability

Generated logs, metrics, and events allow complete monitoring, auditing, and reconstruction of the automation's behavior during any execution.

---

### NAC-015. Overall Compliance

All non-functional requirements defined in this document can be verified through objective evidence obtained during testing, operation, or review of the project's official documentation.

---

## 18. Non-Functional Requirements Index

This document contains the following groups of non-functional requirements:

| Range | Category |
|--------|----------|
| NFR-001 – NFR-010 | Performance |
| NFR-011 – NFR-020 | Scalability |
| NFR-021 – NFR-030 | Availability |
| NFR-031 – NFR-040 | Security |
| NFR-041 – NFR-050 | Reliability |
| NFR-051 – NFR-060 | Maintainability |
| NFR-061 – NFR-070 | Portability |
| NFR-071 – NFR-080 | Compatibility |
| NFR-081 – NFR-090 | Usability |
| NFR-091 – NFR-100 | Technological Constraints |
| NFR-101 – NFR-110 | Expected Resource Consumption |
| NFR-111 – NFR-120 | Maximum Execution Times |
| NFR-121 – NFR-130 | Failure Recovery |
| NFR-131 – NFR-140 | Observability (Logs and Metrics) |

Each requirement has a unique and immutable identifier that may be used as a reference throughout the project's documentation, implementation, testing, architecture, and future documents.

NFR identifiers shall not be reused or modified once this document has been approved.
