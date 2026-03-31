import argparse
import json
import urllib.error
import urllib.request


REQUIRED_SECURITY_HEADERS = [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Content-Security-Policy",
    "Strict-Transport-Security",
]


def _request(url: str, token: str = "") -> tuple[int, dict, str]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read().decode("utf-8")
        return response.status, dict(response.headers), body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token", default="")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    checks = {
        "health_status": False,
        "ready_status": False,
        "security_headers_present": False,
        "unauthorized_protected_route_blocked": False,
        "metrics_endpoint_available": False,
    }
    findings: list[str] = []

    try:
        status, headers, body = _request(f"{base}/health")
        checks["health_status"] = status == 200 and '"status": "ok"' in body.replace(" ", "")
        missing_headers = [key for key in REQUIRED_SECURITY_HEADERS if key not in headers]
        checks["security_headers_present"] = len(missing_headers) == 0
        if missing_headers:
            findings.append(f"headers ausentes: {', '.join(missing_headers)}")
    except Exception as exc:
        findings.append(f"falha em /health: {exc}")

    try:
        status, _, body = _request(f"{base}/ready")
        checks["ready_status"] = status == 200 and '"status": "ready"' in body.replace(" ", "")
    except Exception as exc:
        findings.append(f"falha em /ready: {exc}")

    try:
        status, _, _ = _request(f"{base}/ops/metrics")
        checks["metrics_endpoint_available"] = status == 200
    except Exception as exc:
        findings.append(f"falha em /ops/metrics: {exc}")

    try:
        _request(f"{base}/users/me")
    except urllib.error.HTTPError as exc:
        checks["unauthorized_protected_route_blocked"] = exc.code in (401, 403)
    except Exception as exc:
        findings.append(f"falha em validação de rota protegida: {exc}")

    result = {
        "checks": checks,
        "findings": findings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
