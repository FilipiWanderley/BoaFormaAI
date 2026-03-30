from typing import List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    muscle_group: Mapped[str] = mapped_column(String(50), index=True)
    secondary_muscles: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    equipment: Mapped[str] = mapped_column(String(50), index=True)
    level: Mapped[str] = mapped_column(String(20), index=True)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    # Comma-separated injury/condition keywords, e.g. "joelho,lombar"
    # Matched against free-text user.restrictions at query time.
    contraindications: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    workout_exercises: Mapped[List["WorkoutExercise"]] = relationship(
        back_populates="exercise"
    )

    __table_args__ = (
        CheckConstraint(
            "level IN ('iniciante', 'intermediario', 'avancado')",
            name="ck_exercises_level",
        ),
    )


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"), index=True
    )
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[str] = mapped_column(String(20))  # "12" or "8-12"
    rest_seconds: Mapped[int] = mapped_column(Integer)
    order: Mapped[int] = mapped_column(Integer)  # position within the workout

    workout: Mapped["Workout"] = relationship(back_populates="workout_exercises")  # noqa: F821
    exercise: Mapped["Exercise"] = relationship(back_populates="workout_exercises")
