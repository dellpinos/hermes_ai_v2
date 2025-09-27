import os
from llm.model_files.rag.embeddings import create_vectorstore

# from ai_models.hermes.rag.embeddings import create_vectorstore

def make_documents_list():
    
    DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "docs")
    file_names = [
        os.path.splitext(f)[0]  # elimina extensión
        for f in os.listdir(DOCS_FOLDER)
        if os.path.isfile(os.path.join(DOCS_FOLDER, f)) and f.endswith(".md")
    ]
    return file_names

def vectorize_docs():
    
    docs_names = make_documents_list()
    
    for doc in docs_names:
        create_vectorstore(doc)
        

# Call to the vectorize
vectorize_docs()