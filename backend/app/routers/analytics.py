from __future__ import annotations
from datetime import date, timedelta
from typing import Optional, Dict, List, Tuple
from collections import defaultdict
import math
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..schemas import SummaryResponse, SummaryItem, ParticipantDailyResponse, DailyPoint
from ..models import UsageDaily, Limit, Participant

router = APIRouter(prefix="/analytics/v1", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
async def summary(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    cohort: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    if cohort:
        # participantsにcohort_idがある前提でJOINして絞り込み（簡易実装）
        from sqlalchemy import select as sa_select
        from sqlalchemy import join
        j = join(UsageDaily, Participant, UsageDaily.participant_id == Participant.participant_id)
        stmt = sa_select(UsageDaily).select_from(j).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date, Participant.cohort_id == cohort)

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
        UsageDaily.usage_date >= start_date,
        UsageDaily.usage_date <= end_date,
    )
    rows = session.exec(stmt).all()
    # 日毎に合計を算出
    daily: dict[date, DailyPoint] = {}
    for r in rows:
        if r.usage_date not in daily:
            daily[r.usage_date] = DailyPoint(date=r.usage_date, total_minutes=0, pickups=0, notifications=0)
        d = daily[r.usage_date]
        d.total_minutes += r.total_minutes
        d.pickups += r.pickups
        d.notifications += r.notifications

    points = [daily[k] for k in sorted(daily.keys())]
    return ParticipantDailyResponse(participant_id=participant_id, points=points)


@router.get("/cohort-timeseries")
async def cohort_timeseries(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
):
    from sqlalchemy import select as sa_select, func
    from sqlalchemy import join
    j = join(UsageDaily, Participant, UsageDaily.participant_id == Participant.participant_id)
    stmt = sa_select(UsageDaily.usage_date, Participant.cohort_id, func.sum(UsageDaily.total_minutes)).select_from(j).where(
        UsageDaily.usage_date.between(start_date, end_date)
    ).group_by(UsageDaily.usage_date, Participant.cohort_id)
    rows = session.exec(stmt).all()
    out: Dict[str, Dict[date, int]] = defaultdict(lambda: defaultdict(int))
    for d, cohort_id, total in rows:
        out[cohort_id or "unknown"][d] = int(total)
    series = {k: [{"date": d.isoformat(), "total_minutes": v} for d, v in sorted(m.items())] for k, m in out.items()}
    return {"series": series}


# ---- KPI ----
@router.get("/kpi")
async def kpi(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    cohort: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    rows = session.exec(stmt).all()
    total_minutes = sum(r.total_minutes for r in rows)
    pickups = sum(r.pickups for r in rows)
    notifications = sum(r.notifications for r in rows)
    # カテゴリ比率
    by_cat: Dict[Optional[str], int] = defaultdict(int)
    for r in rows:
        by_cat[r.category] += r.total_minutes
    total_for_ratio = sum(by_cat.values()) or 1
    category_ratio = {str(k): v / total_for_ratio for k, v in by_cat.items()}
    # 上位アプリ（上位10件）
    by_app: Dict[str, int] = defaultdict(int)
    for r in rows:
        if r.app_bundle_id:
            by_app[r.app_bundle_id] += r.total_minutes
    top_apps = sorted(by_app.items(), key=lambda kv: kv[1], reverse=True)[:10]
    # 夜間使用（簡易推定: 利用不可ならNone）
    night_usage_minutes = None
    return {
        "total_minutes": total_minutes,
        "pickups": pickups,
        "notifications": notifications,
        "category_ratio": category_ratio,
        "top_apps": top_apps,
        "night_usage_minutes": night_usage_minutes,
    }


# ---- 時系列（移動平均） ----
@router.get("/timeseries")
async def timeseries(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    window: int = Query(7, ge=1, le=60),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    rows = session.exec(stmt).all()
    daily_totals: Dict[date, int] = defaultdict(int)
    for r in rows:
        daily_totals[r.usage_date] += r.total_minutes
    days = sorted(daily_totals.keys())
    series = [{"date": d.isoformat(), "total_minutes": daily_totals[d]} for d in days]
    # 移動平均
    vals = [daily_totals[d] for d in days]
    ma: List[Optional[float]] = []
    for i in range(len(vals)):
        if i + 1 < window:
            ma.append(None)
        else:
            win = vals[i + 1 - window : i + 1]
            ma.append(sum(win) / window)
    for i, d in enumerate(days):
        series[i]["ma"] = ma[i]
    return {"series": series, "window": window}


# ---- 曜日/学校日比較 ----
@router.get("/dow-pattern")
async def dow_pattern(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    rows = session.exec(stmt).all()
    by_dow: Dict[int, List[int]] = defaultdict(list)
    for r in rows:
        by_dow[r.usage_date.weekday()].append(r.total_minutes)
    pattern = {str(d): (sum(v) / len(v) if v else 0) for d, v in by_dow.items()}
    # 学校日(0-4) vs 休日(5-6)
    school = [m for d, vs in by_dow.items() if d < 5 for m in vs]
    holiday = [m for d, vs in by_dow.items() if d >= 5 for m in vs]
    def mean(xs: List[int]) -> float:
        return sum(xs) / len(xs) if xs else 0.0
    return {"pattern": pattern, "school_mean": mean(school), "holiday_mean": mean(holiday)}


# ---- アラート（z-score） ----
@router.get("/alerts")
async def alerts(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    z: float = Query(2.5, ge=1.0, le=10.0),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    rows = session.exec(stmt).all()
    by_pid: Dict[str, Dict[date, int]] = defaultdict(lambda: defaultdict(int))
    for r in rows:
        by_pid[r.participant_id][r.usage_date] += r.total_minutes
    alerts: List[Dict] = []
    for pid, series in by_pid.items():
        vals = list(series.values())
        if len(vals) < 5:
            continue
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5 or 1.0
        for d, v in series.items():
            zscore = (v - mu) / sd
            if zscore >= z:
                alerts.append({"participant_id": pid, "date": d.isoformat(), "value": v, "z": zscore})
    return {"alerts": sorted(alerts, key=lambda a: a["z"], reverse=True)[:200]}


# ---- 遵守（limits対比） ----
@router.get("/compliance")
async def compliance(
    start_date: date = Query(..., alias="from"),
    end_date: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
):
    stmt = select(UsageDaily).where(UsageDaily.usage_date >= start_date, UsageDaily.usage_date <= end_date)
    rows = session.exec(stmt).all()
    # ルール: rule_name == "total" を総量として解釈
    limits = {l.participant_id: l.minutes_per_day for l in session.exec(select(Limit)).all() if l.rule_name == "total"}
    by_pid: Dict[str, List[int]] = defaultdict(list)
    for r in rows:
        by_pid[r.participant_id].append(r.total_minutes)
    out = []
    for pid, vals in by_pid.items():
        total = sum(vals)
        days = len(vals)
        limit = limits.get(pid)
        if not limit:
            continue
        over_days = sum(1 for v in vals if v > limit)
        max_streak = 0
        cur = 0
        for v in vals:
            if v <= limit:
                cur += 1
                max_streak = max(max_streak, cur)
            else:
                cur = 0
        out.append({
            "participant_id": pid,
            "avg_minutes": total / days if days else 0,
            "limit": limit,
            "overrate": over_days / days if days else 0,
            "max_consecutive_compliant_days": max_streak,
        })
    return {"items": out}
