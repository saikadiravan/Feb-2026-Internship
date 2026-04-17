from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate.from_template("""
You are an AI recruiter.

Extract ONLY the following from the resume:
- skills
- tools
- experience (years and roles)

STRICT RULES:
- Do NOT assume anything
- Do NOT add skills not explicitly mentioned
- If something is missing, leave it empty
- Output must be valid JSON only

Resume:
{resume}

Output format:
{{
  "skills": [],
  "tools": [],
  "experience": ""
}}
""")