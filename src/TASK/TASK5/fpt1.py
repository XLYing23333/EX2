from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import LengthBasedExampleSelector
from Qwen3_8b import llm

# 定义Few-Shot示例（语言翻译）
examples = [
    {"input": "Hello", "output": "你好"},
    {"input": "Goodbye", "output": "再见"},
    {"input": "Thank you", "output": "谢谢"},
]

# 创建示例模板
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入: {input}\n输出: {output}"
)

# 创建Few-Shot提示模板
prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="将英语翻译成中文:",
    suffix="输入: {input}\n输出:",
    input_variables=["input"],
)

# 执行翻译
input_text = "Welcome"
formatted_prompt = prompt_template.format(input=input_text)
response = llm.invoke(formatted_prompt)

print(f"输入: {input_text}")
print(f"输出: {response.content.strip()}")