"""Graph nodes: intent classifier, tool router, escalation check, tier handlers, response generator."""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from typing import Protocol, Sequence

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool

from agent.prompts import CLASSIFIER_PROMPT, build_system_prompt
from agent.state import (
    AgentReply,
    ConversationState,
    EscalationDecision,
    IntentResult,
    LeadScore,
    RetrievedChunk,
    Stage,
)
from config import COLD_DRIP_SECONDS, WARM_REENGAGE_SECONDS, Settings
from storage import Job, Store
from tools.crm_update import lead_payload
from tools.escalation import ActionsWriter, Notifier, escalate_to_human, evaluate_triggers, is_explicit_human_request

log = logging.getLogger("nodes")

_ARABIC = re.compile(r"[؀-ۿ]")

NO_CONTEXT_FALLBACK = {
    "en": "I don't have that information in our product docs — let me connect you with a specialist.",
    "ar": "لا تتوفر لديّ هذه المعلومة في وثائق المنتج، وسأوصلك الآن بأحد المختصين.",
}
ERROR_FALLBACK = {
    "en": "Sorry, I couldn't process that just now. Could you say it another way?",
    "ar": "عذرًا، لم أتمكن من معالجة رسالتك الآن. هل يمكنك إعادة صياغتها؟",
}

PRODUCT_INTENTS = {"product_question", "pricing_question", "objection", "buying_signal"}


def lang_of(text: str) -> str:
    return "ar" if _ARABIC.search(text) else "en"


def latest_customer_text(messages: Sequence[AnyMessage]) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return m.content if isinstance(m.content, str) else str(m.content)
    return ""


def customer_texts(messages: Sequence[AnyMessage]) -> list[str]:
    return [m.content if isinstance(m.content, str) else str(m.content) for m in messages if isinstance(m, HumanMessage)]


class Classifier(Protocol):
    async def classify(self, messages: Sequence[AnyMessage]) -> IntentResult: ...


class Responder(Protocol):
    async def respond(self, system: str, messages: Sequence[AnyMessage]) -> AgentReply: ...


class OpenAIClassifier:
    def __init__(self, runnable, company_name: str):
        self._runnable = runnable
        self._prompt = CLASSIFIER_PROMPT.format(company_name=company_name)

    async def classify(self, messages: Sequence[AnyMessage]) -> IntentResult:
        return await self._runnable.ainvoke([SystemMessage(self._prompt), *messages])


class OpenAIResponder:
    def __init__(self, runnable):
        self._runnable = runnable

    async def respond(self, system: str, messages: Sequence[AnyMessage]) -> AgentReply:
        return await self._runnable.ainvoke([SystemMessage(system), *messages])


@dataclass
class Deps:
    settings: Settings
    classifier: Classifier
    responder: Responder
    tools: dict[str, BaseTool]  # search_products, score_lead, escalate_to_human, update_crm
    notifier: Notifier
    actions_writer: ActionsWriter | None
    store: Store


