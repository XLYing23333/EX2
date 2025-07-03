import requests

def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

url = "http://localhost:11434/api/chat"

def llama3(prompt):
    data = {
        "model": "qwen3:8b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['message']['content']

file_path = 'data.txt'
external_data = read_data_from_file(file_path)
prompt = f"Based on the following data: {external_data}, 简述小说内容。"

response = llama3(prompt)
print(response)
