from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# # 创建一个包含系统消息、历史消息占位符和人类问题的提示模板
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful assistant."),
#     MessagesPlaceholder(variable_name="history"),
#     HumanMessage(content="{question}")
# ])

# # 模拟一些历史消息
# history = [
#     HumanMessage(content="What's the weather today?"),
#     AIMessage(content="It's sunny and warm."),
# ]

# # 调用提示模板，传入历史消息和当前问题
# formatted_prompt = prompt.format_prompt(history=history, question="Can you recommend a good book to read?")
# print(formatted_prompt.to_messages())


# 创建一个包含系统消息、限制为最近一条的历史消息占位符和人类问题的提示模板
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history", n_messages=1),
    HumanMessage(content="{question}")
])

# 模拟多条历史消息
history = [
    HumanMessage(content="What's the weather today?"),
    AIMessage(content="It's sunny and warm."),
    HumanMessage(content="Great, thank you!"),
    AIMessage(content="You're welcome!")
]

# 调用提示模板，传入历史消息和当前问题
formatted_prompt = prompt.format_prompt(history=history, question="Can you tell me something else interesting?")
print(formatted_prompt.to_messages())