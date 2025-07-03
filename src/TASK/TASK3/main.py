from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import uuid
import psutil

class MockLLM:
    def invoke(self, messages):
        last = messages[-1]
        if isinstance(last, HumanMessage):
            if "量子" in last.content:
                return AIMessage(content="主要优势在于并行计算能力和解决特定难题（如素因数分解）的速度提升。")
        if any(isinstance(m, SystemMessage) for m in messages):
            return AIMessage(content="1. 电子管计算机\n2. 集成电路\n3. 个人计算机的到来")
        if any(isinstance(m, ToolMessage) for m in messages):
            tm = [m for m in messages if isinstance(m, ToolMessage)][-1]
            return AIMessage(content=f"工具调用({tm.tool_call_id})返回结果为:\n{tm.content}")
        return AIMessage(content="(模拟回答)")

model = MockLLM()

# 基本人类消息对话
messages = [HumanMessage(content="量子计算的主要优势是什么？")]
response = model.invoke(messages)
print("==== 基础对话 ====")
print(f"AI: {response.content}\n")

# 系统消息参与角色定义
messages = [
    SystemMessage(content="你是一位科技史专家，用简短的列表回答问题"),
    HumanMessage(content="列出计算机发展史上的三个重要里程碑")
]
response = model.invoke(messages)
print("==== 带系统提示的对话 ====")
print(f"AI: {response.content}\n")


# 显式AI消息流程演示
print("=== 对话开始 ===")
system_message = SystemMessage(content="你是一个天气助手，用简洁的句子回复用户关于天气的提问。")
user_message = HumanMessage(content="今天北京的天气怎么样？")
ai_response = AIMessage(content="北京今天晴天，气温 25°C，空气质量优。建议穿轻薄衣物。")
print(f"[系统指令]: {system_message.content}")
print(f"[用户]: {user_message.content}")
print(f"[AI助手]: {ai_response.content}")
print("=== 对话结束 ===\n")


# 工具消息
call_id = f"tool_{uuid.uuid4().hex[:8]}"
print(f"工具调用请求ID: {call_id}")

def get_system_info(info_type: str, call_id: str) -> str:
    print( f"正在处理工具调用: {call_id}")
    """获取电脑系统信息"""
    try:
        if info_type == "cpu":
            return f"CPU使用率: {psutil.cpu_percent()}%\n" \
                   f"核心数: {psutil.cpu_count(logical=False)}物理/{psutil.cpu_count()}逻辑"
        elif info_type == "memory":
            mem = psutil.virtual_memory()
            return f"内存使用: {mem.used / 1024 ** 3:.1f}GB/{mem.total / 1024 ** 3:.1f}GB ({mem.percent}%)\n" \
                   f"可用内存: {mem.available / 1024 ** 3:.1f}GB"
        elif info_type == "all":
            return "\n".join([
                get_system_info("cpu", call_id),
                get_system_info("memory", call_id)
            ])
        else:
            return f"未知查询类型: {info_type}"
    except Exception as e:
        return f"查询失败: {str(e)}"

# 模拟工具调用、消息流
messages = [
    HumanMessage(content="查看CPU使用率"),
    SystemMessage(content="你是一个系统监控助手。在回复工具调用结果时，必须在回答中包含工具调用ID（call_id）。"),
    # AIMessage 请求工具
    AIMessage(
        content="",
        tool_calls=[{
            "name": "get_system_info",
            "args": {"info_type": "cpu", "call_id": call_id},
            "id": call_id
        }]
    ),
    ToolMessage(
        tool_call_id=call_id,
        content=get_system_info("cpu", call_id)
    )
]

response = model.invoke(messages)
print("==== 系统信息查询结果 ====")
print(f"AI回复内容: {response.content}\n")

# 演示通用型工具流
messages = [
    HumanMessage(content="旧金山现在的温度是多少？"),
    AIMessage(
        content="",
        tool_calls=[{
            "name": "get_current_weather",
            "args": {"location": "San Francisco"},
            "id": "tool_123"
        }]
    ),
    ToolMessage(
        tool_call_id="tool_123",
        name="get_current_weather",
        content='{"temperature": "22°C", "condition": "Sunny"}'
    )
]
response = model.invoke(messages)
print("==== 工具调用场景 ====")
print(f"AI: {response.content}\n")