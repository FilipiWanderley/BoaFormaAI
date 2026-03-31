import time
import unittest
from unittest.mock import patch

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
        ready_response = self.client.get("/ready")
        self.assertEqual(ready_response.status_code, 200)
        self.assertEqual(ready_response.json(), {"status": "ready"})

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
            "accept_terms": True,
            "privacy_policy_version": "2026-01",
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
            "accept_terms": True,
            "privacy_policy_version": "2026-01",
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

    def test_google_login_creates_and_links_user(self) -> None:
        unique_suffix = str(time.time_ns())
        google_claims = {
            "email": self._unique_email(),
            "name": "Google User",
            "sub": f"google-sub-{unique_suffix}",
        }
        with patch("app.routers.auth.verify_google_credential", return_value=google_claims):
            first = self.client.post("/auth/google", json={"token": "valid-token", "accept_terms": True, "privacy_policy_version": "2026-01"})
        self.assertEqual(first.status_code, 200)
        body = first.json()
        self.assertTrue(body.get("access_token"))
        self.assertTrue(body.get("refresh_token"))
        self.assertEqual(body["user"]["email"], google_claims["email"])
        self.assertEqual(body["user"]["provider"], "google")

        password = "SenhaForte@123"
        register_payload = {
            "name": "Pessoa Vinculada",
            "email": self._unique_email(),
            "password": password,
            "age": 28,
            "weight_kg": 74,
            "height_cm": 173,
            "goal": "hipertrofia",
            "level": "intermediario",
            "restrictions": "nenhuma",
            "accept_terms": True,
            "privacy_policy_version": "2026-01",
        }
        self.client.post("/users", json=register_payload)

        linked_claims = {
            "email": register_payload["email"],
            "name": register_payload["name"],
            "sub": f"google-sub-linked-{unique_suffix}",
        }
        with patch("app.routers.auth.verify_google_credential", return_value=linked_claims):
            linked = self.client.post("/auth/google", json={"token": "valid-token-2", "accept_terms": True, "privacy_policy_version": "2026-01"})
        self.assertEqual(linked.status_code, 200)
        linked_user = linked.json()["user"]
        self.assertEqual(linked_user["email"], register_payload["email"])
        self.assertEqual(linked_user["provider"], "google")

    def test_delete_account_removes_user_access(self) -> None:
        email = self._unique_email()
        password = "SenhaForte@123"
        register_payload = {
            "name": "Teste Excluir Conta",
            "email": email,
            "password": password,
            "age": 29,
            "weight_kg": 79,
            "height_cm": 176,
            "goal": "saude",
            "level": "iniciante",
            "restrictions": "nenhuma",
            "accept_terms": True,
            "privacy_policy_version": "2026-01",
        }
        self.client.post("/users", json=register_payload)

        login_response = self.client.post("/auth/login", json={"email": email, "password": password})
        token = login_response.json()["access_token"]
        delete_response = self.client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(delete_response.status_code, 204)

        login_after_delete = self.client.post("/auth/login", json={"email": email, "password": password})
        self.assertEqual(login_after_delete.status_code, 401)


if __name__ == "__main__":
    unittest.main()
