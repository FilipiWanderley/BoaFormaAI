import logging
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from time import perf_counter, sleep
from typing import Any, Callable, List, Optional, Tuple, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.workout import WorkoutGenerateRequest, _LLMWorkout
from app.services.ai.context_manager import build_user_context
from app.services.ai.prompt_builder import (
    SYSTEM_EXERCISE_SELECTOR_PROMPT,
    SYSTEM_WORKOUT_PROMPT,
    build_exercise_selection_prompt,
    build_workout_assembly_prompt,
    build_chat_system_prompt,
)
from app.services.ai.response_evaluator import validate_workout_response
from app.services.ai.response_handler import parse_json_response
from app.services.llm_service import _build_fallback_workout, _get_client
from app.services.metrics import metrics_store
from app.services.prompt_manager import (
    PROMPT_CHAT_ASSISTANT,
    PROMPT_WORKOUT_GENERATE,
    PROMPT_WORKOUT_SELECT,
    get_active_prompt,
    log_prompt_run,
)


_logger = logging.getLogger("app.ai_orchestrator")
T = TypeVar("T")


class _ExerciseSelection(BaseModel):
    exercise_ids: List[int] = Field(min_length=6, max_length=10)


def _execute_with_retry(operation: Callable[[], T], *, operation_name: str) -> Tuple[T, int]:
    attempts = max(1, settings.llm_max_retries + 1)
    retries = 0
    last_error: Optional[Exception] = None
    for attempt in range(attempts):
        start = perf_counter()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(operation)
            try:
                result = future.result(timeout=float(settings.llm_timeout_seconds))
                latency_ms = (perf_counter() - start) * 1000
                metrics_store.track_ai_call(operation=operation_name, latency_ms=latency_ms, retries=retries, error=False)
                return result, retries
            except FutureTimeoutError:
                last_error = TimeoutError(f"Tempo limite excedido ({settings.llm_timeout_seconds}s).")
                future.cancel()
            except Exception as exc:
                last_error = exc
        if attempt < attempts - 1:
            retries += 1
            sleep(float(settings.llm_retry_backoff_seconds) * (attempt + 1))
    metrics_store.track_ai_call(operation=operation_name, retries=retries, error=True)
    if last_error is None:
        raise RuntimeError("Falha inesperada ao executar operação de IA.")
    raise last_error


def generate_workout_plan(
    *,
    db: Optional[Session],
    user: User,
    exercises: list[Exercise],
    request: WorkoutGenerateRequest,
    history_context: str,
    client: Optional[Any] = None,
) -> _LLMWorkout:
    context = build_user_context(user, request, history_context)
    selector_prompt = build_exercise_selection_prompt(context=context, exercises=exercises)
    selector_template = get_active_prompt(
        db,
        name=PROMPT_WORKOUT_SELECT,
        fallback_content=SYSTEM_EXERCISE_SELECTOR_PROMPT,
    ) if db else None
    selector_system_prompt = selector_template.content if selector_template else SYSTEM_EXERCISE_SELECTOR_PROMPT
    generator_template = get_active_prompt(
        db,
        name=PROMPT_WORKOUT_GENERATE,
        fallback_content=SYSTEM_WORKOUT_PROMPT,
    ) if db else None
    generator_system_prompt = generator_template.content if generator_template else SYSTEM_WORKOUT_PROMPT
    llm_client = client or _get_client()

    def _attempt_select() -> List[int]:
        completion = llm_client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": selector_system_prompt},
                {"role": "user", "content": selector_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=1024,
        )
        raw = completion.choices[0].message.content or ""
        data = parse_json_response(raw)
        parsed = _ExerciseSelection.model_validate(data)
        return parsed.exercise_ids

    selected_exercises: List[Exercise] = exercises[: min(8, len(exercises))]
    select_retries = 0
    select_elapsed_ms = 0.0
    try:
        select_start = perf_counter()
        selected_ids, select_retries = _execute_with_retry(_attempt_select, operation_name="workout_select_exercises")
        select_elapsed_ms = (perf_counter() - select_start) * 1000
        selected_exercises = _resolve_selected_exercises(exercises=exercises, selected_ids=selected_ids)
        _logger.info("ai_select_ok retries=%s elapsed_ms=%.2f selected=%s", select_retries, select_elapsed_ms, len(selected_exercises))
        if db and selector_template:
            log_prompt_run(
                db,
                operation="workout_select_exercises",
                prompt_name=PROMPT_WORKOUT_SELECT,
                prompt_version=selector_template.version,
                context_json=json.dumps(context, ensure_ascii=False),
                response_json=json.dumps({"exercise_ids": [item.id for item in selected_exercises]}, ensure_ascii=False),
                latency_ms=int(select_elapsed_ms),
                retries=select_retries,
            )
    except Exception as exc:
        select_elapsed_ms = (perf_counter() - select_start) * 1000
        _logger.exception("ai_select_error elapsed_ms=%.2f detail=%s", select_elapsed_ms, str(exc))
        if db and selector_template:
            log_prompt_run(
                db,
                operation="workout_select_exercises",
                prompt_name=PROMPT_WORKOUT_SELECT,
                prompt_version=selector_template.version,
                context_json=json.dumps(context, ensure_ascii=False),
                response_json="",
                latency_ms=int(select_elapsed_ms),
                retries=settings.llm_max_retries,
                error_text=str(exc)[:4000],
            )
        if not settings.llm_enable_fallback:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Falha na seleção de exercícios pela IA: {exc}",
            )

    workout_prompt = build_workout_assembly_prompt(context=context, selected_exercises=selected_exercises)
    valid_ids = {exercise.id for exercise in selected_exercises}

    def _attempt_assembly() -> _LLMWorkout:
        completion = llm_client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": generator_system_prompt},
                {"role": "user", "content": workout_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
            max_tokens=2048,
        )
        raw = completion.choices[0].message.content or ""
        data = parse_json_response(raw)
        llm_workout = _LLMWorkout.model_validate(data)
        validate_workout_response(
            llm_workout=llm_workout,
            valid_exercise_ids=valid_ids,
            target_duration_minutes=request.duration_minutes,
        )
        return llm_workout

    start = perf_counter()
    try:
        workout, retries = _execute_with_retry(_attempt_assembly, operation_name="workout_generate")
        elapsed_ms = (perf_counter() - start) * 1000
        _logger.info("ai_workout_ok retries=%s elapsed_ms=%.2f prompt_len=%s selected=%s", retries, elapsed_ms, len(workout_prompt), len(selected_exercises))
        if db and generator_template:
            log_prompt_run(
                db,
                operation="workout_generate",
                prompt_name=PROMPT_WORKOUT_GENERATE,
                prompt_version=generator_template.version,
                context_json=json.dumps(context, ensure_ascii=False),
                response_json=workout.model_dump_json(),
                latency_ms=int(elapsed_ms),
                retries=retries,
            )
        return workout
    except Exception as exc:
        elapsed_ms = (perf_counter() - start) * 1000
        _logger.exception("ai_workout_error elapsed_ms=%.2f detail=%s", elapsed_ms, str(exc))
        if db and generator_template:
            log_prompt_run(
                db,
                operation="workout_generate",
                prompt_name=PROMPT_WORKOUT_GENERATE,
                prompt_version=generator_template.version,
                context_json=json.dumps(context, ensure_ascii=False),
                response_json="",
                latency_ms=int(elapsed_ms),
                retries=settings.llm_max_retries,
                error_text=str(exc)[:4000],
            )
        if settings.llm_enable_fallback:
            return _build_fallback_workout(exercises, request)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na comunicação com o serviço de IA: {exc}",
        )


