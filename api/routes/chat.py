import uuid
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.responses import StreamingResponse
from datetime import datetime, timezone
from db.session import get_db
from router.graph import app as graph_app
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

@router.post("/")
async def chat(request: ChatRequest, db = Depends(get_db)):
    """
    Send a message to the Multi-Agent AI Chatbot.
    The response is streamed back to the client using Server-Sent Events (SSE).
    """
    logger.info(f"Received query from {request.user_id} (thread {request.thread_id})")
    
    # 1. Fetch existing chat history from DB
    cursor = db.chat_history.find({"session_id": request.thread_id}).sort("created_at", 1)
    existing_messages = await cursor.to_list(length=None)
    
    # 2. Convert DB rows to LangChain messages
    messages = []
    for msg in existing_messages:
        # Skip fallback messages so they don't poison the LLM context
        if msg.get("content") == "No response generated.":
            continue
            
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            messages.append(AIMessage(content=msg["content"]))
            
    # 3. Add the new user query to the memory context
    messages.append(HumanMessage(content=request.query))
    
    # 4. Save the user's new query to DB immediately
    now = datetime.now(timezone.utc)
    user_db_msg = {
        "session_id": request.thread_id,
        "role": "user",
        "content": request.query,
        "created_at": now
    }
    await db.chat_history.insert_one(user_db_msg)
    
    # Also update the conversation updated_at time
    await db.conversations.update_one(
        {"_id": request.thread_id},
        {"$set": {"updated_at": now}}
    )
    
    # Construct the input state
    inputs = {
        "messages": messages
    }
    
    config = {"configurable": {"thread_id": request.thread_id}}
    
    async def event_generator():
        final_message_chunks = []
        try:
            # Stream events using LangGraph's astream_events
            async for event in graph_app.astream_events(inputs, version="v2", config=config):
                kind = event["event"]
                tags = event.get("tags", [])
                
                # Only stream tokens from the Worker LLMs
                if kind == "on_chat_model_stream" and "workflow" in tags:
                    raw_chunk = event["data"]["chunk"].content
                    if raw_chunk:
                        chunk_str = ""
                        if isinstance(raw_chunk, list):
                            chunk_str = "".join([c.get("text", "") for c in raw_chunk if isinstance(c, dict) and "text" in c])
                        elif isinstance(raw_chunk, str):
                            chunk_str = raw_chunk
                        else:
                            chunk_str = str(raw_chunk)
                            
                        if chunk_str:
                            final_message_chunks.append(chunk_str)
                            # Yield standard Server-Sent Events format
                            yield f"data: {json.dumps({'chunk': chunk_str})}\n\n"
                        
                elif kind == "on_chat_model_end" and "workflow" in tags:
                    # If the local model didn't stream properly due to tool usage, capture the final output here
                    if not final_message_chunks:
                        try:
                            # Safely extract the content depending on the LangChain version/structure
                            raw_msg = event.get("data", {}).get("output", {}).content
                            msg_str = ""
                            if isinstance(raw_msg, list):
                                msg_str = "".join([c.get("text", "") for c in raw_msg if isinstance(c, dict) and "text" in c])
                            elif isinstance(raw_msg, str):
                                msg_str = raw_msg
                            
                            if msg_str:
                                final_message_chunks.append(msg_str)
                                yield f"data: {json.dumps({'chunk': msg_str})}\n\n"
                        except Exception:
                            pass
            
            # After the stream successfully finishes, save the synthesized message to DB
            final_message = "".join(final_message_chunks)
            if not final_message:
                final_message = "No response generated."
                # Stream the fallback message so the UI shows something
                yield f"data: {json.dumps({'chunk': final_message})}\n\n"
                
            assistant_db_msg = {
                "session_id": request.thread_id,
                "role": "assistant",
                "content": final_message,
                "metadata": {"workflow": "Worker"},
                "created_at": datetime.now(timezone.utc)
            }
            await db.chat_history.insert_one(assistant_db_msg)
            
            # Signal the client that the stream is complete
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Error executing graph stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{thread_id}/history")
async def get_history(thread_id: str, db = Depends(get_db)):
    """
    Retrieve the chronological chat history for a given thread.
    """
    cursor = db.chat_history.find({"session_id": thread_id}).sort("created_at", 1)
    existing_messages = await cursor.to_list(length=None)
    
    return [
        {
            "role": msg.get("role"),
            "content": msg.get("content"),
            "timestamp": msg.get("created_at"),
            "metadata": msg.get("metadata", {})
        }
        for msg in existing_messages
    ]
