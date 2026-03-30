import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.workout import _LLMExercise, _LLMWorkout


class ApiWorkoutHistoryFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def _unique_email(self) -> str:
        return f"teste.workout.{time.time_ns()}@boaforma.ai"

    def _register_and_login(self) -> str:
        email = self._unique_email()
        password = "SenhaForte@123"
        register_payload = {
            "name": "Teste Fluxo",
            "email": email,
            "password": password,
            "age": 31,
            "weight_kg": 82,
            "height_cm": 179,
            "goal": "hipertrofia",
            "level": "intermediario",
            "restrictions": "nenhuma",
        }
        register_response = self.client.post("/users", json=register_payload)
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json().get("access_token")
        self.assertTrue(token)
        return token

    def _auth_headers(self, token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def _fake_llm_workout(_user, exercises, _request, history_context=None) -> _LLMWorkout:
        selected = exercises[:5]
        return _LLMWorkout(
            workout_name="Treino de Teste API",
            focus="Fluxo automatizado de teste",
            estimated_duration_minutes=50,
            exercises=[
                _LLMExercise(
                    exercise_id=exercise.id,
                    exercise_name=exercise.name,
                    sets=3,
                    reps="10-12",
                    rest_seconds=60,
                    notes=None,
                )
                for exercise in selected
            ],
            general_tips="Mantenha técnica e boa hidratação.",
        )

    def test_workout_full_flow_generate_list_get_feedback(self) -> None:
        token = self._register_and_login()
        headers = self._auth_headers(token)

        with patch(
            "app.services.workout_service.call_groq_for_workout",
            side_effect=self._fake_llm_workout,
        ):
            generate_response = self.client.post(
                "/workout/generate",
                headers=headers,
                json={"duration_minutes": 50},
            )

        self.assertEqual(generate_response.status_code, 201)
        generated = generate_response.json()
        workout_id = generated["id"]
        self.assertGreaterEqual(len(generated["exercises"]), 4)

        list_response = self.client.get("/workout/me", headers=headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(w["id"] == workout_id for w in list_response.json()))

        detail_response = self.client.get(f"/workout/{workout_id}", headers=headers)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["id"], workout_id)

        feedback_response = self.client.patch(
            f"/workout/{workout_id}/feedback",
            headers=headers,
            json={"feedback": "ok"},
        )
        self.assertEqual(feedback_response.status_code, 200)
        self.assertEqual(feedback_response.json()["feedback"], "ok")

    def test_history_complete_and_prevent_duplicate(self) -> None:
        token = self._register_and_login()
        headers = self._auth_headers(token)

        with patch(
            "app.services.workout_service.call_groq_for_workout",
            side_effect=self._fake_llm_workout,
        ):
            generate_response = self.client.post(
                "/workout/generate",
                headers=headers,
                json={"duration_minutes": 45},
            )

        self.assertEqual(generate_response.status_code, 201)
        workout_id = generate_response.json()["id"]

        first_complete = self.client.post(
            "/history",
            headers=headers,
            json={"workout_id": workout_id, "notes": "Treino concluído com sucesso"},
        )
        self.assertEqual(first_complete.status_code, 201)

        duplicate_complete = self.client.post(
            "/history",
            headers=headers,
            json={"workout_id": workout_id},
        )
        self.assertEqual(duplicate_complete.status_code, 409)

        history_response = self.client.get("/history/me", headers=headers)
        self.assertEqual(history_response.status_code, 200)
        self.assertTrue(any(item["workout_id"] == workout_id for item in history_response.json()))

    def test_protected_endpoints_require_auth(self) -> None:
        workout_response = self.client.get("/workout/me")
        history_response = self.client.get("/history/me")
        self.assertEqual(workout_response.status_code, 403)
        self.assertEqual(history_response.status_code, 403)

    def test_history_by_user_id_allows_owner_and_blocks_other_users(self) -> None:
        token = self._register_and_login()
        headers = self._auth_headers(token)

        me_response = self.client.get("/users/me", headers=headers)
        self.assertEqual(me_response.status_code, 200)
        current_user_id = me_response.json()["id"]

        own_history_response = self.client.get(f"/history/{current_user_id}", headers=headers)
        self.assertEqual(own_history_response.status_code, 200)

        other_history_response = self.client.get(f"/history/{current_user_id + 999}", headers=headers)
        self.assertEqual(other_history_response.status_code, 403)

    def test_dashboard_returns_today_workout_when_generated_today(self) -> None:
        token = self._register_and_login()
        headers = self._auth_headers(token)

        with patch(
            "app.services.workout_service.call_groq_for_workout",
            side_effect=self._fake_llm_workout,
        ):
            generate_response = self.client.post(
                "/workout/generate",
                headers=headers,
                json={"duration_minutes": 45},
            )

        self.assertEqual(generate_response.status_code, 201)
        generated_workout_id = generate_response.json()["id"]

        dashboard_response = self.client.get("/dashboard", headers=headers)
        self.assertEqual(dashboard_response.status_code, 200)
        payload = dashboard_response.json()
        self.assertIsNotNone(payload["today_workout"])
        self.assertEqual(payload["today_workout"]["id"], generated_workout_id)


if __name__ == "__main__":
    unittest.main()
