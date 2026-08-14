# Marketing-intelligence review — «ما قيمة الحملة وكيف نستفيد منها فعليًا؟»

2026-08-11 · Expert-panel artifact · Reviewed: `massar-engine/src/insights.ts`,
`src/dashboard.ts` (vHome, vHomeCharts, vKmon, vKmonDetail, vCustomer, campStats),
`src/tracker.ts`, `src/db.ts`, `src/index.ts`, honesty contract in
`.orbit/artifacts/intel-slice/plan.md`.

---

## 0. The value thesis (answer the founder's question first)

For B2B outbound WhatsApp with an AI closer and **no revenue data in the system**, the
honest value of a campaign is exactly three things, all computable from the ledger:

1. **Pipeline yield** — qualified leads handed to a human per 100 sends
   (hot/warm tags + handoffs), and later *human-confirmed outcomes* (meeting booked).
   This is the money proxy until revenue data exists.
2. **Market learning** — what the conversations taught us: which objections, which
   products, which segments, which hours. Aggregated from data we already store
   (tags, cached فهم المساعد reads, entity attrs, timestamps). A campaign that yields
   0 leads but proves «عيادات الأسنان لا تردّ والمجمعات تسأل عن السعر» paid for itself.
3. **List health** — what the campaign cost the WhatsApp number: failed sends,
   opt-outs, silence. Protecting the number is goal #4 in CLAUDE.md and nothing
   surfaces it today.

Value is only *realized* through next actions. Every surface should end in a verb:
call these 3, retarget these 12, stop targeting this segment, send at 10am next time.
The system already has the muscle (startRetarget carries a filtered cohort into the
wizard; insights produce next_action per contact) — what's missing is the connective
tissue that turns ledger facts into a ranked action queue.

**Measurement chain (all honest):** sends → delivered → seen → replied →
*qualified reply* (tag or intent ≥ medium) → handoff/hot → **human-logged outcome**.
The last link doesn't exist yet and is the single cheapest high-value addition (R2).

---

## 1. What decision should each surface drive?

| Surface | The one decision it must answer | Today | Gap |
|---|---|---|---|
| **Home** (vHome) | «أين أضع انتباهي اليوم؟» — who to call now, who is going cold, which retarget is ripe | KPI counts, rates strip, aggregate funnel, أفضل الفرص (top 6) | No urgency ordering, no fade alerts, no retarget prompt, no week-over-week movement |
| **Campaign detail** (vKmonDetail) | «هل نجحت هذه الحملة، وما الخطوة التالية؟» | 6 absolute stat cards + filters + retarget button | No verdict (yield, vs. average), no learning summary, no recommended next moves; seen-no-reply not directly filterable |
| **Campaign list** (vKmon) | «أي حملة أفضل — ماذا أكرر وماذا أوقف؟» | audience / seen% / reply% / delivery progress, sort by raw counts | Not comparable: no yield column, no hot count, no list-cost, status hardcoded «جارية», numbers bleed across campaigns (see R1) |
| **Profile** (vCustomer) | «كيف أُغلق هذا العميل؟» | Identity + فهم المساعد (next_action/why/best_time) + timeline — genuinely good | No way for the human to log what happened after the call → the loop never closes |

---

## 2. Prioritized recommendations

Ordered by (value ÷ effort) with structural prerequisites first. Effort: S ≤ ½ day,
M ≈ 1–2 days, L ≥ 3 days.

### R1 — Per-campaign send ledger (fix attribution before it lies) — **M**
- **What:** `campaign_sends` table (campaign_id, phone, gupshup msg_id, sent_at,
  delivered_at, read_at, first_reply_at, failed). Write a row at launch (the send loop
  in `index.ts /admin/campaign/launch` already receives `messageId` from
  `gupshup.postForm`); update it from the status webhook by msg_id; set
  first_reply_at = first inbound after sent_at.
