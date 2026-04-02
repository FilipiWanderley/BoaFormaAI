from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PromptTemplate(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), index=True)
    version: Mapped[str] = mapped_column(String(20), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AIPromptRun(Base):
    __tablename__ = "ai_prompt_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    operation: Mapped[str] = mapped_column(String(50), index=True)
    prompt_name: Mapped[str] = mapped_column(String(80), index=True)
    prompt_version: Mapped[str] = mapped_column(String(20), index=True)
    context_json: Mapped[str] = mapped_column(Text)
    response_json: Mapped[str] = mapped_column(Text)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    retries: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    error_text: Mapped[str] = mapped_column(Text, default="", server_default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
