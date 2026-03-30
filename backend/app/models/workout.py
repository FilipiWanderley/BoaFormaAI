from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    exercises_json: Mapped[str] = mapped_column(Text)
    prompt_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # easy/ok/hard

    user: Mapped["User"] = relationship(back_populates="workouts")  # noqa: F821
    history: Mapped[List["History"]] = relationship(back_populates="workout")
    workout_exercises: Mapped[List["WorkoutExercise"]] = relationship(  # noqa: F821
        back_populates="workout", cascade="all, delete-orphan", order_by="WorkoutExercise.order"
    )


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id", ondelete="CASCADE"))
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    workout: Mapped["Workout"] = relationship(back_populates="history")
