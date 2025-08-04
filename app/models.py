from datetime import date
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    USER = "User"
    CAREGIVER = "Caregiver"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    birthday: date
    gender: Optional[str] = None
    role: UserRole


class Interest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class UserInterest(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    interest_id: Optional[int] = Field(
        default=None, foreign_key="interest.id", primary_key=True
    )


class Username(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preferred_username: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_active: bool = False


class UserReminder(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    reminder_id: Optional[int] = Field(
        default=None, foreign_key="reminder.id", primary_key=True
    )


class LanguagePreference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preference: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
