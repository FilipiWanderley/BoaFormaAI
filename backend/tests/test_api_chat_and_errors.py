import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class _FakeChatMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _FakeChatChoice:
    def __init__(self, content: str) -> None:
        self.message = _FakeChatMessage(content)


class _FakeChatCompletion:
    def __init__(self, content: str) -> None:
        self.choices = [_FakeChatChoice(content)]


class _FakeCompletions:
    def create(self, **_kwargs) -> _FakeChatCompletion:
        return _FakeChatCompletion("Resposta de teste do assistente.")


class _FakeChat:
    def __init__(self) -> None:
        self.completions = _FakeCompletions()


class _FakeGroqClient:
    def __init__(self) -> None:
        self.chat = _FakeChat()


class ApiChatAndErrorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def _unique_email(self) -> str:
        return f"teste.chat.{time.time_ns()}@boaforma.ai"

    def _register_and_login(self) -> str:
        email = self._unique_email()
        password = "SenhaForte@123"
        register_payload = {
            "name": "Teste Chat",
            "email": email,
            "password": password,
            "age": 27,
            "weight_kg": 75,
            "height_cm": 173,
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

    def test_chat_flow_send_list_clear(self) -> None:
        token = self._register_and_login()
        headers = self._auth_headers(token)

        with patch("app.services.chat_service._get_client", return_value=_FakeGroqClient()):
            send_response = self.client.post(
                "/chat",
                headers=headers,
                json={"message": "Como melhorar meu treino de peito?"},
            )

        self.assertEqual(send_response.status_code, 200)
        body = send_response.json()
        self.assertEqual(body["reply"]["role"], "assistant")
        self.assertGreaterEqual(len(body["history"]), 2)

        history_response = self.client.get("/chat/history", headers=headers)
        self.assertEqual(history_response.status_code, 200)
        self.assertGreaterEqual(len(history_response.json()), 2)

        clear_response = self.client.delete("/chat/history", headers=headers)
        self.assertEqual(clear_response.status_code, 204)

        history_after_clear = self.client.get("/chat/history", headers=headers)
        self.assertEqual(history_after_clear.status_code, 200)
        self.assertEqual(history_after_clear.json(), [])

    def test_error_scenarios_403_404_422(self) -> None:
        unauthorized_chat = self.client.get("/chat/history")
        self.assertEqual(unauthorized_chat.status_code, 403)

        token = self._register_and_login()
        headers = self._auth_headers(token)

        not_found_workout = self.client.get("/workout/999999", headers=headers)
        self.assertEqual(not_found_workout.status_code, 404)

        invalid_generate = self.client.post(
            "/workout/generate",
            headers=headers,
            json={"duration_minutes": 10},
        )
        self.assertEqual(invalid_generate.status_code, 422)


if __name__ == "__main__":
    unittest.main()
