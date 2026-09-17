# Redesign «الرئيسية» — layout and graphs

The founder rejected the current home layout. He supplied a reference (a light fintech dashboard:
a large balance figure with a dense time-series chart under it, then a three-column row of
Income-vs-Expenses, Financial Goals with progress rails, and Recent Transactions).

He wants: **better layout, and graphs.**

---

## The product

**Massar (مسار)** — Lean's Arabic-first, RTL sales platform. The reader is the founder. He opens
this page to answer one question in five seconds:

> **«هل سنحقق الرقم؟»** — are we going to hit the number?

---

## The hard part, and the reason a naive copy of the reference fails

The reference dashboard is dense with history. **Massar has almost none.** This is the entire
production dataset:

| Fact | Value |
| --- | --- |
| Won revenue, all time | **0 ر.س**. No deal has ever closed. |
| Recorded target | **34,000 ر.س** — ONE product (الإجازات المرضية), ONE quarter (Q3 2026) |
| Products | 8. **Seven have no target recorded at all** (null, not zero) |
| Open opportunity lines | **6**. One priced at 4,200 ر.س; five unpriced |
| Days without a stage change, per line | 3, 9, 16, 21, 24, 24 |
| Stages occupied | تواصل أولي (4), اكتشاف الحاجة (1), عرض السعر (1). Five other rungs empty |
| Sectors | قطاع المستشفيات (4 open, the only one targeted), قطاع الصيدليات (2 open), قطاع الأعمال (0) |
| Accounts | 16, all approved, **none has an owner assigned** |
| Campaign 38 | 21 sent → 19 delivered → 12 seen → 4 replied → 2 interested → 0 opportunities |
| Knowledge readiness | 34/100; 3 of 8 sections complete |
| Quarterly targets | Q3 = 34,000. Q1, Q2, Q4 = **no target recorded** |

**A revenue-over-time chart here would be a flat line at zero, and a fabricated one is worse.**
A previous design was blocked for exactly this: it divided the annual target by twelve to draw a
monthly series, inventing a "required to date" for periods that never had a target.

## What CAN be charted honestly, because the records support it

1. **Stage distribution** — 6 lines across 8 rungs. A real distribution; five rungs are genuinely
   empty and that emptiness is the finding.
2. **Days without movement, per line** — 3/9/16/21/24/24. Six real values. This is the closest
   thing to a trend the product has, and it is the founder's real risk signal.
3. **Campaign funnel** — 21/19/12/4/2/0. Six counts of ONE cohort followed through. A legitimate
   funnel. **Do not print a conversion rate between steps** unless it is that cohort's own.
4. **Quarterly target coverage** — 1 of 4 quarters carries a target. Draw the quarters, hatch or
   grey the three that have none. Never draw them as zero.
5. **Target coverage across products** — 1 of 8. A completeness meter, not a performance one.
6. **Knowledge readiness** — 34/100, 3 of 8 sections.

## Hard constraints — breaking any one disqualifies the work

1. **RTL.** Logical properties only (`inset-inline-start`, `padding-block`, `margin-inline`).
   Never `left`/`right`. **Time runs right to left** in any chart: the earliest point is at the
   RIGHT edge. A chart that runs left-to-right is simply wrong here.
2. **Western numerals**, each wrapped: `.m-n { direction:ltr; unicode-bidi:isolate; tabular-nums }`.
   A currency or `٪` that belongs to the number goes INSIDE that span or it renders on the wrong
   side of the digits.
3. **Arabic counted nouns are four-way**, never `n + noun`: مفرد / مثنى / جمع القلة (3–10) /
   تمييز (11+). «6 بنود» is right; «6 بندًا» is wrong.
4. **One accent** (`#245BD6`). Colour means status, never decoration. **No gradients on a data
   surface.** The reference's purple/blue gradient bars are explicitly out.
5. **Absences are typed, not dashed.** Three kinds, three treatments:
   `m-nil--owed` (a number someone owes: «لم يُسعَّر», «بلا مستهدف»),
   `m-nil--unset` (a classification nobody made: «لم يُصنَّف»),
   `m-nil--none` (a legitimate nothing: «لا بنود مفتوحة»).
   **Never a bare `—`.**
6. **Motion:** one curve, enter 180ms, exit 120ms, press 100ms with `scale(.97)`. Never enter from
   `scale(0)`. Hover behind `@media (hover:hover) and (pointer:fine)`. `prefers-reduced-motion`
   honoured. Nothing over 300ms. **No animation on anything triggered by a keyboard or repeated
   many times a day.**
7. **Invent nothing.** Every figure traces to the table above or is not shown. No forecast, no
   probability, no weighted pipeline presented as revenue, no rate whose denominator is not
   printed beside it, no percentage computed over a population different from its numerator.

## Layout requirement from the founder

- **Three columns.** He has said this twice. The leading revenue figure may span the full width;
  everything below reads three across and stacks on a narrow screen.
- Dense. The current version wastes enormous horizontal space — a 1658px row holding four short
  values, and three-quarters of the page empty.

## Deliver

1. `home.html` — one complete, self-contained, runnable file (inline CSS and JS, no build step,
   no external requests except a Google font if you want one). Must render correctly at **1440px
   and at 400px**. Use the real data above, verbatim.
2. `NOTES.md` — at most one page: the single organising idea, which graphs you chose and **what
   record each one is drawn from**, what you refused to draw and why, and where the design is
   weakest.

Judged on: does the five-second question answer itself; is every figure traceable; is the RTL and
Arabic correct; is it genuinely denser than what it replaces; and are the graphs honest about a
dataset that is mostly empty. A beautiful page that invents one number loses to a plain one that
invents none.
