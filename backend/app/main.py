from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.lifecycle import run_db_migrations
from app.models import ChatMessage, Exercise, History, User, Workout, WorkoutExercise  # noqa: F401
from app.routers import (
    auth_router,
    chat_router,
    dashboard_router,
    exercises_router,
    history_router,
    users_router,
    workout_router,
)

app = FastAPI(
    title="Academia Boa Forma AI",
    description="Plataforma de treinos personalizados com IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(exercises_router)
app.include_router(workout_router)
app.include_router(history_router)
app.include_router(dashboard_router)
app.include_router(chat_router)


@app.on_event("startup")
def startup() -> None:
    run_db_migrations()


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
