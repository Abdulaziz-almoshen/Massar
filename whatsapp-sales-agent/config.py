"""Environment vars, scoring weights, thresholds.

Weights and thresholds are the blueprint's Table 3 values verbatim. They are overridable from the
environment (SCORING_WEIGHTS / THRESHOLDS as JSON) because the blueprint calls them "configurable
thresholds", but the defaults below are the spec.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SCORING_WEIGHTS = {
    "budget_match": 3,
    "timeline_urgency": 2,
    "pain_point_clarity": 2,
    "decision_maker_authority": 2,
    "engagement_velocity": 1.5,
    "question_depth": 1,
}

THRESHOLDS = {
    "HOT": 8,  # Immediate escalation
    "WARM": 5,  # Nurture sequence
    "COLD": 0,  # Self-service
}

ESCALATION_SLA_SECONDS = 45  # Max wait before abandonment spikes

# Table 4: per-priority SLA. P0 < 30s, P1 < 45s, P2 < 2 min.
PRIORITY_SLA_SECONDS = {"P0": 30, "P1": ESCALATION_SLA_SECONDS, "P2": 120}

# WARM leads get a 48-hour re-engagement; COLD leads enter a long-term drip.
WARM_REENGAGE_SECONDS = 48 * 60 * 60
COLD_DRIP_SECONDS = 14 * 24 * 60 * 60

# WhatsApp customer service window.
SERVICE_WINDOW_SECONDS = 24 * 60 * 60


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- persona
    agent_name: str = "Sara"
    company_name: str = "Lean"

    # --- LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-terra"
    # gpt-5.6-terra rejects tool/structured calls on chat.completions unless reasoning is "none"
    # (verified live in massar-engine, Aug 10 2026). Empty string = don't send the parameter.
    openai_reasoning_effort: str = "none"
    embedding_model: str = "text-embedding-3-small"

    # --- RAG
    knowledge_base_dir: str = "knowledge_base"
    weaviate_host: str = "localhost"
    weaviate_port: int = 8088
    weaviate_grpc_port: int = 50061
    weaviate_collection: str = "ProductChunk"
    chunk_size_tokens: int = 512
    chunk_overlap_tokens: int = 64
    hybrid_alpha: float = 0.5  # 0 = pure BM25, 1 = pure vector
    retrieve_top_k: int = 20
    rerank_top_n: int = 5
    contextual_retrieval: bool = True

    # --- state
    redis_url: str = ""  # empty = in-memory checkpointer and store (tests, local dev)

    # --- scoring (JSON overrides; defaults are the module constants above)
    scoring_weights: dict[str, float] = Field(default_factory=lambda: dict(SCORING_WEIGHTS))
    thresholds: dict[str, float] = Field(default_factory=lambda: dict(THRESHOLDS))

    # --- messaging provider: "cloud_api" (Meta WhatsApp Cloud API) or "gupshup"
    whatsapp_provider: str = "cloud_api"
    wa_access_token: str = ""
    wa_phone_number_id: str = ""
    wa_app_secret: str = ""  # X-Hub-Signature-256 verification
    wa_verify_token: str = ""  # GET hub.verify_token handshake
    wa_graph_version: str = "v21.0"
    gupshup_api_key: str = ""
    gupshup_app_name: str = ""
    gupshup_source_number: str = ""
    gupshup_webhook_token: str = ""
    reengage_template_name: str = ""  # approved template for WARM re-engagement
    reengage_template_language: str = "ar"
    drip_template_name: str = ""  # approved template for COLD drip

    # --- send safety. Outbound is OFF unless explicitly enabled, and even then only to the
    # allowlist unless allow_all_recipients is set. A dry-run send is logged, never delivered.
    whatsapp_send_enabled: bool = False
    send_allowlist: str = ""  # comma-separated E.164 digits
    allow_all_recipients: bool = False

    # --- escalation / CRM
    crm_webhook_url: str = ""
    slack_webhook_url: str = ""
    teams_webhook_url: str = ""

    # --- admin
    admin_token: str = ""

    # --- PDPL: data minimisation
    data_retention_days: int = 90

    @model_validator(mode="after")
    def _scoring_config_complete(self) -> "Settings":
        # A partial override would otherwise fail silently: a missing weight scores 0, a missing
        # threshold raises inside scoring and every lead stays COLD forever.
        if set(self.scoring_weights) != set(SCORING_WEIGHTS):
            raise ValueError(f"SCORING_WEIGHTS must have exactly the keys {sorted(SCORING_WEIGHTS)}")
        if set(self.thresholds) != set(THRESHOLDS) or not self.thresholds["HOT"] > self.thresholds["WARM"] >= self.thresholds["COLD"]:
            raise ValueError("THRESHOLDS must have HOT > WARM >= COLD")
        return self

    @property
    def allowlist(self) -> set[str]:
        return {"".join(ch for ch in p if ch.isdigit()) for p in self.send_allowlist.split(",") if p.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
