"""Markdown chunking + contextual retrieval + embedding pipeline.

Three-stage chunking: header split (H1/H2/H3) → tables kept atomic → recursive split of prose at
the configured token size. Each chunk then gets an LLM-written 50–100 token situating context
(Anthropic Contextual Retrieval); the context is prepended before BOTH embedding and BM25 indexing.

Run: `uv run python -m rag.ingest`
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Sequence

from langchain_core.messages import HumanMessage
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from agent.prompts import CONTEXTUAL_CHUNK_PROMPT
from config import Settings, get_settings

log = logging.getLogger("ingest")

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
_HEADING = re.compile(r"^\s*#{1,6}\s")


@dataclass
class Chunk:
    chunk_id: str
    source: str
    headers: str
    content: str
    is_table: bool = False
    context: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def contextualized(self) -> str:
        return f"{self.context}\n\n{self.content}" if self.context else self.content


def split_tables(text: str) -> list[tuple[str, bool]]:
    """Split a section into (block, is_table) runs so a pricing table is never cut in half."""
    blocks: list[tuple[str, bool]] = []
    buf: list[str] = []
    in_table = False
    for line in text.splitlines():
        row = bool(_TABLE_ROW.match(line))
        if row != in_table and buf:
            blocks.append(("\n".join(buf).strip(), in_table))
            buf = []
        in_table = row
        buf.append(line)
    if buf:
        blocks.append(("\n".join(buf).strip(), in_table))
    blocks = [(b, t) for b, t in blocks if b]
    # A run that is only heading lines ("## Pricing" right above a table) is not a chunk: fold it
    # into the block that follows, or drop it when nothing follows (the headers are in metadata).
    merged: list[tuple[str, bool]] = []
    carry = ""
    for b, t in blocks:
        if not t and all(_HEADING.match(line) or not line.strip() for line in b.splitlines()):
            carry = f"{carry}\n{b}".strip()
            continue
        merged.append((f"{carry}\n{b}".strip() if carry else b, t))
        carry = ""
    return merged


def chunk_markdown(text: str, source: str, *, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS, strip_headers=False)
    prose_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks: list[Chunk] = []
    for section in header_splitter.split_text(text):
        headers = " › ".join(section.metadata[k] for k in ("h1", "h2", "h3") if k in section.metadata)
        for block, is_table in split_tables(section.page_content):
            pieces = [block] if is_table else prose_splitter.split_text(block)
            for piece in pieces:
                digest = hashlib.sha1(f"{source}|{headers}|{len(chunks)}|{piece}".encode()).hexdigest()
                chunks.append(Chunk(chunk_id=digest, source=source, headers=headers, content=piece, is_table=is_table))
    return chunks


def load_knowledge_base(directory: str | Path) -> list[tuple[str, str]]:
    root = Path(directory)
    return [(str(p.relative_to(root)), p.read_text(encoding="utf-8")) for p in sorted(root.rglob("*.md")) if p.name.lower() != "readme.md"]


class ContextWriter(Protocol):
    async def situate(self, document: str, chunk: str) -> str: ...


class OpenAIContextWriter:
    def __init__(self, chat):
        self._chat = chat

    async def situate(self, document: str, chunk: str) -> str:
        msg = await self._chat.ainvoke([HumanMessage(CONTEXTUAL_CHUNK_PROMPT.format(document=document, chunk=chunk))])
        return str(msg.content).strip()


async def contextualize(chunks: list[Chunk], documents: dict[str, str], writer: ContextWriter, concurrency: int = 8) -> None:
    sem = asyncio.Semaphore(concurrency)

    async def one(c: Chunk) -> None:
        async with sem:
            try:
                c.context = await writer.situate(documents[c.source], c.content)
            except Exception as e:  # a missing context degrades retrieval, it must not abort ingest
                log.error("contextualize.fail chunk=%s err=%s", c.chunk_id, e)

    await asyncio.gather(*(one(c) for c in chunks))


def ensure_collection(client, name: str):
    from weaviate.classes.config import Configure, DataType, Property, Tokenization

    if client.collections.exists(name):
        return client.collections.get(name)
    return client.collections.create(
        name,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            Property(name="chunk_id", data_type=DataType.TEXT, skip_vectorization=True, index_searchable=False),
            Property(name="source", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
            Property(name="headers", data_type=DataType.TEXT),
            Property(name="content", data_type=DataType.TEXT),
            # contextual BM25 runs on this field
            Property(name="contextualized", data_type=DataType.TEXT),
            Property(name="is_table", data_type=DataType.BOOL),
        ],
    )


async def ingest(settings: Settings, *, client, embedder, writer: ContextWriter | None) -> int:
    docs = load_knowledge_base(settings.knowledge_base_dir)
    if not docs:
        log.warning("ingest: no .md files in %s", settings.knowledge_base_dir)
        return 0
    documents = dict(docs)
    chunks: list[Chunk] = []
    for source, text in docs:
        chunks += chunk_markdown(text, source, chunk_size=settings.chunk_size_tokens, chunk_overlap=settings.chunk_overlap_tokens)
    if settings.contextual_retrieval and writer is not None:
        await contextualize(chunks, documents, writer)
    vectors = await embedder.aembed_documents([c.contextualized for c in chunks])

    collection = ensure_collection(client, settings.weaviate_collection)
    # Full rebuild per source: delete what this run replaces, then insert.
    from weaviate.classes.query import Filter

    for source in documents:
        collection.data.delete_many(where=Filter.by_property("source").equal(source))
    # Files removed from the knowledge base must stop being searchable (a retired price sheet).
    # An EMPTY directory returns earlier without touching the index, so a wrong path cannot wipe it.
    collection.data.delete_many(where=Filter.by_property("source").contains_none(list(documents)))
    with collection.batch.fixed_size(batch_size=100) as batch:
        for c, v in zip(chunks, vectors):
            batch.add_object(
                properties={
                    "chunk_id": c.chunk_id,
                    "source": c.source,
                    "headers": c.headers,
                    "content": c.content,
                    "contextualized": c.contextualized,
                    "is_table": c.is_table,
                },
                vector=v,
                uuid=uuid.UUID(c.chunk_id[:32]),
            )
    failed = collection.batch.failed_objects
    if failed:
        raise RuntimeError(f"weaviate rejected {len(failed)} of {len(chunks)} chunks: {failed[0].message}")
    log.info("ingest: %d chunks from %d files", len(chunks), len(docs))
    return len(chunks)


def main(argv: Sequence[str] | None = None) -> None:
    import weaviate

    from agent.llm import chat_model, embeddings

    logging.basicConfig(level=logging.INFO)
    s = get_settings()
    client = weaviate.connect_to_local(host=s.weaviate_host, port=s.weaviate_port, grpc_port=s.weaviate_grpc_port)
    try:
        n = asyncio.run(ingest(s, client=client, embedder=embeddings(s), writer=OpenAIContextWriter(chat_model(s))))
        print(f"ingested {n} chunks")
    finally:
        client.close()


if __name__ == "__main__":
    main()
