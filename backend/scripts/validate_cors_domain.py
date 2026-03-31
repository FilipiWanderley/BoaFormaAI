import argparse
import json
import urllib.request


def _request(url: str, origin: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, method="GET", headers={"Origin": origin})
    with urllib.request.urlopen(req, timeout=15) as response:
        response.read()
        return response.status, dict(response.headers)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--frontend-origin", required=True)
    args = parser.parse_args()

    status, headers = _request(f"{args.api_base_url.rstrip('/')}/health", args.frontend_origin)
    allow_origin = headers.get("Access-Control-Allow-Origin", "")
    allow_credentials = headers.get("Access-Control-Allow-Credentials", "")

    result = {
        "status_code": status,
        "allow_origin": allow_origin,
        "allow_credentials": allow_credentials,
        "cors_ok": status == 200 and allow_origin == args.frontend_origin and allow_credentials.lower() == "true",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["cors_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
