import argparse
import json
import urllib.error
import urllib.request


def request_json(url: str, token: str = "") -> tuple[int, dict]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token", default="")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    checks = [
        ("health", f"{base}/health", False),
        ("ready", f"{base}/ready", False),
        ("metrics", f"{base}/ops/metrics", False),
    ]
    if args.token:
        checks.extend(
            [
                ("me", f"{base}/users/me", True),
                ("dashboard", f"{base}/dashboard", True),
                ("workouts", f"{base}/workout/me", True),
            ]
        )

    failed = False
    for name, url, needs_token in checks:
        try:
            status, payload = request_json(url, args.token if needs_token else "")
            preview = json.dumps(payload, ensure_ascii=False)
            print(f"{name}: {status} {preview[:180]}")
            if status >= 400:
                failed = True
        except urllib.error.HTTPError as exc:
            failed = True
            print(f"{name}: {exc.code} {exc.read().decode('utf-8')[:180]}")
        except Exception as exc:
            failed = True
            print(f"{name}: error {exc}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
