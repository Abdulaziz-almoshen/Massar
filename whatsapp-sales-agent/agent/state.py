"""Conversation state schema (Pydantic)."""

from __future__ import annotations

import operator
from enum import Enum
from typing import Annotated, Literal

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, field_validator


class Stage(str, Enum):
    GREETING = "greeting"
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    VALUE_PRESENTATION = "value_presentation"
    OBJECTION_HANDLING = "objection_handling"
    CONVERSION = "conversion"
    HANDOFF = "handoff"


Tier = Literal["HOT", "WARM", "COLD"]
Priority = Literal["P0", "P1", "P2"]
ObjectionType = Literal["price", "priority", "timing", "trust", "security", "competitor", "fit"]


class IntentResult(BaseModel):
    """classify_intent output for the latest customer message."""

    intent: Literal[
        "greeting",
        "product_question",
        "pricing_question",
        "objection",
        "buying_signal",
        "human_request",
        "off_topic",
        "opt_out",
        "other",
    ] = "other"
    stage: Stage = Stage.DISCOVERY
    sentiment: float = Field(0.0, ge=-1.0, le=1.0, description="-1 very negative .. 1 very positive")
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    explicit_human_request: bool = False
    high_value_signal: bool = Field(False, description="budget discussion, RFP mention, 'ready to buy'")
    complex_issue: bool = Field(False, description="multi-department, policy exception, legal topic")
    objection_type: ObjectionType | None = None
    needs_product_search: bool = False
    search_query: str = ""


class DimensionSignal(BaseModel):
    strength: float = Field(0.0, ge=0.0, le=1.0)
    evidence: str = ""


class BantSignals(BaseModel):
    """LLM-extracted qualifying signals. engagement_velocity is computed in code, not here."""

    budget_match: DimensionSignal = Field(default_factory=DimensionSignal)
    timeline_urgency: DimensionSignal = Field(default_factory=DimensionSignal)
    pain_point_clarity: DimensionSignal = Field(default_factory=DimensionSignal)
    decision_maker_authority: DimensionSignal = Field(default_factory=DimensionSignal)
    question_depth: DimensionSignal = Field(default_factory=DimensionSignal)


class LeadScore(BaseModel):
    score: float = 0.0
    tier: Tier = "COLD"
    signals_detected: dict[str, str] = Field(default_factory=dict)
    missing_dimensions: list[str] = Field(default_factory=list)


class RetrievedChunk(BaseModel):
    chunk_id: str
    source: str
    headers: str = ""
    content: str
    score: float = 0.0


class Button(BaseModel):
    title: str


class AgentReply(BaseModel):
    text: str
    # No max_length: a 4-button reply from the model must be trimmed, not turned into a parse failure.
    buttons: list[Button] = Field(default_factory=list)

    @field_validator("buttons")
    @classmethod
    def _at_most_three(cls, v: list[Button]) -> list[Button]:
        return v[:3]


class EscalationDecision(BaseModel):
    escalate: bool = False
    priority: Priority | None = None
    reasons: list[str] = Field(default_factory=list)


class ConversationState(BaseModel):
    phone: str
    messages: Annotated[list[AnyMessage], add_messages] = Field(default_factory=list)
    # epoch seconds of every customer message, for engagement velocity
    customer_timestamps: Annotated[list[float], operator.add] = Field(default_factory=list)
    stage: Stage = Stage.GREETING
    intent: IntentResult | None = None
    retrieved: list[RetrievedChunk] = Field(default_factory=list)
    lead_score: LeadScore = Field(default_factory=LeadScore)
    failed_attempts: int = 0
    escalation: EscalationDecision = Field(default_factory=EscalationDecision)
    escalated: bool = False
    # Set when a HOT score caused a handoff. Survives /release: the score rereads the whole history,
    # so without it a released HOT lead would be handed straight back on the next message.
    hot_handoff_done: bool = False
    reply: AgentReply | None = None


# Checkpoints are deserialized with an explicit allowlist: only these state types (plus LangGraph's
# built-in safe types, which include LangChain messages) can be rebuilt from Redis.
CHECKPOINT_TYPES = [
    ("agent.state", name)
    for name in (
        "Stage",
        "IntentResult",
        "DimensionSignal",
        "BantSignals",
        "LeadScore",
        "RetrievedChunk",
        "Button",
        "AgentReply",
        "EscalationDecision",
        "ConversationState",
    )
]


def checkpoint_serde(*, redis: bool = False):
    """Serializer for the checkpointer. The Redis saver needs its JSON subclass; without the JSON
    allowlist it silently returns these models as raw constructor dicts, which breaks every resumed
    conversation after a restart (caught by tests/test_services.py)."""
    if redis:
        from langgraph.checkpoint.redis.jsonplus_redis import JsonPlusRedisSerializer

        return JsonPlusRedisSerializer(
            allowed_msgpack_modules=CHECKPOINT_TYPES,
            allowed_json_modules=[(*module.split("."), name) for module, name in CHECKPOINT_TYPES],
        )
    from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

    return JsonPlusSerializer(allowed_msgpack_modules=CHECKPOINT_TYPES)
