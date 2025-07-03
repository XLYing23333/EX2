from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from pprint import pprint


template = """
你是一个资深产品经理，请为{product}撰写一段推广文案。
要求：
- 突出产品核心优势
- 使用{tone}的语言风格
- 不超过50字
"""

# 显式定义输入变量
prompt = PromptTemplate(
    input_variables=["product", "tone"],
    template=template
)

# 单行创建（自动提取{framework}和{function}）
auto_prompt = PromptTemplate.from_template(
   """
    你是一个资深产品经理，请为{product}撰写一段推广文案。
    要求：
    - 突出产品核心优势
    - 使用{tone}的语言风格
    - 不超过50字
    """)
# print(prompt.input_variables)
# print(auto_prompt.input_variables)


chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是{domain}专家，用{level}级别术语回答"),
    ("human", "解释什么是{concept}"),
    ("ai", "好的，我会从{aspect}角度解释")
])

# 生成对话提示
messages = chat_template.format_messages(
    domain="量子物理",
    level="本科生",
    concept="量子纠缠",
    aspect="数学原理"
)

pprint(messages)

# 输出结构化消息
for msg in messages:
    pprint(f"{msg.type}: {msg.content}")



# 复用之前的聊天模板
prompt_value = chat_template.format_prompt(
    domain="量子物理",
    level="本科生",
    concept="量子纠缠",
    aspect="数学原理"
)
print(prompt_value)

# 转换输出
print("--- 文本模式 ---")
print(prompt_value.to_string())  # 单字符串

print("\n--- 消息模式 ---")
for msg in prompt_value.to_messages():
    print(f"[{msg.type.upper()}] {msg.content}")  # 结构化消息
    

text_prompt = PromptTemplate.from_template(
    "将'{text}'翻译成{language}，保留专业术语"
)

result = text_prompt.format(
    text="Artificial Intelligence", 
    language="法语"
)

print(type(result))  # <class 'str'>
print(result)        # 将'Artificial Intelligence'翻译成法语，保留专业术语