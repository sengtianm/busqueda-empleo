# Document 11 - Technology Stack

## 1. Purpose of the document

This document defines the official technology stack for the job search automation.

Its purpose is to establish, justify and document the technologies, tools, libraries, frameworks, components and methodologies that will form the technological foundation of the project, ensuring that all technical decisions are consistent with the objectives, scope, requirements and principles defined in the official documentation.

This document constitutes the official reference for the selection of technologies during the design, development, testing, maintenance and evolution of the automation. No technological component may be incorporated into the project without having been previously evaluated according to the criteria established in this document.

The decisions documented here must maintain consistency with Documents 0 through 10, including the functional and non-functional requirements, the decision model, the data flow, the project standards, the error handling model, the folder architecture, the scope and objectives, the job source research and the user's professional profile.

The selected technologies must satisfy the main criteria of the project, prioritizing the use of free tools, a practical, maintainable and scalable architecture, and adequate technological independence that facilitates the future evolution of the solution.

Likewise, this document will serve as the foundation for the preparation of subsequent documents on General System Architecture, Data Model and MVP Development, ensuring that all implementation decisions are supported by a previously analyzed, justified and approved technology stack.

Any modification to the technology stack must be documented, justified and formally approved before being incorporated into the project, preserving traceability and consistency with the rest of the official documentation.

---

## 2. Principles for technology selection

The selection of any technology, tool, library, framework or component that forms part of the automation's technology stack must be carried out according to the principles defined in this chapter.

These principles constitute the official technology evaluation criteria of the project and will be mandatory during the analysis, comparison, selection, replacement or update of any technological component.

Every technology decision must be duly justified through an objective evaluation of these principles, ensuring consistency with the project objectives and with the previously approved official documentation.

The following official principles are established:

### PST-001. Use of free technologies

Only technologies whose use is free of charge for the defined scope of the project will be prioritized.

### PST-002. Compatible licensing

Selected technologies must have licenses that allow their use, modification and distribution according to the project objectives.

### PST-003. Technological maturity

Technologies must be sufficiently consolidated and demonstrate stability for use in real environments.

### PST-004. Stability

Technologies with a history of stable operation and low risk of frequent disruptive changes will be prioritized.

### PST-005. Community and ecosystem

Technologies must have an active community that facilitates support, evolution and availability of technical resources.

### PST-006. Documentation quality

They must have complete, up-to-date and sufficient official documentation to facilitate their implementation and maintenance.

### PST-007. Compatibility

Technologies must integrate correctly with the rest of the selected technology stack.

### PST-008. Modularity

They should favor a modular architecture that facilitates the isolation of responsibilities and the reuse of components.

### PST-009. Scalability

Technologies must allow the functional and technical growth of the automation without requiring significant redesigns.

### PST-010. Maintainability

Selected solutions should facilitate the understanding, updating and maintenance of the system in the long term.

### PST-011. Performance

They must offer adequate performance for the workloads planned in the project.

### PST-012. Security

Technologies must incorporate mechanisms that favor the development of secure and reliable solutions.

### PST-013. Portability

Technologies that allow the solution to run in different environments with the least possible effort will be prioritized.

### PST-014. Technological independence

Whenever feasible, unnecessary dependencies on specific vendors, platforms or services will be avoided.

### PST-015. Ease of integration

Technologies must integrate easily with the internal and external components of the automation.

### PST-016. Sustainable updating

Technologies should present an evolution cycle that allows updating the system without significantly affecting its stability.

### PST-017. Efficient resource consumption

Technologies that efficiently use available hardware resources will be prioritized.

### PST-018. Ease of testing

Technologies should facilitate the implementation of automated tests and validation processes.

### PST-019. Compatibility with artificial intelligence

They must integrate adequately with the language models and other artificial intelligence components used by the automation.

### PST-020. Compatibility with web automation

Technologies must allow robust automation of navigation, extraction and interaction processes with web platforms.

### PST-021. Learning curve

Technologies whose adoption complexity is reasonable to facilitate future maintenance of the project will be valued.

### PST-022. Obsolescence risk

Technologies with favorable prospects for continuity, maintenance and evolution within the industry will be prioritized.

All principles defined in this chapter are mandatory and will serve as the basis for the comparative evaluation of the technological alternatives analyzed in subsequent chapters of this document.

---

## 3. Technology evaluation criteria

The selection of any technology, tool, library, framework or component of the technology stack must be carried out through an objective, uniform, reproducible and documented evaluation process.

All technological alternatives must be evaluated using the methodology defined in this chapter, with the purpose of ensuring that the decisions made are technically justifiable, consistent with the principles established in this document and aligned with the general objectives of the project.

The official technology evaluation of the project will consist of two mandatory stages: the evaluation of elimination criteria and the evaluation of scoring criteria.

---

### 3.1. Evaluation of elimination criteria

Elimination criteria correspond to those principles whose non-compliance makes a technology incompatible with the objectives, restrictions or requirements of the project.

Every technology must meet all of these criteria to continue the evaluation process.

Non-compliance with any of them will imply the immediate discard of the evaluated alternative, regardless of the advantages it may present in other aspects.

The official elimination criteria are as follows:

| Code | Principle |
|-------|-----------|
| PST-001 | Use of free technologies |
| PST-002 | Compatible licensing |
| PST-007 | Compatibility with the rest of the technology stack |
| PST-012 | Security |
| PST-015 | Ease of integration |
| PST-019 | Compatibility with artificial intelligence (when applicable) |
| PST-020 | Compatibility with web automation (when applicable) |

---

### 3.2. Evaluation of scoring criteria

Technologies that pass the previous stage will be evaluated using a weighted scoring system.

Each criterion will receive a weight proportional to its importance within the project.

Subsequently, each technology will be rated against each criterion, obtaining a total score that will allow objective comparisons between different alternatives.

The official scoring criteria are as follows:

| Code | Principle |
|-------|-----------|
| PST-003 | Technological maturity |
| PST-004 | Stability |
| PST-005 | Community and ecosystem |
| PST-006 | Documentation quality |
| PST-008 | Modularity |
| PST-009 | Scalability |
| PST-010 | Maintainability |
| PST-011 | Performance |
| PST-013 | Portability |
| PST-014 | Technological independence |
| PST-016 | Sustainable updating |
| PST-017 | Efficient resource consumption |
| PST-018 | Ease of testing |
| PST-021 | Learning curve |
| PST-022 | Obsolescence risk |

---

### 3.3. Evaluation principles

Every technology evaluation must comply with the following principles:

- Objectivity.
- Uniformity.
- Traceability.
- Transparency.
- Reproducibility.
- Comparability.
- Documentary justification.

No technology may be selected based on subjective criteria or personal preferences.

---

### 3.4. Official technology evaluation matrix

