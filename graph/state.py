from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import AnyMessage, add_messages

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    
    Attributes:
        messages: The list of messages in the conversation. Use `add_messages` to append.
        next_worker: The next worker agent to route to, or 'FINISH' if the task is complete.
        supervisor_reason: The reason provided by the supervisor for the routing decision.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    next_worker: Optional[str]
    sub_node: Optional[str]
    supervisor_reason: Optional[str]
