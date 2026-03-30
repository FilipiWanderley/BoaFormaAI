from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserResponse
from app.schemas.workout import WorkoutSummary


class DashboardStats(BaseModel):
    total_workouts_generated: int
    total_workouts_completed: int
    current_streak_days: int
    last_completed_at: Optional[datetime]


class DashboardResponse(BaseModel):
    user: UserResponse
    today_workout: Optional[WorkoutSummary]
    last_workout: Optional[WorkoutSummary]
    stats: DashboardStats