Every technology decision must be supported by an official evaluation matrix that documents, at a minimum:

- Technologies evaluated.
- Elimination criteria applied.
- Result of each elimination criterion.
- Scoring criteria considered.
- Weight assigned to each criterion.
- Score obtained by each alternative.
- Total score obtained.
- Technical justification of the decision made.

The evaluation matrix will constitute the official documentary support for all technology decisions recorded in this document.

---

### 3.5. Decision rules

The selection of a technology must simultaneously meet the following conditions:

1. Pass all elimination criteria.
2. Obtain the highest weighted score among the evaluated alternatives.
3. Not contradict any official project document.
4. Not breach the functional requirements nor the non-functional requirements.
5. Maintain consistency with the general architecture defined for the automation.

---

### 3.6. Technology reassessment

When a technology is replaced, updated or incorporated into the project, a new evaluation must be carried out using exactly this same methodology.

Every reassessment must be formally documented to preserve the historical traceability of the project's technology decisions.

### 3.7. Official scoring scale

In order to guarantee the uniformity of all technology evaluations carried out within the project, the following official scoring scale for the scoring criteria is adopted.

| Score | Interpretation |
|-------|---------------|
| 0 | Does not meet the criterion. |
| 1 | Very poor compliance. |
| 2 | Poor compliance. |
| 3 | Acceptable compliance. |
| 4 | High compliance. |
| 5 | Excellent compliance. |

All evaluated technologies must be rated using exclusively this scale.

Different scales are not allowed within this document.

---

### 3.8. Official criteria weighting

The scoring criteria will have a relative weight that reflects their importance to the project.

The official weighting is as follows:

| Code | Criterion | Weight (%) |
|-------|-----------|----------:|
| PST-003 | Technological maturity | 8 |
| PST-004 | Stability | 8 |
| PST-005 | Community and ecosystem | 8 |
| PST-006 | Documentation quality | 8 |
| PST-008 | Modularity | 7 |
| PST-009 | Scalability | 10 |
| PST-010 | Maintainability | 10 |
| PST-011 | Performance | 7 |
| PST-013 | Portability | 5 |
| PST-014 | Technological independence | 6 |
| PST-016 | Sustainable updating | 5 |
| PST-017 | Efficient resource consumption | 5 |
| PST-018 | Ease of testing | 6 |
| PST-021 | Learning curve | 2 |
| PST-022 | Obsolescence risk | 5 |

The sum of all weights must always equal 100%.

The final score of each technological alternative will be calculated by applying these weights to the score obtained in each scoring criterion.

---

### 3.9. Calculation of the final score

The final score of a technology will be obtained by adding the weighted scores of all scoring criteria, once it has successfully passed the evaluation of the elimination criteria.

This score will constitute the official reference for comparing technological alternatives within the project.

The selection of a technology will not depend exclusively on its final score, but also on compliance with the elimination criteria and the decision rules established in this document.


---

## 4. General technological architecture

The technological architecture of the automation defines the way in which the technical components of the system will be organized to ensure compliance with the objectives, requirements and principles established in the project's official documentation.

Its purpose is to provide a coherent, maintainable, scalable and decoupled technological structure that serves as the basis for the selection of technologies and for the development of all automation modules.

The architecture defined in this document constitutes the official model that all technological components incorporated into the project must respect.

---

### 4.1. Architectural model

The automation adopts a **hybrid architecture**, composed of the integration of several complementary architectural patterns, selected according to the specific characteristics and needs of the project.

This architecture combines the following approaches:

- Modular architecture.
- Internal layer organization.
- Sequential processing flow.
- Shared services.
- Centralized persistence.

The combination of these patterns allows leveraging the strengths of each without introducing unnecessary complexity.

---

### 4.2. Modular architecture

The solution will be divided into independent functional modules, each responsible for a specific stage of the offer processing flow.

Each module will have a single responsibility and may evolve independently as long as it respects the interfaces and contracts defined by the architecture.

---

### 4.3. Internal layer organization

Each module must internally organize its components through a clear separation of responsibilities.

As a general principle, there must be separation between:

- Business logic.
- Data access.
- Integration with external services.
- Configuration.
- Infrastructure components.

This organization seeks to reduce internal coupling and facilitate system maintenance.

---

### 4.4. Sequential processing flow

The architecture will respect the official processing flow defined for the automation.

Each module will receive an offer in a given state, execute exclusively the operations corresponding to its responsibility and deliver the result to the next module in the flow.

Dependencies that alter the official processing order are not allowed.

---

### 4.5. Shared services

Common functionalities of the automation must be implemented as reusable services accessible by the different modules of the system.

These services may include, among others:

- Configuration.
- Persistence.
- State management.
- Event logging.
- Error handling.
- Artificial intelligence.
- Prompt management.
- Common utilities.

Reuse of these components should avoid duplication of responsibilities within the architecture.

---

### 4.6. Centralized persistence

All official project information must be maintained in a single persistence source shared by authorized modules.

The architecture must guarantee the consistency, traceability and integrity of information throughout the entire lifecycle of processed offers.

Parallel repositories that compromise data integrity are not allowed.

---

### 4.7. Principles of the technological architecture

The technological architecture must permanently preserve the following principles:

- Modularity.
- Low coupling.
- High cohesion.
- Scalability.
- Maintainability.
- Component reuse.
- Separation of responsibilities.
- Data consistency.
- Traceability.
- Controlled evolution.

---

### 4.8. Architectural evolution

Every incorporation, replacement or modification of technological components must respect the architecture defined in this document.

Any structural change must be documented, justified and approved before its implementation, ensuring compatibility with the rest of the system and with the official project documentation.

---

## 5. Programming language

### 5.1. Objective

The programming language constitutes the technological foundation on which the entire automation will be developed.

Its selection must guarantee compatibility with the technological architecture defined in this document, as well as satisfy the functional requirements, non-functional requirements and the official evaluation criteria established for the project.

---

### 5.2. Evaluated alternatives

For the selection of the programming language, the following alternatives were evaluated:

- Python
- Node.js (JavaScript/TypeScript)
- C#
- Java
- Go

The other alternatives were discarded for not offering relevant technical advantages for the specific objectives of the automation.

---

### 5.3. Technical evaluation

The alternatives were analyzed considering, among others, the following aspects:

- Compatibility with web automation.
- Integration with artificial intelligence models.
- Library ecosystem.
- Data processing.
- Technological maturity.
- Community and documentation.
- Ease of maintenance.
- Scalability.
- Compatibility with the project architecture.

As a result of the analysis, Python obtained the best overall evaluation by offering the greatest compatibility with the objectives and needs of the automation.

---

### 5.4. Selected language

**Python 3.12** is established as the official programming language of the project.

Python will be used for the development of all functional modules, shared components, automation processes, integration with artificial intelligence, data processing and other elements that make up the solution.

