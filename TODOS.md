# TODOS

## Programme scope

### Keep the 12-week vertical slice on the shelf

**What:** A fully specified fallback to the 47-week Massar v2 programme, reaching the founder's core
outcome in twelve weeks. Weeks 1-2: the thin pilot plus minimal users and products. Weeks 3-4:
`handoffs` and `handoff_items` referencing today's `entities`, with spreadsheet import. Weeks 5-6:
sales inbox, assignment, tap-only call and visit outcomes. Weeks 7-9: the product-manager dashboard,
combining handoffs, manual outcomes, the existing opportunity board and existing WhatsApp history.
Weeks 10-12: production pilot, reconciliation, permissions, tests, rollout. v1 stays authoritative
and the slice reads from it; no cutover happens in these twelve weeks.

**Defers:** full account migration, dedup, merge and branches, configurable pipelines and forms,
voice and transcription, the AI payback loop, reminders, campaign migration, the WhatsApp adapter
rewrite, automatic claims, change-data-capture, and v1 retirement.

**Why:** the approved programme reached 40.5 weeks of work (47 buffered) after the engineering
review, a 65% increase driven by choosing the most complete option on eleven of thirteen findings.
Every addition is defensible alone. If the schedule stops being acceptable, this is the alternative,
and having it written down means taking it is a decision rather than a scramble.

**Trigger:** the three numbers from the handoff audit. If accounts never touched are few and the
median days from handoff to first contact is short, the blindness costs less than the programme
does, and this slice is the right shape. Proposed by Codex during the 2026-09-03 engineering review
and declined at the time; recorded so it stays available.

**Effort:** L (12 weeks, against 47)
**Priority:** P3 — an option, not a plan
**Depends on:** the handoff audit numbers.

## Operations

### Make the in-memory contact ceiling visible before it is reached

**What:** Report `contacts` count and process RSS on `GET /health`, and act when contacts cross
2,000 or RSS crosses 350MB by capping live transcripts or paging contacts from Postgres instead of
holding all of them.

**Why:** `tracker.ts` holds every contact in a `Map` and `hydrate()` fills it from Postgres at boot,
on a single 512MB Fly machine with `min_machines_running = 1`. At today's 21 contacts this is free.
The rep queue is the first surface that iterates the whole Map, and it arrives in the same quarter
as WhatsApp campaigns that would multiply contacts by two orders of magnitude. An OOM here is not a
slow page: it kills the one machine that also holds the webhook, and a dropped webhook can be an
«إيقاف».

**Related defect found in the same review, and arguably worse:** `db.ts:698` hydrates only the last
50 messages per contact (`rn <= 50`), so runtime memory grows uncapped but **every restart truncates
every transcript to 50 turns**. `readSeriousness` and `replyLatencies` therefore return different
answers before and after a deploy, which means a rep queue's ranking silently reshuffles on every
deploy. Found by the Codex outside voice; it contradicted this review's own claim that transcripts
were uncapped, and it was verified in the source.

**Effort:** S for the /health line (1h), M for the fix when the trigger fires
**Priority:** P2 — the instrumentation now, the fix on trigger
**Depends on:** nothing. The trigger depends on the campaign engine scaling, which is priority 1.

## Design system

### Amend DESIGN.md with a documented state palette

**What:** Write the semantic state hues into `DESIGN.md` as a named exception to rule 3: which four
hues exist, what each means, where each may appear, and the contrast floor each must clear.

**Why:** Rule 3 says teal `#1F7A73` is the only accent. The shipped product also uses navy
`#2F5F94` for «متجاوب» / «مهتم» / «نشطة» / «للتنفيذ», green for won, amber for warning and red for
lost, across roughly thirty sites in six files. Those hues carry meaning people read every day, so
the rule as written is the thing that is out of date. Today the token authority is a document the
code openly contradicts, which means no reviewer can tell a real drift from an accepted one.

**Context:** Found by /design-review on 2026-09-03 (finding 013) and confirmed independently by the
Codex source audit. Sites are in `dashboard.ts`, `campaigns-crm.ts`, `activity-crm.ts`,
`customers-crm.ts`, `opps-crm.ts` and `tasks-crm.ts`; grep `#2F5F94` for the full list. The teal
family (`#2E7D77`, `#3FB6B0` and the tints) is NOT part of this: it is one hue ramp and already
compliant. Once written, the palette is checkable, so the next drift is catchable.

**Effort:** S
**Priority:** P2
**Depends on:** None.

### Give the row checkbox a 44px tap area without growing the row

**What:** On coarse pointers, expand the selection cell's hit area to 44px with padding plus a
negative margin, leaving the visible checkbox at 20px and the row at 36px.

