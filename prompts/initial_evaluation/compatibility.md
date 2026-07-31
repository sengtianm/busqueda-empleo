## PRM-001 Offer-profile compatibility

**Objective.**

Analyze qualitative compatibility between a processed job offer and the user's professional profile, evaluating aspects not covered by the deterministic rules of the decision engine.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level

**Variables.**

- `{{ offer }}`: JSON object with ProcessedOffer fields
- `{{ profile }}`: JSON object with Profile fields

**Instructions.**

You are an assistant specialized in job compatibility analysis. You will receive a job offer and a candidate's professional profile. You must evaluate the qualitative compatibility between both considering:

1. General alignment: how well the offer fits the candidate's profile in terms of career, aspirations, and work environment.
2. Differentiating factors: aspects of the offer that make it especially attractive or relevant for the candidate.
3. Gaps or risks: areas where the candidate does not fully meet the requirements or where the offer presents disadvantages.
4. Cultural compatibility: affinity with the type of company, industry, values, and work style.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "compatibility": "ALTA|MEDIA|BAJA",
  "justification": "Explanatory text of the overall evaluation.",
  "key_factors": ["Positive factor 1", "Positive factor 2"],
  "gaps": ["Gap or risk 1", "Gap or risk 2"],
  "cultural_compatibility": "Text about the perceived cultural affinity."
}
```

**Observations.**

- This prompt is complementary to the rule-based decision engine. It does not replace the deterministic score.
- The analysis should be qualitative and focused on aspects that rules cannot capture (culture, narrative, context).
- The `compatibility` field must use exactly the values ALTA, MEDIA, or BAJA.

**Version:** v1
