from langchain.output_parsers import PydanticOutputParser

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from Qwen3_8b import llm

# 定义目标模型
class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")

parser = PydanticOutputParser(pydantic_object=Person)

template = """
请解析并根据指定格式返回以下个人介绍中的姓名和年龄：
用户输入个人介绍：{introduce}
输出格式 {format_instructions}
"""

prompt = PromptTemplate(
    input_variables=["introduce"],
    template=template,
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


# 知识点生成链
llm_chain = prompt | llm | parser

llm_output = llm_chain.invoke(input={"introduce":"我叫张三，今年30岁"})
print(type(llm_output))
print(llm_output.model_dump_json(indent=2))