**Why:** Touch guidance wants 44px; `DESIGN.md` rule 8 fixes list rows at 36px, and that density is
what the product sells. A 44px control cannot sit inside a 36px row, so today the checkbox ships at
20px, which is the largest honest size inside the current rule and still under the guidance. Growing
the hit area satisfies both rules at once and changes nothing about how the list reads on a desktop.

**Context:** Found by /design-review on 2026-09-03 (finding 009 residue); the compromise and its
reason are already commented in the `@media (pointer: coarse)` block in `src/dashboard.ts`. Care is
needed so the expanded area does not swallow the row's own click target. Verify on a real touch
device or with device emulation: `(pointer: coarse)` never matches a headless desktop browser, which
is what made the first measurement of this fix read as a regression.

**Effort:** S
**Priority:** P3
**Depends on:** None.

## Tooling

### Make the smoke gate wait for the record route instead of racing it

**What:** Replace the fixed 4000ms wait in `massar-engine/scripts/smoke.py` with a wait on the
route's own content, or retry once before failing.

**Why:** The record route (`#customer/<phone>`) does a per-contact fetch after load. On a machine
that has just restarted, that fetch loses a 4-second race and the gate reports a broken deploy on a
page that works. It happened on this cycle's first deploy: 160 chars and a missing landmark, then
24,398 chars and green on a warm re-run, same build. A gate that fails for a reason outside the diff
teaches its operator to re-run it, which is exactly how the blank-page class it guards comes back.

**Context:** Found by /design-review on 2026-09-03 (finding 014). The script already has a precedent
for this reasoning in its third-party-CDN filter comment. Prefer waiting on the landmark string with
a timeout over lengthening the fixed sleep, so the gate stays fast when the machine is warm.

**Effort:** S
**Priority:** P2
**Depends on:** None.

## Work queue (slice A)

### Fold the customer's own stated time into the queue exit rule

**What:** When a contact filed as `later` carries `scheduledAt` (the agent's reading of the customer's words), hide the queue row until that time and show `scheduledSaid` verbatim as the reason.

**Why:** Slice A adds a rep-set follow-up store (`tasks.due_at`) beside one that already exists on the contact. The exit rule reads only the new one, so an AI-managed chat where the customer said «كلمني الأحد» resurfaces in the rep's queue too early.

**Context:** `massar-engine/src/tracker.ts` stores `scheduledSaid` verbatim and `scheduledAt` as an advisory reading, never shown as if the customer typed a date. The exit rule lives in `massar-engine/src/workqueue-domain.ts` (slice A) and takes the last tap and the follow-up date as inputs; this is one more input and one branch. Surface the phrase, never a bare date. Raised by the outside-voice review on 2026-09-03 (point 3).

**Effort:** S
**Priority:** P2
**Depends on:** slice A's `workqueue-domain.ts` exit rule shipped.

### Let the team stop maintaining the shared sheet

**What:** After the pilot, give the team a concrete reason to close the shared spreadsheet: either Massar writes seriousness, last contact, and next action back into the sheet's columns, or the sheet is retired once the CEO's pipeline view exists.

**Why:** Slice A imports the sheet into Massar but nothing flows back, so the sheet stays the team's source of truth and Massar is a second place to record. The weekly check-in question «هل فتحت الجدول؟» will be yes for structural reasons, not adoption ones.

**Context:** Write-back was Approach C in the 2026-09-03 office hours (declined as the whole product, still the cheapest bridge). A Google Sheets connector is a new dependency and a new credential; retiring the sheet needs the CEO reports that `docs/designs/massar-commercial-platform.md` gates on non-zero adoption. This TODO is the trigger for that gate. Raised by the outside-voice review (point 13).

**Effort:** M
**Priority:** P2
**Depends on:** slice A live for two weeks and the adoption count read once.

### Let a task link to an opportunity line

**What:** Extend `tasks.ref_kind` (CHECK constraint in `massar-engine/src/db.ts` and `REF_KIND`) to accept `opportunity`, and show line-linked tasks on the card in «فرص البيع».

**Why:** Slice A attaches follow-up tasks to the contact by phone because the constraint allows only `contact` or `campaign`. A follow-up about one product line of a two-line account is therefore account-level, and the board cannot show «الخطوة التالية: الثلاثاء» on the right card.

**Context:** The schema comment says a third kind must add a constraint, not a convention; this is that constraint. One migration (`ALTER TABLE tasks DROP CONSTRAINT … ADD CONSTRAINT …`) on a live schema in a public repo, plus a third link label on the tasks screen. Only matters once accounts carry several products. Raised in the 2026-09-03 engineering review (findings 7 and 12).

