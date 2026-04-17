from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate.from_template("""
You are comparing a resume with a job description.

Return:
- matched_skills
- missing_skills

STRICT RULES:
- Only use explicitly mentioned skills
- Do NOT assume anything

Job Description:
{jd}

Resume Data:
{resume_data}

Output format:
{{
  "matched_skills": [],
  "missing_skills": []
}}
""")