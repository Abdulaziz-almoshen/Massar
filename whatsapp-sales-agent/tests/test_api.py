"""HTTP layer: verification handshake, signatures, token auth, admin endpoints, background processing."""

from __future__ import annotations

import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient

from main import App, create_app
from tests.fakes import Harness

PHONE = "966500000001"


def cloud_body(text: str, msg_id: str = "wamid.1") -> bytes:
    return json.dumps(
        {"entry": [{"changes": [{"value": {"messages": [{"id": msg_id, "from": PHONE, "type": "text", "text": {"body": text}}]}}]}]}
    ).encode()


def sign(body: bytes, secret: str = "app-secret") -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


@pytest.fixture
def harness():
    return Harness()


@pytest.fixture
def client(harness):
    async def factory(s, stack):
        return App(
            settings=harness.settings,
            store=harness.store,
            gate=harness.gate,
            notifier=harness.notifier,
            processor=harness.processor,
            graph=harness.graph,
        )

    with TestClient(create_app(runtime_factory=factory, settings=harness.settings, start_worker=False)) as c:
        yield c


def test_health_reports_send_disabled(client):
    body = client.get("/health").json()
    assert body["ok"] and body["send_enabled"] is False and body["state"] == "memory"


def test_meta_verification_handshake(client):
    ok = client.get("/webhook/whatsapp", params={"hub.mode": "subscribe", "hub.verify_token": "verify-me", "hub.challenge": "42"})
    assert ok.status_code == 200 and ok.text == "42"
    bad = client.get("/webhook/whatsapp", params={"hub.mode": "subscribe", "hub.verify_token": "nope", "hub.challenge": "42"})
    assert bad.status_code == 403


def test_unsigned_or_badly_signed_webhook_rejected(client, harness):
    body = cloud_body("hi")
    assert client.post("/webhook/whatsapp", content=body).status_code == 401
    assert client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body, "wrong")}).status_code == 401
    assert harness.gate.log == []


def test_signed_webhook_runs_the_agent(client, harness):
    body = cloud_body("hi there")
    r = client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert r.status_code == 200 and r.json() == {"received": 1}
    msg, result = harness.gate.log[-1]  # TestClient runs background tasks before returning
    assert msg.to == PHONE and result.status == "dry_run"


def test_unparseable_signed_body_is_400_not_silent_200(client):
    body = b"not json"
    assert client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)}).status_code == 400


def test_gupshup_token(client, harness):
    payload = {"type": "message", "payload": {"id": "g1", "source": PHONE, "type": "text", "payload": {"text": "hi"}}}
    assert client.post("/webhook/gupshup", json=payload).status_code == 401
    assert client.post("/webhook/gupshup?token=gs-token", json=payload).json() == {"received": 1}
    assert harness.gate.log


def test_admin_endpoints_need_token_and_ack_and_release_work(client, harness):
    body = cloud_body("talk to a human")
    client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)})
    import asyncio

    contact = asyncio.run(harness.store.get_contact(PHONE))
    assert contact.human_active
    eid = contact.active_escalation_id

    assert client.post(f"/escalations/{eid}/ack").status_code == 401
    auth = {"Authorization": "Bearer admin-secret"}
    acked = client.post(f"/escalations/{eid}/ack", headers=auth).json()
    assert acked["within_sla"] is True
    assert f"sla:{eid}" not in harness.store.jobs
    assert client.post("/escalations/nope/ack", headers=auth).status_code == 404

    assert client.post(f"/conversations/{PHONE}/release", headers=auth).json()["human_active"] is False
    # Released: a new human request escalates again rather than being swallowed.
    body2 = cloud_body("talk to a human again", "wamid.2")
    client.post("/webhook/whatsapp", content=body2, headers={"X-Hub-Signature-256": sign(body2)})
    again = asyncio.run(harness.store.get_contact(PHONE))
    assert again.human_active and again.active_escalation_id != eid


def test_release_unknown_contact_is_404(client):
    r = client.post("/conversations/966599999999/release", headers={"Authorization": "Bearer admin-secret"})
    assert r.status_code == 404


def test_opt_out_is_stored_before_ack_and_a_store_failure_returns_500(client, harness):
    body = cloud_body("إيقاف", "wamid.stop")
    real_save = harness.store.save_contact
    calls = {"n": 0}

    async def flaky(contact):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("redis timeout")
        await real_save(contact)

    harness.store.save_contact = flaky
    first = client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert first.status_code == 500  # provider will redeliver
    again = client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert again.status_code == 200
    import asyncio

    assert asyncio.run(harness.store.get_contact(PHONE)).opted_out, "redelivery must not be dropped as a duplicate"


def test_release_accepts_plus_prefixed_phone_and_cancels_sla(client, harness):
    body = cloud_body("talk to a human")
    client.post("/webhook/whatsapp", content=body, headers={"X-Hub-Signature-256": sign(body)})
    import asyncio

    eid = asyncio.run(harness.store.get_contact(PHONE)).active_escalation_id
    assert f"sla:{eid}" in harness.store.jobs
    r = client.post(f"/conversations/+{PHONE}/release", headers={"Authorization": "Bearer admin-secret"})
    assert r.status_code == 200 and f"sla:{eid}" not in harness.store.jobs
