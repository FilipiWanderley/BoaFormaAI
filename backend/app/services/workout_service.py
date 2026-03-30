"""
Workout service — orchestrates the full generate → validate → persist → respond pipeline.
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.exercise import Exercise, WorkoutExercise
from app.models.user import User
from app.models.workout import Workout
from app.schemas.workout import (
    WorkoutExerciseDetail,
    WorkoutGenerateRequest,
    WorkoutResponse,
    WorkoutSummary,
    _LLMExercise,
    _LLMWorkout,
)
from app.services.exercise import filter_exercises, get_compatible_exercises
from app.services.llm_service import call_groq_for_workout


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _select_exercises(
    db: Session,
    user: User,
    request: WorkoutGenerateRequest,
) -> List[Exercise]:
    """
    Build the exercise pool that will be sent to the LLM.
    Respects user level, restrictions, and optional request filters.
    """
    compatible = get_compatible_exercises(db, user)

    if not request.muscle_groups and not request.equipment_available:
        return compatible

    # Apply additional filters from the request on top of compatibility filter
    compatible_ids = {ex.id for ex in compatible}
    further_filtered = filter_exercises(
        db,
        muscle_groups=request.muscle_groups,
        equipment=request.equipment_available,
    )
    return [ex for ex in further_filtered if ex.id in compatible_ids]


def _build_workout_exercise_detail(
    item: _LLMExercise,
    exercise: Exercise,
    order: int,
) -> WorkoutExerciseDetail:
    return WorkoutExerciseDetail(
        exercise_id=exercise.id,
        exercise_name=exercise.name,
        muscle_group=exercise.muscle_group,
        equipment=exercise.equipment,
        sets=item.sets,
        reps=item.reps,
        rest_seconds=item.rest_seconds,
        notes=item.notes,
        order=order,
        image_url=exercise.image_url,
    )


def _persist_workout(
    db: Session,
    user: User,
    llm_workout: _LLMWorkout,
    exercise_map: dict[int, Exercise],
    prompt_context: str,
) -> Workout:
    workout = Workout(
        user_id=user.id,
        exercises_json=llm_workout.model_dump_json(),
        prompt_context=prompt_context,
    )
    db.add(workout)
    db.flush()  # populate workout.id before inserting children

    workout_exercises = [
        WorkoutExercise(
            workout_id=workout.id,
            exercise_id=item.exercise_id,
            sets=item.sets,
            reps=item.reps,
            rest_seconds=item.rest_seconds,
            order=order,
        )
        for order, item in enumerate(llm_workout.exercises, start=1)
    ]
    db.add_all(workout_exercises)
    db.commit()
    db.refresh(workout)
    return workout


def _to_workout_response(
    workout: Workout,
    llm_workout: _LLMWorkout,
    exercise_map: dict[int, Exercise],
) -> WorkoutResponse:
    exercises = [
        _build_workout_exercise_detail(item, exercise_map[item.exercise_id], order)
        for order, item in enumerate(llm_workout.exercises, start=1)
    ]
    return WorkoutResponse(
        id=workout.id,
        workout_name=llm_workout.workout_name,
        focus=llm_workout.focus,
        estimated_duration_minutes=llm_workout.estimated_duration_minutes,
        exercises=exercises,
        general_tips=llm_workout.general_tips,
        created_at=workout.created_at,
        feedback=workout.feedback,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_workout(
    db: Session,
    user: User,
    request: WorkoutGenerateRequest,
) -> WorkoutResponse:
    exercises = _select_exercises(db, user, request)

    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Nenhum exercício compatível encontrado com os filtros informados. "
                "Tente remover filtros de equipamento ou grupo muscular."
            ),
        )

    llm_workout = call_groq_for_workout(user, exercises, request)

    exercise_map = {ex.id: ex for ex in exercises}
    prompt_context = request.model_dump_json()

    workout = _persist_workout(db, user, llm_workout, exercise_map, prompt_context)
    return _to_workout_response(workout, llm_workout, exercise_map)


def get_workout(db: Session, workout_id: int, user_id: int) -> WorkoutResponse:
    workout = (
        db.query(Workout)
        .options(
            joinedload(Workout.workout_exercises).joinedload(WorkoutExercise.exercise)
        )
        .filter(Workout.id == workout_id, Workout.user_id == user_id)
        .first()
    )
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado.",
        )

    import json as _json
    llm_data = _json.loads(workout.exercises_json)
    llm_workout = _LLMWorkout.model_validate(llm_data)

    exercise_map = {we.exercise_id: we.exercise for we in workout.workout_exercises}
    return _to_workout_response(workout, llm_workout, exercise_map)


def list_user_workouts(
    db: Session,
    user_id: int,
    limit: int = 20,
    offset: int = 0,
) -> List[WorkoutSummary]:
    workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .order_by(Workout.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        WorkoutSummary(
            id=w.id,
            workout_name=_parse_workout_name(w.exercises_json),
            focus=_parse_workout_focus(w.exercises_json),
            estimated_duration_minutes=_parse_duration(w.exercises_json),
            created_at=w.created_at,
            feedback=w.feedback,
        )
        for w in workouts
    ]


def submit_feedback(
    db: Session,
    workout_id: int,
    user_id: int,
    feedback: str,
) -> WorkoutSummary:
    workout = (
        db.query(Workout)
        .filter(Workout.id == workout_id, Workout.user_id == user_id)
        .first()
    )
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado.",
        )
    workout.feedback = feedback
    db.commit()
    db.refresh(workout)
    return WorkoutSummary(
        id=workout.id,
        workout_name=_parse_workout_name(workout.exercises_json),
        focus=_parse_workout_focus(workout.exercises_json),
        estimated_duration_minutes=_parse_duration(workout.exercises_json),
        created_at=workout.created_at,
        feedback=workout.feedback,
    )


# ---------------------------------------------------------------------------
# JSON field extraction helpers (avoids full model parse for list views)
# ---------------------------------------------------------------------------

def _parse_workout_name(exercises_json: str) -> str:
    import json as _json
    try:
        return _json.loads(exercises_json).get("workout_name", "Treino")
    except Exception:
        return "Treino"


def _parse_workout_focus(exercises_json: str) -> str:
    import json as _json
    try:
        return _json.loads(exercises_json).get("focus", "")
    except Exception:
        return ""


def _parse_duration(exercises_json: str) -> int:
    import json as _json
    try:
        return int(_json.loads(exercises_json).get("estimated_duration_minutes", 60))
    except Exception:
        return 60
