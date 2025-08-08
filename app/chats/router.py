from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session

from app.auth import get_current_user
from app.chats.dependencies import SpitchClient, get_spitch_client
from app.chats.models import Chat, DataType
from app.database import engine
from app.users.models import User

chats_router = APIRouter(prefix="/chats")


@chats_router.post("/")
async def create_chat(
    q: Optional[str] = None,
    audio_file: Optional[UploadFile] = None,
    spitch_client: SpitchClient = Depends(get_spitch_client),
    current_user: User = Depends(get_current_user),
):
    if audio_file:
        query_audio_bytes = await audio_file.read()
        query = await spitch_client.stt(query_audio_bytes)
        answer_audio_bytes = await spitch_client.tts("Answer")
        with Session(engine) as session:
            chat = Chat(
                user_id=current_user.id,
                query=query_audio_bytes,
                answer=answer_audio_bytes,
                datatype=DataType.BYTES,
            )
            session.add(chat)
            session.commit()
            session.refresh(chat)

        return {"chat": chat}

    elif q:
        with Session(engine) as session:
            chat = Chat(
                user_id=current_user.id,
                query=q.encode("utf-8"),
                answer=b"Answer",
                datatype=DataType.TEXT,
            )
            session.add(chat)
            session.commit()
            session.refresh(chat)

        return {"chat": chat}

    else:
        raise HTTPException(status_code=400, detail="No input provided")
