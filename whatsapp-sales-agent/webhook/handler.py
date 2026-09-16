"""One inbound message → dedupe → opt-out → human-owned check → agent graph → send gate."""

from __future__ import annotations

import asyncio
import logging
import re
import time

from langchain_core.messages import HumanMessage

from agent.state import AgentReply
from storage import Store
from tools.escalation import Notifier
from webhook.outbound import Outgoing, SendGate
from webhook.whatsapp import InboundMessage

log = logging.getLogger("handler")

# Opt-out is decided in code, before the model sees the message. Two failure directions matter
# equally: a miss keeps messaging someone who said stop, and a false positive silently drops a buyer
# who asked "can your system stop sending duplicate reminders?". So the whole-message matcher is
# broad, and the in-sentence phrasings must name US messaging THEM. The classifier's opt_out intent
# is a second net for phrasings neither list knows (agent/nodes.py routes it here).
_STRIP = re.compile(r"[^\w\s'’]+")
_OPT_OUT_WHOLE = re.compile(
    r"^(please\s+|pls\s+)?(stop|unsubscribe|quit|cancel|opt\s*out|end)(\s+(it|me|now|please|pls|thanks|thank\s+you))*$"
    r"|^(please\s+|pls\s+)?stop\s+(sending|messaging|texting)(\s+(me|us))?(\s+(messages|texts|these|this|them))?(\s+(please|pls|thanks))?$"
    r"|^(إيقاف|ايقاف|أوقف|اوقف|توقف|توقفوا|وقف|الغاء|إلغاء|حظر|الغاء الاشتراك|إلغاء الاشتراك)(\s+(الرسائل|الاشتراك|لو سمحت|من فضلك))*$",
    re.I,
)
_OPT_OUT_PHRASES = [
    re.compile(r"\bstop\s+(messaging|texting|sending|contacting|spamming)\s+(me|us)\b", re.I),
    re.compile(r"\b(don['’]?t|do\s+not|never)\s+(message|text|contact|whatsapp)\s+(me|us)\b", re.I),
    re.compile(r"\bremove\s+(me|us|my\s+number)\s+from\b", re.I),
    re.compile(r"\bunsubscribe\s+(me|us)\b", re.I),
    re.compile(r"\bno\s+more\s+(messages|texts)(\s+(please|pls|thanks))?$", re.I),
    re.compile(r"(أوقفوا|اوقفوا|وقفوا|أوقف|اوقف|توقفوا عن)\s+(ال)?(رسائل|رسايل|مراسلتي|مراسلة|الارسال|الإرسال)"),
    re.compile(r"(?<!\S)(لا|مو|مب)\s+(ترسلوا|ترسل|تراسلوني|تراسلني|تتواصلوا|تكلموني)(?!\S)"),
    re.compile(r"(?<!\S)(لا|ما|مو|مب)\s+(اريد|أريد|ابي|أبي|ابغى|أبغى)\s+(ال)?(رسائل|رسايل|مراسلات|مراسلة)(?!\S)"),
    re.compile(r"(الغاء|إلغاء)\s+الاشتراك"),
]
_OPT_IN = re.compile(r"^(start|subscribe|ابدأ|ابدا|اشتراك)$", re.I)

OPT_OUT_CONFIRMATION = {
    "ar": "تم إيقاف الرسائل. لن نراسلك مجددًا، ويمكنك إرسال «ابدأ» في أي وقت لإعادة الاشتراك.",
    "en": "You're unsubscribed and won't receive further messages. Send START any time to resubscribe.",
}


def _normalize(text: str) -> str:
    # Emoji and punctuation off ("STOP 🛑", "stop!!"), whitespace collapsed.
    return " ".join(_STRIP.sub(" ", text).split())


def is_opt_out(text: str) -> bool:
    t = _normalize(text)
    return bool(_OPT_OUT_WHOLE.match(t) or any(p.search(t) for p in _OPT_OUT_PHRASES))


def is_opt_in(text: str) -> bool:
    return bool(_OPT_IN.match(_normalize(text)))


