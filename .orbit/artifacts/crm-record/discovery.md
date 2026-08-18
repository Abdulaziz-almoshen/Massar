# Discovery — the client record (`#customer/<phone>`)

Cycle `crm-record` · task #13 · `[product-discovery]`

## 1. The job this screen is hired for

Moment of use: the sorter hands over a list; he opens **one clinic out of ~18,000**. The 10-second
decision is *"does this account get a human's next hour, or get parked/dropped — and if it gets it,
what do I lead with?"*

Job story: **When I open one contact out of thousands, I want the FACTS about this clinic separated
from the AI's GUESSES, so I can commit a rep's time without re-reading the transcript — and not be
embarrassed on the call by something a machine invented.**

Second job, same screen, currently impossible: *after the call, write down what I learned so nobody
re-litigates it and the AI can't overwrite it.* Evidence (inferred from repo, not interviews):
`Contact` (tracker.ts:14–41) has no org fields at all — no decision-maker, branches, owner, note; the
only human-writable state is `outcome`, `tags`, `human`, `test`.

## 2. Riskiest assumption — what "enrich" means

Reading: **(a) operator-written facts + (c) better visual indicators, where (c) exists to trigger (a).
Not (b).**

Grammar: "indicators **for users to enrich them**" makes *users* the actor and *them* (the clients) the
object. If he meant an automatic pull, users would not be the subject. If he meant visuals only,
"enrich" is the wrong verb — an indicator displays a client, it does not enrich one.

History is the stronger evidence: every accepted correction in this codebase is the same complaint —
**the screen asserted a guess where he expected a fact.** Round-22 deleted a fabricated readiness card
and six authored knowledge scores; `«نتيجة موثقة يدويًا»` matched nothing any writer produced; the
"customer's voice" field showed the *longest* message. And his own earlier line — "no indicators of
the client stage and level of interest **still**" — the *still* means the AI's reading was already on
screen and did not count as an indicator.

"Like HubSpot" decodes identically: a HubSpot record is a left rail of **owned, editable, attributed
properties** plus a timeline. Massar has the timeline and the AI opinion; it owns no properties.

Falsifiable form: **the operator holds facts the AI cannot know, and will type them in once the screen
shows a visible hole.** High importance, near-zero evidence — nobody has ever typed a fact into Massar
because no field exists. Runner-up risk: editable fields make provenance *worse* unless every field is
stamped human vs. agent.

## 3. Cheapest build that proves it

One **facts panel** above the AI card. Six fields, no more: decision-maker (name + role), organisation
(branches/size), product interest (reuse `replaceTags`), next step + date, one free note, disqualify
reason. Each renders in exactly one of three states — **حقيقة** (human, with who/when), **قراءة** (AI,
with one-tap «أكّد» → becomes fact, «صحّح» → overwrite), **ناقص** (a visible hole, tap to fill). Cost:
one type `{value, source:'human'|'agent', by, ts}`, one PATCH route, one panel. *Quick win that can ship
alone:* the tap-to-confirm on readings already on screen.

Pass/fail after two working days over ≥20 real contacts: **PASS** if ≥60% of opened contacts carry ≥1
human-written field and ≥1 AI reading was corrected. **FAIL** → he only confirms, never writes → the
need was visual; keep confirm/deny, delete the editors.

Rejected en route: enrichment vendor (no Saudi clinic source wired), a free-text notes wall
(unqueryable at 18k), org-hierarchy model first (right later, premature now), richer AI inference (more
guessing — the exact complaint).

**Surprise dividend:** every confirmation/correction is typed, dated, attributed — so the sorter gets a
free labelled eval set, and Massar can publish its first honest number: *"the agent's interest reading
is confirmed X% of the time."* That is the only thing that makes an 18,000-contact blast trustworthy.
He asked for indicators; he gets a measurable sorter.

## 4. Do not build

Deal pipeline with amounts/probability/forecast (no prices; sorter, not closer) · numeric lead score
(the banned invented-number defect) · email/calendar sync · workflow builder · custom-property admin UI
(hardcode the six) · assignment, permissions, teammate activity feed (one operator) · duplicate merge and
company hierarchy (defer) · third-party enrichment. And **shrink**, don't grow, the 6-step مرحلة البيع
chip — it is an inference that changes no decision.
