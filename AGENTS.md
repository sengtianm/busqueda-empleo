# AGENTS.md

# Job Search Automation

## Project Status

The project is currently in the planning phase.

There is currently no implemented code.

All official documentation is located in `/docs`.

Development of the MVP must not begin until the corresponding documentation has been approved.

---

# General Principles

- Official documentation always takes priority.
- Never assume information that is not documented.
- If documentation contains a contradiction, stop implementation and request a decision.
- Do not modify the architecture, data model, workflow, technology stack, or business rules without explicit authorization.
- The user retains all functional and strategic decision-making authority.

---

# Workflow

For each task:

1. Understand the scope.
2. Read only the necessary documentation.
3. Present a plan.
4. Wait for approval.
5. Implement.
6. Validate.
7. Deliver a report.
8. Wait for approval before continuing to the next task.

Never work on more than one task simultaneously.

---

# Version Control

- Every new phase, module, or significant development must be developed in a dedicated branch.
- The branch is created when work begins and remains active until the user explicitly instructs it to be merged into `main`.
- Do not merge any branch without the user's explicit authorization.

---

# Documentation

All official documentation is located in `docs/`.

Reading order:

1. DOC-00 (Glossary)
2. The document related to the current task
3. Documents referenced by that document

Do not read unnecessary documentation.

---

# Architecture

Three-layer architecture:

- Functional modules
- Shared services
- Infrastructure

General workflow:

Discovery →  
Preparation →  
Evaluation →  
Processing →  
Management

All implementations must follow this architecture.

---

# Technology Stack

- Python 3.12
- Playwright
- BeautifulSoup + lxml
- SQLite
- Pydantic
- httpx
- Loguru
- RapidFuzz
- Tenacity
- Ollama
- PyYAML
- python-dotenv
- pytest
- Ruff
- mypy

Do not add new dependencies without authorization.

---

# Conventions

- Language: English for all code, documentation, configuration, prompts, commit messages, directory names, and file names.
- Language: Spanish for everything related to data — the SQLite database (table names, column names, and stored data), the Pydantic models and persistence layer that mirror it (`shared/models.py`, `shared/persistence.py`), the profile and evaluation criteria data in `config.yaml`, and test fixture data.
- Language: Spanish for all conversations with the user (unless the user explicitly requests otherwise).
- Language: Spanish for all natural-language data stored in the database (`job_search.db`) — job titles, descriptions, interview preparation, cover letter drafts, and any other user-facing content.
- Configuration must be separated from business logic.
- Prompts must be separated from the code.
- No hardcoded values.
- Every transformation must preserve the original data.
- No functional module may access the database directly.

---

# Validation

Before completing a task:

- Run only the validations relevant to the implemented change.
- Review the official acceptance criteria.
- Generate a report containing:
  - Objective
  - Modified files
  - Validations performed
  - Result
  - Issues encountered

---

# Session History

At the end of each development session:

- Update `Session History.md` with **one entry per calendar day**.
- Before writing, check today's date:
  - If an entry already exists for that date, update it.
  - Otherwise, create a new entry.
- Keep the history cumulative.
- Record the information in three sections using keyword-style bullet points.

### Topics

- Short keyword-style bullet points (maximum one line each).
- Describe **what** was done, not **how** it was done (unless the implementation approach is itself the decision).
- **Do NOT include:**
  - Commit hashes
  - Individual file paths
  - Rule/AC/EP numbers unless they are the central topic
- If the session contains multiple work blocks (morning/afternoon), separate them with bracketed headings, for example:
  - `[Morning]`
  - `[Afternoon]`

### Decisions

- Include only decisions that are new or modified compared to previous sessions.
- Omit anything that simply repeats previous agreements.

### Status

- Mark completed and pending phases using ✅ and ⬜.
- Include Ruff, mypy, and pytest results if changes were made.
- Include the active branch only when applicable.

If there is any doubt about whether a detail should be included or omitted, ask the user.

---

# When There Is Uncertainty

Never invent a solution.

Stop the implementation.

Explain the problem.

Wait for a decision.
