from datetime import date
from enum import Enum
from typing import Optional

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Column, Field, SQLModel


class CreateUserForm(SQLModel):
    first_name: str
    last_name: str
    birthday: date
    gender: str


class User(CreateUserForm, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: Optional[str] = None


class UserInterest(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    interests: dict = Field(sa_column=Column(JSON), default_factory=list)
