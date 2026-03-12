from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Roles(str, Enum):
    AI = "ai"
    USER = "user"


class MessageCreation(BaseModel):
    chat_id: UUID
    content: str
    role: Roles
    rating: Optional[bool] = None


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[bool] = None


class MessageResponse(BaseModel):
    message_id: UUID
    chat_id: UUID
    content: str
    rating: Optional[bool]
    sent_at: datetime
    role: Roles
