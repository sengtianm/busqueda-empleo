# Document 1
# Functional Requirements

## 1. System Purpose

Develop a comprehensive automation that autonomously discovers, collects, processes, evaluates, and manages job postings by handling all repetitive tasks involved in the job search process.

The system shall transform discovered job postings into structured information, evaluate them according to predefined criteria, and generate all the resources required to facilitate and accelerate the application process.

The automation shall act as an intelligent assistant specialized in job searching, automating repetitive and operational activities while keeping strategic or high-impact decisions under the user's control.

---

## 2. General Objective

Design and implement a modular, scalable, and maintainable automation that comprehensively manages the job search process, from discovering opportunities to generating the resources required for job applications, while automating repetitive tasks and providing the user with structured information and analysis to support decision-making.

---

## 3. Specific Objectives

1. Automatically discover job opportunities from the configured job sources.

2. Centralize all discovered job postings in a single structured repository, preventing duplicates and maintaining their history.

3. Prepare each job posting through data cleaning, normalization, and validation processes.

4. Automatically evaluate job postings using predefined criteria to determine their compatibility with the user's professional profile.

5. Classify job postings according to their priority and processing status.

6. Perform in-depth analysis of job postings that pass the initial evaluation in order to generate valuable information for the application process.

7. Automatically generate the resources required to support the job application process according to the characteristics of each job posting.

8. Maintain a complete record of each job posting's lifecycle, including status changes, decisions, and results.

9. Provide the user with clear, organized, and sufficient information to support decision-making throughout every stage of the process.

10. Reduce the time and effort spent on repetitive job search tasks through automated processes.

11. Allow the incorporation of new job sources, evaluation rules, and functionalities without affecting the operation of existing components.

---

## 4. Functional Scope

The automation shall provide the following functional capabilities:

### 4.1 Opportunity Discovery

- Query the configured job sources.
- Detect new job postings.
- Extract the available information from each job posting.
- Register discovered job postings.

### 4.2 Job Posting Preparation

- Clean and normalize the extracted information.
- Validate data integrity.
- Detect and remove duplicate job postings.
- Assign the initial processing status.

### 4.3 Initial Evaluation

- Automatically analyze each job posting according to the defined criteria.
- Calculate a compatibility score.
- Classify job postings by priority.
- Automatically discard job postings that violate predefined rules.

### 4.4 Deep Processing

- Perform a detailed analysis of selected job postings.
- Identify requirements, responsibilities, benefits, and other relevant information.
- Generate structured information to support application preparation.
- Prepare the defined resources for the application process.

### 4.5 Process Management

- Maintain the complete history of each job posting.
- Manage processing workflow statuses.
- Record decisions and results.
- Enable tracking of each job posting throughout its lifecycle.

### 4.6 Administration

- Allow the configuration of job sources.
- Allow updates to evaluation criteria.
- Allow the incorporation of new rules and functionalities without affecting existing components.

## Out of Scope

The automation shall not be responsible for:

- Making strategic decisions that require user approval.
- Modifying the user's professional profile without authorization.
- Automatically submitting job applications unless that functionality has been explicitly approved and implemented.
- Replacing the user's judgment in high-impact decisions.
- Performing activities unrelated to the job search and job opportunity preparation process.

---

## 5. Main System Functions

The system shall provide the following primary functions:

### F1. Opportunity Discovery

- Automatically query the configured job sources.
- Detect newly available job postings.
- Extract relevant information from each job posting.
- Record the date, time, and source of discovery.

---

### F2. Job Posting Management

- Create a unique record for each job posting.
- Detect and prevent duplicate records.
- Update information when a job posting changes.
- Maintain a history of modifications.

---

### F3. Information Preparation

- Clean extracted data.
- Normalize formats and structures.
- Complete derived information whenever possible.
- Validate the quality of the obtained data.

---

### F4. Automated Evaluation

- Analyze job postings using predefined criteria.
- Calculate a compatibility score.
- Classify job postings according to priority.
- Automatically identify job postings that should be discarded.

---

### F5. Deep Processing

- Analyze the complete content of job postings.
- Identify technical and functional requirements.
- Extract responsibilities, benefits, and working conditions.
- Generate structured information to support the application process.

