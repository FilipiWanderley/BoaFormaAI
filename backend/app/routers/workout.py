from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.workout import (
    WorkoutFeedbackRequest,
    WorkoutGenerateRequest,
    WorkoutResponse,
    WorkoutSummary,
)
from app.services.workout_service import (
    generate_workout,
    get_workout,
    list_user_workouts,
    submit_feedback,
)

router = APIRouter(prefix="/workout", tags=["workout"])


@router.post("/generate", response_model=WorkoutResponse, status_code=201)
def generate(
    body: WorkoutGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkoutResponse:
    """
    Generates a personalized workout using AI.
    The IA selects exercises exclusively from our validated database.
    """
    return generate_workout(db, current_user, body)


@router.get("/me", response_model=List[WorkoutSummary])
def list_my_workouts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[WorkoutSummary]:
    """Returns the authenticated user's workout history, most recent first."""
    return list_user_workouts(db, current_user.id, limit=limit, offset=offset)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_one(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkoutResponse:
    """Returns a specific workout with full exercise detail."""
    return get_workout(db, workout_id, current_user.id)


@router.patch("/{workout_id}/feedback", response_model=WorkoutSummary)
def give_feedback(
    workout_id: int,
    body: WorkoutFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkoutSummary:
    """
    Submits feedback on a completed workout.
    Feedback is used to calibrate the intensity of the next generated workout.
    """
    return submit_feedback(db, workout_id, current_user.id, body.feedback)
