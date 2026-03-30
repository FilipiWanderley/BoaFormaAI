from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from app.schemas.exercise import Equipment, MuscleGroup


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------

class WorkoutGenerateRequest(BaseModel):
    muscle_groups: Optional[List[MuscleGroup]] = Field(
        default=None,
        description="Grupos musculares para focar. Se omitido, a IA escolhe o melhor split.",
    )
    equipment_available: Optional[List[Equipment]] = Field(
        default=None,
        description="Equipamentos disponíveis na sessão. Se omitido, usa tudo da base.",
    )
    duration_minutes: int = Field(
        default=60,
        ge=20,
        le=120,
        description="Duração alvo do treino em minutos.",
    )
    feedback_on_last: Optional[Literal["facil", "ok", "dificil"]] = Field(
        default=None,
        description="Feedback do último treino. Usado para calibrar a intensidade do novo.",
    )


# ---------------------------------------------------------------------------
# Internal — LLM response contract (never exposed directly to the API caller)
# ---------------------------------------------------------------------------

class _LLMExercise(BaseModel):
    exercise_id: int
    exercise_name: str
    sets: int = Field(ge=1, le=10)
    reps: str = Field(min_length=1, max_length=20)  # "12" or "8-12"
    rest_seconds: int = Field(ge=10, le=600)
    notes: Optional[str] = None


class _LLMWorkout(BaseModel):
    workout_name: str
    focus: str
    estimated_duration_minutes: int = Field(ge=10, le=180)
    exercises: List[_LLMExercise] = Field(min_length=4, max_length=12)
    general_tips: str


# ---------------------------------------------------------------------------
# Public response
# ---------------------------------------------------------------------------

class WorkoutExerciseDetail(BaseModel):
    exercise_id: int
    exercise_name: str
    muscle_group: str
    equipment: str
    sets: int
    reps: str
    rest_seconds: int
    notes: Optional[str]
    order: int
    image_url: Optional[str]

    model_config = {"from_attributes": True}


class WorkoutResponse(BaseModel):
    id: int
    workout_name: str
    focus: str
    estimated_duration_minutes: int
    exercises: List[WorkoutExerciseDetail]
    general_tips: str
    created_at: datetime
    feedback: Optional[str]

    model_config = {"from_attributes": True}


class WorkoutSummary(BaseModel):
    id: int
    workout_name: str
    focus: str
    estimated_duration_minutes: int
    created_at: datetime
    feedback: Optional[str]

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Feedback patch
# ---------------------------------------------------------------------------

class WorkoutFeedbackRequest(BaseModel):
    feedback: Literal["facil", "ok", "dificil"]
