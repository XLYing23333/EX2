from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from prompt import ice_cream_prompt_template

llm = ChatOllama(model="qwen3:8b", temperature=0)

llm_chain = LLMChain(llm=llm, prompt=ice_cream_prompt_template)

question = "Who are you?"
print(llm_chain.invoke({'question': question})['text'])