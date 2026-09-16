"""CRM webhook integration for pipeline management."""

from __future__ import annotations

import time

from langchain_core.tools import StructuredTool

from agent.state import LeadScore
from tools.escalation import Notifier


def lead_payload(phone: str, lead_score: LeadScore, stage: str, intent: str | None) -> dict:
    return {
        "event": "lead_update",
        "phone": phone,
        "score": lead_score.score,
        "tier": lead_score.tier,
        "signals_detected": lead_score.signals_detected,
        "missing_dimensions": lead_score.missing_dimensions,
        "stage": stage,
        "intent": intent,
        "updated_at": time.time(),
    }


async def update_crm(notifier: Notifier, lead_data: dict) -> bool:
    return await notifier.post_crm(lead_data)


def make_update_crm_tool(notifier: Notifier) -> StructuredTool:
    async def _update(lead_data: dict) -> dict:
        """Push lead data to the CRM webhook."""
        return {"delivered": await update_crm(notifier, lead_data)}

    return StructuredTool.from_function(coroutine=_update, name="update_crm")
