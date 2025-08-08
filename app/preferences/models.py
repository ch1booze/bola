import uuid
from enum import StrEnum
from typing import Optional

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Column, Field, SQLModel


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
