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

    def track_ai_call(self) -> None:
        with self._lock:
            self._ai_calls += 1

    def track_pwa_event(self, event: str) -> None:
        with self._lock:
            self._pwa_events[event] += 1

    def snapshot(self) -> dict:
        with self._lock:
            by_endpoint = {}
            for path, count in self._latency_count.items():
                avg = self._latency_sum_ms[path] / count if count else 0.0
                by_endpoint[path] = {"count": count, "avg_latency_ms": round(avg, 2)}
            return {
                "uptime_seconds": int(time() - self._started_at),
                "request_count": self._request_count,
                "error_count": self._error_count,
                "ai_usage_count": self._ai_calls,
                "pwa_events": dict(self._pwa_events),
                "endpoints": by_endpoint,
            }


metrics_store = MetricsStore()
