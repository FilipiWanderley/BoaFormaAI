import unittest

from fastapi import HTTPException

from app.schemas.workout import _LLMWorkout
from app.services.ai.response_evaluator import validate_workout_response


def _build_payload(**overrides):
    base = {
        "workout_name": "Treino A",
        "focus": "Peito e tríceps",
        "estimated_duration_minutes": 45,
        "exercises": [
            {
                "exercise_id": 1,
                "exercise_name": "Supino",
                "sets": 4,
                "reps": "8-12",
                "rest_seconds": 90,
                "notes": None,
            },
            {
                "exercise_id": 2,
                "exercise_name": "Crucifixo",
                "sets": 3,
                "reps": "10-12",
                "rest_seconds": 60,
                "notes": None,
            },
            {
                "exercise_id": 3,
                "exercise_name": "Tríceps",
                "sets": 3,
                "reps": "12",
                "rest_seconds": 60,
                "notes": None,
            },
            {
                "exercise_id": 4,
                "exercise_name": "Flexão",
                "sets": 3,
                "reps": "10-12",
                "rest_seconds": 60,
                "notes": None,
            },
            {
                "exercise_id": 5,
                "exercise_name": "Mergulho",
                "sets": 3,
                "reps": "8-10",
                "rest_seconds": 75,
                "notes": None,
            },
        ],
        "general_tips": "Aqueça bem.",
    }
    base.update(overrides)
    return base


class ResponseEvaluatorTests(unittest.TestCase):
    def test_accepts_valid_response(self) -> None:
        workout = _LLMWorkout.model_validate(_build_payload())
        validate_workout_response(llm_workout=workout, valid_exercise_ids={1, 2, 3, 4, 5}, target_duration_minutes=45)

    def test_rejects_invalid_exercise_id(self) -> None:
        workout = _LLMWorkout.model_validate(_build_payload(exercises=[{**_build_payload()["exercises"][0], "exercise_id": 999}] + _build_payload()["exercises"][1:]))
        with self.assertRaises(HTTPException):
            validate_workout_response(llm_workout=workout, valid_exercise_ids={1, 2, 3, 4, 5}, target_duration_minutes=45)

    def test_rejects_duration_far_from_target(self) -> None:
        workout = _LLMWorkout.model_validate(_build_payload(estimated_duration_minutes=90))
        with self.assertRaises(HTTPException):
            validate_workout_response(llm_workout=workout, valid_exercise_ids={1, 2, 3, 4, 5}, target_duration_minutes=45)


if __name__ == "__main__":
    unittest.main()
