"""Against real Weaviate and Redis (docker compose up -d). Skipped when they aren't running.

Embeddings and contexts are faked so no OpenAI call is made; everything else — collection schema,
batch insert, hybrid query with rank fusion, Redis store, Redis checkpointer — is the real code path.
"""

from __future__ import annotations

import contextlib
import hashlib
import math
import os
import re
import socket
import uuid

import pytest

from config import Settings
from rag.ingest import ingest
from rag.reranker import PassthroughReranker
from rag.retriever import HybridRetriever
from storage import Contact, Job, RedisStore
from tests.fakes import Harness, settings

WEAVIATE = ("localhost", 8088)
REDIS_URL = os.environ.get("TEST_REDIS_URL", "redis://localhost:6390/0")


def _up(host: str, port: int) -> bool:
    with contextlib.closing(socket.socket()) as s:
        s.settimeout(0.3)
        return s.connect_ex((host, port)) == 0


needs_weaviate = pytest.mark.skipif(not _up(*WEAVIATE), reason="weaviate not running (docker compose up -d)")
needs_redis = pytest.mark.skipif(not _up("localhost", 6390), reason="redis not running (docker compose up -d)")


class HashEmbedder:
    """Bag-of-words hashed into 256 dims: similar text → similar vectors, deterministic, offline."""

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * 256
        for w in re.findall(r"\w+", text.lower()):
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 256] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]

    async def aembed_documents(self, texts):
        return [self._vec(t) for t in texts]

    async def aembed_query(self, text):
        return self._vec(text)


class StubContext:
    async def situate(self, document: str, chunk: str) -> str:
        title = document.splitlines()[0].lstrip("# ")
        return f"This chunk is from the {title} document."


@needs_weaviate
async def test_ingest_and_hybrid_search_on_real_weaviate(tmp_path):
    import weaviate

    (tmp_path / "growth.md").write_text(
        "# Growth Plan\n## Pricing\n| Plan | Price |\n|---|---|\n| Growth | 900 SAR per month |\n\n## Integrations\nConnects to HIS systems over a REST API.\n",
        encoding="utf-8",
    )
    (tmp_path / "support.md").write_text("# Support\n## Hours\nSupport is available Sunday to Thursday, 8am to 5pm.\n", encoding="utf-8")
    name = f"TestChunk_{uuid.uuid4().hex[:8]}"
    s: Settings = settings(knowledge_base_dir=str(tmp_path), weaviate_collection=name, chunk_size_tokens=128, chunk_overlap_tokens=0)
    client = weaviate.connect_to_local(host=WEAVIATE[0], port=WEAVIATE[1], grpc_port=50061)
    try:
        n = await ingest(s, client=client, embedder=HashEmbedder(), writer=StubContext())
        assert n == 3
        # idempotent: a second run replaces, never duplicates
        assert await ingest(s, client=client, embedder=HashEmbedder(), writer=StubContext()) == 3
        assert client.collections.get(name).aggregate.over_all(total_count=True).total_count == 3

        retriever = HybridRetriever(client=client, collection=name, embedder=HashEmbedder(), reranker=PassthroughReranker(), alpha=0.5, top_k=10, top_n=2)
        hits = await retriever.search("how much is the growth plan price")
        assert hits and hits[0].source == "growth.md" and "900 SAR" in hits[0].content
        assert hits[0].headers == "Growth Plan › Pricing"

        # contextual BM25: "Support document" only exists in the prepended context, not the chunk text
        ctx_hits = await retriever.search("support document")
        assert ctx_hits[0].source == "support.md"

        # A file removed from the knowledge base stops being searchable after re-ingest.
        (tmp_path / "support.md").unlink()
        assert await ingest(s, client=client, embedder=HashEmbedder(), writer=StubContext()) == 2
        remaining = client.collections.get(name).query.fetch_objects(limit=10).objects
        assert {o.properties["source"] for o in remaining} == {"growth.md"}
    finally:
        client.collections.delete(name)
        client.close()


@needs_redis
async def test_redis_store_roundtrip_and_single_claim():
    store = RedisStore(REDIS_URL, retention_days=1, prefix=f"test{uuid.uuid4().hex[:6]}")
    try:
        c = Contact(phone="966500000001", opted_out=True, tier="WARM")
        await store.save_contact(c)
        assert (await store.get_contact(c.phone)).opted_out
        assert await store.mark_seen("m1") and not await store.mark_seen("m1")
        await store.schedule(Job(job_id="drip:1", kind="drip", phone="1", due_at=10))
        await store.schedule(Job(job_id="drip:2", kind="drip", phone="2", due_at=10**12))
        assert [j.job_id for j in await store.due_jobs(100)] == ["drip:1"]
        assert await store.due_jobs(100) == []
        await store.save_escalation("e1", {"priority": "P0"})
        assert (await store.get_escalation("e1"))["priority"] == "P0"
    finally:
        await store.close()


@needs_redis
async def test_conversation_state_survives_restart_in_redis():
    from langgraph.checkpoint.redis.aio import AsyncRedisSaver

    from agent.state import checkpoint_serde

    phone = f"9665{uuid.uuid4().int % 10**8:08d}"
    store = RedisStore(REDIS_URL, retention_days=1, prefix=f"test{uuid.uuid4().hex[:6]}")
    try:
        async with AsyncRedisSaver.from_conn_string(REDIS_URL) as saver:
            saver.serde = checkpoint_serde(redis=True)
            await saver.asetup()
            first = Harness(checkpointer=saver, store=store)
            await first.say(phone, "we struggle with manual claims")
            await first.say(phone, "what is the pricing for the growth plan?")

        # A new process: fresh saver connection, fresh graph, same Redis.
        async with AsyncRedisSaver.from_conn_string(REDIS_URL) as saver2:
            saver2.serde = checkpoint_serde(redis=True)
            second = Harness(checkpointer=saver2, store=store)
            second._n = 100
            values = await second.state(phone)
            assert len(values["messages"]) == 4
            assert values["lead_score"].tier == "WARM"
            assert values["retrieved"][0].source == "pricing.md"
            assert (await second.say(phone, "thanks")).startswith("replied")
            assert len((await second.state(phone))["messages"]) == 6
    finally:
        await store.close()
