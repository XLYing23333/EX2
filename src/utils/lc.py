def context_init(
    system_prompt: str = 'You are an AI assistant'
):
    context = [{'role': 'system', 'content': system_prompt}]
    return context

def context_input(msg, context: list):
    context.append({'role': 'user', 'content': msg})
