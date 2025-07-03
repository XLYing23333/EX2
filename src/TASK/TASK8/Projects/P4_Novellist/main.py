# main.py
import os
from dotenv import load_dotenv
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain.agents import initialize_agent, Tool
import tools  # 导入自定义工具

load_dotenv()

# 初始化LLM
llm = BaseChatOpenAI(
    model='deepseek-ai/DeepSeek-V3',
    openai_api_key=os.getenv('KEY_SF'),
    openai_api_base='https://api.siliconflow.cn/v1',
    max_tokens=1024
)

# 封装自定义工具为LangChain工具
def tool_generate_poem(topic: str):
    prompt = tools.generate_poem(topic)
    return llm.invoke(prompt).content.strip()

def tool_rephrase_text(text: str):
    prompt = tools.rephrase_text(text)
    return llm.invoke(prompt).content.strip()

def tool_doc_save(text: str, filename: str = "output.txt"):
    return tools.doc_save(text, filename)

# 构造LangChain的Tool对象
custom_tools = [
    Tool(
        name="generate_poem",
        func=tool_generate_poem,
        description="根据主题生成七言诗。输入示例：'春天'"
    ),
    Tool(
        name="rephrase_text",
        func=tool_rephrase_text,
        description="对输入文本进行润色。输入示例：'请润色这段话：xxx'"
    ),
    Tool(
        name="doc_save",
        func=tool_doc_save,
        description="将文本保存到指定文件。输入示例：'（文本内容）, output.txt'"
    ),
]

# system_prompt
system_prompt = "你是创意写作助手，擅长文本生成和润色"

# 初始化Agent
agent = initialize_agent(
    tools=custom_tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_message=system_prompt
)

def main():
    while True:
        user_input = input("> ")
        if user_input == "exit":
            break
        output = agent.run(user_input)
        print(output)

if __name__ == "__main__":
    main()