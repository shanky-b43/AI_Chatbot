from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger
from mcp.clients import execute_sql_tool, search_documents_tool

@WorkflowRegistry.register("IT")
def build_it_workflow():
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.2
    )
    
    tools = [execute_sql_tool, search_documents_tool]
    
    system_prompt = (
        "You are an expert IT Support AI assistant. "
        "You assist with technical issues, hardware requests, software access, and password resets. "
        "You have access to a database (for IT assets and tickets) and Elasticsearch (for IT guides). "
        "Ask for error codes or specific system details if troubleshooting."
    )
    
    # We use LangGraph's built-in ReAct agent for tool execution
    agent = create_react_agent(llm, tools=tools, state_modifier=system_prompt)
    return agent
