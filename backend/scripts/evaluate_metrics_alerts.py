import argparse
import json
from typing import Any
from urllib.request import Request, urlopen


def fetch_metrics(base_url: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/ops/metrics"
    req = Request(url, method="GET")
    with urlopen(req, timeout=12) as response:
        payload = response.read().decode("utf-8")
        return json.loads(payload)


def evaluate(
    metrics: dict[str, Any],
    *,
    max_error_rate_percent: float,
    max_avg_latency_ms: float,
    min_request_count: int,
    critical_endpoints: list[str],
) -> list[str]:
    alerts: list[str] = []
    request_count = int(metrics.get("request_count", 0))
    error_count = int(metrics.get("error_count", 0))
    endpoints = metrics.get("endpoints", {}) or {}

    if request_count < min_request_count:
        alerts.append(
            f"request_count abaixo do mínimo: atual={request_count}, mínimo={min_request_count}"
        )

    if request_count > 0:
        error_rate = (error_count / request_count) * 100
        if error_rate > max_error_rate_percent:
            alerts.append(
                f"error_rate acima do limite: atual={error_rate:.2f}%, limite={max_error_rate_percent:.2f}%"
            )

    for endpoint in critical_endpoints:
        endpoint_data = endpoints.get(endpoint)
        if not endpoint_data:
            continue
        avg_latency = float(endpoint_data.get("avg_latency_ms", 0))
        if avg_latency > max_avg_latency_ms:
            alerts.append(
                f"latência alta em {endpoint}: atual={avg_latency:.2f}ms, limite={max_avg_latency_ms:.2f}ms"
            )

    return alerts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--max-error-rate-percent", type=float, default=5.0)
    parser.add_argument("--max-avg-latency-ms", type=float, default=1200.0)
    parser.add_argument("--min-request-count", type=int, default=1)
    parser.add_argument(
        "--critical-endpoints",
        default="/auth/login,/auth/google,/workout/generate,/chat,/dashboard",
    )
    args = parser.parse_args()

    metrics = fetch_metrics(args.base_url)
    critical = [item.strip() for item in args.critical_endpoints.split(",") if item.strip()]
    alerts = evaluate(
        metrics,
        max_error_rate_percent=args.max_error_rate_percent,
        max_avg_latency_ms=args.max_avg_latency_ms,
        min_request_count=args.min_request_count,
        critical_endpoints=critical,
    )

    if not alerts:
        print("ok: métricas dentro dos limites")
        return

    print("alert:")
    for item in alerts:
        print(f"- {item}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