---

### F6. Resource Generation

- Generate the documents, analyses, or resources defined to support each job application.
- Organize generated resources by job posting.
- Maintain traceability between each generated resource and its corresponding job posting.

---

### F7. Workflow Management

- Control the status of each job posting throughout its entire lifecycle.
- Record every status transition.
- Record both automated decisions and user decisions.
- Allow interrupted processes to be resumed.

---

### F8. Administration

- Manage job sources.
- Manage evaluation criteria.
- Manage general system settings.
- Manage catalogs, rules, and parameters.

---

### F9. Query and Tracking

- Allow users to view the complete history of job postings.
- Display the current status of each job posting.
- View evaluation results.
- Access information generated during processing.

---

### F10. Logging and Auditing

- Record relevant system events.
- Record errors and exceptions.
- Record automated decisions.
- Maintain complete traceability for the processing of every job posting.

---

## 6. Functions Out of Scope

The automation shall not be responsible for the following functions unless their implementation is explicitly approved in future versions of the project.

### FNA-1. Automatic Job Application

The system shall not automatically submit job applications without the user's explicit approval.

---

### FNA-2. Strategic Decision-Making

The system shall not replace the user's judgment in high-impact decisions, including but not limited to:

- Choosing which company to apply to.
- Deciding whether an opportunity is personally worthwhile.
- Modifying professional criteria without authorization.

---

### FNA-3. Professional Profile Modification

The system shall not automatically modify the user's professional information, including:

- Resume.
- Professional profile.
- Portfolio.
- Personal information.
- Job preferences.

---

### FNA-4. Communication with Third Parties

The system shall not send emails, messages, or any other external communication on behalf of the user unless such functionality has been explicitly designed, implemented, and approved.

---

### FNA-5. Interview Management

The system shall not schedule interviews, accept invitations, or respond automatically to recruitment processes.

---

### FNA-6. Activities Outside the Scope

The system shall not perform tasks that are not directly related to the discovery, analysis, evaluation, preparation, and management of job opportunities.

---

### FNA-7. Autonomous Learning

The system shall not modify business rules, evaluation criteria, or system configurations on its own without user intervention.

---

## 7. System Actors

Actors represent the people or systems that interact directly or indirectly with the automation.

Actors and external dependencies:

- User

External dependencies:

- Job platforms
- AI model
- Database
- Browser
- File system
- APIs

---

### A1. User

The owner and operator of the automation.

**Responsibilities:**

- Configure the system.
- Define evaluation criteria.
- Authorize decisions that require human intervention.
- Review generated results.
- Update professional information when necessary.

---

### A2. Job Platforms

The sources from which the automation retrieves job opportunities.

**Examples:**

- LinkedIn
- Indeed
- Computrabajo
- Magneto
- Corporate career websites
- Other sources configured by the user

**Responsibilities:**

- Publish job postings.
- Provide the available information for processing.

---

### A3. Artificial Intelligence Model

The AI service used by the automation to analyze and generate information.

**Responsibilities:**

- Analyze job postings.
- Extract relevant information.
- Classify content.
- Generate analyses.
- Support the generation of application resources.

---

### A4. External Services

Any service used to support the operation of the automation.

**Examples:**

- Storage services.
- Databases.
- File services.
- Automation tools.
- Auxiliary APIs.

**Responsibilities:**

- Store information.
- Facilitate communication between components.
- Provide supporting services for the system.

---

## 8. System Inputs

System inputs include all the information required to execute the discovery, evaluation, processing, and management of job opportunities.

### E-001. User Configuration

Information defined by the user to customize the behavior of the automation.

Includes, among others:

- Job sources.
- Execution frequency.
- General preferences.
- Configuration parameters.

---

### E-002. Professional Profile

Information used to evaluate compatibility between the user and job postings.

Includes:

- Resume.
- Professional profile.
- Work experience.
- Skills.
- Technologies.
- Languages.
- Certifications.
- Academic background.
- Job preferences.
- Salary expectations.
- Work arrangement.
- Location.
- Target companies.
- Restricted companies.

---

### E-003. Job Postings

