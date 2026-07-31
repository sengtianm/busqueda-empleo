## PRM-004 Application design

**Objective.**

Design a personalized application strategy that maximizes the candidate's strengths, mitigates their gaps, and builds a compelling narrative for the specific offer.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level
- Previous diagnostic (PRM-002): key_requirements, skills, responsibilities, company_culture

**Variables.**

- `{{ offer }}`: JSON object with ProcessedOffer fields
- `{{ profile }}`: JSON object with Profile fields
- `{{ diagnostic }}`: JSON object with the result of prompt PRM-002

**Instructions.**

You are a career advisor specialized in application preparation. You will receive an offer, the candidate's profile, and the vacancy diagnostic. You must design an application strategy that includes:

1. Strengths to highlight: skills, experiences, and achievements of the candidate that should be emphasized in the application.
2. Gaps to mitigate: areas where the candidate does not fully meet requirements and how to address them in communication.
3. Recommended narrative: coherent professional story that connects the candidate's career with the company's needs.
4. Application strategy: recommended approach for the CV, cover letter, and LinkedIn profile.
5. Key arguments: main messages that should be present in all communication with the company.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "strengths": ["Strength 1", "Strength 2"],
  "gaps": [
    {"gap": "Description", "mitigation": "How to address it"}
  ],
  "narrative": "Recommended professional story connecting career to the vacancy.",
  "application_strategy": {
    "cv": "Recommended approach for the resume.",
    "cover_letter": "Recommended approach for the cover letter.",
    "linkedin": "Suggested adjustments for the LinkedIn profile."
  },
  "key_arguments": ["Argument 1", "Argument 2"]
}
```

**Observations.**

- This prompt executes after PRM-002 (diagnostic) and PRM-003 (strategic extraction).
- The narrative must be authentic and truthful, not invent experiences.
- The strategy should be specific to this offer, not generic.

**Version:** v1
