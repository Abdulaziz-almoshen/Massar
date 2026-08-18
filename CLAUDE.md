# Massar (مَسار) — Agent System Memory

> Read this file first, every cycle. Working state lives in `.orbit/STATE.md`.
> Update both after significant work (see "Maintenance").

## 1. Project Overview & Goals
Massar is Lean's Arabic-first, RTL sales-management platform. The live initiative is the
**WhatsApp AI campaign MVP**: launch template campaigns via Gupshup, let an Arabic AI
salesperson hold each conversation, track every contact (delivered/seen/replied/interest
tags), and retarget. The design prototype in `_مسار/مسار.dc.html` is the product spec; the
deployed engine lives in `massar-engine/`; the architecture doc is
https://claude.ai/code/artifact/11645969-2dcd-4515-8fba-5f00c3b48abd .

Goals, in priority order:
1. Production-ready campaign engine (Postgres ledger → outbox/pacer → campaign wizard API).
2. Arabic agent quality + safety (grounded on approved KB, opt-out sacred, human handoff).
3. Massar dashboard (Next.js, RTL) implementing the prototype's marketing screens.
4. Protect the WhatsApp number: quality rating, frequency caps, consent — never burn it.

## 2. Current State — pointer
Live state: **`.orbit/STATE.md`** (read after this file).
Last major milestone: **account graph deployed (Aug 18, 2026)** — the agent no longer interviews
every prospect. Prospect facts moved from a never-set env blob to `entities.facts` with provenance
(`src/facts.ts`); imports, operators and the customer's own answers all write through one door; the
prompt gained a named, ask-ordered gap list so a fact learned once is never asked again. Coverage is
honest and currently near zero — the next real gain is an audience re-import carrying HIS/ERP
columns. Next slices: portal fact editing, pre-launch enrichment, HIS/ERP vendor registry, KB
retrieval (decks are still concatenated into every prompt).

## 3. Success Criteria & Evaluation Metrics
- Build: `npm run build` in `massar-engine/` exits 0 (strict TS). After any deploy,
  `GET https://massar-engine.fly.dev/health` returns `ok: true` and `outbound.ok: true`.
- Quality: Reviewer rubric ≥ 8/10 on the diff; QA delivery-evidence gate PASS for any UI
  or user-flow change.
- Safety (booleans, all must hold): no outbound WhatsApp to real customers without a human
  approval; «إيقاف»/STOP path verified when agent code changes; webhook token auth intact;
  no secret in git.
- Agent output: Arabic (clear MSA), ≤ 4 lines per message, one question max, grounded only
  in the approved KB — spot-check one transcript whenever agent code/prompt changes.
- Completeness: the increment ends with deployed health green and STATE.md updated.

## 4. Tech Stack & Conventions
- TypeScript / Node 22, Fastify, npm, ESM (NodeNext). Strict tsc; no `any` unless quoted.
- LLM: OpenAI via adapter — `OPENAI_MODEL=gpt-5.6-terra` (conversation), auto-pick fallback.
- WhatsApp: Gupshup BSP. Current app: **sandbox** `Massar`, source `917834811114` (India
  sandbox number; recipients must opt in by messaging it first). Production WABA number is a
  planned migration. `src/gupshup.ts` is the ONLY file that knows the wire format (v1 send,
  v2 + v3/Meta webhooks).
- Deploy: Fly.io app `massar-engine` (fra, 1 machine, always-on). **`npm run deploy`** —
  `npm run check` (catalogue + numerals) then `fly deploy --ha=false && npm run smoke`. Smoke loads seven real routes in a browser
  and fails on a blank render; a deploy is not done until it exits 0. Never run the bare
  `fly deploy` and call it finished.
- **`src/dashboard.ts`: anchored string replacements only, never range edits** — a deleted
  helper is invisible to `tsc` and `node --check` and ships a blank page.
  See `.orbit/decisions/0001-dashboard-no-range-edits.md`.
- Secrets: `massar-engine/.env` (gitignored) + `fly secrets` — OPENAI_API_KEY,
  GUPSHUP_API_KEY, GUPSHUP_APP_ID, GUPSHUP_APP_NAME, GUPSHUP_SOURCE_NUMBER, WEBHOOK_TOKEN,
  ADMIN_TOKEN. Never commit; never echo values into chat/logs.
- Hard rules live in code (opt-out, turn caps, window checks) — never only in prompts.

## 5. Instructions for All Agents
- Work in small, verifiable steps; read `STATE.md` before acting, write it after.
- **NO WHATSAPP SEND, TO ANY NUMBER, FOR ANY REASON.** Standing instruction, Aug 12 2026:
  *"Don't ever send a text to the client for any test or anything… I will tell you what number
  you should test with."* This revokes the earlier "sandbox self-tests to the team's own opted-in
  phones are fine" allowance and every previously approved number. Verify agent behaviour by unit
  test and by reading existing transcripts; if a claim can only be proven by sending, leave it
  unproven and say so. Lifted only when the user names an explicit allowlist.
- Treat Gupshup/OpenAI/Fly as reliable tools; don't reinvent; keep the adapter seam clean.
- Never take an irreversible, financial, or outward-facing action autonomously; propose it.
- Stay within §8. Announce yourself (`[role] …`), emit to `.orbit/activity.jsonl`, keep the
  checklist current (TaskCreate/TaskUpdate + `.orbit/tasks.json`).