Information obtained from the different job platforms.

May include:

- Title.
- Company.
- Description.
- Requirements.
- Responsibilities.
- Benefits.
- Salary.
- Work arrangement.
- Location.
- Publication date.
- URL.
- Job posting identifier.
- Source platform.

---

### E-004. Business Rules

The set of criteria defined to control the behavior of the automation.

Includes:

- Evaluation rules.
- Rejection rules.
- Acceptance rules.
- Priorities.
- Thresholds.
- Exceptions.

---

### E-005. AI Prompts and Configurations

The set of instructions used to request analysis and information generation from the AI model.

Includes:

- Prompts.
- Templates.
- Execution parameters.
- Processing configurations.

---

### E-006. Historical Information

Information generated during previous executions.

Includes:

- Job posting history.
- Previous statuses.
- Evaluation results.
- Generated documents.
- Execution logs.
- User decisions.

---

### E-007. User Decisions

Information provided by the user whenever a decision cannot be made automatically.

**Examples:**

- Approve a job posting.
- Reject a job posting.
- Request a new analysis.
- Modify evaluation criteria.
- Resume a process.

---

## 9. Internal System Data

Internal data consists of all information generated, transformed, and maintained by the automation to control job posting processing and ensure system consistency.

### DI-001. Internal Identifiers

Information used to uniquely identify system elements.

Includes:

- Internal job posting ID.
- Processing ID.
- Execution ID.
- Analysis ID.
- Generated document ID.

---

### DI-002. Processing Status

Information used to track the progress of each job posting within the workflow.

Includes:

- Current status.
- Previous status.
- Date of change.
- Reason for the change.
- Entity responsible for the change (user or system).

---

### DI-003. Intermediate Results

Information generated during the different processing stages.

Examples:

- Partial scores.
- Temporary classifications.
- Extracted information.
- Normalized data.
- Validation results.

---

### DI-004. Operational Configuration

Information used by the automation during execution.

Includes:

- Internal parameters.
- Execution variables.
- Module configuration.
- Workflow configuration.
- Internal thresholds.

---

### DI-005. System History

Information maintained to guarantee processing traceability.

Includes:

- Change history.
- Evaluation history.
- Decision history.
- Reprocessing history.

---

### DI-006. Execution Metrics

Information used to measure the performance of the automation.

Includes:

- Execution time.
- Duration per module.
- Number of processed job postings.
- Number of errors.
- Number of retries.
- Performance indicators.

---

### DI-007. Internal Relationships

Information used to relate the different system elements.

Examples:

- Job Posting ↔ Evaluations
- Job Posting ↔ Documents
- Job Posting ↔ History
- Job Posting ↔ Decisions
- Job Posting ↔ Executions

---

## 10. System Outputs

System outputs consist of all information generated by the automation as a result of processing job postings.

### S-001. Structured Job Postings

Normalized information for each job posting, ready to be used by the different automation processes.

Includes, among others:

- Clean information.
- Normalized fields.
- Validated data.
- Internal identifiers.

---

### S-002. Initial Evaluation Results

Information obtained during the automated compatibility analysis.

Includes:

- Score.
- Compatibility level.
- Priority.
- Acceptance reasons.
- Rejection reasons.
- Recommendations.

---

### S-003. In-Depth Job Posting Analysis

Information obtained during the detailed processing of the job posting.

Includes:

- Executive summary.
- Identified requirements.
- Technical competencies.
- Soft skills.
- Responsibilities.
- Benefits.
- Risks.
- Relevant observations.

---

### S-004. Application Resources

Resources generated to facilitate the preparation of a job application.

May include:

- Strategic analyses.
- Organized information.
- Documents defined for each job posting.
- Other resources approved during project development.

---

### S-005. Job Posting Status

Updated information about the current situation of each job posting within the processing workflow.

Includes:

- Current status.
- Last update date.
- Status history.
- Person or system responsible for the latest decision.

---

### S-006. Reports

Consolidated information about the operation of the automation.

May include:

- Number of discovered job postings.
- Number of discarded job postings.
- Number of prioritized job postings.
- Processing time.
- Execution metrics.
- General statistics.

---

