# Appendix 5B - Official technical standards

This appendix establishes the official technical standards that must be used uniformly during the design, implementation, and evolution of the job search automation.

Its purpose is to turn the general conventions defined in Document 5 into concrete specifications.

Every implementation in the project must respect the standards defined in this appendix.

---

# B.1. Date standard

## Official format

```text
YYYY-MM-DD
```

### Example

```text
2026-07-17
```

---

# B.2. Date and time standard

## Official format

```text
YYYY-MM-DDTHH:mm:ssZ
```

Compatible with ISO 8601.

### Example

```text
2026-07-17T14:30:45Z
```

---

# B.3. Official time zone

During internal processing:

* All dates must be stored in UTC.

During user presentation:

* Dates may be converted to the corresponding time zone.

---

# B.4. Duration standard

Recommended format:

```text
PT2H35M20S
```

Compatible with ISO 8601.

When the process only requires internal calculations, seconds may also be used as the base unit.

---

# B.5. Official identifier format

General structure:

```text
<PREFIX>-<NUMBER>
```

Examples:

```text
RF-001
RNF-014
MD-032
FD-018
PRM-005
CFG-003
```

---

# B.6. Official version format

Semantic Versioning will be used.

Structure:

```text
vMajor.Minor.Patch
```

Examples:

```text
v1.0.0
v1.1.0
v2.3.4
```

---

# B.7. Official JSON naming convention

All JSON keys must use:

```text
camelCase
```

Examples:

```json
{
  "jobTitle": "",
  "companyName": "",
  "publicationDate": "",
  "evaluationScore": 0
}
```

---

# B.8. Official variable naming convention

The following will be used:

```text
camelCase
```

Examples:

```text
jobOffer
evaluationScore
candidateProfile
```

---

# B.9. Official constant naming convention

The following will be used:

```text
UPPER_SNAKE_CASE
```

Examples:

```text
MAX_RETRIES
DEFAULT_TIMEOUT
MIN_SCORE_REQUIRED
```

---

# B.10. Official file naming convention

Recommended format:

```text
descriptive-name.extension
```

Examples:

```text
decision-model.md
general-config.json
data-flow.drawio
```

When it is necessary to include versions:

```text
descriptive-name_v1.0.0.extension
```

---

# B.11. Official folder naming convention

Recommended format:

```text
kebab-case
```

Examples:

```text
project-docs
job-offers
generated-files
prompt-library
```

---

# B.12. Official prompt naming convention

Format:

```text
PRM-XXX Descriptive Name
```

Examples:

```text
PRM-001 Initial Evaluation

PRM-002 Offer Classification

PRM-003 Strategy Generation
```

---

# B.13. Official document naming convention

Format:

```text
Document N - Document Name
```

Examples:

```text
Document 3 - Decision Model

Document 5 - Project Standards
```

---

# B.14. Convention for auto-generated files

Format:

```text
YYYYMMDD_HHmmss_type-identifier.extension
```

Examples:

```text
20260717_103015_report.md

20260717_121540_evaluation.json

20260717_183250_log.txt
```

---

# B.15. Log convention

Recommended format:

```text
YYYYMMDD_HHmmss_module.log
```

Example:

```text
20260717_103015_evaluation.log
```

---

# B.16. File encoding convention

All project text files must use:

```text
UTF-8
```

---

# B.17. Line ending convention

The following will be used:

```text
LF
```

to maintain cross-platform compatibility.

---

# B.18. Markdown document convention

All official documents must use:

* Extension `.md`
* UTF-8 encoding
* Markdown headers (`#`)
* Markdown tables
* Code blocks with specified language when applicable.

---

# B.19. Compatibility

Any exception to the standards defined in this appendix must be documented and approved before use.

---

# B.20. Official source

This appendix constitutes the official technical reference for all concrete standards used by the job search automation.
