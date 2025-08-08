from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth import get_current_user
from app.database import engine
from app.preferences.models import (
    SetInterestsForm,
    SetNicknameForm,
    SpeechPreference,
    UpdatePreferencesForm,
    UserPreferences,
)
from app.users.models import User

preferences_router = APIRouter(prefix="/preferences")


@preferences_router.post("/nickname")
def set_nickname(form: SetNicknameForm, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(
                user_id=current_user.id,
                nickname=form.nickname,
                interests=[],
                speech_preference=SpeechPreference.NEUTRAL,
            )
        else:
            prefs.nickname = form.nickname

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Nickname updated", "preferences": prefs}


@preferences_router.post("/interests")
def set_interests(
    form: SetInterestsForm, current_user: User = Depends(get_current_user)
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(
                user_id=current_user.id,
                interests=form.interests,
                speech_preference=SpeechPreference.NEUTRAL,
            )
        else:
            prefs.interests = form.interests

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Interests updated", "preferences": prefs}


@preferences_router.get("/")
def get_preferences(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            return {"message": "No preferences set yet", "preferences": None}
        return {"preferences": prefs}


@preferences_router.put("/")
def update_preferences(
    form: UpdatePreferencesForm,
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        prefs = session.get(UserPreferences, current_user.id)
        if not prefs:
            prefs = UserPreferences(user_id=current_user.id)

        for field, value in form.model_dump(exclude_unset=True).items():
            setattr(prefs, field, value)

        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        return {"message": "Preferences updated", "preferences": prefs}