### S-007. System Logs

Information used for auditing and monitoring.

Includes:

- Events.
- Errors.
- Warnings.
- Automated decisions.
- User decisions.
- Execution history.

---

## 11. General Functional Workflow

The system shall manage every job posting through a functional workflow consisting of the following stages.

### FF-01. Discovery

- Query configured job sources.
- Detect new job postings.
- Extract available information.
- Register the job posting in the system.

↓

### FF-02. Preparation

- Clean the information.
- Normalize the data.
- Validate the integrity of the job posting.
- Detect duplicates.
- Assign the initial status.

↓

### FF-03. Initial Evaluation

- Analyze compatibility with the professional profile.
- Apply rejection rules.
- Calculate the initial score.
- Classify priority.

↓

### FF-04. Initial Decision

If the job posting does not meet the minimum criteria:

→ End processing.

If it meets the criteria:

→ Continue to Deep Processing.

↓

### FF-05. Deep Processing

- Analyze the job posting in detail.
- Identify requirements.
- Identify competencies.
- Analyze responsibilities.
- Analyze benefits.
- Generate structured information.

↓

### FF-06. Resource Generation

- Prepare the resources defined to support the application.
- Organize the generated results.
- Associate the generated resources with the corresponding job posting.

↓

### FF-07. User Review

Whenever the workflow requires a strategic decision:

- Present the information to the user.
- Wait for the corresponding decision.
- Record the decision made.

↓

### FF-08. Management and Tracking

- Update the job posting status.
- Record its history.
- Preserve complete traceability.
- Keep all generated information available.

↓

### FF-09. Completion

- Mark processing as completed.
- Record the completion date.
- Preserve all information for future reference.

---

## 12. Job Posting Lifecycle

Each job posting shall follow a lifecycle consisting of the following stages.

### LC-01. Discovered

The job posting has been found on a job source and registered in the system for the first time.

---

### LC-02. Prepared

The information has been cleaned, normalized, validated, and is ready for evaluation.

---

### LC-03. Evaluated

The job posting has been analyzed using the initial evaluation rules and has received a compatibility score.

---

### LC-04. Accepted

The job posting has passed the initial evaluation and is approved to continue in the process.

---

### LC-05. Discarded

The job posting is no longer being processed because it did not satisfy the defined rules or because the user decided to discard it.

---

### LC-06. Processed

The job posting has been analyzed in depth, and all information required to support the application has been generated.

---

### LC-07. Finalized

The job posting has completed its lifecycle within the automation, and all related information has been stored for future reference.

---

## 13. Job Posting Status Catalog

The system shall control the lifecycle of every job posting using a predefined set of statuses.

> **Official catalog (decision 2026-07-30):** the 7 statuses below are the single source of truth for the offer lifecycle, aligned with `shared/state_machine.py`. Previous versions of this catalog (EST-001..010, EST-999 Error) are superseded.

### EST-001. Discovered

**Description**

The job posting has been identified from a job source and registered for the first time.

**Functional Process**

FP-01 — Discovery

**Assigned By**

System

**Previous Statuses**

None

**Next Statuses**

- EST-002 Prepared

---

### EST-002. Prepared

**Description**

The information has been cleaned, normalized, and validated.

**Functional Process**

FP-02 — Preparation

**Assigned By**

System

**Previous Statuses**

- EST-001

**Next Statuses**

- EST-003 Evaluated

---

### EST-003. Evaluated

**Description**

The job posting has been evaluated according to the business rules.

**Functional Process**

FP-03 — Initial Evaluation

**Assigned By**

System

**Previous Statuses**

- EST-002

**Next Statuses**

- EST-004 Accepted
- EST-005 Discarded

---

### EST-004. Accepted

**Description**

The job posting has passed the initial evaluation and is approved to continue in the process.

**Functional Process**

FP-03 — Initial Evaluation

**Assigned By**

System

**Previous Statuses**

- EST-003

**Next Statuses**

- EST-006 Processed

---

### EST-005. Discarded

**Description**

The job posting is no longer being processed because it did not satisfy the defined rules or because the user decided to discard it.

**Functional Process**

FP-03 — Initial Evaluation
FP-07 — User Review

