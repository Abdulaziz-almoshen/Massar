# User model — Massar

Owned by the CPO (see `.orbit/skills/product-acceptance.md`). Updated on every CPO
verdict. Evidence = the user's own words and choices only. Project-scoped — never
copied to other repos or global memory.

## Rules (durable — 3+ consistent signals each)

1. **Professional marketing-tool fit is the standing acceptance bar** for every marketing-module
   screen: he judges Massar screens against how best-in-class marketing platforms
   (Mailchimp/Klaviyo/HubSpot-tier) build the same surface, and "works but looks like an admin
   script" fails. (evidence: R15 "redesign this page to fit the use case"; R17 "see how marketing
   platforms build campaign trackers — clicking a user opening all chat is horrible"; R18/R19
   "onboarding should be through file, then segmented… current flow is not ok" + "400,000 numbers
   would look very bad — do better UX"; R20 "not happy with the UX/UI for creating a campaign and
   clients and dashboards; there is no retargeting". Promoted at round-7, 2026-08-11.)

2. **Numbers must be real, sourced, and honestly bounded — never invented.** Default views show
   real-only truth (test traffic behind an explicit toggle); AI readings are labeled as the
   assistant's understanding (فهم المساعد) and grounded in quotable evidence with honest
   learning/degraded states; no fabricated probabilities, scores, or estimates (churn %, LTV);
   honest zeros beat demo numbers; captions state the data source («لا تقديرات», «من أعمدة ملفك»).
   (evidence: R23 "separate campaign data from users talk in sandbox"; R27 "fires don't make
   sense… worry about how we really get value"; R29-R30 era — honest-data captions explicitly
   valued in the reviewed checkpoint. Promoted at round-8, 2026-08-11.)

3. **He briefs by concrete reference artifact — adopt the PATTERN, never the palette.** His specs
   arrive as screenshots/links of real products (CXP profile, Tableau dashboard, Emaily campaigns
   list) or his own phone captures; "follow this" means re-express the referenced structure and
   information grammar in Massar's own design language (navy/teal/gold, RTL, Arabic), not clone
   the reference's branding or colors. (evidence: R17 marketing-platform prior-art; R21 his-phone
   screenshot "the file should be embedded… show buttons"; R27 CXP screenshots "this is the type
   of things I want"; R28 Tableau link "dashboard is a must"; R29 Tableau screenshot; R30 Emaily
   screenshot "follow this". Promoted at round-8, 2026-08-11.)

4. **AI features must explain CAUSALLY, with the customer's own words as the evidence.** Any
   intelligence surface has to justify its own reading from the ledger — the reading, the reason,
   and the verbatim quote that proves it — or it reads as decoration to him. Corollary: a status
   widget that cannot justify itself does not ship. (evidence: R27 "fires don't make sense… worry
   about how we really get value" — decorative 🔥 chips rejected; R28-R30 real-numbers/Tableau
   cluster; R34 "why we could sell / why we couldn't sell — maybe user issue, product issue,
   communication issues, the file is not clear"; R41a, where the accepted shape of the sales path
   is stage + «لماذا هذه المرحلة» quoting his own customer back at him. Promoted at round-11,
   2026-08-12.)
5. **Zero outbound WhatsApp — no test is an exception, and he names the number.** Not "no cold
   sends to real customers": no WhatsApp message at all, of any kind, to anyone, until he
   personally supplies the number to test with. This is stricter than CLAUDE.md §8's current
   wording, which still permits sandbox self-tests to the team's own opted-in phones — that
   carve-out is withdrawn. (evidence: R47/U34 2026-08-12 "Don't ever send a text to the client
   for any test or anything. Don't shoot any WhatsApp message at all. Okay? Stop shooting
   messages, and I will tell you what number you need to test with"; consistent with R2's
   protect-the-number instinct and with §8's existing human-approval checkpoint, which he has
   now tightened rather than relaxed. Promoted at round-15, 2026-08-12.)
6. **Stopping the leak is not wiping the spill — a fix must clean the artifacts the defect
   already produced.** Removing the write path, the row, or the code that caused a wrong thing
   leaves the wrong thing on every screen it already reached. Enumerate the derived surfaces —
   counters, aggregates, chips, next-actions, timelines, and above all the stored transcripts he
   will actually open — before calling anything fixed. (evidence: round-13, the fabricated tag
   deleted from `contact.tags` while `contact_insights` kept asserting it; round-14, the row
   removed while three derived surfaces still made the claim; round-15, the Proxy matcher landed
   forward-only while all four real transcripts still open «هل تقصدون خدمة باسم Proxy Massar؟».
   round-17, the campaigns list unified its numerals while #kmon/<id> — one click away, and where
  the demo goes next — still renders «4 من 4» beside «الكل (٤)», with #home, #aimkt and #kb also
  still mixed. FOUR consecutive rounds, same shape. Promoted at round-15, 2026-08-12; reinforced
  at round-17, 2026-08-13. Corollary added at round-17: when a fix is stated as a page-level
  PROPERTY, assert that property across every screen that shares it — by measurement, not claim.
  SIX consecutive rounds as of round-19, 2026-08-13. Second corollary added at round-19: the
  enumeration must run over STATES as well as screens, and it must run over the SOURCE, because a
  live-DOM measurement is structurally blind to a branch that is not currently rendered.
  SEVEN consecutive rounds as of round-20, 2026-08-13. Third corollary added at round-20: an
  audit's SCOPE must be derived from the system — every branch of the router's dispatch, including
  sub-routes — never from a human's recollection of which screens were named last round. Round 20
  honoured the STATE corollary in full and still lost, because the six audited routes had not
  changed since round-17 and the defect simply moved to route seven, #kb/<product>. Any scope
  typed by hand is a scope that freezes.
  STATUS at round-22, 2026-08-13: the eight-round streak BREAKS — the fourth corollary was followed
  exactly and closed all seven surfaces in one edit. Rule retained, not demoted: it bit once more at
  reduced severity, producing the FIFTH COROLLARY — when a fix introduces a NEW DISTINCTION the
  product had no word for, teach that word to every surface that speaks about the same objects in
  the same edit. A vocabulary that exists on only one screen is a contradiction, not a fix.)

7. **The loop's own claims are subject to Rule 2.** Every number, count and property assertion the
   loop makes ABOUT ITSELF — in evidence files, commit messages, check output, and reports to the
   CPO — must be bounded by what was actually measured. A green check that asserts a property it
   does not verify is worse than no check, because the next role in the chain cites it as proof.
   AMENDED at round-21: the original wording added «the bias is consistently toward OVER-claiming,
   never under-claiming». That is falsified — at e4facd0 `visual.note` says «16 comparisons» over an
   array of 18, an UNDER-claim. Drop the direction clause. What is constant is the CHANNEL, not the
   direction: the loop's PROSE about its evidence is unbounded by its evidence, while the evidence
   itself has been clean for two rounds. Four-for-four across rounds 18-21.
   (evidence: round-18 «portal-wide numeral sweep» for a six-screen sweep; round-19 «13 real
   non-zero ratios» when 12 were non-zero; round-20, three at once — «15 comparisons, all with
   genuine non-zero ratios» when salespath@375 is 0.00000, «S6 shipped… ONE numeral path» when
   four surfaces still render Latin, and `check-numerals.mjs` printing «every number in
   src/dashboard.ts routes through fmtN()» at a commit where that is false on four live sites.
   Promoted at round-20, 2026-08-13.
   STATUS at round-22, 2026-08-13: FIRST CLEAN ROUND in four, on every axis this rule has ever
   caught. The mechanism that cleaned it is worth keeping: the loop stopped describing its
   instruments and made the instruments describe themselves — the guard publishes its own miss
   rate, the evidence note's count matches its array, and the re-baseline states that the image is
   not what carried the evidence. Rule retained; a check that reports its own failure rate cannot
   be quoted upward as proof of a property.)

## Signals (dated observations, newest first)

