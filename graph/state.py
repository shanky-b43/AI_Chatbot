from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import AnyMessage, add_messages

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    
    Attributes:
        messages: The list of messages in the conversation. Use `add_messages` to append.
        selected_workflow: The workflow selected by the router (e.g., 'HR', 'Finance', 'IT', 'General').
        router_confidence: The confidence score from the router.
        router_reason: The reason provided by the router for selecting the workflow.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    selected_workflow: Optional[str]
    router_confidence: Optional[float]
    router_reason: Optional[str]
