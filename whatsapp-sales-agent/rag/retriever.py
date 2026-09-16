"""Hybrid search (vector + BM25) with rank fusion, then rerank."""

from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from agent.state import RetrievedChunk
from rag.reranker import Reranker

log = logging.getLogger("retriever")


class Retriever(Protocol):
    async def search(self, query: str) -> list[RetrievedChunk]: ...


class HybridRetriever:
    def __init__(self, *, client, collection: str, embedder, reranker: Reranker, alpha: float, top_k: int, top_n: int):
        self._client = client
        self._collection = collection
        self._embedder = embedder
        self._reranker = reranker
        self._alpha, self._top_k, self._top_n = alpha, top_k, top_n

    async def search(self, query: str) -> list[RetrievedChunk]:
        from weaviate.classes.query import HybridFusion, MetadataQuery

        if not query.strip():
            return []
        vector = await self._embedder.aembed_query(query)
        collection = self._client.collections.get(self._collection)

        def _query():
            return collection.query.hybrid(
                query=query,
                vector=vector,
                alpha=self._alpha,
                query_properties=["contextualized"],
                fusion_type=HybridFusion.RANKED,
                limit=self._top_k,
                return_metadata=MetadataQuery(score=True),
            )

        result = await asyncio.to_thread(_query)
        candidates = [
            RetrievedChunk(
                chunk_id=str(o.properties.get("chunk_id", o.uuid)),
                source=str(o.properties.get("source", "")),
                headers=str(o.properties.get("headers", "")),
                content=str(o.properties.get("content", "")),
                score=float(o.metadata.score or 0.0),
            )
            for o in result.objects
        ]
        return await self._reranker.rerank(query, candidates, self._top_n)
