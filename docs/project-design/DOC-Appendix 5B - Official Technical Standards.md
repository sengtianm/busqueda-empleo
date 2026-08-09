# Appendix 5B – Official Technical Standards

Concretizes Document 5 general conventions into technical standards for the job search automation. These standards apply uniformly to design, implementation, and evolution; every implementation must comply.

| ID | Standard | Specification |
|---|---|---|
| B.1 | Date | Format: `YYYY-MM-DD`. Example: `2026-07-17`. |
| B.2 | Date and time | Format: `YYYY-MM-DDTHH:mm:ssZ`. ISO 8601 compatible. Example: `2026-07-17T14:30:45Z`. |
| B.3 | Time zone | Internal processing: store all dates in UTC. User presentation: dates may be converted to the corresponding time zone. |
| B.4 | Duration | Recommended format: `PT2H35M20S`. ISO 8601 compatible. For internal calculations only, seconds may be used as the base unit. |
| B.5 | Identifier | Structure: `<PREFIX>-<NUMBER>`. Examples: `RF-001`, `RNF-014`, `MD-032`, `FD-018`, `PRM-005`, `CFG-003`. |
| B.6 | Version | Semantic Versioning: `vMajor.Minor.Patch`. Examples: `v1.0.0`, `v1.1.0`, `v2.3.4`. |
| B.7 | JSON naming | All JSON keys must use `camelCase`. Example: `{"jobTitle": "", "companyName": "", "publicationDate": "", "evaluationScore": 0}`. |
| B.8 | Variable naming | Use `camelCase`. Examples: `jobOffer`, `evaluationScore`, `candidateProfile`. |
| B.9 | Constant naming | Use `UPPER_SNAKE_CASE`. Examples: `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `MIN_SCORE_REQUIRED`. |
| B.10 | File naming | Recommended: `descriptive-name.extension`. Examples: `decision-model.md`, `general-config.json`, `data-flow.drawio`. When including versions: `descriptive-name_v1.0.0.extension`. |
| B.11 | Folder naming | Recommended: `kebab-case`. Examples: `project-docs`, `job-offers`, `generated-files`, `prompt-library`. |
| B.12 | Prompt naming | Format: `PRM-XXX Descriptive Name`. Examples: `PRM-001 Initial Evaluation`, `PRM-002 Offer Classification`, `PRM-003 Strategy Generation`. |
| B.13 | Document naming | Format: `Document N - Document Name`. Examples: `Document 3 - Decision Model`, `Document 5 - Project Standards`. |
| B.14 | Auto-generated files | Format: `YYYYMMDD_HHmmss_type-identifier.extension`. Examples: `20260717_103015_report.md`, `20260717_121540_evaluation.json`, `20260717_183250_log.txt`. |
| B.15 | Log naming | Recommended: `YYYYMMDD_HHmmss_module.log`. Example: `20260717_103015_evaluation.log`. |
| B.16 | File encoding | All project text files must use UTF-8. |
| B.17 | Line endings | Use LF to maintain cross-platform compatibility. |
| B.18 | Markdown official documents | Must use: `.md` extension; UTF-8 encoding; Markdown headers (`#`); Markdown tables; code blocks with specified language when applicable. |
| B.19 | Exceptions | Any exception to these standards must be documented and approved before use. |
| B.20 | Official source | This appendix is the official technical reference for all concrete standards used by the job search automation. |
