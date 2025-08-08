from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

from app.auth import get_current_user
from app.database import engine
from app.users.models import User
from app.caregivers.models import CreateCaregiverForm, Caregiver

caregivers_router = APIRouter(prefix="/caregivers")


@caregivers_router.post("/")
def create_caregiver(
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
