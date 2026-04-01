import argparse
import concurrent.futures
import json
import random
import statistics
import string
import time
import urllib.error
import urllib.request
from typing import Optional


def _request(method: str, url: str, data: Optional[dict] = None, token: str = "") -> tuple[int, str, float]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=25) as response:
        elapsed_ms = (time.perf_counter() - started) * 1000
        return response.status, response.read().decode("utf-8"), elapsed_ms


def _random_email(prefix: str) -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}.{int(time.time() * 1000)}.{suffix}@boaforma.ai"


def _register_and_login(base_url: str) -> str:
    email = _random_email("load")
    password = "Load@12345"
    register_payload = {
        "name": "Load User",
        "email": email,
        "password": password,
        "age": 30,
        "weight_kg": 80,
        "height_cm": 178,
        "goal": "hipertrofia",
        "level": "intermediario",
        "restrictions": "nenhuma",
        "accept_terms": True,
        "privacy_policy_version": "2026-01",
    }
    _request("POST", f"{base_url.rstrip('/')}/users", data=register_payload)
    status, body, _ = _request(
        "POST",
        f"{base_url.rstrip('/')}/auth/login",
        data={"email": email, "password": password},
    )
    if status != 200:
        raise RuntimeError("Falha de login no setup de carga.")
    return json.loads(body)["access_token"]


def _exercise_user_flow(base_url: str) -> dict:
    token = _register_and_login(base_url)
    calls = []
    for method, path, payload in [
        ("POST", "/chat", {"message": "Dica rápida de treino"}),
        ("POST", "/workout/generate", {"duration_minutes": 45}),
        ("GET", "/dashboard", None),
    ]:
        url = f"{base_url.rstrip('/')}{path}"
        status, _, elapsed = _request(method, url, data=payload, token=token)
        calls.append({"path": path, "status": status, "latency_ms": elapsed})
    return {"calls": calls}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--users", type=int, default=20)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--max-p95-ms", type=float, default=3000)
    args = parser.parse_args()

    failures = 0
    latencies: list[float] = []
    by_path: dict[str, list[float]] = {}
    error_samples: dict[str, int] = {}

    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(_exercise_user_flow, args.base_url) for _ in range(args.users)]
        for future in concurrent.futures.as_completed(futures):
            try:
                flow = future.result()
                for call in flow["calls"]:
                    if call["status"] >= 400:
                        failures += 1
                    latencies.append(call["latency_ms"])
                    by_path.setdefault(call["path"], []).append(call["latency_ms"])
            except Exception:
                failures += 1
                exc = future.exception()
                if exc:
                    key = f"{type(exc).__name__}:{str(exc)}"[:120]
                else:
                    key = "UnknownError"
                error_samples[key] = error_samples.get(key, 0) + 1

    total_seconds = time.perf_counter() - started
    sorted_latencies = sorted(latencies)
    p95 = 0.0
    if sorted_latencies:
        idx = min(len(sorted_latencies) - 1, max(0, int(len(sorted_latencies) * 0.95) - 1))
        p95 = sorted_latencies[idx]

    per_endpoint = {}
    for path, values in by_path.items():
        sorted_values = sorted(values)
        ep_p95 = 0.0
        if sorted_values:
            idx = min(len(sorted_values) - 1, max(0, int(len(sorted_values) * 0.95) - 1))
            ep_p95 = sorted_values[idx]
        per_endpoint[path] = {
            "count": len(values),
            "avg_latency_ms": round(statistics.fmean(values), 2) if values else 0.0,
            "p95_latency_ms": round(ep_p95, 2),
        }

    report = {
        "users": args.users,
        "concurrency": args.concurrency,
        "total_calls": len(latencies),
        "failure_count": failures,
        "error_rate_percent": round((failures / max(1, len(latencies))) * 100, 2),
        "avg_latency_ms": round(statistics.fmean(latencies), 2) if latencies else 0.0,
        "p95_latency_ms": round(p95, 2),
        "throughput_rps": round(len(latencies) / total_seconds, 2) if total_seconds > 0 else 0.0,
        "per_endpoint": per_endpoint,
        "error_samples": error_samples,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if failures > 0 or p95 > args.max_p95_ms:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
