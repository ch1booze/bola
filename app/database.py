from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.caregivers.models import Caregiver
from app.chats.models import Chat
from app.environment import DATABASE_URL
from app.preferences.models import UserPreferences
from app.reminders.models import Reminder
from app.users.models import User

engine = create_engine(DATABASE_URL, echo=True)
_ = [Caregiver, Chat, UserPreferences, Reminder, User]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
