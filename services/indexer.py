from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.documents import Document
from core.config import settings
from loguru import logger

def get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_URL
    )

def index_documents(docs: list[Document], index_name: str = "knowledge_base"):
    """
    Chunks documents and indexes them into Elasticsearch.
    """
    logger.info("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    
    chunks = text_splitter.split_documents(docs)
    logger.info(f"Split into {len(chunks)} chunks.")
    
    embeddings = get_embeddings()
    
    logger.info(f"Indexing to Elasticsearch at {settings.ELASTICSEARCH_URL} into index '{index_name}'...")
    try:
        db = ElasticsearchStore.from_documents(
            chunks,
            embeddings,
            es_url=settings.ELASTICSEARCH_URL,
            index_name=index_name,
            # We don't have basic auth enabled in our dev compose for now
        )
        logger.info("Indexing complete.")
        return db
    except Exception as e:
        logger.error(f"Failed to index documents: {e}")
        raise
