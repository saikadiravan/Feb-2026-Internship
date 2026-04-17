from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate.from_template("""
You are scoring a candidate.

Rules:
- Score must be between 0 and 100
- More matched skills = higher score
- Missing important skills = lower score

IMPORTANT SCORING LOGIC:
- If no required skills are matched → score should NOT be 0
- Give a minimum score (5–20) if candidate has basic or related background (e.g., IT, CS, or technical education)
- Only give 0 if the candidate is completely unrelated to the field

- If most required skills are missing → score should be below 40

Matching Data:
{match_data}

Output format:
{{
  "score": 0
}}
""")