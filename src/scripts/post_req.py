import requests

def Chat_OLLAMA(
    prompt: str = "Hi", 
    url: str = "http://localhost:11434/api/chat", 
    model_name: str = 'gemma3:12b',
    output_stream: bool = False
):
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": output_stream
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
    # return response.json()['message']['content']
    
if __name__ == '__main__':
    prompt = input('> ')
    response = Chat_OLLAMA(prompt)
    print(response)
    print("="*50)
    print(response['message']['content'])
    