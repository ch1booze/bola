from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from app.caregivers.router import caregivers_router
from app.chats.router import chats_router
from app.database import create_db_and_tables
from app.preferences.router import preferences_router
from app.reminders.cron import reminder_job
from app.reminders.router import reminders_router
from app.users.router import users_router

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    scheduler.add_job(
        reminder_job,
        trigger=CronTrigger(second=0),
    )
    scheduler.start()
    print("Scheduler started ✅")
    app.state.scheduler = scheduler
    yield
    scheduler.shutdown()
    print("Scheduler stopped 🛑")


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(preferences_router)
app.include_router(caregivers_router)
app.include_router(reminders_router)
app.include_router(chats_router)
