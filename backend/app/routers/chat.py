from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatMessageResponse, ChatRequest, ChatResponse
from app.services.chat_service import chat, clear_chat_history, list_chat_history
from app.services.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/chat", tags=["chat"])

chat_rate_limit = enforce_rate_limit(
    key_prefix="chat:send",
    limit=settings.chat_rate_limit,
    window_seconds=settings.chat_rate_window_seconds,
)


@router.post("", response_model=ChatResponse)
def send_message(
    body: ChatRequest,
    _: None = Depends(chat_rate_limit),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """
    Sends a message to the AI fitness assistant.
    The last 10 messages are used as conversation memory.
    """
    return chat(db, current_user, body.message)


@router.get("/history", response_model=List[ChatMessageResponse])
def get_history(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ChatMessageResponse]:
    """Returns the full chat history of the authenticated user, chronological order."""
    return list_chat_history(db, current_user.id, limit=limit, offset=offset)


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
def clear_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Clears the entire chat history for the authenticated user."""
    clear_chat_history(db, current_user.id)
