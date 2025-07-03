import json
from system_info import get_system_info

def parse_tool_calls(model_response: str):
    """
    从模型响应中解析工具调用请求
    期望格式:
    <tool_call>
    {
        "name": "get_system_info",
        "parameters": {
            "info_type": "cpu"
        }
    }
    </tool_call>
    """
    start_tag = "<tool_call>"
    end_tag = "</tool_call>"

    if start_tag in model_response and end_tag in model_response:
        # 提取JSON部分
        json_str = model_response.split(start_tag)[1].split(end_tag)[0].strip()
        try:
            tool_call = json.loads(json_str)
            return [tool_call]
        except json.JSONDecodeError:
            print(f"无法解析工具调用JSON: {json_str}")
            return []
    return []

# 自定义工具执行器
def execute_tool_call(tool_call: dict, call_id: str) -> str:
    name = tool_call.get("name")
    params = tool_call.get("parameters", {})

    if name == "get_system_info":
        info_type = params.get("info_type", "all")
        # 调用你定义的获取系统信息方法
        return get_system_info(info_type)
    else:
        return f"未知工具名: {name}"
