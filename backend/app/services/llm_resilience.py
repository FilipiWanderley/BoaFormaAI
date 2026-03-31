from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from time import sleep
from typing import Callable, Optional, TypeVar


T = TypeVar("T")


def execute_with_retry(
    operation: Callable[[], T],
    *,
    timeout_seconds: float,
    max_retries: int,
    backoff_seconds: float,
) -> T:
    attempts = max(1, max_retries + 1)
    last_error: Optional[Exception] = None

    for attempt in range(attempts):
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(operation)
        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError as exc:
            last_error = TimeoutError(f"Tempo limite excedido ({timeout_seconds}s).")
            future.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            if attempt < attempts - 1:
                sleep(backoff_seconds * (attempt + 1))
            continue
        except Exception as exc:
            last_error = exc
            if attempt < attempts - 1:
                sleep(backoff_seconds * (attempt + 1))
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    if last_error is None:
        raise RuntimeError("Falha inesperada na execução com retry.")
    raise last_error
