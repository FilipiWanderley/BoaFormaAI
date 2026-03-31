"""
LLM integration layer — Groq client, prompt construction and response parsing.

Responsibilities:
- Build structured, injection-resistant prompts
- Call Groq with JSON mode enabled
- Parse and validate the raw LLM response against our internal schema
- Never expose raw LLM output to callers; always return typed objects
"""

import json
from collections import Counter
import re
from typing import List, Optional

from fastapi import HTTPException, status
from groq import Groq

from app.config import settings
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.workout import WorkoutGenerateRequest, _LLMWorkout
from app.services.llm_resilience import execute_with_retry
from app.services.metrics import metrics_store

# ---------------------------------------------------------------------------
# Client — lazy singleton
# ---------------------------------------------------------------------------

_groq_client: Optional[Groq] = None


def _get_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        if not settings.groq_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de IA não configurado. Contate o administrador.",
            )
        _groq_client = Groq(api_key=settings.groq_api_key)
    return _groq_client


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

_INTENSITY_HINT: dict[str, str] = {
    "facil": (
        "O último treino foi relatado como FÁCIL. Aumente a intensidade: "
        "adicione mais séries, reduza o descanso ou inclua exercícios mais desafiadores."
    ),
    "ok": "O último treino teve intensidade adequada. Mantenha nível similar.",
    "dificil": (
        "O último treino foi relatado como DIFÍCIL. Reduza levemente a intensidade: "
        "diminua as séries ou aumente o tempo de descanso."
    ),
}

_GOAL_PARAMS: dict[str, str] = {
    "hipertrofia": "3-4 séries de 8-12 repetições, descanso de 60-90 segundos.",
    "força":       "4-5 séries de 3-6 repetições, descanso de 2-4 minutos.",
    "resistência": "2-3 séries de 15-20 repetições, descanso de 30-45 segundos.",
    "emagrecimento": "3 séries de 12-15 repetições, descanso de 30-45 segundos, prefira circuito.",
    "condicionamento": "3 séries de 12-15 repetições, descanso de 45-60 segundos.",
    "saúde":       "2-3 séries de 12-15 repetições, descanso de 60 segundos.",
    "reabilitação": "2-3 séries de 12-15 repetições leves, descanso de 60-90 segundos.",
}

_SYSTEM_PROMPT = """\
Você é um personal trainer especializado em montagem de treinos personalizados.
Você responde EXCLUSIVAMENTE com JSON válido — sem texto adicional, sem markdown.
Você NUNCA inventa exercícios: usa apenas os exercícios da lista fornecida pelo sistema.
Todos os campos do JSON são obrigatórios, exceto "notes" em cada exercício.\
"""

_REPS_PATTERN = re.compile(r"^\d{1,2}(-\d{1,2})?$")


def _sanitize(value: Optional[str], max_len: int = 200) -> str:
    """Remove control characters and truncate user-controlled strings."""
    if not value:
        return "não informado"
    clean = re.sub(r"[\x00-\x1f\x7f]", " ", value)
    return clean[:max_len].strip()


def _build_exercise_catalog(exercises: List[Exercise]) -> str:
    lines = [
        f"[ID:{ex.id}] {ex.name} | músculo: {ex.muscle_group} | equipamento: {ex.equipment} | nível: {ex.level}"
        for ex in exercises
    ]
    return "\n".join(lines)


def _build_user_prompt(
    user: User,
    exercises: List[Exercise],
    request: WorkoutGenerateRequest,
    history_context: Optional[str] = None,
) -> str:
    goal_params = _GOAL_PARAMS.get(
        user.goal.lower(),
        "3-4 séries de 8-12 repetições, descanso de 60-90 segundos.",
    )
    feedback_hint = (
        _INTENSITY_HINT[request.feedback_on_last]
        if request.feedback_on_last
        else ""
    )
    focus_hint = (
        f"Foco nos grupos musculares: {', '.join(request.muscle_groups)}."
        if request.muscle_groups
        else "Escolha o split mais adequado ao objetivo e ao histórico do aluno."
    )

    return f"""\
Monte um treino completo para o seguinte aluno:

PERFIL DO ALUNO
---------------
Objetivo       : {_sanitize(user.goal)}
Nível          : {user.level}
Restrições     : {_sanitize(user.restrictions)}
Peso           : {user.weight_kg} kg
Altura         : {user.height_cm} cm
Duração alvo   : {request.duration_minutes} minutos

PARÂMETROS DO TREINO
--------------------
{focus_hint}
Parâmetros de volume para o objetivo "{_sanitize(user.goal)}": {goal_params}
{feedback_hint}

HISTÓRICO RECENTE
-----------------
{_sanitize(history_context, max_len=400)}

EXERCÍCIOS DISPONÍVEIS (use APENAS estes — copie o ID exato)
-------------------------------------------------------------
{_build_exercise_catalog(exercises)}

FORMATO DE RESPOSTA (JSON estrito)
-----------------------------------
{{
  "workout_name": "Nome descritivo do treino",
  "focus": "Descrição de 1-2 frases sobre o foco e lógica do treino",
  "estimated_duration_minutes": <número inteiro>,
  "exercises": [
    {{
      "exercise_id": <ID numérico da lista acima>,
      "exercise_name": "<nome exato da lista acima>",
      "sets": <número de séries>,
      "reps": "<número ou faixa, ex: 12 ou 8-12>",
      "rest_seconds": <segundos de descanso>,
      "notes": "<dica de execução opcional ou null>"
    }}
  ],
  "general_tips": "Dicas gerais para a sessão de treino"
}}

REGRAS OBRIGATÓRIAS
-------------------
- Inclua entre 5 e 10 exercícios.
- Todos os exercise_id devem existir na lista fornecida.
- Não repita exercise_id dentro do mesmo treino.
- Ordene os exercícios de forma pedagógica (compostos antes de isolados).
- Adapte séries, reps e descanso ao objetivo e nível do aluno.
- Use "reps" no formato "N" ou "N-M" (ex: "12" ou "8-12").
- A duração estimada deve ficar próxima da duração alvo (diferença máxima de 15 minutos).
- Não use exercícios contraindicados para as restrições do aluno.
- Responda APENAS com o JSON — nenhum texto antes ou depois.\
"""


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def _extract_json(raw: str) -> str:
    """
    Extract the first JSON object from the raw string.
    Handles cases where the model adds markdown fences or preamble text.
    """
    # Try to find a JSON block between ```json ... ```
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if fence_match:
        return fence_match.group(1)

    # Fall back to first {...} block
    brace_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if brace_match:
        return brace_match.group(0)

    return raw


