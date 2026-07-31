## PRM-004 Fit scoring

**Objective.**

Score the fit between the candidate and the vacancy in the three dimensions of the detailed evaluation (technical, functional, and strategic), each with its justification, using a scale from 0 to 10.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level
- Vacancy diagnostic (PRM-002): resultado_organizacional, problema_organizacional, perfil_profesional_requerido
- Fit analysis (PRM-003): coincidencias_perfil, logica_xyz, hipotesis_valor, informacion_descartada

**Variables.**

- `{{ oferta }}`: JSON object with ProcessedOffer fields
- `{{ perfil }}`: JSON object with Profile fields
- `{{ diagnostico }}`: JSON object with the result of prompt PRM-002
- `{{ analisis }}`: JSON object with the result of prompt PRM-003

**Instructions.**

You are an evaluation expert. You will receive the vacancy diagnostic and the candidate fit analysis. You must score the fit in three dimensions on a scale of 0 to 10 (decimals allowed, e.g. 8.5), each with a justification grounded in the evidence:

1. `ajuste_tecnico`: fit of technical skills, technologies, and experience with the required profile.
2. `ajuste_funcional`: fit of the candidate's role, responsibilities, and way of working with the position's demands.
3. `ajuste_estrategico`: fit of the candidate's career direction, seniority, and motivations with the company's organizational result.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "ajuste_tecnico": 8.5,
  "justificacion_ajuste_tecnico": "Justification grounded in the evidence.",
  "ajuste_funcional": 7.0,
  "justificacion_ajuste_funcional": "Justification grounded in the evidence.",
  "ajuste_estrategico": 9.0,
  "justificacion_ajuste_estrategico": "Justification grounded in the evidence."
}
```

**Observations.**

- Scores must be justified with concrete elements of the offer and the profile; no unsubstantiated scores.
- A score without justification must never be produced.
- This scoring feeds the risk, recommendation, and handoff prompt (PRM-005).
- All generated content must be written in Spanish.

**Version:** v2