- **Why:** `campStats()` today reads the contact's *global* `statusTimes` — a contact
  in two campaigns counts its reply in **both**. The UI actively encourages retargeting,
  so campaign #2's cohort is by construction campaign #1's contacts: the moment
  retarget is used, every per-campaign number and the whole comparison view become
  fiction. Also `statusTimes.replied` is overwritten on every inbound (tracker.ts:70),
  so reply *timing* per campaign is unrecoverable without this. This is the honesty
  contract applied to campaign math.
- **Data source:** launch loop + `normalizeWebhook` events (already carry msg ids) + inbound timestamps.
- **Where:** `db.ts`, `index.ts` (launch + webhook), `campStats` reads the new rows with fallback to the current heuristic for legacy campaigns.
- **Note:** everything in R3–R7 gets more truthful automatically once this lands; ship it first or clearly label cross-campaign numbers as approximate.

### R2 — Human outcome logging on the profile (close the loop) — **S**
- **What:** 4 buttons on vCustomer: «حُجز اجتماع» · «أُرسل عرض سعر» · «مؤجل — ذكّرني» ·
  «غير مناسب». Writes a system turn + sets/extends `outcome`; appears in the timeline;
  aggregates per campaign as «اجتماعات من هذه الحملة».
- **Why:** The founder's question «كيف نستفيد؟» is unanswerable without ground truth
  about what happened *after* the AI handed over. Meetings-per-100-sends is the closest
  honest proxy to revenue we can have, and it costs one afternoon. It also creates the
  dataset that will later justify (or kill) every other metric.
- **Data source:** human click → `tracker.setOutcome` + `addSystemNote` (both exist).
- **Where:** `vCustomer` actions row, one small POST in `index.ts`, chip in `chipRow`.

### R3 — Campaign verdict block: «قيمة الحملة» on vKmonDetail — **S**
- **What:** Above the stat cards, one strip with 4 honest numbers:
  - **العائد** — qualified leads per 100 sends: `(hot+warm tagged ∪ handoff) / sent × 100`
  - **جودة الردود** — qualified replies ÷ replies (a reply that produced a tag or
    intent ≥ medium vs. «ليس الآن»/silence-after-one-line). Distinguishes a 20% reply
    rate full of «لا شكرًا» from a 10% rate full of price questions.
  - **مقارنة بمتوسطك** — this campaign's yield vs. the account's average across settled
    campaigns, shown as raw delta with n («٦ مؤهلون/١٠٠ مقابل متوسط ٤ — عيّنة ٤٨ إرسال»). No significance theater.
  - **كلفة القائمة** — failed + opt-outs this campaign caused.
- **Why:** «Did THIS campaign work» currently requires mental math over 6 absolute
  counts. Yield-per-100 is the one number that survives different audience sizes.
- **Data source:** campStats + tags + outcomes (+ R1 for exact per-campaign truth).
- **Where:** `vKmonDetail` above `statgrid`; helper next to `campStats`.

### R4 — Next-move engine: deterministic recommendations after a campaign — **M**
- **What:** A «الخطوة التالية» card on vKmonDetail (and surfaced on Home) computed by
  rules over the ledger, each with a one-click action that reuses `startRetarget()` /
  the cohort snapshot machinery that already exists:
  1. `hot/warm ∧ no human takeover` → **«اتصل بهؤلاء الثلاثة أولًا»** ordered by
     intent level then recency, each with its cached `next_action` + `best_time`.
  2. `read ∧ ¬replied ∧ settled (no events 48h)` → **«أعد استهداف ١٢ شاهدوا ولم يردوا»**
     with a suggested different angle: if the campaign's aggregated objections say
     «السعر», suggest the value-first opener; template pre-named (naming logic exists).
  3. `delivered ∧ ¬read ≥72h` → **«جرّب توقيتًا مختلفًا»** — pair with R7's reply-hour data.
  4. `outcome = later` → **«موعد متابعة بعد ٧ أيام»** list.
  5. `failed` → **«صحّح هذه الأرقام»** (list hygiene).
