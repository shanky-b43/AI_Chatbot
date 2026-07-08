from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger

def general_agent(state: GraphState):
    logger.info("Executing General Agent")
    
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.7
    )
    
    system_prompt = SystemMessage(
        content="You are a helpful, friendly enterprise AI assistant. "
                "Answer general questions, make small talk, and assist the user."
    )
    
    messages = [system_prompt] + state.get("messages", [])
    response = llm.invoke(messages)
    
    return {"messages": [response]}

@WorkflowRegistry.register("General")
def build_general_workflow() -> StateGraph:
    builder = StateGraph(GraphState)
    builder.add_node("general_agent", general_agent)
    builder.add_edge(START, "general_agent")
    builder.add_edge("general_agent", END)
    
    return builder.compile()
