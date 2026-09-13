# Massar (مَسار) — Project Memory

> Read this file first. Working state lives in `docs/STATE.md`.
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
3. Massar as the commercial platform between product and sales (design record:
   `docs/designs/massar-commercial-platform.md`, Sep 3 2026). UI stays on `src/dashboard.ts`
   until rep adoption is proven; the separate Next.js dashboard is retired as a goal.
4. Protect the WhatsApp number: quality rating, frequency caps, consent — never burn it.

## 2. Current State — pointer
Live state: **`docs/STATE.md`** (read after this file).
Last major milestone: **the admin layer, and the review round that found a function shadowing another (Sep 13, 2026)** —
two reviewers rejected the products build and the finding that mattered was a class no gate could see: `coveragePct`
was declared by both `product-domain` and `sales-domain`, and the page ran whichever was concatenated last, so every
coverage figure read «—» while the unit test passed. `scripts/check-browser-globals.mjs` is now gate step 24: no
top-level name in the page script may be declared twice. The same round fixed a wizard that silently fell back to the
embedded six products, a phone summary broken by a container query written against another container's name, and an
open-line count that disagreed with its own link. Then the founder's admin layer: «إعدادات النظام» (sales stages the
admin may add/rename/reweight/pause with an SLA — code owns the stage KEY, the admin owns everything else — plus
divisions and a team directory), «تصعيد»/«طلب دعم» on every opportunity (recorded, never sent: no mail sender is
configured), the product record led by the assistant-readiness band, and western numerals everywhere the dashboard
prints a number. Previous: **V5 — «فرص البيع» rebuilt to one grammar (Sep 12, 2026)** — the founder rejected the
opportunities page; it was redesigned from Dribbble/Pinterest references and three design voices, and shipped only
after Claude AND GPT (codex, gpt-6-astra) both approved every criterion against production screenshots and 114
executed browser checks. The reviews caught a global checkbox that drew an X, a toolbar that clipped, and a
selection bar that moved the table; capture caught `/admin/opps` rendering «لا فرص مسجّلة بعد» during a database
blip. Open: massar-db (256MB) keeps failing health checks, and OpenAI credits are exhausted. Previous: **V4 — the Tonomo blue (Sep 8, 2026)** — a third founder-chosen reference
moved the accent to `#2563EB`, but the hue was the smallest part: radii halved, shadows retired for
a hairline, accent surfaces solid rather than gradient, controls compacted. 1,186 value sites, every
ratio measured first. The day's real lesson: the doc-vs-code drift gate built that morning caught
its own author twice, and the second catch exposed a hole in it — a check that compares only shared
keys cannot see a token the doc never mentions. Previous: **V3 — the violet revamp, and two guards that could not fail (Sep 7, 2026)**
— the founder chose two references (Pillio for the overview surfaces, an AI-Manager leads dashboard
for the lists) and the accent moved from Seha blue to violet across **1,164 value sites**, with new
radii, violet-grey shadows and a tinted `--canvas`. Three contrast failures were caught by measuring
before drawing, one of them byte-identical to a failure DESIGN.md had already retired. Delete became
a **hold**, the gesture §8.5 named and nothing implemented. But the finding that mattered was the
guards: `dashboard.ts` returned early without touching `#body`, so `#home` and `#kmon` painted an
empty white page for ~5s; and `smoke.py` asserted landmarks against the whole page, so **six** routes
were matching a string in the nav rail or breadcrumb and were green on a screen that rendered
nothing. Scoping the assertion to `#body` exposed all six in one run. Review and remaining tasks:
`docs/designs/massar-ui-transformation.md`. Previous: **the commercial engine, and the four reviews that caught what it got wrong
(Sep 4, 2026)** — «المستهدفات والأداء» ships on eight weighted stages recovered from Lean's own
archive, over an append-only stage ledger. Four independent reviews followed: security (the first
dedicated one in this project's history — ten findings, including a stored XSS that stole
`ADMIN_TOKEN` from an uploaded spreadsheet cell, proven by attack then defeated), technical, design,
and CEO. The CEO review found the one that mattered: `track_stage_events` **had no writer**, so a
won deal left the open pipeline and never reached «المحقق» — measured, a 1,440,000 SAR deal
vanishing — and every figure was frozen at migration-day values. `scripts/check-ledger-writers.mjs`
is now gate step 18: a table a screen reads must have a writer outside the migrations. Still open
and stated on the screen itself: the target basis (bookings / ACV / TCV) was never decided, and two
of the eight stages are unreachable because `opps-domain.ts` still carries six. Previous: **five live send/receive defects fixed (Sep 4, 2026)** — found by verifying
the platform plan's claims, not by hunting bugs: the webhook accepted every POST when
`WEBHOOK_TOKEN` was unset, it acked before parsing so one throw silently lost every later event
(including an inbound «إيقاف»), a provider timeout delivered the same message twice, `/health`
reported healthy in memory-only mode, and per-recipient launch failures were computed and dropped
by the UI. One shared three-way send-outcome rule now decides resend-vs-mark-vs-retry, locked by
`tests/send-outcome.test.ts`. The plan itself was wrong about the biggest thing: `src/outbound.ts`
IS the send gate, and 13 of 15 call sites bypass it — `scripts/check-optout.mjs` had been printing
that on every build for three weeks. Previous: **«مؤشرات المحادثة» on the client record (Aug 27, 2026)** — the record answers
«how is this conversation going?» with signals instead of prose: a 0–100 seriousness meter, momentum,
reply speed, silence, a 21-day activity chart, and one suggested next action. Every number is earned
from the ledger by `src/signal-domain.ts` (pure, unit-tested) — no model produces a figure on that
card, and «لماذا هذه القراءة؟» itemises each one with its evidence. Previous: **the opportunity board (Aug 23, 2026)** — «فرص البيع» is now the
prototype's own screen: an account card over stored product lines, each carrying WHERE it came from
(حملة واتساب · مكالمة · زيارة · إحالة · طلب وارد). It is the first surface whose stage is stored
rather than derived, and `docs/STATE.md` says why. Previous: **account graph (Aug 18, 2026)** —
prospect facts live in `entities.facts` with provenance (`src/facts.ts`), so the agent no longer
interviews every prospect; coverage is honest and near zero until an audience re-import carries the
HIS/ERP columns. Next slices: opportunity value on the home board and in reports, portal fact
editing, pre-launch enrichment, HIS/ERP vendor registry, KB retrieval (decks are still concatenated
into every prompt), and the Arabic counted-noun retrofit beyond `opps-crm.ts`.

