import uuid
from datetime import date
from enum import StrEnum
from typing import Optional

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Column, Field, SQLModel


class CreateUserForm(SQLModel):
    first_name: str
    last_name: str
    birthday: date
    gender: str


class User(CreateUserForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class SpeechPreference(StrEnum):
    CASUAL = "casual"
    NEUTRAL = "neutral"
    RESPECTFUL = "respectful"


class SetNicknameForm(SQLModel):
    nickname: str


class SetInterestsForm(SQLModel):
    interests: list[str]


class UserPreferences(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    nickname: Optional[str] = None
    interests: dict = Field(sa_column=Column(JSON), default_factory=list)
    speech_preference: SpeechPreference


class CreateCaregiverForm(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    first_name: str
    last_name: str
    relationship_to_user: str
    contact: str


class Caregiver(CreateCaregiverForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
