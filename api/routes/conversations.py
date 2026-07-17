from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from db.session import get_db
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from fastapi.responses import Response
import uuid

router = APIRouter(prefix="/conversations", tags=["Conversations"])

class ConversationResponse(BaseModel):
    id: str
    title: str
    updated_at: datetime
    
class ConversationUpdate(BaseModel):
    title: str

@router.get("", response_model=List[ConversationResponse])
async def list_conversations(db = Depends(get_db)):
    cursor = db.conversations.find().sort("updated_at", -1)
    conversations = await cursor.to_list(length=100)
    
    return [
        ConversationResponse(
            id=c["_id"],
            title=c.get("title", "New Conversation"),
            updated_at=c.get("updated_at")
        ) for c in conversations
    ]

@router.post("", response_model=ConversationResponse)
async def create_conversation(db = Depends(get_db)):
    conv_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    new_conv = {
        "_id": conv_id,
        "title": "New Conversation",
        "created_at": now,
        "updated_at": now
    }
    
    await db.conversations.insert_one(new_conv)
    
    # Add a default greeting message
    welcome_msg = {
        "session_id": conv_id,
        "role": "assistant",
        "content": "Hello! I am your AI Assistant. How can I help you today?",
        "metadata": {"workflow": "System"},
        "created_at": now
    }
    await db.chat_history.insert_one(welcome_msg)
    
    return ConversationResponse(
        id=conv_id,
        title="New Conversation",
        updated_at=now
    )

@router.get("/search", response_model=List[ConversationResponse])
async def search_conversations(q: str = Query(...), db = Depends(get_db)):
    # Simple regex search for MongoDB
    cursor = db.conversations.find({"title": {"$regex": q, "$options": "i"}}).sort("updated_at", -1)
    conversations = await cursor.to_list(length=100)
    
    return [
        ConversationResponse(
            id=c["_id"],
            title=c.get("title", "New Conversation"),
            updated_at=c.get("updated_at")
        ) for c in conversations
    ]

@router.get("/{id}", response_model=ConversationResponse)
async def get_conversation(id: str, db = Depends(get_db)):
    conv = await db.conversations.find_one({"_id": id})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    return ConversationResponse(
        id=conv["_id"],
        title=conv.get("title", "New Conversation"),
        updated_at=conv.get("updated_at")
    )

@router.patch("/{id}", response_model=ConversationResponse)
async def update_conversation(id: str, update_data: ConversationUpdate, db = Depends(get_db)):
    now = datetime.now(timezone.utc)
    result = await db.conversations.update_one(
        {"_id": id},
        {"$set": {"title": update_data.title, "updated_at": now}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return ConversationResponse(
        id=id,
        title=update_data.title,
        updated_at=now
    )

@router.delete("/{id}")
async def delete_conversation(id: str, db = Depends(get_db)):
    result = await db.conversations.delete_one({"_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Also delete associated chat history
    await db.chat_history.delete_many({"session_id": id})
    
    return {"status": "ok"}

@router.get("/{id}/download")
async def download_conversation(id: str, format: str = "md", db = Depends(get_db)):
    conv = await db.conversations.find_one({"_id": id})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    cursor = db.chat_history.find({"session_id": id}).sort("created_at", 1)
    messages = await cursor.to_list(length=None)
    
    content = f"# {conv.get('title', 'Conversation')}\n\n"
    for msg in messages:
        role = msg.get("role", "unknown")
        text = msg.get("content", "")
        content += f"**{role.capitalize()}**: {text}\n\n"
        
    if not messages:
        content += "No messages downloaded yet."
    
    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=conversation-{id}.md"}
    )
