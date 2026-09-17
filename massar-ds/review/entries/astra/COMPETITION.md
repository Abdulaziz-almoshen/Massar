# Massar design competition — the brief

Two models get this identical brief and produce independent work. The founder picks. Nothing is
merged from both by default: a blend of two design systems is how Massar got 2,765 class
definitions across 28 prefixes in the first place.

---

## The product

**Massar (مسار)** is Lean's Arabic-first, RTL sales platform. Postgres + Fastify. The dashboard is
a single-page app whose screens are template literals in TypeScript modules.

**The reader is the founder**, and he opens it to answer one question in five seconds:

> **«هل سنحقق الرقم؟»** — are we going to hit the number?

He is numbers-literate and detail-obsessed. His North Star is money actually collected. He does not
want prose, tours, or explanations. He wants the figure and what is blocking it.

**Twenty-six screens**, seven doors: الرئيسية · فرص البيع · العملاء · المنتجات · الحملات · التقارير ·
الإعدادات. Sub-tabs under five of them. Detail routes for a product, an account, a customer, a
sector, a campaign.

---

## The real data — this is the whole dataset, and it is mostly empty

Do not design for a full dashboard. **Design for this**, because this is what production holds:

| Fact | Value |
| --- | --- |
| Won revenue | **0 ر.س**. No closed deal, ever. |
| Recorded target | **34,000 ر.س** — on ONE product (الإجازات المرضية), for ONE quarter (Q3) |
| Products | **8**. Seven have no target recorded at all |
| Products with no published price | 1 (six publish a basis, not a figure) |
| Products with an inferred sector | 4 |
| Products the assistant will not sell | 1 |
| Open opportunity lines | **6**. One is priced (4,200 ر.س); five are not |
| Stagnation | every line 3–24 days without a stage change |
| Accounts | 16, all approved, **none has an owner assigned** |
| Campaigns | 1 (الحملة 38): 21 sent, 19 delivered, 12 seen, 4 replied, 2 interested, 0 opportunities |
| Knowledge readiness | 34/100. 3 of 8 sections complete |

**An empty state is the normal state here, not an edge case.** A design that only looks good with
data is the wrong design for this product. Six different kinds of empty must stay visually and
verbally distinct: «لم يُسعَّر» · «لم يُصنَّف» · «لا بنود مفتوحة» · «بلا مستهدف» · «لم تُسجَّل» ·
«لا سعر منشور». One grey em-dash for all six is a failure.

---

## What a prior GPT review (Astra) already blocked, and why it matters

It returned **Block** on five findings. Every one was the same defect: **the page printed figures
the records do not contain.**

1. A monthly target series produced by dividing the annual target by twelve — but that target is
   Q3-only and single-product. Periods with no target got a fabricated "required to date".
2. «6 على المسار» labelled six stationary lines healthy.
3. A funnel drop of «▾ 75%» between stage populations that were never a tracked cohort.
4. A weighted forecast with no probability model behind it.
5. Summaries disagreeing with their own tables — the nav said 6 products, the page said "5 of 6",
   the truth was 8 and 7.

**The bar this sets:** every figure traces to a stored value or is not shown. `annualTarget` is
`number | null` in the schema, and **null means no target recorded, which is not a target of zero.**
Do not compute an attainment percentage over partial coverage: it reads as company performance and
it is one product's quarter wearing the company's name.

---

## Hard constraints — violating any of these disqualifies the entry

1. **RTL, always.** Logical properties only: `inline-start`, `inline-end`, `padding-block`,
   `margin-inline`. Never `left`/`right`/`padding-left`. Time runs right to left in any chart.
2. **Western numerals**, wrapped: `.m-n { direction: ltr; unicode-bidi: isolate; tabular-nums }`.
   A percent sign or currency goes INSIDE the isolate span or it renders on the wrong side.
3. **Arabic counted nouns are four-way**, never `n + noun`: مفرد / مثنى / جمع القلة (3–10) /
   تمييز (11+). «6 بندًا» is wrong; «6 بنود» is right.
4. **One accent.** Colour means status, never decoration. No gradients on data surfaces.
5. **Motion:** one curve, enter 180ms, exit 120ms, press 100ms, `scale(.97)` on `:active`.
   Never enter from `scale(0)`. Hover behind `@media (hover:hover) and (pointer:fine)`.
   `prefers-reduced-motion` honoured. Nothing over 300ms.
6. **No AI slop.** No explanatory paragraphs, no "Welcome back", no invented insights, no advice
   the data cannot support, no decorative iconography. Enterprise density, not a consumer app.
7. **Every screen's data is fixed.** You may reorganise, re-rank and re-present. You may not invent
   a field, drop a field, or add a metric the records cannot produce.

---

## The eight directions already rejected by the founder

Do not resubmit these: a blue SaaS dashboard; card grids of KPI tiles; a dark "executive deck";
pastel fintech; gradient hero numbers; sidebar-with-avatar-and-search-bar boilerplate; anything
that looks like a Tailwind UI template; anything where the leading figure is smaller than the
chrome around it.

---

## What to deliver

1. **`SYSTEM.md`** — the design system as rules, not adjectives. Tokens with measured values, the
   type scale with the reason each level exists, the component vocabulary, the motion spec.
   Where a value came from a real reference implementation, say which and what you measured.
2. **`home.html`** — one complete, self-contained, runnable screen against the real data above.
   Inline CSS is fine. It must render correctly at 1440px and at 400px.
3. **`ledger.html`** — the table/board screen: 6 open lines, 5 unpriced, stage, days stationary.
   This is the densest surface in the product and the one the system lives or dies on.
4. **`RATIONALE.md`** — at most one page. What is the single idea holding the system together,
   what did you deliberately NOT do, and where is your design weakest.

## How the entries are judged

| Weight | Criterion |
| --- | --- |
| 30% | **Truthfulness.** Does every figure trace to a record? Are the six empties distinct? |
| 25% | **The five-second question.** Does «هل سنحقق الرقم؟» answer itself on open? |
| 20% | **Density and craft at the table.** This is a CRM; the ledger is where it is used. |
| 15% | **RTL and Arabic correctness.** Grammar, numerals, logical properties. |
| 10% | **Motion and state.** Correct, restrained, reduced-motion honoured. |

A beautiful entry that fabricates one number loses to a plain entry that fabricates none.
