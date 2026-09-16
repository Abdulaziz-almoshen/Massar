"""Weighted scoring engine (blueprint Table 3).

The LLM only reads the conversation and reports per-dimension strength with evidence. The score,
the tier and the missing dimensions are computed here, deterministically, so a threshold change is
a config change and every score can be explained dimension by dimension.
"""

from __future__ import annotations

from statistics import median
from typing import Protocol, Sequence

from langchain_core.messages import AnyMessage, SystemMessage
from langchain_core.tools import StructuredTool

from agent.prompts import SCORER_PROMPT
from agent.state import BantSignals, LeadScore, Tier

# The four BANT dimensions whose absence is reported as "missing". Engagement velocity and question
# depth are supporting signals, not qualification facts.
BANT_DIMENSIONS = ("budget_match", "decision_maker_authority", "pain_point_clarity", "timeline_urgency")

# A dimension counts as detected once the extractor is at least this sure.
DETECTED_AT = 0.3


class SignalExtractor(Protocol):
    async def extract(self, messages: Sequence[AnyMessage]) -> BantSignals: ...


class OpenAISignalExtractor:
    def __init__(self, runnable):
        self._runnable = runnable  # chat_model.with_structured_output(BantSignals)

    async def extract(self, messages: Sequence[AnyMessage]) -> BantSignals:
        return await self._runnable.ainvoke([SystemMessage(SCORER_PROMPT), *messages])


def engagement_velocity(customer_timestamps: Sequence[float]) -> float:
    """Fast responses, multiple messages → active lead. Computed from timestamps, never guessed."""
    if len(customer_timestamps) < 2:
        return 0.0
    ordered = sorted(customer_timestamps)
    gap = median(b - a for a, b in zip(ordered, ordered[1:]))
    if len(ordered) >= 3 and gap <= 120:
        return 1.0
    if gap <= 600:
        return 0.5
    return 0.0


def tier_for(score: float, thresholds: dict[str, float]) -> Tier:
    if score >= thresholds["HOT"]:
        return "HOT"
    if score >= thresholds["WARM"]:
        return "WARM"
    return "COLD"


def compute_score(
    signals: BantSignals,
    velocity: float,
    weights: dict[str, float],
    thresholds: dict[str, float],
) -> LeadScore:
    strengths = {name: getattr(signals, name).strength for name in BantSignals.model_fields}
    strengths["engagement_velocity"] = velocity
    score = round(sum(weights[name] * strengths.get(name, 0.0) for name in weights), 2)
    detected = {
        name: getattr(signals, name).evidence or f"strength {getattr(signals, name).strength:.1f}"
        for name in BantSignals.model_fields
        if getattr(signals, name).strength >= DETECTED_AT
    }
    if velocity >= DETECTED_AT:
        detected["engagement_velocity"] = f"velocity {velocity:.1f}"
    missing = [name for name in BANT_DIMENSIONS if strengths[name] < DETECTED_AT]
    return LeadScore(score=score, tier=tier_for(score, thresholds), signals_detected=detected, missing_dimensions=missing)


async def score_lead(
    extractor: SignalExtractor,
    conversation_history: Sequence[AnyMessage],
    customer_timestamps: Sequence[float],
    weights: dict[str, float],
    thresholds: dict[str, float],
) -> LeadScore:
    signals = await extractor.extract(conversation_history)
    return compute_score(signals, engagement_velocity(customer_timestamps), weights, thresholds)


def make_score_lead_tool(extractor: SignalExtractor, weights: dict[str, float], thresholds: dict[str, float]) -> StructuredTool:
    async def _score(conversation_history: list, user_profile: dict | None = None) -> dict:
        """Score the lead from the conversation. Returns {score, tier, signals_detected, missing_dimensions}."""
        timestamps = (user_profile or {}).get("customer_timestamps", [])
        result = await score_lead(extractor, conversation_history, timestamps, weights, thresholds)
        return result.model_dump()

    return StructuredTool.from_function(coroutine=_score, name="score_lead")
