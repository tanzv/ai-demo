from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from flask import current_app
from config.settings import settings

def create_access_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.get('auth.access_token_expire_minutes', 30)
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.get('auth.secret_key'),
        algorithm=settings.get('auth.algorithm')
    )
    return encoded_jwt

def create_refresh_token(subject: int) -> str:
    """Create JWT refresh token"""
    expire = datetime.utcnow() + timedelta(
        days=settings.get('auth.refresh_token_expire_days', 7)
    )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.get('auth.secret_key'),
        algorithm=settings.get('auth.algorithm')
    )
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(
            token,
            settings.get('auth.secret_key'),
            algorithms=[settings.get('auth.algorithm')]
        )
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            return None
        return int(payload["sub"])
    except JWTError:
        return None 