import re

from fastapi import HTTPException, status

from app.schemas.workout import _LLMWorkout


_RE_REPS = re.compile(r"^\d{1,2}(-\d{1,2})?$")


def validate_workout_response(
    *,
    llm_workout: _LLMWorkout,
    valid_exercise_ids: set[int],
    target_duration_minutes: int,
) -> None:
    _validate_domain(llm_workout, valid_exercise_ids)
    _validate_structure(llm_workout, target_duration_minutes)


def _validate_domain(llm_workout: _LLMWorkout, valid_exercise_ids: set[int]) -> None:
    invalid_ids = [item.exercise_id for item in llm_workout.exercises if item.exercise_id not in valid_exercise_ids]
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"A IA retornou exercícios inválidos (IDs: {invalid_ids}). Tente gerar o treino novamente.",
        )


def _validate_structure(llm_workout: _LLMWorkout, target_duration_minutes: int) -> None:
    exercise_ids = [item.exercise_id for item in llm_workout.exercises]
    if len(exercise_ids) != len(set(exercise_ids)):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="A IA repetiu exercícios no treino. Tente gerar novamente.",
        )
    invalid_reps = [item.reps for item in llm_workout.exercises if not _RE_REPS.match(item.reps)]
    if invalid_reps:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"A IA retornou formato de repetições inválido ({invalid_reps}).",
        )
    if abs(llm_workout.estimated_duration_minutes - target_duration_minutes) > 15:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="A IA retornou duração incompatível com o solicitado.",
        )
