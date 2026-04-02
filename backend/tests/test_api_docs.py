import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_swagger_docs_endpoint_is_available(self) -> None:
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Swagger UI", response.text)

    def test_openapi_contains_main_routes(self) -> None:
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        paths = response.json().get("paths", {})
        for route in [
            "/auth/login",
            "/auth/refresh",
            "/auth/google",
            "/admin/exercises",
            "/users",
            "/dashboard",
            "/workout/generate",
            "/history/me",
            "/chat",
            "/exercises/compatible",
            "/ops/metrics",
            "/ops/alerts",
            "/ops/pwa-events",
        ]:
            self.assertIn(route, paths)

    def test_metrics_endpoint_returns_observability_payload(self) -> None:
        response = self.client.get("/ops/metrics")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("uptime_seconds", payload)
        self.assertIn("request_count", payload)
        self.assertIn("error_count", payload)
        self.assertIn("ai_usage_count", payload)
        self.assertIn("ai_alerts", payload)
        self.assertIn("pwa_events", payload)
        self.assertIn("endpoints", payload)

    def test_alerts_endpoint_returns_alert_payload(self) -> None:
        response = self.client.get("/ops/alerts")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("generated_at", payload)
        self.assertIn("alerts", payload)
        self.assertIn("has_alerts", payload)

    def test_pwa_events_are_tracked(self) -> None:
        event_response = self.client.post("/ops/pwa-events", json={"event": "install_prompt_shown"})
        self.assertEqual(event_response.status_code, 204)
        metrics_response = self.client.get("/ops/metrics")
        self.assertEqual(metrics_response.status_code, 200)
        payload = metrics_response.json()
        self.assertGreaterEqual(payload.get("pwa_events", {}).get("install_prompt_shown", 0), 1)


if __name__ == "__main__":
    unittest.main()
