from __future__ import annotations
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..schemas import SummaryResponse, SummaryItem, ParticipantDailyResponse, DailyPoint
from ..models import UsageDaily

router = APIRouter(prefix="/analytics/v1", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
async def summary(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    cohort: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.date >= start_date, UsageDaily.date <= end_date)
    if cohort:
        stmt = stmt.where(UsageDaily.category == cohort)  # NOTE: 実際はparticipantsとJOINしてcohortで絞る

    rows = session.exec(stmt).all()

    # サンプル集計（カテゴリ毎の合計）
    bucket: dict[Optional[str], SummaryItem] = {}
    for r in rows:
        key = r.category
        if key not in bucket:
            bucket[key] = SummaryItem(category=key, total_minutes=0, pickups=0, notifications=0)
        b = bucket[key]
        b.total_minutes += r.total_minutes
        b.pickups += r.pickups
        b.notifications += r.notifications

    return SummaryResponse(
        start_date=start_date,
        end_date=end_date,
        cohort=cohort,
        items=list(bucket.values()),
    )


@router.get("/participant/{participant_id}/daily", response_model=ParticipantDailyResponse)
async def participant_daily(
    participant_id: str,
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(
        UsageDaily.participant_id == participant_id,
        UsageDaily.date >= start_date,
        UsageDaily.date <= end_date,
    )
    rows = session.exec(stmt).all()
    # 日毎に合計を算出
    daily: dict[date, DailyPoint] = {}
    for r in rows:
        if r.date not in daily:
            daily[r.date] = DailyPoint(date=r.date, total_minutes=0, pickups=0, notifications=0)
        d = daily[r.date]
        d.total_minutes += r.total_minutes
        d.pickups += r.pickups
        d.notifications += r.notifications

    points = [daily[k] for k in sorted(daily.keys())]
    return ParticipantDailyResponse(participant_id=participant_id, points=points)