**Assigned By**

System
User

**Previous Statuses**

- EST-003

**Final Status**

Yes

---

### EST-006. Processed

**Description**

The job posting has been analyzed in depth, and all information required to support the application has been generated.

**Functional Process**

FP-05 — Deep Processing

**Assigned By**

System

**Previous Statuses**

- EST-004

**Next Statuses**

- EST-007 Finalized

---

### EST-007. Finalized

**Description**

The job posting has completed its lifecycle within the automation, and all related information has been stored for future reference.

**Functional Process**

FP-08 — Management and Tracking

**Assigned By**

System

**Previous Statuses**

- EST-005
- EST-006

**Final Status**

Yes

---

## 14. Automated Decisions

The automation may make decisions autonomously only when predefined and documented rules exist.

### DA-001. Job Discovery

- Detect new job postings.
- Identify whether a job posting already exists.
- Register new opportunities.

---

### DA-002. Information Preparation

- Clean data.
- Normalize formats.
- Validate required fields.
- Detect inconsistent information.

---

### DA-003. Duplicate Management

- Identify duplicate job postings.
- Associate equivalent records.
- Prevent duplicate processing.

---

### DA-004. Initial Evaluation

- Calculate the compatibility score.
- Apply rejection rules.
- Assign a priority.
- Classify the job posting.

---

### DA-005. Deep Processing

- Analyze the content of the job posting.
- Extract requirements.
- Identify competencies.
- Generate structured information.
- Produce the analyses defined by the system.

---

### DA-006. Resource Generation

- Generate the resources defined to support the job application.
- Organize the generated information.
- Associate each resource with its corresponding job posting.

---

### DA-007. Workflow Management

- Change the lifecycle status when the defined conditions are met.
- Update the operational status.
- Record events.
- Record metrics.
- Record history.

---

### DA-008. Operational Recovery

- Retry processes when a recovery strategy has been defined.
- Resume interrupted processes.
- Mark processes that require user intervention.

---

### General Principle

Every automated decision shall be:

- Reproducible.
- Traceable.
- Auditable.
- Based on documented rules.
- Reversible whenever technically possible.

---

## 15. Decisions Requiring User Intervention

The following decisions shall be made exclusively by the user unless their automation is explicitly approved in a future version of the project.

### DU-001. Opportunity Approval

Decide whether a job posting should continue to be considered a worthwhile opportunity.

---

### DU-002. Manual Rejection

Discard a job posting for personal or strategic reasons that cannot be determined automatically.

Examples:

- Personal preferences.
- Organizational culture.
- Interest in the company.
- External information unavailable to the system.

---

### DU-003. Exceptional Prioritization

Manually modify the priority automatically assigned by the system.

---

### DU-004. Job Application Approval

Authorize the final preparation of an application for a specific job posting.

---

### DU-005. Application Submission

Authorize any action that involves sending the user's information to third parties.

Examples:

- Send a resume.
- Complete an application form.
- Send an email.
- Share documents.

---

### DU-006. Professional Profile Modification

Authorize changes to:

- Resume.
- Professional profile.
- Portfolio.
- Personal information.
- Job preferences.

---

### DU-007. System Rule Modification

Approve changes to:

- Evaluation rules.
- Rejection rules.
- Thresholds.
- Critical configurations.
- Decision criteria.

---

### DU-008. Exceptional Reprocessing

Authorize the reprocessing of job postings when the system detects situations that cannot be resolved automatically.

---

### General Principle

Any decision involving strategic, legal, personal, or user representation consequences shall require the user's explicit approval before execution.

---

## 16. General Functional Rules

The following rules shall be observed throughout the operation of the automation.

### GFR-001. Traceability

Every action, decision, recommendation, and status change shall be recorded.

---

### GFR-002. Unique Identification

Every job posting shall have a unique and immutable identifier within the system.

---

### GFR-003. No Duplication

The same job posting shall never be processed simultaneously more than once.

---

### GFR-004. Information Integrity

The automation shall not delete or modify the original information obtained from job sources.

Any transformations shall be performed on derived or normalized data.

---

### GFR-005. Data Separation

