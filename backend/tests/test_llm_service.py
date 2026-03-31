import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException

from app.schemas.workout import WorkoutGenerateRequest
from app.services.llm_service import (
    _build_user_prompt,
    _extract_json,
    _validate_exercise_ids,
    _validate_workout_quality,
    call_groq_for_workout,
)


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = _FakeMessage(content)


class _FakeCompletion:
    def __init__(self, content: str) -> None:
        self.choices = [_FakeChoice(content)]


class _FakeCompletions:
    def create(self, **_kwargs) -> _FakeCompletion:
        payload = (
            '{"workout_name":"Treino IA","focus":"Foco em superiores",'
            '"estimated_duration_minutes":50,'
            '"exercises":[{"exercise_id":1,"exercise_name":"Supino","sets":3,"reps":"10-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":2,"exercise_name":"Remada","sets":3,"reps":"10-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":3,"exercise_name":"Desenvolvimento","sets":3,"reps":"10-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":4,"exercise_name":"Rosca","sets":3,"reps":"10-12","rest_seconds":45,"notes":null}],'
            '"general_tips":"Mantenha postura e controle de carga."}'
        )
        return _FakeCompletion(payload)


class _AlwaysFailCompletions:
    def create(self, **_kwargs):
        raise RuntimeError("llm unavailable")


class _AlwaysFailGroqClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=_AlwaysFailCompletions())


class _FakeChat:
    def __init__(self) -> None:
        self.completions = _FakeCompletions()


class _FakeGroqClient:
    def __init__(self) -> None:
        self.chat = _FakeChat()


class LlmServiceTests(unittest.TestCase):
    def test_extract_json_from_markdown_block(self) -> None:
        raw = "```json\n{\"ok\": true}\n```"
        self.assertEqual(_extract_json(raw), "{\"ok\": true}")

    def test_validate_exercise_ids_rejects_outside_catalog(self) -> None:
        llm_workout = SimpleNamespace(
            exercises=[SimpleNamespace(exercise_id=1), SimpleNamespace(exercise_id=999)]
        )
        with self.assertRaises(HTTPException) as ctx:
            _validate_exercise_ids(llm_workout, {1, 2, 3})
        self.assertEqual(ctx.exception.status_code, 502)

    def test_call_groq_for_workout_returns_validated_model(self) -> None:
        user = SimpleNamespace(
            goal="hipertrofia",
            level="intermediario",
            restrictions="nenhuma",
            weight_kg=80,
            height_cm=178,
        )
        exercises = [
            SimpleNamespace(id=1, name="Supino", muscle_group="peito", equipment="barra", level="intermediario"),
            SimpleNamespace(id=2, name="Remada", muscle_group="costas", equipment="barra", level="intermediario"),
            SimpleNamespace(id=3, name="Desenvolvimento", muscle_group="ombros", equipment="haltere", level="intermediario"),
            SimpleNamespace(id=4, name="Rosca", muscle_group="biceps", equipment="haltere", level="intermediario"),
        ]
        request = WorkoutGenerateRequest(duration_minutes=50)

        with patch("app.services.llm_service._get_client", return_value=_FakeGroqClient()):
            workout = call_groq_for_workout(user, exercises, request)

        self.assertEqual(workout.workout_name, "Treino IA")
        self.assertEqual(len(workout.exercises), 4)

    def test_validate_workout_quality_rejects_duplicate_exercises(self) -> None:
        llm_workout = SimpleNamespace(
            estimated_duration_minutes=50,
            exercises=[
                SimpleNamespace(exercise_id=1, reps="10-12"),
                SimpleNamespace(exercise_id=1, reps="10-12"),
            ],
        )
        with self.assertRaises(HTTPException) as ctx:
            _validate_workout_quality(llm_workout, target_duration_minutes=50)
        self.assertEqual(ctx.exception.status_code, 502)

    def test_validate_workout_quality_rejects_invalid_reps(self) -> None:
        llm_workout = SimpleNamespace(
            estimated_duration_minutes=50,
            exercises=[SimpleNamespace(exercise_id=1, reps="dez")],
        )
        with self.assertRaises(HTTPException) as ctx:
            _validate_workout_quality(llm_workout, target_duration_minutes=50)
        self.assertEqual(ctx.exception.status_code, 502)

    def test_validate_workout_quality_rejects_duration_far_from_target(self) -> None:
        llm_workout = SimpleNamespace(
            estimated_duration_minutes=95,
            exercises=[SimpleNamespace(exercise_id=1, reps="10-12")],
        )
        with self.assertRaises(HTTPException) as ctx:
            _validate_workout_quality(llm_workout, target_duration_minutes=45)
        self.assertEqual(ctx.exception.status_code, 502)

    def test_build_user_prompt_includes_history_and_duration_rules(self) -> None:
        user = SimpleNamespace(
            goal="emagrecimento",
            level="iniciante",
            restrictions="lombar",
            weight_kg=92,
            height_cm=175,
        )
        exercises = [
            SimpleNamespace(id=1, name="Agachamento Goblet", muscle_group="pernas", equipment="haltere", level="iniciante"),
            SimpleNamespace(id=2, name="Remada Curvada", muscle_group="costas", equipment="barra", level="intermediario"),
        ]
        request = WorkoutGenerateRequest(duration_minutes=40)
        history_context = "Treinos concluídos no total: 6. Feedbacks recentes: dificil, ok."

        prompt = _build_user_prompt(user, exercises, request, history_context=history_context)

        self.assertIn("HISTÓRICO RECENTE", prompt)
        self.assertIn("diferença máxima de 15 minutos", prompt)
        self.assertIn("Não repita exercise_id", prompt)
        self.assertIn("Treinos concluídos no total: 6", prompt)

    def test_call_groq_for_workout_uses_fallback_when_llm_fails(self) -> None:
        user = SimpleNamespace(
            goal="hipertrofia",
            level="intermediario",
            restrictions="nenhuma",
            weight_kg=80,
            height_cm=178,
        )
        exercises = [
            SimpleNamespace(id=1, name="Supino", muscle_group="peito", equipment="barra", level="intermediario"),
            SimpleNamespace(id=2, name="Remada", muscle_group="costas", equipment="barra", level="intermediario"),
            SimpleNamespace(id=3, name="Desenvolvimento", muscle_group="ombros", equipment="haltere", level="intermediario"),
            SimpleNamespace(id=4, name="Rosca", muscle_group="biceps", equipment="haltere", level="intermediario"),
            SimpleNamespace(id=5, name="Tríceps Corda", muscle_group="triceps", equipment="cabo", level="intermediario"),
        ]
        request = WorkoutGenerateRequest(duration_minutes=45)

        with patch("app.services.llm_service._get_client", return_value=_AlwaysFailGroqClient()):
            with patch("app.services.llm_service.settings.llm_enable_fallback", True):
                workout = call_groq_for_workout(user, exercises, request)

        self.assertEqual(workout.workout_name, "Treino Base de Contingência")
        self.assertGreaterEqual(len(workout.exercises), 4)


if __name__ == "__main__":
    unittest.main()
