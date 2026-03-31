from fastapi import APIRouter

from app.services.metrics import metrics_store

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/metrics")
def metrics() -> dict:
    return metrics_store.snapshot()
