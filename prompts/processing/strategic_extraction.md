## PRM-003 Strategic extraction

**Objective.**

Identify the strategic elements of a job offer in relation to the candidate's profile: differentiating factors, negotiable requirements, risks, and opportunities for the application.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level

**Variables.**

- `{{ offer }}`: JSON object with ProcessedOffer fields
- `{{ profile }}`: JSON object with Profile fields

**Instructions.**

You are a career strategy expert. You will receive a job offer and a candidate's profile. You must extract strategic information to maximize the chances of success in the process:

1. Differentiating factors: aspects of the offer or the candidate's profile that can make a difference compared to other applicants.
2. Negotiable requirements: offer requirements where the candidate could compensate with equivalent experience, training, or transferable skills.
3. Risks: aspects that could work against the candidate (lack of experience in a key area, technological gap, etc.).
4. Opportunities: elements of the offer that represent a growth or learning opportunity for the candidate.
5. Recommended positioning: suggested general strategy for approaching the application.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "differentiators": ["Differentiator 1", "Differentiator 2"],
  "negotiable_requirements": [
    {"requirement": "Description", "strategy": "How to compensate"}
  ],
  "risks": [
    {"risk": "Description", "severity": "high|medium|low"}
  ],
  "opportunities": ["Opportunity 1", "Opportunity 2"],
  "positioning": "Recommended general strategy for the application."
}
```

**Observations.**

- Risks should be prioritized by severity to focus mitigation efforts.
- The positioning should be actionable: what emphasis to give the application.
- This prompt executes after the vacancy diagnostic (PRM-002).

**Version:** v1
