import chainlit as cl
from langchain.memory.buffer import ConversationBufferMemory
from prompt import ice_cream_assistant_prompt_template
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain


@cl.on_chat_start
def query_llm():
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=200,
                                                   return_messages=True,
                                                   )
    llm = ChatOllama(model="qwen3:8b", temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=ice_cream_assistant_prompt_template, memory=conversation_memory)
    cl.user_session.set("llm_chain", llm_chain)

 
 
@cl.on_message
async def handle_message(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")

    response = await llm_chain.acall(message.content,
                                     callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(response["text"]).send()
   
