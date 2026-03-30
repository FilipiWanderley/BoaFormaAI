from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.exercise import ExerciseResponse, WorkoutExerciseResponse
from app.services.exercise import filter_exercises, get_compatible_exercises, get_exercise_by_id

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/compatible", response_model=List[ExerciseResponse])
def list_compatible(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[ExerciseResponse]:
    """
    Returns all exercises compatible with the authenticated user's training
    level and health restrictions. Respects the level progression rule
    (avancado can also do iniciante exercises, etc.).
    """
    return get_compatible_exercises(db, current_user)


@router.get("", response_model=List[ExerciseResponse])
def list_exercises(
    muscle_group: Optional[List[str]] = Query(default=None),
    equipment: Optional[List[str]] = Query(default=None),
    level: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> List[ExerciseResponse]:
    """
    General exercise listing with optional filters.
    Unlike /compatible, level filtering here is exact (not cumulative).
    """
    levels = [level] if level else None
    return filter_exercises(db, muscle_groups=muscle_group, equipment=equipment, levels=levels)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ExerciseResponse:
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado",
        )
    return exercise