**Effort:** S
**Priority:** P3
**Depends on:** slice A shipped.

## Completed

## From /autoplan, 2026-09-03 (four-phase review of the platform plan)

### Fix the five live production defects
**What:** Found while verifying claims about the plan, not caused by it.
1. `index.ts:41` acks the Gupshup webhook before persisting — a crash loses the event, including
   an inbound «إيقاف», and the number stays sendable.
2. `gupshup.ts:44` has no `AbortSignal`; `agent.ts:1503-1509` re-sends the same content as text
   when a quick-reply throws. A provider timeout that actually succeeded messages twice.
3. `db.ts:321` falls back to memory-only on a failed migration and `/health` still returns `ok:true`.
4. `index.ts:36` — `if (cfg.webhookToken && ...)` accepts every POST when the token is unset.
5. `index.ts:428` returns per-recipient launch failures; `dashboard.ts` never reads them.
**Priority:** P0 for 1 and 2. They are cheap and they are about consent and duplicate sends.

### SSO instead of hand-rolled sessions
**What:** Phase 2 ships password auth. For an internal Lean tool, SSO is the right answer.
**Why deferred:** blocked on Lean IT, not on this plan.
**Priority:** P2 — revisit when a second department joins.

### Arabic transcription for voice-note engagements
**What:** provider, dialect handling, speaker attribution, correction, consent, data residency.
**Why deferred:** outside the blast radius; already an open question.
**Priority:** P2.

### Retire the 12-week vertical slice entry, or take it
**What:** `TODOS.md` has carried a fully specified 12-week fallback since the v2 review, filed
"P3 — an option, not a plan", triggered by the handoff audit. The amended plan's Gate A now covers
the same ground inside the main plan.
**Priority:** P3 — resolve when The Assignment's three numbers exist.

## Found while building the sector board (2026-09-04, Lane C)

### Two production products the agent has never heard of

**What:** `/admin/tags` in production returns 8 products. `SERVICE_CATALOGUE` (insights.ts) and
`PRODUCTS` (agent.ts) both list 6. The extras are **«سجل التطعيمات الوطني»** and
**«صحة أعمال Plus»**. The agent cannot pitch, price or answer a question about either, and the
analyst files any mention of them under «خدمة أخرى».

**Why it matters:** they also have no sector, so they land in the «بلا قطاع» bucket on the new
sector board rather than in a sector total. That is deliberate and visible, not silent, but it is
a hole in the board until someone says which sector each belongs to.

**Needed:** a founder decision on the sector for each, then one `UPDATE product_meta` per product.
No deal stores a sector, so nothing else has to change. Adding them to the agent's KB is separate
and larger.

**Effort:** S for the sector (two UPDATEs) · M for agent KB coverage
**Priority:** P1 for the sector, P2 for the KB

### The catalogue drift check cannot see the live product list

**What:** `checkCatalogueDrift` (agent.ts:152) compares `PRODUCTS` against `SERVICE_CATALOGUE` —
two constants in the same repo. It never compares either against the `tags` table, which is what
deals actually store and what every board groups by. That is why the two products above drifted
in without a single warning, on a build that prints a drift check on every run.

**Needed:** extend the check to compare against live tags, or a boot-time log naming any tag with
no catalogue entry. Cannot throw (agent.ts is imported before the server listens; throwing
crash-loops the engine and takes down the opt-out path).

**Effort:** S
**Priority:** P2

### Rotate one rep portal token

**What:** on 2026-09-04 a `. ./.env` in this session hit an unquoted value on line 11 and zsh
echoed the value in its error text, putting one `REP_TOKENS` entry (rep name plus token) into the
session transcript. Not committed, not pushed, absent from the tracked tree — but printed.

**Needed:** rotate that rep's token in `.env` and `fly secrets`. Quoting the `REP_TOKENS` value in
`.env` prevents the recurrence.

**Effort:** S
**Priority:** P1

### Local dev database carries an orphan product tag

**What:** the `massar` dev database has a tag «تكامل الأنظمة» (no `(HIS/ERP)` suffix) holding 4
opportunities and a 4,000,000 target. It is residue from the incident where the DB test suite
truncated and re-seeded the dev database; the fixture seeds that exact short name. **Production
does not have it.** Left in place because deleting data needs approval, and because it is a
useful live example of the unclassified bucket doing its job.

**Effort:** S
**Priority:** P3 — local only

## The redesign eng review — all 19 items closed (2026-09-04)

Five lanes plus the three items that were never assigned to one. Recorded here because the review's
task list lived only in a conversation, never in `docs/artifacts/`.

