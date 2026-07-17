import os
import sys
import argparse
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from loguru import logger

# Add parent directory to sys.path so we can    import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.indexer import index_documents

def ingest_directory(directory_path: str):
    """
    Reads all text and PDF files from a directory and indexes them into Elasticsearch.
    """
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        logger.error(f"Directory {directory_path} does not exist.")
        return

    documents = []
    
    # Supported file extensions
    for ext in ["*.txt", "*.md", "*.pdf"]:
        for file_path in path.rglob(ext):
            logger.info(f"Loading {file_path}")
            try:
                if file_path.suffix.lower() == ".pdf":
                    loader = PyPDFLoader(str(file_path))
                else:
                    loader = TextLoader(str(file_path), encoding="utf-8")
                
                docs = loader.load()
                # Add workflow/department metadata based on parent folder if you want
                # e.g., data/hr/policy.pdf -> doc.metadata['department'] = 'hr'
                department = file_path.parent.name
                for d in docs:
                    d.metadata["department"] = department
                    
                documents.extend(docs)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

    if not documents:
        logger.warning(f"No documents found in {directory_path}")
        return

    logger.info(f"Loaded {len(documents)} document pages/files. Starting indexing...")
    
    # Store everything in the default 'knowledge_base' index
    index_documents(documents, index_name="knowledge_base")
    logger.info("Successfully ingested all documents!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into Elasticsearch.")
    parser.add_argument("data_dir", type=str, help="Path to the directory containing documents (e.g., ./data)")
    
    args = parser.parse_args()
    ingest_directory(args.data_dir)
