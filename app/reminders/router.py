from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.database import SessionDep
from app.reminders.models import Reminder, SetReminderForm
from app.users.models import User

reminders_router = APIRouter(prefix="/reminders", tags=["Reminders"])


@reminders_router.post("/")
async def set_reminder(
    form: SetReminderForm,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    reminder = Reminder(**form.model_dump(), user_id=current_user.id)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)

    return {"message": "Reminder set"}