---

### 5.5. Justification of the decision

The selection of Python is based on the following factors:

- Excellent compatibility with web automation processes.
- Mature and widely consolidated ecosystem for integration with artificial intelligence models.
- Wide availability of libraries for data processing.
- Excellent official documentation and development community.
- High level of maintainability.
- Great technological stability.
- Compatibility with modular architectures.
- Low obsolescence risk.
- Compatibility with the technology criteria defined in this document.

The evaluation carried out concludes that Python represents the alternative with the best balance between functionality, maintainability, scalability and ease of evolution for the project objectives.

---

### 5.6. Scope of the decision

This decision will be applicable to all developments that form part of the automation.

The incorporation of components implemented in other languages may only be carried out when there is a duly documented and approved technical justification according to the evaluation methodology defined in this document.

---

# 6. Main libraries and dependencies

## 6.1 Objective

To define the main libraries that will form part of the core of the automation, establishing those dependencies that provide essential functionality and that cannot be adequately replaced by the Python standard library or by another technology already adopted within the stack.

The selected libraries must be actively maintained, compatible with the rest of the technology stack and provide a real technical benefit to the project.

---

## 6.2 Selection criteria

Every library incorporated into the project must meet, at a minimum, the following criteria:

- Solve a real need of the automation.
- Provide a technical benefit over the Python standard library.
- Not duplicate functionality already covered by another technology in the stack.
- Have active maintenance and a consolidated community.
- Be stable and widely used in production projects.
- Integrate correctly with the rest of the selected technologies.
- Keep the project complexity to a minimum.

Dependencies will not be incorporated solely for convenience, popularity or for offering functionalities that will not be used by the automation.

---

## 6.3 Official libraries

### BeautifulSoup4

**BeautifulSoup4** is adopted as the official library for processing and analyzing HTML code obtained during automation.

Its responsibility will be to interpret the DOM structure and facilitate organized information extraction.

---

### lxml

**lxml** is adopted as the official parser used by BeautifulSoup4.

Its use will improve performance during HTML processing without modifying the work interface provided by BeautifulSoup4.

---

### Pydantic v2

**Pydantic v2** is adopted as the official library for defining, validating, serializing and deserializing all data models used by the automation.

All information exchanged between modules must be represented using Pydantic models.

---

### Loguru

**Loguru** is adopted as the official library for the event logging, traceability and audit system of the automation.

All operational logging must be carried out using this library.

---

### RapidFuzz

**RapidFuzz** is adopted as the official library for performing approximate text comparisons and string similarity calculations when such operations can be resolved using deterministic algorithms.

---

### Tenacity

**Tenacity** is adopted as the official library for implementing retry policies on operations that interact with potentially unstable external resources.

Its use will allow centralizing the recovery strategy against temporary errors.

---

### httpx

**httpx** is adopted as the official library for making HTTP requests when such operations do not require the use of the automated browser.

Its selection guarantees compatibility with synchronous and asynchronous architectures.

---

## 6.4 Python standard library

In addition to the above libraries, the automation will use components from the Python standard library when they are sufficient to solve a specific need.

Among them are:

- pathlib
- re
- json
- hashlib
- datetime
- time
- sqlite3

Other standard library libraries may be used when there is a justified technical need, without this implying modifying the official technology stack.

---

## 6.5 Discarded libraries

During the technology evaluation, different alternatives were analyzed that were ultimately not incorporated into the project because they did not provide sufficient technical benefit or duplicated functionality already covered by other selected technologies.

Among them are:

- requests
- spaCy
- NLTK
- Stanza
- jsonschema

These technologies may be re-evaluated only if a functional requirement arises in the future that justifies their incorporation.

---

## 6.6 Principles of use

Official libraries must be used respecting the following principles:

- Each library will have a single clearly defined responsibility.
- Dependencies that duplicate existing functionality are not allowed.
- The Python standard library will always be prioritized when it adequately covers the need.
- Every new dependency must be evaluated according to the criteria defined in this document before being incorporated into the project.

---

# 7. Frameworks

## 7.1 Objective

To define whether the automation requires the adoption of one or more frameworks as part of the official technology stack.

The incorporation of a framework will only be accepted when it provides a real technical benefit that cannot be obtained through the programming language, the defined architecture or the official libraries of the project.

---

## 7.2 Evaluation

During the research, different framework alternatives for Python were analyzed, including automation, web development and scraping frameworks.

As a result of the analysis, it was concluded that the project architecture does not require the incorporation of any framework.

The necessary functionalities will be covered by:

- Python as the programming language.
- Custom modular architecture.
- Official libraries defined in this document.
- Playwright for browser automation.
- Ollama as the inference engine for artificial intelligence.

Adopting a framework would introduce additional complexity without providing a significant technical benefit for the project objectives.

---

## 7.3 Decision

The project **will not adopt any framework** as part of the official technology stack.

The automation will be developed using a modular architecture implemented directly on Python and the selected official libraries.

---

## 7.4 Justification

This decision is based on the following criteria:

- The defined architecture does not require the functionalities provided by a framework.
- Incorporating a framework would increase the project complexity without offering proportional advantages.
- Greater control over the architecture and evolution of the system is maintained.
- The number of external dependencies is reduced.
- Code maintenance and understanding is facilitated.

---

## 7.5 Scope

If a functional requirement arises in the future that justifies the incorporation of a framework, such decision must again undergo the technology evaluation process defined in this document before becoming part of the official stack.

---

# 8. Browser automation

## 8.1 Objective

To define the official technology responsible for browser automation to carry out interaction with job portals during all stages of discovery, collection and processing of offers.

---

## 8.2 Need

The automation requires interacting with modern web applications that use dynamic content, authentication, JavaScript and various asynchronous loading mechanisms.

Among the operations that the browser will perform are:

- Access job portals.
- Perform searches.
- Apply filters.
- Navigate through results.
- Manage user sessions when necessary.
- Extract information from offers.
- Download files when applicable.
- Obtain the HTML code for subsequent processing.

These needs require a robust automation tool compatible with modern web applications.

---

## 8.3 Evaluated technologies

During the technology research, the following alternatives were evaluated:

- Selenium.
- Playwright.
- Puppeteer.

After the technical analysis, it was concluded that Playwright represents the most suitable alternative for the objectives and architecture of the project.

---

## 8.4 Selected technology

**Playwright** is adopted as the official technology for browser automation.

---

## 8.5 Technical justification

The selection of Playwright is based on the following aspects:

- Excellent compatibility with modern web applications.
- Native support for Chromium, Firefox and WebKit.
- Automatic wait management during navigation.
- Modern and actively maintained API.
- Excellent integration with Python.
- High stability during prolonged automation processes.
- Excellent documentation and widespread community adoption.

