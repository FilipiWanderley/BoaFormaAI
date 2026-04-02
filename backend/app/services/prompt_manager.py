from __future__ import annotations

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.ai_prompt import AIPromptRun, PromptTemplate


PROMPT_WORKOUT_GENERATE = "generate_workout"
PROMPT_CHAT_ASSISTANT = "chat_assistant"


def get_active_prompt(db: Session, *, name: str, fallback_content: str) -> PromptTemplate:
    latest = (
        db.query(PromptTemplate)
        .filter(PromptTemplate.name == name)
        .order_by(desc(PromptTemplate.id))
        .first()
    )
    if latest:
        return latest
    first = PromptTemplate(name=name, version="v1", content=fallback_content)
    db.add(first)
    db.commit()
    db.refresh(first)
    return first


def create_prompt_version(db: Session, *, name: str, content: str) -> PromptTemplate:
    latest = (
        db.query(PromptTemplate)
        .filter(PromptTemplate.name == name)
        .order_by(desc(PromptTemplate.id))
        .first()
    )
    if latest and latest.content == content:
        return latest
    next_number = 1
    if latest and latest.version.startswith("v") and latest.version[1:].isdigit():
        next_number = int(latest.version[1:]) + 1
    created = PromptTemplate(name=name, version=f"v{next_number}", content=content)
    db.add(created)
    db.commit()
    db.refresh(created)
    return created


def rollback_prompt(db: Session, *, name: str, version: str) -> PromptTemplate:
    target = (
        db.query(PromptTemplate)
        .filter(PromptTemplate.name == name, PromptTemplate.version == version)
        .order_by(desc(PromptTemplate.id))
        .first()
    )
    if target is None:
        raise ValueError(f"Prompt {name} na versão {version} não encontrado.")
    return create_prompt_version(db, name=name, content=target.content)


def log_prompt_run(
    db: Session,
    *,
    operation: str,
    prompt_name: str,
    prompt_version: str,
    context_json: str,
    response_json: str,
    latency_ms: int,
    retries: int,
    error_text: str = "",
) -> None:
    row = AIPromptRun(
        operation=operation,
        prompt_name=prompt_name,
        prompt_version=prompt_version,
        context_json=context_json,
        response_json=response_json,
        latency_ms=latency_ms,
        retries=retries,
        error_text=error_text,
    )
    db.add(row)
    db.commit()