def _resolve_selected_exercises(*, exercises: List[Exercise], selected_ids: List[int]) -> List[Exercise]:
    by_id = {exercise.id: exercise for exercise in exercises}
    chosen: List[Exercise] = []
    seen: set[int] = set()
    for exercise_id in selected_ids:
        exercise = by_id.get(exercise_id)
        if exercise and exercise_id not in seen:
            chosen.append(exercise)
            seen.add(exercise_id)
    if len(chosen) < 5:
        return exercises[: min(8, len(exercises))]
    return chosen


def generate_chat_reply(
    *,
    db: Optional[Session],
    user: User,
    system_last_workout_context: str,
    messages: List[dict],
    client: Optional[Any] = None,
) -> str:
    context = {
        "goal": user.goal,
        "level": user.level,
        "weight_kg": user.weight_kg,
        "height_cm": user.height_cm,
        "restrictions": user.restrictions or "",
    }
    built_system_prompt = build_chat_system_prompt(context=context, last_workout_context=system_last_workout_context)
    prompt_template = get_active_prompt(db, name=PROMPT_CHAT_ASSISTANT, fallback_content=built_system_prompt) if db else None
    system_prompt = prompt_template.content if prompt_template else built_system_prompt
    payload = [{"role": "system", "content": system_prompt}, *messages]
    llm_client = client or _get_client()

    def _attempt() -> str:
        completion = llm_client.chat.completions.create(
            model=settings.groq_model,
            messages=payload,
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content or ""

    start = perf_counter()
    try:
        reply, retries = _execute_with_retry(_attempt, operation_name="chat_reply")
        elapsed_ms = (perf_counter() - start) * 1000
        _logger.info("ai_chat_ok retries=%s elapsed_ms=%.2f prompt_len=%s", retries, elapsed_ms, sum(len(item.get("content", "")) for item in payload))
        if db and prompt_template:
            log_prompt_run(
                db,
                operation="chat_reply",
                prompt_name=PROMPT_CHAT_ASSISTANT,
                prompt_version=prompt_template.version,
                context_json=json.dumps({"user_context": context, "message_count": len(messages)}, ensure_ascii=False),
                response_json=reply,
                latency_ms=int(elapsed_ms),
                retries=retries,
            )
        return reply
    except Exception as exc:
        elapsed_ms = (perf_counter() - start) * 1000
        _logger.exception("ai_chat_error elapsed_ms=%.2f detail=%s", elapsed_ms, str(exc))
        if db and prompt_template:
            log_prompt_run(
                db,
                operation="chat_reply",
                prompt_name=PROMPT_CHAT_ASSISTANT,
                prompt_version=prompt_template.version,
                context_json=json.dumps({"user_context": context, "message_count": len(messages)}, ensure_ascii=False),
                response_json="",
                latency_ms=int(elapsed_ms),
                retries=settings.llm_max_retries,
                error_text=str(exc)[:4000],
            )
        if settings.llm_enable_fallback:
            return (
                "Estou com instabilidade temporária no serviço de IA. "
                "Posso continuar com orientações básicas de treino e segurança enquanto normaliza."
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na comunicação com o serviço de IA: {exc}",
        )
