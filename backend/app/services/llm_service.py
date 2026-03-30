"""
LLM integration layer — Groq client, prompt construction and response parsing.

Responsibilities:
- Build structured, injection-resistant prompts
- Call Groq with JSON mode enabled
- Parse and validate the raw LLM response against our internal schema
- Never expose raw LLM output to callers; always return typed objects
"""

import json
import re
from typing import List, Optional

from fastapi import HTTPException, status
from groq import Groq

from app.config import settings
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.workout import WorkoutGenerateRequest, _LLMWorkout

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
- Ordene os exercícios de forma pedagógica (compostos antes de isolados).
- Adapte séries, reps e descanso ao objetivo e nível do aluno.
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
) -> _LLMWorkout:
    """
    Calls Groq and returns a validated _LLMWorkout.
    Raises HTTPException on any LLM or parsing failure.
    """
    client = _get_client()
    user_prompt = _build_user_prompt(user, exercises, request)
    valid_ids = {ex.id for ex in exercises}

    try:
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,  # low enough for consistent structure, high enough for variety
            max_tokens=2048,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha na comunicação com o serviço de IA: {exc}",
        )

    raw_content = completion.choices[0].message.content or ""

    try:
        json_str = _extract_json(raw_content)
        data = json.loads(json_str)
        llm_workout = _LLMWorkout.model_validate(data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"A IA retornou uma resposta inválida. Tente novamente. ({exc})",
        )

    _validate_exercise_ids(llm_workout, valid_ids)
    return llm_workout


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
