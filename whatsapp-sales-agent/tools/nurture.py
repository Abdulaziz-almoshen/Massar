"""Scheduled jobs: WARM 48-hour re-engagement, COLD drip, and escalation SLA breach alerts.

Re-engagement always lands outside the 24-hour window (the timer resets on every inbound message),
so it can only be an approved template. With no template configured the job is logged and skipped.
"""

from __future__ import annotations

import asyncio
import logging
import time

from config import Settings
from storage import Job, Store
from tools.escalation import ContextCard, Notifier, slack_text
from webhook.outbound import Outgoing, SendGate

log = logging.getLogger("nurture")


async def run_job(job: Job, *, settings: Settings, store: Store, gate: SendGate, notifier: Notifier) -> str:
    if job.kind == "sla":
        card = await store.get_escalation(job.payload.get("escalation_id", ""))
        if not card or card.get("acknowledged_at"):
            return "sla_ok"
        if (await store.get_contact(job.phone)).opted_out:
            return "sla_skipped_opted_out"
        await notifier.alert(slack_text(ContextCard.model_validate(card), breach=True))
        return "sla_breach_alerted"

    contact = await store.get_contact(job.phone)
    if contact.opted_out or contact.human_active:
        return "skipped_contact_state"
    template = settings.reengage_template_name if job.kind == "reengage" else settings.drip_template_name
    if not template:
        log.info("job.skip kind=%s phone=%s (no approved template configured)", job.kind, job.phone)
        return "skipped_no_template"
    msg = Outgoing(kind="template", to=job.phone, template_name=template, template_language=settings.reengage_template_language)
    result = await gate.send(msg, contact)
    return f"template_{result.status}"


async def worker(*, settings: Settings, store: Store, gate: SendGate, notifier: Notifier, interval: float = 5.0) -> None:
    while True:
        try:
            for job in await store.due_jobs(time.time()):
                try:
                    outcome = await run_job(job, settings=settings, store=store, gate=gate, notifier=notifier)
                    log.info("job.done id=%s outcome=%s", job.job_id, outcome)
                except Exception as e:
                    log.error("job.fail id=%s err=%s", job.job_id, e)
        except Exception as e:
            log.error("worker.poll_fail err=%s", e)
        await asyncio.sleep(interval)
