from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import SessionLocal
from app.lifecycle import run_db_migrations
from app.models import ChatMessage, Exercise, History, RefreshTokenSession, User, Workout, WorkoutExercise  # noqa: F401
from app.routers import (
    admin_router,
    auth_router,
    chat_router,
    dashboard_router,
    exercises_router,
    history_router,
    ops_router,
    users_router,
    workout_router,
)
from app.services.metrics import metrics_store

app = FastAPI(
    title="Academia Boa Forma AI",
    description="Plataforma de treinos personalizados com IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=settings.cors_allowed_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.trusted_hosts_list or ["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    started_at = perf_counter()
    response = await call_next(request)
    latency_ms = (perf_counter() - started_at) * 1000
    metrics_store.track_request(
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency_ms,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:;"
    )
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(users_router)
app.include_router(exercises_router)
app.include_router(workout_router)
app.include_router(history_router)
app.include_router(dashboard_router)
app.include_router(chat_router)
app.include_router(ops_router)


@app.on_event("startup")
def startup() -> None:
    run_db_migrations()


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
def readiness() -> dict:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    finally:
        db.close()
    return {"status": "ready"}
