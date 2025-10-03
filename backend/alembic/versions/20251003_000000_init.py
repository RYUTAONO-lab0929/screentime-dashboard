from __future__ import annotations
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251003_000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'participant',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('participant_id', sa.String, nullable=False, unique=True),
        sa.Column('cohort_id', sa.String),
        sa.Column('enrollment_date', sa.Date),
        sa.Column('consent_flags', sa.JSON),
        sa.Column('status', sa.String, nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'device',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('device_id', sa.String, nullable=False, unique=True),
        sa.Column('participant_id', sa.String),
        sa.Column('model', sa.String),
        sa.Column('os_version', sa.String),
        sa.Column('last_seen_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'raw_event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.String),
        sa.Column('device_id', sa.String, nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('payload_json', sa.JSON, nullable=False),
        sa.Column('signature', sa.String),
        sa.Column('source', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'usage_daily',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('participant_id', sa.String, nullable=False),
        sa.Column('category', sa.String),
        sa.Column('app_bundle_id', sa.String),
        sa.Column('total_minutes', sa.Integer, nullable=False, server_default='0'),
        sa.Column('pickups', sa.Integer, nullable=False, server_default='0'),
        sa.Column('notifications', sa.Integer, nullable=False, server_default='0'),
        sa.Column('sessions_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('date', 'participant_id', 'category', 'app_bundle_id', name='uq_usage_daily'),
    )

    op.create_table(
        'web_domain_daily',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('participant_id', sa.String, nullable=False),
        sa.Column('domain', sa.String, nullable=False),
        sa.Column('total_minutes', sa.Integer, nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('date', 'participant_id', 'domain', name='uq_web_domains_daily'),
    )

    op.create_table(
        'limit',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('participant_id', sa.String, nullable=False),
        sa.Column('rule_name', sa.String, nullable=False),
        sa.Column('target', sa.String, nullable=False),
        sa.Column('minutes_per_day', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'anonymization_key',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('participant_id', sa.String, nullable=False),
        sa.Column('salt_id', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('actor', sa.String),
        sa.Column('event_type', sa.String, nullable=False),
        sa.Column('object_type', sa.String),
        sa.Column('object_id', sa.String),
        sa.Column('ip_address', sa.String),
        sa.Column('metadata', sa.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    for table in [
        'audit_log',
        'anonymization_key',
        'limit',
        'web_domain_daily',
        'usage_daily',
        'raw_event',
        'device',
        'participant',
    ]:
        op.drop_table(table)
