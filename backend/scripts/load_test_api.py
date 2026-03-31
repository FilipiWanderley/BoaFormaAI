import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.error
import urllib.request


def _request(url: str, token: str = "") -> tuple[int, float]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=20) as response:
        elapsed_ms = (time.perf_counter() - started) * 1000
        response.read()
        return response.status, elapsed_ms


def run_load(
    *,
    base_url: str,
    token: str,
    endpoint: str,
    requests_total: int,
    concurrency: int,
) -> dict:
    url = f"{base_url.rstrip('/')}{endpoint}"
    durations: list[float] = []
    failures = 0

    def _single_call() -> tuple[bool, float]:
        try:
            status, elapsed = _request(url, token=token)
            if status >= 400:
                return False, elapsed
            return True, elapsed
        except urllib.error.HTTPError:
            return False, 0.0
        except Exception:
            return False, 0.0

    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(_single_call) for _ in range(requests_total)]
        for future in concurrent.futures.as_completed(futures):
            ok, elapsed = future.result()
            if not ok:
                failures += 1
                continue
            durations.append(elapsed)
    total_seconds = time.perf_counter() - started

    p95 = 0.0
    if durations:
        sorted_durations = sorted(durations)
        idx = min(len(sorted_durations) - 1, max(0, int(len(sorted_durations) * 0.95) - 1))
        p95 = sorted_durations[idx]

    return {
        "endpoint": endpoint,
        "requests_total": requests_total,
        "success_count": len(durations),
        "failure_count": failures,
        "error_rate_percent": round((failures / requests_total) * 100, 2),
        "avg_latency_ms": round(statistics.fmean(durations), 2) if durations else 0.0,
        "p95_latency_ms": round(p95, 2),
        "throughput_rps": round(requests_total / total_seconds, 2) if total_seconds > 0 else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token", default="")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument(
        "--endpoints",
        default="/health,/ready,/ops/metrics",
    )
    args = parser.parse_args()

    endpoints = [item.strip() for item in args.endpoints.split(",") if item.strip()]
    report = []
    has_failure = False
    for endpoint in endpoints:
        result = run_load(
            base_url=args.base_url,
            token=args.token,
            endpoint=endpoint,
            requests_total=args.requests,
            concurrency=args.concurrency,
        )
        report.append(result)
        if result["failure_count"] > 0:
            has_failure = True

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if has_failure:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
