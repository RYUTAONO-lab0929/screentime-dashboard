from __future__ import annotations
import hmac
import hashlib
from datetime import datetime, timezone
from typing import Optional


class HMACVerifier:
    @staticmethod
    def make_signature(secret: str, timestamp: str, body: bytes) -> str:
        message = (timestamp + "." + body.decode("utf-8")).encode("utf-8")
        return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

    @staticmethod
    def verify(signature: str, secret: str, timestamp: str, body: bytes, max_skew_seconds: int = 300) -> bool:
        try:
            ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except Exception:
            return False
        now = datetime.now(timezone.utc)
        if abs((now - ts).total_seconds()) > max_skew_seconds:
            return False
        expected = HMACVerifier.make_signature(secret, timestamp, body)
        return hmac.compare_digest(expected, signature)


def is_bearer_authorized(authorization_header: Optional[str], allowed_tokens: list[str]) -> bool:
    if not authorization_header:
        return False
    if not authorization_header.lower().startswith("bearer "):
        return False
    token = authorization_header.split(" ", 1)[1].strip()
    return token in (allowed_tokens or [])
