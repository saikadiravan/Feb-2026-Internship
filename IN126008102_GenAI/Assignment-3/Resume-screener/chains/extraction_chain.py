from prompts.extract_prompt import extract_prompt
from utils.llm import get_llm

llm = get_llm()

extraction_chain = extract_prompt | llm