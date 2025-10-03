from __future__ import annotations
import random
from datetime import date, timedelta
from sqlmodel import Session, select
from app.db import engine
from app.models import UsageDaily, Participant, Limit


def seed(num_participants: int = 100, days: int = 30) -> None:
    start = date.today() - timedelta(days=days)
    with Session(engine) as session:
        # 参加者の作成（A/B コホート）+ デフォルト制限
        for i in range(num_participants):
            pid = f"P{i:04d}"
            cohort = "experiment" if i % 2 == 0 else "control"
            if not session.exec(select(Participant).where(Participant.participant_id == pid)).first():
                session.add(Participant(participant_id=pid, cohort_id=cohort))
            if not session.exec(select(Limit).where(Limit.participant_id == pid, Limit.rule_name == "total")).first():
                session.add(Limit(participant_id=pid, rule_name="total", target="overall", minutes_per_day=120))
        session.commit()

        for i in range(num_participants):
            pid = f"P{i:04d}"
            for d in range(days):
                dt = start + timedelta(days=d)
                base = random.randint(60, 180)
                jitter = random.randint(-30, 30)
                total = max(10, base + jitter)
                row = UsageDaily(
                    usage_date=dt,
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
