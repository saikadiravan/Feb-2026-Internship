from prompts.match_prompt import match_prompt
from utils.llm import get_llm

llm = get_llm()

matching_chain = match_prompt | llm