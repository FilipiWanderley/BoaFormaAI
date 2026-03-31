from typing import List, Optional

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider: Mapped[str] = mapped_column(String(20), default="email", server_default="email")
    provider_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True, index=True)
    age: Mapped[int] = mapped_column()
    weight_kg: Mapped[float] = mapped_column()
    height_cm: Mapped[float] = mapped_column()
    goal: Mapped[str] = mapped_column(String(50))
    level: Mapped[str] = mapped_column(String(20))
    restrictions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    workouts: Mapped[List["Workout"]] = relationship(back_populates="user")  # noqa: F821
    chat_messages: Mapped[List["ChatMessage"]] = relationship(back_populates="user")  # noqa: F821

    __table_args__ = (
        CheckConstraint("age > 0 AND age < 120", name="ck_users_age"),
        CheckConstraint("weight_kg > 0", name="ck_users_weight"),
        CheckConstraint("height_cm > 0", name="ck_users_height"),
        CheckConstraint(
            "level IN ('iniciante', 'intermediario', 'avancado')",
            name="ck_users_level",
        ),
    )
