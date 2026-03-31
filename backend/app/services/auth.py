from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.refresh_token import RefreshTokenSession
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: Optional[str]) -> bool:
    if not hashed:
        return False
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(subject), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None


def decode_access_token(token: str) -> Optional[int]:
    payload = _decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    sub = payload.get("sub")
    return int(sub) if sub else None


def create_refresh_token(subject: int) -> tuple[str, str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    token_id = uuid4().hex
    payload = {"sub": str(subject), "exp": expire, "type": "refresh", "jti": token_id}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, token_id, expire


def decode_refresh_token(token: str) -> Optional[tuple[int, str]]:
    payload = _decode_token(token)
    if not payload or payload.get("type") != "refresh":
        return None
    sub = payload.get("sub")
    token_id = payload.get("jti")
    if not sub or not token_id:
        return None
    return int(sub), str(token_id)


def issue_token_pair(db: Session, user_id: int) -> tuple[str, str]:
    access_token = create_access_token(user_id)
    refresh_token, token_id, expires_at = create_refresh_token(user_id)
    session = RefreshTokenSession(user_id=user_id, token_id=token_id, expires_at=expires_at)
    db.add(session)
    db.commit()
    return access_token, refresh_token


def rotate_refresh_token(db: Session, refresh_token: str) -> Optional[tuple[str, str]]:
    decoded = decode_refresh_token(refresh_token)
    if not decoded:
        return None
    user_id, token_id = decoded
    token_session = (
        db.query(RefreshTokenSession)
        .filter(
            RefreshTokenSession.token_id == token_id,
            RefreshTokenSession.user_id == user_id,
        )
        .first()
    )
    if not token_session or token_session.revoked_at is not None:
        return None
    if token_session.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        return None

    token_session.revoked_at = datetime.now(timezone.utc)
    access_token, new_refresh_token = issue_token_pair(db, user_id)
    return access_token, new_refresh_token


def revoke_refresh_token(db: Session, refresh_token: str, user_id: int) -> bool:
    decoded = decode_refresh_token(refresh_token)
    if not decoded:
        return False
    token_user_id, token_id = decoded
    if token_user_id != user_id:
        return False
    token_session = (
        db.query(RefreshTokenSession)
        .filter(
            RefreshTokenSession.token_id == token_id,
            RefreshTokenSession.user_id == user_id,
            RefreshTokenSession.revoked_at.is_(None),
        )
        .first()
    )
    if not token_session:
        return False
    token_session.revoked_at = datetime.now(timezone.utc)
    db.commit()
    return True


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
