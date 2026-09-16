"""The one door every outbound message goes through.

Order of checks: kill switch → recipient allowlist → opt-out → 24-hour window. Free-form messages
need an open window; templates do not. A blocked or dry-run send is logged with its full payload so
behaviour can be verified without delivering anything.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Literal, Protocol

from config import SERVICE_WINDOW_SECONDS, Settings
from storage import Contact

log = logging.getLogger("outbound")

MAX_BUTTONS = 3
MAX_BUTTON_TITLE_BYTES = 20
MAX_INTERACTIVE_BODY_CHARS = 1024  # Meta rejects an interactive body longer than this


def clamp_title(title: str, limit: int = MAX_BUTTON_TITLE_BYTES) -> str:
    """Truncate to a byte budget on a character boundary (Arabic letters are 2 bytes in UTF-8)."""
    encoded = title.strip().encode("utf-8")
    if len(encoded) <= limit:
        return title.strip()
    return encoded[:limit].decode("utf-8", errors="ignore").strip()


def clean_buttons(titles: list[str]) -> list[str]:
    out: list[str] = []
    for t in titles:
        c = clamp_title(t)
        if c and c not in out:
            out.append(c)
    return out[:MAX_BUTTONS]


@dataclass
class Outgoing:
    kind: Literal["text", "buttons", "template"]
    to: str
    text: str = ""
    buttons: list[str] = field(default_factory=list)
    template_name: str = ""
    template_language: str = "ar"
    template_params: list[str] = field(default_factory=list)


@dataclass
class SendResult:
    status: Literal["sent", "dry_run", "blocked", "failed"]
    reason: str = ""
    provider_id: str = ""


class Provider(Protocol):
    async def send(self, msg: Outgoing) -> str: ...


def window_open(contact: Contact, now: float | None = None) -> bool:
    now = time.time() if now is None else now
    return contact.last_inbound_at > 0 and now - contact.last_inbound_at < SERVICE_WINDOW_SECONDS


class SendGate:
    def __init__(self, settings: Settings, provider: Provider | None):
        self._s = settings
        self._provider = provider
        self.log: list[tuple[Outgoing, SendResult]] = []  # recent decisions, for tests and /health

    def _record(self, msg: Outgoing, result: SendResult) -> SendResult:
        self.log.append((msg, result))
        del self.log[:-200]
        log.info("outbound %s to=%s kind=%s reason=%s text=%r", result.status, msg.to, msg.kind, result.reason, msg.text[:200])
        return result

    async def send(self, msg: Outgoing, contact: Contact, *, opt_out_confirmation: bool = False) -> SendResult:
        if msg.kind == "buttons":
            msg.buttons = clean_buttons(msg.buttons)
            if not msg.buttons or len(msg.text) > MAX_INTERACTIVE_BODY_CHARS:
                # Drop the buttons rather than have the provider reject the whole reply.
                msg.kind, msg.buttons = "text", []
        if contact.opted_out and not opt_out_confirmation:
            return self._record(msg, SendResult("blocked", "opted_out"))
        if msg.kind != "template" and not window_open(contact):
            return self._record(msg, SendResult("blocked", "outside_24h_window"))
        if not self._s.whatsapp_send_enabled or self._provider is None:
            return self._record(msg, SendResult("dry_run", "WHATSAPP_SEND_ENABLED is false"))
        if not self._s.allow_all_recipients and msg.to not in self._s.allowlist:
            return self._record(msg, SendResult("blocked", "recipient_not_in_allowlist"))
        try:
            provider_id = await self._provider.send(msg)
        except Exception as e:
            # Outcome unknown: never retry automatically, the message may already be delivered.
            return self._record(msg, SendResult("failed", f"provider_error: {str(e)[:200]}"))
        return self._record(msg, SendResult("sent", provider_id=provider_id))
