import os
from dotenv import load_dotenv
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain import LLMChain
from langchain.chains import APIChain
from langchain.memory import ConversationBufferMemory

from prompt import (
    ordering_machine_response_prompt,
    api_response_prompt,
    api_url_prompt
)

from api_docs import ordering_api_docs


@cl.on_chat_start
async def start():
    load_dotenv()

    llm = ChatOpenAI(
        model_name='deepseek-ai/DeepSeek-V3',
        api_key=os.getenv('KEY_SF'),
        base_url='https://api.siliconflow.cn/v1',
        streaming=True,
        temperature=0.7,
        max_tokens=1024,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        max_len=200,
    )

    llm_chain = LLMChain(
        llm=llm,
        prompt=ordering_machine_response_prompt,
        memory=memory
    )

    api_chain = APIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=ordering_api_docs,
        api_url_prompt=api_url_prompt,
        api_response_prompt=api_response_prompt,   # ← 用正确的prompt
        verbose=True,
        limit_to_domains=["http://127.0.0.1:1143/"]
        )

    cl.user_session.set("llm_chain", llm_chain)
    cl.user_session.set("api_chain", api_chain)
    cl.user_session.set("memory", memory)


@cl.on_message
async def main(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    api_chain = cl.user_session.get("api_chain")
    memory = cl.user_session.get("memory")

    user_message = message.content.strip().lower()

    api_keywords = ["menu", "customization", "offer", "review"]

    callback_handler = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=[]
    )

    if any(keyword in user_message for keyword in api_keywords):
        response = await api_chain.acall(user_message, callbacks=[callback_handler])
    else:
        response = await llm_chain.acall(user_message, callbacks=[callback_handler])

    if memory:
        memory.chat_memory.add_user_message(message.content)
        if isinstance(response, dict):
            # APIChain返回dict，一般含"output"字段
            output_text = response.get("output") or response.get("text") or str(response)
        else:
            output_text = str(response)
        memory.chat_memory.add_ai_message(output_text)
    # await cl.Message(content=output_text).send()