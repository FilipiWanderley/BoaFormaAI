from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.exercise import Exercise, WorkoutExercise
from app.models.user import User
from app.models.workout import Workout
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, WorkoutExerciseCreate


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_contraindication_keywords(value: Optional[str]) -> List[str]:
    """Split a comma-separated contraindications string into cleaned keywords."""
    if not value:
        return []
    return [kw.strip().lower() for kw in value.split(",") if kw.strip()]


def _is_contraindicated(exercise: Exercise, user_restrictions: str) -> bool:
    """
    Return True when any of the exercise's contraindication keywords appear
    inside the user's free-text restrictions field.
    """
    keywords = _parse_contraindication_keywords(exercise.contraindications)
    if not keywords:
        return False
    restrictions_lower = user_restrictions.lower()
    return any(kw in restrictions_lower for kw in keywords)


def _eligible_levels(user_level: str) -> List[str]:
    """
    An intermediario can perform iniciante exercises;
    an avancado can perform all levels.
    """
    progression = ["iniciante", "intermediario", "avancado"]
    cutoff = progression.index(user_level)
    return progression[: cutoff + 1]


# ---------------------------------------------------------------------------
# Public service API
# ---------------------------------------------------------------------------

def get_compatible_exercises(
    db: Session,
    user: User,
    *,
    limit: int = 100,
    offset: int = 0,
) -> List[Exercise]:
    """
    Return all exercises compatible with the user's training level and
    health restrictions. Higher-level users have access to all easier exercises.
    """
    return filter_exercises(
        db,
        levels=_eligible_levels(user.level),
        restrictions=user.restrictions,
        limit=limit,
        offset=offset,
    )


def filter_exercises(
    db: Session,
    *,
    muscle_groups: Optional[List[str]] = None,
    equipment: Optional[List[str]] = None,
    levels: Optional[List[str]] = None,
    restrictions: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Exercise]:
    """
    General-purpose exercise filter. All parameters are optional; omitting
    one means "no restriction on that dimension".
    """
    query = db.query(Exercise)

    if muscle_groups:
        query = query.filter(Exercise.muscle_group.in_(muscle_groups))
    if equipment:
        query = query.filter(Exercise.equipment.in_(equipment))
    if levels:
        query = query.filter(Exercise.level.in_(levels))

    items = (
        query.order_by(Exercise.muscle_group, Exercise.name)
        .offset(offset)
        .limit(limit)
        .all()
    )
    if restrictions:
        items = [exercise for exercise in items if not _is_contraindicated(exercise, restrictions)]
    return items


def get_exercise_by_id(db: Session, exercise_id: int) -> Optional[Exercise]:
    return db.get(Exercise, exercise_id)


def create_exercise(db: Session, data: ExerciseCreate) -> Exercise:
    existing = db.query(Exercise).filter(Exercise.name == data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exercício com este nome já existe.",
        )
    exercise = Exercise(**data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def update_exercise(db: Session, exercise: Exercise, data: ExerciseUpdate) -> Exercise:
    values = data.model_dump(exclude_none=True)
    for field, value in values.items():
        setattr(exercise, field, value)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise: Exercise) -> None:
    db.delete(exercise)
    db.commit()


def add_exercises_to_workout(
    db: Session,
    workout: Workout,
    items: List[WorkoutExerciseCreate],
) -> List[WorkoutExercise]:
    """
    Bulk-insert WorkoutExercise rows for a given workout.
    Existing entries are replaced (delete + insert).
    """
    db.query(WorkoutExercise).filter(
        WorkoutExercise.workout_id == workout.id
    ).delete()

    records = [
        WorkoutExercise(
            workout_id=workout.id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            rest_seconds=item.rest_seconds,
            order=item.order,
        )
        for item in items
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records
