"""Webhook verification. Fails closed: an unset secret rejects every request."""

from __future__ import annotations

import hashlib
import hmac


def verify_subscription(mode: str | None, token: str | None, challenge: str | None, expected_token: str) -> str | None:
    """Meta GET handshake. Returns the challenge to echo, or None to reject."""
    if not expected_token or mode != "subscribe" or token is None or challenge is None:
        return None
    return challenge if hmac.compare_digest(token, expected_token) else None


def verify_signature(body: bytes, signature_header: str | None, app_secret: str) -> bool:
    """X-Hub-Signature-256: sha256=<hex HMAC of the raw body with the app secret>."""
    if not app_secret or not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature_header.removeprefix("sha256="), expected)


def verify_token(provided: str | None, expected: str) -> bool:
    """Shared-token check for providers without body signatures (Gupshup)."""
    return bool(expected) and provided is not None and hmac.compare_digest(provided, expected)
