import uuid
from enum import StrEnum

from sqlmodel import Field, SQLModel


class DataType(StrEnum):
    TEXT = "text"
    BYTES = "bytes"


class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    query: bytes = Field(sa_type=bytes)
    answer: bytes = Field(sa_type=bytes)
    datatype: DataType
