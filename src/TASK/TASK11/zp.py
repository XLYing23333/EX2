import os
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv

def chat(msg: str):
    load_dotenv()

    os.environ["ZHIPUAI_API_KEY"] = os.getenv('KEY_ZP')

    messages = [
        SystemMessage(content="Your are an AI chatbot."),
        HumanMessage(content=msg)
    ]

    streaming_chat = ChatZhipuAI(
        model="GLM-4-Plus",
        temperature=0.5,
        streaming=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    streaming_chat(messages)

if __name__ == '__main__':
    chat(input('> '))
    

