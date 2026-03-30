import json
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.workout import History, Workout
from app.schemas.history import HistoryCreate, HistoryResponse


def _workout_name_from_json(exercises_json: str) -> str:
    try:
        return json.loads(exercises_json).get("workout_name", "Treino")
    except Exception:
        return "Treino"


def complete_workout(
    db: Session,
    user_id: int,
    data: HistoryCreate,
) -> HistoryResponse:
    workout = (
        db.query(Workout)
        .filter(Workout.id == data.workout_id, Workout.user_id == user_id)
        .first()
    )
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado.",
        )

    already_done = (
        db.query(History)
        .filter(History.workout_id == data.workout_id, History.user_id == user_id)
        .first()
    )
    if already_done:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este treino já foi marcado como concluído.",
        )

    record = History(
        user_id=user_id,
        workout_id=data.workout_id,
        notes=data.notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return HistoryResponse(
        id=record.id,
        workout_id=record.workout_id,
        workout_name=_workout_name_from_json(workout.exercises_json),
        completed_at=record.completed_at,
        notes=record.notes,
    )


def list_history(
    db: Session,
    user_id: int,
    limit: int = 30,
    offset: int = 0,
) -> List[HistoryResponse]:
    records = (
        db.query(History, Workout)
        .join(Workout, History.workout_id == Workout.id)
        .filter(History.user_id == user_id)
        .order_by(History.completed_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        HistoryResponse(
            id=h.id,
            workout_id=h.workout_id,
            workout_name=_workout_name_from_json(w.exercises_json),
            completed_at=h.completed_at,
            notes=h.notes,
        )
        for h, w in records
    ]