The evaluation carried out did not identify sufficient technical advantages in Selenium or Puppeteer to justify their incorporation into the project.

---

## 8.6 Scope

Playwright will be exclusively responsible for browser automation.

Among its responsibilities are:

- Browser control.
- Navigation between pages.
- Interaction with interface elements.
- Session management.
- Obtaining HTML content.
- Screenshots when necessary.
- File download.

Processing of the obtained HTML will be the responsibility of BeautifulSoup4 using lxml as parser, according to the decisions defined in the technology stack.

---

## 8.7 Restrictions

All browser automation must be performed using Playwright.

No additional browser automation technologies will be incorporated while Playwright covers the functional requirements of the project.

Any future replacement must undergo the technology evaluation process defined in this document.

---

# 9. Artificial intelligence (LLM)

## 9.1 Objective

To define the architecture, technologies and official criteria for the incorporation of artificial intelligence through Large Language Models (LLMs), which will be responsible for the analysis, interpretation and generation of content within the automation.

---

## 9.2 Need

The automation requires reasoning capabilities that cannot be solved solely by deterministic rules or traditional algorithms.

The language model will be responsible for tasks such as:

- Analyzing job offers.
- Interpreting technical and functional requirements.
- Extracting relevant information.
- Evaluating compatibility between offers and the professional profile.
- Generating diagnostics and recommendations.
- Writing professional documents.
- Responding following instructions defined through structured prompts.

---

## 9.3 Artificial intelligence strategy

The project adopts a cloud-primary strategy: all AI purposes route to the cloud model via Ollama Cloud (free plan), through a local proxy. A local model is available as an optional, configurable fallback for development and for scenarios where the cloud is unreachable.

> **Decision 2026-07-30 (Phase 3):** `ai_routing: evaluation=cloud, processing=cloud` is the official configuration. The offline requirement of previous versions of this document is superseded by a configurable fallback (`ai_routing` in `config.yaml`).

This decision balances:

- Superior quality where it matters most (cloud).
- Zero recurring cost through the free plan.
- Simple operation (single provider, no local hardware requirements).
- Configurable local fallback to mitigate free-plan limits (usage caps, availability, term changes).

---

## 9.4 Inference engines

The project adopts two inference engines according to purpose:

### 9.4.1 Local engine

**Ollama** is adopted as the local engine for running language models in high-volume tasks.

The selection of Ollama as the local engine is based on:

- Completely local execution.
- Simple installation and administration.
- Excellent integration with Python.
- Wide catalog of compatible models.
- Active maintenance.
- Excellent documentation.

### 9.4.2 Cloud engine

**Ollama Cloud** is adopted as the cloud engine for tasks requiring greater reasoning capacity.

The selection of Ollama Cloud is based on:

- Access to large-scale models without requiring local hardware.
- Free plan with high-capacity models.
- Same API interface as local Ollama, facilitating integration.
- No operating costs for the free plan.

---

## 9.5 Integration architecture

The automation will not access the language model directly.

All communication with the LLM must be carried out through an internal AI Service that will act as the single access point to the inference engines.

This service will be responsible for:

- Managing communication with AI providers (local and cloud).
- Routing each request to the appropriate provider according to purpose.
- Centralizing prompt management.
- Validating requests and responses.
- Managing errors and retries.
- Decoupling the rest of the architecture from the model used.

Routing is defined through the `ai_routing` section in `config.yaml`, where each purpose (`evaluation`, `processing`) is assigned to the corresponding provider (`cloud` or `local`).

This strategy will allow replacing or rebalancing models and providers without modifying the functional modules of the automation.

---

## 9.6 Model usage strategy

The language model will be used only for tasks requiring understanding, reasoning or content generation.

Deterministic operations will continue to be solved using traditional algorithms and specialized libraries.

This separation avoids using the LLM for tasks where it does not provide a technical benefit.

---

## 9.7 Model selection

The project uses two models according to purpose and available hardware:

### 9.7.1 Local model (optional fallback)

- **Family:** Qwen.
- **Model:** Qwen 3.5 4B (`qwen3.5:4b`).
- **Target hardware:** GPU with 4 GB VRAM (NVIDIA GTX 1650 Mobile).
- **Role:** optional fallback for development or when the cloud route is unavailable.

The selection is based on:

- Good instruction following.
- Good performance in Spanish and English.
- Sufficient capacity for classification and basic analysis.
- Fits completely in 4 GB VRAM, ensuring speed.
- Compatibility with Ollama.

### 9.7.2 Cloud model

- **Model:** Gemma 4 31B.
- **Provider:** Ollama Cloud (free plan).

The selection is based on:

- High performance in reasoning and text generation.
- Excellent quality in Spanish and English.
- Capacity for deep analysis and professional writing.
- Free access through Ollama Cloud free plan.

---

## 9.8 Model evolution

The models defined in this document correspond to the initial selection of the project.

The architecture will allow replacing any of the models in the future provided that:

- There is technical evidence justifying the change.
- The new model meets the admission criteria defined by the project.
- It passes the official technology evaluation process.
- Its incorporation does not affect the general architecture of the automation.

The separation by purpose (local/cloud) facilitates the independent evolution of each model without affecting the other.

---

## 9.9 Scope

The language model will be used for:

- Interpretation of offers.
- Intelligent information extraction.
- Compatibility evaluation.
- Professional content generation.
- Classification and reasoning.
- Decision support within the processing flow.

It will not be used for deterministic tasks that can be solved using traditional algorithms.

---

## 9.10 Restrictions

The artificial intelligence of the project must comply with the following restrictions:

- The local model must run via Ollama (when the local fallback is used).
- The cloud model must be accessible via a free plan, with no recurring costs.
- The routing between models must be transparent to the functional modules.
- All communication must be carried out exclusively through the AI Service defined by the architecture.
- The initial evaluation flow (module 3) must be able to work with the cloud route or, if unreachable, through a configurable local fallback.
- The models must be replaceable in the future without modifying the business logic of the automation.

---

# 10. Database

## 10.1 Objective

To define the official persistent storage system of the automation, ensuring that information can be stored, queried, updated and maintained in a simple, robust, queryable and completely local manner.

---

## 10.2 Need

The automation requires persistently storing the information generated during its operation.

Among the data that must be preserved are:

- Job offers.
- Companies.
- Offer sources.
- Locations.
- Processed offers.
- Evaluation results.
- Processing status.
- Execution history.
- Information necessary for the operation of the automation.

The storage should facilitate both automatic access by the system and manual querying and editing by the user when necessary.

---

## 10.3 Evaluated technologies

During the research, the following alternatives were evaluated:

- SQLite.
- Google Sheets.
- Local spreadsheet.

Initially, a local spreadsheet was selected. Subsequently, during MVP development, it was migrated to SQLite to leverage its structured query capability, referential integrity and superior performance.

