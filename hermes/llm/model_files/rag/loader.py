import os
# from transformers import AutoTokenizer
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document

from llm.model_files.model import llm


# # Nombre del documento (sin extensión)
# DOCUMENT_NAME = "tlw_docs"

# # Ruta absoluta al archivo .md
# DOC_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", f"{DOCUMENT_NAME}.md")

# Tokenizer oficial de Llama
# MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)


def count_tokens(text):
    """Cuenta tokens de un texto usando llama.cpp"""
    tokens = llm.tokenize(text.encode("utf-8"))
    return len(tokens)


def split_text(text, max_tokens=50):
    """Divide un texto largo en chunks usando llama.cpp"""
    tokens = llm.tokenize(text.encode("utf-8"))
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        piece = tokens[i:i+max_tokens]
        chunk = llm.detokenize(piece).decode("utf-8", errors="ignore")
        chunks.append(chunk)
    return chunks


def load_docs(doc_name: str):
    """Carga y divide el documento .md en objetos Document de LangChain"""
    DOC_PATH = os.path.join(os.path.dirname(__file__), "docs", f"{doc_name}.md")
    
    loader = TextLoader(DOC_PATH, encoding="utf-8")
    documents = loader.load()

    full_text = documents[0].page_content
    chunks = split_text(full_text, max_tokens=70)

    return [Document(page_content=chunk) for chunk in chunks]

