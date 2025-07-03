import json
import uuid
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from LCDS import llm
from system_prompt import system_msg
from common import parse_tool_calls, execute_tool_call

# 用户请求
human_message = HumanMessage(content=input('> '))
messages = [system_msg[0], human_message]
print("=== 历史消息 ===")
for m in messages:
    print(m)

response = llm.invoke(messages)
response_content = response.content
print("\n=== LLM 首次回复内容 ===")
print(response_content)

# 检查是否有工具调用
tool_calls = parse_tool_calls(response_content)
if not tool_calls:
    print("\n==== 最终回复：无工具调用请求，exit ====")
    print(response_content)
    exit()

tool_messages = []
for tool_call in tool_calls:
    print(f"\n检测到工具调用: {tool_call['name']}({tool_call['parameters']})")
    call_id = f"call_{uuid.uuid4().hex[:6]}"
    # 执行工具
    
    tool_result = execute_tool_call(tool_call, call_id)
    tool_msg = ToolMessage(tool_call_id=call_id, content=tool_result)
    tool_messages.append(tool_msg)
    messages.append(
        AIMessage(content=response_content,
                  additional_kwargs={
                      "tool_calls": [{
                          "id": call_id,
                          "type": "function",
                          "function": {
                              "name": tool_call["name"],
                              "arguments": json.dumps(tool_call["parameters"], ensure_ascii=False)
                          }
                      }]
                  }))  # 保存原始模型响应

messages.extend(tool_messages)  # 添加工具响应

# 将工具结果发送给模型生成最终回复
final_response = llm.invoke(messages)
print("\n=== AI 最终回复内容 ===")
print(final_response.content)
