from prompts.explain_prompt import explain_prompt
from utils.llm import get_llm

llm = get_llm()

explanation_chain = explain_prompt | llm