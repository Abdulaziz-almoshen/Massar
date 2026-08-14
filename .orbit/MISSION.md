# 🌙 OVERNIGHT MISSION — team demo at wake-up (R34, ~8h autonomous)
Started 2026-08-11 ~21:30 Riyadh. User asleep. FULL permission granted ("do whatever you
want, don't stop, don't talk — build"). Deploy freely (standing rule). Real-customer sends
still forbidden (only his 966559402621 + fake test numbers). Read this file FIRST after any
context compaction — it is the mission brain. Working state: STATE.md. Board: tasks #27-30+.

## The bar (his words)
Team must SEE: value, design, experience, "how they will sell better than the sales",
AI that explains WHY we sold / WHY we didn't sell — per customer (user issue / product
issue / communication issue / unclear file). "Brand new design, UX, intelligence.
Surprise me: intelligence, animation, insights, dashboard, agent flow, how agents use
photo/header/body/files, how Product Hub connects everything." Be smarter than all
their current tools. CPO round-9 judges vs the 5 reference images + this brief.

## Mission phases (execute in order; each ends with deploy + capture + STATE.md line)
### P1 — Consolidate the expert panel (4 agents dispatched, reports →
.orbit/artifacts/expert-panel/{reference-fidelity,design-spec,marketing-intelligence,agent-evaluation}.md)
Wait for/read all 4 → write expert-panel/CONSOLIDATED.md: the agreed build list. If an
agent died, proceed with the other reports + own judgment (note it).

### P2 — Win/Loss Intelligence («لماذا بعنا ولماذا لم نبع») — THE headline surprise
- insights.ts: extend the per-contact read with: deal_state (won/lost/stalled/active),
  loss_cause from taxonomy [السعر, التوقيت, منتج غير مناسب, تواصل غير واضح, الملف غير
  واضح, لا استجابة, جهة غير مناسبة, طلب بشريًا], win_drivers[], evidence quote (verbatim),
  fix_suggestion (what would have won it). Same honesty contract: only from transcript.
- db: extend contact_insights data JSONB (no schema change needed).
- New aggregate endpoint /admin/intel/winloss: per-product win rate, ranked loss causes
  w/ counts + example quotes, ranked win drivers (computed over cached insights only —
  compute-on-open for uncached w/ cap ~10 LLM calls, then cache).
- UI: home gets «لماذا نكسب ولماذا نخسر» two-column card (win drivers vs loss causes,
  each row: cause + count + sample quote + المنتج chip); campaign detail gets its cohort's
  version; profile's فهم المساعد shows deal_state + loss_cause + fix_suggestion when lost.

### P3 — Reference-grade design completion (apply P1 specs)
- Campaign detail page + wizard restyle (the two screens with no reference image — use
  design-spec.md blueprints). Funnel: bigger, centered, animated draw-in.
- Micro-animations (CSS only, respect prefers-reduced-motion): staggered card fade-up on
  route enter (~40ms steps), KPI count-up (JS rAF, 600ms), funnel segments scale-in,
  progress bars width-transition, live-chip pulse, hover lifts (translateY(-2px)+shadow).
- Skeleton loading states instead of blank/«جارٍ التجميع» (shimmer blocks).
- Apply fidelity-audit fixes to home/list/profile/customers.

### P4 — Agent flow + Product Hub interconnection
- Apply agent-evaluation.md improvements to the system prompt + tool docs (opener
  quality, question discipline, closing moves). Save its Arabic template pack to
  .orbit/artifacts/templates-pack.md (for production WABA; do NOT submit anywhere).
- Product page (kb/<name>) becomes the connected hub: readiness, linked campaigns +
  their stats, win rate + top loss cause for THIS product (from winloss data), asset
  status, «أطلق حملة بهذا المنتج ←» CTA (deep-link into the prefilled wizard).
- Agent: if product has intro PDF → opener already sends single doc+caption bubble ✓;
  add buttons follow-up mastery per evaluation report.

### P5 — The demo layer (he presents FROM this)
- #home becomes presentation-worthy: hero strip «مسار — مساعد المبيعات الذي يفسّر
  السوق» + live counters + the winloss card + أفضل الفرص + charts (all animated).
- Seed a realistic demo dataset IF needed for visual richness: mark test=true, clearly
  fake names? NO — keep data honest: use existing test contacts + import a small clinics
  file (test-flagged) and run 2-3 simulated webhook conversations with VARIED outcomes
  (one interested→won-ish, one price objection→lost, one silent→no response) so the
  winloss board has real LLM-derived rows. All via fake 96650000078x numbers (agent
  replies fail harmlessly = no real messages; transcripts still form).
- Every send ONLY to fake numbers or his own.

### P6 — Gates (before he wakes)
- Full capture sweep ×3 viewports ×(home, kmon, kmon/1, customer profile, customers,
  aimkt, kb product page) + diffs; SIDE-BY-SIDE self-audit vs the 5 reference images.
