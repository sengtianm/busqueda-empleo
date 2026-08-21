# Job Search Automation

Automated system for discovery, evaluation, and processing of job opportunities, with LinkedIn as the primary source.

## Documentation

All official documentation is located in `docs/`:

| Document | Purpose |
|----------|---------|
| [Ficha técnica — Descubrimiento (M1)](docs/diagrams/Ficha%20técnica%20-%20Diagrama%20de%20flujo%20(Descubrimiento%20de%20oportunidades).md) | Module 1 (Opportunity Discovery) — node-level spec, as-built (D22, D25, D28, D29, D30, D31, D32). |
| [Ficha técnica — Preparación de ofertas (M2)](docs/diagrams/Ficha%20técnica%20-%20Diagrama%20de%20flujo%20(Preparación%20de%20ofertas).md) | Module 2 (Offer Preparation, Phase 5) — node-level spec, authoritative construction base (D33, 2026-08-20). |
| [Ficha técnica — Orquestador transversal](docs/diagrams/Ficha%20técnica%20-%20Diagrama%20de%20flujo%20(Orquestador%20transversal).md) | Transversal orchestrator (modules 1 → 2) — authoritative construction base (D34, 2026-08-20). |
| [DOC-13A](docs/project-design/Document%2013A%20-%20Detailed%20Data%20Model%20Design.md) | Detailed data model (entities, attributes, catalogs, ERD) — v1.11. |
| [Appendix 5A](docs/project-design/DOC-Appendix%205A%20-%20Official%20Prefix%20Catalog.md) | Official prefix catalog (IDs, codes) — FNT retired (D31); module scope generalized (D33/D34). |
| [Decision log](docs/history/decision%20log.md) | Approved decisions and deviations — D33/D34 register Module 2 + transversal orchestrator. |
| [MVP Execution Plan](docs/plans/MVP%20Execution%20Plan.md) | Build order and acceptance criteria |
| [tracker.md](docs/history/tracker.md) | Current status of each phase and task |
| [Adding a new source](docs/adding-a-new-source.md) | Step-by-step guide to integrate a new platform (config, adapter, registry, tests) |
| [Plan funcional fase 5](docs/plans/Plan%20funcional%20fase%205.md) | Phase 5 functional plan — Module 2 + transversal orchestrator (decisions, gaps, optimizations). |

## Status

Project in development phase. Phases 0-3 and Module 1 (Opportunity Discovery) completed. **Phase 5 plan closed:** Module 2 (Offer Preparation) and the transversal orchestrator are specified in their respective fichas técnicas (`docs/diagrams/`); implementation pending approval (decisions D33/D34).

## Technology Stack

Python 3.12, Playwright, BeautifulSoup4, Pydantic v2, Loguru, RapidFuzz, Tenacity, httpx, Ollama + Gemma 4 31B cloud (via local proxy), SQLite.
