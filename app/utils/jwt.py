from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings


def creer_token(data: dict) -> str:
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decoder_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
