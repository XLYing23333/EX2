from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from Qwen3_8b import llm

# 1. 创建列表解析器
list_parser = CommaSeparatedListOutputParser()

# 2. 创建提示模板（包含格式说明）
template = """
请列举{count}个常见的{item_type}，仅输出编程语言列表。
输出格式要求：{format_instructions}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["count", "item_type"],
    partial_variables={"format_instructions": list_parser.get_format_instructions()}
)


# 4. 创建处理链
chain = prompt | llm | list_parser


result = chain.invoke({"item_type": "编程语言","count": 5})
print(result)