import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, Tool
from langchain_openai.chat_models.base import BaseChatOpenAI

from file_tools import code_name_format_tool

load_dotenv()

# 初始化LLM
llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

# 加载通用工具
tools = load_tools([], llm=llm)

# 添加我们的文件名自动补齐工具
tools.append(
    Tool(
        name="code_name_format",
        func=lambda x: code_name_format_tool(x),
        description="自动为目录下所有无扩展名的代码文件补齐扩展名。输入参数为目录路径。"
    )
)

# 初始化Agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_prompt='你是高级文件管理助手，擅长自动化整理文件'
)

if __name__ == "__main__":
    print("请输入操作指令")
    # print("查找test文件夹下所有文件，并根据其代码使用的语言为其重命名出扩展名")
    # print("或者直接输入目录名如 test/")
    while True:
        instr = input("> ")
        if instr.strip() == "exit":
            break
        resp = agent.run(instr)
        print("Agent:", resp)
