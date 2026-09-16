"""WhatsApp webhook handling: payload parsing for Cloud API and Gupshup, plus the send providers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

import httpx

from webhook.outbound import Outgoing


@dataclass
class InboundMessage:
    message_id: str
    phone: str  # E.164 digits
    name: str
    text: str
    timestamp: float
    is_button_tap: bool = False


def _digits(value: object) -> str:
    return re.sub(r"\D", "", str(value or ""))


def parse_cloud_api(body: dict) -> list[InboundMessage]:
    """Meta Cloud API shape: entry[].changes[].value.{contacts,messages,statuses}. Statuses ignored."""
    out: list[InboundMessage] = []
    for entry in body.get("entry") or []:
        for change in entry.get("changes") or []:
            value = change.get("value") or {}
            names = {c.get("wa_id"): (c.get("profile") or {}).get("name", "") for c in value.get("contacts") or []}
            for m in value.get("messages") or []:
                interactive = m.get("interactive") or {}
                text = (
                    (m.get("text") or {}).get("body")
                    or (m.get("button") or {}).get("text")
                    or (interactive.get("button_reply") or {}).get("title")
                    or (interactive.get("list_reply") or {}).get("title")
                    or ""
                )
                if not text:
                    continue  # media, reactions, location: no text for the agent to act on
                out.append(
                    InboundMessage(
                        message_id=str(m.get("id", "")),
                        phone=_digits(m.get("from")),
                        name=names.get(m.get("from"), ""),
                        text=text,
                        timestamp=float(m.get("timestamp") or 0),
                        is_button_tap=m.get("type") in ("button", "interactive"),
                    )
                )
    return out


def parse_gupshup(body: dict) -> list[InboundMessage]:
    """Gupshup v2 envelope; a Meta-format (v3) body is delegated to the Cloud API parser."""
    if isinstance(body.get("entry"), list):
        return parse_cloud_api(body)
    if body.get("type") != "message":
        return []
    p = body.get("payload") or {}
    inner = p.get("payload") or {}
    text = inner.get("text") if isinstance(inner.get("text"), str) else inner.get("title", "")
    if not text:
        return []
    return [
        InboundMessage(
            message_id=str(p.get("id", "")),
            phone=_digits((p.get("sender") or {}).get("phone") or p.get("source")),
            name=str((p.get("sender") or {}).get("name", "")),
            text=text,
            timestamp=float(body.get("timestamp", 0)) / 1000 if body.get("timestamp") else 0.0,
            is_button_tap=str(p.get("type", "")) in ("button_reply", "list_reply", "quick_reply", "interactive"),
        )
    ]


class CloudApiProvider:
    def __init__(self, *, token: str, phone_number_id: str, graph_version: str, client: httpx.AsyncClient | None = None):
        self._url = f"https://graph.facebook.com/{graph_version}/{phone_number_id}/messages"
        self._headers = {"Authorization": f"Bearer {token}"}
        self._client = client or httpx.AsyncClient(timeout=15)

    @staticmethod
    def payload(msg: Outgoing) -> dict:
        base = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": msg.to}
        if msg.kind == "text":
            return {**base, "type": "text", "text": {"body": msg.text, "preview_url": False}}
        if msg.kind == "buttons":
            return {
                **base,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": msg.text},
                    "action": {
                        "buttons": [{"type": "reply", "reply": {"id": f"b{i}", "title": t}} for i, t in enumerate(msg.buttons)]
                    },
                },
            }
        template: dict = {"name": msg.template_name, "language": {"code": msg.template_language}}
        if msg.template_params:
            template["components"] = [{"type": "body", "parameters": [{"type": "text", "text": p} for p in msg.template_params]}]
        return {**base, "type": "template", "template": template}

    async def send(self, msg: Outgoing) -> str:
        r = await self._client.post(self._url, headers=self._headers, json=self.payload(msg))
        r.raise_for_status()
        return str((r.json().get("messages") or [{}])[0].get("id", ""))


class GupshupProvider:
    MSG_URL = "https://api.gupshup.io/wa/api/v1/msg"
    TEMPLATE_URL = "https://api.gupshup.io/wa/api/v1/template/msg"

    def __init__(self, *, api_key: str, app_name: str, source: str, client: httpx.AsyncClient | None = None):
        self._key, self._app, self._source = api_key, app_name, source
        self._client = client or httpx.AsyncClient(timeout=15)

    def form(self, msg: Outgoing) -> tuple[str, dict]:
        base = {"channel": "whatsapp", "source": self._source, "destination": msg.to, "src.name": self._app}
        if msg.kind == "template":
            # Gupshup templates are addressed by template id; template_name carries it for this provider.
            return self.TEMPLATE_URL, {**base, "template": json.dumps({"id": msg.template_name, "params": msg.template_params})}
        if msg.kind == "buttons":
            message = {
                "type": "quick_reply",
                "msgid": "qr",
                "content": {"type": "text", "text": msg.text},
                "options": [{"title": t} for t in msg.buttons],
            }
        else:
            message = {"type": "text", "text": msg.text}
        return self.MSG_URL, {**base, "message": json.dumps(message, ensure_ascii=False)}

    async def send(self, msg: Outgoing) -> str:
        url, data = self.form(msg)
        r = await self._client.post(url, headers={"apikey": self._key}, data=data)
        r.raise_for_status()
        body = r.json()
        if body.get("status") == "error":
            raise RuntimeError(f"gupshup error: {body}")
        return str(body.get("messageId", ""))
