from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from Qwen3_8b import llm


# 定义情感分析示例
examples = [
    {"text": "这部电影太棒了！特效超震撼", "sentiment": "积极"},
    {"text": "这个餐厅的服务真差，等了一个小时", "sentiment": "消极"},
    {"text": "今天天气还可以，适合散步", "sentiment": "中性"},
]

# 创建示例模板
example_template = """
文本: {text}
情感: {sentiment}
"""

# 创建Few-Shot提示模板
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate(
        input_variables=["text", "sentiment"],
        template=example_template
    ),
    prefix="请分析以下文本的情感倾向（积极/消极/中性）:",
    suffix="文本: {input}\n情感:",
    input_variables=["input"]
)

# 创建LLM链
chain = LLMChain(llm=llm, prompt=prompt)

# 测试情感分析
test_text = "这个手机的电池续航太差了，用了半天就没电了"
result = chain.run(input=test_text)

print(f"文本: {test_text}")
print(f"情感: {result.strip()}")