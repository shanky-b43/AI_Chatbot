from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger
from mcp.clients import execute_sql_tool, search_documents_tool

@WorkflowRegistry.register("HR")
def build_hr_workflow():
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.2
    )
    
    tools = [execute_sql_tool, search_documents_tool]
    
    system_prompt = (
        "You are an expert HR AI assistant. "
        "You assist employees with leave policies, payroll inquiries, and company benefits. "
        "You have access to a database (for employee records) and Elasticsearch (for HR policies). "
        "If you need more information, ask clarifying questions."
    )
    
    # We use LangGraph's built-in ReAct agent for tool execution
    agent = create_react_agent(llm, tools=tools, state_modifier=system_prompt)
    return agent
