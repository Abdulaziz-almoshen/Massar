# CPO acceptance — campaigns-crm

**Verdict: ITERATE** · round-30 · envelope `.orbit/cpo/round-30.json`
**Commit-bound:** parent `f2203dd5b1d7480225771ec908322dd61ad21680` · engine `3273b1e1db8ea812c295dc806008d9f2a4a97070`
**Gate:** `delivery-quality-gate.py --commit f2203dd5b1d…` → `passed: true`
(an abbreviated `--commit` returns a false `blocked` — the gate string-compares the sha; filed as N2)
**Memory:** checkpoint clean, request 113 reviewed, zero pending events.

**The goal, restated as intent:** give him his campaigns module re-expressed with Frappe CRM's
*working model* — list/group/board, real filters, multi-select bulk actions, a tabbed record — in
Massar's RTL Arabic, so operating a campaign stops being one scrolling table.

**Scores** — intent fidelity 7 · completeness 6 · coherence 6 · taste 8 · surprise 7.
ACCEPT needs intent fidelity **and** completeness ≥ 8 with nothing `must` open. Neither clears.

---

## What I verified myself, rather than accepting

- Rebuilt the exact commit in a clean worktree: `npm ci`, `npm run build` (strict tsc) and
  `npm run check` all exit 0; `check:crm` 21/21. Not quoted — run.
- Recomputed all six pixel ratios in Pillow. Every one reproduces exactly
  (0.00177 / 0.000632 / 0.000515 / 0.00154 / 0.000692 / 0.000488), all six baseline/actual pairs are
  distinct sha256, every baseline predates its actual. **Evidence integrity: clean, second round running.**
- Opened all 27 captures at three viewports and read the screens as a founder about to demo.
  Twice my first read was wrong and zooming corrected it (the hero's «٠٪» is the Arabic-Indic zero,
  not a tofu box; the targets filter reads «٦» not «١»). Both corrections are why the findings below
  are the ones that survived.
- Read `src/campaigns-crm.ts` end to end and traced every network call: exactly one,
  `POST /admin/campaign/test`. No send path exists in this module.

---

## Your four decisions, ruled

**1 — Kanban built. UPHELD.** He asked for Frappe's view model and the board is its most legible
half. Keying it on التصنيف / الخدمة / شهر الإطلاق / حالة الأداء invents no lifecycle, and refusing
the drag where nothing can be persisted — with the board saying *why* — is the honest version of a
feature that is usually where invented state enters a product. BA was right; you ruled correctly.

**2 — Field rail dropped. UPHELD, and it was the better call.** I re-ran the census rather than
taking it: the campaign has six fields, the header renders four, `message` was the one substantive
unrendered field. A rail would have been four read-only repeats of the header wrapped around one
real value — structure without content, which is precisely the pattern I hunt under slop. The
launch strip exposes the one field that mattered and does it better than a rail would have.

**3 — «مكتملة» retired. UPHELD IN PRINCIPLE, INCOMPLETE IN EXECUTION.** Retiring it was right:
nothing on the campaigns table could back the claim, and changing a label he has seen is cheap next
to leaving a false one. But see M1 — the replacement vocabulary has no word for the state that the
*same commit* taught the verdict to say, so the two now contradict each other on one screen.

**4 — The not-ported list. UPHELD for the six named, INCOMPLETE as a list.** Every one of the six is
correctly out (no user table, no second entity, and a composer would be a send affordance under the
standing zero-send rule). But **FR-2 (the filter condition builder) and FR-5 (the columns picker)
are also not built**, each with its own AC, and neither appears in the list handed to me. Your own
QA had already recorded it — RTM AC-1 is marked CONCERNS with exactly this text. It did not travel.

---

## The central question you asked me to call

**Does this read as "exact design and UX and functionality" of Frappe CRM — or is he short-changed?**

My call: **the pattern port is genuinely there, and it is not what will disappoint him.** The view
switcher, the quick filters, row selection with a floating bulk bar, a board that drags only where a
write exists, a tabbed record — that *is* the Frappe working model, re-expressed in navy/teal RTL
Arabic with zero borrowed branding. Rule 3 is honoured about as well as it has been in this project.
The bulk bar in particular is best-in-class-grade and reads as Massar's own, not as a port.

