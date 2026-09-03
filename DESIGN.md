# DESIGN.md — Massar token authority

**Read this before writing any UI code. These tokens override newly invented values.**

Full spec, with rationale and the RTL translation reasoning:
`docs/artifacts/campaigns-crm/frappe-visual-system.md` (cycle V1) and
`docs/artifacts/campaigns-crm/frappe-shell.md` (cycle V2 — shell, sidebar, kanban).
Selection record: `design/approved.json`.

## Current visual system
**Frappe UI, translated to RTL/Arabic** — adopted Aug 2026 by explicit founder decision
(option B). Rule 3 ("adopt the pattern, never the palette") now governs **branding only**.

## Non-negotiable invariants
1. **Greys are pure neutral, zero chroma.** `#F8F8F8 #F3F3F3 #EDEDED #E2E2E2 #C7C7C7 #999999
   #7C7C7C #525252 #383838 #171717 #0F0F0F`. No blue-tinted grey (`#EAECF0`, `#98A2B3`,
   `#667085`, `#475467`, `#101828`, `#F4F6FA`, `#F9FAFB`) may re-enter the content canvas.
2. **Canvas is `#FFFFFF`.** `#F8F8F8` marks strips, never pages. The sidebar is a strip.
3. **Teal `#1F7A73` is the only accent**, and only in: the one primary button per screen, focus
   rings, the selected-row `border-inline-start`, checkbox `accent-color`, progress fill, and
   the 28px sidebar `م` mark. **Gold `#C9A227` and the navy gradient are retired from the
   product** (V2, founder decision — the dark sidebar they lived on no longer exists).
4. **Type:** **Cairo** (founder's call, Aug 18 — overrides the V1 IBM Plex switch). Loaded as the
   VARIABLE face `wght@200..1000`, so it holds 450 natively; the swap existed only because the
   static Cairo cut jumps 400→500. Base 14px / lh 1.45 / **ls 0** / weight 450. Ladder:
   11·12·13·**14**·15·18. Weight 700 is retired from list rows.
5. **`letter-spacing: 0` on all Arabic.** `0.02em` is Latin/LTR spans only.
6. **Lightest text token is `#7C7C7C`** (4.76:1). `#999999` = icons and placeholders only.
7. **Radii:** buttons/inputs `6`, cards/modals `10`, pills `999`, **list wrapper `0`**.
8. **List rows:** flush, `border-top 1px #EDEDED`, block padding 8px, gutters 20/12,
   min-height 36px. No card wrapper, no shadow. Row state is a dot + label, never a filled chip.
9. **Spacing:** row block 8 · gutters 12/20 · control bar 16/20 · gap 8.

## Correctness rules that outrank all taste
- Arabic-Indic numerals via `fmtN`; `check:numerals` must stay green.
- RTL **logical properties only** — no `left`/`right`, no physical offsets.
- Honest-absence vocabulary: «لم تُرسل بعد» · «بلا جمهور» · «—»; `crmRate` may return `null`.
- No invented values. Denser rows do not get filled with computed placeholders.
- The dashed `.c-read` chip keeps its dash (assistant reading ≠ recorded fact).
- `src/dashboard.ts`: anchored single-property replacements only (ADR-0001).

## Charts, and what a chart is allowed to encode  (added 2026-08-19)

1. **A chart's geometry must be its data.** The city treemap's tiles were flex items in a wrapping
   row, so flex-grow measured against whatever survived the wrap and «الجنوب ١» drew larger than
   «الرياض ٥». An area chart whose areas invert the data is worse than no chart. Where a shape
   cannot be trusted to encode the value, use a horizontal bar, whose length is unambiguous.
2. **A funnel is drawn as a funnel.** Each band's top edge is the stage above it and its bottom edge
   is its own value, so the slope between two bands IS the drop. Equal stages draw a column — the
   honest picture of a campaign that lost nobody.
3. **Time runs right to left**, like the language. Mirror the x mapping; do not reverse the array.
   A curve whose newest point sits opposite its own «اليوم» label is a bug, not a style.
4. **One accent per surface.** Teal `#1F7A73` is the only saturated hue in a chart. A single-hue
   ramp may encode ORDER (funnel depth); it may never encode a second meaning. Four bars in four
   colours taught that teal, green and navy meant something. They did not.
5. **A label you truncate is a label you did not draw.** No `text-overflow` on an axis: if the
   category name does not fit horizontally, the chart is the wrong orientation.
6. **Zero denominators render «—», never «٠٪».** A rate over nothing is unmeasured, not zero.
7. **No decoration that carries no data**: no pastel icon discs on number cards, no hover lift on a
   non-interactive card, no gauge over a two-state boolean, no gradient that is not a value ramp.

## Lists at production scale  (added 2026-08-19)

8. **Truncation is not pagination.** A list that slices to N and says «narrow your search» is
   lying: search narrows the same list and slices the same N. Every flat list uses `pageSlice` and
   states «٦١–١٢٠ من ١٬٧٠٠» — the range is the sentence that tells the reader the list continues.
9. **Per-group preview caps are allowed on GROUPED surfaces only**, and must state the whole
   group's count in its header.
10. **A count in the chrome is a count of work OWED, never a total.** «العملاء ١٬٧٠٠» is
    decoration; «فرص البيع ٤» is a reason to click.
11. **Elapsed time is stated in the unit a person would say it in** — hours under two days, then
    days, then months. «منذ ٢٬٨٧٩ ساعة» is arithmetically true and unreadable.
12. **A shortlist must say what it is a top-of.** «٩ إجراء» above 359 qualified contacts reads as
    nine things to do.
13. **A page must have a point of view.** Five identical number cards is a spreadsheet: one figure
    leads at the size that says so, the rest support it. Equal weight everywhere is no hierarchy.
14. **Every new list design is verified at production scale** (`npm run qa:scale`: 200 campaigns,
    3,000 targets, 1,000 onboarded), not at demo scale. Six defects in this file were invisible at
    16 contacts.

## Motion and the half-second after a click  (added 2026-09-03)

Two external references are consulted on any UI work, alongside the invariants above and never over
them:

- **transitions.dev** — the named UI transition patterns (card resize, number pop-in, text-state
  swap, origin-aware dropdown, modal, panel reveal, icon swap, success check, page side-by-side).
- **interior.dev** — micro-interactions for the half-second after a click: *"the fade a beat too
  slow, the spinner outliving the request, the row that jumps as it loads."*

They govern TIMING and BEHAVIOUR, never palette, type or spacing — invariants 1 to 9 win on those.
The engine is server-rendered, so interior.dev's React components are read as a specification of
behaviour, not installed. Every state a surface can be in (pending, optimistic, settled, failed) is
designed, because today the dashboard has one `transition: width` and almost no state-change motion
at all: a tap, a stage move and a list refresh all land instantly and flatly.
