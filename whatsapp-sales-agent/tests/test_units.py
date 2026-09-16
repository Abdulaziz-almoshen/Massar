"""Pure-function tests: scoring, triggers, chunking, verification, parsing, send gate, jobs."""

from __future__ import annotations

import hashlib
import hmac
import time

import pytest

from agent.state import BantSignals, DimensionSignal, IntentResult, LeadScore
from config import SCORING_WEIGHTS, THRESHOLDS
from rag.ingest import chunk_markdown, split_tables
from storage import Contact, Job, MemoryStore
from tests.fakes import SLACK_URL, Harness, settings
from tools.escalation import evaluate_triggers, is_all_caps, is_explicit_human_request, repeated_question_count
from tools.lead_scorer import compute_score, engagement_velocity, tier_for
from tools.nurture import run_job
from webhook.handler import is_opt_out
from webhook.outbound import Outgoing, SendGate, clamp_title, clean_buttons
from webhook.verification import verify_signature, verify_subscription, verify_token
from webhook.whatsapp import CloudApiProvider, GupshupProvider, parse_cloud_api, parse_gupshup


# ---------------- scoring


def signals(**strengths: float) -> BantSignals:
    return BantSignals(**{k: DimensionSignal(strength=v, evidence=k) for k, v in strengths.items()})


def test_weights_and_thresholds_are_the_blueprint_values():
    assert SCORING_WEIGHTS == {
        "budget_match": 3,
        "timeline_urgency": 2,
        "pain_point_clarity": 2,
        "decision_maker_authority": 2,
        "engagement_velocity": 1.5,
        "question_depth": 1,
    }
    assert THRESHOLDS == {"HOT": 8, "WARM": 5, "COLD": 0}


@pytest.mark.parametrize(("score", "tier"), [(8, "HOT"), (7.99, "WARM"), (5, "WARM"), (4.9, "COLD"), (0, "COLD")])
def test_tier_boundaries(score, tier):
    assert tier_for(score, THRESHOLDS) == tier


def test_budget_plus_timeline_plus_authority_plus_pain_is_hot():
    s = compute_score(signals(budget_match=1, timeline_urgency=1, decision_maker_authority=1, pain_point_clarity=1), 0, SCORING_WEIGHTS, THRESHOLDS)
    assert s.score == 9 and s.tier == "HOT" and s.missing_dimensions == []


def test_partial_strength_is_weighted_and_missing_dims_listed():
    s = compute_score(signals(budget_match=0.5, question_depth=1), 1.0, SCORING_WEIGHTS, THRESHOLDS)
    assert s.score == 1.5 + 1 + 1.5
    assert s.tier == "COLD"
    assert s.missing_dimensions == ["decision_maker_authority", "pain_point_clarity", "timeline_urgency"]
    assert "engagement_velocity" in s.signals_detected


def test_engagement_velocity():
    assert engagement_velocity([]) == 0
    assert engagement_velocity([0, 30, 60]) == 1.0
    assert engagement_velocity([0, 400]) == 0.5
    assert engagement_velocity([0, 5000]) == 0.0


# ---------------- escalation triggers


def decide(text="hello", texts=None, score=0.0, failed=0, **intent):
    return evaluate_triggers(
        latest_text=text,
        customer_texts=texts or [text],
        intent=IntentResult(**intent),
        lead_score=LeadScore(score=score),
        failed_attempts=failed,
        hot_threshold=8,
    )


def test_no_trigger_no_escalation():
    assert not decide().escalate


@pytest.mark.parametrize(
    "text",
    ["talk to a human", "Can I speak with someone?", "get me a manager", "real person please", "agent", "ابي اكلم موظف", "حولني على خدمة العملاء"],
)
def test_explicit_human_request_patterns(text):
    assert is_explicit_human_request(text)
    assert decide(text).priority == "P0"


@pytest.mark.parametrize("text", ["what does your agent pricing look like for real estate?", "who is the human resources contact"])
def test_human_request_false_positives(text):
    assert not is_explicit_human_request(text)


