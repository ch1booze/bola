from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.database import engine
from app.environment import JWT_SECRET_KEY
from app.users.models import User

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24

security = HTTPBearer()


async def create_access_token(user_id: str):
    expires = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expires,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None or not user.is_verified:
            raise HTTPException(
                status_code=401, detail="User not found or not verified"
            )
        return user
