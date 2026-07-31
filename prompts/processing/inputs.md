## PRM-005 Application inputs

**Objective.**

Generate concrete resources to support the application: a cover letter draft and an interview preparation guide.

**Inputs.**

- ProcessedOffer: clean_title, clean_description, salary_min, salary_max, currency, clean_location, modality, requirements, technologies, languages, experience_years
- Profile: technologies, experience_years, languages, preferred_locations, preferred_modalities, minimum_salary, seniority, target_companies, excluded_companies, education_level
- Application strategy (PRM-004): strengths, gaps, narrative, key_arguments

**Variables.**

- `{{ offer }}`: JSON object with ProcessedOffer fields
- `{{ profile }}`: JSON object with Profile fields
- `{{ strategy }}`: JSON object with the result of prompt PRM-004

**Instructions.**

You are a professional writer specialized in job application resources. You will receive an offer, the candidate's profile, and the application strategy. You must generate:

1. Cover letter draft: professional and persuasive text (maximum 300 words) that the candidate can personalize. It must follow the narrative and arguments defined in the strategy.
2. Interview preparation: guide with likely questions, suggested answers, and specific tips for this offer.
3. Key questions for the candidate: questions the candidate should ask the employer during the interview to demonstrate interest and discern if the offer is suitable.

Respond strictly in JSON format without additional text. Do not include Markdown code blocks.

**Expected output.**

```json
{
  "cover_letter_draft": "Full cover letter text in Markdown format.",
  "interview_preparation": {
    "introduction": "General interview advice.",
    "likely_questions": [
      {"question": "¿...?", "suggested_answer": "Response approach..."}
    ],
    "tips": ["Tip 1", "Tip 2"]
  },
  "key_questions": [
    {"question": "¿...?", "purpose": "What information to obtain with this question."}
  ]
}
```

**Observations.**

- The letter should be a customizable draft, not a final text. The user should review and adapt it.
- The interview questions should demonstrate prior research about the company and the role.
- This prompt executes at the end of the processing chain (after PRM-002, PRM-003, PRM-004).

**Version:** v1
