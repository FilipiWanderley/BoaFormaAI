"""
Chat service — conversational AI with per-user memory.

Design:
- Last MEMORY_WINDOW messages from the DB are sent as context to the LLM.
- Both user and assistant turns are persisted after each exchange.
- The system prompt is rebuilt on every request to reflect the latest user profile.
"""

import json
from typing import List

from sqlalchemy.orm import Session

from app.models.chat import ChatMessage
from app.models.user import User
from app.models.workout import Workout
from app.schemas.chat import ChatMessageResponse, ChatResponse
from app.services.ai_orchestrator import generate_chat_reply
from app.services.llm_service import _get_client, _sanitize

MEMORY_WINDOW = 10  # number of past messages sent as context


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def _build_system_prompt(user: User, db: Session) -> str:
    last_workout_ctx = _last_workout_context(db, user.id)
    return (
        "Você é o assistente virtual da Academia Boa Forma — personal trainer e "
        "nutricionista experiente.\n"
        "Responda em português brasileiro, de forma amigável, direta e motivadora.\n"
        "Mantenha suas respostas focadas em fitness, nutrição, recuperação e bem-estar.\n"
        "Se perguntado sobre algo fora dessa área, redirecione gentilmente.\n\n"
        "PERFIL DO ALUNO\n"
        f"Objetivo     : {_sanitize(user.goal)}\n"
        f"Nível        : {user.level}\n"
        f"Peso         : {user.weight_kg} kg | Altura: {user.height_cm} cm\n"
        f"Restrições   : {_sanitize(user.restrictions)}\n"
        f"{last_workout_ctx}"
    )


def _last_workout_context(db: Session, user_id: int) -> str:
    last = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .order_by(Workout.created_at.desc())
        .first()
    )
    if not last:
        return ""
    try:
        data = json.loads(last.exercises_json)
        name = data.get("workout_name", "Treino")
        focus = data.get("focus", "")
        return f"Último treino gerado : {name} — {focus}\n"
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------

def _load_recent_messages(db: Session, user_id: int) -> List[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(MEMORY_WINDOW)
        .all()[::-1]  # chronological order
    )


def _save_turn(
    db: Session,
    user_id: int,
    user_text: str,
    assistant_text: str,
) -> ChatMessage:
    user_msg = ChatMessage(user_id=user_id, role="user", content=user_text)
    assistant_msg = ChatMessage(user_id=user_id, role="assistant", content=assistant_text)
    db.add_all([user_msg, assistant_msg])
    db.commit()
    db.refresh(assistant_msg)
    return assistant_msg


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def chat(db: Session, user: User, message: str) -> ChatResponse:
    system_prompt = _build_system_prompt(user, db)
    history = _load_recent_messages(db, user.id)
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": message})
    reply_text = generate_chat_reply(
        db=db,
        user=user,
        system_last_workout_context=system_prompt,
        messages=messages,
        client=_get_client(),
    )
    assistant_record = _save_turn(db, user.id, message, reply_text)

    # Reload the full window so the response includes the saved turn
    updated_history = _load_recent_messages(db, user.id)

    return ChatResponse(
        reply=ChatMessageResponse.model_validate(assistant_record),
        history=[ChatMessageResponse.model_validate(m) for m in updated_history],
    )


def list_chat_history(
    db: Session,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
) -> List[ChatMessageResponse]:
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()[::-1]
    )
    return [ChatMessageResponse.model_validate(m) for m in messages]


def clear_chat_history(db: Session, user_id: int) -> None:
    db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
    db.commit()
