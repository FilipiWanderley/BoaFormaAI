from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    GoogleAuthRequest,
    GoogleAuthResponse,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.audit import log_event
from app.services.auth import (
    authenticate_user,
    issue_token_pair,
    revoke_refresh_token,
    rotate_refresh_token,
)
from app.services.google_auth import verify_google_credential
from app.services.login_guard import login_guard
from app.services.rate_limit import client_ip, enforce_rate_limit
from app.services.user import get_by_email

router = APIRouter(prefix="/auth", tags=["auth"])

login_rate_limit = enforce_rate_limit(
    key_prefix="auth:login",
    limit=settings.login_rate_limit,
    window_seconds=settings.login_rate_window_seconds,
)


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    body: LoginRequest,
    _: None = Depends(login_rate_limit),
    db: Session = Depends(get_db),
) -> TokenResponse:
    guard_key = f"{body.email.lower()}:{client_ip(request)}"
    blocked, retry_after = login_guard.is_blocked(guard_key)
    if blocked:
        log_event("auth_login_blocked", email=body.email.lower(), ip=client_ip(request), retry_after=retry_after)
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Conta temporariamente bloqueada por tentativas inválidas.",
            headers={"Retry-After": str(retry_after)},
        )
    user = authenticate_user(db, body.email, body.password)
    if not user:
        login_guard.register_failure(
            key=guard_key,
            threshold=settings.login_lockout_threshold,
            window_seconds=settings.login_rate_window_seconds,
            lockout_seconds=settings.login_lockout_seconds,
        )
        log_event("auth_login_failed", email=body.email.lower(), ip=client_ip(request))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    login_guard.clear(guard_key)
    access_token, refresh_token = issue_token_pair(db, user.id)
    log_event("auth_login_success", user_id=user.id, ip=client_ip(request))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)) -> TokenResponse:
    rotated = rotate_refresh_token(db, body.refresh_token)
    if not rotated:
        log_event("auth_refresh_failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )
    access_token, refresh_token = rotated
    log_event("auth_refresh_success")
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    body: LogoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    revoked = revoke_refresh_token(db, body.refresh_token, current_user.id)
    log_event("auth_logout", user_id=current_user.id, revoked=revoked)


@router.post("/google", response_model=GoogleAuthResponse)
def google_login(
    body: GoogleAuthRequest,
    db: Session = Depends(get_db),
) -> GoogleAuthResponse:
    claims = verify_google_credential(body.token)
    email = str(claims.get("email", "")).strip().lower()
    name = str(claims.get("name", "")).strip() or email.split("@")[0]
    provider_id = str(claims.get("sub", "")).strip()

    user = get_by_email(db, email)
    if user is None:
        user = User(
            name=name,
            email=email,
            hashed_password=None,
            provider="google",
            provider_id=provider_id,
            age=settings.social_default_age,
            weight_kg=settings.social_default_weight_kg,
            height_cm=settings.social_default_height_cm,
            goal=settings.social_default_goal,
            level=settings.social_default_level,
            restrictions=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        log_event("auth_google_user_created", user_id=user.id, email=email)
    else:
        if user.provider_id and user.provider_id != provider_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conta já vinculada a outro provedor Google.",
            )
        user.provider = "google" if user.provider == "email" else user.provider
        user.provider_id = provider_id
        db.commit()
        db.refresh(user)
        log_event("auth_google_user_linked", user_id=user.id, email=email)

    access_token, refresh_token = issue_token_pair(db, user.id)
    return GoogleAuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )
