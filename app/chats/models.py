import uuid
from datetime import datetime
from enum import StrEnum

from sqlmodel import Column, DateTime, Field, LargeBinary, SQLModel


class DataType(StrEnum):
    TEXT = "text"
    BYTES = "bytes"


class ChatRequestForm(SQLModel):
    query: str


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime, nullable=False),
    )
    user_id: uuid.UUID = Field(foreign_key="user.id")
    query: bytes = Field(sa_column=Column(LargeBinary))
    answer: bytes = Field(sa_column=Column(LargeBinary))
    datatype: DataType
