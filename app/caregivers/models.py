import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class CreateCaregiverForm(SQLModel):
    full_name: str
    relationship_to_user: str
    contact: str


class Caregiver(CreateCaregiverForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")


class UpdateCaregiverForm(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    relationship_to_user: Optional[str] = None
    contact: Optional[str] = None
