## 2026-08-13 · ROUND 28 — CPO ACCEPT @9916ed3 (deployed, health green)

Founder's goal met: two genuinely distinct campaign templates (different premise, CTA and audience,
not variants), selectable as a radiogroup in wizard step ٣, with {{1}} resolving from the chosen
service in both preview occurrences while the textarea keeps the raw token as editable source.

Gates: reviewer **8.5/10 PASS** (first time the >=8 bar was met) · safety-gate PASS · qa-engineer
PASS · **delivery-quality-gate exits 0 on the full SHA — first time in this workstream**.

Two over-claims by the loop were caught and corrected in the record this round: the enum was called
"enforcement" when it is guidance (canonicalTitle at the emit site is the load-bearing guard), and a
regex fix was described as closing a case it never matched. Rule 7 held both times — by review, not
by self-report.

Button subsystem FROZEN (planner, upheld by CPO). Next increment: **segment save -> schedule ->
launch**. Carried: gate short-SHA prefix match; strict:true on the tool schema (needs footer moved
into required); production WABA (Meta body-substitution constraint recorded above).

## 2026-08-13 · Round 26 closed — deployed 090ef30

Board #49 and #50 closed. #49 produced the round's best finding: harvesting LIVE transcripts
(80 agent turns) showed **24 distinct button titles actually sent to customers, 15 with no intent**.
The model composes far more freely than the prompt or the table assumed, and under the new emit-time
allowlist all 15 would have been dropped to plain text. Mapped. **Rule: the button table must track
what the model ACTUALLY says — re-harvest from live transcripts whenever the prompt changes.**
#50 verified present: sentAssets, RUNG_ONE_MARK, openerOf, per-message nextObjective.

**CORRECTION to commit d85d037's message.** It claims the decline test «was unanchored and matched
inside «لاحقًا»». That is false — the old alternation's «^لا$» branch was already anchored and does
NOT match «لاحقًا» (verified). The anchoring change was a no-op for that case; the real M2 fix was
the outcome-downgrade guard. Recorded rather than rewritten: Rule 7 — the loop's claims about itself
are subject to Rule 2, and this is the loop over-claiming in the very commit meant to stop it.

Reviewer never met the >=8 bar this round (best 7.5). Delivery gate does not exit 0: the only
failing rows are the three intended #aimkt launch-bar re-baselines.

## 2026-08-13 · PRODUCTION-WABA MIGRATION — carry-forward constraint (reviewer item 8)

The wizard's warning banner was removed on the founder's ruling «pretend it is approved template»,
which is correct for the sandbox (session messages carry whatever body we send). **The constraint
returns at the production number and is no longer represented anywhere in the UI:** `sendTemplate()`
puts `template:{id,params}` on the wire — there is no field for body text — so Meta sends the
APPROVED body and an operator's wizard edit does not travel. Recorded here so it is not rediscovered
during the migration. Fix at that point: read-only registry + `metaTemplateId` + approval status.

## 2026-08-13 · All five re-review blockers closed (e4121fa, deployed)

Reviewer re-review returned 7/10 BLOCKED with five blockers; all are closed at e4121fa. The two that
mattered most: `canonicalTitle` was rewriting outbound copy by proximity rather than fidelity
(«لا أريد العرض التجاري» → «أريد العرض التجاري» — a button saying the opposite of what was meant),
and the widened `wantsInfo` had re-opened complaint #1 («التفاصيل والسعر لو سمحتم» short-circuited to
the PDF before the model ran). Also: the pre-deploy gate was asserting a hand-copied button list
already divergent from boot's; every prompt-prescribed `send_buttons` title was being dropped, so the
scheduling close shipped with no buttons; and the drop path could send four bubbles in one turn.

**A defect the gate caught that review had not:** anchoring the objection stems was necessary because
an unanchored «لم» matches inside «الـمـلـف» — so «الملف التعريفي للإجازات المرضية» read as an
objection. Same Arabic-substring family as the `\b` bug. A canary case now guards it.

check-buttons.mjs: 82 → 118 assertions. Two of the previous 82 proved nothing (one compared a value
to itself; one used a title the old check would also have rejected) — both replaced.

## 2026-08-13 · Template registry + button contract — REVISED after review (f9a51f0, deployed)

**5f38d56 was BLOCKED by the reviewer at 6/10.** Its headline claim — "every emitted button now
routes" — was provably false: `send_buttons` lets the MODEL compose titles at runtime, so the
largest emission site was outside the contract, and the system prompt's own «أريد العرض التجاري»
routed nowhere → «أي وصف يناسبكم؟». The founder's complaint #1 was still reachable by the route the
contract did not cover. Lesson recorded in the domain skill: **enumerate every emission site before
declaring a contract closed** — this one had four, and the check covered three.

**product-discovery** found the second real defect: turn two of the upsell was the intro's. One tap
after «لاحظنا أن لديكم استخدامًا مرتفعًا» we asked who they are. Every green check tested the opener;
none tested turn two.

