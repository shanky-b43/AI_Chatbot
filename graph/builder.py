from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.nodes.router import route_query
from workflows.registry import WorkflowRegistry
from loguru import logger
import workflows  # This triggers the registration of all workflows

def route_to_workflow(state: GraphState):
    """
    Conditional edge function that routes the graph based on the selected workflow.
    """
    workflow_name = state.get("selected_workflow", "General")
    logger.info(f"Routing to: {workflow_name} Workflow")
    return workflow_name

def execute_workflow(state: GraphState):
    """
    Node that executes the dynamically loaded workflow.
    """
    workflow_name = state.get("selected_workflow", "General")
    workflow = WorkflowRegistry.get_workflow(workflow_name)
    
    # We pass the state to the sub-workflow and merge the result
    logger.debug(f"Invoking {workflow_name} workflow...")
    result = workflow.invoke(state)
    return {"messages": result.get("messages", [])}

def build_main_graph() -> StateGraph:
    """
    Builds the main LangGraph orchestration graph.
    """
    builder = StateGraph(GraphState)
    
    # Add Nodes
    builder.add_node("router", route_query)
    builder.add_node("workflow_executor", execute_workflow)
    
    # Add Edges
    builder.add_edge(START, "router")
    builder.add_edge("router", "workflow_executor")
    builder.add_edge("workflow_executor", END)
    
    return builder.compile()

# Instantiate the main graph
app = build_main_graph()
