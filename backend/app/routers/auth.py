from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, LogoutRequest, RefreshTokenRequest, TokenResponse
from app.services.auth import (
    authenticate_user,
    issue_token_pair,
    revoke_refresh_token,
    rotate_refresh_token,
)
from app.services.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])

login_rate_limit = enforce_rate_limit(
    key_prefix="auth:login",
    limit=settings.login_rate_limit,
    window_seconds=settings.login_rate_window_seconds,
)


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    _: None = Depends(login_rate_limit),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    access_token, refresh_token = issue_token_pair(db, user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)) -> TokenResponse:
    rotated = rotate_refresh_token(db, body.refresh_token)
    if not rotated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )
    access_token, refresh_token = rotated
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    body: LogoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    revoke_refresh_token(db, body.refresh_token, current_user.id)
