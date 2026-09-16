"""Human handoff: three-layer triggers (Table 4), context card, CRM + Slack/Teams notification, SLA.

Trigger evaluation is pure and lives in `evaluate_triggers`. An explicit request for a human is
matched in code as well as by the classifier: the blueprint requires that escalation to be
absolute, so it cannot depend on a model noticing it.
"""

from __future__ import annotations

import difflib
import logging
import re
import time
import uuid
from typing import Protocol, Sequence

import httpx
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from agent.prompts import CONTEXT_CARD_ACTIONS_PROMPT
from agent.state import EscalationDecision, IntentResult, LeadScore, Priority
from config import PRIORITY_SLA_SECONDS

log = logging.getLogger("escalation")

_AR_PERSON = r"(موظف|شخص|انسان|إنسان|بشري|مندوب|مسؤول|مسئول|مدير|أحد|احد|خدمة\s*العملاء|فريق\s*المبيعات)"
_HUMAN_REQUEST = [
    re.compile(r"\b(talk|speak|chat)\s+(to|with)\s+(a\s+|an\s+|the\s+|your\s+)?(real\s+)?(human|person|someone|somebody|agent|representative|rep|manager|sales(\s*(person|rep|team))?)\b", re.I),
    re.compile(r"\bconnect\s+me\s+(to|with)\s+(a\s+|an\s+|the\s+|your\s+)?(human|person|someone|agent|representative|rep|manager|sales)\b", re.I),
    re.compile(r"\b(want|need)\s+(a|an)\s+(real\s+)?(human|agent|person|representative)\b", re.I),
    re.compile(r"\b(real|live)\s+(person|human|agent)\b", re.I),
    re.compile(r"\bget\s+me\s+(a|the)\s+(manager|human|person|agent)\b", re.I),
    re.compile(r"^\s*(human|agent|representative|operator)\s*[.!?]*\s*$", re.I),
    re.compile(
        r"(أبي|ابي|أبغى|ابغى|أبغي|ابغي|أريد|اريد|ودي|بغيت|ممكن|يمكنني|أقدر|اقدر|أود|اود)\s+"
        r"(أكلم|اكلم|أتكلم|اتكلم|أتواصل|اتواصل|التواصل|أحاكي|احاكي|التحدث|أتحدث|اتحدث|الحديث)\s+((مع|إلى|الى|ل)\s*)?" + _AR_PERSON
    ),
    re.compile(r"(أبي|ابي|أبغى|ابغى|أبغي|ابغي|أريد|اريد|ودي)\s+(موظف|مندوب|انسان|إنسان|شخص\s+حقيقي)(?!\S)"),
    re.compile(r"(حولني|حوّلني|حولوني|وصلني|وصّلني|وصلوني)\s*(على|ل|لـ|إلى|الى|مع)?\s*(موظف|مندوب|مسؤول|مسئول|مدير|خدمة\s*العملاء|شخص)"),
    re.compile(r"^\s*(موظف|مندوب|خدمة\s*العملاء)[\s.!؟]*$"),
]
# "I don't want to talk to a human" must not force a handoff: reject a match with a negation just before it.
_NEGATED = re.compile(r"(\b(don['’]?t|do\s+not|no\s+need\s+to|not|never|without)\b|(?<!\S)(ما|مو|لا|مب|بدون)(?!\S))(\s+\S+){0,2}\s*$", re.I)

_PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2}

NEGATIVE_SENTIMENT = -0.4
LOW_CONFIDENCE = 0.5
FAILED_ATTEMPTS_LIMIT = 2
REPEATED_QUESTIONS_LIMIT = 3


def is_explicit_human_request(text: str) -> bool:
    for p in _HUMAN_REQUEST:
        for m in p.finditer(text):
            if not _NEGATED.search(text[: m.start()]):
                return True
    return False


def is_all_caps(text: str) -> bool:
    letters = [c for c in text if c.isascii() and c.isalpha()]
    return len(letters) >= 8 and sum(c.isupper() for c in letters) / len(letters) >= 0.8


def _norm(text: str) -> str:
    return re.sub(r"[\W_]+", " ", text.lower()).strip()


