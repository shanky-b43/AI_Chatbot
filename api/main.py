from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logging import setup_logging
from loguru import logger
from api.routes import chat, conversations, documents

# Initialize logging
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Enterprise Multi-Agent AI Chatbot API",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")

# Include Routers
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(documents.router, prefix="/api/documents")

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok", "app_name": settings.APP_NAME}
