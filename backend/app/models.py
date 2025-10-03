from __future__ import annotations
from datetime import datetime, date, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, UniqueConstraint


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class Participant(TimestampMixin, SQLModel, table=True):
    __tablename__ = "participant"
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: str = Field(index=True, unique=True)
    cohort_id: Optional[str] = Field(default=None, index=True)
    enrollment_date: Optional[date] = None
    consent_flags: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: str = Field(default="active", index=True)


class Device(TimestampMixin, SQLModel, table=True):
    __tablename__ = "device"
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(index=True, unique=True)
    participant_id: Optional[str] = Field(default=None, index=True)
    model: Optional[str] = None
    os_version: Optional[str] = None
    last_seen_at: Optional[datetime] = None


class RawEvent(TimestampMixin, SQLModel, table=True):
    __tablename__ = "raw_event"
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: Optional[str] = Field(default=None, index=True)
    device_id: str = Field(index=True)
    captured_at: datetime
    payload_json: dict = Field(sa_column=Column(JSON))
    signature: Optional[str] = None
    source: str = Field(default="ipad", index=True)


class UsageDaily(TimestampMixin, SQLModel, table=True):
    __tablename__ = "usage_daily"
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date = Field(index=True)
    participant_id: str = Field(index=True)
    category: Optional[str] = Field(default=None, index=True)
    app_bundle_id: Optional[str] = Field(default=None, index=True)
    total_minutes: int = 0
    pickups: int = 0
    notifications: int = 0
    sessions_count: int = 0

    __table_args__ = (
        UniqueConstraint("date", "participant_id", "category", "app_bundle_id", name="uq_usage_daily"),
    )


class WebDomainDaily(TimestampMixin, SQLModel, table=True):
    __tablename__ = "web_domain_daily"
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date = Field(index=True)
    participant_id: str = Field(index=True)
    domain: str = Field(index=True)
    total_minutes: int = 0

    __table_args__ = (
        UniqueConstraint("date", "participant_id", "domain", name="uq_web_domains_daily"),
    )


class Limit(TimestampMixin, SQLModel, table=True):
    __tablename__ = "limit"
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: str = Field(index=True)
    rule_name: str
    target: str
    minutes_per_day: int


class AnonymizationKey(SQLModel, table=True):
    __tablename__ = "anonymization_key"
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: str = Field(index=True)
    salt_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLog(TimestampMixin, SQLModel, table=True):
    __tablename__ = "audit_log"
    id: Optional[int] = Field(default=None, primary_key=True)
    actor: Optional[str] = None
    event_type: str
    object_type: Optional[str] = None
    object_id: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))