- **Why:** This is the literal answer to «how do we benefit from a campaign». Every
  rule is computable, explainable in one sentence, and ends in an existing safe action
  (human still launches; §8 intact). Also add the missing **«شوهدت ولم تردّ»** filter —
  today's «شوهدت» filter includes repliers, so the most valuable retarget cohort can't
  even be selected directly.
- **Data source:** statusTimes/campaign_sends, tags, outcomes, insight cache, timestamps.
- **Where:** new `nextMoves(camp)` helper in dashboard.ts; card in `vKmonDetail`; top item mirrored on Home.

### R5 — Home becomes a ranked action queue — **M**
- **What:** Reframe vHome's top as «قائمة اليوم»:
  1. **Hot now** — أفضل الفرص upgraded: order by intent then `lastEventAt`, show
     next_action + best_time (already wired via insCache).
  2. **يبردون** (cost of silence) — contacts with hot/warm tag or handoff and **no
     activity > 72h**: `interestedOf(c) ∧ now − lastEventAt > 72h`. Count + top 3 +
     days silent. B2B deals die of silence, not rejection; nothing shows this today.
  3. **فرصة إعادة الاستهداف** — largest seen-no-reply cohort among settled campaigns,
     one click into R4's flow.
  4. Rates strip gains **week-over-week deltas** (this 7 days vs. prior 7, from
     timestamps) — movement, not levels, is what a founder scans daily.
- **Why:** Home's decision is «where does my attention go today». Counts and a funnel
  don't rank attention; a queue does.
- **Data source:** all existing; no LLM calls (insight cache only).
- **Where:** `vHome` (replace/extend the two-card grid), helpers near `interestedOf`.

### R6 — Campaign list as an honest comparison table — **S**
- **What:** Columns: الجمهور · نسبة الردود · **مؤهلون/١٠٠** (yield, new default sort) ·
  **حارّون** (count) · كلفة (فشل+إيقاف) · الحالة. Status becomes computed lifecycle:
  «نشطة» (events < 48h) / «استقرت» (no events ≥ 48h) instead of the hardcoded «جارية».
  Best-yield settled campaign gets a subtle «الأفضل» badge.
- **Why:** «Compare performance» requires normalized, per-campaign-true numbers
  (R1) and a value column, not delivery progress. Sorting by raw reply counts favors
  big audiences over good campaigns.
- **Data source:** campStats/R1 + tags + event recency.
- **Where:** `vKmon` table columns + `campSortKey` options.

### R7 — Reply-timing intelligence (best send windows, honest version) — **S**
- **What:** One card: histogram of inbound-message hours (KSA time) + median
  time-to-first-reply, always labeled with sample size; render only at n ≥ 20 inbound,
  else «تظهر بعد ٢٠ ردًا». Feed the winning window into R4's rule 3 and campaign-launch
  hint («أفضل نافذة مجرّبة: ١٠–١٢ صباحًا، من ٣٤ ردًا»).
- **Why:** Real timestamps exist in every transcript turn; per-contact best_time is
  already LLM-guessed — the aggregate deterministic version is stronger and free. The
  n-gate keeps it inside the honesty contract at sandbox volume.
- **Data source:** `transcript[].ts` where role=customer; campaign `created_at` / R1 `sent_at` for lag.
- **Where:** helper + card in `vHomeCharts`; one line in `vAimkt` near the launch button.

### R8 — Campaign learning panel: aggregate فهم المساعد — **S/M**
- **What:** On vKmonDetail: «ماذا تعلّمنا» — top objections (with counts), top buying
  signals, product-interest distribution, aggregated across the campaign's contacts
  that have a cached insight (≥2 inbound). Label: «من قراءات المساعد — ٧ محادثات».
  Optionally roll the same aggregation up by segment (city/size via entity attrs).
- **Why:** This converts conversations into market intelligence — value type #2. It is
  pure aggregation of already-labeled LLM reads; nothing invented, and the count label
  keeps provenance visible. Objection counts also power R4's angle suggestions.
