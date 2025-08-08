from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.caregivers.router import caregivers_router
from app.database import create_db_and_tables
from app.preferences.router import preferences_router
from app.reminders.router import reminders_router
from app.users.router import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(preferences_router)
app.include_router(caregivers_router)
app.include_router(reminders_router)