## 3. Success Criteria & Evaluation Metrics
- Build: `npm run build` in `massar-engine/` exits 0 (strict TS). After any deploy,
  `GET https://massar-engine.fly.dev/health` returns `ok: true` and `outbound.ok: true`.
- Quality: review the diff before calling work done; any UI or user-flow change needs delivery
  evidence (smoke green, screenshots or a walkthrough of the real route).
- Safety (booleans, all must hold): no outbound WhatsApp to real customers without a human
  approval; «إيقاف»/STOP path verified when agent code changes; webhook token auth intact;
  no secret in git.
- Agent output: Arabic (clear MSA), ≤ 4 lines per message, one question max, grounded only
  in the approved KB — spot-check one transcript whenever agent code/prompt changes.
- Completeness: the increment ends with deployed health green and STATE.md updated.

## 4. Tech Stack & Conventions
- **Technical Standards apply.** `massar-engine/STANDARDS.md` is the adoption + DEVIATION register
  (what complies, what does not, why, and the exit for each). Read it before any new module. The
  binding rules for new work: business rules live in a pure, unit-tested `*-domain.ts` — never in a
  UI module; `is`/`has`/`can` booleans and verb functions (§2.1); comments say WHY; `npm test` must
  pass (it is first in `npm run check` and the 60% coverage gate BLOCKS a deploy); new endpoints are
  designed to the OpenAPI CRITICAL/HIGH rules (201+`Location`, RFC 9457 `problem+json`, documented
  401/403/429). Open: `openapi.yaml` (D-5) and the Postgres-vs-SQL-Server ruling on §6 (D-6).
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
  See `docs/decisions/0001-dashboard-no-range-edits.md`.
- Git: **two PUBLIC repos**, not a monorepo — `github.com/Abdulaziz-almoshen/Massar` (this dir)
  and `.../massar-engine` (nested, gitignored here, own history). Both on `master`, both over
  **HTTPS** (no SSH key on this machine). Push each from its own directory.
  **Public since Aug 24, 2026, by the founder's explicit decision** after being shown that the
  tracked tree carries real customer numbers and verbatim WhatsApp transcripts. Credentials are
  verified absent from both histories and MUST stay that way: every push is now a publication.