- **Data source:** `contact_insights` cache (`db.listInsights` endpoint already exists) × campaign targets × entity attrs.
- **Where:** `vKmonDetail` card; reuse `hbarRows`.

### R9 — Segment yield: where to spend the next 50 sends — **M**
- **What:** Table on Home (or reports): yield-per-100 by المدينة/الحجم/القطاع, computed
  as campaign contacts joined to entity attrs; only rows with ≥ 15 sends; ends with an
  action: «الشريحة الأعلى: مجمعات الرياض — ٢٢ جهة مستهدفة لم تُراسل بعد → أنشئ حملة»
  (entities minus contacted, pre-filtered into the wizard — the entFilters machinery exists).
- **Why:** Cohort deltas between *segments* are more decision-useful than deltas
  between campaigns at this volume, and they answer «who next» with data instead of instinct.
- **Data source:** entities.attrs × campaign membership × tags/outcomes.
- **Where:** helper + card in `vHomeCharts`; deep-link presets into `vCustomers`/`vAimkt`.

### R10 — List-health panel (protect the number) — **S**
- **What:** Small strip on Home: failed rate trend, opt-outs total + this week, sends
  per day vs. pacing cap. Red state if opt-outs/sends > 2% on any campaign.
- **Why:** CLAUDE.md goal #4 («never burn the number») has zero instrumentation today.
  One opt-out spike caught early is worth more than any dashboard chart.
- **Data source:** `statusTimes.failed`, `outcome=opted_out`, counters/recentEvents.
- **Where:** `vHome` under the KPI row.

### R11 — Definitions cleanup (one honest vocabulary) — **S**
- **What:** (a) Delete dead `funnelData()` (dashboard.ts:277 — never called, and its
  «interested» = `outcome==="interested"` contradicts `interestedOf()` used everywhere
  else). (b) Define «مؤهل/مهتم» once (tag hot|warm ∪ outcome interested|handoff) in one
  helper used by funnel, stats, home, filters. (c) Rates strip denominators documented
  in the tooltip («الردود من الذين وصلتهم»).
- **Why:** Two definitions of the flagship metric is how dashboards lose trust; the
  cleanup is 30 minutes and prevents a founder-facing contradiction.
- **Where:** `dashboard.ts`.

---

## 3. What NOT to build yet (and why)

- **Revenue/ROI attribution, LTV, deal size** — no revenue data anywhere in the ledger. Any number would be fabricated. Revisit only after R2 outcomes accumulate and a deal value field exists in a real CRM flow.
- **Predicted conversion/churn probabilities or ML lead scores** — no historical outcomes to train or even calibrate on. Intent stays a *labeled LLM read* (as designed), never a percentage.
- **Industry benchmarks** («متوسط القطاع ١٢٪») — no source; pure invention.
- **Composite «engagement score» indexes** — hides the raw truth behind an arbitrary formula; the context score already covers "how much we know" honestly.
- **A/B testing with significance claims** — at n < 100 per arm it's noise theater. Show raw cohort deltas with sample sizes (R3) instead.
- **Automated send-time optimization / auto-retargeting** — data too thin and it violates the human-gate rule; recommend (R4/R7), human launches.
- **Multi-touch attribution models** — single channel, tiny volume; the per-campaign send ledger (R1) is the whole attribution story needed now.
- **Headline vanity counters** (total messages sent, city treemap as a KPI) — keep them as context, never as the answer to «هل نجحنا؟».

---

## 4. Suggested sequencing

1. **Week 1:** R11 + R2 + R3 (S+S+S — the vocabulary, the loop, the verdict).
2. **Week 2:** R1 (the structural fix) then R6 (comparison becomes real) + R4 (the benefit engine).
3. **Week 3:** R5 + R7 + R8 (home queue, timing, learning), then R9 + R10.

Everything above uses only: delivery statuses, transcripts + timestamps, interest tags,
outcomes, entity attributes, campaign membership, and cached labeled LLM reads —
nothing fabricated, every number traceable to a ledger row.
