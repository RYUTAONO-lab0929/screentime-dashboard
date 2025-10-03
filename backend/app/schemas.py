from __future__ import annotations
from datetime import datetime, date
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class IngestEvent(BaseModel):
    event_id: Optional[str] = None
    device_id: str
    captured_at: datetime
    payload: Dict[str, Any] = Field(default_factory=dict)
    source: Literal["ipad", "mdm"] = "ipad"
    participant_pseudo_id: Optional[str] = None


class IngestRequest(BaseModel):
    source: Literal["ipad", "mdm"]
    events: List[IngestEvent]


class SummaryQuery(BaseModel):
    start_date: date
    end_date: date
    cohort: Optional[str] = None


class SummaryItem(BaseModel):
    category: Optional[str] = None
    total_minutes: int
    pickups: int
    notifications: int


class SummaryResponse(BaseModel):
    start_date: date
    end_date: date
    cohort: Optional[str] = None
    items: List[SummaryItem]


class DailyPoint(BaseModel):
    date: date
    total_minutes: int
    pickups: int
    notifications: int


class ParticipantDailyResponse(BaseModel):
    participant_id: str
    points: List[DailyPoint]
