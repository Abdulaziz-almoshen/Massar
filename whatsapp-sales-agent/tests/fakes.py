"""Deterministic stand-ins for the model-backed components, so tests run offline."""

from __future__ import annotations

import json
import re
from typing import Sequence

import httpx
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from agent.nodes import Deps
from agent.orchestrator import build_graph
from agent.state import checkpoint_serde
from agent.state import AgentReply, BantSignals, Button, DimensionSignal, IntentResult, RetrievedChunk, Stage
from config import Settings
from storage import MemoryStore
from tools.crm_update import make_update_crm_tool
from tools.escalation import Notifier, make_escalate_tool
from tools.lead_scorer import make_score_lead_tool
from tools.product_search import make_search_products_tool
from webhook.handler import InboundProcessor
from webhook.outbound import SendGate

CRM_URL = "https://crm.test/hook"
SLACK_URL = "https://slack.test/hook"


def _customer(messages: Sequence[AnyMessage]) -> list[str]:
    return [str(m.content) for m in messages if isinstance(m, HumanMessage)]


class FakeClassifier:
    async def classify(self, messages: Sequence[AnyMessage]) -> IntentResult:
        t = _customer(messages)[-1].lower()
        product = any(w in t for w in ("price", "pricing", "plan", "integrat", "feature", "cost"))
        return IntentResult(
            intent="pricing_question" if "pric" in t else "product_question" if product else "greeting" if "hi" in t else "other",
            stage=Stage.QUALIFICATION if product else Stage.DISCOVERY,
            sentiment=-0.8 if "terrible" in t else 0.3,
            confidence=0.9,
            high_value_signal="ready to buy" in t,
            needs_product_search=product,
            search_query=t,
        )


class FakeExtractor:
    """Reads the whole conversation like the LLM would; strength 1.0 when the cue is present."""

    CUES = {
        "budget_match": ("budget", "pricing", "price"),
        "timeline_urgency": ("asap", "this month", "by q1", "deadline"),
        "pain_point_clarity": ("problem", "manual", "losing", "struggle"),
        "decision_maker_authority": ("i'm the", "i am the", "director", "i approve", "ceo"),
        "question_depth": ("integrat", "api", "implementation"),
    }

    async def extract(self, messages: Sequence[AnyMessage]) -> BantSignals:
        text = " ".join(_customer(messages)).lower()
        fields = {}
        for dim, cues in self.CUES.items():
            hit = next((c for c in cues if c in text), None)
            fields[dim] = DimensionSignal(strength=1.0 if hit else 0.0, evidence=hit or "")
        return BantSignals(**fields)


class FakeResponder:
    def __init__(self) -> None:
        self.systems: list[str] = []

    async def respond(self, system: str, messages: Sequence[AnyMessage]) -> AgentReply:
        self.systems.append(system)
        if "[HANDOFF IN PROGRESS]" in system:
            return AgentReply(text="A specialist is joining now and will continue from here.")
        m = re.search(r"\[1\] source: (\S+)", system)
        text = f"From {m.group(1)}: here is what our docs say." if m else "Happy to help — what are you looking to solve?"
        return AgentReply(text=text, buttons=[Button(title="See pricing"), Button(title="Book a demo")])


class FakeRetriever:
    def __init__(self, chunks: list[RetrievedChunk]):
        self.chunks = chunks
        self.queries: list[str] = []

    async def search(self, query: str) -> list[RetrievedChunk]:
        self.queries.append(query)
        words = set(re.findall(r"\w+", query.lower()))
        return [c for c in self.chunks if words & set(re.findall(r"\w+", c.content.lower()))][:5]


class Recorder:
    """httpx transport capturing every CRM/Slack POST."""

    def __init__(self) -> None:
        self.requests: list[tuple[str, dict]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append((str(request.url), json.loads(request.content)))
        return httpx.Response(200, json={"ok": True})

    def to(self, url: str) -> list[dict]:
        return [body for u, body in self.requests if u == url]


PRICING_CHUNK = RetrievedChunk(
    chunk_id="c1",
    source="pricing.md",
    headers="Plans › Pricing",
    content="| Plan | Price |\n|---|---|\n| Growth | 900 SAR / month |\n| Enterprise | custom pricing |",
)
INTEGRATION_CHUNK = RetrievedChunk(
    chunk_id="c2", source="integrations.md", headers="Integrations", content="The API integrates with HIS systems over REST."
)


def settings(**overrides) -> Settings:
    base = dict(
        openai_api_key="test",
        crm_webhook_url=CRM_URL,
        slack_webhook_url=SLACK_URL,
        admin_token="admin-secret",
        wa_app_secret="app-secret",
        wa_verify_token="verify-me",
        gupshup_webhook_token="gs-token",
        reengage_template_name="reengage_v1",
        _env_file=None,
    )
    base.update(overrides)
    return Settings(**base)


class Harness:
    def __init__(self, s: Settings | None = None, chunks: list[RetrievedChunk] | None = None, checkpointer=None, store=None):
        self.settings = s or settings()
        self.recorder = Recorder()
        self.notifier = Notifier(
            crm_url=self.settings.crm_webhook_url,
            slack_url=self.settings.slack_webhook_url,
            teams_url="",
            client=httpx.AsyncClient(transport=httpx.MockTransport(self.recorder)),
        )
        self.store = store or MemoryStore()
        self.retriever = FakeRetriever(chunks if chunks is not None else [PRICING_CHUNK, INTEGRATION_CHUNK])
        self.responder = FakeResponder()
        tools = {
            "search_products": make_search_products_tool(self.retriever),
            "score_lead": make_score_lead_tool(FakeExtractor(), self.settings.scoring_weights, self.settings.thresholds),
            "escalate_to_human": make_escalate_tool(self.notifier, None),
            "update_crm": make_update_crm_tool(self.notifier),
        }
        self.graph_tools = tools
        deps = Deps(
            settings=self.settings,
            classifier=FakeClassifier(),
            responder=self.responder,
            tools=tools,
            notifier=self.notifier,
            actions_writer=None,
            store=self.store,
        )
        self.checkpointer = checkpointer or InMemorySaver(serde=checkpoint_serde())
        self.graph = build_graph(deps, checkpointer=self.checkpointer)
        self.gate = SendGate(self.settings, provider=None)
        self.processor = InboundProcessor(store=self.store, gate=self.gate, graph=self.graph, notifier=self.notifier)
        self._n = 0

    async def say(self, phone: str, text: str) -> str:
        from webhook.whatsapp import InboundMessage

        self._n += 1
        return await self.processor.handle(InboundMessage(message_id=f"m{self._n}", phone=phone, name="Test", text=text, timestamp=0))

    def last_sent(self):
        return self.gate.log[-1]

    async def state(self, phone: str):
        return (await self.graph.aget_state({"configurable": {"thread_id": phone}})).values
