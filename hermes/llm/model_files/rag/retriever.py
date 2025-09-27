from llm.model_files.rag.embeddings import load_vectorstore

def retrieve_context(query: str, doc_name : str, k: int = 2) -> str:
    """Busca los chunks más relevantes del documento y devuelve el texto"""
    
    # Cargar FAISS
    db = load_vectorstore(doc_name)

    docs = db.similarity_search(query, k=k)
    return "\n\n".join([d.page_content for d in docs])