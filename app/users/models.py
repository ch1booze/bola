import uuid
from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel


class UserRole(StrEnum):
    USER = "user"
    CAREGIVER = "caregiver"


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class SignupUserForm(SQLModel):
    full_name: str
    birthday: date
    gender: Gender
    email_or_phone: str = Field(unique=True)
    role: UserRole


class LoginUserForm(SQLModel):
    email_or_phone: str


class User(SignupUserForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class AuthResponse(SQLModel):
    user: User
    access_token: str
