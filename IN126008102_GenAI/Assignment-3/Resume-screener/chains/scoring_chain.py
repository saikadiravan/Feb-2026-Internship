from prompts.score_prompt import score_prompt
from utils.llm import get_llm

llm = get_llm()

scoring_chain = score_prompt | llm