- delivery-evidence.json rebound @final commit w/ new scenarios (winloss extraction,
  animations don't break console, hub interconnection); gate PASS.
- Reviewer packet (SendMessage to reviewer agent a54abacf3d5b36840 — context intact) on
  the night's diff. Fix musts. CPO round-9 (fresh agent): bar = reference images + R34
  brief; must view screens by eye. Reporter: final wake-up report — what to demo, in
  what order, with the story per screen ("the pitch script").

## Hard rules tonight
- NO real-customer sends. NO secrets in logs. Opt-out/caps untouched. fly deploy free.
- Verify every deploy: build + node --check page JS + /health + captures. The
  template-literal escaping discipline (\\n, \\') — node --check catches.
- LLM cost sanity: winloss compute capped + cached (watermark pattern).
- If a panel agent's report conflicts with a reference image → the IMAGE wins (R32 rule).
- Timebox: if P3 runs long, cut scope at campaign-detail restyle, keep animations light.
  P2 (winloss) is NON-NEGOTIABLE — it is his headline ask.

## Status log (append as phases complete)
- P0 done pre-mission: single-bubble PDF @7db6509 (proof on his phone), design-system
  foundation @9848b82 (live), 4 panel agents dispatched (notifications pending).
- P1 partial: marketing-intelligence.md LANDED (top: campaign_sends ledger fixes cross-campaign stat contamination; human outcome buttons; verdict block; next-move engine; home action queue; seen-no-reply cohort filter gap; replied-overwrite bug tracker.ts:70; dead funnelData). 3 reports pending (fidelity, design, agent-eval).
- P2 CORE DONE @3b87966 (not yet deployed): Insights type + SYSTEM prompt extended w/ deal_state/loss_cause(taxonomy)/win_drivers/evidence/fix_suggestion + coercion; winLossBoard() aggregate over cached rows; GET /admin/intel/winloss. NEXT: (a) home «لماذا نكسب ولماذا نخسر» card + profile deal-state/fix display + campaign-detail cohort version; (b) deploy; (c) P5 simulate 3 varied-outcome fake conversations (96650000078x — price-objection lost, interested won-ish, silent stalled) then force-refresh their insights to populate the board; (d) remaining panel reports (design-spec, reference-fidelity, agent-eval agents still out) → P3/P4.
- P3 progress: campaigns list = Emaily anatomy @9fc7cd2 (verified by capture); home = title block + icon KPIs + stage-bar funnel + navy treemap @7a482fc; campaign detail verdict strip (deploying). P2 PROVEN LIVE: seeded 3 varied demo threads (test-flagged) → board shows lost:2 (التوقيت, الملف غير واضح) w/ verbatim evidence + win drivers + per-product. Agent hard-rule fixes @84ac266 (opt-out precision, turn-cap dead end).
NEXT: profile prediction-panel anatomy, product-hub interconnection, templates pack file, KPI count-up animation, capture sweep + gates + CPO round-9.
- P6 IN PROGRESS: gate PASS @43a5015 (21 captures/3 viewports/0 console errors, 6 new scenarios); reviewer packet dispatched for the 11-commit night diff; CPO round-9 next.
- P5 done: seeded 3 varied demo threads (test-flagged), auto-reveal so the demo never opens on zeros, count-up + rise animations live.
- P4 done: agent hard-rule fixes + code-enforced single bubble + caption tool; templates-pack.md extracted; Product Hub interconnection (campaigns + market verdict + launch CTA).
REMAINING before wake: CPO round-9, wake-up report w/ demo script (order: home command center → win/loss card → click a lost customer → profile evidence + fix → campaigns list → campaign verdict → wizard single-bubble preview → product hub).
- REVIEWER ROUND CLOSED: 6.5 BLOCKED → M1/M2/M3 + S1/S2/S5/S6 all landed (@e9a735a, @e6f421a). Opt-out matrix 22/22 executed. Gate PASS @e6f421a. CPO round-9 dispatched (bar: the 5 reference images + demo readiness). DEMO-SCRIPT.md written for his presentation.
- REMAINING: CPO verdict → any blockers → final wake-up report.
- FINAL STATE @49d9ddb: gate PASS, 21 captures 0 errors, health green. Added post-reviewer: S3 stall window, S4 CSV guard, human outcome capture (loop closer). WAKE-UP.md + DEMO-SCRIPT.md written. Awaiting CPO round-9 verdict (dispatched ~01:00).

## MISSION COMPLETE (2026-08-11T19:29Z)
- CPO round-9 **ACCEPT** @e6f421a — 9/9/9/9/9, demo risk LOW. Watch items landed @ab4b847.
- Final: gate PASS @ab4b847, health green, 24 captures 0 console errors, 20 commits.
- Deliverables for him: WAKE-UP.md (what changed) + DEMO-SCRIPT.md (7-minute presentation).