def test_priority_is_highest_hit():
    d = decide(score=9, complex_issue=True, confidence=0.2)
    assert d.priority == "P0" and len(d.reasons) == 3


def test_negative_sentiment_needs_two_exchanges():
    assert not decide(sentiment=-0.9).escalate
    assert decide("bad", texts=["hi", "bad"], sentiment=-0.9).priority == "P1"


def test_frustration_signals():
    assert is_all_caps("WHY IS THIS NOT WORKING")
    assert not is_all_caps("OK")
    qs = ["how much is it?", "hi", "How much is it??", "how much is it?"]
    assert repeated_question_count(qs) == 3
    assert decide(qs[-1], texts=qs).priority == "P1"


def test_confidence_failure_after_two_attempts():
    assert not decide(failed=1).escalate
    assert decide(failed=2).priority == "P1"


def test_complex_issue_is_p2():
    assert decide(complex_issue=True).priority == "P2"


# ---------------- chunking


DOC = """# Product X
Intro paragraph.

## Pricing
Our plans:

| Plan | Price |
|---|---|
| Growth | 900 |
| Enterprise | custom |

After the table.

### Notes
""" + ("Long prose sentence about onboarding. " * 400)


def test_tables_stay_atomic_and_headers_recorded():
    chunks = chunk_markdown(DOC, "x.md", chunk_size=256, chunk_overlap=20)
    tables = [c for c in chunks if c.is_table]
    assert len(tables) == 1
    assert tables[0].content.count("\n") == 3 and "Enterprise" in tables[0].content
    assert tables[0].headers == "Product X › Pricing"
    assert any(c.headers == "Product X › Pricing › Notes" for c in chunks)
    assert len([c for c in chunks if "Notes" in c.headers]) > 1, "long prose must be split"
    assert len({c.chunk_id for c in chunks}) == len(chunks)


def test_split_tables_runs():
    runs = split_tables("a\n|x|y|\n|1|2|\nb")
    assert [t for _, t in runs] == [False, True, False]


def test_contextualized_text_prepends_context():
    c = chunk_markdown("# A\ntext", "a.md", chunk_size=100, chunk_overlap=0)[0]
    c.context = "This chunk is from doc A."
    assert c.contextualized.startswith("This chunk is from doc A.\n\n")


# ---------------- verification


def test_signature_fails_closed_and_verifies():
    body = b'{"a":1}'
    sig = "sha256=" + hmac.new(b"s3cret", body, hashlib.sha256).hexdigest()
    assert verify_signature(body, sig, "s3cret")
    assert not verify_signature(body, sig, "")
    assert not verify_signature(body + b" ", sig, "s3cret")
    assert not verify_signature(body, None, "s3cret")


def test_subscription_and_token():
    assert verify_subscription("subscribe", "t", "123", "t") == "123"
    assert verify_subscription("subscribe", "t", "123", "") is None
    assert verify_subscription("subscribe", "x", "123", "t") is None
    assert not verify_token("anything", "")
    assert verify_token("t", "t")


# ---------------- parsing and providers


CLOUD = {
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "contacts": [{"wa_id": "966500000009", "profile": {"name": "Noura"}}],
                        "messages": [
                            {"id": "wamid.1", "from": "966500000009", "timestamp": "1700000000", "type": "text", "text": {"body": "hi"}},
                            {"id": "wamid.2", "from": "966500000009", "type": "interactive", "interactive": {"button_reply": {"id": "b0", "title": "See pricing"}}},
                            {"id": "wamid.3", "from": "966500000009", "type": "image", "image": {}},
                        ],
                        "statuses": [{"id": "wamid.0", "status": "read"}],
                    }
                }
            ]
        }
    ]
}


def test_parse_cloud_api():
    msgs = parse_cloud_api(CLOUD)
    assert [(m.message_id, m.text, m.is_button_tap) for m in msgs] == [("wamid.1", "hi", False), ("wamid.2", "See pricing", True)]
    assert msgs[0].name == "Noura" and msgs[0].phone == "966500000009"


