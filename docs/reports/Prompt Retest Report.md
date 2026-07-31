# Prompt Retest Report — PRM-001 to PRM-005 (C2 Resolution)

**Project:** Job Search Automation (MVP)
**Date:** 30/07/2026
**Status:** Task completed

---

## 1. Objective

Validate the v2 processing prompts (PRM-002 to PRM-005) and the corrected PRM-001 against the real cloud model (`gemma4:31b-cloud` via local Ollama proxy), confirming:

- The `{{ oferta }}` / `{{ perfil }}` variable injection works (previous session fixed a placeholder mismatch: `{{ offer }}`/`{{ profile }}` did not match the injected variables).
- Each prompt returns valid JSON with the exact fields of the Detailed Evaluation entity (DOC-13A §2.7).
- Catalog values comply with the official catalogs (DOC-13A §3.15/§3.16).
- Generated content complies with the project language convention (Spanish for all stored data).

---

## 2. Activities Performed

### 2.1. Connectivity verification

- Local Ollama running at `http://localhost:11434`.
- `gemma4:31b-cloud` available in the local model list (the local Ollama acts as authenticated proxy to Ollama Cloud; no `config/.env` required).

### 2.2. First real retest (PRM-001 to PRM-005)

| Prompt | JSON valid | Expected fields | Language | Result |
|--------|-----------|-----------------|----------|--------|
| PRM-001 | ✅ | compatibility (ALTA), justification, key_factors, gaps, cultural_compatibility | English | ⚠️ Functionally correct, wrong language |
| PRM-002 | ✅ | resultado_organizacional, problema_organizacional, perfil_profesional_requerido | English | ⚠️ Functionally correct, wrong language |
| PRM-003 | ✅ | coincidencias_perfil, logica_xyz, hipotesis_valor, informacion_descartada | English | ⚠️ Functionally correct, wrong language |
| PRM-004 | ✅ | ajuste_tecnico, justificacion_ajuste_tecnico, ajuste_funcional, justificacion_ajuste_funcional, ajuste_estrategico, justificacion_ajuste_estrategico | English | ⚠️ Functionally correct, wrong language |
| PRM-005 | ✅ | riesgo_sobrecalificacion (Bajo), justificacion_riesgo, recomendacion_final (Aplicar), justificacion_recomendacion, insumos_carta_presentacion | Spanish | ✅ |

**Finding:** Only PRM-005 returned Spanish content, because its JSON example already used Spanish catalog values. Prompts PRM-001 to PRM-004 did not specify an output language, and the model defaulted to English. This violates the project convention that all data persisted in `job_search.db` (including natural-language content) must be in Spanish.

### 2.3. Fix applied

Added the mandatory instruction `All generated content must be written in Spanish.` to the **Observations** section of the 5 prompts:

| File | Prompt |
|------|--------|
| `prompts/initial_evaluation/compatibility.md` | PRM-001 |
| `prompts/processing/diagnostic.md` | PRM-002 |
| `prompts/processing/strategic_extraction.md` | PRM-003 |
| `prompts/processing/application_design.md` | PRM-004 |
| `prompts/processing/inputs.md` | PRM-005 |

### 2.4. Final real retest (PRM-001 to PRM-005)

All 5 prompts executed against the cloud model after the fix. Results:

| Prompt | JSON valid | Expected fields | Catalog values | Language | Result |
|--------|-----------|-----------------|----------------|----------|--------|
| PRM-001 | ✅ | 5/5 | ALTA | Spanish | ✅ |
| PRM-002 | ✅ | 3/3 with sub-structures | — | Spanish | ✅ |
| PRM-003 | ✅ | 4/4 | — | Spanish | ✅ |
| PRM-004 | ✅ | 6/6 (3 scores 0–10 + 3 justifications) | — | Spanish | ✅ |
| PRM-005 | ✅ | 5/5 | Bajo / Aplicar | Spanish | ✅ |

**Content coherence verified:** responses reference the example offer (Senior Data Engineer, fintech, AWS/Spark/Airflow, 65k–85k, remote) and the example profile (8 years, Python/SQL/Spark/AWS, C1, 60k minimum) consistently; the chained reasoning (PRM-002 → PRM-003 → PRM-004 → PRM-005) is preserved in the content of each response.

---

## 3. Validations

| Validation | Result |
|-----------|--------|
| Real execution PRM-001..005 against `gemma4:31b-cloud` | 5/5 valid JSON, Spanish content |
| Unresolved `{{ }}` placeholders in dry-run (5 prompts) | 0/5 prompts with unresolved placeholders |
| Expected fields per prompt (vs DOC-13A §2.7) | 23/23 present |
| Catalog values (ALTA/MEDIA/BAJA, Bajo/Medio/Alto, Aplicar/Aplicar con reservas/No aplicar) | ✅ Used exactly |

*Note: ruff, mypy and pytest were not run — no Python code was modified in this task (only `.md` prompt files).*

---

## 4. Files Modified

| File | Change |
|------|--------|
| `prompts/initial_evaluation/compatibility.md` | Added Spanish output instruction |
| `prompts/processing/diagnostic.md` | Added Spanish output instruction |
| `prompts/processing/strategic_extraction.md` | Added Spanish output instruction |
| `prompts/processing/application_design.md` | Added Spanish output instruction |
| `prompts/processing/inputs.md` | Added Spanish output instruction |

---

## 5. Problems Found

1. **Output language not specified:** PRM-001..004 generated content in English because no output language instruction existed. Fixed by adding a mandatory Spanish instruction to the 5 prompts. PRM-005 only complied because its JSON example used Spanish values — an unreliable mechanism.
2. **PRM-004 justification references stale scores:** in the final retest, `justificacion_recomendacion` (PRM-005) mentions scores 8.5/9.0 from the first PRM-004 run, while the final PRM-004 run returned 9.0/8.5/9.5. Cause: each prompt is tested in isolation with simulated chained inputs (fixtures). This is a test-fixture artifact, not a production defect: in the real pipeline PRM-005 always receives the live PRM-004 output.

---

## 6. Observations

- The placeholder bug fixed in the previous session is confirmed resolved: all prompts now receive the offer/profile data (responses reference real values from the fixtures).
- The cloud path works without `config/.env` because the local Ollama proxy is already authenticated with Ollama Cloud (`ollama login`).
- The retest required no changes to `shared/ia_service.py`, `scripts/prompt_tester.py`, or the fixtures.

---

*End of report — PRM-001..005 validated against the cloud model, pending Architect approval.*
