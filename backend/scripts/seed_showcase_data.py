import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models.chat import ChatMessage
from app.models.exercise import Exercise, WorkoutExercise
from app.models.user import User
from app.models.workout import History, Workout
from app.services.auth import hash_password


DEMO_EMAIL = "demo@boaforma.ai"
DEMO_PASSWORD = "Demo@12345"


def _pick_exercises(db, muscle_group: str, amount: int = 6) -> list[Exercise]:
    selected = (
        db.query(Exercise)
        .filter(Exercise.muscle_group == muscle_group)
        .order_by(Exercise.name.asc())
        .limit(amount)
        .all()
    )
    if len(selected) >= amount:
        return selected
    fallback = db.query(Exercise).order_by(Exercise.name.asc()).limit(amount).all()
    return fallback


def _build_workout_payload(name: str, focus: str, duration: int, exercises: list[Exercise]) -> str:
    payload = {
        "workout_name": name,
        "focus": focus,
        "estimated_duration_minutes": duration,
        "exercises": [
            {
                "exercise_id": ex.id,
                "exercise_name": ex.name,
                "sets": 4 if i < 2 else 3,
                "reps": "8-12",
                "rest_seconds": 90 if i < 2 else 60,
                "notes": "Execução controlada e foco em técnica.",
            }
            for i, ex in enumerate(exercises[:6])
        ],
        "general_tips": "Hidrate-se, mantenha boa técnica e ajuste carga progressivamente.",
    }
    return json.dumps(payload, ensure_ascii=False)


def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if existing:
            db.delete(existing)
            db.commit()

        user = User(
            name="Filipi Moraes",
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
            provider="email",
            is_admin=True,
            consent_given_at=datetime.now(timezone.utc),
            privacy_policy_version="2026-01",
            avatar_url="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=600",
            age=29,
            weight_kg=82,
            height_cm=178,
            goal="hipertrofia",
            level="intermediario",
            restrictions="nenhuma",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        blueprints = [
            ("Push Day Premium", "Peito, ombros e tríceps", "peito", 60, "ok", 0),
            ("Pull Performance", "Costas e bíceps", "costas", 55, "facil", 1),
            ("Leg Day Intenso", "Quadríceps, posterior e glúteos", "quadriceps", 70, "dificil", 2),
            ("Upper Balance", "Tronco completo", "ombros", 50, "ok", 3),
            ("Full Body Metabólico", "Corpo inteiro e condicionamento", "abdomen", 45, None, 5),
        ]

        for name, focus, group, duration, feedback, days_ago in blueprints:
            selected = _pick_exercises(db, group)
            workout = Workout(
                user_id=user.id,
                exercises_json=_build_workout_payload(name, focus, duration, selected),
                prompt_context=json.dumps(
                    {
                        "muscle_groups": [group],
                        "duration_minutes": duration,
                        "feedback_on_last": feedback,
                    },
                    ensure_ascii=False,
                ),
                feedback=feedback,
            )
            workout.created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
            db.add(workout)
            db.flush()

            for order, ex in enumerate(selected[:6], start=1):
                db.add(
                    WorkoutExercise(
                        workout_id=workout.id,
                        exercise_id=ex.id,
                        sets=4 if order <= 2 else 3,
                        reps="8-12",
                        rest_seconds=90 if order <= 2 else 60,
                        order=order,
                    )
                )

            if days_ago <= 3:
                history = History(
                    user_id=user.id,
                    workout_id=workout.id,
                    notes="Treino concluído com ótima execução.",
                )
                history.completed_at = workout.created_at + timedelta(hours=1)
                db.add(history)

        chat_rows = [
            ("user", "Como melhorar meu desempenho no supino reto?"),
            ("assistant", "Priorize progressão de carga semanal, mantenha escápulas estáveis e faça aquecimento progressivo."),
            ("user", "Dá para encaixar cardio sem perder hipertrofia?"),
            ("assistant", "Sim. Faça 2-3 sessões leves de 20-30 min em dias alternados e mantenha ingestão proteica adequada."),
            ("user", "Me passa uma dica rápida para recuperação muscular."),
            ("assistant", "Sono de qualidade, hidratação e ingestão proteica de 1.6-2.2g/kg são os pilares da recuperação."),
        ]
        now = datetime.now(timezone.utc)
        for idx, (role, content) in enumerate(chat_rows):
            row = ChatMessage(user_id=user.id, role=role, content=content)
            row.created_at = now - timedelta(minutes=(len(chat_rows) - idx) * 8)
            db.add(row)

        db.commit()
        print(f"Usuário demo criado: {DEMO_EMAIL}")
        print(f"Senha demo: {DEMO_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
