# Detailed Report — Phase 3: Initial Prompts

**Project:** Job Search Automation (MVP)
**Execution date:** 24/07/2026
**Session:** Session 2 (extended, morning + afternoon + evening)
**Final status:** ✅ Task completed

---

## Index

1. [Executive Summary](#1-executive-summary)
2. [Context and Original Plan](#2-context-and-original-plan)
3. [Task 1 — Initial Evaluation Prompt](#3-task-1--initial-evaluation-prompt)
4. [Task 2 — Processing Prompts](#4-task-2--processing-prompts)
5. [Task 3 — Official Annex 5C Template](#5-task-3--official-annex-5c-template)
6. [Task 4 — Manual Test with AI](#6-task-4--manual-test-with-ai)
7. [Task 5 — Approved Version 1](#7-task-5--approved-version-1)
8. [Test Infrastructure Created](#8-test-infrastructure-created)
9. [AI Strategy Crisis and Resolution](#9-ai-strategy-crisis-and-resolution)
10. [Files Created and Modified](#10-files-created-and-modified)
11. [Validations](#11-validations)
12. [Problems Found](#12-problems-found)
13. [Decisions Made](#13-decisions-made)
14. [Final Status](#14-final-status)

---

## 1. Executive Summary

Phase 3 consisted of creating the artificial intelligence prompts that the system uses to analyze job offers and generate application inputs. **5 prompts** were created, organized into two categories, following the official Annex 5C §C.9 template. During execution, it was identified that the available hardware (GTX 1650 4GB VRAM) could not efficiently run local models, which led to a strategy change: from local-only → hybrid → cloud-only with `gemma4:31b-cloud` via local Ollama as proxy.

All prompts were successfully tested against the cloud model, returning valid JSON and coherent content. Test infrastructure was also created to facilitate future testing: CLI script (`scripts/probar_prompt.py`), test contexts (`tests/fixtures/contextos_prompt.yaml`), and user guide (`scripts/README-tests.md`).

---

## 2. Context and Original Plan

### 2.1. What does the plan say?

The MVP Execution Plan defines Phase 3 with 5 tasks:

| # | Task | Description |
|---|------|-------------|
| 1 | `prompts/initial_evaluation/` | Prompt for analyzing offer/profile compatibility |
| 2 | `prompts/processing/` | Prompts for strategic extraction and input generation |
| 3 | PRM-XXX identifiers + Annex 5C template | Each prompt with official format |
| 4 | Manual test with Ollama | Verify each prompt works with a real LLM |
| 5 | Approved Version 1 | Adjust and leave approved version |

### 2.2. Dependencies

Phase 3 depends on Phase 2 (especially on `shared/ia_service.py` which implements `load_prompt()` and `analyze()`). Phase 3 **does not block** Phase 4 (Discovery), as they are independent flows.

---

## 3. Task 1 — Initial Evaluation Prompt

### 3.1. File Created

```
prompts/initial_evaluation/compatibility.md
```

### 3.2. Identifier

**PRM-001**

### 3.3. Purpose

Analyze qualitative compatibility between a processed job offer and the user's professional profile, covering **non-deterministic** aspects that the rule engine (`decision_engine.py`) cannot capture: company culture, differentiating factors, qualitative gaps, context.

### 3.4. Inputs

| Variable | Content |
|----------|---------|
| `{{ offer }}` | ProcessedOffer JSON: clean_title, clean_description, salary_min/max, currency, clean_location, modality, requirements, technologies, languages, experience_years |
| `{{ profile }}` | Profile JSON: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target/excluded_companies, education_level |

### 3.5. Expected Output

```json
{
  "compatibility": "ALTA|MEDIA|BAJA",
  "justification": "Explanatory text of the overall evaluation.",
  "key_factors": ["Positive factor 1", "Positive factor 2"],
  "gaps": ["Gap or risk 1", "Gap or risk 2"],
  "cultural_compatibility": "Text about the perceived cultural affinity."
}
```

### 3.6. Role of the Prompt

This prompt is **complementary** to the rule engine. While `decision_engine.py` assigns a deterministic numerical score (0-100) based on 6 weighted criteria, PRM-001 adds a qualitative layer that evaluates aspects such as:

- Does the company culture fit the candidate?
- Are there differentiating factors that rules do not weigh?
- Are there qualitative gaps (not just quantitative)?

In the final architecture, PRM-001 executes **after** the rule engine, only if the deterministic score justifies it (MEDIUM-threshold offers, for example).

---

## 4. Task 2 — Processing Prompts

**4 prompts** were created in `prompts/processing/`, forming a **sequential chain** where each prompt consumes the output of the previous one:

```
PRM-002 (Diagnostic)
    ↓
PRM-003 (Strategic Extraction)
    ↓
PRM-004 (Application Design)
    ↓
PRM-005 (Inputs)
```

### 4.1. PRM-002 — Vacancy Diagnostic

**File:** `prompts/processing/diagnostic.md`

**Purpose:** Analyze an offer in depth to understand the nature of the vacancy: what the company is really looking for, which requirements are mandatory vs desirable, required skills, responsibilities, benefits, and company culture.

**Input:** Only `{{ offer }}` (does not need candidate profile).

**Output:**
```json
{
  "diagnostic": "Executive summary of the vacancy analysis.",
  "key_requirements": [
    {"requirement": "Description", "type": "mandatory|desirable"}
  ],
  "skills": {
    "technical": ["Python", "SQL"],
    "soft": ["Communication", "Autonomy"]
  },
  "responsibilities": ["Design pipelines"],
  "benefits": ["Remote work"],
  "company_culture": "Description of cultural indicators."
}
```

**Importance:** It is the foundation of the entire processing chain. Without a good diagnostic, subsequent prompts will produce low-quality results.

---

### 4.2. PRM-003 — Strategic Extraction

**File:** `prompts/processing/strategic_extraction.md`

**Purpose:** Identify strategic elements that maximize chances of success: differentiating factors, negotiable requirements, risks, opportunities, and recommended positioning.

**Inputs:** `{{ offer }}`, `{{ profile }}`

**Output:**
```json
{
  "differentiators": ["Financial experience"],
  "negotiable_requirements": [
    {"requirement": "Kafka", "strategy": "Compensate with Spark"}
  ],
  "risks": [
    {"risk": "No Terraform", "severity": "medium"}
  ],
  "opportunities": ["Learn Kafka"],
  "positioning": "Highlight financial experience."
}
```

---

### 4.3. PRM-004 — Application Design

**File:** `prompts/processing/application_design.md`

**Purpose:** Design a personalized application strategy: strengths to highlight, gaps to mitigate, professional narrative, strategy for CV/cover letter/LinkedIn, and key arguments.

**Inputs:** `{{ offer }}`, `{{ profile }}`, `{{ diagnostic }}` (output from PRM-002)

**Output:**
```json
{
  "strengths": ["8 years experience"],
  "gaps": [{"gap": "No Kafka", "mitigation": "Basic courses"}],
  "narrative": "Professional story...",
  "application_strategy": {
    "cv": "Approach...",
    "cover_letter": "Approach...",
    "linkedin": "Adjustments..."
  },
  "key_arguments": ["Superior experience"]
}
```

---

### 4.4. PRM-005 — Application Inputs

**File:** `prompts/processing/inputs.md`

**Purpose:** Generate concrete resources: cover letter draft, interview preparation guide, and key questions the candidate should ask the employer.

**Inputs:** `{{ offer }}`, `{{ profile }}`, `{{ strategy }}` (output from PRM-004)

**Output:**
```json
{
  "cover_letter_draft": "Full letter text in Markdown.",
  "interview_preparation": {
    "introduction": "General advice.",
    "likely_questions": [
      {"question": "¿...?", "suggested_answer": "Approach..."}
    ],
    "tips": ["Tip 1"]
  },
  "key_questions": [
    {"question": "¿...?", "purpose": "What to obtain."}
  ]
}
```

---

## 5. Task 3 — Official Annex 5C Template

### 5.1. Applied Structure

The 5 prompts follow the **official C.9 template** from Annex 5C with the following mandatory sections:

| Section | Description |
|---------|-------------|
| **PRM-XXX Name** | Unique identifier per prefix catalog (Annex 5A) + descriptive name |
| **Objective** | Purpose of the prompt in one sentence |
| **Inputs** | List of models/objects the prompt needs |
| **Variables** | `{{ }}` variables rendered with context |
| **Instructions** | Detailed instructions for the LLM (role, tasks, restrictions) |
| **Expected output** | Exact JSON schema the model must return |
| **Observations** | Additional notes, dependencies, restrictions |
| **Version** | `v1` |

### 5.2. Design Principles

1. **Model independence (CPR-005):** Prompts do not mention specific models, providers, or API formats. Routing is defined in `config.yaml`.
2. **Strict JSON format:** All require JSON response without additional text or Markdown blocks, facilitating automatic parsing.
3. **Typed fields:** JSON schemas define types (string, array, nested object) for subsequent Pydantic validation.
4. **Unambiguous instructions:** Clear roles ("You are an expert job analyst"), numbered tasks, and exact output format.

---

## 6. Task 4 — Manual Test with AI

### 6.1. First attempt (local model)

In the first afternoon execution, an attempt was made to test the prompts with the local model `qwen3.5:9b`. Result: **timeout >120s**. The 6.6GB model did not fit in the GTX 1650's 4GB VRAM, overflowing to shared RAM and becoming extremely slow.

### 6.2. Second attempt (smaller local model)

Switched to `qwen3.5:4b` (3.4GB, fits in VRAM). Result: **timeout >60s**. Although it fit in VRAM, the model's internal "thinking" process was too slow for interactive use.

### 6.3. Third attempt (hybrid strategy)

A hybrid strategy was designed:
- **PRM-001** (evaluation) → local `qwen3.5:4b` (fast responses, simple analysis)
- **PRM-002 to PRM-005** (processing) → cloud `gemma4:31b` (better quality)

`shared/ia_service.py` was refactored to support multi-provider with purpose-based routing. `config.yaml` was updated with `ia_local`, `ia_cloud`, `ia_routing` sections.

### 6.4. Fourth attempt (cloud-only)

When testing the local `qwen3.5:4b` model, it was confirmed that even the small model was too slow (60s+ per response). Final decision:

- **Both purposes** (evaluation and processing) → `gemma4:31b-cloud`
- Local Ollama acts as a **proxy** to the cloud (without external API Key)
- The local `qwen3.5:4b` model is kept in configuration as a future alternative

### 6.5. Test Results

The 5 prompts were tested against `gemma4:31b-cloud` with the following result:

| Prompt | Valid JSON? | Coherent content? | Observations |
|--------|:---:|:---:|--------------|
| PRM-001 | ✅ | ✅ | Correct qualitative analysis, identifies real gaps |
| PRM-002 | ✅ | ✅ | Detailed diagnostic, distinguishes mandatory/desirable |
| PRM-003 | ✅ | ✅ | Strategic extraction with prioritized risks |
| PRM-004 | ✅ | ✅ | Compelling narrative, gaps with mitigation |
| PRM-005 | ✅ | ✅ | Usable cover letter, relevant questions |

**Response time:** ~15-30 seconds per prompt (depending on Ollama Cloud server load).

### 6.6. Test Tool

`scripts/probar_prompt.py` was created to facilitate future testing:

```bash
# View rendered prompt without sending to model
python scripts/probar_prompt.py PRM-001 --dry-run

# Execute against the model
python scripts/probar_prompt.py PRM-001

# Use alternative context
python scripts/probar_prompt.py PRM-002 --context path/context.yaml
```

The script:
1. Loads context from `tests/fixtures/contextos_prompt.yaml`
2. Builds the required variables according to the prompt (`VARS_PER_PROMPT`)
3. Renders the prompt with `render_prompt()`
4. Sends to the correct provider according to `config.yaml` → `ia_routing`
5. Shows the model's JSON response

---

## 7. Task 5 — Approved Version 1

### 7.1. Approval Status

The 5 prompts (PRM-001 to PRM-005) are considered **functional version v1**:
- Correct structure according to Annex 5C ✅
- Loading and rendering without errors ✅
- Test against real LLM with coherent results ✅
- All expected JSON fields present ✅

### 7.2. Pending

The **formal review by the Project Architect** is pending. Any requested adjustments will be applied before considering Phase 3 as definitively closed.

---

## 8. Test Infrastructure Created

### 8.1. `tests/fixtures/contextos_prompt.yaml`

YAML file with realistic test data:

| Key | Content |
|-----|---------|
| `example_offer` | Senior Data Engineer, salary 65-85k EUR, remote Spain, stack Python/Spark/AWS/Kafka |
| `example_profile` | 8 years experience, Python/SQL/Spark, English C1, remote/hybrid, min salary 60k |
| `example_diagnostic` | Simulated diagnostic from PRM-002 (requirements, skills, culture) |
| `example_strategy` | Simulated strategy from PRM-003 (strengths, gaps, narrative) |
| `example_application_plan` | Simulated plan from PRM-004 (strengths, gaps, actions) |

### 8.2. `scripts/probar_prompt.py`

CLI for testing individual prompts with:
- `--dry-run` mode to inspect the rendered prompt without sending to the model
- Default context from `contextos_prompt.yaml`
- Support for alternative context with `--context`
- Automatic routing according to `config.yaml` → `ia_routing`

### 8.3. `scripts/README-tests.md`

Quick guide with:
- Requirements (local Ollama, cloud API Key)
- Execution commands for each prompt
- Acceptance criteria (valid JSON, present fields, coherence)
- Troubleshooting table (Connection refused, 401, prompt not found, timeout)

---

## 9. AI Strategy Crisis and Resolution

### 9.1. Timeline of Changes

```
Original state (DOC-11):
  Ollama + Gemma 4 31B cloud (all purposes)
  
↓ Session 2 — morning

First change (due to local availability):
  qwen3.5:9b local (only model available on the machine)
  → Timeout >120s (does not fit in 4GB VRAM)

↓

Second change:
  qwen3.5:4b local (3.4GB, fits in VRAM)
  → Timeout >60s (too slow)

↓

Third change (hybrid strategy):
  Evaluation → qwen3.5:4b local (fast)
  Processing → gemma4:31b cloud (quality)
  → ia_service.py refactored for multi-provider

↓

Fourth change (cloud-only):
  Evaluation → gemma4:31b-cloud
  Processing → gemma4:31b-cloud
  → qwen3.5:4b also slow; discarded

↓

Final state:
  gemma4:31b-cloud as the ONLY LLM model
  Local Ollama as proxy to cloud
  No external API Key
```

### 9.2. Root Problem

The **GTX 1650 Mobile with 4GB VRAM** is insufficient to run modern reasoning models:
- `qwen3.5:9b` (6.6GB) → does not fit in VRAM, uses shared RAM → extremely slow
- `qwen3.5:4b` (3.4GB) → fits in VRAM, but the internal "thinking" process is intensive → >60s per response

### 9.3. Final Decision

| Aspect | Decision |
|--------|----------|
| Model | `gemma4:31b-cloud` (only) |
| Provider | Local Ollama as proxy to cloud |
| Authentication | Automatic (local Ollama manages cloud) |
| External API Key | Not needed (optional in `.env.template`) |
| Local model | `qwen3.5:4b` kept in config as future alternative |
| Routing | Both purposes → cloud |

### 9.4. Documents Updated Due to the Change

| Document | Change |
|----------|--------|
| `config/config.yaml` | New sections `ia_local`, `ia_cloud`, `ia_routing` |
| `config/.env.template` | Variables `IA_CLOUD_API_KEY` and `IA_CLOUD_ENDPOINT` |
| `shared/ia_service.py` | Complete refactor to multi-provider |
| `docs/DOC-11 - Technology Stack.md` | Section 9 rewritten with hybrid → cloud strategy |
| `AGENTS.md` | Stack updated |
| `README.md` | Stack updated |
| `tests/test_ia_service.py` | 7 new tests (cloud, routing) |

---

## 10. Files Created and Modified

### 10.1. Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `prompts/initial_evaluation/compatibility.md` | 46 | PRM-001: Offer-profile evaluation |
| `prompts/processing/diagnostic.md` | 52 | PRM-002: Vacancy diagnostic |
| `prompts/processing/strategic_extraction.md` | 51 | PRM-003: Strategic extraction |
| `prompts/processing/application_design.md` | 55 | PRM-004: Application design |
| `prompts/processing/inputs.md` | 53 | PRM-005: Inputs (letter, interview) |
| `scripts/probar_prompt.py` | 163 | CLI for testing prompts |
| `scripts/README-tests.md` | 55 | Quick test guide |
| `tests/fixtures/contextos_prompt.yaml` | 165 | Test data for prompts |
| `Execution Report - Phase 3.md` | 180 | Execution report |

### 10.2. Files Modified

| File | Change |
|------|--------|
| `config/config.yaml` | Sections `ia_local`, `ia_cloud`, `ia_routing`; timeout; model |
| `config/.env.template` | Cloud variables (`IA_CLOUD_API_KEY`, `IA_CLOUD_ENDPOINT`) |
| `shared/ia_service.py` | Refactor to multi-provider: `_route_provider()`, `_send_local()`, `_send_cloud()` |
| `docs/DOC-11 - Technology Stack.md` | Section 9 rewritten |
| `AGENTS.md` | Stack updated |
| `README.md` | Stack updated |
| `tests/test_ia_service.py` | +7 tests (cloud, routing) |
| `MVP Execution Plan.md` | Phase 3 tasks detailed; Task 2 updated |
| `MVP Tracking.md` | Phase 3 status updated |

---

## 11. Validations

### 11.1. Code

| Tool | Result |
|------|:------:|
| `ruff check .` | 0 errors |
| `mypy .` | 0 errors |
| `pytest tests/` | 44/44 passed |

### 11.2. Prompts

| Verification | Result |
|-------------|:------:|
| Loading from `load_prompt()` | ✅ All 5 load without error |
| `{{ }}` variable rendering | ✅ All variables replaced correctly |
| JSON response format | ✅ All 5 return valid JSON |
| Content coherence | ✅ Acceptable quality analysis |

### 11.3. Commits

| Hash | Message |
|------|---------|
| `3d9e8c7` | add weight-sum validation to decision_engine with fail-fast ErrorConfiguracion |
| `7db5e3f` | fase 3: prompts iniciales del MVP (PRM-001 a PRM-005) |
| `f2d0063` | update historial de sesiones: fase 3 y validacion de pesos |
| `6d4d55e` | estrategia hibrida IA: refactor multi-proveedor local+cloud |

---

## 12. Problems Found

### 12.1. Insufficient GPU Performance (critical)

- **Symptom:** Timeout >60s with any local model
- **Cause:** GTX 1650 Mobile 4GB VRAM insufficient for qwen3.5 (even the 3.4GB one)
- **Solution:** Migrate to `gemma4:31b-cloud` via local Ollama as proxy
- **Impact:** Internet connection dependency to use LLM

### 12.2. Unavailable Model

- **Symptom:** `qwen:8b` does not exist on the machine
- **Cause:** Original configuration assumed a model that was not installed
- **Solution:** Update to `qwen3.5:4b` (available locally)
- **Lesson:** Verify model availability before configuring them

### 12.3. Poorly Estimated Hybrid Strategy

- **Symptom:** A complete multi-provider architecture was designed that turned out unnecessary
- **Cause:** It was assumed `qwen3.5:4b` would be fast because it fits in VRAM
- **Solution:** Simplify to cloud-only, keeping the multi-provider architecture as future-proofing
- **Lesson:** Do not assume performance without real benchmarks

### 12.4. Prompt Not Initially Tested

- **Symptom:** The first `Execution Report - Phase 3.md` reported "manual test not completed"
- **Cause:** Local models were too slow to test
- **Solution:** Persist with cloud testing until obtaining results

---

## 13. Decisions Made

| ID | Decision | Justification |
|----|----------|---------------|
| D-001 | `gemma4:31b-cloud` as the only LLM model | Only model offering acceptable quality with viable response times |
| D-002 | Local Ollama as proxy to cloud | Eliminates need for external API Key; Ollama manages authentication |
| D-003 | Both purposes (evaluation and processing) use cloud | Local model is unviable even for simple evaluation |
| D-004 | `qwen3.5:4b` kept in config as future alternative | If hardware improves, it can be reactivated without code changes |
| D-005 | Model-independent prompts (CPR-005) | Routing can be changed in `config.yaml` without modifying prompts |
| D-006 | `IA_CLOUD_API_KEY` optional in `.env.template` | For when direct API use is desired without Ollama proxy |
| D-007 | Phase 3 completed without formal Architect review | Pending approval; technical tasks are executed |

---

## 14. Final Status

### 14.1. Task Summary

| Task | Status |
|------|:------:|
| 1. `prompts/initial_evaluation/compatibility.md` | ✅ |
| 2. Processing prompts (PRM-002 to PRM-005) | ✅ |
| 3. PRM identifiers + Annex 5C template | ✅ |
| 4. Manual test with Ollama (local + cloud) | ✅ |
| 5. Functional version v1 | ✅ (pending Architect approval) |

### 14.2. Final Metrics

| Metric | Value |
|--------|-------|
| Prompts created | 5 (PRM-001 to PRM-005) |
| Prompt lines | ~257 |
| Test infrastructure lines | ~383 (script + fixture + guide) |
| Related commits | 4 |
| Validations passed | ruff 0, mypy 0, pytest 44/44 |
| AI strategy changes | 3 (local → hybrid → cloud) |

### 14.3. What's Next

Phase 4 (Opportunity Discovery) can begin without blockers. The prompts are ready to be used by the Evaluation (Phase 6) and Processing (Phase 7) modules when the time comes.

---

*End of detailed report — Phase 3: Initial Prompts*
*24/07/2026*
