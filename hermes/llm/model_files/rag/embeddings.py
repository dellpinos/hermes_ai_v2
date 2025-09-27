import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from llm.model_files.rag.loader import load_docs

# VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), "vectorstore")

BASE_VECTORSTORE_PATH = os.path.join(os.path.dirname(__file__), "vectorstores")
os.makedirs(BASE_VECTORSTORE_PATH, exist_ok=True) # It creates the dir vectorstores if it doesn't exist

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def create_vectorstore(doc_name: str):
    # docs = load_docs()
    docs = load_docs(doc_name)  # le paso el nombre del archivo
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    db = FAISS.from_documents(docs, embeddings)
    
    # db.save_local(VECTORSTORE_PATH)
    
    vectorstore_path = os.path.join(BASE_VECTORSTORE_PATH, f"{doc_name}_faiss")
    db.save_local(vectorstore_path)
    
    print(f"✅ Vectorstore guardado en {vectorstore_path}")

def load_vectorstore(doc_name: str):
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore_path = os.path.join(BASE_VECTORSTORE_PATH, f"{doc_name}_faiss")
    return FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
