from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class ChatMessageResponse(BaseModel):
    id: int
    role: str  # "user" | "assistant"
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    reply: ChatMessageResponse
    history: List[ChatMessageResponse]
