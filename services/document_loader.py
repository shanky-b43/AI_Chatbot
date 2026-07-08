import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from loguru import logger

def load_document(file_path: str) -> list[Document]:
    """
    Loads a document (PDF or TXT) and returns LangChain Document objects.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} pages from PDF: {file_path}")
            return docs
        elif ext in [".txt", ".md", ".csv"]:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
            logger.info(f"Loaded text document: {file_path}")
            return docs
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    except Exception as e:
        logger.error(f"Failed to load document {file_path}: {e}")
        raise
