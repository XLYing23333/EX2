import asyncio
import os
import sys
from openai import OpenAI, AsyncOpenAI
from utils.config import get_model_info




def get_client_and_id(model_name):
    model_info = get_model_info(model_name)
    OPENAI_API_KEY = model_info['key']
    BASE_URL = model_info['URL']
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)
    async_client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)
    return client, async_client, model_info['ID']
    


def context_init(
    system_prompt: str = 'You are an AI assistant'
):
    context = [{'role': 'system', 'content': system_prompt}]
    return context

def chat_normal(model_name, context: list):
    """
    Normal Chat
    """
    client, _, model = get_client_and_id(model_name)
    completion = client.chat.completions.create(
        model=model,
        messages=context
    )
    reply = completion.choices[0].message.content
    context.append({'role': 'assistant', 'content': reply})
    return reply

async def chat_stream(model_name, context: list):
    """
    Stream Chat
    Group: OLLAMA / CA(OpenAI), SF(SiliconFlow)
    """
    full_reply = ""
    _, async_client, model = get_client_and_id(model_name)
    stream = await async_client.chat.completions.create(
        model=model,
        messages=context,
        stream=True,
    )
    async for chunk in stream:
        if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], "delta"):
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                print(content, end="", flush=True)
                full_reply += content
    print()
    context.append({'role': 'assistant', 'content': full_reply})
    return full_reply

def demo(model_name):
    context = context_init()
    loop = asyncio.get_event_loop()
    while True:
        msg = input("> ")
        if msg.lower() in ('q', 'exit', 'quit'):
            sys.exit(0)
        mode = input("Stream?(y): ").lower()
        if mode == 'y':
            res = loop.run_until_complete(chat_stream(model_name, context))
            print('GPT: ', res)
        else:
            reply = chat_normal(model_name, context)
            print('GPT: ', reply)
        print('\nCONTEXT: ', context)

if __name__ == "__main__":
    pass
# TODO: add user content to context