---

## 10.4 Selected technology

**SQLite** (included in the Python standard library via `sqlite3`) is adopted as the official database management system.

It requires no external libraries or additional installation.

---

## 10.5 Technical justification

The selection of SQLite is based on the following aspects:

- It is part of the Python standard library (`sqlite3` module).
- It does not require installing or administering an external database management system.
- All information remains stored locally in a single file.
- It supports referential integrity, transactions, SQL queries and normalized schemas.
- It allows querying and modifying information using free tools such as DB Browser for SQLite.
- It offers better performance than a spreadsheet for medium data volumes.
- It allows structured queries (filters, joins, searches) without loading the entire database into memory.
- The `.db` file is portable and maintainable without depending on office software.

---

## 10.6 Information organization

The database is organized into normalized tables, each with its unique sequential identifier and audit fields (`fecha_creacion`, `fecha_actualizacion`).

The official tables are:

| Table | ID Prefix | Purpose |
|-------|-----------|---------|
| `fuentes` | FNT | Offer sources (LinkedIn, etc.) |
| `empresas` | EMP | Employing companies |
| `ubicaciones` | UBI | Geographic locations |
| `ofertas` | OFE | Raw job offers |
| `ofertas_procesadas` | OFP | Processed and cleaned offers |
| `evaluaciones` | EVL | Evaluation results |
| `resultados_procesamiento` | RSP | Deep processing results |

There is also the internal table `secuencia_ids` that manages counters to generate sequential identifiers with the format `{PREFIX}-{NUMBER:04d}` (e.g. `EMP-0001`, `OFE-0042`).

---

## 10.7 Data access

All reading and writing to the database must be performed exclusively through the shared service `shared/persistence.py`.

Functional modules are not allowed to execute SQL directly.

This separation reduces coupling and facilitates future modifications to the storage system if necessary.

---

## 10.8 Compatibility

The database file (`data/job_search.db`) is compatible with:

- Python (`sqlite3` module).
- DB Browser for SQLite (free graphical tool).

---

## 10.9 Restrictions

The persistent storage of the project must comply with the following restrictions:

- Remain completely local.
- Use SQLite as the database engine.
- Manage access exclusively through `shared/persistence.py`.
- Not depend on external services or remote management systems.

---

# 11. Configuration management and environment variables

## 11.1 Objective

To define the official mechanism for managing the automation configuration and environment-dependent variables, ensuring a clear separation between system configuration and source code.

---

## 11.2 Need

The automation requires storing configuration parameters that may be modified during the project's lifespan without needing to make changes to the code.

Among them are:

- Working directories.
- Main database path.
- Resume location.
- Professional portfolio location.
- Generated documents directory.
- AI model configuration.
- Browser configuration.
- General operating parameters.

The separation between configuration and code facilitates maintenance, portability and reuse of the automation.

---

## 11.3 Configuration strategy

The project configuration will be divided into two independent components:

### Functional configuration

Corresponds to the parameters that define the behavior of the automation.

It will be stored in a file:

**config.yaml**

---

### Environment variables

Correspond to the specific information of the machine where the automation runs.

They will be stored in a file:

**.env**

---

## 11.4 config.yaml file

The `config.yaml` file will contain the functional configuration of the project.

Among other aspects, it may store:

- General configuration.
- Processing parameters.
- Browser configuration.
- AI model configuration.
- Processing limits.
- Evaluation parameters.
- Module configuration.

Its content will be organized hierarchically to facilitate maintenance and reading.

---

## 11.5 .env file

The `.env` file will contain only information dependent on the execution environment.

Among other aspects, it may store:

- Local paths.
- Working directories.
- Ollama location.
- Database path.
- Machine-specific variables.

This file will allow moving the automation to another computer by modifying only the environment configuration, without altering the source code or the functional configuration.

---

## 11.6 Selected technologies

The following technologies are adopted as part of the official stack:

### PyYAML

It will be the official library for reading and writing the `config.yaml` file.

---

### python-dotenv

It will be the official library for loading variables defined in the `.env` file.

---

## 11.7 Principles of use

Configuration management must comply with the following principles:

- The source code will not contain modifiable configuration values.
- All functional configuration must be stored in `config.yaml`.
- All machine-dependent configuration must be stored in `.env`.
- The configuration must be loaded automatically during automation startup.
- Modules will access the configuration through the mechanisms defined by the project architecture.

---

## 11.8 Restrictions

Configuration management must comply with the following restrictions:

- Do not store configuration information directly in the code.
- Keep functional configuration and environment variables separate.
- Use exclusively `config.yaml` and `.env` as official configuration mechanisms.
- Ensure that the automation can be moved to another machine by modifying only the configuration files.

---

# 12. Dependency management

## 12.1 Objective

To define the official mechanism for installing, updating and managing the dependencies used by the automation, ensuring a reproducible, stable and easy-to-maintain development environment.

---

## 12.2 Need

The automation will use various external libraries to implement its functionalities.

A mechanism is needed that allows:

- Installing all project dependencies.
- Maintaining compatible versions between them.
- Reproducing the development environment at any time.
- Facilitating future updates.
- Reducing problems derived from version incompatibilities.

---

## 12.3 Evaluated technologies

During the technology evaluation, the following alternatives were analyzed:

- pip
- Poetry
- uv

After the technical analysis, it was concluded that `pip` represents the most suitable alternative for the project needs.

---

## 12.4 Selected technology

**pip** is adopted as the official dependency manager of the automation.

The file used as the official dependency inventory is:

**requirements.txt**

---

## 12.5 Technical justification

The selection of `pip` is based on the following aspects:

- It is part of the official Python ecosystem.
- Excellent stability.
- Extensive documentation.
- Compatibility with all libraries selected for the project.
- Simplicity of use.
- Does not introduce unnecessary complexity.

The evaluated alternatives offer additional functionalities that do not represent a significant benefit for the defined architecture.

---

## 12.6 requirements.txt file

The `requirements.txt` file will constitute the official dependency inventory of the project.

It will record all external libraries approved as part of the technology stack, indicating their corresponding versions to guarantee environment reproducibility.

Libraries from the Python standard library should not be included.

The requirements.txt file will also constitute the official reference for the versions of the dependencies used by the project. In case of differences between this document and the requirements.txt file, the versions recorded in the latter shall prevail.

---

## 12.7 Version management

Dependency versions must be kept under control to avoid incompatibilities between system components.

Every incorporation, update or removal of a dependency must be immediately reflected in the `requirements.txt` file.

---

## 12.8 Restrictions

Dependency management must comply with the following restrictions:

- Use exclusively `pip` as the official manager.
- Keep the `requirements.txt` file updated.
- Do not incorporate dependencies that have not been previously evaluated and approved.
- Avoid duplication of functionalities between libraries.
- Always prioritize the Python standard library when it adequately covers a project need.

