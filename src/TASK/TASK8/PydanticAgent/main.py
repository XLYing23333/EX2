from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import tools
import os
import sys
load_dotenv()


deepseek_provider = OpenAIProvider(
    base_url='https://api.siliconflow.cn/v1',
    api_key=os.getenv('KEY_SF'),
)

model = OpenAIModel(
    'deepseek-ai/DeepSeek-V3',
    provider=deepseek_provider
)
agent = Agent(model,
              system_prompt="You are an experienced programmer",
              tools=[tools.read_file, tools.list_files, tools.rename_file])

def main():
    history = []
    while True:
        user_input = input("Input: ")
        if user_input.lower() in ["quit", "exit", "q", "bye"]:
            sys.exit(0)
        resp = agent.run_sync(user_input,
                              message_history=history)
        history = list(resp.all_messages())
        print(resp.output)


if __name__ == "__main__":
    main()
