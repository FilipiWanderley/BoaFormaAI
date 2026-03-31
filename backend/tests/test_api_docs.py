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
            "/users",
            "/dashboard",
            "/workout/generate",
            "/history/me",
            "/chat",
            "/exercises/compatible",
        ]:
            self.assertIn(route, paths)


if __name__ == "__main__":
    unittest.main()