f9a51f0 closes both: `canonicalTitle()` normalises model-composed titles at the EMIT site (unmappable
→ dropped, body sent as text); the campaign marker carries the template id so rung one knows its
opener and the upsell qualifies on implementation, never identity. Plus: unknown `templateId` 400s,
`{product}` guarded with `{{1}}`, UTF-16 length alignment with the adapter, role-filtered rung-one
marker, one source for the fallback buttons, designer's picker changes, and a wizard warning that an
edited body will not survive Meta approval (market research: `sendTemplate` has no body field).

`scripts/check-buttons.mjs` is new and in `npm run check` — 82 assertions against compiled code and
the real objective block, each printing its measured value. The planner's verdict on the prior round
was that the proof existed only in a chat message; it is now re-runnable and pre-deploy.

Stage owners on this increment: product-discovery · business-analyst · market-researcher · designer ·
planner · safety-gate (PASS) · reviewer (BLOCKED@5f38d56, re-review in flight on f9a51f0) · QA (in
flight). **No WhatsApp message sent.**

## 2026-08-13 · Template registry + the button contract (5f38d56, superseded by f9a51f0)

Founder supplied a SECOND opener (high-usage upsell: «لاحظنا أن لديكم استخدامًا مرتفعًا») and asked
to pick it at campaign creation. Built as a registry — `src/templates.ts` — so a third template is
data, not code. `GET /admin/templates` feeds both the wizard preview and the launch path, so a
template cannot preview one way and send another. `{{1}}` = service, resolved client- and
server-side; launch 400s if `{{1}}` survives with no service chosen.

**The durable rule this round produced:** every reply button the system emits must be answered by
the code that receives the tap. `BUTTON_INTENT` is that table and `assertButtonsHandled()` enforces
it at boot — a button with no intent, or a title over WhatsApp's 20 chars, refuses to start the
process. Both had already shipped: a 21-char title failed three sends (131009), and «العرض التجاري»
dead-ended the customer who tapped it, reproducing the founder's own complaint #1.

Also closed from CPO r25: «تسعير» stem; `RUNG_ONE_SENT` moved from an in-memory Set (45 deploys in
one day) to a transcript marker; `rungOne()` and the asset lookup parameterised by service — both
were hardcoded to التطعيمات and answered an الإجازات المرضية question about vaccinations.

Evidence: build 0 · check:numerals · check:catalogue · smoke 7/7 · client script parses · 20/20
registry assertions · 16/16 intent cases run against the real objective block sliced from agent.ts ·
picker + resolved {{1}} rendered at 1440/1024/390. **No WhatsApp message sent.**

Open: CPO r25 MUST-2 (agent-matrices.txt lost its contradicting rows instead of making them
self-checking — needs machine-written `measured` fields) and the campaign-windowed `asked`/`agentSaid`
(a price ask before the last `[حملة]` marker is invisible).

# Working State — Massar (مَسار)

_Last updated: 2026-08-13T04:30Z by orchestrator_

## Run goal
No loop run active. Next run's goal: increment 2 — Postgres ledger replacing the in-memory
tracker (queue below).

## Current snapshot  (overwrite every cycle)
- Iteration: idle. Last increment CPO-ACCEPTED (round-22, 9/8/8/8/6, zero musts), hardened after.
- Engine: deployed + healthy @76ff28a. `npm run deploy` = check:catalogue + check:numerals →
  fly deploy → smoke (7 routes). Three consecutive clean smoke runs after the font-CDN fix.
- Data: 4 REAL conversations, all customer-initiated (966535106365 · 966502444737 ·
  966543464327 · 966592681957) + 16 sandbox. **No cold outbound to a real customer, ever.**
  1 real campaign («حملة أغسطس — عيادات الرياض»), 10 rehearsals filed under «تجريبية».
- Blockers: none.
- ⚠️ Demo prerequisite: turn **«إظهار التجريبية»** ON before presenting — the four real
  conversations are all still active, so the loss side of the win/loss board is honestly empty
  without it. Do NOT click past «إعادة استهداف» into confirm-launch: that sends real WhatsApp.
- Next: segmentation + retargeting build, from `.orbit/artifacts/segmentation/BENCHMARK.md`.

## Task queue  (priority order)
0. **Right-size capability enforcement for T1** — the strict owner chain fired on a 2-line
   deletion; tune `capability_enforcement.work_event_threshold` / add a T1 exemption in
   loop.config.json + stop-check so the gearbox's fast lane stays fast (do openly, next cycle).
