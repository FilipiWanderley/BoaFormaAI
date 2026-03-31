from collections import defaultdict, deque
from time import time


class LoginGuard:
    def __init__(self) -> None:
        self._failures: dict[str, deque[float]] = defaultdict(deque)
        self._blocked_until: dict[str, float] = {}

    def is_blocked(self, key: str) -> tuple[bool, int]:
        now = time()
        blocked_until = self._blocked_until.get(key, 0.0)
        if blocked_until > now:
            return True, int(max(1, blocked_until - now))
        if key in self._blocked_until:
            del self._blocked_until[key]
        return False, 0

    def register_failure(self, *, key: str, threshold: int, window_seconds: int, lockout_seconds: int) -> None:
        now = time()
        bucket = self._failures[key]
        cutoff = now - window_seconds
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        bucket.append(now)
        if len(bucket) >= threshold:
            self._blocked_until[key] = now + lockout_seconds
            bucket.clear()

    def clear(self, key: str) -> None:
        self._failures.pop(key, None)
        self._blocked_until.pop(key, None)


login_guard = LoginGuard()