- 2026-08-14 U59 [stated]: R59, his own framing of the working contract: 'I give you a goal, and you'll give me a deliverable.' Two hard rules follow. (1) INCIDENTAL WORK RUNS SILENTLY: technical debt, prerequisites and self-inflicted fixes must not consume his attention or his turns - do them without narrating each step, or defer them. He should be interrupted only for a decision only he can make. (2) HIS TIME IS THE SCARC…
- 2026-08-13 R48/R49 [stated, CORROLARY to Rule 2 — third instance, promote into the Rule next round]:
  «this doesnt represent the real interation make it reflect the agent and customer feedback», then
  «just sent a campaign why this data is not real? the user hasnt seen it». **The corollary: a number
  attributed to an EVENT must be scoped to that event.** Both defects were the same shape — lifetime
  contact state rendered as event state. The campaign screen credited a fresh send with replies from
  33 hours earlier and reported failed 0 while both sends had actually failed; the profile gauge
  scored fields we hold on file and read 80% on a customer whose only sentence was «ماني مهتم لا
  تتصل علي». **How he catches it**: he validates against his own lived experience of the event — he
  had just pressed send, so he knew nobody had seen it. Any screen that describes something he
  personally witnessed will be checked against his memory of it within seconds. **How to apply**:
  before rendering any count on a screen about a THING (a campaign, a message, a turn), ask what
  window it belongs to and window it explicitly; never let lifetime state stand in for event state.
  Prior instances: round-13 the fabricated tag surviving in a second store; the home KPI/funnel
  mismatch counting disjoint sets.

- 2026-08-13 R47 [stated, THIRD consistent signal — promote to a Rule next round if it holds]:
  «try to do it quick you take too much», then «finish these as quick as possible». Said directly
  after I recommended holding a commit for another review pass. **The signal: he wants momentum and
  a short reply, and he experiences the loop's deliberation as cost.** Consistent with R46 («dont
  worry about template pretend it is approved») and the 2026-08-10 standing deploy instruction
  («once done, just deploy it and fly»). **How to apply**: deploy on his word without re-arguing;
  run verification in PARALLEL rather than in sequence; report in a few lines, lead with what he can
  now do, and put process detail behind a single sentence. **What it is NOT**: permission to skip
  the §8 safety wall or the zero-send rule — he has tightened those himself, never relaxed them, and
  the two defects found this round (a button emitted as its own opposite; a price question answered
  with a brochure) are exactly what he does want caught. Speed comes out of MY overhead — fewer
  turns, less narration, parallel owners — not out of the checks.

- 2026-08-13 round-26 @7ee7756 [Rule 7 — the streak RESUMES after one clean round, and the channel
  gains a THIRD mechanism]. Round-22 broke this rule's four-round streak by making instruments
  describe themselves. Round 26 resumes it in the same channel — the loop's PROSE about its evidence
  is unbounded by its evidence — and adds a mechanism beyond over- and under-claiming: **an
  instrument that is structurally incapable of the failure it is quoted for.** Three at once, all
  measured by me: four of five pixel "comparisons" compare a file with itself (sha256-identical
  baseline and actual, so «0/1296000 pixels differ = 0.0000%» is arithmetic, not measurement);
  `regression/build.log` is 0 bytes and is cited as `exit_code 0, verdict PASS, measured "strict TS
  build exit 0"`; and the reviewer's MUT5 flips the shipped `wantsInfo` composition from `&&` to `||`
  with all 133 gate assertions still GREEN, because the gate slices the expression out of `agent.ts`
  and hand-types it back instead of executing it. COROLLARY to add: ask of every green number not
  «is it true» but **«what input would make it red»** — if the answer is «none», it is not evidence.

- 2026-08-13 round-26 @7ee7756 [Rule 2 — FIRST EXTENSION FROM SCREENS TO THE LEDGER]. Every prior
  instance of «numbers must be real» was a rendered surface: the fabricated readiness card, six
  authored knowledge scores, decorative 🔥 chips. This round the rule is violated **in the
  database**: `agent.ts:832` writes «ضغط زر: لا» as the recorded REASON for an outcome when the
  customer typed the word and pressed nothing — `buttonIntent("لا") === "decline"`, measured at the
  delivered commit, with no tap provenance anywhere in the call path. A false claim on a screen is
  corrected by a redeploy; a false claim in the ledger is permanent, propagates into every later
  reading, and is exactly the material Rule 4's causal explanations are built from. Rule 2 must be
  read as covering **writes**, not just renders. Watch for a second instance before promoting.

- 2026-08-13 round-26 @7ee7756 [THRASHING — second consecutive ruling; the diagnosis sharpens].
  Round 24 ruled thrashing on «one string answering two opposed questions» and named the exit: split
  `disclosed` from `asked`. That exit LANDED at round 25 (agent.ts:228-230) and the shape reappeared
  within one round, one layer up (`wantsInfo`), then one layer above that (`buttonIntent`). Sharper
  diagnosis: the recurring unit is not a string, it is a **shared table or matcher with multiple
  consumers, widened for one consumer and re-tested only for that consumer.** Five commits in ninety
  minutes, five new defects, one shape. Two generalisable lessons. (a) Fixing one INSTANCE of a
  structural defect buys exactly one round — the fix has to make the property structural (a consumer
  matrix generated from the table) or the class returns at a new address. (b) **Severity went UP on
  the last step while the code footprint went DOWN** — shrinking diffs are not evidence of
  convergence, and a defect that moves from «wrong word on a button» to «false permanent write to
  the lead ledger» is diverging no matter how few lines it took.

- 2026-08-13 round-26 @7ee7756 [accepted pattern — DATA-SHAPED FEATURES, signal 2 of 3]. He asked
  for «a second template». What shipped was a REGISTRY (`src/templates.ts` + `GET /admin/templates`)
  where a third template is a new entry rather than a code change, read by both the wizard preview
  and the launch path so a template cannot preview one way and send another. Same shape that earned
  acceptance at round-22 (one numeral path, one catalogue). **When he asks for «one more X», build
  the place where X lives, not the second X.** NOT yet a Rule — 2 of 3.

- 2026-08-13 round-26 @7ee7756 [process — deploy authorisation is not a definition of «done»].
  «Once done, just deploy it and fly» (2026-08-10) was exercised **five times in ninety minutes**
  this round; four of those deploys carried an unreviewed new defect to production and the fifth
  (v185) is live with a reviewer-named blocker. He pre-authorised the DEPLOY; «once done» is
  load-bearing and this round read it as «once written». Proposed loop amendment for human review
  via `scripts/orbit-memory review`: **a commit that closes a reviewer blocker does not deploy until
  the reviewer has scored the commit that closes it.** Playbook gap, not a builder failure — third
  round in which a fix shipped ahead of its own verification.

- 2026-08-13 R46 [stated]: «dont worry about template pretend it is approved template» — a direct
  SCOPE ruling, issued after market research established that Meta substitutes variables into the
  approved body it already holds, so an operator's wizard edit has no field on the template wire and
  would not travel on a production WABA. His call, in his own words, was to treat the constraint as
  out of scope for this phase. **What this is evidence of** (2 of 3 toward a Rule, NOT yet durable):
  when a raised concern binds only at a FUTURE state — the production-number migration — and does
  not block what is being built today, he rules it out of scope and expects the work to keep moving.
  Prior consistent signal: the standing deploy instruction of 2026-08-10, «once done, just deploy it
  and fly». **How to apply now**: state such a constraint once, plainly, then proceed without
  re-raising it; record it where the future work will find it (STATE.md migration carry-forward +
  the domain skill) rather than leaving it as a live blocker or a UI warning. **What this is NOT
  evidence of**: it says nothing about defects that bind TODAY — those he has consistently wanted
  found and fixed («fix all issues and best UI must be delivered»), and this round he was given two
  such defects (a button rewritten into its opposite, a price question answered with a brochure)
  which were fixed, not deferred. Do not generalise this signal into tolerance for present-tense
  correctness problems.

