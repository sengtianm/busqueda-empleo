# Appendix 5A. Official prefix catalog

This appendix establishes the official catalog of prefixes used by the job search automation documentation.

Its purpose is to guarantee uniform identification of documents, chapters, principles, rules, conventions, and other normative elements of the project.

This catalog constitutes the only official reference for assigning new prefixes.

---

# A.1. General principles

* Every prefix must be unique within the project.
* A prefix may only represent a single concept.
* Prefixes must remain stable throughout the life of the project.
* No document may reuse a prefix already assigned to another category.
* Any incorporation of a new prefix must update this catalog before being considered official.

---

# A.2. Document prefixes

| Prefix | Document                 |
| ------- | ------------------------- |
| DOC-00  | Project Glossary          |
| DOC-01  | Functional Requirements   |
| DOC-02  | Non-Functional Requirements |
| DOC-03  | Decision Model            |
| DOC-04  | Data Flow                 |
| DOC-05  | Project Standards         |

---

# A.3. Chapter prefixes

| Prefix | Meaning                                        |
| ------- | ------------------------------------------------ |
| PEP     | Principles of project standards                  |
| CEG     | General conventions                              |
| CNP     | Naming conventions                               |
| CID     | Identifier conventions                           |
| CED     | State conventions                                |
| CFH     | Date and time conventions                        |
| CFDT    | Data format conventions                          |
| CJS     | JSON structure conventions                       |
| CDO     | Documentation conventions                        |
| CPR     | Prompt conventions                               |
| CNA     | File and document naming conventions             |
| COC     | Folder organization conventions                  |
| CVE     | Versioning conventions                           |
| CLR     | Log conventions                                  |
| CAT     | Audit and traceability conventions               |
| CEM     | Entity and data model conventions                |
| CMC     | Module and component conventions                 |
| CCS     | System configuration conventions                 |
| RES     | Standard restrictions                            |
| CAE     | Acceptance criteria                              |

---

# A.4. Requirement prefixes

| Prefix | Meaning            |
| ------- | ------------------ |
| RF      | Functional Requirement |
| RNF     | Non-Functional Requirement |

---

# A.5. Decision prefixes

| Prefix | Meaning                    |
| ------- | ---------------------------- |
| MD      | Decision Model Rule          |

---

# A.6. Data flow prefixes

| Prefix | Meaning              |
| ------- | ---------------------- |
| FD      | Data Flow Rule         |

---

# A.7. Process prefixes

| Prefix | Meaning |
| ------- | ------- |
| PRC     | Process |
| ETP     | Stage   |
| SUB     | Subprocess |

---

# A.8. Module prefixes

| Prefix | Meaning |
| ------- | ------- |
| MOD     | Module  |
| CMP     | Component |
| SRV     | Service |
| INT     | Integration |

---

# A.9. Entity prefixes

| Prefix | Meaning |
| ------- | ------- |
| ENT     | Entity  |
| ATR     | Attribute |
| REL     | Relation |

---

# A.9b. Persistent data ID prefixes

| Prefix | SQLite Table        | Meaning                  |
| ------- | ------------------- | ------------------------- |
| FNT     | sources             | Job source (LinkedIn)     |
| EMP     | companies           | Employer company          |
| UBI     | locations           | Geographic location       |
| OFE     | offers              | Raw job offer             |
| OFP     | processed_offers    | Processed and cleaned offer |
| EVL     | evaluations         | Compatibility evaluation  |
| RSP     | processing_results  | Deep processing result    |
| COR     | corridas            | Run of the Discovery module (Module 1) |
| SES     | sesiones            | Platform session of the Discovery module |
| EVT     | eventos             | Event (error or success) of the Discovery module |
| BLO     | bloqueo             | Concurrency lock record (Module 1) |

---

# A.10. Configuration prefixes

| Prefix | Meaning         |
| ------- | --------------- |
| CFG     | Configuration   |
| ENV     | Environment variable |
| PAR     | Parameter       |

---

# A.11. Log prefixes

| Prefix | Meaning        |
| ------- | -------------- |
| LOG     | Operational log |
| EVT     | Event          |
| ERR     | Error          |
| WRN     | Warning        |
| INF     | Information    |

---

# A.12. Prompt prefixes

| Prefix | Meaning            |
| ------- | ------------------ |
| PRM     | Prompt             |
| SYS     | System instruction |
| TMP     | Prompt template    |

---

# A.13. File prefixes

| Prefix | Meaning          |
| ------- | ---------------- |
| DOC     | Document         |
| IMG     | Image            |
| CFG     | Configuration    |
| DB      | Database         |
| JSON    | JSON file        |
| LOG     | Log file         |

---

# A.14. Catalog administration

Any incorporation, modification, or deletion of a prefix must comply with the following conditions:

* Must not conflict with existing prefixes.
* Must maintain catalog uniqueness.
* Must update this appendix before using the new prefix.
* Must document the justification for the corresponding modification.

---

# A.15. Official source

This appendix constitutes the only official reference for the assignment and administration of prefixes used by the job search automation.

No project document may define prefixes that are different from or incompatible with those established in this catalog.
