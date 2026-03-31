from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.dashboard import router as dashboard_router
from app.routers.exercises import router as exercises_router
from app.routers.history import router as history_router
from app.routers.ops import router as ops_router
from app.routers.users import router as users_router
from app.routers.workout import router as workout_router

__all__ = [
    "auth_router",
    "users_router",
    "exercises_router",
    "workout_router",
    "history_router",
    "dashboard_router",
    "chat_router",
    "ops_router",
]