Inputs, internal data, and outputs shall remain conceptually independent entities.

---

### GFR-006. Document Traceability

Every generated document, analysis, or resource shall be traceable to the job posting from which it originated.

---

### GFR-007. Status Control

Every job posting shall always have exactly one lifecycle status and one operational status.

Conflicting statuses shall never exist simultaneously.

---

### GFR-008. Pre-Validation

No process shall be executed unless the job posting satisfies the minimum requirements defined for that stage.

---

### GFR-009. Controlled Recovery

Whenever a recoverable error occurs, the system shall attempt to resolve it according to the defined recovery strategy before requesting user intervention.

---

### GFR-010. User Intervention

Strategic decisions shall only be executed after the user's explicit authorization.

---

### GFR-011. Processing Consistency

Every job posting shall progress through the functional workflow according to the defined lifecycle transitions.

---

### GFR-012. Auditability

Every automated decision shall be justifiable through documented rules.

---

### GFR-013. Centralized Configuration

Business rules, parameters, and configurations shall be managed from a single configuration point.

---

### GFR-014. Modularity

Components shall be designed to minimize dependencies and facilitate maintenance, replacement, and future expansion.

---

### GFR-015. Scalability

The addition of new job sources, business rules, modules, or functionalities shall not require significant modifications to existing components.

---

## 17. Use Case Catalog

The following use cases represent the system's primary functionalities. The detailed specification of each use case shall be documented in a separate document.

### Configuration Management

- UC-001 Configure the system.
- UC-002 Configure job sources.
- UC-003 Configure evaluation rules.
- UC-004 Configure user preferences.

---

### Discovery

- UC-005 Discover new job postings.
- UC-006 Register a job posting.
- UC-007 Detect duplicate job postings.

---

### Preparation

- UC-008 Prepare a job posting.
- UC-009 Normalize information.
- UC-010 Validate information.

---

### Evaluation

- UC-011 Evaluate a job posting.
- UC-012 Classify a job posting.
- UC-013 Discard a job posting.

---

### Deep Processing

- UC-014 Analyze a job posting.
- UC-015 Extract requirements.
- UC-016 Generate analyses.
- UC-017 Generate application resources.

---

### Management

- UC-018 View a job posting.
- UC-019 View history.
- UC-020 View the status of a job posting.
- UC-021 Reprocess a job posting.
- UC-022 Record a user decision.

---

### Administration

- UC-023 View metrics.
- UC-024 View logs.
- UC-025 Manage system configurations.

---

## 18. Functional Constraints

### FC-001

The system shall process only job postings originating from previously configured sources.

---

### FC-002

Every job posting shall have a unique identifier before processing begins.

---

### FC-003

No more than one active processing instance shall exist for the same job posting.

---

### FC-004

No job posting shall advance to the next workflow stage unless it has successfully completed the previous stage, except when a documented rule explicitly allows it.

---

### FC-005

Strategic decisions shall always require the user's explicit authorization.

---

### FC-006

Every automated decision shall be supported by a documented rule.

---

### FC-007

All generated information shall maintain traceability to the job posting from which it originated.

---

### FC-008

The automation shall preserve the complete history of every job posting.

---

### FC-009

Errors shall be recorded before any recovery process begins.

---

### FC-010

The system shall maintain consistency between the lifecycle status and the operational status of every job posting.

---

## 19. Acceptance Criteria

The system shall satisfy the functional requirements when it can be verified that:

### AC-001

It is capable of discovering job postings from the configured sources.

---

### AC-002

It registers every job posting with a unique identifier.

---

### AC-003

It correctly prepares and validates the obtained information.

---

### AC-004

It automatically evaluates job postings using the defined rules.

---

### AC-005

It generates the information required to support the job application process.

---

### AC-006

It keeps both the lifecycle status and the operational status of every job posting up to date.

---

### AC-007

It records every action, decision, and recommendation performed during processing.

---

### AC-008

It requests user intervention whenever a strategic decision is required.

---

### AC-009

It maintains complete traceability for every job posting throughout its entire lifecycle.

---

### AC-010

It allows the system to be extended with new job sources, business rules, and functionalities without affecting the behavior of existing components.
