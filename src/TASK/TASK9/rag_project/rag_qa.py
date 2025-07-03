import logging

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
from dotenv import load_dotenv




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_vector_db_and_model(vector_db_path='vector_db'):
    logger.info("初始化嵌入模型...")
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    logger.info("加载向量数据库...")
    vectordb = FAISS.load_local(vector_db_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    logger.info("向量数据库加载成功")

    logger.info("初始化聊天模型...")
    chat_model = BaseChatOpenAI(
        model='deepseek-ai/DeepSeek-V3',
        openai_api_key=os.getenv('KEY_SF'),
        openai_api_base='https://api.siliconflow.cn/v1',
        max_tokens=1024
    )
    
    return vectordb, chat_model


def retriever(vectordb, query: str, top_k: int = 5) -> str:
    logger.info(f"正在查询: {query}")
    results = vectordb.similarity_search(query, k=top_k)
    logger.info(f"查询完成，返回 {len(results)} 条结果")

    combined_results = "\n\n".join([f"资料{i+1}: {result.page_content}" for i, result in enumerate(results)])
    return combined_results


def generate_answer(chat_model, question: str, context: str) -> str:
    naive_agent_prompt = f"""
根据下面的问题和支持文档，给出一个全面的答案。
只回答所问的问题，回答应该简洁且与问题相关。
如果你无法找到信息，就如实回答。

Question:
{question}

{context}
    """

    logger.info(f"构造提示词:\n{naive_agent_prompt}")

    response = chat_model.invoke(input=[{"role": "user", "content": naive_agent_prompt}])
    logger.info("模型响应完成")
    return response.content


if __name__ == '__main__':
    load_dotenv()
    vectordb, model = load_vector_db_and_model()

    question = input('> ')
    context = retriever(vectordb, question)
    answer = generate_answer(model, question, context)

    print(f"问题: {question}")
    print(f"答案: {answer}")