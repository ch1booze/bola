import pyotp
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth import create_access_token, get_current_user
from app.database import engine
from app.environment import OTP_SECRET_KEY
from app.users.models import (
    LoginUserForm,
    SignupUserForm,
    User,
    VerifyUserForm,
)

totp = pyotp.TOTP(OTP_SECRET_KEY, interval=900)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/signup")
async def signup_user(form: SignupUserForm):
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.email_or_phone == form.email_or_phone)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        otp = totp.now()
        user = User(**form.model_dump(), otp=otp, is_verified=False)
        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"OTP for {form.email_or_phone}: {otp}")
        return {"message": "User created, verify OTP sent"}


@users_router.post("/login")
async def login_user(form: LoginUserForm):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email_or_phone == form.email_or_phone)
        ).first()
        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")

        otp = totp.now()
        user.otp = otp
        session.add(user)
        session.commit()

        print(f"OTP for {form.email_or_phone}: {otp}")
        return {"message": "OTP sent to user"}


@users_router.post("/verify")
async def verify_user(form: VerifyUserForm):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email_or_phone == form.email_or_phone)
        ).first()
        if not user or user.otp != form.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user.is_verified = True
        user.otp = None
        session.add(user)
        session.commit()

        access_token = create_access_token(str(user.id))
        return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/me")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@users_router.delete("/")
async def delete_user(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        user = session.get(User, current_user.id)
        if user:
            session.delete(user)
            session.commit()
