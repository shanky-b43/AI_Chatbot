from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from core.config import settings
from graph.state import GraphState
from loguru import logger

class RouterDecision(BaseModel):
    workflow: str = Field(
        description="The workflow to route the user's query to. Must be one of: 'HR', 'Finance', 'IT', 'General'. If unknown or ambiguous, use 'General'."
    )
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0 that the selected workflow is the correct one."
    )
    reason: str = Field(
        description="A brief reason for selecting this workflow."
    )

def route_query(state: GraphState) -> GraphState:
    """
    Router node that evaluates the user's latest query and decides which workflow to route to.
    """
    logger.info("Executing Router Node")
    messages = state.get("messages", [])
    if not messages:
        return {"selected_workflow": "General", "router_confidence": 1.0, "router_reason": "No messages found"}

    latest_message = messages[-1].content

    # System prompt for the router
    system_prompt = """You are an intelligent router for an Enterprise AI Chatbot.
Your job is to analyze the user's latest message and route it to the appropriate specialized workflow.
Available Workflows:
- HR: For questions about leave, payroll, company policies, employee benefits.
- Finance: For questions about invoices, expenses, budgets, reimbursements.
- IT: For questions about technical support, hardware assets, software licenses, resetting passwords, IT tickets.
- General: For greetings, small talk, fallback queries, or if the intent does not clearly match HR, Finance, or IT.

Respond using the requested structured output. Be highly accurate."""

    llm = ChatGoogleGenerativeAI(
        model=settings.ROUTER_MODEL,
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(RouterDecision)
    
    # Construct conversation context (we can just pass the system prompt and the latest message for routing)
    try:
        decision: RouterDecision = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            {"role": "user", "content": latest_message}
        ])
        
        logger.info(f"Router decided: {decision.workflow} (Confidence: {decision.confidence})")
        
        # Fallback if confidence is low
        if decision.confidence < 0.6:
            logger.warning("Low confidence in routing. Falling back to General workflow.")
            return {
                "selected_workflow": "General",
                "router_confidence": decision.confidence,
                "router_reason": "Low confidence fallback: " + decision.reason
            }
            
        return {
            "selected_workflow": decision.workflow,
            "router_confidence": decision.confidence,
            "router_reason": decision.reason
        }
    except Exception as e:
        logger.error(f"Router node failed: {e}")
        # Graceful fallback
        return {
            "selected_workflow": "General",
            "router_confidence": 0.0,
            "router_reason": f"Routing failed with error: {str(e)}"
        }
