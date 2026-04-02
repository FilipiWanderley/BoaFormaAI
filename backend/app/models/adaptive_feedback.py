from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserAdaptiveProfile(Base):
    __tablename__ = "user_adaptive_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    total_feedbacks: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    easy_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    ok_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    hard_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    last_feedback: Mapped[str] = mapped_column(String(20), default="", server_default="")
    preferred_intensity: Mapped[str] = mapped_column(String(30), default="balanced", server_default="balanced")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
