# Job Search Automation

Automated system for discovery, evaluation, and processing of job opportunities, with LinkedIn as the primary source.

## Documentation

All official documentation is located in `docs/`:

| Document | Purpose |
|----------|---------|
| [Ficha técnica](docs/diagrams/) | Node-level module specifications (authoritative for building) |
| [DOC-13A](docs/project-design/Document%2013A%20-%20Detailed%20Data%20Model%20Design.md) | Detailed data model (entities, attributes, catalogs, ERD) |
| [Appendix 5A](docs/project-design/DOC-Appendix%205A%20-%20Official%20Prefix%20Catalog.md) | Official prefix catalog (IDs, codes) |
| [Decision log](docs/history/decision%20log.md) | Approved decisions and deviations |
| [MVP Execution Plan](docs/plans/MVP%20Execution%20Plan.md) | Build order and acceptance criteria |
| [tracker.md](docs/history/tracker.md) | Current status of each phase and task |
| [Adding a new source](docs/adding-a-new-source.md) | Step-by-step guide to integrate a new platform (config, adapter, registry, tests) |

## Status

Project in development phase. Phases 0-3 and Module 1 (Opportunity Discovery) completed.

## Technology Stack

Python 3.12, Playwright, BeautifulSoup4, Pydantic v2, Loguru, RapidFuzz, Tenacity, httpx, Ollama + Gemma 4 31B cloud (via local proxy), SQLite.
