from collections import defaultdict, deque
from time import time

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    def hit(self, *, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        now = time()
        bucket = self._buckets[key]
        cutoff = now - window_seconds
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= limit:
            retry_after = int(max(1, bucket[0] + window_seconds - now))
            return False, retry_after
        bucket.append(now)
        return True, 0


limiter = InMemoryRateLimiter()


def client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def enforce_rate_limit(*, key_prefix: str, limit: int, window_seconds: int):
    def dependency(request: Request) -> None:
        key = f"{key_prefix}:{client_ip(request)}"
        allowed, retry_after = limiter.hit(key=key, limit=limit, window_seconds=window_seconds)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisições excedido. Tente novamente em instantes.",
                headers={"Retry-After": str(retry_after)},
            )

    return dependency
