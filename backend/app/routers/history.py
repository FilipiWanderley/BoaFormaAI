from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.history import HistoryCreate, HistoryResponse
from app.services.history_service import complete_workout, list_history

router = APIRouter(prefix="/history", tags=["history"])


@router.post("", response_model=HistoryResponse, status_code=status.HTTP_201_CREATED)
def mark_completed(
    body: HistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HistoryResponse:
    """Marks a workout as completed and records it in the training history."""
    return complete_workout(db, current_user.id, body)


@router.get("/me", response_model=List[HistoryResponse])
def get_my_history(
    limit: int = Query(default=30, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[HistoryResponse]:
    """Returns the authenticated user's completed workout history, most recent first."""
    return list_history(db, current_user.id, limit=limit, offset=offset)


@router.get("/{user_id}", response_model=List[HistoryResponse])
def get_history_by_user_id(
    user_id: int,
    limit: int = Query(default=30, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[HistoryResponse]:
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode acessar seu próprio histórico.",
        )
    return list_history(db, current_user.id, limit=limit, offset=offset)
