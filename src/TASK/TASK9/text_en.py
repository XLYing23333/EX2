import chromadb
from langchain_ollama import OllamaEmbeddings
import sys
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
# 设置支持中文的字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False


chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection("rag_tiny")

ollama_emb = OllamaEmbeddings(model="nomic-embed-text:latest")


def create_db(documents: list[str]) -> None:
    r1 = ollama_emb.embed_documents(documents)
    print("embed:",r1)
    chromadb_collection.upsert (
        ids=["1", "2"],
        documents=documents,
        embeddings=r1
    )
    
def query_db(question: str) -> list[str]:
    r2 = ollama_emb.embed_query(question)
    print("query:",r2)
    result = chromadb_collection.query(
        query_embeddings=r2,
        n_results=1
    )
    return result["documents"][0]

def vector_visual(embeddings,  texts):
    
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    # 可视化
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    for i, (x, y) in enumerate(reduced):
        ax.scatter(x, y, color='blue')
        ax.text(x + 0.02, y + 0.02, texts[i][:10], fontsize=9)
    ax.set_aspect('equal')
    plt.show()

   
if __name__ == '__main__':
    documents = ["Alpha is the first letter of Greek alphabet",
                 "Beta is the second letter of Greek alphabet", ]

    question = "What is the second letter of Greek alphabet"

    create_db(documents)
    print("=================================================")
    chunks = query_db(question)
    print("=================================================")
    print(chunks)
    print("END")
    embeddings = chromadb_collection.get(include=["embeddings"])["embeddings"][:50]
    texts = chromadb_collection.get(include=["documents"])["documents"][:50]
    vector_visual(embeddings, texts)
    sys.exit(0)