def test_parse_gupshup_v2_and_v3():
    v2 = {"type": "message", "timestamp": 1700000000000, "payload": {"id": "g1", "source": "+966 50 000 0009", "type": "text", "payload": {"text": "مرحبا"}, "sender": {"phone": "966500000009", "name": "N"}}}
    [m] = parse_gupshup(v2)
    assert (m.message_id, m.phone, m.text) == ("g1", "966500000009", "مرحبا")
    assert parse_gupshup({"type": "message-event", "payload": {}}) == []
    assert len(parse_gupshup(CLOUD)) == 2


def test_cloud_api_payload_shapes():
    btn = CloudApiProvider.payload(Outgoing(kind="buttons", to="1", text="Pick", buttons=["A", "B"]))
    assert btn["interactive"]["action"]["buttons"][1]["reply"]["title"] == "B"
    tpl = CloudApiProvider.payload(Outgoing(kind="template", to="1", template_name="t", template_params=["x"]))
    assert tpl["template"]["components"][0]["parameters"][0]["text"] == "x"


def test_gupshup_form():
    p = GupshupProvider(api_key="k", app_name="App", source="917834811114")
    url, form = p.form(Outgoing(kind="text", to="966", text="hi"))
    assert url.endswith("/msg") and form["src.name"] == "App" and '"text": "hi"' in form["message"]


# ---------------- send gate


def test_button_titles_clamped_to_20_bytes_on_char_boundary():
    assert clamp_title("See pricing") == "See pricing"
    arabic = "أرسلوا الملف التعريفي"
    clamped = clamp_title(arabic)
    assert len(clamped.encode()) <= 20 and arabic.startswith(clamped)
    assert clean_buttons(["a", "a", "b", "c", "d"]) == ["a", "b", "c"]


class OkProvider:
    def __init__(self):
        self.sent = []

    async def send(self, msg):
        self.sent.append(msg)
        return "id-1"


def contact(**kw) -> Contact:
    return Contact(phone="966500000001", last_inbound_at=time.time(), **kw)


async def test_gate_defaults_to_dry_run():
    gate = SendGate(settings(), OkProvider())
    r = await gate.send(Outgoing(kind="text", to="966500000001", text="hi"), contact())
    assert r.status == "dry_run"


async def test_gate_allowlist_window_and_opt_out():
    provider = OkProvider()
    gate = SendGate(settings(whatsapp_send_enabled=True, send_allowlist="+966 500 000 001"), provider)
    msg = lambda **kw: Outgoing(to="966500000001", text="hi", **{"kind": "text", **kw})  # noqa: E731
    assert (await gate.send(msg(), contact())).status == "sent"
    assert (await gate.send(Outgoing(kind="text", to="966599999999", text="hi"), contact())).reason == "recipient_not_in_allowlist"
    assert (await gate.send(msg(), Contact(phone="966500000001"))).reason == "outside_24h_window"
    assert (await gate.send(msg(kind="template", template_name="t"), Contact(phone="966500000001"))).status == "sent"
    assert (await gate.send(msg(), contact(opted_out=True))).reason == "opted_out"
    assert (await gate.send(msg(), contact(opted_out=True), opt_out_confirmation=True)).status == "sent"
    assert len(provider.sent) == 3


async def test_gate_provider_error_is_failed_not_retried():
    class Boom:
        calls = 0

        async def send(self, msg):
            Boom.calls += 1
            raise RuntimeError("timeout")

    gate = SendGate(settings(whatsapp_send_enabled=True, allow_all_recipients=True), Boom())
    r = await gate.send(Outgoing(kind="text", to="1", text="hi"), contact())
    assert r.status == "failed" and Boom.calls == 1


@pytest.mark.parametrize("text", ["STOP", "stop!", "إيقاف", "please stop sending messages", "لا اريد رسائل"])
def test_opt_out_patterns(text):
    assert is_opt_out(text)


