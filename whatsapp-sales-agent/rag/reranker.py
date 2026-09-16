"""Result reranking. LLM listwise reranker; falls back to hybrid order if the model call fails."""

from __future__ import annotations

import logging
from typing import Protocol

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from agent.prompts import RERANK_PROMPT
from agent.state import RetrievedChunk

log = logging.getLogger("reranker")


class Reranker(Protocol):
    async def rerank(self, query: str, candidates: list[RetrievedChunk], top_n: int) -> list[RetrievedChunk]: ...


class _Ranked(BaseModel):
    index: int
    relevance: float = Field(ge=0.0, le=1.0)


class _Ranking(BaseModel):
    ranking: list[_Ranked]


class PassthroughReranker:
    async def rerank(self, query: str, candidates: list[RetrievedChunk], top_n: int) -> list[RetrievedChunk]:
        return candidates[:top_n]


class LLMReranker:
    def __init__(self, runnable):
        self._runnable = runnable  # chat_model.with_structured_output(_Ranking)

    async def rerank(self, query: str, candidates: list[RetrievedChunk], top_n: int) -> list[RetrievedChunk]:
        if len(candidates) <= 1:
            return candidates
        listing = "\n\n".join(f"[{i}] {c.headers}\n{c.content[:1200]}" for i, c in enumerate(candidates))
        try:
            result: _Ranking = await self._runnable.ainvoke(
                [SystemMessage(RERANK_PROMPT), HumanMessage(f"Query: {query}\n\nCandidates:\n{listing}")]
            )
        except Exception as e:
            log.error("rerank.fail err=%s — using hybrid order", e)
            return candidates[:top_n]
        out: list[RetrievedChunk] = []
        seen: set[int] = set()
        for r in result.ranking:
            if 0 <= r.index < len(candidates) and r.index not in seen:
                seen.add(r.index)
                out.append(candidates[r.index].model_copy(update={"score": r.relevance}))
        return out[:top_n]