## 6. Sub-Agent Roster  (specs in `.orbit/roles/`, adapters in `.claude/agents/`)
- dispatcher — classifies each message (task/question) per §10; routes.
- orchestrator — conducts the loop, owns STATE.md.
- advisor — (on demand) read-only senior judgment for hard forks.
- product-discovery · business-analyst · market-researcher · planner — the substantial-lane
  planning chain (convened for real bets, folded into orchestrator for small work).
- backend-engineer — massar-engine: gateway, agent runtime, tracker, Postgres/queues.
- frontend-engineer — the Next.js RTL dashboard (prototype screens → real UI).
- designer — UI surfaces only; guards the Massar design language (see skills).
- reviewer — technical quality gate on the diff (≥ 8/10 to pass).
- qa-engineer — scenario/dependency/pixel evidence; runs the delivery-quality gate.
- safety-gate — veto power; §8 is its charter.
- cpo — final acceptance against the reviewed evidence.
- reporter — decision-ready summaries.
- watchdog — background drift/health checks.

## 7. Skills Index  (`.orbit/skills/`)
- `whatsapp-campaign-engineering.md` — **the core domain skill**: engine layout, Gupshup
  wire shapes (send/webhook v2+v3), WhatsApp platform rules, agent tool contract, ops
  runbook (deploy/secrets/test curls), sandbox specifics. Load for any engine work.
- `massar-design-language.md` — RTL/Arabic design system from the prototype (palette,
  type, component idioms, screen map). Load for any dashboard/UI work.
- Library playbooks (provisioned): `loop-tiers.md` (gearbox), `technical-review.md`,
  `qa-validation.md`, `safety-rules.md`, `product-discovery.md`,
  `market-and-competitive-research.md`, `planning-and-decision-briefs.md`,
  `architecture-decisions.md`, `active-learning.md`, design playbooks (methodology,
  anti-ai-aesthetics, styles, taste-preflight, design-taste-frontend).

## 8. Stop Conditions & Safety Rules  ← the most important section
Hard limits (enforced by `.orbit/loop.config.json`):
- Max iterations per run: 6. Cost budget: $1.00/cycle, $5.00/run. Max runtime: 45 min.
- Gate-failure streak: 2 consecutive failures → hard stop.
Eval gates: build green · reviewer ≥ 8/10 · QA evidence PASS (UI/flows) · safety checks pass.
Human-approval checkpoints (loop pauses):
- **Any WhatsApp message to a real customer** (template blast or session send outside
  team test numbers). Any template submission to Meta. Any data deletion. Any spend > $5.
  (`fly deploy` of massar-engine is pre-authorized by the user's standing instruction of
  Aug 10, 2026 — "once done, just deploy it and fly"; revert to human-gated anytime.)
- FORBIDDEN outright: moving money; `fly apps destroy`; unsetting secrets; disabling the
  opt-out path or webhook token auth.
Explicit done: the run goal in STATE.md is met, or a cap trips.
The system never takes an irreversible, financial, or outward-facing action on its own.

## 9. Loop Structure
read `CLAUDE.md` + `STATE.md` → plan → act via sub-agent(s) → evaluate vs §3 → update
STATE.md → decide (continue / spawn / STOP). Runners: `.orbit/loop.py` (portable; dispatch
seam unwired) or `scripts/ralph_loop.sh` (Claude Code). Config: §8 / `loop.config.json`.

## 10. Request Routing — the Gearbox  (read on EVERY user message)
Pick the **smallest gear that can still PROVE the result** (rubric: `.orbit/skills/loop-tiers.md`;
scorecard: ambiguity · blast radius · surfaces · research · compliance · reversibility · cost;
highest trigger wins). Declare the gear before moving. Lite cost-mode: run
`scripts/orbit-context doctor` before T2+.
- **T0 · Direct** — question/status ("is the engine live?", "what's the reply rate?") → answer.
- **T1 · Quick** — small · clear · reversible (a copy tweak, a log line) → just do it well;
  one STATE.md line. Small UI edits don't wake the Designer.
- **T2 · Standard** — a real change, one workstream (a new endpoint, a tracker field) →
  plan/build with one active specialist at a time; tiny packets (≤ 8 files, ≤ 500 words out).
- **T3 · Deep** — multi-surface / ambiguous / compliance-heavy (the Postgres migration, the
  campaign wizard, production-number migration) → Map → Research → Plan → Critique → Build,
  capped by `gears.deep`.
- **T4 · Mission** — days-long / production migration / real-customer sends at scale → the
  durable runner with a human gate per irreversible step.
Massar examples: "أطلق الحملة على 50 عيادة" → T2/T3 **+ mandatory human approval** (outbound).
"صمّم شاشة المتابعة" → T3 with Designer. "غيّر نبرة المساعد" → T2 + agent spot-check (§3).
Every gear T1+ runs on the visible board (`set_team` + `set_tasks` + TaskCreate) — never the
background `Workflow(...)` runner. Guardrails scale with the gear.
**Router ↔ Dispatcher:** `.orbit/checks/route.py` injects a deterministic lane every message —
take it unless concretely wrong; override with one stated line. The §8 guard is a hard wall in
every lane. Questions to the user: only critical blockers, always one batched
`AskUserQuestion` with the recommendation first.

## 11. Active learning
In UPDATE (and after any user correction) run `.orbit/skills/active-learning.md` silently;
promote only clear-bar learnings (user-stated rules → here; techniques → the domain skill;
dated choices → STATE.md). Surface one quiet `📝 Learned:` line when it happens.

## Maintenance
Update §2's milestone line + STATE.md every cycle. §3/§4/§6/§7/§8 only on durable change.
Keep this file readable in one glance.
