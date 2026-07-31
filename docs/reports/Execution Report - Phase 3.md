# Execution Report — Phase 3

**Project:** Job Search Automation (MVP)
**Date:** 24/07/2026
**Status:** Task completed with observations

---

## 1. Objective

Execute Phase 3 of the MVP Execution Plan, which consists of creating the system's initial prompts:
- `prompts/initial_evaluation/` — prompt for analyzing offer-profile compatibility via LLM
- `prompts/processing/` — prompts for deep processing of accepted offers

---

## 2. Activities Performed

### 2.1. Task 1 — Create `prompts/initial_evaluation/`

**File created:** `prompts/initial_evaluation/compatibility.md`

**Identifier:** PRM-001

**Purpose:** Analyze qualitative compatibility between a processed offer and the user's professional profile, covering non-deterministic aspects that the rule engine cannot capture (company culture, differentiating factors, qualitative gaps).

**Structure (Annex 5C §C.9):**
- Objective, Inputs (`ProcessedOffer` + `Profile`), Variables (`{{ offer }}`, `{{ profile }}`), Instructions, Expected output (JSON with fields `compatibility`, `justification`, `key_factors`, `gaps`, `cultural_compatibility`), Observations, Version v1.

---

### 2.2. Task 2 — Create `prompts/processing/`

**Files created (4):**

| File | ID | Purpose | Variables | Expected output |
|------|----|---------|-----------|-----------------|
| `diagnostic.md` | PRM-002 | Analyze the vacancy in depth | `{{ offer }}` | JSON: diagnostic, key_requirements, skills, responsibilities, benefits, company_culture |
| `strategic_extraction.md` | PRM-003 | Extract differentiating factors and risks | `{{ offer }}`, `{{ profile }}` | JSON: differentiators, negotiable_requirements, risks, opportunities, positioning |
| `application_design.md` | PRM-004 | Design application strategy | `{{ offer }}`, `{{ profile }}`, `{{ diagnostic }}` | JSON: strengths, gaps, narrative, application_strategy, key_arguments |
| `inputs.md` | PRM-005 | Generate cover letter and interview preparation | `{{ offer }}`, `{{ profile }}`, `{{ strategy }}` | JSON: cover_letter_draft, interview_preparation, key_questions |

All prompts follow the official Annex 5C §C.9 template with the 8 mandatory sections.

---

### 2.3. Task 3 — Official Annex 5C Template

The 5 prompts were structured with:

```markdown
## PRM-XXX Prompt Name

**Objective.**
**Inputs.**
**Variables.**
**Instructions.**
**Expected output.**
```json
{ ... }
```
**Observations.**
**Version:** v1
```

Each prompt explicitly defines:
- The `ProcessedOffer` and `Profile` fields it uses
- The exact JSON format the LLM must return
- Clear instructions to avoid additional text and Markdown blocks

---

### 2.4. Task 4 — Manual Test with AI (pending)

**Status:** ⏳ Not completed

**What was verified:**
- Prompts load correctly from `shared/ia_service.py::load_prompt()`
- `{{ }}` variables render without errors from `render_prompt()`

**Note on model strategy:**
A hybrid strategy was adopted: the local model (`qwen3.5:4b`) will be used for PRM-001 (evaluation), and the cloud model (`gemma4:31b` via Ollama Cloud) for PRM-002 through PRM-005 (processing). This allows the manual test to be performed in two steps:

1. **PRM-001** with local `qwen3.5:4b` (fits in 4GB VRAM, fast responses)
2. **PRM-002 to PRM-005** with cloud `gemma4:31b` (better quality, requires API Key)

**Recommendation:** Run the test locally with:
```bash
cd /project/path
# PRM-001 with local model
python3 -c "
from shared.ia_service import analyze
import json

result = analyze('initial_evaluation/compatibility', {
    'offer': json.dumps(offer),
    'profile': json.dumps(profile)
}, purpose='evaluation')
print(result)
"
# PRM-002 to PRM-005 with cloud model
python3 -c "
result = analyze('processing/diagnostic', {
    'offer': json.dumps(offer)
}, purpose='processing')
print(result)
"
```

---

### 2.5. Task 5 — Version v1 (pending approval)

**Status:** ⬜ Pending

The 5 prompts are created as version `v1` but are not considered approved until:
1. The manual test with Ollama is executed (Task 4)
2. The Project Architect reviews and approves

---

## 3. Files Created

| File | Lines |
|------|-------|
| `prompts/initial_evaluation/compatibility.md` | 46 |
| `prompts/processing/diagnostic.md` | 52 |
| `prompts/processing/strategic_extraction.md` | 51 |
| `prompts/processing/application_design.md` | 55 |
| `prompts/processing/inputs.md` | 53 |
| **Total** | **~257 lines** |

## 4. Files Modified

| File | Change |
|------|--------|
| `MVP Execution Plan.md` | Tasks 3 and 4 of Phase 3 detailed with Annex 5C template and specification of both prompts |
| `MVP Tracking.md` | Phase 3 status updated (tasks 1-3 ✅, task 4 ⏳, task 5 ⬜) |
| `config/config.yaml` | Model changed to `qwen3.5:9b` due to local availability; timeout restored to 60s |

## 5. Validations

| Tool | Result |
|------|--------|
| `ruff check .` | 0 errors |
| `mypy .` | 0 errors |
| `pytest tests/` | 39/39 passed |

## 6. Commits Made

| Hash | Message |
|------|---------|
| `3d9e8c7` | add weight-sum validation to decision_engine with fail-fast ErrorConfiguracion |
| `7db5e3f` | fase 3: prompts iniciales del MVP (PRM-001 a PRM-005) |
| `f2d0063` | update historial de sesiones: fase 3 y validacion de pesos |

## 7. Problems Found

1. **Local Ollama performance:** The `qwen3.5:9b` model (6.6 GB) does not fit in the GPU's 4GB VRAM, causing slowness. `qwen3.5:4b` (3.4 GB) was adopted as the local model, which does fit in VRAM.

2. **Hybrid strategy:** The local-only strategy was replaced with a hybrid one: local `qwen3.5:4b` for evaluation + cloud `gemma4:31b` for processing. This required updating `DOC-11`, `ia_service.py`, and the configuration.

3. **Unavailable model:** The originally configured model (`qwen:8b`) is not available on the machine. It was updated to `qwen3.5:4b` as the local model.

## 8. Identified Risks

- The prompts have not been tested with a real LLM, so they may require adjustments in the next testing session
- If the user changes the LLM model in the future, the prompts are designed to be model-independent (CPR-005 from DOC-05), but may require minor adjustments
- The cloud model (`gemma4:31b`) requires an Ollama Cloud API Key and Internet connection; without it, deep processing will not be available

## 9. Observations

- Phase 4 (Discovery) can begin without waiting for the Phase 3 manual test, as they are independent flows
- The `processing/` prompts have a sequential dependency: PRM-002 → PRM-003 → PRM-004 → PRM-005, where each consumes the output of the previous one
- The `initial_evaluation/compatibility` prompt uses the local model (`qwen3.5:4b`) and is optional in Phase 6 — the rule engine (`decision_engine.py`) makes the primary decision
- The `processing/` prompts (PRM-002 to PRM-005) use the cloud model (`gemma4:31b`) for maximum quality

---

*End of report — Version v1 pending manual test and Architect approval.*
