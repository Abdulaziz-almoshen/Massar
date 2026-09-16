"""FastAPI app entry point.

Run: `uv run uvicorn main:app --port 8000`
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import time
from dataclasses import dataclass

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from agent.state import AgentReply, BantSignals, IntentResult, checkpoint_serde
from config import Settings, get_settings
from storage import MemoryStore, RedisStore, Store
from tools.escalation import Notifier, OpenAIActionsWriter, _Actions
import re

from webhook.handler import InboundProcessor, is_opt_out
from webhook.outbound import SendGate
from webhook.verification import verify_signature, verify_subscription, verify_token
from webhook.whatsapp import CloudApiProvider, GupshupProvider, InboundMessage, parse_cloud_api, parse_gupshup

log = logging.getLogger("main")


@dataclass
class App:
    settings: Settings
    store: Store
    gate: SendGate
    notifier: Notifier
    processor: InboundProcessor
    graph: object | None = None
    weaviate_client: object | None = None


def build_provider(s: Settings):
    if s.whatsapp_provider == "gupshup":
        return GupshupProvider(api_key=s.gupshup_api_key, app_name=s.gupshup_app_name, source=s.gupshup_source_number)
    return CloudApiProvider(token=s.wa_access_token, phone_number_id=s.wa_phone_number_id, graph_version=s.wa_graph_version)


async def build_runtime(s: Settings, stack: contextlib.AsyncExitStack) -> App:
    """Production wiring: OpenAI models, Weaviate retriever, Redis (or memory) state."""
    import weaviate
    from langgraph.checkpoint.memory import InMemorySaver

    from agent.llm import embeddings, structured
    from agent.nodes import Deps, OpenAIClassifier, OpenAIResponder
    from agent.orchestrator import build_graph
    from rag.reranker import LLMReranker, _Ranking
    from rag.retriever import HybridRetriever
    from tools.crm_update import make_update_crm_tool
    from tools.escalation import make_escalate_tool
    from tools.lead_scorer import OpenAISignalExtractor, make_score_lead_tool
    from tools.product_search import make_search_products_tool

    store: Store
    if s.redis_url:
        from langgraph.checkpoint.redis.aio import AsyncRedisSaver

        store = RedisStore(s.redis_url, s.data_retention_days)
        checkpointer = await stack.enter_async_context(
            AsyncRedisSaver.from_conn_string(s.redis_url, ttl={"default_ttl": s.data_retention_days * 24 * 60})
        )
        checkpointer.serde = checkpoint_serde(redis=True)
        await checkpointer.asetup()
    else:
        log.warning("REDIS_URL unset — conversation state is in memory and lost on restart")
        store = MemoryStore()
        checkpointer = InMemorySaver(serde=checkpoint_serde())

    client = weaviate.connect_to_local(host=s.weaviate_host, port=s.weaviate_port, grpc_port=s.weaviate_grpc_port)
    stack.callback(client.close)
    retriever = HybridRetriever(
        client=client,
        collection=s.weaviate_collection,
        embedder=embeddings(s),
        reranker=LLMReranker(structured(s, _Ranking)),
        alpha=s.hybrid_alpha,
        top_k=s.retrieve_top_k,
        top_n=s.rerank_top_n,
    )
    notifier = Notifier(crm_url=s.crm_webhook_url, slack_url=s.slack_webhook_url, teams_url=s.teams_webhook_url)
    actions_writer = OpenAIActionsWriter(structured(s, _Actions))
    tools = {
        "search_products": make_search_products_tool(retriever),
        "score_lead": make_score_lead_tool(OpenAISignalExtractor(structured(s, BantSignals)), s.scoring_weights, s.thresholds),
        "escalate_to_human": make_escalate_tool(notifier, actions_writer),
        "update_crm": make_update_crm_tool(notifier),
    }
    deps = Deps(
        settings=s,
        classifier=OpenAIClassifier(structured(s, IntentResult), s.company_name),
        responder=OpenAIResponder(structured(s, AgentReply)),
        tools=tools,
        notifier=notifier,
        actions_writer=actions_writer,
        store=store,
    )
    graph = build_graph(deps, checkpointer=checkpointer)
    gate = SendGate(s, build_provider(s))
    processor = InboundProcessor(store=store, gate=gate, graph=graph, notifier=notifier)
    return App(settings=s, store=store, gate=gate, notifier=notifier, processor=processor, graph=graph, weaviate_client=client)


def create_app(runtime_factory=build_runtime, settings: Settings | None = None, start_worker: bool = True) -> FastAPI:
    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        s = settings or get_settings()
        async with contextlib.AsyncExitStack() as stack:
            rt: App = await runtime_factory(s, stack)
            app.state.rt = rt
            task = None
            if start_worker:
                from tools.nurture import worker

                task = asyncio.create_task(worker(settings=s, store=rt.store, gate=rt.gate, notifier=rt.notifier))
            try:
                yield
            finally:
                if task:
                    task.cancel()
                await rt.store.close()

    app = FastAPI(title="WhatsApp AI Sales Agent", lifespan=lifespan)

    def rt(request: Request) -> App:
        return request.app.state.rt

    async def accept(runtime: App, messages: list[InboundMessage], background: BackgroundTasks) -> dict:
        # Opt-outs are handled before the 200: if storing one fails the provider gets a 500 and
        # redelivers, instead of the «إيقاف» vanishing behind an acknowledgement.
        rest = []
        for m in messages:
            if is_opt_out(m.text):
                try:
                    await runtime.processor.handle(m)
                except Exception as e:
                    log.exception("opt_out.fail phone=%s id=%s", m.phone, m.message_id)
                    raise HTTPException(500, "opt-out not stored, retry") from e
            else:
                rest.append(m)
        background.add_task(process, runtime, rest)
        return {"received": len(messages)}

    async def process(runtime: App, messages: list[InboundMessage]) -> None:
        for m in messages:
            try:
                outcome = await runtime.processor.handle(m)
                log.info("inbound phone=%s id=%s outcome=%s", m.phone, m.message_id, outcome)
            except Exception:
                log.exception("inbound.fail phone=%s id=%s", m.phone, m.message_id)

    @app.get("/health")
    async def health(runtime: App = Depends(rt)):
        s = runtime.settings
        return {
            "ok": True,
            "provider": s.whatsapp_provider,
            "send_enabled": s.whatsapp_send_enabled,
            "allowlist_size": len(s.allowlist),
            "state": "redis" if s.redis_url else "memory",
        }

    @app.get("/webhook/whatsapp")
    async def verify(
        runtime: App = Depends(rt),
        mode: str | None = Query(None, alias="hub.mode"),
        token: str | None = Query(None, alias="hub.verify_token"),
        challenge: str | None = Query(None, alias="hub.challenge"),
    ):
        echo = verify_subscription(mode, token, challenge, runtime.settings.wa_verify_token)
        if echo is None:
            raise HTTPException(403, "verification failed")
        return PlainTextResponse(echo)

    @app.post("/webhook/whatsapp")
    async def whatsapp_webhook(
        request: Request,
        background: BackgroundTasks,
        runtime: App = Depends(rt),
        x_hub_signature_256: str | None = Header(None),
    ):
        body = await request.body()
        if not verify_signature(body, x_hub_signature_256, runtime.settings.wa_app_secret):
            raise HTTPException(401, "invalid signature")
        # Parse BEFORE acknowledging: a body we cannot read must fail loudly, not vanish behind a 200.
        try:
            messages = parse_cloud_api(json.loads(body))
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(400, f"unparseable payload: {e}") from e
        return await accept(runtime, messages, background)

    @app.post("/webhook/gupshup")
    async def gupshup_webhook(
        request: Request,
        background: BackgroundTasks,
        runtime: App = Depends(rt),
        token: str | None = Query(None),
        x_webhook_token: str | None = Header(None),
    ):
        if not verify_token(x_webhook_token or token, runtime.settings.gupshup_webhook_token):
            raise HTTPException(401, "invalid token")
        try:
            messages = parse_gupshup(await request.json())
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(400, f"unparseable payload: {e}") from e
        return await accept(runtime, messages, background)

    def admin(runtime: App = Depends(rt), authorization: str | None = Header(None)) -> App:
        provided = (authorization or "").removeprefix("Bearer ").strip() or None
        if not verify_token(provided, runtime.settings.admin_token):
            raise HTTPException(401, "admin token required")
        return runtime

    @app.post("/escalations/{escalation_id}/ack")
    async def ack(escalation_id: str, runtime: App = Depends(admin)):
        card = await runtime.store.get_escalation(escalation_id)
        if not card:
            raise HTTPException(404, "unknown escalation")
        card.setdefault("acknowledged_at", time.time())
        await runtime.store.save_escalation(escalation_id, card)
        await runtime.store.cancel(f"sla:{escalation_id}")
        return {"acknowledged_at": card["acknowledged_at"], "within_sla": card["acknowledged_at"] <= card["sla_deadline"]}

    @app.post("/conversations/{phone}/release")
    async def release(phone: str, runtime: App = Depends(admin)):
        phone = re.sub(r"\D", "", phone)  # the Slack card prints "+966…"
        contact = await runtime.store.get_contact(phone)
        if not contact.last_inbound_at:
            raise HTTPException(404, "unknown contact")
        if contact.active_escalation_id:
            await runtime.store.cancel(f"sla:{contact.active_escalation_id}")
        contact.human_active = False
        contact.active_escalation_id = ""
        await runtime.store.save_contact(contact)
        config = {"configurable": {"thread_id": phone}}
        if runtime.graph is not None and (await runtime.graph.aget_state(config)).values:
            # Without this the graph still believes it escalated and would never escalate this contact again.
            await runtime.graph.aupdate_state(config, {"escalated": False}, as_node="generate_response")
        return {"phone": phone, "human_active": False}

    return app


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = create_app()
