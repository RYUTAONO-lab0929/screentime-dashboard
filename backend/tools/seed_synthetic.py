from __future__ import annotations
import random
from datetime import date, timedelta
from sqlmodel import Session
from app.db import engine
from app.models import UsageDaily


def seed(num_participants: int = 100, days: int = 30) -> None:
    start = date.today() - timedelta(days=days)
    with Session(engine) as session:
        for i in range(num_participants):
            pid = f"P{i:04d}"
            for d in range(days):
                dt = start + timedelta(days=d)
                base = random.randint(60, 180)
                jitter = random.randint(-30, 30)
                total = max(10, base + jitter)
                row = UsageDaily(
                    date=dt,
                    participant_id=pid,
                    category=random.choice(["education", "social", "entertainment", None]),
                    app_bundle_id=None,
                    total_minutes=total,
                    pickups=random.randint(20, 80),
                    notifications=random.randint(10, 100),
                    sessions_count=random.randint(5, 25),
                )
                session.add(row)
        session.commit()


if __name__ == "__main__":
    seed()
