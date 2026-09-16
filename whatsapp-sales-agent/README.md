# WhatsApp AI Sales Agent

Implementation of *AI-Powered WhatsApp Sales Agent: Complete Development Blueprint*: FastAPI webhook,
LangGraph orchestration, hybrid RAG over Markdown (Weaviate + contextual retrieval + rerank), BANT
weighted lead scoring with HOT/WARM/COLD routing, and human handoff with a context card and SLA.

Standalone service. It is **not** connected to massar-engine's live Gupshup webhook.

## Run locally

```bash
docker compose up -d                 # Weaviate :8088, Redis :6390
cp .env.example .env                 # fill OPENAI_API_KEY, provider creds, webhook URLs
uv sync
# put approved product docs in knowledge_base/*.md, then:
uv run python -m rag.ingest
uv run uvicorn main:app --port 8000
uv run pytest -q                     # 106 tests; the Weaviate/Redis ones skip if compose is down
```

Or everything in Docker: `docker compose --profile app up --build`.

## Flow

```
POST /webhook/whatsapp (X-Hub-Signature-256)  or  POST /webhook/gupshup (?token=)
  → parse (400 on bad body, never a silent 200) → dedupe by message id → per-contact lock
  → opt-out in code (STOP / إيقاف …) → rep owns thread? forward to Slack/CRM, agent silent
  → LangGraph: classify_intent → route_to_tool (search_products, score_lead)
               → check_escalation ─ trigger/HOT → escalate_to_human ─┐
                                 ─ WARM → nurture (48h re-engage)   ─┤→ generate_response
                                 ─ COLD → self_service (drip)       ─┘
  → SendGate: kill switch → allowlist → opt-out → 24h window → provider
```

| Blueprint item | Where |
|---|---|
| Weights `3/2/2/2/1.5/1`, thresholds HOT ≥ 8, WARM 5–7 | `config.py`, `tools/lead_scorer.py` |
| Header split → atomic tables → 256–512 token recursive split | `rag/ingest.py` |
| Contextual retrieval (context prepended to embedding and BM25 text) | `rag/ingest.py` |
| Hybrid vector + BM25, rank fusion, rerank | `rag/retriever.py`, `rag/reranker.py` |
| Five-layer system prompt | `agent/prompts.py` |
| Triggers P0 (explicit request, HOT, purchase signal) / P1 (frustration, low confidence, 2+ failures, out-of-KB) / P2 (complex) | `tools/escalation.py` |
| Context card: transcript, intent, sentiment, score, profile, qualifying answers, next actions | `tools/escalation.py` |
| CRM webhook + Slack/Teams alert, SLA re-alert on breach, `POST /escalations/{id}/ack` | `tools/escalation.py`, `tools/nurture.py`, `main.py` |
| 24h window, reply buttons (≤ 3, ≤ 20 bytes), template re-engagement | `webhook/outbound.py`, `webhook/whatsapp.py` |
| Cloud API or Gupshup | `WHATSAPP_PROVIDER` |
| PDPL: opt-out, data retention TTL | `webhook/handler.py`, `storage.py`, `DATA_RETENTION_DAYS` |

## Safety defaults

- `WHATSAPP_SEND_ENABLED=false`: every reply is logged as `dry_run`, nothing is delivered.
- When enabled, only `SEND_ALLOWLIST` numbers receive messages unless `ALLOW_ALL_RECIPIENTS=true`.
- Webhooks fail closed: an unset `WA_APP_SECRET` / `GUPSHUP_WEBHOOK_TOKEN` rejects every request.
- A product question with no retrieved context gets the fixed "I don't have that information…" reply
  and a P1 handoff; no model call composes an answer without context.
- A provider error is recorded as `failed` and never retried (the message may already be delivered).

## Endpoints

| | |
|---|---|
| `GET /health` | provider, send switch, state backend |
| `GET/POST /webhook/whatsapp` | Meta verification handshake / inbound |
| `POST /webhook/gupshup` | Gupshup inbound (v2 or Meta-format v3) |
| `POST /escalations/{id}/ack` | rep picked it up; stops the SLA re-alert (`Authorization: Bearer $ADMIN_TOKEN`) |
| `POST /conversations/{phone}/release` | hand the thread back to the agent (admin) |

## Deploy

`Dockerfile` runs on Railway, Render, Fly, or any container host. `REDIS_URL` must point at
database 0 (the checkpointer's search index refuses others) on Redis 8 or Redis Stack.