| item | what it was | closed by |
|---|---|---|
| A | five CRM primitives declared once, not five times | `crm-primitives.ts` |
| R5 | reference price on the package, not the product | migration 004 + composite FK |
| R7 | `sectors` had no runtime writer, so the guard would fail by design | boot seed beside `seedDefaultPipeline` |
| R9 | three market sectors, structure only | migration 005 + `PRODUCT_SECTOR` |
| R10 | read endpoints for sectors / products / packages | `/admin/sales/sectors`, `/admin/products`, `/admin/sectors` |
| R12 | rail from fifteen doors to six, nothing orphaned | `NAV`/`SUBS` + gate step `check:nav` |
| R14 | `#home` off the 5s tick | tick + «مباشر» chip both scoped to الحملات |
| R19 | the exec dashboard says who it is for | rep-aware unauthorized gate |
| R16 | smoke + DB suite attached to a gate | `.github/workflows/ci.yml` |
| R17 | two mandatory regressions | `tests/safety-regressions.test.ts` |
| R18 | one «قيمة الفرصة» | `OPP_VALUE_SQL` + `tests/value-parity.test.ts` |
| R8 | product rename cascades all ten tables | migration 006 + gate step `check:rename` |
| R11 | the four named reports, specified | `src/reports-domain.ts` |
| R13 | four quarters in one pass, honest money label | `quarterlyPerformance` + `VALUE_BASIS_*` |

**Gate is now 21 steps. 235 unit tests + 47 DB-backed.**

### What this leaves open

- **Nothing is deployed.** Seven commits sit on local `master` in `massar-engine`, unpushed.
- **Two of the six doors lead to placeholders.** «المنتجات» and «التقارير» have real data and real
  endpoints behind them and no screen in front. That was never one of the 19 items — the review
  scoped endpoints — but a door that leads nowhere is visible to the founder in a way an unbuilt
  endpoint is not.
- **Sector for the two production-only products** and **rotating one rep token**, both above.

## Design-system debt, ratcheted by gate step 22 (2026-09-06)

`scripts/check-design.mjs` records a baseline and fails the build on any INCREASE. These four are
the recorded baseline — each may only shrink. Contrast and token categories are already at **0**.

### Migrate 413 off-ladder font sizes
**What:** `src/` uses 26 distinct font sizes; the DESIGN.md §2 ladder has 8. 11.5px appears 103
times, 12.5px 88, 10.5px 33 — none on the ladder.
**Why:** a type scale nobody follows is not a scale, and Arabic leading is currently per-author
(seven different line-heights).
**Context:** DESIGN.md §2 carries the migration map (`11.5 → --t-xs`, `13 → --t-sm`, etc). Purely
mechanical, but 413 edits across 14 modules, so it wants its own commit and a visual pass.
**Effort:** M · **Priority:** P2

### Retire `font-weight:700` — 129 uses
**What:** the pre-rebrand doc retired 700 from list rows; the rebrand dropped the rule and it is
now restored in DESIGN.md §2 (700 survives only on `--t-num` and `--t-3xl`).
**Why:** three weights is the ladder. 129 uses means the rule is losing.
**Depends on:** the ladder migration above. **Effort:** S · **Priority:** P3

### Move 13 integer z-index values onto the scale
**What:** 1, 5, 20, 30, 60, 69, 70, 99, 120, 140, 200 exist in `src/`. DESIGN.md §2 now defines
`--z-base` through `--z-tooltip`.
**Why:** the product has drawers, toasts, a tab strip and a new-items pill. A drawer opening behind
the sticky header is a certainty, not a risk, and the fix would be another arbitrary number.
**Effort:** S · **Priority:** P2

### Four KPI tiles are 73.7px wide on a phone
**What:** `.crm-kpis` is `repeat(4,1fr)` with no breakpoint. Measured at 390px: tiles 73.7px,
labels wrapping to four lines. `.pc-q` (the four quarters) is 84px each.
**Why:** DESIGN.md now defines `--bp-sm/md/lg`; nothing uses them. `/rep` is the phone surface but
the admin screens are reachable on a phone too.
**Effort:** S · **Priority:** P2

### Subnav tab is 43px under a coarse pointer
**What:** measured 43px; DESIGN.md §3.10 requires 44. The strip is 44px but carries a 1px border.
**Effort:** XS · **Priority:** P2

### Delete the dead `.userbox` CSS
**What:** `.userbox` is not in the DOM — a leftover of the retired navy sidebar. `.userbox .n` still
sets `color:#fff`, which would be invisible on today's light rail.
**Why:** dead CSS that fails a contrast reading and confuses the next reader. Not deleted in this
pass because ADR-0001 limits `dashboard.ts` to anchored single-property edits.
**Effort:** XS · **Priority:** P3
