"""RAG-enhanced product lookup."""

from __future__ import annotations

import logging

from langchain_core.tools import StructuredTool

from agent.state import RetrievedChunk
from rag.retriever import Retriever

log = logging.getLogger("product_search")


async def search_products(retriever: Retriever, query: str) -> list[RetrievedChunk]:
    try:
        return await retriever.search(query)
    except Exception as e:
        # A retrieval outage must surface as "no context", which the agent answers with the
        # honest fallback, never as a crashed turn.
        log.error("search_products.fail err=%s", e)
        return []


def make_search_products_tool(retriever: Retriever) -> StructuredTool:
    async def _search(query: str) -> list[dict]:
        """Search the product knowledge base. Returns cited chunks."""
        return [c.model_dump() for c in await search_products(retriever, query)]

    return StructuredTool.from_function(coroutine=_search, name="search_products")
