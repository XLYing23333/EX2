from langchain_openai import OpenAI
from langchain.chains import LLMChain, APIChain
from prompt import ice_cream_assistant_prompt_template, api_response_prompt, api_url_prompt
from langchain.memory.buffer import ConversationBufferMemory
from api_docs import scoopsie_api_docs
import chainlit as cl
from langchain_community.chat_models import ChatOllama


@cl.on_chat_start
def setup_multiple_chains():
    llm = ChatOllama(model="qwen3:8b", temperature=0)
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=200,
                                                   return_messages=True,
                                                   )
    llm_chain = LLMChain(llm=llm, prompt=ice_cream_assistant_prompt_template, memory=conversation_memory)
    cl.user_session.set("llm_chain", llm_chain)

    api_chain = APIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=scoopsie_api_docs, # 描述可用的 API 接口信息
        api_url_prompt=api_url_prompt, # 指导模型生成 API URL
        api_response_prompt=api_response_prompt, # 指导模型将 API 响应转为自然语言
        verbose=True,
        limit_to_domains=["http://127.0.0.1:1143/"] # 白名单域名，防止调用非法 API
    )
    cl.user_session.set("api_chain", api_chain)


@cl.on_message
async def handle_message(message: cl.Message):
    user_message = message.content.lower()
    llm_chain = cl.user_session.get("llm_chain")
    api_chain = cl.user_session.get("api_chain")

    if any(keyword in user_message for keyword in ["menu", "customization",
                                                   "offer", "review"]):
        # If any of the keywords are in the user_message, use api_chain
        response = await api_chain.acall(user_message,
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])
    else:
        # Default to llm_chain for handling general queries
        response = await llm_chain.acall(user_message,
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])

    response_key = "output" if "output" in response else "text"
    await cl.Message(response.get(response_key, "")).send()