def repeated_question_count(customer_texts: Sequence[str]) -> int:
    """How many customer questions (including the latest) are near-duplicates of the latest one."""
    if not customer_texts:
        return 0
    latest = customer_texts[-1]
    if "?" not in latest and "؟" not in latest:
        return 0
    target = _norm(latest)
    return sum(
        1
        for t in customer_texts
        if ("?" in t or "؟" in t) and difflib.SequenceMatcher(None, _norm(t), target).ratio() >= 0.8
    )


def evaluate_triggers(
    *,
    latest_text: str,
    customer_texts: Sequence[str],
    intent: IntentResult,
    lead_score: LeadScore,
    failed_attempts: int,
    hot_threshold: float,
) -> EscalationDecision:
    hits: list[tuple[Priority, str]] = []
    if intent.explicit_human_request or is_explicit_human_request(latest_text):
        hits.append(("P0", "explicit_human_request"))
    if lead_score.score >= hot_threshold:
        hits.append(("P0", f"hot_lead score={lead_score.score}"))
    if intent.high_value_signal:
        hits.append(("P0", "high_value_purchase_signal"))
    if intent.sentiment <= NEGATIVE_SENTIMENT and len(customer_texts) >= 2:
        hits.append(("P1", f"negative_sentiment {intent.sentiment:.2f}"))
    if is_all_caps(latest_text):
        hits.append(("P1", "all_caps"))
    repeats = repeated_question_count(customer_texts)
    if repeats >= REPEATED_QUESTIONS_LIMIT:
        hits.append(("P1", f"repeated_question x{repeats}"))
    if intent.confidence < LOW_CONFIDENCE:
        hits.append(("P1", f"low_confidence {intent.confidence:.2f}"))
    if failed_attempts >= FAILED_ATTEMPTS_LIMIT:
        hits.append(("P1", f"failed_attempts x{failed_attempts}"))
    if intent.complex_issue:
        hits.append(("P2", "complex_multi_step_issue"))
    if not hits:
        return EscalationDecision()
    priority = min((p for p, _ in hits), key=_PRIORITY_RANK.__getitem__)
    return EscalationDecision(escalate=True, priority=priority, reasons=[r for _, r in hits])


class ContextCard(BaseModel):
    escalation_id: str
    phone: str
    priority: Priority
    reasons: list[str]
    created_at: float
    sla_deadline: float
    intent: str
    sentiment: float
    lead_score: float
    tier: str
    customer_profile: dict = Field(default_factory=dict)
    qualifying_answers: dict[str, str] = Field(default_factory=dict)
    missing_dimensions: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    transcript: list[dict] = Field(default_factory=list)


class _Actions(BaseModel):
    actions: list[str] = Field(default_factory=list)


class ActionsWriter(Protocol):
    async def write(self, messages: Sequence[AnyMessage]) -> list[str]: ...


class OpenAIActionsWriter:
    def __init__(self, runnable):
        self._runnable = runnable  # chat_model.with_structured_output(_Actions)

    async def write(self, messages: Sequence[AnyMessage]) -> list[str]:
        result: _Actions = await self._runnable.ainvoke([SystemMessage(CONTEXT_CARD_ACTIONS_PROMPT), *messages])
        return result.actions[:4]


def fallback_actions(lead_score: LeadScore) -> list[str]:
    labels = {
        "budget_match": "Confirm budget range",
        "decision_maker_authority": "Confirm who approves the purchase",
        "pain_point_clarity": "Clarify the business problem to solve",
        "timeline_urgency": "Confirm the timeline",
    }
    actions = ["Reply on WhatsApp now and introduce yourself as the specialist"]
    actions += [labels[d] for d in lead_score.missing_dimensions if d in labels]
    return actions[:4]


def transcript(messages: Sequence[AnyMessage]) -> list[dict]:
    out = []
    for m in messages:
        role = "customer" if isinstance(m, HumanMessage) else "agent" if isinstance(m, AIMessage) else m.type
        out.append({"role": role, "text": m.content if isinstance(m.content, str) else str(m.content)})
    return out


