from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

model ="qwen3:8b"


def easy_stream():
    # 创建链
    llm = ChatOllama(model)
    prompt = PromptTemplate.from_template("解释 {concept} 及其应用")
    chain = prompt | llm

    # 流式调用
    for chunk in chain.stream({"concept": "深度学习"}):
        print(chunk, end="", flush=True)  # 实时输出
        
def recall_stream():     
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=model,
        callbacks=[StreamingStdOutCallbackHandler()]  # 自动流式输出到控制台
    )

    llm.invoke("用三句话描述人工智能的现状")
    


if __name__ == '__main__':
    # easy_stream()
    recall_stream()
    