- Secrets: `massar-engine/.env` (gitignored) + `fly secrets` — OPENAI_API_KEY,
  GUPSHUP_API_KEY, GUPSHUP_APP_ID, GUPSHUP_APP_NAME, GUPSHUP_SOURCE_NUMBER, WEBHOOK_TOKEN,
  ADMIN_TOKEN. Never commit; never echo values into chat/logs.
- Hard rules live in code (opt-out, turn caps, window checks) — never only in prompts.

## 5. Working Rules
- Work in small, verifiable steps; read `docs/STATE.md` before acting, write it after.
- **NO WHATSAPP SEND, TO ANY NUMBER, FOR ANY REASON.** Standing instruction, Aug 12 2026:
  *"Don't ever send a text to the client for any test or anything… I will tell you what number
  you should test with."* This revokes the earlier "sandbox self-tests to the team's own opted-in
  phones are fine" allowance and every previously approved number. Verify agent behaviour by unit
  test and by reading existing transcripts; if a claim can only be proven by sending, leave it
  unproven and say so. Lifted only when the user names an explicit allowlist.
- Treat Gupshup/OpenAI/Fly as reliable tools; don't reinvent; keep the adapter seam clean.
- Never take an irreversible, financial, or outward-facing action autonomously; propose it.
- Questions to the user: only critical blockers, one batched question with the recommendation
  first. Otherwise follow the recommendation and proceed (standing instruction, Aug 10 2026).

## 6. Project Docs  (`docs/`)
- `STATE.md` — working state and the dated log of every increment. Read second, write last.
- `whatsapp-campaign-engineering.md` — **the core domain doc**: engine layout, Gupshup
  wire shapes (send/webhook v2+v3), WhatsApp platform rules, agent tool contract, ops
  runbook (deploy/secrets/test curls), sandbox specifics. Load for any engine work.
- `massar-design-language.md` — RTL/Arabic design system from the prototype (palette,
  type, component idioms, screen map). Load for any dashboard/UI work. Token authority:
  `DESIGN.md` at the root; selection record: `design/approved.json`.
- `decisions/` — architecture decision records (ADR-0001 dashboard edits, ADR-0002 attribution).
- `artifacts/` — plans, reviews, discovery briefs, and agent-eval transcripts per slice
  (`massar-engine/scripts/eval-agent.mjs` writes `artifacts/agent-eval/<stamp>/`).
- `qa/` — the agent-eval verdict schema and the campaigns-crm requirements traceability evidence.
- `design-previews/` — the HTML design variants that were shown before a screen was chosen.

## 7. Safety Rules & Human Checkpoints  ← the most important section
Human approval required before:
- **Any WhatsApp message to a real customer** (template blast or session send outside
  team test numbers) — and, per §5, currently any send at all. Any template submission to Meta.
  Any data deletion. Any spend > $5.
  (`fly deploy` of massar-engine is pre-authorized by the user's standing instruction of
  Aug 10, 2026 — "once done, just deploy it and fly"; revert to human-gated anytime.)
- FORBIDDEN outright: moving money; `fly apps destroy`; unsetting secrets; disabling the
  opt-out path or webhook token auth.
Work is done when the goal in STATE.md is met with deployed health green; never take an
irreversible, financial, or outward-facing action alone.

## 8. Learning
After any user correction, promote the learning to where it lasts: user-stated rules → this
file; techniques → the domain doc; dated choices → STATE.md. Surface one quiet `📝 Learned:` line
when it happens.

## gstack
Use the `/browse` skill from gstack for **all** web browsing. **Never** use `mcp__claude-in-chrome__*` tools.
Install once per machine: `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`.

Available gstack skills:
`/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/design-consultation`, `/design-shotgun`, `/design-html`, `/review`, `/ship`, `/land-and-deploy`, `/canary`, `/benchmark`, `/browse`, `/connect-chrome`, `/qa`, `/qa-only`, `/design-review`, `/setup-browser-cookies`, `/setup-deploy`, `/setup-gbrain`, `/retro`, `/investigate`, `/document-release`, `/document-generate`, `/codex`, `/cso`, `/autoplan`, `/plan-devex-review`, `/devex-review`, `/careful`, `/freeze`, `/guard`, `/unfreeze`, `/gstack-upgrade`, `/learn`

## Maintenance
Update §2's milestone line + STATE.md every cycle. §3/§4/§6/§7 only on durable change.
Keep this file readable in one glance.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec
