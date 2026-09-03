#!/bin/bash
# Boot a LOCAL massar-engine for QA. Outbound is dead by construction:
#   GUPSHUP_API_KEY / GUPSHUP_SOURCE_NUMBER / GUPSHUP_APP_NAME are forced EMPTY, so
#   gupshup.outboundReady() is false and baseParams() throws before any URL is built;
#   spy.mjs then blocks api.gupshup.io at the fetch layer as a second, independent wall.
#   NOTIFY_NUMBER empty → the lead-alert path cannot send either.
#   OPENAI_API_KEY is a stub string; the real key never enters this process.
set -u
ENG=/Users/abdulaziz/Projects/Massar/massar-engine
H=/Users/abdulaziz/Projects/Massar/docs/artifacts/crm-record/qa/harness
PORT="$1"; shift
DBURL="${1:-}"; shift || true
cd "$ENG"
export PORT
export GUPSHUP_API_KEY="" GUPSHUP_SOURCE_NUMBER="" GUPSHUP_APP_NAME="" GUPSHUP_APP_ID=""
export NOTIFY_NUMBER=""
export OPENAI_API_KEY="sk-qa-stub-not-a-real-key"
export OPENAI_MODEL="gpt-5.6-terra"
export ADMIN_TOKEN="qa-admin-token"
export WEBHOOK_TOKEN="qa-webhook-token"
export QA_SPY_LOG="$H/egress-$PORT.jsonl"
export QA_LLM_SCRIPT="$H/llm-script.json"
export QA_INSIGHTS_JSON="$H/insights.json"
export QA_LLM_TRACE="$H/llm-trace.jsonl"
if [ -n "$DBURL" ]; then export DATABASE_URL="$DBURL"; else unset DATABASE_URL; fi
exec node --import "$H/spy.mjs" dist/index.js