class InboundProcessor:
    def __init__(self, *, store: Store, gate: SendGate, graph, notifier: Notifier):
        self._store, self._gate, self._graph, self._notifier = store, gate, graph, notifier
        self._locks: dict[str, asyncio.Lock] = {}

    def _lock(self, phone: str) -> asyncio.Lock:
        return self._locks.setdefault(phone, asyncio.Lock())

    async def handle(self, msg: InboundMessage) -> str:
        if not msg.phone or not msg.message_id:
            return "ignored_malformed"
        if not await self._store.mark_seen(msg.message_id):
            return "duplicate"
        try:
            # Turns for one contact run strictly in order; different contacts run concurrently.
            async with self._lock(msg.phone):
                return await self._handle_locked(msg)
        except BaseException:
            # Un-mark so a provider redelivery is processed instead of being dropped as a duplicate.
            await self._store.forget_seen(msg.message_id)
            raise

    async def _opt_out(self, contact, msg: InboundMessage, now: float) -> str:
        from agent.nodes import lang_of

        was_with_rep = contact.human_active
        contact.opted_out = True
        await self._store.save_contact(contact)
        await self._store.cancel(f"reengage:{msg.phone}")
        await self._store.cancel(f"drip:{msg.phone}")
        if contact.active_escalation_id:
            await self._store.cancel(f"sla:{contact.active_escalation_id}")
        await self._notifier.post_crm({"event": "opt_out", "phone": msg.phone, "at": now})
        if was_with_rep:
            # Reps reply outside SendGate, so this alert is the only thing standing between them and a breach.
            await self._notifier.alert(f"Customer +{msg.phone} OPTED OUT. Do not message them. Last message: {msg.text[:200]}")
        await self._gate.send(
            Outgoing(kind="text", to=msg.phone, text=OPT_OUT_CONFIRMATION[lang_of(msg.text)]), contact, opt_out_confirmation=True
        )
        return "opted_out"

    async def _handle_locked(self, msg: InboundMessage) -> str:
        now = time.time()
        # The 24h window runs from when the customer wrote, not when a (possibly delayed) webhook arrived.
        sent_at = msg.timestamp if 0 < msg.timestamp <= now + 300 else now
        contact = await self._store.get_contact(msg.phone)
        contact.last_inbound_at = max(contact.last_inbound_at, sent_at)
        if msg.name:
            contact.name = msg.name

        if is_opt_out(msg.text):
            return await self._opt_out(contact, msg, now)
        if contact.opted_out:
            if not is_opt_in(msg.text):
                await self._store.save_contact(contact)
                return "ignored_opted_out"
            contact.opted_out = False

        await self._store.save_contact(contact)

        if contact.human_active:
            await self._notifier.alert(f"Customer +{msg.phone} replied on a handed-off conversation: {msg.text[:300]}")
            await self._notifier.post_crm({"event": "customer_message", "phone": msg.phone, "text": msg.text, "at": now})
            return "forwarded_to_human"

        result = await self._graph.ainvoke(
            {"phone": msg.phone, "messages": [HumanMessage(msg.text)], "customer_timestamps": [sent_at]},
            config={"configurable": {"thread_id": msg.phone}},
        )
        values = result if isinstance(result, dict) else result.model_dump()
        intent = values.get("intent")
        if intent is not None and getattr(intent, "intent", None) == "opt_out":
            # Second net: the classifier recognised an opt-out phrasing the matcher does not know.
            return await self._opt_out(await self._store.get_contact(msg.phone), msg, now)
        reply = values.get("reply")
        if reply is None:
            return "no_reply"
        reply = reply if isinstance(reply, AgentReply) else AgentReply.model_validate(reply)
        contact = await self._store.get_contact(msg.phone)  # the graph may have escalated
        tier = values.get("lead_score")
        if tier is not None:
            contact.tier = tier.tier if hasattr(tier, "tier") else tier["tier"]
            await self._store.save_contact(contact)
        titles = [b.title for b in reply.buttons]
        out = Outgoing(kind="buttons" if titles else "text", to=msg.phone, text=reply.text, buttons=titles)
        sent = await self._gate.send(out, contact)
        return f"replied_{sent.status}"