- 2026-08-13 U44 [stated]: R55 «6/10 — better operationally, still not a strong sales agent». The founder's governing principle, in his words: **every message must move the lead one step forward**. He named the required micro-structure — Deliver → Reinforce value → Qualify — and rejected 'send document + ask qualification question' as transactional. His worked example: after sending the PDF, summarise in one or two lines wh…
- 2026-08-13 round-22 @1936a22 [Rule 6 — the eight-round streak BREAKS, and the fourth corollary is
  what broke it]: round-21's corollary was «when a fabricated VALUE is removed, grep for the value's
  SOURCE, never for the string that displayed it». It was followed exactly — six literals deleted
  from `PRODUCTS`, `kbRegistry` neutralised, seven render surfaces cleared in one edit, and I
  verified all seven live rather than crediting them. The rule still bites once, at much reduced
  severity and in a NEW DIRECTION: the wizard's new «معرفة مدمجة» vocabulary did not travel to #kb,
  so the same six services now read «معرفة مدمجة» on one screen and «لا معرفة بعد» one click away.
  FIFTH COROLLARY, and it is about fixes rather than defects: when a fix introduces a NEW
  DISTINCTION the product did not previously have a word for, that distinction is itself a property
  — enumerate every surface that speaks about the same objects and teach them all the new word in
  the same edit. A vocabulary that exists on only one screen is a contradiction, not a fix.
- 2026-08-13 round-22 @1936a22 [Rule 7 — FIRST CLEAN ROUND in four, and the mechanism is worth
  naming]: every axis I have caught this rule on is clean at this commit. `check-numerals.mjs`
  retracted its universal claim and now publishes its own miss rate («a review wrote 21 mutations
  and 18 passed»). `visual.note`'s «18 comparisons» matches an array of 18 and claims nothing about
  the ratios. The wizard re-baseline declares itself, carries `measured_before_rebaseline`, states
  the reason, and says explicitly that the image is NOT what carried the evidence. The pattern
  across all three: the loop stopped DESCRIBING its instruments and started making the instruments
  describe themselves. A check that reports its own failure rate cannot be quoted upward as proof
  of a property — that is the whole content of Rule 7, solved structurally rather than by discipline.
- 2026-08-13 round-22 @1936a22 [CPO self-correction — my own measurement was wrong, second
  consecutive round I have had to record one]: at round 21 I wrote that a geometric rect-overlap
  test found «0 chip-over-name collisions across all four rows» on #kmon/5 at 375, and concluded
  «the symptom is misalignment, not overprinting». Measuring again with the row markup's real
  selectors, all four rows overlap by 58×32px, and the overprint is plainly visible in a screenshot
  I should have looked at then. The likely cause is a NULL-SET CLEAN — a selector matching nothing,
  so the collision loop had nothing to iterate — which is precisely the unearned-clean failure I
  have charged the builder with for six rounds, committed by the gate. Procedural lesson for me,
  symmetric to the one I keep giving: a geometric test returning zero must first assert that BOTH
  input sets are non-empty, and any negative finding about a VISUAL defect must be confirmed against
  a capture before it is written down.
- 2026-08-13 round-22 @1936a22 [new signal, toward a possible rule — the builder's first downstream
  self-catch]: he shipped a correct fix, saw a 14-20% pixel delta on the screen he had just edited,
  and instead of re-baselining it he went to find out what moved — discovering that removing the
  invented scores had collapsed every wizard card onto a chip claiming uploaded knowledge for six
  services that have none. In eight rounds this is the first real defect found downstream of my gate
  by the builder rather than by me. One occurrence, so a signal and not a rule; but it is the exact
  behaviour Rule 6 has been trying to induce since round 15, and a third occurrence would promote
  «interrogate an unexpected delta before accepting it» from an order into how this loop works.
- 2026-08-13 round-21 @e4facd0 [against Rule 6, EIGHTH consecutive occurrence — rule holds, and the
  last axis this shape has]: round-20's third corollary (derive the audit's scope from the ROUTER,
  never from a human's memory) was honoured, and honoured well — #kb/<product> was added, all four
  of its named defects fixed, and my own router-derived sweep of 17 routes × 3 viewports found the
  numeral property holding PORTAL-WIDE for the first time in eight rounds. The audited set finally
  grew. And the defect moved again — not sideways to an adjacent screen, not to an unrendered state,
  but UP ONE DOM NODE on the screen that was just fixed. `KB_SECTIONS` was correctly deleted;
  `PRODUCTS[].sc = 92/74/71/55/55/63` (src/dashboard.ts:299-306), the constant that fed its «92%»,
  was left, and still renders as «٩٢٪ درجة معرفة المساعد» with coloured progress bars on SEVEN
  surfaces — including the hero ring of the page that was fixed, where «٧٤٪ جاهزية معرفة المساعد»
  now sits beside a chip reading «بانتظار ملف المعرفة» and above a real card reading «٠ من ٤».
  On #kb the grammar is inverted: bars on the six services with no knowledge, none on the two that
  have it. FOURTH COROLLARY, and the one this shape has left: when a fabricated VALUE is removed,
  grep for the value's SOURCE, never for the string that displayed it. Deleting the render site is
  deleting the symptom.
- 2026-08-13 round-21 @e4facd0 [CPO self-correction — recorded against the gate, not the builder]:
  round-20's M1(b) read «do not leave a hardcoded 92 beside a computed ring — either derive it from
  `ready` or delete the heading's number». Backwards. `ready = r.sc` IS the hardcoded 92 (:1061);
  the ring was the fabrication and the heading its duplicate. I named the fabrication as the fix
  SOURCE and aimed the builder at the symptom — which is why the root survived a correct fix. I also
  called KB_SECTIONS «the round's ONLY correctness defect», and SC-Y2 quotes that phrase back.
  Procedural lesson, symmetric to the one I keep giving the builder: before ordering a fabricated
  number fixed, `git grep` the VALUE and enumerate every render site, or the order closes one of them.
- 2026-08-13 round-21 @e4facd0 [round-19's orchestrator lesson, THIRD occurrence — promote to a
  process rule]: «when a CPO order distinguishes an INSTANCE half from a MECHANISM half, the
  mechanism half cannot be silently deferred — it is the one that ends the series.» Round-19: fmtPct
  + delete-every-bare-toLocaleString deferred. Round-20: the guard's honesty fix deferred. Round-21:
  M2's instance (the TypeError) shipped and its mechanism (decide countUp's fate) did not — the
  animation is still dead, proven by 10-frame rAF sampling, and SC-Y1 is marked PASS against the
  expectation «Then the animation works»; M4's nine import counts shipped and the tenth and eleventh
  (`d.skippedCount`, `s.row`) did not; S1 was a pure mechanism order and was not attempted at all.
  Every partial delivery is the same cut. Proposed rule for the ORCHESTRATOR: split a two-halved
  change order into two tracked items at intake, so partial delivery reads as one closed and one open.
