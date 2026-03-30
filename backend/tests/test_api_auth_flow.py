import time
import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiAuthFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def _unique_email(self) -> str:
        return f"teste.api.{time.time_ns()}@boaforma.ai"

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_register_login_and_get_me(self) -> None:
        email = self._unique_email()
        password = "SenhaForte@123"
        register_payload = {
            "name": "Teste Integracao",
            "email": email,
            "password": password,
            "age": 29,
            "weight_kg": 79,
            "height_cm": 176,
            "goal": "hipertrofia",
            "level": "intermediario",
            "restrictions": "nenhuma",
        }

        register_response = self.client.post("/users", json=register_payload)
        self.assertEqual(register_response.status_code, 201)
        self.assertEqual(register_response.json()["email"], email)

        login_response = self.client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json().get("access_token")
        self.assertTrue(token)

        me_response = self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["email"], email)

    def test_login_with_invalid_credentials(self) -> None:
        response = self.client.post(
            "/auth/login",
            json={"email": "naoexiste@boaforma.ai", "password": "senhaerrada"},
        )
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
