# Intelligence slice — العميل ٣٦٠: from campaign plumbing to customer understanding
2026-08-11 · R27 (reference screenshots: CXP predictions card, customer-360 w/ history
timeline + LTV + reachability, AI resolving + "every interaction makes the next one
better"): "this is the type of things I want to see… current implementation is not
product-market fit yet. Revise functions, solutions, UI/UX. Huge drag-drop box, fires —
don't make sense. Worry about how we really get value from this platform."

## Discovery (product-discovery)
The real gap he's naming: the platform SENDS but doesn't UNDERSTAND. Value = knowing WHO
to sell WHAT, WHEN, and WHY — per person, accumulating across touches. We already hold
the raw material per contact (full transcript, interest tags, outcomes, delivery
statuses, campaign touches, imported attrs, events) — nobody assembled it into a person.
The bet: a Customer-360 profile + an honest AI-signals layer on TOP of existing data,
plus de-uglifying the utility screens. NOT the bet: fake percentages (churn %, purchase
% need history we don't have), LTV (no revenue data), multi-channel (WhatsApp only
today). Honesty contract: deterministic context score (computable), LLM-READ signals
labeled as فهم المساعد (intent level, signals, objections, next action + best moment),
"يتعلم…" empty state below 2 customer messages — mirroring the reference's Month-1
Learning state.

## Business rules (business-analyst)
Insights: computed per contact from transcript+tags+statuses+attrs via OpenAI
(structured JSON); cached in PG keyed by turns watermark (recompute only when the
conversation grew); fields: summary (1 line), intent (high/medium/low/none), signals[],
objections[], product_interest[{product,level}], next_action (verb phrase), why,
best_time (from message timestamps + KSA business hours), risk (quiet-fade flag from
last-inbound age). Context score (deterministic): name 15 + entity-match 10 + attrs≥2 10
+ ≥2 inbound msgs 20 + replied 10 + tag 15 + activity<72h 10 + intro-file received 10 =
/100. Profile: #customer/<phone> — header (name/company/attrs/reachability/first-seen),
context rail, merged timeline (campaign sent/delivered/read, inbound, tags, handoff,
files, opt-events) newest-first, فهم المساعد card, actions (فتح المحادثة panel, takeover,
test-flag). Rows/home surface the insight (badge + next action), click → profile. UI
revision: dropzone → compact toolbar row (رفع ملف button + قالب link + لصق link); emoji
chips (🔥/⭐/👁/🙈) → text badges with tone dots; keep glyph minimalism per prototype.
ACs: (1) profile of the hot test lead shows real timeline + honest insights incl. a
concrete next action; (2) <2-message contact shows «يتعلم…»; (3) context score visibly
differs between rich and thin contacts; (4) insights recompute only on new turns (cache
hit proven in logs); (5) home «أفضل الفرص» rows carry why+next-action and link to
profiles; (6) upload toolbar compact, template still one click; (7) no emoji-fire chips
remain in tracker/home/panel; (8) build+node--check+3-viewport captures ×(profile, home,
customers)+0 console errors+gate PASS; (9) zero outbound sends by the insights layer.

## Prior art (market-researcher)
Reference product (user's screenshots) = CDP/CXP pattern: Segment/Klaviyo profile pages
(identity header + traits + event timeline), Intercom contact view (attributes rail +
conversation history), HubSpot contact insights (activity feed + AI summary + next
steps), Dynamics/Salesforce "next best action". Distilled honest v1: identity header +
traits chips + unified event timeline + AI summary/next-action card + completeness meter
(HubSpot-style) — all buildable from our ledger today. The "context %" rail maps to our
deterministic score; "CXP predictions" maps to LLM-read intent (labeled), not invented
probabilities.

## Plan (planner)
1. db.ts: contact_insights(phone PK, data JSONB, turns_at INT, computed_at BIGINT) +
   repo get/save. 2. src/insights.ts: contextScore(), buildTimeline(), computeInsights()
   (gpt-5.6, reasoning_effort none, strict JSON, KB-free — reads only this contact),
   getInsights(phone,{force}) cache-by-watermark. 3. index.ts: GET /admin/customer/:phone
   (contact+entity+insights+timeline+contextScore), POST /admin/insights/refresh.
   4. dashboard.ts: route #customer/<phone> + vCustomer (two-col: timeline | فهم المساعد;
   header w/ context rail; actions); refits: contactRowsHtml name→profile link + badge
   swap; vHome «أفضل الفرص الآن» w/ summary+next action; vCustomers compact toolbar +
   rows→profiles; emoji-chip sweep. 5. Prove ACs live (test lead has a real 4-turn
   transcript; user contact rich), captures, evidence @commit, gate, reviewer packet,
   CPO round-8. Cost control: insights computed lazily (profile open / فرص top rows w/
   ≥2 turns), cached by watermark; zero sends.

## Design treatment (designer — massar-design-language, NOT the reference's purple)
Profile header: navy identity block (avatar initial, name, company · city chips), left
context rail (vertical meter, % + label «اكتمال السياق», teal fill) mirroring the
reference's CONTEXT rail in Massar tokens. Timeline: prototype kbrow idiom — tone dot +
title + meta time, channel tag (واتساب/حملة/نظام), newest first, max-height scroll.
فهم المساعد card: tinted teal (#F4FBFA) w/ ⁂ mark, summary line bold, intent badge
(dot + نية شراء مرتفعة/متوسطة/منخفضة), signals/objections as compact rows, «الخطوة
التالية» emphasized block w/ best-time line, «حدّث القراءة» ghost button. Badges: 8px
tone dot + 11px label (high=#1f8a52, med=#b5810f, low=#7b8597, fade=#c43d3d). Upload
toolbar: single 44px row — primary small button «⬆ رفع ملف المستهدفين», ghost «القالب»,
ghost «لصق يدوي» (opens details) — dropzone deleted. Fires removed everywhere; ⟲ kept.