---

# 13. Development tools

## 13.1 Objective

To define the official tools that will be used during the development, debugging and maintenance of the automation, ensuring a stable, simple work environment compatible with the technology stack defined for the project.

---

## 13.2 Need

The development of the automation requires tools that facilitate:

- Source code editing.
- Development environment administration.
- Application debugging.
- Code quality validation.
- Static type checking verification.

The selection of these tools should prioritize simplicity, stability and integration with the rest of the technology stack.

---

## 13.3 Evaluated technologies

During the technology evaluation, different tools commonly used for Python development were analyzed.

As a result of the analysis, only those that provide a real technical benefit to the project were selected.

---

## 13.4 Code editor

**Visual Studio Code** is adopted as the official development environment.

The selection is based on:

- Python compatibility.
- Excellent integration with Git.
- Wide extension ecosystem.
- Integrated debugging tools.
- Stability.
- Free availability.

---

## 13.5 Virtual environment

**venv** is adopted as the official mechanism for creating and managing virtual environments.

As it is part of the Python standard library, it requires no additional dependencies and fully covers the project needs.

---

## 13.6 Code formatting

**Black** is adopted as the official tool for automatic source code formatting.

Its use will ensure a uniform style throughout the development of the automation.

---

## 13.7 Static analysis

**Ruff** is adopted as the official tool for static code analysis.

Its use will allow detecting potential errors, quality issues and deviations from good development practices before program execution.

---

## 13.8 Type checking

**mypy** is adopted as the official tool for static type checking of the project.

Its use will complement the validation performed by Pydantic, detecting inconsistencies during development.

---

## 13.9 Principles of use

Development tools must be used following the following principles:

- Maintain a uniform code style.
- Detect errors as early as possible during development.
- Reduce maintenance complexity.
- Favor code readability and consistency.
- Integrate correctly with the rest of the technology stack.

---

## 13.10 Restrictions

Development tools must comply with the following restrictions:

- Be free.
- Maintain compatibility with Python and the official technology stack.
- Not duplicate functionality already covered by other tools.
- Be incorporated only when they provide a demonstrable technical benefit to the project.

---

# 14. Testing tools

## 14.1 Objective

To define the official tools for carrying out tests during the development of the automation, in order to verify the correct operation of its components and reduce the risk of introducing errors during the project evolution.

---

## 14.2 Need

The automation will be composed of multiple independent modules that will evolve progressively.

It will be necessary to verify that new functionalities do not affect the behavior of previously developed components and that the results obtained are consistent with the project requirements.

---

## 14.3 Evaluated technologies

During the technology evaluation, the following alternatives were analyzed:

- unittest
- pytest

After the technical analysis, it was concluded that **pytest** represents the most suitable alternative for the project needs.

---

## 14.4 Selected technology

**pytest** is adopted as the official tool for executing automated tests in the project.

---

## 14.5 Technical justification

The selection of pytest is based on the following aspects:

- Simple and easy-to-maintain syntax.
- Excellent documentation.
- Wide adoption within the Python ecosystem.
- Great flexibility for different types of tests.
- Excellent integration with Visual Studio Code.
- Possibility of extending its capabilities through plugins when necessary.

---

## 14.6 Scope

Automated tests may be used to verify, among other aspects:

- Operation of individual modules.
- Integration between components.
- Data processing.
- Validation of business rules.
- Correct functioning of critical functions.

The implementation of tests will be carried out when the complexity or impact of the component justifies it.

---

## 14.7 Principles of use

Tests must comply with the following principles:

- Verify the expected behavior of the system.
- Be reproducible.
- Maintain independence from each other.
- Facilitate early detection of errors.
- Evolve together with the source code.

---

## 14.8 Restrictions

Testing tools must comply with the following restrictions:

- Be compatible with the official technology stack.
- Stay updated.
- Not introduce unnecessary complexity.
- Be used mainly to validate components whose criticality justifies the existence of automated tests.

---

# 15. Documentation tools

## 15.1 Objective

To define the format and official tools for creating, maintaining and updating the project documentation, ensuring that all technical and functional information remains organized, consistent and easily consultable throughout the entire lifecycle of the automation.

---

## 15.2 Need

The automation requires structured documentation that allows:

- Recording the technical decisions of the project.
- Documenting the architecture.
- Maintaining functional specifications.
- Documenting the developed modules.
- Recording installation, configuration and maintenance procedures.
- Facilitating the future evolution of the project.

---

## 15.3 Evaluated technologies

During the technology evaluation, the following alternatives were analyzed:

- Markdown (.md)
- MkDocs
- Sphinx

After the technical analysis, it was concluded that **Markdown** represents the most suitable alternative for the project needs.

---

## 15.4 Selected technology

**Markdown (.md)** is adopted as the official format for all technical and functional documentation of the project.

---

## 15.5 Technical justification

The selection of Markdown is based on the following aspects:

- Open and widely adopted format.
- Excellent readability in both editable and rendered format.
- Native integration with Git.
- Compatibility with Visual Studio Code.
- Low maintenance.
- No additional tools required for its use.
- Facilitates versioning of documentation along with source code.

The evaluated alternatives incorporate functionalities mainly oriented to automatic generation of documentation sites, which do not represent a need for this project.

---

## 15.6 Documentation organization

All official project documentation must be kept organized following the document structure defined for the automation.

Each document should address a specific topic and remain updated as the project evolves.

---

## 15.7 Principles of use

Documentation must comply with the following principles:

- Maintain consistency with the project implementation.
- Be updated when relevant changes are approved.
- Remain organized and structured.
- Avoid duplication of information.
- Be clear, precise and easily consultable.

---

## 15.8 Restrictions

Documentation tools must comply with the following restrictions:

- Use Markdown as the official format.
- Maintain compatibility with Visual Studio Code and Git.
- Not incorporate additional automatic documentation generation tools while there is no functional requirement that justifies it.

---

# 16. Version control tools

## 16.1 Objective

To define the official tools for version control of the source code and project documentation, ensuring traceability of changes, recovery of previous versions and organized evolution of the automation.

---

## 16.2 Need

The project will evolve progressively through the incorporation of new functionalities, corrections and improvements.

It is necessary to have a mechanism that allows:

- Recording the change history.
- Recovering previous versions.
- Maintaining the integrity of the project.
- Facilitating the safe development of new functionalities.
- Versioning both the code and the official documentation.

---

## 16.3 Evaluated technologies

During the technology evaluation, the following alternatives were analyzed:

- Git.
- Manual version administration.

After the technical analysis, it was concluded that **Git** represents the most suitable alternative for the project needs.

---

## 16.4 Selected technology

**Git** is adopted as the official version control system of the project.

