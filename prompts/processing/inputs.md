## PRM-005 Risk, recommendation and handoff

**Objective.**

Conclude the detailed evaluation: assess the overqualification risk, issue the final recommendation on whether to apply, and summarize the strategic inputs that will feed the cover letter construction phase.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level
- Vacancy diagnostic (PRM-002): resultado_organizacional, problema_organizacional, perfil_profesional_requerido
- Fit analysis (PRM-003): coincidencias_perfil, logica_xyz, hipotesis_valor, informacion_descartada
- Fit scoring (PRM-004): ajuste_tecnico, justificacion_ajuste_tecnico, ajuste_funcional, justificacion_ajuste_funcional, ajuste_estrategico, justificacion_ajuste_estrategico

**Variables.**

- `{{ oferta }}`: JSON object with ProcessedOffer fields
- `{{ perfil }}`: JSON object with Profile fields
- `{{ diagnostico }}`: JSON object with the result of prompt PRM-002
- `{{ analisis }}`: JSON object with the result of prompt PRM-003
- `{{ puntuaciones }}`: JSON object with the result of prompt PRM-004

**Instructions.**

You are a senior career advisor. You will receive the vacancy diagnostic, the fit analysis, and the fit scoring. You must produce the conclusion of the detailed evaluation:

1. `riesgo_sobrecalificacion`: overqualification risk level — `Bajo`, `Medio`, or `Alto` — based on the candidate's seniority and experience versus the position's requirements.
2. `justificacion_riesgo`: justification for the assigned risk level.
3. `recomendacion_final`: final recommendation — `Aplicar`, `Aplicar con reservas`, or `No aplicar` — weighing scores, risks, and the candidate's professional criteria.
4. `justificacion_recomendacion`: justification for the final recommendation.
5. `insumos_carta_presentacion`: summary of strategic inputs for the cover letter construction phase: the central message, key arguments, experiences to highlight, and aspects to mitigate.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "riesgo_sobrecalificacion": "Bajo|Medio|Alto",
  "justificacion_riesgo": "Justification for the assigned risk level.",
  "recomendacion_final": "Aplicar|Aplicar con reservas|No aplicar",
  "justificacion_recomendacion": "Justification for the final recommendation.",
  "insumos_carta_presentacion": {
    "mensaje_central": "Central message of the candidacy.",
    "argumentos_clave": ["Key argument 1", "Key argument 2"],
    "experiencias_a_destacar": ["Experience to highlight 1"],
    "aspectos_a_mitigar": ["Aspect to mitigate 1"]
  }
}
```

**Observations.**

- The recommendation must be consistent with the scores and the candidate's professional criteria; it is advisory, never binding.
- The cover letter inputs must be specific to this vacancy, not generic.
- This prompt concludes the processing chain (after PRM-002, PRM-003, PRM-004). The cover letter draft and interview preparation belong to a later document generation phase.
- All generated content must be written in Spanish.

**Version:** v2
