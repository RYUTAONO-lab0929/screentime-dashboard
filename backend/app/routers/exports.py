from __future__ import annotations
from fastapi import APIRouter, Depends, Response
from io import StringIO
import csv
from sqlmodel import Session, select
from ..db import get_session
from ..core.auth import require_role
from ..models import UsageDaily

router = APIRouter(prefix="/exports/v1", tags=["exports"])


@router.get("/csv")
async def export_csv(
    _: bool = Depends(require_role("researcher")),
    session: Session = Depends(get_session),
):
    rows = session.exec(select(UsageDaily)).all()
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["date", "participant_id", "category", "app_bundle_id", "total_minutes", "pickups", "notifications", "sessions_count"])
    for r in rows:
        writer.writerow([r.date, r.participant_id, r.category, r.app_bundle_id, r.total_minutes, r.pickups, r.notifications, r.sessions_count])
    return Response(content=buf.getvalue(), media_type="text/csv")
