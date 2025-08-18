from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.database import SessionDep
from app.preferences.models import UpdatePreferenceForm, UserPreferences
from app.users.models import User

preferences_router = APIRouter(prefix="/preferences", tags=["Preferences"])


@preferences_router.post("/")
async def update_preferences(
    form: UpdatePreferenceForm,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> UserPreferences:
    prefs = session.get(UserPreferences, current_user.id)

    if not prefs:
        prefs = UserPreferences(user_id=current_user.id)

    if form.nickname is not None:
        prefs.nickname = form.nickname
    if form.language is not None:
        prefs.language = form.language
    if form.speech_preference is not None:
        prefs.speech_preference = form.speech_preference
    if form.interests is not None:
        prefs.interests = form.interests

    session.add(prefs)
    session.commit()
    session.refresh(prefs)
    return prefs


@preferences_router.get("/")
async def get_preferences(
    session: SessionDep, current_user: User = Depends(get_current_user)
) -> UserPreferences | None:
    prefs = session.get(UserPreferences, current_user.id)
    return prefs
