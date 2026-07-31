## PRM-003 Candidate fit analysis

**Objective.**

Analyze the fit between the vacancy diagnostic and the candidate's professional profile: the evidence of match, the X → Y → Z logic, the value hypothesis, and the profile information that does not add value for this vacancy.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level
- Vacancy diagnostic (PRM-002): resultado_organizacional, problema_organizacional, perfil_profesional_requerido

**Variables.**

- `{{ oferta }}`: JSON object with ProcessedOffer fields
- `{{ perfil }}`: JSON object with Profile fields
- `{{ diagnostico }}`: JSON object with the result of prompt PRM-002

**Instructions.**

You are a career strategy expert. You will receive the vacancy diagnostic, the offer, and the candidate's profile. You must analyze the fit between both and produce:

1. `coincidencias_perfil`: the main and complementary evidence demonstrating that the candidate's profile matches the vacancy (capabilities, experiences, achievements, and competencies).
2. `logica_xyz`: the X → Y → Z logic constructed for the application (X: what the company needs; Y: what the candidate has done; Z: the specific value the candidate can generate for this company).
3. `hipotesis_valor`: the value hypothesis that supports the candidacy, phrased as a verifiable claim of the contribution the candidate can make.
4. `informacion_descartada`: professional profile information determined not to add value for this vacancy and that should not be highlighted.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "coincidencias_perfil": {
    "principales": ["Main evidence of fit 1", "Main evidence of fit 2"],
    "complementarias": ["Complementary evidence 1", "Complementary evidence 2"]
  },
  "logica_xyz": "X → Y → Z logic in a single paragraph.",
  "hipotesis_valor": "Value hypothesis that supports the candidacy.",
  "informacion_descartada": ["Discarded information 1", "Discarded information 2"]
}
```

**Observations.**

- The evidence must be truthful: never invent experiences or achievements.
- The logic X → Y → Z must connect the vacancy diagnosis with concrete facts of the candidate.
- This analysis feeds the fit scoring (PRM-004).
- All generated content must be written in Spanish.

**Version:** v2
