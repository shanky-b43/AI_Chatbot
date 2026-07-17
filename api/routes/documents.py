from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import uuid
from typing import Optional
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, Docx2txtLoader
import pandas as pd
from loguru import logger

from core.config import settings
from services.indexer import index_documents
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

TEMP_DIR = "data/tmp"
os.makedirs(TEMP_DIR, exist_ok=True)

class IngestRequest(BaseModel):
    filename: str
    tmp_path: str
    department: str
    sub_node: str

def get_document_text(filepath: str, ext: str) -> str:
    """Extract text from supported file types."""
    try:
        if ext == ".txt" or ext == ".md":
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            return "\n".join([d.page_content for d in docs])
        elif ext == ".pdf":
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            return "\n".join([d.page_content for d in docs])
        elif ext == ".csv":
            loader = CSVLoader(filepath)
            docs = loader.load()
            return "\n".join([d.page_content for d in docs])
        elif ext == ".docx" or ext == ".doc":
            loader = Docx2txtLoader(filepath)
            docs = loader.load()
            return "\n".join([d.page_content for d in docs])
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath)
            return df.to_string()
        elif ext in [".jpg", ".jpeg", ".png"]:
            # Basic fallback since we don't have OCR running
            return f"Image file: {os.path.basename(filepath)}"
        else:
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {e}")
        return ""

@router.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Receives a file, saves to tmp, extracts text, and asks LLM to classify it."""
    ext = os.path.splitext(file.filename)[1].lower()
    supported = [".txt", ".md", ".pdf", ".csv", ".docx", ".doc", ".xls", ".xlsx", ".jpg", ".jpeg", ".png"]
    if ext not in supported:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension {ext}")

    tmp_filename = f"{uuid.uuid4()}{ext}"
    tmp_path = os.path.join(TEMP_DIR, tmp_filename)
    
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    text = get_document_text(tmp_path, ext)
    
    # Analyze text with LLM
    # We'll use the CHAT_MODEL to classify if we are worried about hallucination
    # Since reading documents requires better context window, we use CHAT_MODEL.
    # Analyze text with LLM using structured output
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.1
    )
    
    from router.schema import RouterOutput
    structured_llm = llm.with_structured_output(RouterOutput)
    
    system_prompt = """You are a document classifier for an enterprise chatbot.
Your job is to read a snippet of a document and classify it into exactly ONE of these departments: 'hr', 'finance', 'it', or 'general'.
You MUST also provide the specific sub-node for that department based on the available schema.
Respond strictly matching the requested JSON format."""

    snippet = text[:2000] if text else f"Filename: {file.filename}\n(This file could not have its text automatically extracted)."
    
    try:
        res = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Classify this document snippet:\n\n{snippet}")
        ])
        department = res.agent if res.agent in ["hr", "finance", "it"] else "general"
        
        if department == "general":
            sub_node = "general"
        else:
            sub_node = res.sub_node.lower().replace(" ", "_").replace("&", "and") if res.sub_node else "general"
            
    except Exception as e:
        logger.error(f"Failed to classify: {e}")
        department = "general"
        sub_node = "general"
        
    return {
        "filename": file.filename,
        "tmp_path": tmp_path,
        "department": department,
        "sub_node": sub_node,
        "type": ext
    }

@router.post("/ingest")
async def ingest_document(req: IngestRequest):
    """Moves document to permanent storage and indexes it."""
    if not os.path.exists(req.tmp_path):
        raise HTTPException(status_code=404, detail="Temporary file not found.")
        
    # Move file to permanent data dir
    target_dir = os.path.join("data", req.department.lower(), req.sub_node)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, req.filename)
    
    shutil.move(req.tmp_path, target_path)
    
    # Ingest to elasticsearch
    try:
        from langchain_core.documents import Document
        text = get_document_text(target_path, os.path.splitext(target_path)[1].lower())
        if not text:
            text = f"Content of {req.filename}"
            
        doc = Document(page_content=text, metadata={"source": target_path, "department": req.department.lower(), "sub_node": req.sub_node})
        index_documents([doc], index_name="knowledge_base")
        
        return {"status": "success", "message": f"Successfully ingested {req.filename} into {req.department}/{req.sub_node}."}
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest document")
