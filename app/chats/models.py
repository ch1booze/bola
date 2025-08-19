import uuid
from datetime import datetime
from enum import StrEnum
from typing import Optional

from sqlmodel import Column, DateTime, Field, LargeBinary, SQLModel


class DataType(StrEnum):
    TEXT = "text"
    AUDIO = "audio"


class ChatRequestForm(SQLModel):
    query: str


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column=Column(DateTime, nullable=False),
    )
    user_id: uuid.UUID = Field(foreign_key="user.id")
    query: str
    answer: str
    answer_audio: Optional[bytes] = Field(sa_column=Column(LargeBinary), default=None)
    datatype: DataType
