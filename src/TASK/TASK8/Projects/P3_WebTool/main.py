
import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, Tool
from langchain_openai.chat_models.base import BaseChatOpenAI

from tools import scrape_website

# 加载环境变量
load_dotenv()

# 初始化LLM
llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

# 定义网页抓取工具
scrape_tool = Tool(
    name="scrape_website",
    func=scrape_website,
    description="抓取指定URL的网页纯文本内容。例如：输入一个新闻网页URL，会返回网页的正文文本。"
)

# 可按需添加其他工具
# tools = load_tools(["llm-math"], llm=llm) + [scrape_tool]
tools = [scrape_tool]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_prompt='你是网页操作专家，擅长自动化网页任务。'
)

def main():
    print("==== 🌐 网页摘要小助手 ====")
    print("请输入网页URL，自动生成内容摘要。")
    while True:
        url = input('输入URL（或q退出）：').strip()
        if url.lower() in ['q', 'quit', 'exit']:
            break
        if not url.startswith('http'):
            print("请输入正确的URL（以http/https开头）")
            continue
        # Agent自动抓取，并总结
        prompt = f"请抓取这个网页的内容并给出简要摘要：{url}"
        result = agent.run(prompt)
        print("\n------ 摘要 ------\n")
        print(result)
        print("\n==================\n")

if __name__ == "__main__":
    main()