def make_nodes(deps: Deps):
    s = deps.settings

    async def classify_intent(state: ConversationState) -> dict:
        latest = latest_customer_text(state.messages)
        try:
            intent = await deps.classifier.classify(state.messages)
        except Exception as e:
            log.error("classify_intent.fail phone=%s err=%s", state.phone, e)
            intent = IntentResult(needs_product_search=True, search_query=latest, stage=state.stage)
        if is_explicit_human_request(latest):
            intent.explicit_human_request = True
        return {
            "intent": intent,
            "stage": intent.stage,
            "retrieved": [],
            "reply": None,
            "escalation": EscalationDecision(),
        }

    async def route_to_tool(state: ConversationState) -> dict:
        intent = state.intent or IntentResult()
        update: dict = {}
        if intent.needs_product_search or intent.intent in PRODUCT_INTENTS:
            query = intent.search_query or latest_customer_text(state.messages)
            raw = await deps.tools["search_products"].ainvoke({"query": query})
            update["retrieved"] = [RetrievedChunk.model_validate(c) for c in raw]
        try:
            scored = await deps.tools["score_lead"].ainvoke(
                {
                    "conversation_history": list(state.messages),
                    "user_profile": {"customer_timestamps": list(state.customer_timestamps)},
                }
            )
            update["lead_score"] = LeadScore.model_validate(scored)
        except Exception as e:
            log.error("score_lead.fail phone=%s err=%s — keeping previous score", state.phone, e)
        return update

    async def check_escalation(state: ConversationState) -> dict:
        if state.escalated:
            return {"escalation": EscalationDecision()}
        intent = state.intent or IntentResult()
        decision = evaluate_triggers(
            latest_text=latest_customer_text(state.messages),
            customer_texts=customer_texts(state.messages),
            intent=intent,
            lead_score=state.lead_score,
            failed_attempts=state.failed_attempts,
            # A lead already handed off for being HOT is not re-escalated for the same score after release.
            hot_threshold=float("inf") if state.hot_handoff_done else s.thresholds["HOT"],
        )
        # "Question exceeds knowledge base scope": a product question with nothing retrieved.
        needs_kb = intent.needs_product_search or intent.intent in PRODUCT_INTENTS
        if needs_kb and not state.retrieved:
            decision.escalate = True
            decision.priority = decision.priority if decision.priority in ("P0",) else "P1"
            decision.reasons.append("question_exceeds_kb_scope")
        return {"escalation": decision}

    def route_after_opt_out_check(state: ConversationState) -> str:
        # The model recognised an opt-out: stop here; webhook/handler.py runs the opt-out in code.
        return "opt_out" if state.intent and state.intent.intent == "opt_out" else "continue"

    def route_after_check(state: ConversationState) -> str:
        if state.escalation.escalate:
            return "escalate"
        if state.lead_score.tier == "HOT" and (state.escalated or state.hot_handoff_done):
            # Already handed off: a HOT score alone must not open a second handoff (and a card with no priority).
            return "nurture"
        return {"HOT": "escalate", "WARM": "nurture", "COLD": "self_service"}[state.lead_score.tier]

    async def escalate(state: ConversationState) -> dict:
        if not state.escalation.escalate:
            state.escalation = EscalationDecision(escalate=True, priority="P0", reasons=[f"hot_lead score={state.lead_score.score}"])
        contact = await deps.store.get_contact(state.phone)
        card = await escalate_to_human(
            notifier=deps.notifier,
            actions_writer=deps.actions_writer,
            phone=state.phone,
            decision=state.escalation,
            intent=state.intent or IntentResult(),
            lead_score=state.lead_score,
            messages=state.messages,
            profile={"name": contact.name, "first_seen_at": contact.first_seen_at},
        )
        await deps.store.save_escalation(card.escalation_id, card.model_dump())
        contact.human_active = True
        contact.active_escalation_id = card.escalation_id
        contact.tier = state.lead_score.tier
        await deps.store.save_contact(contact)
        await deps.store.cancel(f"reengage:{state.phone}")
        await deps.store.cancel(f"drip:{state.phone}")
        await deps.store.schedule(
            Job(job_id=f"sla:{card.escalation_id}", kind="sla", phone=state.phone, due_at=card.sla_deadline, payload={"escalation_id": card.escalation_id})
        )
        hot = state.escalation.priority == "P0" and any(r.startswith("hot_lead") for r in state.escalation.reasons)
        return {"escalated": True, "stage": Stage.HANDOFF, "hot_handoff_done": state.hot_handoff_done or hot}

    async def _crm_and_schedule(state: ConversationState, keep: str, drop: str, delay: float) -> None:
        intent = state.intent.intent if state.intent else None
        await deps.tools["update_crm"].ainvoke({"lead_data": lead_payload(state.phone, state.lead_score, state.stage.value, intent)})
        await deps.store.cancel(f"{drop}:{state.phone}")
        # Rescheduled on every inbound message, so the clock always runs from the customer's last word.
        await deps.store.schedule(Job(job_id=f"{keep}:{state.phone}", kind=keep, phone=state.phone, due_at=time.time() + delay))

    async def nurture(state: ConversationState) -> dict:
        await _crm_and_schedule(state, "reengage", "drip", WARM_REENGAGE_SECONDS)
        return {}

    async def self_service(state: ConversationState) -> dict:
        await _crm_and_schedule(state, "drip", "reengage", COLD_DRIP_SECONDS)
        return {}

    async def generate_response(state: ConversationState) -> dict:
        latest = latest_customer_text(state.messages)
        lang = lang_of(latest)
        intent = state.intent or IntentResult()
        handoff = state.escalation.priority if state.escalation.escalate else None
        kb_miss = "question_exceeds_kb_scope" in state.escalation.reasons
        if kb_miss and not intent.explicit_human_request:
            # Code, not the prompt, guarantees a product question with no context gets no invented answer.
            reply = AgentReply(text=NO_CONTEXT_FALLBACK[lang])
            return {"reply": reply, "messages": [AIMessage(reply.text)]}
        system = build_system_prompt(
            agent_name=s.agent_name,
            company_name=s.company_name,
            hot_threshold=s.thresholds["HOT"],
            stage=state.stage,
            lead_score=state.lead_score,
            retrieved=state.retrieved,
            handoff_priority=handoff,
            tier=state.lead_score.tier,
        )
        try:
            reply = await deps.responder.respond(system, state.messages)
            failed = 0
        except Exception as e:
            log.error("generate_response.fail phone=%s err=%s", state.phone, e)
            reply = AgentReply(text=ERROR_FALLBACK[lang])
            failed = state.failed_attempts + 1
        if handoff:
            reply.buttons = []
        return {"reply": reply, "messages": [AIMessage(reply.text)], "failed_attempts": failed}

    return {
        "classify_intent": classify_intent,
        "route_to_tool": route_to_tool,
        "check_escalation": check_escalation,
        "escalate_to_human": escalate,
        "nurture": nurture,
        "self_service": self_service,
        "generate_response": generate_response,
        "route_after_check": route_after_check,
        "route_after_opt_out_check": route_after_opt_out_check,
    }
