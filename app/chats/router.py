from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import select

from app.auth import get_current_user
from app.chats.dependencies import (
    GroqClient,
    SpitchClient,
    get_groq_client,
    get_spitch_client,
)
from app.chats.models import Chat, ChatRequestForm, DataType
from app.chats.prompts import generate_system_prompt
from app.database import SessionDep
from app.preferences.models import UserPreferences
from app.users.models import User

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.post("/audio")
async def create_chat_from_audio(
    session: SessionDep,
    audio_file: UploadFile,
    spitch_client: SpitchClient = Depends(get_spitch_client),
    groq_client: GroqClient = Depends(get_groq_client),
    current_user: User = Depends(get_current_user),
):
    languages = {"en": "English", "yo": "Yoruba", "ha": "Hausa", "ig": "Igbo"}
    previous_chats = session.exec(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    ).all()
    user_preferences = session.exec(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    ).first()

    interests = []
    preferred_lang = "en"
    if user_preferences:
        interests = user_preferences.interests
        preferred_lang = user_preferences.language

    system_prompt = generate_system_prompt(
        interests=interests,
        previous_chats=previous_chats,
        language=languages[preferred_lang],
    )

    query_audio_bytes = await audio_file.read()
    query = await spitch_client.stt(query_audio_bytes)
    reply = await groq_client.generate(system_prompt=system_prompt, user_query=query)
    answer_audio_bytes = await spitch_client.tts(reply)

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


@chats_router.post("/text")
async def create_chat_from_text(
    session: SessionDep,
    form: ChatRequestForm,
    groq_client: GroqClient = Depends(get_groq_client),
    current_user: User = Depends(get_current_user),
):
    languages = {"en": "English", "yo": "Yoruba", "ha": "Hausa", "ig": "Igbo"}
    previous_chats = session.exec(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    ).all()
    user_preferences = session.exec(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    ).first()

    interests = []
    preferred_lang = "en"
    if user_preferences:
        interests = user_preferences.interests
        preferred_lang = user_preferences.language

    system_prompt = generate_system_prompt(
        interests=interests,
        previous_chats=previous_chats,
        language=languages[preferred_lang],
    )

    reply = await groq_client.generate(
        system_prompt=system_prompt, user_query=form.query
    )
    chat = Chat(
        user_id=current_user.id,
        query=form.query.encode("utf-8"),
        answer=reply.encode("utf-8"),
        datatype=DataType.TEXT,
    )
    session.add(chat)
    session.commit()
    session.refresh(chat)

    return {"chat": chat}


@chats_router.get("/")
async def get_chats(
    session: SessionDep, current_user: User = Depends(get_current_user)
):
    statement = (
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    )
    results = session.exec(statement).all()
    return results
