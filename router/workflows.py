from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from langchain_core.messages import AIMessage
from loguru import logger

# 1. DBTalk Workflow (Placeholder)
@WorkflowRegistry.register("dbtalk")
def build_dbtalk_workflow() -> StateGraph:
    """
    Placeholder for the future DBTalk workflow.
    """
    def dbtalk_node(state: GraphState):
        logger.info("Executing DBTalk placeholder...")
        return {"messages": [AIMessage(content="[DBTalk Workflow Placeholder] This would query the database.", name="worker")]}
    
    builder = StateGraph(GraphState)
    builder.add_node("dbtalk_worker", dbtalk_node)
    builder.add_edge(START, "dbtalk_worker")
    builder.add_edge("dbtalk_worker", END)
    return builder.compile()


# 2. Summary Workflow (Placeholder)
@WorkflowRegistry.register("summary")
def build_summary_workflow() -> StateGraph:
    """
    Placeholder for the future Summary workflow.
    """
    def summary_node(state: GraphState):
        logger.info("Executing Summary placeholder...")
        return {"messages": [AIMessage(content="[Summary Workflow Placeholder] This would summarize the text.", name="worker")]}
    
    builder = StateGraph(GraphState)
    builder.add_node("summary_worker", summary_node)
    builder.add_edge(START, "summary_worker")
    builder.add_edge("summary_worker", END)
    return builder.compile()
