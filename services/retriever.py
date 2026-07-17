from langchain_elasticsearch import ElasticsearchStore
from core.config import settings
from services.indexer import get_embeddings
from loguru import logger

def get_retriever(index_name: str = "knowledge_base", sub_node: str = None):
    """
    Returns a LangChain retriever for the given Elasticsearch index.
    """
    logger.info(f"Connecting to Elasticsearch store '{index_name}' for retrieval.")
    try:
        db = ElasticsearchStore(
            es_url=settings.ELASTICSEARCH_URL,
            index_name=index_name,
            embedding=get_embeddings()
        )
        search_kwargs = {"k": 4}
        if sub_node:
            search_kwargs["filter"] = [{"term": {"metadata.sub_node.keyword": sub_node}}]
        return db.as_retriever(search_kwargs=search_kwargs)
    except Exception as e:
        logger.error(f"Failed to initialize retriever: {e}")
        raise

def retrieve_context(query: str, index_name: str = "knowledge_base", sub_node: str = None) -> str:
    """
    Utility function to retrieve and format context directly.
    """
    retriever = get_retriever(index_name, sub_node=sub_node)
    docs = retriever.invoke(query)
    
    if not docs:
        return "No relevant context found."
        
    formatted_context = "\n\n".join([f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in docs])
    return formatted_context
