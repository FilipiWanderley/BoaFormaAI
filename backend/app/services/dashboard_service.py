import json
from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout import History, Workout
from app.schemas.dashboard import DashboardResponse, DashboardStats
from app.schemas.user import UserResponse
from app.schemas.workout import WorkoutSummary


# ---------------------------------------------------------------------------
# Streak calculation
# ---------------------------------------------------------------------------

def _calculate_streak(completion_dates: List[date]) -> int:
    """
    Returns the number of consecutive days (ending today or yesterday)
    on which the user completed at least one workout.
    """
    if not completion_dates:
        return 0

    unique_dates = sorted(set(completion_dates), reverse=True)
    today = date.today()

    # Streak only active if the user trained today or yesterday
    if unique_dates[0] < today - timedelta(days=1):
        return 0

    streak = 0
    expected = unique_dates[0]
    for d in unique_dates:
        if d == expected:
            streak += 1
            expected = d - timedelta(days=1)
        else:
            break

    return streak


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _workout_name_from_json(exercises_json: str) -> str:
    try:
        return json.loads(exercises_json).get("workout_name", "Treino")
    except Exception:
        return "Treino"


def _workout_focus_from_json(exercises_json: str) -> str:
    try:
        return json.loads(exercises_json).get("focus", "")
    except Exception:
        return ""


def _workout_duration_from_json(exercises_json: str) -> int:
    try:
        return int(json.loads(exercises_json).get("estimated_duration_minutes", 60))
    except Exception:
        return 60


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_dashboard(db: Session, user: User) -> DashboardResponse:
    # ── Last generated workout ───────────────────────────────────────────
    last_workout_row: Optional[Workout] = (
        db.query(Workout)
        .filter(Workout.user_id == user.id)
        .order_by(Workout.created_at.desc())
        .first()
    )
    last_workout: Optional[WorkoutSummary] = None
    if last_workout_row:
        last_workout = WorkoutSummary(
            id=last_workout_row.id,
            workout_name=_workout_name_from_json(last_workout_row.exercises_json),
            focus=_workout_focus_from_json(last_workout_row.exercises_json),
            estimated_duration_minutes=_workout_duration_from_json(
                last_workout_row.exercises_json
            ),
            created_at=last_workout_row.created_at,
            feedback=last_workout_row.feedback,
        )

    # ── History stats ────────────────────────────────────────────────────
    history_rows = (
        db.query(History)
        .filter(History.user_id == user.id)
        .order_by(History.completed_at.desc())
        .all()
    )

    total_completed = len(history_rows)
    last_completed_at = history_rows[0].completed_at if history_rows else None
    completion_dates = [h.completed_at.date() for h in history_rows]
    streak = _calculate_streak(completion_dates)

    total_generated: int = (
        db.query(func.count(Workout.id))
        .filter(Workout.user_id == user.id)
        .scalar()
        or 0
    )

    return DashboardResponse(
        user=UserResponse.model_validate(user),
        last_workout=last_workout,
        stats=DashboardStats(
            total_workouts_generated=total_generated,
            total_workouts_completed=total_completed,
            current_streak_days=streak,
            last_completed_at=last_completed_at,
        ),
    )
