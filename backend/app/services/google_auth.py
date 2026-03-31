import json
from time import time
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import HTTPException, status

from app.config import settings


GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
VALID_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}


def verify_google_credential(token: str) -> dict:
    if not settings.google_oauth_client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Login Google indisponível no momento.",
        )

    query = urlencode({"id_token": token})
    url = f"{GOOGLE_TOKENINFO_URL}?{query}"

    try:
        with urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token Google inválido: {exc}",
        )

    _validate_google_payload(payload)
    return payload


def _validate_google_payload(payload: dict) -> None:
    issuer = str(payload.get("iss", "")).strip()
    audience = str(payload.get("aud", "")).strip()
    subject = str(payload.get("sub", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    exp_str = str(payload.get("exp", "")).strip()

    if issuer not in VALID_ISSUERS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Issuer Google inválido.")

    if audience != settings.google_oauth_client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Client ID do Google inválido.")

    if not subject or not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Payload Google incompleto.")

    exp = _to_int(exp_str)
    if exp is None or exp <= int(time()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Google expirado.")


def _to_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None
