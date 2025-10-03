from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete
from ..db import get_session
from ..core.auth import require_role
from ..models import Participant, Device, RawEvent, UsageDaily, WebDomainDaily, Limit, AnonymizationKey

router = APIRouter(prefix="/privacy/v1", tags=["privacy"])


@router.delete("/participant/{participant_id}", status_code=202)
async def delete_participant(
    participant_id: str,
    _: bool = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    # 研究倫理: 忘れられる権利に準拠した削除処理（ソフト/ハードは運用方針に合わせる）
    exists = session.exec(select(Participant).where(Participant.participant_id == participant_id)).first()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found")

    # 論理削除方針に合わせて切替可能。ここではハードデリート例。
    for model in [Device, RawEvent, UsageDaily, WebDomainDaily, Limit]:
        session.exec(delete(model).where(model.participant_id == participant_id) if hasattr(model, "participant_id") else delete(model))
    session.exec(delete(Participant).where(Participant.participant_id == participant_id))
    session.commit()

    return {"status": "accepted"}
