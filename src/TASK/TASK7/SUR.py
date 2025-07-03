# from langchain_community.chat_models import ChatOllama
import requests
import json
url = "http://localhost:11434/api/chat"

def Qwen3():
    data = {
        "model": "qwen3:8b",
        "messages": [
            {
                "role": "user",
                "content": "你是谁？"
            }
        ],
        "stream": True
    }
    headers = {
        'Content-Type': 'application/json',
        # "Accept": "text/event-stream"
    }

    # 使用 stream=True 并配合 iter_lines() 处理流式数据
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                try:
                    # 每一行单独解析为JSON
                    json_line = json.loads(line.decode('utf-8'))
                    print(json.dumps(json_line, indent=4, ensure_ascii=False))
                except json.JSONDecodeError as e:
                    print(f"无法解析JSON: {e}")
                    continue

Qwen3()

# Ollama返回的内容类型为 application/json 流，
# 不是标准的 Server-Sent Events (SSE)。
