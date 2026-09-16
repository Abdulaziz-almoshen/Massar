"""Contact metadata, dedupe, escalations and scheduled follow-ups.

Conversation state itself lives in the LangGraph checkpointer; this store holds what the webhook
layer needs before and around a graph run. Redis in production, memory in tests and local dev.
"""

from __future__ import annotations

import json
import time
from typing import Protocol

from pydantic import BaseModel, Field


class Contact(BaseModel):
    phone: str
    name: str = ""
    last_inbound_at: float = 0.0
    opted_out: bool = False
    human_active: bool = False  # a rep owns the conversation; the agent stays silent
    active_escalation_id: str = ""
    tier: str = "COLD"
    first_seen_at: float = Field(default_factory=time.time)


class Job(BaseModel):
    job_id: str  # "<kind>:<phone>" — one pending job per kind per contact
    kind: str  # "reengage" | "drip" | "sla"
    phone: str
    due_at: float
    payload: dict = Field(default_factory=dict)


class Store(Protocol):
    async def get_contact(self, phone: str) -> Contact: ...
    async def save_contact(self, contact: Contact) -> None: ...
    async def mark_seen(self, message_id: str) -> bool: ...
    async def forget_seen(self, message_id: str) -> None: ...
    async def save_escalation(self, escalation_id: str, card: dict) -> None: ...
    async def get_escalation(self, escalation_id: str) -> dict | None: ...
    async def schedule(self, job: Job) -> None: ...
    async def cancel(self, job_id: str) -> None: ...
    async def due_jobs(self, now: float) -> list[Job]: ...
    async def close(self) -> None: ...


class MemoryStore:
    def __init__(self) -> None:
        self.contacts: dict[str, Contact] = {}
        self.seen: set[str] = set()
        self.escalations: dict[str, dict] = {}
        self.jobs: dict[str, Job] = {}

    async def get_contact(self, phone: str) -> Contact:
        return self.contacts.get(phone, Contact(phone=phone)).model_copy()

    async def save_contact(self, contact: Contact) -> None:
        self.contacts[contact.phone] = contact.model_copy()

    async def mark_seen(self, message_id: str) -> bool:
        if message_id in self.seen:
            return False
        self.seen.add(message_id)
        return True

    async def forget_seen(self, message_id: str) -> None:
        self.seen.discard(message_id)

    async def save_escalation(self, escalation_id: str, card: dict) -> None:
        self.escalations[escalation_id] = card

    async def get_escalation(self, escalation_id: str) -> dict | None:
        return self.escalations.get(escalation_id)

    async def schedule(self, job: Job) -> None:
        self.jobs[job.job_id] = job

    async def cancel(self, job_id: str) -> None:
        self.jobs.pop(job_id, None)

    async def due_jobs(self, now: float) -> list[Job]:
        due = [j for j in self.jobs.values() if j.due_at <= now]
        for j in due:
            self.jobs.pop(j.job_id, None)
        return due

    async def close(self) -> None:
        return None


class RedisStore:
    def __init__(self, url: str, retention_days: int, prefix: str = "wsa") -> None:
        import redis.asyncio as redis

        self._r = redis.from_url(url, decode_responses=True)
        self._ttl = retention_days * 24 * 3600
        self._p = prefix

    def _k(self, *parts: str) -> str:
        return ":".join((self._p, *parts))

    async def get_contact(self, phone: str) -> Contact:
        raw = await self._r.get(self._k("contact", phone))
        return Contact.model_validate_json(raw) if raw else Contact(phone=phone)

    async def save_contact(self, contact: Contact) -> None:
        # PDPL data minimisation: contact records expire after the retention period of inactivity.
        await self._r.set(self._k("contact", contact.phone), contact.model_dump_json(), ex=self._ttl)

    async def mark_seen(self, message_id: str) -> bool:
        return bool(await self._r.set(self._k("seen", message_id), "1", nx=True, ex=7 * 24 * 3600))

    async def forget_seen(self, message_id: str) -> None:
        await self._r.delete(self._k("seen", message_id))

    async def save_escalation(self, escalation_id: str, card: dict) -> None:
        await self._r.set(self._k("escalation", escalation_id), json.dumps(card, ensure_ascii=False), ex=self._ttl)

    async def get_escalation(self, escalation_id: str) -> dict | None:
        raw = await self._r.get(self._k("escalation", escalation_id))
        return json.loads(raw) if raw else None

    async def schedule(self, job: Job) -> None:
        pipe = self._r.pipeline()
        pipe.set(self._k("job", job.job_id), job.model_dump_json())
        pipe.zadd(self._k("jobs"), {job.job_id: job.due_at})
        await pipe.execute()

    async def cancel(self, job_id: str) -> None:
        pipe = self._r.pipeline()
        pipe.delete(self._k("job", job_id))
        pipe.zrem(self._k("jobs"), job_id)
        await pipe.execute()

    async def due_jobs(self, now: float) -> list[Job]:
        ids = await self._r.zrangebyscore(self._k("jobs"), 0, now)
        out: list[Job] = []
        for job_id in ids:
            # ZREM returns 1 only for the worker that claimed it, so two replicas never run a job twice.
            if await self._r.zrem(self._k("jobs"), job_id):
                raw = await self._r.getdel(self._k("job", job_id))
                if raw:
                    out.append(Job.model_validate_json(raw))
        return out

    async def close(self) -> None:
        await self._r.aclose()