def call_groq_for_workout(
    user: User,
    exercises: List[Exercise],
    request: WorkoutGenerateRequest,
    history_context: Optional[str] = None,
) -> _LLMWorkout:
    """
    Calls Groq and returns a validated _LLMWorkout.
    Raises HTTPException on any LLM or parsing failure.
    """
    client = _get_client()
    user_prompt = _build_user_prompt(user, exercises, request, history_context)
    valid_ids = {ex.id for ex in exercises}

    def _attempt() -> _LLMWorkout:
        metrics_store.track_ai_call()
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
            max_tokens=2048,
        )
        raw_content = completion.choices[0].message.content or ""
        json_str = _extract_json(raw_content)
        data = json.loads(json_str)
        llm_workout = _LLMWorkout.model_validate(data)
        _validate_exercise_ids(llm_workout, valid_ids)
        _validate_workout_quality(llm_workout, request.duration_minutes)
        return llm_workout

    try:
        return execute_with_retry(
            _attempt,
            timeout_seconds=float(settings.llm_timeout_seconds),
            max_retries=settings.llm_max_retries,
            backoff_seconds=float(settings.llm_retry_backoff_seconds),
        )
    except Exception as exc:
        if settings.llm_enable_fallback:
            return _build_fallback_workout(exercises, request)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na comunicação com o serviço de IA: {exc}",
        )


def _build_fallback_workout(exercises: List[Exercise], request: WorkoutGenerateRequest) -> _LLMWorkout:
    selected = exercises[: min(6, len(exercises))]
    if len(selected) < 4:
        selected = exercises[:4]

    goal = request.feedback_on_last or "ok"
    if goal == "dificil":
        sets, reps, rest = 3, "10-12", 75
    elif goal == "facil":
        sets, reps, rest = 4, "8-12", 60
    else:
        sets, reps, rest = 3, "10-12", 60

    workout_exercises = [
        {
            "exercise_id": ex.id,
            "exercise_name": ex.name,
            "sets": sets,
            "reps": reps,
            "rest_seconds": rest,
            "notes": "Treino gerado em modo de contingência. Ajuste carga conforme percepção de esforço.",
        }
        for ex in selected
    ]

    estimated = min(max(request.duration_minutes, 20), 120)
    return _LLMWorkout.model_validate(
        {
            "workout_name": "Treino Base de Contingência",
            "focus": "Plano temporário gerado automaticamente para manter a consistência do treino.",
            "estimated_duration_minutes": estimated,
            "exercises": workout_exercises,
            "general_tips": "Mantenha técnica estrita e interrompa se houver dor aguda.",
        }
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _validate_exercise_ids(llm_workout: _LLMWorkout, valid_ids: set[int]) -> None:
    """Ensure the LLM did not hallucinate exercise IDs outside our filtered set."""
    invalid = [
        ex.exercise_id
        for ex in llm_workout.exercises
        if ex.exercise_id not in valid_ids
    ]
    if invalid:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                f"A IA retornou exercícios inválidos (IDs: {invalid}). "
                "Tente gerar o treino novamente."
            ),
        )


def _validate_workout_quality(llm_workout: _LLMWorkout, target_duration_minutes: int) -> None:
    exercise_ids = [item.exercise_id for item in llm_workout.exercises]
    id_counts = Counter(exercise_ids)
    duplicate_ids = sorted([ex_id for ex_id, count in id_counts.items() if count > 1])
    if duplicate_ids:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                f"A IA repetiu exercícios no treino (IDs duplicados: {duplicate_ids}). "
                "Tente gerar novamente."
            ),
        )

    invalid_reps = [item.reps for item in llm_workout.exercises if not _REPS_PATTERN.match(item.reps)]
    if invalid_reps:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                f"A IA retornou formato de repetições inválido ({invalid_reps}). "
                "Use apenas N ou N-M."
            ),
        )

    if abs(llm_workout.estimated_duration_minutes - target_duration_minutes) > 15:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "A IA retornou duração incompatível com o solicitado. "
                "Tente gerar o treino novamente."
            ),
        )
