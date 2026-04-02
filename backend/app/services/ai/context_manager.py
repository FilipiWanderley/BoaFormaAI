from app.models.user import User
from app.schemas.workout import WorkoutGenerateRequest


def build_user_context(user: User, request: WorkoutGenerateRequest, history_context: str) -> dict:
    return {
        "goal": user.goal,
        "level": user.level,
        "restrictions": user.restrictions or "não informado",
        "weight_kg": user.weight_kg,
        "height_cm": user.height_cm,
        "duration_minutes": request.duration_minutes,
        "muscle_groups": request.muscle_groups or [],
        "equipment_available": request.equipment_available or [],
        "feedback_on_last": request.feedback_on_last or "",
        "history_context": history_context or "Sem histórico de treino anterior.",
    }
