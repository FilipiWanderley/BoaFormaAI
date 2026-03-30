from typing import List, Literal, Optional

from pydantic import BaseModel, Field

MuscleGroup = Literal[
    "peito",
    "costas",
    "quadriceps",
    "posterior",
    "gluteos",
    "ombros",
    "biceps",
    "triceps",
    "abdomen",
    "panturrilha",
    "trapezio",
    "antebraco",
]

Equipment = Literal[
    "barra",
    "haltere",
    "maquina",
    "cabo",
    "peso_corporal",
    "kettlebell",
    "elastico",
]

Level = Literal["iniciante", "intermediario", "avancado"]


class ExerciseResponse(BaseModel):
    id: int
    name: str
    muscle_group: str
    secondary_muscles: Optional[str]
    equipment: str
    level: str
    instructions: Optional[str]
    image_url: Optional[str]
    contraindications: Optional[str]

    model_config = {"from_attributes": True}


class ExerciseFilterParams(BaseModel):
    muscle_groups: Optional[List[MuscleGroup]] = None
    equipment: Optional[List[Equipment]] = None
    level: Optional[Level] = None


class WorkoutExerciseCreate(BaseModel):
    exercise_id: int
    sets: int = Field(gt=0, le=10)
    reps: str = Field(min_length=1, max_length=20)  # "12" or "8-12"
    rest_seconds: int = Field(gt=0, le=600)
    order: int = Field(ge=1)


class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    exercise: ExerciseResponse
    sets: int
    reps: str
    rest_seconds: int
    order: int

    model_config = {"from_attributes": True}