Initially, the repository will be managed locally on the machine where the automation is developed.

---

## 16.5 Technical justification

The selection of Git is based on the following aspects:

- It is the industry standard for version control.
- It allows maintaining a complete history of the project.
- It facilitates the recovery of previous versions.
- It integrates correctly with Visual Studio Code.
- It allows versioning code and documentation together.
- It does not require external services to function.

---

## 16.6 Scope

Git will be used to version:

- Source code.
- Technical documentation.
- Configuration files.
- Resources necessary for the development of the project.

It will not be used to store automatically generated files or temporary information.

---

## 16.7 Principles of use

Version management must comply with the following principles:

- Record changes in an organized manner.
- Maintain a clear development history.
- Make commits only when changes are functionally stable.
- Keep code and documentation synchronized.

---

## 16.8 Restrictions

Version control must comply with the following restrictions:

- Use Git as the only official version control system.
- Keep the repository updated throughout the entire project development.
- Not depend on remote platforms for the functioning of the version control system.

---

# 17. Auxiliary tools

## 17.1 Objective

To define the complementary tools that will support the development, execution and maintenance of the automation, without being directly part of the source code or the main stack of the project.

---

## 17.2 Need

During the development and use of the automation, it will be necessary to have tools that facilitate certain operational activities without affecting the system architecture.

These tools should complement the operation of the automation and provide a practical benefit to the user.

---

## 17.3 Selected technology

**ONLYOFFICE** is adopted as the official tool for querying, editing and managing the spreadsheet files used by the automation.

---

## 17.4 Technical justification

The selection of ONLYOFFICE is based on the following aspects:

- It allows working directly with files in `.xlsx` format.
- It works completely locally.
- It does not require cloud services.
- It offers a familiar interface for the user.
- It facilitates the review and manual editing of information stored by the automation.
- It is compatible with the storage mechanism defined for the project.

---

## 17.5 Scope

ONLYOFFICE will be used for:

- Querying information stored by the automation.
- Reviewing results.
- Making manual modifications when necessary.
- Verifying the content of spreadsheets used by the system.

The automation will continue to be responsible for automatic reading and writing of files via `openpyxl`.

---

## 17.6 Principles of use

Auxiliary tools must comply with the following principles:

- Complement the operation of the automation.
- Not replace components of the official technology stack.
- Facilitate user interaction with the system.
- Reduce the operational complexity of the project.

---

## 17.7 Restrictions

Auxiliary tools must comply with the following restrictions:

- Be free.
- Work locally.
- Maintain compatibility with the official technology stack.
- Not duplicate functionalities provided by other project technologies.

---

# 18. Compatibility between technologies

## 18.1 Objective

To define the compatibility criteria between the technologies that make up the official stack of the project, ensuring that all its components can be correctly integrated and function as a single, coherent system.

---

## 18.2 Compatibility principle

All selected technologies must be compatible with each other and perform a clearly defined responsibility within the architecture.

Technologies that:
- Duplicate existing functionalities.
- Generate integration conflicts.
- Introduce unnecessary dependencies.
- Increase project complexity without providing a demonstrable technical benefit.

---

## 18.3 Technology stack compatibility

| Technology | Compatible with | Main function |
|------------|----------------|---------------|
| Python | Entire stack | Main language of the project. |
| Playwright | BeautifulSoup4, Tenacity, Loguru | Browser automation. |
| BeautifulSoup4 + lxml | Playwright | HTML processing and analysis. |
| Pydantic | Entire system | Data validation and serialization. |
| Ollama | Qwen, Gemma | Local inference engine for AI. |
| Ollama Cloud | Gemma 4 31B | Cloud inference engine for AI. |
| Qwen 3.5 4B | Ollama | Local language model. |
| Gemma 4 31B | Ollama Cloud | Cloud language model. |
| openpyxl | ONLYOFFICE | Management of storage in `.xlsx` files. |
| PyYAML | python-dotenv | Project configuration management. |
| Loguru | Entire stack | Event logging and auditing. |
| Tenacity | Playwright, Ollama, httpx | Automatic retries. |
| RapidFuzz | Pydantic | Approximate text comparison. |
| httpx | Tenacity, Loguru | HTTP requests when the browser is not required. |
| Git | Entire project | Version control. |

---

## 18.4 Architectural integration

Each component of the technology stack should interact only with the elements necessary to fulfill its responsibility.

The architecture should favor:

- Low coupling.
- High cohesion.
- Separation of responsibilities.
- Ease of maintenance.
- Possibility of future evolution without affecting the rest of the system.

---

## 18.5 Future compatibility

Every proposed new technology must pass an evaluation process before being incorporated into the official stack.

At a minimum, it must demonstrate:

- Technical compatibility with existing technologies.
- Absence of functional conflicts.
- Integration with the defined architecture.
- Clearly justified technical benefit.

---

## 18.6 Restrictions

The incorporation of new technologies must comply with the following restrictions:

- Maintain compatibility with the official stack.
- Not replace existing components without prior evaluation.
- Not introduce redundant dependencies.
- Preserve the stability and coherence of the project architecture.


---

# 19. Technological restrictions

## 19.1 Objective

To define the technological restrictions that must be respected throughout the entire lifecycle of the project, in order to guarantee the coherence of the technology stack, facilitate the maintenance of the automation and avoid incorporating technologies that contradict the principles defined for the project.

---

## 19.2 Free software

All technologies, tools, libraries and components incorporated into the project must be free to use.

Technologies whose use depends on paid licenses, mandatory subscriptions or recurring costs for the operation of the automation will not be adopted.

---

## 19.3 Local execution

The automation must run entirely on the user's machine.

It will not depend on external services for its main operation.

Critical system components must operate locally.

---

## 19.4 Artificial intelligence

Artificial intelligence must run using local models.

Commercial APIs will not be used as the main component of the automation.

All interaction with the language model must be carried out through the architecture defined for the AI Service.

---

## 19.5 Technological compatibility

Every new technology incorporated must be compatible with the official technology stack.

Components that generate incompatibilities, integration conflicts or duplication of functionalities may not be introduced.

---

## 19.6 Minimization of dependencies

External dependencies should be incorporated only when:

- They solve a real need of the project.
- They provide a demonstrable technical advantage.
- There is no equivalent solution in the Python standard library.
- They do not duplicate functionalities already covered by another technology in the stack.

---

## 19.7 Maintainability

Technologies that meet the following criteria will be prioritized:

- Active maintenance.
- Sufficient documentation.
- Consolidated community.
- Stability.
- Wide adoption within the corresponding ecosystem.

---

## 19.8 Simplicity

When several technically equivalent alternatives exist, the one that:

- Introduces less complexity.
- Requires less maintenance.
- Facilitates the future evolution of the project.
- Integrates better with the rest of the technology stack.

---

## 19.9 Portability

