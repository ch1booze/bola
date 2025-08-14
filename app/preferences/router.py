from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth import get_current_user
from app.database import engine
from app.preferences.models import (
    SetInterestsForm,
    SetLanguageForm,
    SetNicknameForm,
    SetSpeechPreferenceForm,
    UserPreferences,
)
from app.users.models import User

preferences_router = APIRouter(prefix="/preferences", tags=["Preferences"])


@preferences_router.post("/nickname")
async def set_nickname(
    form: SetNicknameForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(user_id=current_user.id, nickname=form.nickname)
        else:
            prefs.nickname = form.nickname

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Nickname updated", "preferences": prefs}


@preferences_router.post("/language")
async def set_language(
    form: SetLanguageForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(user_id=current_user.id, language=form.language)
        else:
            prefs.language = form.language

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Nickname updated", "preferences": prefs}


@preferences_router.post("/speech")
async def set_speech_preference(
    form: SetSpeechPreferenceForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(
                user_id=current_user.id, speech_preference=form.speech_preference
            )
        else:
            prefs.speech_preference = form.speech_preference

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Nickname updated", "preferences": prefs}


@preferences_router.post("/interests")
async def set_interests(
    form: SetInterestsForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(
                user_id=current_user.id,
                interests=form.interests,
            )
        else:
            prefs.interests = form.interests

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Interests updated", "preferences": prefs}


@preferences_router.get("/")
async def get_preferences(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            return {"message": "No preferences set yet", "preferences": None}
        return {"preferences": prefs}
