from datetime import date

from fastapi import APIRouter
from sqlmodel import Session

from app.database import engine
from app.models import CreateUserForm, User

router = APIRouter()


@router.post("/users/")
def create_user(create_user_form: CreateUserForm):
    with Session(engine) as session:
        user = User(**create_user_form.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
