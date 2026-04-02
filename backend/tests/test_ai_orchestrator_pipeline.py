import unittest
from types import SimpleNamespace

from app.schemas.workout import WorkoutGenerateRequest
from app.services.ai_orchestrator import generate_workout_plan


class _FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = _FakeMessage(content)


class _FakeCompletion:
    def __init__(self, content: str) -> None:
        self.choices = [_FakeChoice(content)]


class _PipelineCompletions:
    def __init__(self) -> None:
        self._calls = 0

    def create(self, **_kwargs):
        self._calls += 1
        if self._calls == 1:
            return _FakeCompletion('{"exercise_ids":[1,2,3,4,5,6]}')
        return _FakeCompletion(
            '{"workout_name":"Treino Multi-step","focus":"Teste pipeline",'
            '"estimated_duration_minutes":45,'
            '"exercises":['
            '{"exercise_id":1,"exercise_name":"Supino","sets":3,"reps":"8-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":2,"exercise_name":"Remada","sets":3,"reps":"8-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":3,"exercise_name":"Agachamento","sets":3,"reps":"8-12","rest_seconds":90,"notes":null},'
            '{"exercise_id":4,"exercise_name":"Desenvolvimento","sets":3,"reps":"8-12","rest_seconds":60,"notes":null},'
            '{"exercise_id":5,"exercise_name":"Rosca","sets":3,"reps":"10-12","rest_seconds":45,"notes":null},'
            '{"exercise_id":6,"exercise_name":"Tríceps","sets":3,"reps":"10-12","rest_seconds":45,"notes":null}'
            '],'
            '"general_tips":"Controle execução."}'
        )


class _FakeGroqClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=_PipelineCompletions())


class AIOrchestratorPipelineTests(unittest.TestCase):
    def test_generate_workout_plan_runs_multistep_pipeline(self) -> None:
        user = SimpleNamespace(
            goal="hipertrofia",
            level="intermediario",
            restrictions="nenhuma",
            weight_kg=82,
            height_cm=178,
        )
        exercises = [
            SimpleNamespace(id=1, name="Supino", muscle_group="peito", equipment="barra", level="intermediario"),
            SimpleNamespace(id=2, name="Remada", muscle_group="costas", equipment="barra", level="intermediario"),
            SimpleNamespace(id=3, name="Agachamento", muscle_group="quadriceps", equipment="barra", level="intermediario"),
            SimpleNamespace(id=4, name="Desenvolvimento", muscle_group="ombros", equipment="halteres", level="intermediario"),
            SimpleNamespace(id=5, name="Rosca", muscle_group="biceps", equipment="halteres", level="intermediario"),
            SimpleNamespace(id=6, name="Tríceps", muscle_group="triceps", equipment="cabo", level="intermediario"),
            SimpleNamespace(id=7, name="Panturrilha", muscle_group="panturrilha", equipment="maquina", level="intermediario"),
        ]
        request = WorkoutGenerateRequest(duration_minutes=45)

        workout = generate_workout_plan(
            db=None,
            user=user,
            exercises=exercises,
            request=request,
            history_context="Sem histórico.",
            client=_FakeGroqClient(),
        )

        self.assertEqual(workout.workout_name, "Treino Multi-step")
        returned_ids = [item.exercise_id for item in workout.exercises]
        self.assertEqual(returned_ids, [1, 2, 3, 4, 5, 6])


if __name__ == "__main__":
    unittest.main()
