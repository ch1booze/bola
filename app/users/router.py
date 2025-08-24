from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.auth import create_access_token, get_current_user
from app.database import SessionDep
from app.users.models import AuthResponse, LoginUserForm, SignupUserForm, User

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/signup")
async def signup_user(form: SignupUserForm, session: SessionDep) -> AuthResponse:
    existing_user = session.exec(
        select(User).where(User.email_or_phone == form.email_or_phone)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(**form.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = await create_access_token(str(user.id))
    return AuthResponse(access_token=access_token, user=user)


@users_router.post("/login")
async def login_user(form: LoginUserForm, session: SessionDep):
    user = session.exec(
        select(User).where(User.email_or_phone == form.email_or_phone)
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")

    access_token = await create_access_token(str(user.id))
    return AuthResponse(access_token=access_token, user=user)


@users_router.get("/me")
async def get_user_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@users_router.delete("/")
async def delete_user(
    session: SessionDep, current_user: User = Depends(get_current_user)
) -> None:
    user = session.get(User, current_user.id)
    if user:
        session.delete(user)
        session.commit()
