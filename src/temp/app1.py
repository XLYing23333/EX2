from openai import AsyncOpenAI
import chainlit as cl

# 配置OpenAI Client
def get_openai_client():
    OPENAI_API_KEY = "sk-gQXT32OEPANDNDqOSrql4aMh8dOMIitB4FylIaUnsXvwFqxG"
    BASE_URL = "https://api.chatanywhere.tech"
    return AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

client = get_openai_client()
# OpenAI参数
settings = {
    "model": "gpt-4.1-mini",
    "temperature": 0,
}

cl.instrument_openai()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})
    messages = [{"role": "system", "content": "You are a helpful assistant."}] + history

    # 创建初始空内容message，准备流式发送
    msg = cl.Message(content="")
    await msg.send()  # 先发送空消息，后面stream_token逐步追加内容

    full_reply = ""  # 累计助手完整回复
    # 使用OpenAI流式接口
    async for chunk in await client.chat.completions.create(
        messages=messages,
        stream=True,
        **settings
    ):
        # 获取新内容
        delta = chunk.choices[0].delta
        new_content = delta.content if delta and delta.content else ""
        if new_content:
            full_reply += new_content
            await msg.stream_token(new_content)

    # 保存助手回复到历史
    history.append({"role": "assistant", "content": full_reply})
    cl.user_session.set("history", history)