def build_context_card(
    *,
    phone: str,
    decision: EscalationDecision,
    intent: IntentResult,
    lead_score: LeadScore,
    messages: Sequence[AnyMessage],
    profile: dict,
    actions: list[str],
    now: float | None = None,
) -> ContextCard:
    created = time.time() if now is None else now
    assert decision.priority is not None
    return ContextCard(
        escalation_id=uuid.uuid4().hex,
        phone=phone,
        priority=decision.priority,
        reasons=decision.reasons,
        created_at=created,
        sla_deadline=created + PRIORITY_SLA_SECONDS[decision.priority],
        intent=intent.intent,
        sentiment=intent.sentiment,
        lead_score=lead_score.score,
        tier=lead_score.tier,
        customer_profile=profile,
        qualifying_answers=lead_score.signals_detected,
        missing_dimensions=lead_score.missing_dimensions,
        recommended_actions=actions,
        transcript=transcript(messages),
    )


def slack_text(card: ContextCard, *, breach: bool = False) -> str:
    head = "SLA BREACH — still unanswered" if breach else "Lead handoff"
    last = next((t["text"] for t in reversed(card.transcript) if t["role"] == "customer"), "")
    lines = [
        f"*{head}* [{card.priority}] +{card.phone}",
        f"Score {card.lead_score} ({card.tier}) · intent {card.intent} · sentiment {card.sentiment:.2f}",
        f"Why: {', '.join(card.reasons)}",
        f"Last message: {last[:300]}",
    ]
    if card.qualifying_answers:
        lines.append("Qualifying: " + "; ".join(f"{k}: {v}" for k, v in card.qualifying_answers.items()))
    if card.recommended_actions:
        lines.append("Next: " + " · ".join(card.recommended_actions))
    lines.append(f"Ack: POST /escalations/{card.escalation_id}/ack")
    return "\n".join(lines)


class Notifier:
    """CRM webhook + Slack + Teams. Each channel is skipped when its URL is unset."""

    def __init__(self, *, crm_url: str, slack_url: str, teams_url: str, client: httpx.AsyncClient | None = None):
        self._crm, self._slack, self._teams = crm_url, slack_url, teams_url
        self._client = client or httpx.AsyncClient(timeout=10)

    async def _post(self, url: str, payload: dict, channel: str) -> bool:
        if not url:
            log.info("notify.skip channel=%s (url unset)", channel)
            return False
        try:
            r = await self._client.post(url, json=payload)
            r.raise_for_status()
            return True
        except httpx.HTTPError as e:
            log.error("notify.fail channel=%s err=%s", channel, e)
            return False

    async def post_crm(self, payload: dict) -> bool:
        return await self._post(self._crm, payload, "crm")

    async def alert(self, text: str) -> dict[str, bool]:
        return {
            "slack": await self._post(self._slack, {"text": text}, "slack"),
            "teams": await self._post(self._teams, {"text": text}, "teams"),
        }


async def escalate_to_human(
    *,
    notifier: Notifier,
    actions_writer: ActionsWriter | None,
    phone: str,
    decision: EscalationDecision,
    intent: IntentResult,
    lead_score: LeadScore,
    messages: Sequence[AnyMessage],
    profile: dict,
) -> ContextCard:
    actions: list[str] = []
    if actions_writer is not None:
        try:
            actions = await actions_writer.write(messages)
        except Exception as e:  # the handoff must never fail because a summary did
            log.error("context_card.actions_failed err=%s", e)
    card = build_context_card(
        phone=phone,
        decision=decision,
        intent=intent,
        lead_score=lead_score,
        messages=messages,
        profile=profile,
        actions=actions or fallback_actions(lead_score),
    )
    await notifier.post_crm({"event": "escalation", "card": card.model_dump()})
    await notifier.alert(slack_text(card))
    return card


def make_escalate_tool(notifier: Notifier, actions_writer: ActionsWriter | None) -> StructuredTool:
    async def _escalate(reason: str, conversation_summary: str, phone: str = "", priority: str = "P1") -> dict:
        """Hand the conversation to a human sales rep with a context card."""
        decision = EscalationDecision(escalate=True, priority=priority, reasons=[reason])  # type: ignore[arg-type]
        card = await escalate_to_human(
            notifier=notifier,
            actions_writer=None,
            phone=phone,
            decision=decision,
            intent=IntentResult(),
            lead_score=LeadScore(),
            messages=[HumanMessage(conversation_summary)],
            profile={},
        )
        return card.model_dump()

    return StructuredTool.from_function(coroutine=_escalate, name="escalate_to_human")
