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
        self.assertEqual(response.headers.get("x-frame-options"), "DENY")
        self.assertEqual(response.headers.get("x-content-type-options"), "nosniff")

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
        refresh_token = login_response.json().get("refresh_token")
        self.assertTrue(token)
        self.assertTrue(refresh_token)

        me_response = self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["email"], email)

    def test_refresh_and_logout_flow(self) -> None:
        email = self._unique_email()
        password = "SenhaForte@123"
        register_payload = {
            "name": "Teste Refresh",
            "email": email,
            "password": password,
            "age": 30,
            "weight_kg": 82,
            "height_cm": 178,
            "goal": "forca",
            "level": "intermediario",
            "restrictions": "nenhuma",
        }
        self.client.post("/users", json=register_payload)

        login_response = self.client.post("/auth/login", json={"email": email, "password": password})
        self.assertEqual(login_response.status_code, 200)
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]

        refresh_response = self.client.post("/auth/refresh", json={"refresh_token": refresh_token})
        self.assertEqual(refresh_response.status_code, 200)
        new_access_token = refresh_response.json()["access_token"]
        new_refresh_token = refresh_response.json()["refresh_token"]
        self.assertTrue(new_access_token)
        self.assertNotEqual(new_refresh_token, refresh_token)

        logout_response = self.client.post(
            "/auth/logout",
            json={"refresh_token": new_refresh_token},
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        self.assertEqual(logout_response.status_code, 204)

        refresh_after_logout = self.client.post("/auth/refresh", json={"refresh_token": new_refresh_token})
        self.assertEqual(refresh_after_logout.status_code, 401)

    def test_login_with_invalid_credentials(self) -> None:
        response = self.client.post(
            "/auth/login",
            json={"email": "naoexiste@boaforma.ai", "password": "senhaerrada"},
        )
        self.assertEqual(response.status_code, 401)

    def test_login_lockout_after_repeated_failures(self) -> None:
        email = self._unique_email()
        for _ in range(5):
            response = self.client.post(
                "/auth/login",
                json={"email": email, "password": "senhaerrada"},
            )
            self.assertIn(response.status_code, (401, 423))

        blocked_response = self.client.post(
            "/auth/login",
            json={"email": email, "password": "senhaerrada"},
        )
        self.assertEqual(blocked_response.status_code, 423)


if __name__ == "__main__":
    unittest.main()
