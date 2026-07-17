from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from router.router import run_intent_router
from workflows.registry import WorkflowRegistry
from loguru import logger

# Import to trigger registration
import workflows.hr
import workflows.finance
import workflows.it
import router.workflows

from langchain_core.runnables import RunnableConfig

def make_workflow_node(workflow_name: str, workflow_graph: StateGraph):
    """
    Creates a node function that invokes a nested workflow (sub-graph).
    """
    async def node(state: GraphState, config: RunnableConfig):
        logger.debug(f"Routing to {workflow_name} workflow...")
        # Invoke the sub-graph/agent, passing the parent config for tracing/streaming
        # Add a custom tag for our intent level
        config["tags"] = config.get("tags", []) + ["workflow"]
        
        result = await workflow_graph.ainvoke(state, config=config)
        
        old_len = len(state.get("messages", []))
        new_messages = result.get("messages", [])[old_len:]
        
        return {"messages": new_messages}
    return node

def build_intent_graph() -> StateGraph:
    """
    Builds the top-level Workflow Routing LangGraph.
    """
    builder = StateGraph(GraphState)
    
    # 1. Add Router Node
    builder.add_node("intent_router", run_intent_router)
    
    # 2. Add Workflow Nodes dynamically from Registry
    registered_workflows = WorkflowRegistry.get_all_workflows()
    workflow_names = list(registered_workflows.keys())
    
    for name, workflow_graph in registered_workflows.items():
        # lowercase the name in case some were registered with caps (like HR)
        safe_name = name.lower()
        builder.add_node(safe_name, make_workflow_node(safe_name, workflow_graph))
        # Every workflow routes to END when done
        builder.add_edge(safe_name, END)
        
    # Add fallback direct LLM conversation node
    from langchain_ollama import ChatOllama
    from core.config import settings
    async def llm_conversation(state: GraphState, config: RunnableConfig):
        llm = ChatOllama(model=settings.CHAT_MODEL, base_url=settings.OLLAMA_URL, temperature=0.7).with_config({"tags": ["workflow"]})
        response = await llm.ainvoke(state.get("messages", []), config=config)
        return {"messages": [response]}
    
    builder.add_node("conversation", llm_conversation)
    builder.add_edge("conversation", END)
    
    # 3. Add Edges
    builder.add_edge(START, "intent_router")
    
    # The router decides the next step.
    conditional_map = {name.lower(): name.lower() for name in workflow_names}
    conditional_map["conversation"] = "conversation"
    conditional_map["FINISH"] = END
    
    # Force cast to lower to handle any casing mismatches
    builder.add_conditional_edges("intent_router", lambda x: x["next_worker"].lower(), conditional_map)
    
    return builder.compile()

# Instantiate the main intent graph
app = build_intent_graph()
