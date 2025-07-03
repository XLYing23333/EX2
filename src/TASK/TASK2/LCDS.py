from langchain_openai.chat_models.base import BaseChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

response = llm.invoke("Hi!介绍以下你自己和硅基流动平台")
print(response.content)