import uuid

from sqlmodel import Field, SQLModel


class CreateCaregiverForm(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    first_name: str
    last_name: str
    relationship_to_user: str
    contact: str


class Caregiver(CreateCaregiverForm, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
