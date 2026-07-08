import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.builder import app as graph_app
from loguru import logger

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    user_id: str = "default_user"
    thread_id: str = str(uuid.uuid4())

class ChatResponse(BaseModel):
    workflow: str
    response: str
    thread_id: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the Multi-Agent AI Chatbot.
    The router will decide the workflow and the specialized agent will respond.
    """
    logger.info(f"Received query from {request.user_id} (thread {request.thread_id})")
    
    # Construct the input state
    inputs = {
        "messages": [HumanMessage(content=request.query)]
    }
    
    # LangGraph uses a thread-based configuration for memory, but for now we'll do stateless 
    # to prove the router and MCP integrations work.
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        # Invoke the graph
        result = graph_app.invoke(inputs, config=config)
        
        # Extract the final message and workflow
        final_message = result["messages"][-1].content if result.get("messages") else "No response generated."
        workflow = result.get("selected_workflow", "Unknown")
        
        return ChatResponse(
            workflow=workflow,
            response=final_message,
            thread_id=request.thread_id
        )
    except Exception as e:
        logger.error(f"Error executing graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))