@pytest.mark.parametrize("text", ["don't stop now", "what's the stop date for the trial?", "hi"])
def test_opt_out_false_positives(text):
    assert not is_opt_out(text)


# ---------------- jobs


async def test_reengage_job_sends_template_and_skips_without_one():
    h = Harness()
    await h.store.save_contact(Contact(phone="1"))
    job = Job(job_id="reengage:1", kind="reengage", phone="1", due_at=0)
    assert await run_job(job, settings=h.settings, store=h.store, gate=h.gate, notifier=h.notifier) == "template_dry_run"
    s = settings(reengage_template_name="")
    assert await run_job(job, settings=s, store=h.store, gate=h.gate, notifier=h.notifier) == "skipped_no_template"
    await h.store.save_contact(Contact(phone="1", opted_out=True))
    assert await run_job(job, settings=h.settings, store=h.store, gate=h.gate, notifier=h.notifier) == "skipped_contact_state"


async def test_sla_breach_alerts_unless_acknowledged():
    h = Harness()
    await h.say("966500000001", "talk to a human")
    c = await h.store.get_contact("966500000001")
    job = h.store.jobs[f"sla:{c.active_escalation_id}"]
    alerts = len(h.recorder.to(SLACK_URL))
    assert await run_job(job, settings=h.settings, store=h.store, gate=h.gate, notifier=h.notifier) == "sla_breach_alerted"
    assert len(h.recorder.to(SLACK_URL)) == alerts + 1
    assert "SLA BREACH" in h.recorder.to(SLACK_URL)[-1]["text"]
    card = await h.store.get_escalation(c.active_escalation_id)
    card["acknowledged_at"] = time.time()
    await h.store.save_escalation(c.active_escalation_id, card)
    assert await run_job(job, settings=h.settings, store=h.store, gate=h.gate, notifier=h.notifier) == "sla_ok"


async def test_memory_store_due_jobs_claims_once():
    s = MemoryStore()
    await s.schedule(Job(job_id="a", kind="drip", phone="1", due_at=10))
    await s.schedule(Job(job_id="b", kind="drip", phone="2", due_at=10_000))
    assert [j.job_id for j in await s.due_jobs(100)] == ["a"]
    assert await s.due_jobs(100) == []


# ---------------- review regressions


@pytest.mark.parametrize(
    "text",
    [
        "Can your system stop sending duplicate reminders to patients?",
        "we want to stop manual messaging of claims",
        "no more messages lost between branches",
        "ربما أحتاج التواصل مع فريق المبيعات",
        "عندما أريد التواصل معكم",
        "ما أريده هو التواصل مع موظف",
    ],
)
def test_opt_out_review_false_positives(text):
    assert not is_opt_out(text)


@pytest.mark.parametrize(
    "text",
    [
        "unsubscribe me", "please stop", "stop pls", "STOP 🛑", "remove me from your list", "don't message me again",
        "don’t contact me", "إلغاء الاشتراك", "أوقفوا الرسائل", "لا ترسلوا لي رسائل", "لا تراسلوني",
    ],
)
def test_opt_out_review_misses(text):
    assert is_opt_out(text)


@pytest.mark.parametrize(
    "text",
    [
        "I don't want to talk to a human, just tell me the price",
        "no need to speak with a person",
        "ما ابي اكلم موظف، جاوبني انت",
        "can I talk to one of your existing clients as a reference?",
    ],
)
def test_human_request_review_false_positives(text):
    assert not is_explicit_human_request(text)


@pytest.mark.parametrize(
    "text",
    ["أريد التحدث مع موظف", "هل يمكنني التحدث إلى شخص؟", "ابغى موظف", "ممكن أكلم موظف", "connect me to an agent", "I want a human", "can I speak to sales?"],
)
def test_human_request_review_misses(text):
    assert is_explicit_human_request(text)


