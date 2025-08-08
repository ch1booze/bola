from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth import get_current_user
from app.caregivers.models import Caregiver, CreateCaregiverForm, UpdateCaregiverForm
from app.database import engine
from app.users.models import User

caregivers_router = APIRouter(prefix="/caregivers", tags=["Caregivers"])


@caregivers_router.post("/")
async def create_caregiver(
    form: CreateCaregiverForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        user = session.get(User, form.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        caregiver = Caregiver(**form.model_dump())
        session.add(caregiver)
        session.commit()
        session.refresh(caregiver)
        return {"message": "Caregiver added", "caregiver": caregiver}


from sqlmodel import select


@caregivers_router.get("/")
async def get_user_caregivers(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        caregivers = session.exec(
            select(Caregiver).where(Caregiver.user_id == current_user.id)
        ).all()
        return {"caregivers": caregivers}


@caregivers_router.put("/{caregiver_id}")
async def update_caregiver(
    caregiver_id: str,
    form: UpdateCaregiverForm,
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        caregiver = session.get(Caregiver, caregiver_id)
        if not caregiver or caregiver.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Caregiver not found")

        for field, value in form.model_dump(exclude_unset=True).items():
            setattr(caregiver, field, value)

        session.add(caregiver)
        session.commit()
        session.refresh(caregiver)
        return {"message": "Caregiver updated", "caregiver": caregiver}


@caregivers_router.delete("/{caregiver_id}")
async def delete_caregiver(
    caregiver_id: str, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        caregiver = session.get(Caregiver, caregiver_id)
        if not caregiver or caregiver.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Caregiver not found")

        session.delete(caregiver)
        session.commit()
        return {"message": "Caregiver deleted"}
