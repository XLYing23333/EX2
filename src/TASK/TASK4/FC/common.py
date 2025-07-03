# common.py
import json
from tools.calculator import calculator
from tools.open_app import open_app
from tools.run_cmd import run_cmd

# 工具字典注册
TOOL_FUNC = {
    "calculator": calculator,
    "open_app": open_app,
    "run_cmd": run_cmd
}


def parse_tool_calls(text):
    try:
        # 自动去除markdown、反引号等
        text = text.strip().removeprefix("```json").removesuffix("```").strip('` \n')
        obj = json.loads(text)
        if isinstance(obj, dict) and "name" in obj and "parameters" in obj:
            return [obj]
        elif isinstance(obj, list):
            return obj
    except Exception:
        pass
    return []


def execute_tool_call(tool_call, call_id=None):
    name = tool_call.get('name')
    params = tool_call.get('parameters', {})
    # 参数兼容处理
    if name == "run_cmd":
        # 支持 command、cmd 两种参数名
        if "cmd" not in params and "command" in params:
            params["cmd"] = params.pop("command")
    if name == "open_app":
        if "app" not in params and "app_name" in params:
            params["app"] = params.pop("app_name")
    func = TOOL_FUNC.get(name)
    
    print(f"FUNC: {func.__name__}, PARAMS: {params}")
    
    if func is None:
        return f"未找到工具: {name}"
    try:
        result = func(**params) if isinstance(params, dict) else func(params)
        return str(result)
    except Exception as e:
        return f"{name} 调用失败: {str(e)}"