What will disappoint him is smaller and more fixable than the framing feared: he will click the
control bar looking for Frappe's filter chips and not find them, and he will notice that a screen
told him a campaign has «بلا ردود بعد» directly above a sentence saying it was never sent. The first
is a scope call I am **not** asking you to reverse — a condition builder over three campaigns is
theatre — but it must be *said*, not discovered. The second is a correctness defect and it is a
one-function fix.

**Is the launch strip + 3-tab record better than the single scroll?** Yes on the strip, unreservedly
— `camp.message` has been stored and invisible for the whole project, and showing it in its own
medium with «لا يقبل التعديل بعد الإطلاق» stating the constraint is the round's best idea. Qualified
yes on the tabs: the hero keeps the three headline rates page-level, which is the right thing to
refuse to hide. The cost is that «الخطوة التالية» — the action points he asked for by name — now
takes a click (S4).

---

## Must-list, in order

1. **M1 — teach `campPerfState` the word `crmVerdict` already knows.** A campaign with no send
   (`targeted===0` or `sent===0 && delivered===0`) gets its own state and label. Because BR-2's
   one-function design already exists, this lands on the row chip, the حالة الأداء column, the group
   header and the record header in one edit — verify all four, don't credit them. **(b)** In the same
   edit make the rates honest for that state: nothing sent means the view/reply rates are undefined,
   not ٠٪ — return `null` so the hero shows «—» exactly as the zero-target case already does, and the
   row's التقدّم with it.
   *Proof:* the never-sent record where chip, hero and all three rates say the same thing.
2. **M2 — column headers in تجميع.** `crmGroupView` never emits the header row `crmListView` emits,
   so at every viewport the group cards show four unlabelled numbers, three of them identical-looking.
3. **M3 — resolve the board-vs-pill contradiction.** «تجريبية ٠» on the board beside «تجريبية (١)» on
   the pill. Run the class board over all campaigns (tab visibly neutralised) or suppress it under a
   class filter. Decide, too, what the operator sees when a drag moves a card out of the active tab —
   today it silently vanishes.
4. **M4 — close the disclosure gap.** Record the FR-2/FR-5 descope as an explicit dated decision with
   its re-trigger (my ruling: columns picker cancelled; filter builder deferred until ~30 campaigns or
   the first request to slice by a counter or a date). Then tell him in **one line**. Build neither.
5. **M5 — deploy.** He cannot see any of this. Deploy the **reviewed commit**, not the working tree —
   the engine repo is dirty with the concurrent crm-record session's `agent.ts`/`db.ts`/`index.ts`/
   `tracker.ts`, which must not ride out under this cycle's name. Then smoke 7/7 and health green.

Shoulds (S1 phone row · S2 drop keyed on a label · S3 dead expand link · S4 action points demoted ·
S5 fallback removal trigger) and nices are in the envelope with their locations.

---

## Credit, recorded so this gate stays calibrated

- **The QA→fix loop worked as designed.** QA FAILED a hard AC (تحديد المطابقين never implemented) and
  found an invented STATE (a zero-target campaign whose verdict claimed it had been sent); both were
  closed at the root — the second by *naming* the missing concept as `crmVerdict()` rather than
  patching the string. That is the correct instinct, and M1 is the same instinct applied one surface
  further.
- **The builder repaired two of its own vacuous assertions unprompted** — a selector matching nothing,
  and a single-point sample at x=767 against an element starting at x=800 — and said so in the commit
  message. That is the round-26 corollary («ask what input would make this red») being applied by the
  loop to itself.
- **The instruments describe themselves.** `check:crm` prints that it does not execute the views;
  `a11y.json` names contrast and focus-order as uncovered; every visual note declares a first-time
  baseline and states that a 0.0 would have meant the files were identical. Rule 7's structural
  solution is holding.
- **The module owns no statistic.** Every count comes from the existing `campStats`/`campWin` path, so
  the event-scoping that R49/R50 forced cannot drift in a second implementation. That decision, stated
  in the file header, is why this round has no fabricated-number finding at all.

*Not accepted — but the distance to acceptance is four small edits and a deploy.*
