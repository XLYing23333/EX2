from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from Qwen3_8b import llm

# 2. 创建提示模板
prompt = PromptTemplate.from_template(
    "用幽默的方式解释以下概念：{concept}"
)

# 3. 创建包含 StrOutputParser 的链
chain = prompt | llm
# chain = prompt | llm | StrOutputParser()


# 4. 调用链并打印结果
response = chain.invoke({"concept": "量子纠缠"})
print(response)