1. ~~Live sandbox E2E test~~ ✅ done Aug 10.
2. ~~**Postgres ledger increment** (shadow slice)~~ ✅ done Aug 11 @6c66f05 (incl. reviewer's pool-error fix); delivery-quality gate PASS with full evidence bundle (.orbit/qa/delivery-evidence.json) — fly pg
   `massar-db` attached; dual-write + boot-hydrate; SURVIVAL PROOF passed (contact +
   counters lived through machine restart, parity 1==1). Deploys no longer wipe state.
   Remaining from the full §5 schema (next slices): campaigns/campaign_contacts/
   send_outbox with the campaign engine.
2b. **Campaign engine slice** — outbox + pacer (BullMQ/Redis or pg-boss) + campaign API;
   un-gates the wizard launch button. — `campaigns / campaign_contacts / events / interest_tags /
   messages / send_outbox` replacing the in-memory `tracker.ts` (architecture doc §5; keep
   event names). T3.
3. **Outbox + pacer (BullMQ/Redis)** — template blasts with tier ceiling, daily cap, quiet
   hours, per-user cooldown (architecture §6). T3.
4. **KB feed** — replace seed KB constant in `agent.ts` with approved معرفة المنتج items.
5. **Campaign API + dashboard tracker screen** (Next.js RTL, prototype `kmon` spec). T3,
   Designer engaged.
6. **Production number migration** — real KSA WABA + template submissions (human approvals
   throughout). T4 when scheduled.
7. **Rotate OpenAI + Gupshup keys** (they transited chat on Aug 10) — one `fly secrets set`
   + dashboard rotation; anytime.

## Decision log  (append-only, newest first)
- 2026-08-11 [cpo] **ACCEPT @5b373ea** — per-product معرفة المنتج (grid → product page,
  scoped upload). Reviewer 8.5/10, zero must-fix. Follow-up logged: wrap the kb-hash
  decodeURIComponent in try/catch (malformed hand-typed hash blanks view until nav).
- 2026-08-10 [cpo] **ACCEPT-WITH-CONDITIONS @ 7702dfb** (agent v2 + dashboard, sandbox
  scope). Conditions gating production: (1) BINDING live opt-out E2E before real-customer
  sends; (2) load real brochures into ASSETS_JSON before claiming media; (3) Postgres
  persistence; (4) close AC7 handoff + AC8 failure-path testing. massar-engine now under
  git (local only).
- 2026-08-11 [decision] **FIXED** the route-boundary defect: `.orbit/checks/route.py` now
  exits silently on system/background turns (markers: SYSTEM NOTIFICATION / task-notification
  / Stop hook feedback) — no stamp, no classify, no injection. Stage events no longer get
  orphaned mid-run. Note: scaffold refresh will flag route.py as customized (expected;
  never clobbered). Was: stamped a boundary on every prompt-submit → 3 false Stop blocks.
- 2026-08-10 [decision] `fly deploy` of massar-engine reclassified human→auto per the
  user's standing instruction ("once done, just deploy it and fly"); guard rules keep
  deny on apps-destroy/secrets-unset and ask on Gupshup curls + admin/send. Revertable.
- 2026-08-10 [decision] gpt-5.6-terra + function tools on chat.completions requires
  `reasoning_effort:"none"` (per API 400); Responses API migration noted as the seam.
- 2026-08-10 [decision] Orbit installed; loop limits: 6 iters / $5 run / 45 min; WhatsApp
  sends to real customers = human checkpoint; `fly apps destroy` + secrets-unset = denied.
- 2026-08-10 [decision] Webhook payload format = **Meta (v3)**; engine parses v2 + v3;
  source number auto-learns from v3 metadata.
- 2026-08-10 [decision] Gupshup sandbox app "Massar", source 917834811114 (India sandbox);
  production number is a later migration.
- 2026-08-10 [decision] Stack: Node/TS end-to-end; OpenAI gpt-5.6-terra pinned via env;
  Fly.io app `massar-engine` (personal org, fra).
- 2026-08-10 [decision] BSP = Gupshup (user-supplied credentials) — superseded Meta-direct.

## Cycle log  (append-only, newest first)
- 2026-08-13 [T3] **Segmentation UI + agent prompt v2 @c06f71c** (R49 «ابحث… قارن بتسع أدوات ثم ابنِ»,
  R50 «do the UI and then update the agent prompt»).
  **Builder** in campaign wizard step 2 as a «حسب السلوك» mode beside the file-attribute picker —
  placed there deliberately: a behavioural audience is outside WhatsApp's 24h window by
  construction, so choosing it away from the message is how WATI and AiSensy let you build a list
  you may not send to. Preset shelf FILLS the condition rows rather than hiding them; window chips
  ٣/٥/٧/١٤; every zero states its reason (cooldown count, tenure forecast).
  **Prompt v2** installed as the founder authored it (Goal/Context/Expectations/Sources + decision
  engine + stage transitions + منصة صحة paths + pre-send checklist), with EIGHT guards from prior
  safety rounds carried forward inside it — a previous rewrite dropped four and they had to be
  rebuilt. Safety located all eight by line and ran 21/21 adversarial ordering.
  **Defects the roles found in my own work, each fixed:** the launch list was built from a 12-row
  DISPLAY sample, so a segment matching forty would have sent to twelve and reported 12/12
  delivered; the builder promised «قالب معتمد» while the launch path only sends session messages,
  so the button would have produced a send WhatsApp refuses AFTER confirm — behaviour mode now
  yields no targets and says why; the launch bar showed «٠ جهة استهداف» beside a live-looking
  button; an unknown signal returned 500 leaking an internal message; the presets endpoint ran five
  UNCAPPED scans per page load while its sibling capped at 20k to protect the opt-out webhook;
  switching a condition to «لم يحدث» made the window chips a silent no-op on that row; fast edits
  could leave a count belonging to a different segment on screen.
  **And a correction to my own earlier claim**: the smoke gate's third-party filter tested
  `m.text`, but a resource 404 carries no URL there — it is in `m.location.url`. The filter never
  matched, so Google's font CDN kept failing the deploy ~1 run in 3, and the three clean runs I
  cited were luck. Fixed and re-verified 5/5.
  **Scope, stated plainly:** roughly one move of three. An audience can be defined and previewed;
  it cannot be saved, scheduled, or launched from. The send path needs the production WABA number
  and Meta-approved templates. Benchmark: `.orbit/artifacts/segmentation/BENCHMARK.md` (11 tools).
  Gate PASS (71 scenarios, 18 comparisons); safety PASS; reviewer 8/10. CPO round-23 in flight.

- 2026-08-13 [T3] **Segmentation engine @ea6515c** (R49: «ابحث عنه… قارن بتسع أدوات على الأقل، ثم ابنِ»).
  Benchmark of **11 platforms** first (.orbit/artifacts/segmentation/BENCHMARK.md): Klaviyo ships the
  founder's exact case as a preset with the same 5-day window; the market's five primitives are event
  did/did-not-happen · relative window · frequency · AND/OR · live membership; and the standard segment
  names are WATI's «Ignored»/«Read only (didn't reply)», AiSensy's «Replied», Attentive's winback,
  HubSpot's unengaged. We reuse those names rather than invent Arabic.
  **src/segments.ts** implements them over the existing ledger, plus three things the study said the
  market gets wrong: WATI and AiSensy split behaviour (campaign analytics) from attributes (segment
  builder) so the two never join and nothing prevents a double send — here a segment is ONE object and
  a cooldown is enforced at evaluation with the excluded contacts RETURNED, not dropped; Customer.io's
  documented tenure trap is handled by separating contacts younger than the window and forecasting when
  the segment starts matching; and opt-out is never a segmentable audience whatever the conditions say.
  «مهتم بلا موعد» has no competitor equivalent — no benchmarked tool joins an AI-read intent to a
  missing human outcome. Endpoints: POST /admin/segments/preview · GET /admin/segments/presets (both
  read-only, neither can send). 7/7 unit matrix; the matrix caught a real semantic bug — bounding the
  NEGATIVE matched people read six days ago as «never read», so the window belongs on the positive
  signal (Klaviyo's «Before»). Live proof: «مهتم بلا موعد» → 1 match with 3 contacts correctly
  suppressed («رُوسلت قبل ٢٠ ساعة»), and the founder's own case correctly reports «not yet» —
  4 contacts too new, first match in 5 days — instead of a bare zero that would read as broken.
  **UI not built yet**: designer spec ready (behavioural mode inside wizard step 2, preset shelf,
  template binding because the audience is by definition outside the 24h window, tenure state).

- 2026-08-13 [T3] **UI-quality increment — CPO ACCEPT @1936a22 (9·8·8·8·6, zero musts)**, hardened to
  76ff28a. R48 «fix all issues and best UI must be delivered», six acceptance rounds.
  **Campaigns list** made to read as deliberate: sparse-state explainer, the pager that could never
  move removed, the un-switchable switch replaced by a status marker, an in-UI reclassify control
  replacing an authenticated curl, and the list capped with the remainder declared. **Launches now
  classify themselves at creation** from provenance, so the list stays clean without hand-flagging.
  **Every invented number deleted**: the hardcoded «جاهزية الأقسام — 92%» card with its fabricated
  pricing, and the six authored knowledge scores (92/74/71/55/55/63) that were live on seven
  surfaces with inverted grammar — the two services that HAVE knowledge showed none. Both replaced
  by cards computed from real state that say «يتعلّم» when there is nothing to report.
  **Defects the rounds caught in my own work, each fixed:** the opt-out check sat BELOW the sandbox
  branch and swallowed six real opt-out phrasings (safety VETO); a migration ALTERed a table before
  creating it, which would silently drop a restored database to memory-only; a mobile rule misaligned
  every value from its label below 900px so a four-clinic campaign read «٠٪»; the command centre's
  KPI row and funnel measured disjoint populations and rendered «ردّوا ٤» above «ردّوا ٠»; a regex
  sweep shipped `Math.roundfmtN` — a live TypeError past tsc, node --check, smoke and 57 scenarios;
  and removing the invented scores briefly made six services claim Product Hub knowledge they lack.
  **Numerals unified** across the whole demo path (zero Latin digits on six screens, verified in the
  rendered DOM and under a clock aged 12h — a card that only renders past 24h idle would otherwise
  have started mixing systems at 14:48 Riyadh mid-demo).
  **Guards added, each falsified:** `npm run check:numerals` (source-level, catches state-gated
  cards a DOM audit cannot see, and publishes its own miss rate — 21 mutations written, 18 passed),
  `npm run check:catalogue`, and `npm run smoke` fixed to stop failing on Google's font CDN. Font
  stack now degrades through real Arabic faces so the demo does not depend on room wifi.
  **Segmentation research delivered** (R49): 11 platforms benchmarked, `.orbit/artifacts/segmentation/BENCHMARK.md`.
  Carried, none demo-blocking: 375px chip overlap on the campaign audience table (pre-existing);
  no service-creation UI; launch classification unproven because proving it requires a send.

- 2026-08-12 [T2] **Round-14 closures + the Proxy defect @3725740→8ff3f75.** CPO round-14 returned
  **ITERATE** on 9b7cd54 (5 musts). Closed: **M1** — the falsification survived the tag scrub in a
  different store (`product_interest` in `contact_insights`), so «باقات NVR لتغطية 8 مواقع» was still
  on #home as a won deal; service names are now clamped to the catalogue on parse, on aggregate AND
  at the read boundary (17 free-text names → 5 real services), and an assistant reading renders
  hollow/dashed with a «قراءة» marker so it cannot pass as a confirmed tag. **M2** — two predicates
  legitimately differ, so they stopped sharing a word: «ابدأ التواصل مع ٢ جهة تستحق المتابعة» beside
  «جهات مهتمة (١)». **M3** — `replaceTags` stamped `Date.now()` and moved four real customers'
  history hours forward; ts is preserved, the timeline anchors a tag to the message that produced it,
  the DB write is transactional, and an unknown phone 404s instead of manufacturing a contact.
  **M4** — the guard is wired into `npm run deploy` with a runnable venv, covers `#customer/<phone>`,
  and was falsified (exit 1 on a missing landmark). **M5** — actuals re-captured at HEAD; four
  comparisons now have genuinely non-zero ratios, the 375 baseline replaced openly because the old
  one never contained the stepper, stale SC claims repointed to evidence that can carry them, and
  round-13's NVR rationale corrected on the record.
  **Mid-round, user-reported («this is not ok»): the Gupshup sandbox activation phrase.** Every new
  person must send «proxy <botname>» after an English bot-platform boilerplate; that arrived as the
  customer's first message and the model answered it as a product enquiry — all four real
  conversations opened «هل تقصدون خدمة باسم Proxy Massar؟», and Ibrahim's escalated a human handoff
  for a service that does not exist. Now matched in code before the model (16/16 matrix, both
  spellings, length-capped) and answered with a real Arabic opening; markdown banned (the agent had
  sent «**بروكسي مسار**», which WhatsApp renders literally). The boilerplate itself only disappears
  on the production WABA number. Gate PASS @8ff3f75; smoke 7/7; health green.
- 2026-08-12 [T2] **Demo-readiness pass @9b7cd54→3725740.** (1) **Service names clamped to the
  catalogue** — فهم المساعد named services in its own words, so 17 distinct strings existed for
  5 real services and the home board invented rows for things Lean does not sell. «باقات NVR
  لتغطية 8 مواقع» was rendering as a **won deal on a real customer**, for a packaging the agent
  had itself refused in-transcript as outside its approved knowledge — i.e. the round-13
  falsification class survived the tag scrub, in the *insights cache* rather than in tags.
  `canonicalService()` now clamps on parse AND on aggregation (cached rows fixed on read, no LLM
  re-run); unmatched share one «خدمة أخرى» bucket. Live-verified: board reads خدمات التطعيمات ·
  تكامل الأنظمة · الإجازات المرضية · خدمة أخرى; loss causes intact; smoke 6/6, health green.
  (2) **Pixel baselines frozen** (`.orbit/qa/baselines/`) — the visual gate compared each capture
  to itself, so a blank page passed; gate re-run PASS. (3) **WAKE-UP + DEMO-SCRIPT rebuilt on
  verified live data**: corrected terminology (مكتسبة/غير مكتسبة · ما يستحق المتابعة الآن ·
  الخدمة), removed the false "file + text + buttons in one bubble" claim, and added the one
  mandatory pre-demo step — **the sandbox reveal must be ON**, because the four real conversations
  are all still active, so the real-only loss board is legitimately empty and campaign 5 /
  عيادات النخبة are hidden. (4) **Safety re-verified from the ledger**: every real contact's first
  event is inbound — no cold outbound to a real customer. Note `kind:"camp"` in buildTimeline is
  any agent message containing `[أزرار:`, so ordinary button replies are mislabelled «حملة» on the
  profile (open, cosmetic). CPO round-14 dispatched against 9b7cd54.
- 2026-08-12 [T4 MISSION] **Overnight rebuild @7db6509→43a5015** (R32 hard rejection + R33
  expert panel + R34 8h autonomous mission for a team demo). 4 specialist agents delivered
  (reference-fidelity, cm.com design-spec, marketing-intelligence, agent-evaluation) →
  .orbit/artifacts/expert-panel/. Shipped: (1) **win/loss intelligence** — every conversation
  judged won/lost/stalled/active with a taxonomy loss cause, verbatim evidence, and what
  would have won it; home board ranks causes/drivers per product (live proof: «الملف غير
  واضح» and «التوقيت» extracted from real seeded threads). (2) **Design rebuilt to the
  reference images** — unified neutral scale, border-first cards, SVG icon sprite (no
  emoji), Emaily campaigns anatomy (tabs/toolbar/toggles/dot-chips/progress/kebab/CSV),
  Tableau home (icon KPIs, stage-bar funnel with drop-off, navy treemap), prediction-panel
  profile with rail timeline, campaign-detail verdict strip, motion system + count-up.
  (3) **Agent fixes** — opt-out false positive («كيف أوقف التزوير؟») repro'd and fixed,
  turn-cap dead end fixed, single bubble enforced in CODE, caption-carrying send_asset.
  (4) **PDF now truly one bubble** (document+caption) — his device complaint fixed at the
  wire level. (5) Product Hub interconnected (campaigns + market verdict + launch CTA).
  Gate PASS @e6f421a (21 captures, 0 console errors). Reviewer: 6.5 BLOCKED on three real
  demo risks (opt-out matcher missed «أوقفوا الرسائل»-class phrasings; bubble suppression
  could silence a missing-asset reply; KPIs re-animated every 5s) → ALL FIXED @e9a735a with
  an executed 22/22 opt-out matrix, plus shoulds (file-marker drift, data-attribute CTA,
  turn-cap PM alert) and @e6f421a (win/loss respects the sandbox boundary). Demo script
  written: .orbit/artifacts/night/DEMO-SCRIPT.md. **CPO ROUND-9 ACCEPT @e6f421a —
  9·9·9·9·9, demo risk LOW** ("the anatomies he sent are recognizably present, in Massar's
  own language, with numbers that are honest everywhere"). Its watch items landed @ab4b847
  (opt-out 26/26 stem-anchored, toggle a11y, nav highlight) plus the hub capture and an
  outcome-click scenario. Post-ACCEPT additions: campaign next-move engine, human outcome
  buttons, stall window, CSV guard. Final gate PASS @ab4b847; health green.
- 2026-08-11 [cpo] **ROUND-8 ACCEPT @4a40ab9** (intent 9 · taste 8) — R27-R30 all
  DELIVERED-VERIFIED; reviewer re-score 8.5 PASS bound; both waived-shoulds executed
  post-ACCEPT (@4c18d20 svg token, @bf63dee profile title) w/ evidence rebound + gate
  PASS @bf63dee. User-model Rules promoted: (1) marketing-tool fit bar, (2) numbers
  real/sourced/honestly bounded, (3) briefs by reference artifact — adopt pattern never
  palette. Ledger: treemap Massar-ramp recolor, campaigns empty-filter row, learning
  badge wording, watermark+timestamp key, detail test-awareness, campaign-engine epic
  (server-side segmentation/pagination + indexed profile queries + batch upserts).
- 2026-08-11 [cont] Intel cycle extended → @4a40ab9: reviewer intel round 7.5 BLOCKED
  (M1 snapshot-cap froze watermark for active contacts — repro'd; M2 no LLM
  degradation/timeout) → both fixed @c27a3a7, M1 growth-recompute LIVE-proven (5→6
  turns → fresh accurate read). R29 (Tableau reference): rate KPI strip + trapezoid
  funnel SVG + size/sector columns + city treemap @a3617ab. R30 (Emaily reference):
  campaigns list = tabs/search/sort/rate-columns/progress-bars @4a40ab9. Gate PASS
  @4a40ab9; reviewer re-score in flight; CPO round-8 next.
- 2026-08-11 [T3] **Customer-intelligence pivot @9d99ea5→ef6353a** (R27: reference
  screenshots — "not PMF yet, revise functions/UI, how do we really get value"; R28:
  "dashboard is a must"). Built العميل ٣٦٠: src/insights.ts فهم المساعد (LLM-read
  intent/signals/objections/next-action/best-time from the contact's own ledger; honest
  Learning gate <2 inbound; PG cache by transcript watermark; ZERO outbound capability) +
  deterministic 8-part context score + unified timeline; GET /admin/customer/:phone +
  /admin/insights (cached list reads). Portal: #customer/<phone> profile (identity header,
  vertical context rail, timeline card, فهم المساعد card w/ الخطوة التالية block);
  rows/home/customers now lead to profiles; home = analytics dashboard (funnel, 14-day
  stacked activity SVG — RTL-visibility fix @ef6353a, interest by product, targets by
  city; respects real/test toggle); giant dropzone → compact toolbar; emoji chips → toned
  text badges. Live proofs: rich-transcript read is ACCURATE (verbatim signals, concrete
  next action, context 100 8/8), learning state honest, cache hit proven, 404 clean,
  charts render. Gate PASS @ef6353a. Reviewer round 3 in flight; CPO round-8 next.
  Honesty rule kept: no fabricated churn %/LTV — AI reads labeled فهم المساعد.
- 2026-08-11 [cpo] **ROUND-7 ACCEPT @16defb6** (intent 9 · taste 9); waived should
  (dup style attr) fixed+deployed @89b1b4e. Rule 1 promoted in user-model: professional
  marketing-tool fit = standing acceptance bar. New ledger orders: test-aware campaign-
  detail stats, entity-delete confirm, campaign-engine bundle (server-side segmentation/
  pagination, batch tx upserts, persistent alert throttle, per-conversation deep link,
  portal-editable PM number).
- 2026-08-11 [T3] **Growth cycle @48bba0c→987168e** (R20 "not happy w/ UX + no retargeting +
  serious-lead next action", R21 embedded file+buttons, R22 PM number, R23 sandbox
  separation — four mid-cycle directives, one delivery). (1) **Lead alerts**: hot tag/
  handoff → WhatsApp lead card to NOTIFY_NUMBER (code-level, 6h throttle, self-alert
  guard, event-logged) — live-proven: simulated hot lead → card on the PM's phone,
  throttle held on escalation; number surfaced on home. (2) **Embedded launch**: ONE
  bubble = intro PDF + personalized caption + 3 reply buttons (sendQuickReplyDocument;
  fallback only on Gupshup shape-rejection — reviewer's double-send note fixed);
  campaign 3 live proof on the PM's phone. (3) **Retargeting**: campaign detail's
  filtered cohort → «⟲ إعادة استهداف» → wizard locks the cohort (gold card, prefilled
  name) — browser-proven. (4) **UX pass**: vHome = real overview (KPI band, hot-leads w/
  conversation links + alert-number footer, campaign minis, quick actions); wizard sells
  hub products (registry), preview shows the embedded bubble, sticky launch bar.
  (5) **R23 separation**: contact.test persisted (auto PM number, manual panel toggle) —
  real-only KPIs/lists + «إظهار التجريبية» toggle + «تجريبية» campaign chips, browser-
  proven incl. poll survival. (6) **Audience-slice reviewer round**: initial 7/10 BLOCKED
  (sci-notation phone corruption repro'd; paste bypassing normalization) → fixed + two
  shoulds (رقم header order, 9660 prefix) → re-score **8.5/10 PASS**. Gate PASS @987168e.
  Growth-slice reviewer round dispatched; CPO round-7 next. Ledger adds: batch upserts,
  skipped/skippedCount naming, stale entFilters key, per-campaign alert deep link
  (#kmon link is generic), NOTIFY_NUMBER portal-editable setting (prod migration).
- 2026-08-11 [T3] **Audience file onboarding @874a130→0eafcd3** (user R18: "onboarding
  through file… segment by city etc — current flow is not ok" + mid-turn R19: template
  download + 400k-scale UX). entities.attrs JSONB (schemaless columns); src/audience.ts:
  SheetJS parse + Arabic/English header auto-map + KSA phone normalization (05/٠٥/bare-5/
  00-prefix → 966, Arabic digits); POST /admin/entities/import (upsert-by-phone, per-row
  Arabic skip reasons, 5000-row cap); GET /assets/audience-template.xlsx (fill-in template,
  button in dropzone). Portal: العملاء = dropzone-first (detected-columns echo, paste
  demoted, search, capped list); wizard step-2 = chip groups derived from file columns w/
  live counts (OR within key, AND across), LIST_CAP 60 preview + count-forward summary bar
  + mass-select-all + modal >50 cap warning. Round-6 next-touch orders folded same commits
  (convoSig freshness, setHuman res.ok, dup pick). Live proofs: 5-clinic xlsx E2E (all 4
  phone forms normalized), idempotent re-import, 422 Arabic failures, template round-trip,
  308-entity at-scale browser proof (60 rendered, summary bar, select-all 308, cap warning),
  0 console errors; test rows cleaned. Delivery gate PASS @0eafcd3. Ledger: server-side
  segmentation/pagination is the real 400k answer (client fetches all entities today) —
  schedule with campaign-engine slice; value-chip cap 12/group needs "+more" affordance
  for high-cardinality columns.
- 2026-08-11 [T3] **Campaign-tracker UX redesign @19b6f00 → round-5 musts closed @bbe40dd.**
  User: "this page as UX is very bad… clicking a user opens all chat, horrible". Researched
  marketing-platform patterns (Mailchimp report: rate stat-cards as funnel; Intercom/WA-Web:
  inbox side panel). Rebuilt #kmon/<id>: tight header → 6-stat card grid (count + % + mini-bar)
  → table-first card with filter chips + search in header; row click → conversation SIDE PANEL
  (backdrop, header chips, thread, takeover footer) instead of full-page chat dump. Skill zip
  hosted as __skill__ asset → تحميل المهارة ⬇ card in معرفة المنتج (answers "where can I
  download the skill"). CPO round-5 ITERATE caught 3 real regressions of mine; fixed @bbe40dd:
  window.setHuman restored (dead takeover button), __skill__ fenced out of agent KB/send,
  refresh made non-destructive (signature-guarded panel rebuild, scroll+focus+caret preserved,
  Escape/hashchange close, mobile affordance). Proven in a REAL browser at bbe40dd: mute→resume
  roundtrip, typed search survives full poll, 0 console errors; contact left clean. Delivery
  gate PASS @bbe40dd (SC-15 + 3-viewport re-captures; 375 re-baselined for the intentional
  mobile affordance). Round-5's zip-rename nice-order rejected with evidence (VERSION=2.1.3,
  premise false). CPO round-6 envelope: dispatched, pending verdict.
- 2026-08-11 [T2/T3] **Intro-PDF feature + skill compatibility @8ac9754→83fd490.**
  (1) Per-product intro PDF: upload zone on each product page → PG bytea → public
  unguessable /assets/<id>.pdf → agent sends it with the product opener and on any
  details/brochure request (send_asset by product); campaign launches auto-attach it.
  Live proof: user asked for the file → real PDF delivered on WhatsApp + hook line.
  Multipart field-ordering bug found+fixed both sides. (2) lean-proposal-deck skill
  (v2.1.3, VERSION file verified) inspected: extraction prompt now maps its canonical 8 sections; REAL skill
  deck (صحة أعمال Plus) ran through prod → clean 2927-char hub doc; agent now sells
  that product too. CPO envelopes: round-3 ACCEPT @8ac9754; round-4 pending @83fd490.
  Note: with the grid uploader removed, NEW products enter via admin API ?product= —
  a products-module UI (per prototype المنتجات) is the eventual home for adding products.
- 2026-08-11 [T2] **Dead-air fix @43a9717** (user: "the agent doesn't conversate — why").
  Root cause: handoff outcome set human=true → permanent mute with no human team to pick
  up (3 real messages unanswered). Fix: handoff = prompt context only; human flag = explicit
  portal takeover toggle (transcript drawer: إيقاف/استئناف المساعد, chip when muted,
  admin endpoint, persisted+event-logged). Live proof: flag reset → real unanswered «الو»
  replayed → agent apologized and continued the demo thread.
- 2026-08-11 [T3] **kmon redesigned to fit the use case @c00760a→859bdea.** Campaigns are
  now persisted launches (name/product/message/targets) → list view (prototype table,
  per-campaign stats) → per-campaign detail (scoped funnel + filter chips الكل/شوهدت/
  ردّوا/مهتمون/فشل + tracker + transcripts) + محادثات خارج الحملات. Wizard gained campaign
  name; launch lands inside its campaign page. Mid-cycle user question ("where is what
  they're interested in / how serious") → dedicated الاهتمام والجدية column (product ·
  جاد🔥/مهتم/فاتر from agent tags) + unified interested predicate. Live proof: pricing ask
  → exact tiers quoted → tag hot → handoff → column populated. Reviewer 8.5 no must-fix;
  CPO ACCEPT. Follow-up queued: phone→contact Map when contacts scale; tx around
  campaign+targets insert.
- 2026-08-11 [T1] Grid uploader removed per user correction @b66bce0 — uploads scoped to
  product pages only; deployed + verified.
- 2026-08-11 [T3] **Audience module + Product Hub shipped @c2ae576.** (1) Entities
  (name/phone/size/city): paste-import + manager in العملاء; wizard step-2 = researched
  picker (segment chips + live count + search + individual checkboxes + select-matching);
  launch = human-confirm modal → capped 50 → personalized {name} sends → statuses live in
  kmon (proven: sent→delivered→read on opted number; async 1008 failure surfaced for
  non-opted). (2) Product Hub: PDF pitch-deck upload in معرفة المنتج → pdf-parse v2 →
  gpt-5.6 extraction → structured Arabic MD in Postgres → rendered for humans + injected
  into the live agent prompt (proven E2E with a real deck; hub doc «إصدار وإدارة الإجازات
  المرضية» is live). Two incidents caught+fixed by the loop's own gates: pdf-parse v2 boot
  crash (deploy), template-literal newline breaking page JS (found by visual QA — the
  pixel evidence caught a blank page). Delivery gate PASS. Extractor swapped to **Firecrawl AnyDoc** per user directive (@b97244d,
  prod-proven via:anydoc; pdf-parse fallback; uploads now accept PDF/Word/PowerPoint).
  Awaiting user's real target list + skill-generated decks.
- 2026-08-11 [T3] **Portal v0.2 — original Massar design** (user correction: "I don't see
  Massar original design"). Rebuilt /dashboard as the prototype shell: navy sidebar with
  grouped nav + glyphs + gold-tint active state, topbar, marketing module screens —
  متابعة الحملات LIVE (funnel + tracker + transcripts), إنشاء حملة wizard (faithful,
  launch gated pending campaign engine), معرفة المنتج readiness view (real agent KB),
  original empty-state pattern elsewhere. Deployed @635da07; 12/12 DOM design markers
  PASS; pixel-diff not captured (no Playwright) — recorded limitation. Prototype
  (مسار.dc.html) promoted to binding UI spec in user memory.
- 2026-08-10 [T3] **Agent v2 + live dashboard shipped.** Agent: 6-product KB with
  efficiency pitches, closer persona (light emoji, ≤4 lines, never-dead-end, pivot matrix),
  send_buttons + send_asset tools (media adapter: image/PDF), assets registry (env
  ASSETS_JSON, empty pending real brochures). Dashboard: /dashboard (RTL, design-language
  tokens, 5s refresh, token-gated via /admin/state). Live 3-turn suite PASS (planner's
  proof bar met): interest→buttons+tag; objection→reframe; rejection→pivot; 3/3 delivered,
  zero 400s. Designer stage ran INLINE (async runner stalled 2×) — recorded. Dashboard
  opened in the user's browser.
- 2026-08-10 [orbit-setup] Scaffolded Orbit (surfaces web+api → frontend-engineer,
  backend-engineer, designer + standard spine); authored CLAUDE.md + 2 domain skills;
  tuned loop.config.json; added 6 Massar guard rules; hooks + reporter active.
- 2026-08-10 [backend] Added Gupshup v3 (Meta-format) webhook parsing + source-number
  auto-learn; set sandbox number/app name; deployed; verified health + v3 status ingestion.
