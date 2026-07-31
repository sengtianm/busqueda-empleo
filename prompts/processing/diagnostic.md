## PRM-002 Vacancy diagnostic

**Objective.**

Diagnose the vacancy in depth: the organizational result the company pursues, the organizational problem behind the offer, and the professional profile required to occupy the position.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years

**Variables.**

- `{{ oferta }}`: JSON object with ProcessedOffer fields

**Instructions.**

You are an expert job analyst. You will receive the data of a processed job offer. You must produce the vacancy diagnostic that feeds the detailed evaluation of the application:

1. `resultado_organizacional`: the main organizational result the company pursues by filling the position and the secondary results that accompany it.
2. `problema_organizacional`: the main organizational problem that justifies the vacancy, the problems explicitly stated in the offer, the problems inferred from the description, and the aspects that cannot be determined.
3. `perfil_profesional_requerido`: the critical capabilities, way of thinking, experiences, and competencies required for the position, distinguishing what is truly indispensable from what is merely desirable.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "resultado_organizacional": {
    "principal": "Main organizational result the company pursues.",
    "secundarios": ["Secondary result 1", "Secondary result 2"]
  },
  "problema_organizacional": {
    "principal": "Main organizational problem that justifies the vacancy.",
    "explicitos": ["Problem explicitly stated in the offer"],
    "inferidos": ["Problem inferred from the description"],
    "no_determinables": ["Aspect that cannot be determined"]
  },
  "perfil_profesional_requerido": {
    "capacidades_criticas": ["Critical capability 1", "Critical capability 2"],
    "forma_de_pensar": ["Way of thinking 1", "Way of thinking 2"],
    "experiencias": ["Required experience 1", "Required experience 2"],
    "competencias": ["Competency 1", "Competency 2"]
  }
}
```

**Observations.**

- Distinguish clearly between mandatory and desirable requirements.
- The diagnostic must be truthful: infer only what the offer supports.
- This diagnostic feeds the candidate fit analysis (PRM-003).
- All generated content must be written in Spanish.

**Version:** v2