The automation must be movable to another machine with the fewest possible modifications.

System configuration must be kept separate from the source code to facilitate such portability.

---

## 19.10 General restrictions

During the development of the project, the following is not allowed:

- Incorporating technologies without prior technical evaluation.
- Duplicating functionalities through different tools.
- Introducing dependencies that do not provide a clearly justified benefit.
- Modifying the official technology stack without previously updating the corresponding documentation.


---

# 20. Technology update and replacement strategy

## 20.1 Objective

To define the procedure to be followed for updating, replacing or incorporating technologies within the official stack of the project, ensuring the stability of the automation and the coherence of the technological architecture.

---

## 20.2 General principles

The technology stack of the project must be kept as stable as possible.

Selected technologies will not be replaced solely because of the emergence of new alternatives or changes in market trends.

Every modification must respond to a real technical need and provide a demonstrable improvement for the project.

---

## 20.3 Criteria for updating

A technology may be updated when:

- There are relevant improvements in stability, performance or security.
- Errors affecting the operation of the project are corrected.
- The new version maintains compatibility with the rest of the technology stack.
- The update does not involve unjustified architectural changes.

---

## 20.4 Criteria for replacement

A technology may be replaced only when at least one of the following situations occurs:

- It ceases to be actively maintained.
- It presents compatibility problems that cannot be resolved.
- There is a clearly superior alternative for the project needs.
- The replacement provides significant technical benefits that justify the migration cost.

The mere fact that a newer technology exists will not constitute a sufficient reason to carry out a replacement.

---

## 20.5 Evaluation process

Before approving any update or replacement, a technical evaluation must be carried out that contemplates, at a minimum:

- Compatibility with the official technology stack.
- Impact on the project architecture.
- Risks associated with the migration.
- Expected benefits.
- Implementation effort.
- Impact on future maintenance.

The decision must be documented before being incorporated into the project.

---

## 20.6 Compatibility during transition

When a technology is replaced, it must be ensured that the transition does not compromise:

- The integrity of the information.
- The stability of the automation.
- The compatibility with the other components of the system.

Whenever possible, migrations should be carried out in a controlled and verifiable manner.

---

## 20.7 Documentation

Every approved update or replacement must be reflected in the official project documentation.

At a minimum, the following must be updated:

- This document.
- The official technology stack inventory.
- The affected technical documentation.
- The `requirements.txt` file, when applicable.

---

## 20.8 Restrictions

The evolution of the technology stack must comply with the following restrictions:

- Do not modify technologies without prior technical evaluation.
- Do not introduce changes that unnecessarily increase the complexity of the project.
- Maintain coherence with the technological principles defined in this document.
- Preserve the stability, maintainability and portability of the automation.

---

# 21. Acceptance criteria

## 21.1 Objective

To define the criteria that the technology stack must meet to be considered officially approved as part of the automation architecture.

These criteria will serve as a reference for validating future incorporations, modifications or replacements of technologies.

---

## 21.2 General criteria

The technology stack will be considered accepted when it meets, at a minimum, the following criteria:

- All technologies have been technically evaluated.
- There is a documented justification for each decision made.
- There are no functional duplications between technologies.
- All technologies are compatible with each other.
- The stack maintains coherence with the architecture defined for the project.

---

## 21.3 Compatibility

The selected technologies must integrate correctly with each other without generating functional or architectural conflicts.

The incorporation of a new component must not compromise the stability of the rest of the system.

---

## 21.4 Maintainability

The stack should favor the maintenance of the project through:

- Stable technologies.
- Sufficient documentation.
- Active community.
- Low level of complexity.
- Ease of updating.

---

## 21.5 Sustainability

The selected technologies must align with the general principles of the project:

- Free use.
- Local execution.
- Independence from external services for main operation.
- Ease of maintenance.
- Scalability according to the needs of the automation.

---

## 21.6 Documentary consistency

Every approved technology must be documented in:

- This document.
- The official technology stack inventory.
- The corresponding technical documentation, when applicable.

---

## 21.7 Final acceptance

The technology stack will be considered officially approved when it meets all of the criteria defined in this chapter.

Any subsequent incorporation, modification or replacement must be re-evaluated according to these same criteria before becoming part of the official technology stack.

---

# 22. Official technology stack inventory

## 22.1 Objective

To consolidate in a single inventory all officially approved technologies for the development, execution and maintenance of the automation.

This inventory constitutes the official reference of the project's technology stack.

---

## 22.2 Official inventory

| Category | Official technology | Purpose |
|----------|--------------------|---------|
| Programming language | Python | Development of the automation. |
| HTML processing | BeautifulSoup4 | Analysis and extraction of information from HTML. |
| HTML parser | lxml | Parser used by BeautifulSoup4. |
| Data validation | Pydantic v2 | Data validation, serialization and deserialization. |
| Event logging | Loguru | Logging and audit system. |
| Text comparison | RapidFuzz | Approximate string comparison. |
| Retries | Tenacity | Automatic retry management. |
| HTTP client | httpx | HTTP requests when the browser is not required. |
| Browser automation | Playwright | Automation of navigation and interaction with websites. |
| Artificial intelligence (local) | Ollama | Local inference engine for language models. |
| Artificial intelligence (cloud) | Ollama Cloud | Cloud inference engine for language models (free plan). |
| Language model (local) | Qwen 3.5 4B | Local model for evaluation and high-volume tasks. |
| Language model (cloud) | Gemma 4 31B | Cloud model for deep processing and content generation. |
| Persistent storage | `.xlsx` file | Official storage of project information. |
| `.xlsx` file management | openpyxl | Reading and writing of the spreadsheet. |
| Configuration | config.yaml | Functional configuration of the automation. |
| Environment variables | .env | Environment-specific configuration. |
| Configuration management | PyYAML | Reading and writing of YAML files. |
| Environment variables | python-dotenv | Automatic loading of the `.env` file. |
| Dependency management | pip | Installation and management of dependencies. |
| Dependency inventory | requirements.txt | Official registry of external libraries. |
| Code editor | Visual Studio Code | Development of the automation. |
| Virtual environment | venv | Development environment isolation. |
| Code formatting | Black | Automatic source code formatting. |
| Static analysis | Ruff | Code quality analysis. |
| Static typing | mypy | Type checking. |
| Testing | pytest | Automated tests. |
| Documentation | Markdown (.md) | Technical and functional documentation. |
| Version control | Git | Project versioning. |
| Auxiliary tool | ONLYOFFICE | Manual querying and editing of `.xlsx` files. |

---

## 22.3 Remarks

This inventory constitutes the official technology stack of the automation.

Any incorporation, replacement or removal of a technology must comply with the evaluation process defined in this document before becoming part of the official stack.

This inventory must be kept updated throughout the entire lifespan of the project.
