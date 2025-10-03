from __future__ import annotations
from fastapi import APIRouter, Depends, Response
from io import StringIO
import csv
from sqlmodel import Session, select
from ..db import get_session
from ..core.auth import require_role
from ..models import UsageDaily
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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
        writer.writerow([getattr(r, "usage_date", None) or getattr(r, "date", None), r.participant_id, r.category, r.app_bundle_id, r.total_minutes, r.pickups, r.notifications, r.sessions_count])
    return Response(content=buf.getvalue(), media_type="text/csv")


@router.get("/pdf")
async def export_pdf(
    _: bool = Depends(require_role("researcher")),
    session: Session = Depends(get_session),
):
    rows = session.exec(select(UsageDaily)).all()
    total_minutes = sum(r.total_minutes for r in rows)
    pickups = sum(r.pickups for r in rows)
    notifications = sum(r.notifications for r in rows)
    # 簡易PDF
    from io import BytesIO
    bio = BytesIO()
    c = canvas.Canvas(bio, pagesize=A4)
    text = c.beginText(40, 800)
    text.textLine("Screentime Report (Sample)")
    text.textLine("")
    text.textLine(f"Total Minutes: {total_minutes}")
    text.textLine(f"Pickups: {pickups}")
    text.textLine(f"Notifications: {notifications}")
    c.drawText(text)
    c.showPage()
    c.save()
    return Response(content=bio.getvalue(), media_type="application/pdf")
