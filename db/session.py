from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Global MongoDB client
client = None

def get_mongo_client():
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URI)
    return client

async def get_db():
    db_client = get_mongo_client()
    db = db_client[settings.MONGO_DB_NAME]
    yield db