async def test_classifier_opt_out_intent_is_a_backstop():
    from tests.fakes import FakeClassifier

    h = Harness()

    async def classify(messages):
        r = await FakeClassifier().classify(messages)
        if "leave me alone" in str(messages[-1].content):
            r.intent = "opt_out"
        return r

    from agent.nodes import Deps
    from agent.orchestrator import build_graph

    class C:
        async def classify(self, messages):
            return await classify(messages)

    deps = Deps(settings=h.settings, classifier=C(), responder=h.responder, tools=h.graph_tools, notifier=h.notifier, actions_writer=None, store=h.store)
    h.processor._graph = build_graph(deps, checkpointer=h.checkpointer)
    await h.say("966500000001", "hi")
    assert await h.say("966500000001", "please leave me alone now") == "opted_out"
    c = await h.store.get_contact("966500000001")
    assert c.opted_out and "drip:966500000001" not in h.store.jobs


async def test_opt_out_during_handoff_cancels_sla_and_warns_rep():
    h = Harness()
    await h.say("966500000001", "talk to a human please")
    eid = (await h.store.get_contact("966500000001")).active_escalation_id
    assert await h.say("966500000001", "STOP") == "opted_out"
    assert f"sla:{eid}" not in h.store.jobs
    assert "OPTED OUT" in h.recorder.to(SLACK_URL)[-1]["text"]
    job = Job(job_id=f"sla:{eid}", kind="sla", phone="966500000001", due_at=0, payload={"escalation_id": eid})
    assert await run_job(job, settings=h.settings, store=h.store, gate=h.gate, notifier=h.notifier) == "sla_skipped_opted_out"


async def test_released_hot_lead_is_not_handed_back_for_the_same_score():
    h = Harness()
    phone = "966500000001"
    await h.say(phone, "We have a problem: claims are manual")
    await h.say(phone, "I'm the director, what's the pricing? ASAP")
    first = (await h.store.get_contact(phone)).active_escalation_id
    assert first
    # release, as the endpoint does
    c = await h.store.get_contact(phone)
    c.human_active, c.active_escalation_id = False, ""
    await h.store.save_contact(c)
    await h.graph.aupdate_state({"configurable": {"thread_id": phone}}, {"escalated": False}, as_node="generate_response")
    assert (await h.say(phone, "thanks, one more thing about onboarding")).startswith("replied")
    assert not (await h.store.get_contact(phone)).human_active


async def test_contact_edited_without_release_does_not_crash_the_conversation():
    h = Harness()
    phone = "966500000001"
    await h.say(phone, "We have a problem: claims are manual")
    await h.say(phone, "I'm the director, what's the pricing? ASAP")
    c = await h.store.get_contact(phone)
    c.human_active = False  # CRM edit, no /release: graph still has escalated=True
    await h.store.save_contact(c)
    assert (await h.say(phone, "hello again")).startswith("replied")


async def test_window_uses_customer_timestamp_not_arrival_time():
    from webhook.whatsapp import InboundMessage

    h = Harness()
    old = time.time() - 30 * 3600
    out = await h.processor.handle(InboundMessage(message_id="late", phone="966500000001", name="", text="hi", timestamp=old))
    assert out == "replied_blocked"
    assert h.last_sent()[1].reason == "outside_24h_window"


def test_four_button_reply_is_trimmed_not_a_parse_error():
    from agent.state import AgentReply

    r = AgentReply.model_validate({"text": "x", "buttons": [{"title": t} for t in "abcd"]})
    assert [b.title for b in r.buttons] == ["a", "b", "c"]


async def test_long_body_with_buttons_goes_as_text():
    gate = SendGate(settings(), None)
    msg = Outgoing(kind="buttons", to="966500000001", text="x" * 1100, buttons=["A"])
    await gate.send(msg, contact())
    assert msg.kind == "text" and msg.buttons == []


def test_partial_scoring_config_is_rejected():
    with pytest.raises(ValueError):
        settings(thresholds={"HOT": 7})
    with pytest.raises(ValueError):
        settings(scoring_weights={"budget_match": 3})
