from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.services.exercise import create_exercise, delete_exercise, filter_exercises, update_exercise

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/exercises", response_model=List[ExerciseResponse])
def list_exercises_admin(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> List[ExerciseResponse]:
    return filter_exercises(db, limit=limit, offset=offset)


@router.post("/exercises", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise_admin(
    body: ExerciseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ExerciseResponse:
    return create_exercise(db, body)


@router.patch("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_exercise_admin(
    exercise_id: int,
    body: ExerciseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ExerciseResponse:
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
    return update_exercise(db, exercise, body)


@router.delete("/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_admin(
    exercise_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> None:
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
    delete_exercise(db, exercise)
