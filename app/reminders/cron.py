from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.database import engine
from app.reminders.models import Reminder


def reminder_job():
    with Session(engine) as session:
        statement = select(Reminder).where(Reminder.due_date <= datetime.now())
        reminders = session.exec(statement).all()
        for reminder in reminders:
            if reminder.recurring:
                if reminder.recurring == "daily":
                    reminder.due_date += timedelta(days=1)
                elif reminder.recurring == "weekly":
                    reminder.due_date += timedelta(weeks=1)
                elif reminder.recurring == "monthly":
                    reminder.due_date += timedelta(days=30)
                session.add(reminder)
            else:
                session.delete(reminder)

        session.commit()
