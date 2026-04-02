from collections import defaultdict
from threading import Lock
from time import time


class MetricsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._started_at = time()
        self._request_count = 0
        self._error_count = 0
        self._ai_calls = 0
        self._ai_errors = 0
        self._ai_retries = 0
        self._ai_latency_sum_ms = defaultdict(float)
        self._ai_latency_count = defaultdict(int)
        self._pwa_events = defaultdict(int)
        self._latency_sum_ms = defaultdict(float)
        self._latency_count = defaultdict(int)

    def track_request(self, *, path: str, status_code: int, latency_ms: float) -> None:
        with self._lock:
            self._request_count += 1
            if status_code >= 400:
                self._error_count += 1
            self._latency_sum_ms[path] += latency_ms
            self._latency_count[path] += 1

    def track_ai_call(
        self,
        *,
        operation: str = "general",
        latency_ms: float = 0.0,
        retries: int = 0,
        error: bool = False,
    ) -> None:
        with self._lock:
            self._ai_calls += 1
            if error:
                self._ai_errors += 1
            self._ai_retries += max(0, retries)
            if latency_ms > 0:
                self._ai_latency_sum_ms[operation] += latency_ms
                self._ai_latency_count[operation] += 1

    def track_pwa_event(self, event: str) -> None:
        with self._lock:
            self._pwa_events[event] += 1

    def snapshot(self) -> dict:
        with self._lock:
            by_endpoint = {}
            by_ai_operation = {}
            for path, count in self._latency_count.items():
                avg = self._latency_sum_ms[path] / count if count else 0.0
                by_endpoint[path] = {"count": count, "avg_latency_ms": round(avg, 2)}
            for operation, count in self._ai_latency_count.items():
                avg = self._ai_latency_sum_ms[operation] / count if count else 0.0
                by_ai_operation[operation] = {"count": count, "avg_latency_ms": round(avg, 2)}
            return {
                "uptime_seconds": int(time() - self._started_at),
                "request_count": self._request_count,
                "error_count": self._error_count,
                "ai_usage_count": self._ai_calls,
                "ai_error_count": self._ai_errors,
                "ai_retry_count": self._ai_retries,
                "ai_operations": by_ai_operation,
                "pwa_events": dict(self._pwa_events),
                "endpoints": by_endpoint,
            }


metrics_store = MetricsStore()
