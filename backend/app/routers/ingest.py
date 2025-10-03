from __future__ import annotations
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlmodel import Session
from ..config import Settings
from ..db import get_session
from ..models import RawEvent
from ..schemas import IngestRequest
from ..core.security import HMACVerifier, is_bearer_authorized

router = APIRouter(prefix="/ingest/v1", tags=["ingest"])


@router.post("/screentime", status_code=202)
async def ingest_screentime(
    req: Request,
    payload: IngestRequest,
    x_signature: str | None = Header(default=None, alias="X-Signature"),
    x_timestamp: str | None = Header(default=None, alias="X-Timestamp"),
    authorization: str | None = Header(default=None, alias="Authorization"),
    settings: Settings = Depends(Settings),
    session: Session = Depends(get_session),
):
    # 1) Bearerトークン認証（端末/MDMアップローダ向け）
    if not is_bearer_authorized(authorization, settings.ingest_tokens):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # 2) HMAC署名検証（任意だが推奨）
    if not x_signature or not x_timestamp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature headers")

    raw_body = await req.body()
    if not HMACVerifier.verify(x_signature, settings.hmac_secret, x_timestamp, raw_body):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    # 3) 受信イベントを保存
    now_iso = datetime.utcnow().isoformat() + "Z"
    for ev in payload.events:
        raw = RawEvent(
            event_id=ev.event_id,
            device_id=ev.device_id,
            captured_at=ev.captured_at,
            payload_json=ev.payload,
            signature=x_signature,
            source=payload.source,
        )
        session.add(raw)
    session.commit()

    return {"status": "accepted", "received": len(payload.events), "at": now_iso}
