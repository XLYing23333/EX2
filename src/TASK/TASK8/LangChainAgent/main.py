from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, Tool
import os
from dotenv import load_dotenv

load_dotenv()

# 初始化LLM
from langchain_openai.chat_models.base import BaseChatOpenAI

llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

# 初始化LLM和工具
tools = load_tools(["llm-math"], llm=llm)  # 基础计算器工具

# 添加自定义工具（如百度搜索）
def custom_search(query: str) -> str:
    return "模拟搜索结果: " + query

tools.append(
    Tool(name="Search", func=custom_search, description="通用搜索工具")
)

# 使用通用ReAct代理
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",  
    verbose=True
)

# agent.run("3的平方是多少？")
agent.run(input('> '))