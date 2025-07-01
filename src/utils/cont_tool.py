import os
import random

def welcome_text():
    text_ls = [
        "Hello! 😊 How can I help you today?",
        "Hi there! 👋 Ready to chat?",
        "Welcome! 🌟 What brings you here today?",
        "Hey! 😃 Need any assistance?",
        "Good to see you! 🙌 What’s on your mind?",
        "Hi! 👋 Let’s get started!",
        "Greetings! 🤗 How may I assist you?",
        "Welcome aboard! 🚀 How can I help?",
        "Howdy! 🤠 What can I do for you today?",
        "Hello there! 😀",
        "Hey friend! 🫱 How can I support you?",
        "Nice to meet you! 🤝 What do you want to know?",
        "Hey! 😄 Got a question for me?",
        "Hi! 🖐 How can I make your day better?",
        "Hello! 😺 Ready to start our chat?",
        "Good day! 🥳 Let me know how I can help.",
        "Salutations! 😁 What can I assist you with?",
        "Welcome! ❤️ How can I serve you today?",
        "Hi! 🌈 Ask me anything!",
        "Greetings! 👨‍💻 Need help with something?",
        "Hello again! 🔄 Ready for another chat?",
        "Hey! 🐣 Eager to help you today.",
        "Hi there! 💡 What’s on your mind?",
        "Welcome! 🍀 Hope you're having a great day!",
        "Hello! 🪄 Let's solve your problems together.",
        "Greetings! 🔔 How can I assist?",
        "Hey! 🎉 Any questions for me?",
        "Hello! 📚 Ask me anything you like.",
        "Hi! 🌻 How can I guide you today?",
        "Welcome! 🥰 Excited to chat with you.",
    ]
    return random.choice(text_ls)

def context_init(
    system_prompt: str = 'You are an AI assistant'
):
    context = [{'role': 'system', 'content': system_prompt}]
    return context

def context_append(
    context: list,
    role: str, 
    msg: str,
):
    context.append({'role': role, 'content': msg})
    return context

def context_user(
    context: list,
    msg: str,
):
    context = context_append(context, 'user', msg)
    return context

def context_assistant(
    context: list,
    msg: str,
):
    context = context_append(context, 'assistant', msg)
    return context

if __name__ == '__main__':
    print(welcome_text())
    context = context_init()
    print(context)
    context = context_user(context, 'How are you?')
    print(context)
    context = context_assistant(context, 'I am doing well, thank you for asking.')
    print(context)
    