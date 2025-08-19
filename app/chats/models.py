import uuid
from datetime import datetime
from enum import StrEnum

from sqlmodel import Column, DateTime, Field, SQLModel


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
    datatype: DataType = Field(default=DataType.TEXT)


class ChatExample(SQLModel):
    casual: str
    neutral: str
    respectful: str


class ChatExamples(SQLModel):
    English: ChatExample
    Yoruba: ChatExample
    Hausa: ChatExample
    Igbo: ChatExample
