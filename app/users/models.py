import uuid
from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class SignupUserForm(SQLModel):
    first_name: str
    last_name: str
    birthday: date
    gender: str
    email_or_phone: str
    otp: Optional[str] = None
    is_verified: bool = Field(default=False)


class LoginUserForm(SQLModel):
    email_or_phone: str


class VerifyUserForm(SQLModel):
    email_or_phone: str
    otp: str


class User(SignupUserForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class CreateCaregiverForm(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    first_name: str
    last_name: str
    relationship_to_user: str
    contact: str


class Caregiver(CreateCaregiverForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
