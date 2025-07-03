# main.py
import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, Tool
from langchain_openai.chat_models.base import BaseChatOpenAI

from tools import make_col_plot_tool

# 加载环境变量
load_dotenv()

# 初始化 LLM
llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

# 加载内置计算器工具
tools = load_tools(["llm-math"], llm=llm)
# 添加自定义的绘图工具
tools.append(make_col_plot_tool)

# 可选添加通用搜索工具
def custom_search(query: str) -> str:
    return "模拟搜索结果: " + query

tools.append(
    Tool(name="Search", func=custom_search, description="通用搜索工具")
)

# 组装 Agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_message="你是数据分析专家，擅长处理CSV/Excel数据"  # 可显式加入系统提示
)

if __name__ == "__main__":
    print("欢迎使用数据小助手！举例：分析 sales.csv，生成每列 plot 图")
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = agent.run(user_input)
        print(result)