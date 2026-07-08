from fastapi import FastAPI
from core.config import settings
from core.logging import setup_logging
from loguru import logger
from api.routes import chat

# Initialize logging
setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Enterprise Multi-Agent AI Chatbot API",
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")

# Include Routers
app.include_router(chat.router)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {"status": "ok", "app_name": settings.APP_NAME}
