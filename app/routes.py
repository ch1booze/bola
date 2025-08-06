from fastapi import APIRouter
from sqlmodel import Session

from app.database import engine
from app.models import (
    Caregiver,
    CreateCaregiverForm,
    CreateUserForm,
    SetInterestsForm,
    SetNicknameForm,
    User,
    UserPreferences,
)

router = APIRouter()


@router.post("/users/")
def create_user(form: CreateUserForm):
    with Session(engine) as session:
        user = User(**form.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.post("/preferences/nickname")
def set_nickname(form: SetNicknameForm, user_id: str):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, user_id)
        prefs.nickname = form.nickname
        session.add(prefs)
        session.commit()
        return prefs


@router.post("/preferences/interests")
def set_interests(form: SetInterestsForm, user_id: str):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, user_id)
        prefs.interests = form.interests
        session.add(prefs)
        session.commit()
        return prefs


@router.post("/caregivers/", response_model=Caregiver)
def create_caregiver(form: CreateCaregiverForm):
    with Session(engine) as session:
        caregiver = Caregiver(**form.model_dump())
        session.add(caregiver)
        session.commit()
        session.refresh(caregiver)
        return caregiver


@router.get("/caregivers/{user_id}")
def list_caregivers(user_id: UUID):
    with Session(engine) as session:
        caregivers = session.exec(
            select(Caregiver).where(Caregiver.user_id == user_id)
        ).all()
        return caregivers


@router.delete("/caregivers/{caregiver_id}")
def delete_caregiver(caregiver_id: UUID):
    with Session(engine) as session:
        caregiver = session.get(Caregiver, caregiver_id)
        if not caregiver:
            raise HTTPException(status_code=404, detail="Not found")
        session.delete(caregiver)
        session.commit()
        return {"detail": "Deleted"}
