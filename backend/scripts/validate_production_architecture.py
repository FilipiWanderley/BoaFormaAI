import argparse
import json
import urllib.error
import urllib.request


def _request(url: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read().decode("utf-8")
        return response.status, {"body": body, "headers": dict(response.headers)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontend-url", required=True)
    parser.add_argument("--backend-url", required=True)
    args = parser.parse_args()

    checks = {
        "frontend_root": False,
        "backend_health": False,
        "backend_ready": False,
        "backend_metrics": False,
    }
    details = {}

    try:
        code, result = _request(args.frontend_url.rstrip("/"))
        checks["frontend_root"] = code == 200
        details["frontend_root"] = {"status": code}
    except Exception as exc:
        details["frontend_root"] = {"error": str(exc)}

    for key, path in [
        ("backend_health", "/health"),
        ("backend_ready", "/ready"),
        ("backend_metrics", "/ops/metrics"),
    ]:
        try:
            code, result = _request(args.backend_url.rstrip("/") + path)
            checks[key] = code == 200
            details[key] = {"status": code}
        except urllib.error.HTTPError as exc:
            details[key] = {"status": exc.code}
        except Exception as exc:
            details[key] = {"error": str(exc)}

    output = {"checks": checks, "details": details}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
