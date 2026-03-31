from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.services.metrics import metrics_store

router = APIRouter(prefix="/ops", tags=["ops"])


class PwaEventRequest(BaseModel):
    event: Literal["install_prompt_shown", "install_accepted", "install_dismissed", "app_installed"]


@router.get("/metrics")
def metrics() -> dict:
    return metrics_store.snapshot()


@router.post("/pwa-events", status_code=status.HTTP_204_NO_CONTENT)
def pwa_events(body: PwaEventRequest) -> None:
    metrics_store.track_pwa_event(body.event)
