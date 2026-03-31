import json
import logging
from datetime import datetime, timezone
from typing import Any


logger = logging.getLogger("audit")


def log_event(event: str, **data: Any) -> None:
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **data,
    }
    logger.info(json.dumps(payload, ensure_ascii=False))
