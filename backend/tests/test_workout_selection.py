import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.schemas.workout import WorkoutGenerateRequest
from app.services import workout_service


class WorkoutSelectionTests(unittest.TestCase):
    def test_select_exercises_falls_back_to_compatible_when_filters_empty_result(self) -> None:
        compatible = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        further_filtered = [SimpleNamespace(id=99)]
        request = WorkoutGenerateRequest(
            muscle_groups=["peito"],
            equipment_available=["kettlebell"],
            duration_minutes=45,
        )

        with patch("app.services.workout_service.get_compatible_exercises", return_value=compatible), patch(
            "app.services.workout_service.filter_exercises", return_value=further_filtered
        ):
            selected = workout_service._select_exercises(db=None, user=SimpleNamespace(level="iniciante"), request=request)

        self.assertEqual([item.id for item in selected], [1, 2])

    def test_select_exercises_keeps_filtered_when_intersection_exists(self) -> None:
        compatible = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
        further_filtered = [SimpleNamespace(id=2), SimpleNamespace(id=3)]
        request = WorkoutGenerateRequest(
            muscle_groups=["costas"],
            equipment_available=["barra"],
            duration_minutes=45,
        )

        with patch("app.services.workout_service.get_compatible_exercises", return_value=compatible), patch(
            "app.services.workout_service.filter_exercises", return_value=further_filtered
        ):
            selected = workout_service._select_exercises(db=None, user=SimpleNamespace(level="iniciante"), request=request)

        self.assertEqual([item.id for item in selected], [2])


if __name__ == "__main__":
    unittest.main()
