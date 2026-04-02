import json
import re
from typing import Any


_RE_JSON_FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_RE_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def extract_json_block(raw_text: str) -> str:
    match = _RE_JSON_FENCE.search(raw_text)
    if match:
        return match.group(1)
    match = _RE_JSON_OBJECT.search(raw_text)
    if match:
        return match.group(0)
    return raw_text


def parse_json_response(raw_text: str) -> Any:
    return json.loads(extract_json_block(raw_text))