- 2026-08-13 round-21 @e4facd0 [new — credit, recorded so the gate stays calibrated]: four things
  verified good. (1) The numeral property holds portal-wide — 17 router-derived routes × 3 viewports,
  every remaining Latin run a phone number, a filename or a phone-format rule, with four exceptions
  in one paragraph. Eight rounds of instances finally became a property. (2) The replacement
  readiness card is BETTER than the order I wrote: I said «delete it»; it was replaced with four real
  signals, and I broke it deliberately on five services with no KB doc, no asset and no campaigns —
  every one stated absence with its operational consequence («المساعد يبيع من المعرفة المدمجة فقط»).
  It also surfaced a defect the fabricated card was hiding: campaigns carry free-text product names
  that never join to SERVICE_CATALOGUE (round-14's finding, still open). (3) Zero re-baselines for a
  second round; all 18 ratios reproduce under my own Pillow recomputation; the three by-construction
  zeros disclose themselves unprompted. (4) The SC-Y3 exclusion was DECLARED rather than silently
  skipped — Rule 7's discipline applied to the loop's own work within one round of being told. Its
  premises are wrong (the strings are a second hand-typed copy in dashboard.ts, not agent.ts, and
  nothing is verbatim — the agent already sends both «٧٠٪» and «70%» to real people) but the
  instinct is right, and the instinct is the harder half to teach.

- 2026-08-13 round-20 @aed03a3 [new — extends `.orbit/decisions/0001-dashboard-no-range-edits.md`]:
  decision 0001 was written after a range edit deleted five helpers and shipped a blank page that
  `tsc` and `node --check` both cleared. This round an ANCHORED replacement produced
  `Math.roundfmtN(` at src/dashboard.ts:1722 — syntactically valid, type-invalid, live in
  production — and it was cleared by `tsc --noEmit`, `node --check`, the new source guard, smoke's
  `pageerror` listener AND 57 QA scenarios. The rule needs its second half: anchored replacement is
  NECESSARY BUT NOT SUFFICIENT, because src/dashboard.ts:247-1802 is a client `<script>` inside a
  template literal that no static tool in this repo can parse. Any edit landing between those lines
  requires a runtime assertion — execute the edited surface in a browser, in the state that renders
  it — before it can be called done. Amend decision 0001 rather than filing a new one.
- 2026-08-13 round-20 @aed03a3 [CPO self-correction — recorded against the gate, not the builder]:
  countUp() has been dead since 825a557, the commit reviewed in round-19. The numeral sweep made
  every KPI value Arabic-Indic; countUp's `parseInt(m[0].replace(/[^\d]/g,""))` strips them to NaN
  and returns. Round-19 passed M2 on that commit through four DOM channels and never checked
  whether a FEATURE consuming those values still worked. Symmetric lesson for the CPO's own
  procedure: when a change alters the DATA a feature reads, re-run the FEATURE, not just the
  render. A pixel-identical screen can hide a dead behaviour.
- 2026-08-13 round-20 @aed03a3 [new — credit, recorded so the gate stays calibrated and is not
  purely a complaint log]: three things were done well and verified. (1) Every specific `must` from
  round-19 was executed AND holds under its own trigger condition — I checked each by client-side
  state injection, and none was a paper fix. (2) The bare-`toLocaleString` class is genuinely dead:
  1 remaining call, inside `fmtN` itself, against 76 `fmtN` call sites. Mechanisms DO work when
  scoped to a shape. (3) The visual bundle carries zero re-baselines for the first time — all 15
  baselines predate their actuals, verified pairwise. Evidence discipline is improving; the failure
  is in the PROSE around the evidence, which is what Rule 7 now governs.
- 2026-08-13 round-19 @825a557 [against Rule 6, SIXTH consecutive occurrence — rule holds, next
  dimension]: the leak-vs-spill pattern has moved from adjacent SCREENS to adjacent STATES of the
  same screen. Rounds 17-18 fixed #kmon and left #kmon/<id>, fixed #kmon/<id> and left #home.
  Round 19 fixed #home's rendered state — verified clean by me at 1440/768/375 through four DOM
  channels, with every remaining Latin token a phone number or a filename version — and left
  #home's CONDITIONAL state: `src/dashboard.ts:1460` renders «26 ساعة بلا متابعة» in raw Latin
  once a hot contact passes 24h idle, which for the live data happens at 2026-08-13T11:48Z, inside
  the demo window. Generalisation to carry: enumerating surfaces in the user's traversal order
  (round-18's lesson) is necessary and not sufficient — a defect class defined by a CONDITION must
  be enumerated from the SOURCE, because a live-DOM count can only measure the branch that happens
  to be rendered. An acceptance check is not a completeness check.
- 2026-08-13 round-19 @825a557 [new — an ordered mechanism that is skipped returns as the same bug,
  one round later, with a timestamp]: round-18's S6 asked for `fmtPct` plus deletion of every bare
  `.toLocaleString("ar-SA")` and every raw concatenation, on the stated ground that «a convention
  that has leaked three times is not a convention». It was not attempted — `fmtPct` still does not
  exist, 19 bare `toLocaleString` calls remain beside 53 `fmtN` calls, the raw-concat path is
  untouched — and the very next round produced M4 out of that untouched path. Second consecutive
  round where the CPO diagnosed the mechanism gap and the loop shipped instances instead. Process
  lesson for the ORCHESTRATOR, not the builder: when a CPO order distinguishes an INSTANCE order
  from a MECHANISM order, the mechanism order cannot be silently deferred — it is the one that ends
  the series.
- 2026-08-13 round-19 @825a557 [closes the round-17 evidence-integrity caution — do NOT promote to
  a rule]: round-17 said a second occurrence would promote it. There has been none in two rounds,
  and this is the strongest bundle the loop has produced: I recomputed ALL 15 pixel ratios myself
  and every one reproduces to six decimals; re-baselines are labelled as re-baselines with
  `measured_before_rebaseline`; round-18's byte-identical-baseline residual is resolved; the stale
  `visual.note` is rewritten and accurate. Closed as corrected. What survives is smaller and lives
  in the loop's PROSE rather than its numbers — «portal-wide» and «0 Latin digits on 6 screens» are
  still stated wider than measured — which keeps the round-18 signal «the loop's own claims are
  subject to Rule 2» alive at two occurrences, one short of a rule.
- 2026-08-13 round-19 @825a557 [new — the loop's self-measurement is trustworthy on this axis;
  recorded because a gate that only ever reports distrust is not calibrated]: I refused the
  builder's digit script and its exclusion list (phones, 9+ digit runs, semver) and counted from
  scratch with nothing filtered, then added three channels that method never touched — CSS
  pseudo-element `content`, SVG `<text>`, and title/aria/alt/placeholder attributes. My independent
  count reproduced the builder's conclusion exactly, and the exclusions proved substantively
  correct rather than self-serving: every excluded token is an identifier a Saudi reader wants in
  Latin. Carry forward — challenge the loop's exclusion lists by re-deriving them, and say so
  plainly when they survive.
- 2026-08-13 round-18 @d44236f [against Rule 6, FIFTH consecutive occurrence — rule holds, with a
  sharper diagnosis]: the leak-vs-spill pattern is no longer just "fix the edited screen, miss the
  adjacent one". This round the spill moved BACKWARD along the path: round-17 fixed #kmon and left
  #kmon/<id>; round-18 fixed #kmon/<id> (33/27 → 64/2 Arabic-Indic/Latin) and left #home — the
  screen he opens FIRST — at 107/51, showing «١٥» and «٤» beside «1 +10 تجريبية» in one KPI band
  and «100%» in 30px type while the next screen says «٪١٠٠». Generalisation to carry: enumerate the
  surfaces in the order the USER traverses them, not the order the defect was reported. The
  reported screen is where the complaint landed, not where the demo starts.
- 2026-08-13 round-18 @d44236f [new — a property fix must ship with its enforcement, or it returns]:
  the numeral defect has now consumed three consecutive rounds because `src/dashboard.ts` has three
  coexisting ways to render a number (fmtN, bare `.toLocaleString("ar-SA")`, raw concatenation) plus
  two ways to render a percent. Nothing makes the wrong one hard to write. This round even CREATED a
  new mixed token («٣ -25%» in stageBars — Arabic-Indic value, Latin drop, one label) while closing
  others, which is the proof the convention cannot hold itself. Process lesson: when a CPO order is
  phrased as a property ("one numeral system", "no fake controls", "header matches row"), the change
  order must require the mechanism that makes violations impossible, not just the instances.
- 2026-08-13 round-18 @d44236f [confirmed — the honest-limit pattern is the right answer, keep it]:
  round-17's M3 asked the loop to stop labelling a self-comparison as a frozen-baseline comparison.
  The response was not a better-looking number — it was «HONEST LIMIT: this baseline was
  re-established AFTER the redesign, so it cannot prove the redesign itself; it proves only that
  nothing drifted since», plus how the redesign WAS verified. I re-computed nine of the fifteen pixel
  ratios independently and every one reproduced. That is the product's own «لا تقديرات» discipline
  applied to the loop's evidence about itself. Round-17's evidence-integrity caution does NOT escalate
  to a rule — the second occurrence did not happen; it was corrected.
- 2026-08-13 round-18 @d44236f [new — the loop's own claims are subject to Rule 2]: the commit message
  asserts «one numeral system across the demo path». Measured, that is true of two screens out of five
  and false of one label the same commit created. Rule 2 was written from his words about the PRODUCT,
  but he reads commit messages and STATE.md too. A commit line broader than its measurement is the same
  failure mode as an unsourced number on a dashboard. Two more occurrences and this becomes its own rule
  about the loop's self-reporting.
- 2026-08-13 round-17 @0be3226 [against Rule 6, FOURTH consecutive occurrence — rule reinforced]:
  the round's own commit line is «One numeral system per screen on the campaigns list». It is
  true — and true of exactly the one screen that was edited. Measured across the live app:
  #kmon 19 Arabic-Indic / 0 Western, but #kmon/<id> 33/27, #home 90/62, #aimkt 6/30, #kb 0/16.
  #kmon/<id> is ONE CLICK from the fixed screen and is where a demo goes next; it shows
  «جهات الاستهداف 4 من 4» inches from «الكل (٤)» in the same visual band. Rule 6's exact shape a
  fourth time. Generalisation to carry forward: when a fix is expressed as a page-level PROPERTY
  («one numeral system per screen», «no fake controls», «honest empty states»), the property must
  be asserted across every screen that shares it, not only the screen under edit — and asserted
  by measurement, not by claim.
- 2026-08-13 round-17 @0be3226 [new — responsive parity is an unwatched blind spot]: the campaigns
  grid has desynced its header from its rows below 900px since at least a71cd51 — `.trow > div:
  nth-child(4|5)` is hidden by the media rule while the header div carries no `.thead` class, so
  at 768 «الجمهور» sits over «٪٠», «مشاهدة» over the progress bar, «ردود» over the action button,
  and the real audience «٤» is not rendered at all. It survived several UI rounds and a QA matrix
  that captures all three viewports every time, because the checks assert PAGE-level properties
  (landmark present, no page-level overflow, 0 console errors) and this defect lives inside an
  `overflow-x:auto` card where a page-level overflow check is structurally blind to it. Process
  lesson for the QA playbook: responsive evidence must assert intra-component alignment
  (header offset == cell offset) per breakpoint, not merely that the page rendered.
- 2026-08-13 round-17 @0be3226 [confirmed — keep this behaviour]: the sparse explainer is the right
  answer to design's «EMPTY/BROKEN, not honest». It does not hide the short list, apologise for it,
  or pad it with demo rows; it states what is shown, why the rest is elsewhere, and makes the
  elsewhere clickable. That is Rule 2's honesty applied to LAYOUT rather than to numbers — the first
  time a thin state has been made to read as deliberate without inventing data. Reuse this pattern
  for every thin state in the product.
- 2026-08-13 round-17 @0be3226 [caution — evidence integrity, watch for recurrence]: for the first
  time the delivery-evidence file asserted a measurement it did not make. The three kmonlist pixel
  comparisons carry `measured_before_rebaseline == mismatch_ratio` and «real comparison against the
  frozen baseline», but the baselines were rewritten 2026-08-13 02:50 from the SAME build as the
  03:01 actuals — they differ only by the wall clock, so the 0.0008/0.0006/0.0038 ratios prove
  nothing about the redesign. The gate passed because it checks structure, not provenance. Since
  this user's Rule 2 is precisely «numbers must be real, sourced and honestly bounded», the loop's
  own evidence must meet the user's own bar: record re-baselines as re-baselines. A second
  occurrence promotes this to a rule.
- 2026-08-12 U35 [stated]: R48 «fix all issues and best UI must be delivered», sent hours before his team demo and immediately after specialists surfaced open UI defects. Not a new preference — the THIRD escalation of one standing bar already in user-model.md Rule 1 (professional marketing-tool fit): R32 «the design is horrible… show me something professional already for production», R33 «make this worth it», now R48. What …
- 2026-08-12 round-15 @8ff3f75 [against new Rule 6, THIRD consecutive occurrence — promoted]:
  the Proxy fix he demanded («this is not ok») is correct engineering and forward-only. The
  code-level matcher runs before the model, my own 18-case matrix found 0 hard failures on the
  claimed behaviours, opt-out cannot be swallowed, and the Arabic opener holds the
  VOICE-REFERENCE register. And every one of the four real conversations he will demo TODAY
  still opens «Proxy Massar» → «هل تقصدون خدمة أو منتجًا باسم «Proxy Massar»؟» in the live
  «سجل التفاعل», Ibrahim's still escalates a human handoff for that non-existent service, and
  966543464327's still carries the literal «**بروكسي مسار**» with WhatsApp-visible asterisks.
  The leak is closed; the spill is on screen. A render-time suppressor using the matcher that
  already exists closes it without deleting any data.
- 2026-08-12 round-15 @8ff3f75 [confirmed — keep this behaviour]: when two numbers legitimately
  measure different populations, the builder chose to give them different WORDS and disclose the
  definition («ابدأ التواصل مع ٢ جهة تستحق المتابعة» + «وسوم اهتمام مؤكدة، أو نية مرتفعة قرأها
  المساعد… ولم تُسجَّل وسمًا بعد») instead of forcing them equal. That is the mature call: merging
  them would have destroyed a real signal (a high-intent reading with no tag yet is exactly who
  you call next). Supports Rule 4 — the surface justifies its own reading where the number is.
- 2026-08-12 round-15 @8ff3f75 [gate discipline, FIRST genuine close after four rounds]: the
  pixel gate finally compared something. I re-hashed all twelve pairs: four are genuinely
  different files at the claimed ratios (baselines mtime 11:54:57Z frozen at 9b7cd54, actuals
  12:45–12:46Z after f6ab762), and the eight zeros each carry an honest `baseline_note` naming
  why. The one that looks laundered (wizard@375, byte-identical, note claims "real comparison")
  is TRUE — its baseline predates its actual by 51 minutes, so it cannot be a copy; the page
  simply did not change. Honest evidence is achievable here, and it took being told three times.
- 2026-08-12 round-15 @8ff3f75 [technique, confirms the code-not-prompt rule a FOURTH time]:
  the markdown defect he saw («**بروكسي مسار**» rendered literally on WhatsApp) was fixed with a
  prompt line, while the Proxy defect beside it was fixed in code. CLAUDE.md §4 says hard rules
  live in code and never only in prompts; a two-line strip of `**` on the way out of `safeSend`
  is the same class of mechanical rule as the activation matcher. The builder applied its own
  lesson to one of the two defects in the same commit.

- 2026-08-12 U34 [stated]: R47 user-stated, SAFETY-CRITICAL and unambiguous: «Don't ever send a text to the client for any test or anything. Don't shoot any WhatsApp message at all. Okay? Stop shooting messages, and I will tell you what number you need to test with.» This HARDENS CLAUDE.md §8 beyond its current wording: §8 today gates 'any WhatsApp message to a real customer' but explicitly permits 'sandbox self-tests to th…
- 2026-08-12 round-14 @9b7cd54 [against Rule 2, SECOND consecutive occurrence — the round-13
  signal recurs, so its lesson is now a rule candidate at 2 of 3]: deleting the fabricated ROW is
  only half a data-integrity fix. The write path is genuinely gone (verified: three GETs on
  966535106365 mutate nothing, zero tag events) and the ledger is clean — yet the same claim
  survives on three surfaces the founder actually looks at: the campaign row still shows
  «باقات NVR لتغطية 8 مواقع · نية مرتفعة» in the identical `chip c-ok` green as ياسمين's real
  tool-written tag (only a hover `title` separates them); «لماذا نكسب» still credits
  «باقات NVR لتغطية 8 مواقع: 1 مكتسبة»; the row's next action still tells him to review an NVR
  quote. THE RULE THIS TEACHES: when a fabricated value is removed, enumerate every DERIVED
  SURFACE (counters, aggregates, next-actions, timelines) before calling it cleaned — and an
  inference must be VISUALLY distinguishable from a fact, because a `title` attribute is
  invisible at a glance, on touch, and in every screenshot he is sent.
- 2026-08-12 round-14 @9b7cd54 [technique, THIRD consistent occurrence — promote toward a rule]:
  a whitelist stated in a prompt is not a whitelist. insights.ts already instructs the analyst
  «اسم الخدمة كما هو في كتالوج لِين حصرًا» from a six-name SERVICE_CATALOGUE with an
  OTHER_SERVICE fallback — and the live cache holds 17 distinct free-text product names across 14
  rows, four of them separate spellings of «الإجازات المرضية» alone, each becoming its own row on
  the by-product board. Same shape as the closing-ladder counter (round-12) and the exact-string
  idempotency guard (round-13): anything the model must apply MECHANICALLY — count, match,
  constrain — is enforced in code after the response returns, never requested in prose.
  CLAUDE.md §4's «hard rules live in code» now has three independent confirmations.
- 2026-08-12 round-14 [record correction, on my own predecessor]: round-13 justified the NVR
  finding with «NVR is closed-circuit video recording. Lean does not sell it.» That is WRONG —
  .orbit/artifacts/copy/VOICE-REFERENCE.md:20-22 lists «السجل الوطني للتطعيمات (NVR)» as one of
  the founder's own approved template values, and campaigns 8–11 launched on it. The verdict was
  right for a stronger reason: «باقات NVR لتغطية 8 مواقع» is a free-text phrase outside the
  six-name catalogue, promoted to a confirmed HOT interest and a WON deal, for exactly what the
  agent had refused in-transcript («باقات NVR غير متاحة لدي ضمن المعلومات المعتمدة»). Process
  rule re-earned (first learned at round-6): verify an order's PREMISE against the artifact,
  never against a previous envelope. A correct verdict on a false premise is one round from
  becoming a wrong one.
- 2026-08-12 round-14 @9b7cd54 [against Rule 2, third store]: cleaning `contact.tags` does not
  clean the claim. `product_interest` lives in contact_insights, a separate store no tag path can
  reach, and winLossBoard groups by_product straight off it — so the founder's DEFAULT real-only
  #home still credits «باقات NVR لتغطية 8 مواقع: 1 مكتسبة». Corollary to the derived-surface rule
  above: enumerate the STORES as well as the surfaces.
- 2026-08-12 round-14 @9b7cd54 [against Rule 2, new mechanism]: the REMEDY introduced its own
  falsification. `tracker.replaceTags` stamps `ts: Date.now()`, so curating four real contacts at
  11:48:44Z rewrote every genuine tag's timestamp; «سجل التفاعل» — captioned «كل نقاط التماس …
  الأحدث أولًا» — now shows ياسمين an interest touchpoint at ٠٢:٤٨ م, five hours after her
  conversation ended, as her most recent event. Round-13's M1(d) named this exact artifact; the
  fix reproduced it with a genuine product instead of a fabricated one, and destroyed the true
  times (DELETE + re-INSERT) in the process. Correction paths must PRESERVE the original event
  time, never re-stamp it.
- 2026-08-12 round-14 @9b7cd54 [confirmed, keep this behaviour]: when told an approach is wrong at
  the root, the builder reverted its own feature rather than patching around it (56aa2d2 removes
  the writer and says so in the message), reached for the native API instead of a fourth attempt
  at hand-rolled RTL arithmetic (`scrollIntoView({inline:"center"})` — I measured 145..229 inside
  57..318 at 375×812), and wrote a guard that provably catches the class it was built for (I
  falsified `scripts/smoke.py` by blanking `#body` and throwing `nonExistentHelper is not
  defined`; it caught 0 chars + missing landmark + 1 runtime error and exited 1). Three rounds of
  "the fix must be the native/code-level mechanism, not more arithmetic or more prose" now hold.
- 2026-08-12 round-14 [gate discipline, FOURTH consecutive round — this is a playbook gap, not a
  builder failure]: the delivery gate returned PASS on a bundle whose six visual `actual` captures
  were taken 11:08–11:26Z, hours BEFORE the 11:49Z commit they certify, and whose 375 salespath
  capture visibly shows the BROKEN stepper it is cited to prove fixed; whose baselines are
  byte-identical SHA-256 copies of those actuals (mismatch 0.0 still true by construction, third
  round unlanded); and whose three brand-new scenarios certifying this round's musts cite
  screenshots that cannot contain their claims (a stepper PNG for a ledger audit, a wizard PNG for
  a Python run). `coverage_complete: true` while the round's only destructive endpoint has no
  scenario. The deterministic gate checks SHAPE; only reading the artifact checks TRUTH.

- 2026-08-12 round-13 @11e29f4 [against Rule 2, sharpest violation on record — PROMOTE to a
  numbered rule if it recurs once more]: the system wrote «باقات NVR لتغطية 8 مواقع · نية مرتفعة»
  into the ledger of a REAL prospect (966535106365) for a product Lean does not sell, and the
  campaign board reported it back as «١٠٠٪ جهات مهتمة» with «ابدأ التواصل مع ٢ فرصة مؤهلة».
  Rule 2's own wording — "AI readings are labeled as the assistant's understanding (فهم المساعد)"
  — is the specification that was inverted: the label existed (`title="من قراءة المساعد"`) and the
  promotion erased it. THE RULE THIS TEACHES: an AI reading may INFORM a view but must never
  become a WRITE indistinguishable from a human or tool fact. If persisted at all it carries a
  `source`, a weaker level, its own visual treatment, and never feeds a counter he reads as fact.
- 2026-08-12 round-13 @11e29f4 [vocabulary, his own words in R43]: "not listed up to date" is a
  DATA-FRESHNESS complaint, not a display complaint — the board lags behind what the system
  already knows. The correct response is to make the read reach the VIEW faster, not to make the
  inference DURABLE. The fix chosen this round satisfied his sentence and broke his intent.
- 2026-08-12 round-13 @11e29f4 [technique, promote to the domain skill]: exact string equality
  against a free-form LLM field is not an idempotency guard. It failed within 45 seconds in
  production (966502444737, turns 8→10, same interest re-worded → two hot tags) and again an hour
  later (966543464327, a third tag concatenating two it already held). The right pattern is
  already in this codebase: insights.ts's SALES_STAGES whitelist. Anything the model names that
  will be COMPARED or GROUPED must be constrained to a known set first.
- 2026-08-12 round-13 [gate discipline, third consecutive round]: a visual gate whose baseline is
  its own actual cannot fail — and that is not paperwork, it is the mechanical reason a
  functionally-blank page reached production this round with tsc, `node --check` and the delivery
  gate all green. Round-12 ordered the frozen baseline (S5d); it did not land; the failure it
  predicted happened inside the same round. A render assertion (innerText length + required
  selector + zero console errors, per route) is the cheapest guard for this class; static checks
  structurally cannot catch it.
- 2026-08-12 round-13 @11e29f4 [confirmed, R44 — keep this behaviour]: when he edits source himself
  and hands it back, his version is applied verbatim and the identity propagates everywhere it
  belongs. Verified: the diff is exactly two lines, all 11 playbook sections intact, no rule
  reworded, the name carried to insights.ts and kb.ts, zero stragglers repo-wide, and the live
  agent introduced itself with the new name 11 seconds after the deploy booted.
- 2026-08-12 round-12 @d6ef29a [technique, promote to the domain skill — CONFIRMED BY THREE
  ATTEMPTS]: a rule the model must COUNT belongs in code, not in prose. The closing-ladder cadence
  failed twice as prompt text (buried in «# الإغلاق» at 432e40d — never fired; promoted to a
  top-level «# عدّاد التقدم» at 6b513ce — fired once) and became reliable only at d6ef29a, where
  systemPrompt computes `customer messages ≥ 3 && no interest tag` and injects a mandatory
  per-turn instruction. This is CLAUDE.md §4's "hard rules live in code" applied to sales craft:
  the model may write the sentence, but it must never be the one keeping the count.
- 2026-08-12 round-12 @d6ef29a [against Rule 2, unresolved — second round]: 6 of the 8 non-test
  contacts in his ledger are QA-authored fiction (850/861/872/883/894/905), all `test:false`, so
  fabricated facilities sit in the customers list, the KPIs and the win/loss board — on the very
  screen this round built to tell him where a deal stands. The platform's own separation is
  correct and 9 other rows use it. His stated standard ("separate campaign data from users talk
  in sandbox", R23) is being broken by the process that proves the product, not by the product.
- 2026-08-12 round-12 [gate discipline, tightened]: an evidence claim must be checkable against
  the artifact it cites, or it is not evidence. Two claims failed that test this round while the
  gate still returned PASS — SC-S13 «all three «منتج» are the role title» (1 of 3; two are the
  «المنتجات» nav module) and SC-S9 «verified at 1440 and 375» (the 375 capture does not contain
  the stepper it certifies, in three consecutive rounds). Read the artifact, then the claim.

- 2026-08-12 round-12 [taste signal, his standard exceeded — reference artifact]: the system
  produced better copy than the order specified. The reference campaign close is now
  «ما أكثر خطوة تستغرق وقت فريقكم اليوم: التسجيل، إدخال الجرعات، أم إصدار الشهادات؟» — open
  question · about their process · three named options · one-word reply · qualifies the lead by
  whichever they pick. Use it as the shape for future campaign copy, not a yes/no or a binary.
- 2026-08-12 round-12 [process learning, gate]: the round-11 verify-claims-against-artifacts rule
  paid for itself in one round. "All eight musts are landed" held for seven and was 1-of-4 on the
  eighth; re-running the composer myself (4×) and re-measuring the rail in PIL — rather than
  accepting a 4/4 audit and an in-browser geometry read — is the only reason the gate meant
  anything. Cost: minutes.
- 2026-08-12 round-12 [technique, promote to the domain skill]: when a rule must survive a model
  swap, STATE it — never rely on a neighbouring rule producing it as a side effect. The composer's
  4/4 correct openers currently fall out of the close-ban rather than an opener rule, and the one
  surviving prompt contradiction (a facility name handed to the model as «اسمه الأول») is exactly
  where an unstated assumption breaks first.

- 2026-08-12 R41b [stated]: "make openai handle content" → he wants the model to own creative
  PRODUCTION, not just conversation — and by implication expects it to be as good a seller in a
  campaign blast as it is in a chat. The acceptance bar for AI-authored copy is the SAME playbook
  the agent uses, not a lighter one. (Round-11 rejected the composer for opening/closing on
  yes/no questions the agent prompt bans by name.)
- 2026-08-12 R41a [stated]: "lets have action points with the client in the client page, for
  example first check issues with client then propose the product then …" → he describes features
  as an OPERATOR'S SEQUENCE OF ACTIONS, not as a data model. "action" is load-bearing: a stage
  indicator answers a different question than the one he asked. When he names a sequence, each
  step must carry what to DO at it, not just where you are.
- 2026-08-12 R40 [stated, method directive]: "prompts must SHOW worked examples, not list rules"
  (checkpoint, request 30) → Rule 3 (briefs by concrete reference artifact) extends from screens
  to PROMPTS: his reference artifact for an LLM is an example message, not a policy line. Applies
  to every prompt in the system, not just the agent's.
- 2026-08-12 R40 [stated, second language rejection]: "the language is not sales person, enhance
  the language" — aimed at the AGENT's voice, not the portal. Read against R35 ("the language is
  weak" + his own template) this refines the vocabulary: "language" to him means the SELLING
  register, not correctness. R35 taught the words; R40 taught the craft. → Corporate-correct
  Arabic that does not sell is a defect to him. Second consistent language-rejection signal; a
  third makes it a rule.
- 2026-08-12 round-11 [process learning, gate]: **a prompt rewrite is a DELETION event, not only
  an addition.** Four §8-adjacent guarantees (enterprise plural address, AI self-disclosure,
  complaint escalation, mark_not_interested) vanished in the R40 rewrite with no review of what
  was removed, and two of them failed live in the same round's own proof transcript. Standing
  rule: on any prompt rewrite, diff old→new and enumerate every DELETED rule with its owning
  guarantee before reading a single new line.
- 2026-08-12 round-11 [process learning, gate]: **verify a commit's CLAIMS against its own diff**
  — the mirror image of the round-6 rule. cccd609's message asserted «عرض مُرسَل» and «افتح ←
  names its destination»; `git show cccd609` proves neither was made. Trusting the message would
  have passed two round-10 musts as closed.
- 2026-08-12 round-11 [accepted pattern, for builders]: the strongest thing the round shipped is
  a sentence, not a feature — «بما أن لديكم خمسة فروع وإصدار يومي، فإن أكثر ما سيوفره عليكم هو…».
  When a prompt needs to change behaviour, write the sentence you want the model to say.

- 2026-08-11 R34 [stated, autonomy grant + brief]: "do whatever you want, don't stop, don't
  talk — build" + the bar: team must SEE value/design/experience, AI that explains "why we
  could sell / why we couldn't sell — maybe user issue, product issue, communication issues,
  the file is not clear", "surprise me: intelligence, animation, insights, dashboard, agent
  flow, how everything interconnects", "be smarter than all the tools we have right now".
  → (a) Trust mode exists: he grants full autonomy against a hard demo deadline and expects
  the system to spend it, not ask; (b) the AI-value bar is CAUSAL EXPLANATION — per-customer
  attribution with evidence, not decoration. Third value-audit signal (with R27's
  "fires don't make sense" and the R28-30 real-numbers cluster) — one more recurrence
  promotes a rule: "AI features must explain causally with verbatim evidence."
- 2026-08-11 R33 [stated]: "spin up agents… everything they come up with, implement it" →
  he orchestrates by naming specialist expertise and accepts only consolidated
  IMPLEMENTATION, never reports-as-deliverables.
- 2026-08-11 R32 [rejected → re-briefed with artifacts]: "design is horrible, not
  implementing anything correctly", followed by 5 reference screenshots (CXP prediction
  panel ×2, Tableau dashboard, Emaily campaigns list) + his own phone capture of the
  two-bubble PDF. → Rule 3 holds under rejection: his correction arrives as reference
  artifacts, and device-level WhatsApp QA recurs (consistent with R21). A rejection is a
  re-brief, not a retreat.
- 2026-08-11 R29-R30 [stated, reference screenshots]: Tableau analytics grammar (rate KPIs, true
  funnel shape, distribution columns, location treemap) and Emaily campaigns-list pattern (status
  tabs, search/sort, rate columns, progress bars) supplied as the spec — ratified into Rule 3;
  the delivered honest-data captions were consistent with Rule 2.
- 2026-08-11 R27 [stated, screenshots of a CXP product]: "this is the type of things I want in our
  product… current implementation is not PMF yet. Revise functions, solutions, UI/UX — huge
  drag-drop box, fires don't make sense. Worry about how we really get value." → He audits VALUE,
  not feature presence: an AI-flavored surface with decorative signals (🔥 chips) and oversized
  input chrome reads as fake to him. Intelligence features must earn their place with real,
  evidence-backed readings (became Rule 2's third signal; UI de-decoration executed — emoji chips
  removed from the portal, compact toolbar replaced the dropzone).

- 2026-08-11 R23 [stated]: "separate campaign data from users talk in sandbox" → he audits the
  numbers for honesty: mixed test/real data in KPIs is a DEFECT to him, not noise. Default views
  must show real-only truth with test traffic excluded but reachable (toggle), never silently
  blended. Consistent with the honest-zeros posture he accepted on the home KPIs.
- 2026-08-11 R21 [stated, screenshot brief]: sent a screenshot of the campaign message on HIS OWN
  phone — "the file should be embedded in the message. and show buttons." → He QA-checks WhatsApp
  output on his real device and briefs by concrete artifact (screenshot/prior-art), and he expects
  the channel's full richness in ONE bubble (media + text + buttons), not a message train.
  (Second briefs-by-artifact signal after R17's prior-art reference.)
- 2026-08-11 R20 [stated]: "if a potential client is serious what is the next action? agent should
  send a message to product manager" → the R16 no-dead-end law extends to the OWNER side of the
  funnel: a serious lead with no push to the human who can close it is a dead end. (Signal #2
  toward the R16 rule candidate; enforced in code as notifyLead.)

- 2026-08-11 round-6 [record correction, artifact evidence]: the lean-proposal-deck skill/zip is
  v2.1.3 — the VERSION file inside the hosted zip (`lean-proposal-deck-v2.1.3-upload.zip`, built
  Aug 10 23:23) reads `2.1.3`; the earlier "v1.1 installed" note below is stale. It produced
  round-5's false rename order (rejected with evidence in `.orbit/cpo/round-6.json`). Process
  rule for this gate: verify an order's premise against the artifact, never against memory.
- 2026-08-11 R17 [stated]: "see how marketing platforms build campaign trackers; clicking a user
  opening all chat is horrible" → the user briefs by prior-art reference (best-in-class marketing
  tools are the acceptance bar for this screen) and rejects inline disclosure of heavy content:
  full transcripts belong behind an explicit dedicated surface (side panel), never inline
  expansion. Second consecutive campaign-screen signal judging by professional-tool fit (with
  R15) — one more makes it a Rule.
- 2026-08-11 R17 [applied, from R16 law]: the takeover toggle is the user's only sanctioned mute
  path; any redesign that moves it must prove the button still works by clicking it in QA —
  visual presence of the control is not evidence.
- 2026-08-11 R16-era [stated]: the user's deck factory is his own lean-proposal-deck skill
  (v1.1 installed; formal Arabic RTL proposals — Cover + 6 sections + Thank-you; صحة أعمال Plus
  is its worked example). → Decks entering the hub will increasingly be skill outputs;
  canonical-structure compatibility is a durable requirement, and skill upgrades are
  compatibility watch-points (re-verify the kb.ts mapping against reference/section-map.md
  on each skill version bump).
- 2026-08-11 R16 [stated]: feature directive — every product carries an intro PDF uploaded on its
  product page; the agent sends it with the product opener and on any details/brochure request;
  campaign launches auto-attach it. → The user specifies product content by what the ASSISTANT
  does with it (sends/reads/attaches), not as static storage: products are agent-operated sales
  kits. Second consecutive request placing per-product capability inside the product page
  (consistent with the R15-era correction that uploads live only inside product pages, b66bce0).
- 2026-08-11 R16 [stated]: reported as a defect that a handed-off customer was left in dead air
  (3 real messages unanswered after outcome=handoff). → A requested handoff must never mute the
  agent; silence is legitimate only via explicit, reversible human takeover. "لا طريق مسدود"
  (never a dead end) is a code-level law for this user — conversation guarantees must be enforced
  in code, not merely requested in prompts. (Rule candidate at 3 consistent signals; this is #1.)
- 2026-08-11 R15 [stated]: "redesign this page to fit the use case" — متابعة الحملات must be
  campaigns-as-launches: a list of named, persisted launches → per-campaign detail with a scoped
  funnel and a filterable contact tracker (seen/replied/interested/failed). → The user judges
  screens by fit to his founding workflow (launch → track → qualify), and rejects
  global/aggregate views where per-campaign accountability belongs.
- 2026-08-11 R15 [stated]: wants to see, per targeted person, WHICH product they are interested
  in and HOW serious they are (e.g. الإجازات المرضية · جاد 🔥) inside the tracker. → Lead
  qualification/seriousness is a first-class tracker field for this user, not reporting polish.

## Vocabulary

- "the language" → depending on the surface: on the PORTAL it means the written register of his
  own approved template (R35 — enterprise plural, verb-led, one word per concept); on the AGENT
  it means SELLING CRAFT (R40 — pain-led openers, discovery before pitching, objections reframed
  with numbers, choice-closes over yes/no). Correct-but-not-selling Arabic fails the second sense.
- "action points" → per-stage instructions for the operator ("what do I do now"), not a stage
  indicator ("where am I") — R41a.
- "handle content" → the model AUTHORS the customer-facing copy, held to the same sales playbook
  as the conversational agent — R41b.

- "surprise me" → bring capabilities he did NOT specify that demonstrably outclass the
  tools he uses today — aimed via this file, never random decoration (R34).
- "why we sold / why we couldn't sell" → per-customer causal attribution grounded in the
  conversation's verbatim text, with the cause named from his own list (user issue /
  product issue / communication issue / file not clear) — implemented as LOSS_TAXONOMY.
- "not PMF yet" → functionally present but not yet something a customer would pay for — he wants
  functions, solutions, and UI/UX revised TOGETHER around real value, not a visual polish pass.
- "follow this" (+ screenshot) → adopt the referenced product's structure/information grammar,
  re-expressed in Massar's own design language (see Rule 3) — never copy its palette or branding.
- "شريحة استهداف" → a launch filter derived from HIS OWN file's columns (city/size/sector/…),
  not a preconfigured taxonomy — any column he ships becomes a segment.
- "تجريبي" → sandbox/test traffic (his own numbers, simulated leads) — must stay out of real
  KPIs and lists by default.
- "إعادة الاستهداف" → launching a new campaign onto a tracked cohort from a previous campaign
  (the filtered view he is looking at, e.g. الذين شاهدوا ولم يردّوا).
- "متابعة الحملات" → the campaign-monitor screen (list of launches + per-campaign boards).
- "حملة" → a concrete launch: one named send to a targeted list, persisted with
  name/product/targets — not an aggregate marketing construct.
- "جاد" → a hot/serious lead (buying signal), distinct from merely "مهتم" (interested).
- "الملف التعريفي" → the per-product intro/brochure PDF the agent SENDS to customers in WhatsApp —
  distinct from ملف المعرفة (Pitch Deck) the agent READS for answers.
- "الملف التعريفي للشركة" → the lean-proposal-deck skill's §5 Company Profile section (Lean's own
  credentials inside a proposal) — NOT the user's "الملف التعريفي" above; always use the
  disambiguated form when the skill's section is meant.
- 2026-08-13 R49-R50 [stated ×2, defect reports]: «this doesnt represent the real interation make
  it reflect the agent and customer feedback» (a ١٠٠٪ اكتمال السياق gauge) and «just sent a
  campaign why this data is not real ? the user hasnt seen it» (ردّوا ٢ · شوهدت ٢ · مهتم ١ minutes
  after a send nobody opened, while فشل read ٠ against two real failures). → COROLLARY TO RULE 2,
  promoted: **a number attributed to an EVENT must be scoped to that event.** Lifetime contact
  state rendered as campaign state is the same lie as an invented number — the founder catches it
  within minutes because he knows what he just did. Fourth signal in the real-numbers cluster
  (R23 test/real, R27 decorative fires, R28-30, now R49-50): the axis is provenance, and time is
  a provenance axis exactly like test-vs-real. Also: a "context completeness" score is a score he
  never earned; what he wants in its place is the conversation itself — turn counts, his customer's
  own longest sentence verbatim, whose turn it is (consistent with R27/R34's causal-evidence bar).
- 2026-08-13 R50 [CPO gate lesson, engineering discipline — not a user preference]: the first fix
  for the above (f26a2c1) was correct TypeScript, compiled clean, read correct, and was a NO-OP in
  production: `created_at` is BIGINT and node-pg returns int8 as a STRING of digits, so
  `Date.parse("1786644640706")` → NaN and the window collapsed to 0 — the maximally permissive
  value, which re-credited every historical event to the newest send. The fixture that "proved" it
  used an ISO string the author invented; fixture and code were wrong together and agreed.
  Two durable rules: (1) **a fix must be exercised against the shape the SOURCE returns, never the
  shape the fixture assumes** — for any value crossing a boundary (DB, webhook, API), capture the
  raw value and its `typeof` from the live boundary before writing the parser, and build the
  fixture from that capture; (2) **a parse fallback on a truth surface must fail CLOSED** —
  returning 0 for "I could not read the launch time" means "show everything", which defaults the
  failure mode to the exact lie being fixed; `Infinity` (show nothing) is the only honest default.
  Enforced now by `scripts/check-campaign-scope.mjs` in `npm run check`, which executes the SHIPPED
  campStats against real-shape fixtures and was demonstrated to fail 8 assertions on the no-op.
