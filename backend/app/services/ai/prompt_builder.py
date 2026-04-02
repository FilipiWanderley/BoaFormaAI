import re
from typing import Iterable

from app.models.exercise import Exercise


SYSTEM_WORKOUT_PROMPT = (
    "Você é um personal trainer especializado em montagem de treinos personalizados.\n"
    "Você responde EXCLUSIVAMENTE com JSON válido — sem texto adicional, sem markdown.\n"
    "Você NUNCA inventa exercícios: usa apenas os exercícios da lista fornecida pelo sistema.\n"
    "Todos os campos do JSON são obrigatórios, exceto \"notes\" em cada exercício."
)

SYSTEM_CHAT_PROMPT_BASE = (
    "Você é o assistente virtual da Academia Boa Forma — personal trainer e nutricionista experiente.\n"
    "Responda em português brasileiro, de forma amigável, direta e motivadora.\n"
    "Mantenha suas respostas focadas em fitness, nutrição, recuperação e bem-estar.\n"
    "Se perguntado sobre algo fora dessa área, redirecione gentilmente."
)

GOAL_PARAMS: dict[str, str] = {
    "hipertrofia": "3-4 séries de 8-12 repetições, descanso de 60-90 segundos.",
    "força": "4-5 séries de 3-6 repetições, descanso de 2-4 minutos.",
    "resistência": "2-3 séries de 15-20 repetições, descanso de 30-45 segundos.",
    "emagrecimento": "3 séries de 12-15 repetições, descanso de 30-45 segundos, prefira circuito.",
    "condicionamento": "3 séries de 12-15 repetições, descanso de 45-60 segundos.",
    "saúde": "2-3 séries de 12-15 repetições, descanso de 60 segundos.",
    "reabilitação": "2-3 séries de 12-15 repetições leves, descanso de 60-90 segundos.",
}

INTENSITY_HINT: dict[str, str] = {
    "facil": "O último treino foi relatado como FÁCIL. Aumente a intensidade com progressão de carga, mais séries ou menor descanso.",
    "ok": "O último treino teve intensidade adequada. Mantenha nível similar.",
    "dificil": "O último treino foi relatado como DIFÍCIL. Reduza levemente a intensidade com menor volume e descanso maior.",
}


def _sanitize(value: str, max_len: int = 300) -> str:
    clean = re.sub(r"[\x00-\x1f\x7f]", " ", value or "").strip()
    if not clean:
        return "não informado"
    return clean[:max_len]


def _build_catalog(exercises: Iterable[Exercise]) -> str:
    return "\n".join(
        f"[ID:{exercise.id}] {exercise.name} | músculo: {exercise.muscle_group} | equipamento: {exercise.equipment} | nível: {exercise.level}"
        for exercise in exercises
    )


def build_workout_user_prompt(*, context: dict, exercises: list[Exercise]) -> str:
    goal = _sanitize(context["goal"], 100)
    feedback_hint = INTENSITY_HINT.get(context.get("feedback_on_last", ""), "")
    focus_hint = (
        f"Foco nos grupos musculares: {', '.join(context['muscle_groups'])}."
        if context.get("muscle_groups")
        else "Escolha o split mais adequado ao objetivo e ao histórico do aluno."
    )
    return (
        "Monte um treino completo para o seguinte aluno:\n\n"
        "PERFIL DO ALUNO\n"
        "---------------\n"
        f"Objetivo       : {goal}\n"
        f"Nível          : {context['level']}\n"
        f"Restrições     : {_sanitize(context['restrictions'])}\n"
        f"Peso           : {context['weight_kg']} kg\n"
        f"Altura         : {context['height_cm']} cm\n"
        f"Duração alvo   : {context['duration_minutes']} minutos\n\n"
        "PARÂMETROS DO TREINO\n"
        "--------------------\n"
        f"{focus_hint}\n"
        f"Parâmetros de volume para o objetivo \"{goal}\": {GOAL_PARAMS.get(goal.lower(), GOAL_PARAMS['hipertrofia'])}\n"
        f"{feedback_hint}\n\n"
        "HISTÓRICO RECENTE\n"
        "-----------------\n"
        f"{_sanitize(context['history_context'], 600)}\n\n"
        "EXERCÍCIOS DISPONÍVEIS (use APENAS estes — copie o ID exato)\n"
        "-------------------------------------------------------------\n"
        f"{_build_catalog(exercises)}\n\n"
        "FORMATO DE RESPOSTA (JSON estrito)\n"
        "-----------------------------------\n"
        "{\n"
        "  \"workout_name\": \"Nome descritivo do treino\",\n"
        "  \"focus\": \"Descrição de 1-2 frases sobre o foco e lógica do treino\",\n"
        "  \"estimated_duration_minutes\": 45,\n"
        "  \"exercises\": [\n"
        "    {\n"
        "      \"exercise_id\": 1,\n"
        "      \"exercise_name\": \"nome exato\",\n"
        "      \"sets\": 3,\n"
        "      \"reps\": \"8-12\",\n"
        "      \"rest_seconds\": 60,\n"
        "      \"notes\": \"opcional\"\n"
        "    }\n"
        "  ],\n"
        "  \"general_tips\": \"Dicas gerais para a sessão de treino\"\n"
        "}\n\n"
        "REGRAS OBRIGATÓRIAS\n"
        "-------------------\n"
        "- Inclua entre 5 e 10 exercícios.\n"
        "- Todos os exercise_id devem existir na lista fornecida.\n"
        "- Não repita exercise_id dentro do mesmo treino.\n"
        "- Ordene os exercícios de forma pedagógica (compostos antes de isolados).\n"
        "- Adapte séries, reps e descanso ao objetivo e nível do aluno.\n"
        "- Use reps no formato N ou N-M.\n"
        "- Duração estimada próxima da solicitada (diferença máxima de 15 minutos).\n"
        "- Não use exercícios contraindicados para as restrições do aluno.\n"
        "- Responda APENAS com JSON."
    )


def build_chat_system_prompt(*, context: dict, last_workout_context: str) -> str:
    return (
        f"{SYSTEM_CHAT_PROMPT_BASE}\n\n"
        "PERFIL DO ALUNO\n"
        f"Objetivo     : {_sanitize(context['goal'])}\n"
        f"Nível        : {context['level']}\n"
        f"Peso         : {context['weight_kg']} kg | Altura: {context['height_cm']} cm\n"
        f"Restrições   : {_sanitize(context['restrictions'])}\n"
        f"{_sanitize(last_workout_context, 300)}"
    )
