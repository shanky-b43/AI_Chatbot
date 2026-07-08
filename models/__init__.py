from db.base import Base
from models.user import User
from models.chat import ChatHistory

# Export all models so alembic can autogenerate migrations
__all__ = ["Base", "User", "ChatHistory"]
