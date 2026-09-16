"""Integration: HOT, WARM and COLD lead conversations through the full graph, send gate and store."""

from __future__ import annotations

import time

from config import COLD_DRIP_SECONDS, WARM_REENGAGE_SECONDS
from tests.fakes import CRM_URL, SLACK_URL, Harness

PHONE = "966500000001"


async def test_hot_lead_escalates_with_context_card_and_agent_goes_silent():
    h = Harness()
    await h.say(PHONE, "hi")
    await h.say(PHONE, "We have a problem: claims are manual and we are losing money")
    outcome = await h.say(PHONE, "I'm the operations director. What's the pricing? We need this ASAP")

    assert outcome == "replied_dry_run"
    contact = await h.store.get_contact(PHONE)
    assert contact.human_active and contact.active_escalation_id

    card = await h.store.get_escalation(contact.active_escalation_id)
    assert card["priority"] == "P0"
    assert any(r.startswith("hot_lead") for r in card["reasons"])
    assert card["tier"] == "HOT" and card["lead_score"] >= 8
    assert {"budget_match", "timeline_urgency", "pain_point_clarity", "decision_maker_authority"} <= set(card["qualifying_answers"])
    assert [t["role"] for t in card["transcript"]].count("customer") == 3
    assert card["sla_deadline"] - card["created_at"] == 30  # P0 SLA

    assert h.recorder.to(SLACK_URL), "rep must be alerted"
    assert any(b.get("event") == "escalation" for b in h.recorder.to(CRM_URL))
    msg, result = h.last_sent()
    assert "specialist" in msg.text and msg.kind == "text"  # handoff message carries no buttons
    assert f"sla:{card['escalation_id']}" in h.store.jobs

    # The rep owns it now: the next customer message is forwarded, not answered by the agent.
    sent_before = len(h.gate.log)
    assert await h.say(PHONE, "hello?") == "forwarded_to_human"
    assert len(h.gate.log) == sent_before


async def test_warm_lead_gets_answer_from_kb_and_48h_reengagement():
    h = Harness()
    await h.say(PHONE, "hi")
    outcome = await h.say(PHONE, "we struggle with manual claims. what is the pricing for the growth plan, and does the integration use an api?")

    assert outcome == "replied_dry_run"
    values = await h.state(PHONE)
    assert values["lead_score"].tier == "WARM", values["lead_score"]
    assert not (await h.store.get_contact(PHONE)).human_active
    msg, _ = h.last_sent()
    assert msg.text.startswith("From pricing.md") and msg.kind == "buttons"
    job = h.store.jobs[f"reengage:{PHONE}"]
    assert abs(job.due_at - (time.time() + WARM_REENGAGE_SECONDS)) < 60
    assert f"drip:{PHONE}" not in h.store.jobs
    assert any(b.get("event") == "lead_update" and b["tier"] == "WARM" for b in h.recorder.to(CRM_URL))


async def test_cold_lead_enters_drip_and_is_not_escalated():
    h = Harness()
    outcome = await h.say(PHONE, "hi there")
    assert outcome == "replied_dry_run"
    values = await h.state(PHONE)
    assert values["lead_score"].tier == "COLD"
    assert values["lead_score"].missing_dimensions == ["budget_match", "decision_maker_authority", "pain_point_clarity", "timeline_urgency"]
    job = h.store.jobs[f"drip:{PHONE}"]
    assert abs(job.due_at - (time.time() + COLD_DRIP_SECONDS)) < 60
    assert not h.recorder.to(SLACK_URL)
    assert "COLD lead" in h.responder.systems[-1]


async def test_explicit_human_request_is_p0_even_on_first_message():
    h = Harness()
    await h.say(PHONE, "talk to a human please")
    contact = await h.store.get_contact(PHONE)
    card = await h.store.get_escalation(contact.active_escalation_id)
    assert card["priority"] == "P0" and "explicit_human_request" in card["reasons"]


async def test_arabic_human_request_matches_in_code():
    h = Harness()
    await h.say(PHONE, "ابي اكلم موظف")
    assert (await h.store.get_contact(PHONE)).human_active


async def test_product_question_with_no_kb_context_gets_fallback_and_p1_handoff():
    h = Harness(chunks=[])
    await h.say(PHONE, "what features does the plan include?")
    msg, _ = h.last_sent()
    assert msg.text == "I don't have that information in our product docs — let me connect you with a specialist."
    contact = await h.store.get_contact(PHONE)
    card = await h.store.get_escalation(contact.active_escalation_id)
    assert card["priority"] == "P1" and "question_exceeds_kb_scope" in card["reasons"]
    assert not h.responder.systems, "no model call may compose an answer without context"


async def test_opt_out_is_absolute():
    h = Harness()
    await h.say(PHONE, "hi")
    assert await h.say(PHONE, "STOP") == "opted_out"
    msg, result = h.last_sent()
    assert "unsubscribed" in msg.text and result.status == "dry_run"
    assert f"drip:{PHONE}" not in h.store.jobs and f"reengage:{PHONE}" not in h.store.jobs
    assert await h.say(PHONE, "what is the pricing?") == "ignored_opted_out"
    assert await h.say(PHONE, "إيقاف") == "opted_out"


async def test_duplicate_webhook_delivery_runs_once():
    h = Harness()
    from webhook.whatsapp import InboundMessage

    m = InboundMessage(message_id="same", phone=PHONE, name="", text="hi", timestamp=0)
    assert (await h.processor.handle(m)).startswith("replied")
    assert await h.processor.handle(m) == "duplicate"


async def test_release_returns_conversation_to_agent():
    h = Harness()
    await h.say(PHONE, "talk to a human")
    contact = await h.store.get_contact(PHONE)
    contact.human_active = False
    await h.store.save_contact(contact)
    assert (await h.say(PHONE, "thanks, one more question")).startswith("replied")
