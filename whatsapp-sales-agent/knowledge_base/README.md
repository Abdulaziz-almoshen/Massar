Put product documentation here as Markdown (`*.md`, any depth). This README is skipped by ingest.

- Use `#`/`##`/`###` headings: they become each chunk's breadcrumb.
- Keep pricing and feature matrices as Markdown tables: a table is never split across chunks.
- Only approved claims. The agent answers product questions from these files and nothing else.

Then run `uv run python -m rag.ingest`. Re-running replaces each file's chunks.
