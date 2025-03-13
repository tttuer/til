from datetime import datetime, timedelta, UTC

from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "SECRET_KEY_IS_POWERFUL"
ALGORITHM = "HS256"


def create_access_token(
        payload: dict,
        expires_delta: timedelta = timedelta(hours=6)
):
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
