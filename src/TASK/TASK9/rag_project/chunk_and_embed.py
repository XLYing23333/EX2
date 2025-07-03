import logging
from pathlib import Path
from tqdm import tqdm

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings


def chunk_and_embed(output_dir='output', vector_db_path='vector_db'):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("开始加载文档...")
    output_dir = Path(output_dir)
    source_docs = []

    for file_path in output_dir.glob("*.txt"):
        try:
            loader = TextLoader(str(file_path), encoding='utf-8')
            docs = loader.load()
            source_docs.extend(docs)
            logger.info(f"已加载文件: {file_path.name}")
        except Exception as e:
            logger.error(f"加载文件 {file_path} 时出错: {str(e)}")

    logger.info(f"共加载了 {len(source_docs)} 个文档")

    # 初始化文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # 每个文档块的大小
        chunk_overlap=100,  # 块之间重叠的大小
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    logger.info("开始分割文档...")
    docs_processed = []
    unique_texts = set()

    for doc in tqdm(source_docs):
        new_docs = text_splitter.split_documents([doc])
        for new_doc in new_docs:
            content = new_doc.page_content.strip()
            if content not in unique_texts and content != "":
                unique_texts.add(content)
                docs_processed.append(new_doc)

    logger.info(f"已处理 {len(docs_processed)} 个唯一文档块")

    # 初始化嵌入模型
    logger.info("正在初始化嵌入模型...")
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    # 创建向量数据库
    logger.info("正在创建向量数据库...")
    vectordb = FAISS.from_documents(
        documents=docs_processed,
        embedding=embedding_model
    )

    vectordb.save_local(vector_db_path)
    logger.info(f"向量数据库已保存到: {vector_db_path}")


if __name__ == '__main__':
    chunk_and_embed()