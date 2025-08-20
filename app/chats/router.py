from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import select

from app.auth import get_current_user
from app.chats.dependencies import (
    GeminiClient,
    SpitchClient,
    get_gemini_client,
    get_spitch_client,
)
from app.chats.models import Chat, ChatRequestForm, DataType, ChatExample, ChatExamples
from app.chats.prompts import generate_system_prompt
from app.database import SessionDep
from app.preferences.models import Language, UserPreferences, LANGUAGES_UNABBREVIATED
from app.users.models import User

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.post("/audio")
async def create_chat_from_audio(
    session: SessionDep,
    audio_file: UploadFile,
    spitch_client: SpitchClient = Depends(get_spitch_client),
    llm: GeminiClient = Depends(get_gemini_client),
    current_user: User = Depends(get_current_user),
) -> Chat | None:
    previous_chats = session.exec(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    ).all()
    user_preferences = session.exec(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    ).first()

    interests = []
    preferred_lang = Language.EN
    if user_preferences:
        interests = user_preferences.interests
        preferred_lang = user_preferences.language

        system_prompt = generate_system_prompt(
            interests=interests,
            previous_chats=previous_chats,
            language=LANGUAGES_UNABBREVIATED[preferred_lang],
            tone=user_preferences.speech_preference,
            name=current_user.full_name,
            nickname=user_preferences.nickname,
        )

        query_audio_bytes = await audio_file.read()
        query = await spitch_client.stt(query_audio_bytes)
        reply = await llm.generate(system_prompt=system_prompt, user_query=query)

        chat = Chat(
            user_id=current_user.id,
            query=query,
            answer=reply,
            datatype=DataType.AUDIO,
        )
        session.add(chat)
        session.commit()
        session.refresh(chat)

        return chat


@chats_router.post("/text")
async def create_chat_from_text(
    session: SessionDep,
    form: ChatRequestForm,
    llm: GeminiClient = Depends(get_gemini_client),
    current_user: User = Depends(get_current_user),
) -> Chat | None:
    previous_chats = session.exec(
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    ).all()
    user_preferences = session.exec(
        select(UserPreferences).where(UserPreferences.user_id == current_user.id)
    ).first()

    interests = []
    preferred_lang = Language.EN
    if user_preferences:
        interests = user_preferences.interests
        preferred_lang = user_preferences.language

        system_prompt = generate_system_prompt(
            interests=interests,
            previous_chats=previous_chats,
            language=LANGUAGES_UNABBREVIATED[preferred_lang],
            tone=user_preferences.speech_preference,
        )

        reply = await llm.generate(system_prompt=system_prompt, user_query=form.query)
        chat = Chat(
            user_id=current_user.id,
            query=form.query,
            answer=reply,
        )
        session.add(chat)
        session.commit()
        session.refresh(chat)

        return chat


@chats_router.get("/")
async def get_chats(
    session: SessionDep, current_user: User = Depends(get_current_user)
) -> list[Chat]:
    statement = (
        select(Chat)
        .where(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
    )
    results = session.exec(statement).all()
    return list(results)


@chats_router.get("/examples")
async def get_chat_examples() -> ChatExamples:
    return ChatExamples(
        English=ChatExample(
            casual="Hey! How are you doing today?",
            neutral="How are you today?",
            respectful="Good day. How are you feeling today?",
        ),
        Yoruba=ChatExample(
            casual="Báwo ni, ore mi? Ṣé o wa lę̀?",
            neutral="Báwo ni lónìí?",
            respectful="Ẹ káàsán sir/ma. Ṣé ara yín dáa lónìí?",
        ),
        Hausa=ChatExample(
            casual="Sannu aboki! Yaya kake yau?",
            neutral="Yaya kake yau?",
            respectful="Ina wuni ranka ya daɗe. Yaya lafiya?",
        ),
        Igbo=ChatExample(
            casual="Nwannem, kedu? Ị dị mma?",
            neutral="Kedu maka gị taa?",
            respectful="Ụtụtụ ọma sir/ma. Kedu ka ị mere?",
        ),
    )
