from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate.from_template("""
Explain why the candidate received this score.

Include:
- strengths
- weaknesses
- final reasoning

Do NOT assume anything beyond given data.

Input:
{all_data}

Output in bullet points.
""")