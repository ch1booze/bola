from datetime import date

from fastapi import FastAPI
from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import (
    Interest,
    LanguagePreference,
    Reminder,
    User,
    UserInterest,
    Username,
    UserReminder,
    UserRole,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/")
def create_user(full_name: str, birthday: date, gender: str, role: str):
    with Session(engine) as session:
        user_role = UserRole(role=role)
        session.add(user_role)
        session.commit()
        session.refresh(user_role)

        user = User(
            full_name=full_name, birthday=birthday, gender=gender, role_id=user_role.id
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return user


@app.post("/users/{user_id}/interests/")
def add_user_interest(user_id: int, interest_name: str):
    with Session(engine) as session:
        interest = session.exec(
            select(Interest).where(Interest.name == interest_name)
        ).first()
        if not interest:
            interest = Interest(name=interest_name)
            session.add(interest)
            session.commit()
            session.refresh(interest)

        user_interest = UserInterest(user_id=user_id, interest_id=interest.id)
        session.add(user_interest)
        session.commit()
        session.refresh(user_interest)

        return user_interest


@app.post("/users/{user_id}/username/")
def set_username(user_id: int, preferred_username: str):
    with Session(engine) as session:
        username = Username(preferred_username=preferred_username, user_id=user_id)
        session.add(username)
        session.commit()
        session.refresh(username)

        return username


@app.post("/users/{user_id}/reminders/")
def add_user_reminder(user_id: int, reminder_name: str):
    with Session(engine) as session:
        reminder = session.exec(
            select(Reminder).where(Reminder.name == reminder_name)
        ).first()
        if not reminder:
            reminder = Reminder(name=reminder_name)
            session.add(reminder)
            session.commit()
            session.refresh(reminder)

        user_reminder = UserReminder(user_id=user_id, reminder_id=reminder.id)
        session.add(user_reminder)
        session.commit()
        session.refresh(user_reminder)

        return user_reminder


@app.post("/users/{user_id}/language_preference/")
def set_language_preference(user_id: int, preference: str):
    with Session(engine) as session:
        language_preference = LanguagePreference(preference=preference, user_id=user_id)
        session.add(language_preference)
        session.commit()
        session.refresh(language_preference)

        return language_preference
