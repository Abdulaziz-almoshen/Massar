# ASTRA BRIEF — Massar design, and why it is not good enough yet

You are gpt-6-astra. This is a HARD problem and we need your strength on it.
A founder has rejected this product's home page and dashboard EIGHT times in a
row over two days. Every rejection was some version of "this is not a good
design system and UX at all", "it looks old", "AI slop". We need a design that
looks like a HUMAN designer made it — clean, confident, restrained, and
obviously better than what is here now. Do not stop until it is done.

## The product
Massar (مسار) is Lean's Arabic-first, RTL sales-management platform for Saudi
healthcare. The primary user is THE FOUNDER. His five-second question is
«are we going to hit the number?». He is money-first, statistics-driven and
detail-oriented. His North Star is revenue booked.

## Hard constraints (non-negotiable)
- Arabic, RTL, Cairo font. Logical CSS properties only, never left/right.
- WESTERN numerals (0123456789), tabular figures.
- Arabic counted-noun grammar (مفرد/مثنى/جمع القلة/تمييز), never "n + noun".
- Time runs RIGHT to LEFT in charts: January at the right edge.
- Colour is never the only channel; every tone also carries a dot/label.
- Motion: one easing curve, UI motion under 300ms, exit faster than enter,
  scale(.97) press feedback, never enter from scale(0), every hover behind
  @media (hover:hover) and (pointer:fine), prefers-reduced-motion honoured.
- The founder supplied a reference image: a light fintech dashboard — near
  white ground, big tight display type, one huge figure with a delta pill,
  rounded soft cards, pill controls, a chart of gradient bars capped with dots
  over a dotted grid.

## THE REAL DATA (do not invent, do not drop, do not add)
Fiscal year 2026, today is 16 Sep 2026.
- Target 34,000 SAR — and it is set on ONE product, in Q3 ONLY. 7 of 8
  products have no target at all. So the headline % is structurally misleading.
- Achieved 0 SAR. Zero won deals all year.
- Open pipeline 4,200 SAR across 6 opportunity lines; only 1 line is priced.
- Every open line has been stuck 29-35 days. Last movement 18 Aug.
- 16 accounts, all approved, 0 with an owner, 0 with a contact, 7 have a sector,
  7 have a city.
- 21 contacts, 359 messages, 1,233 events. Campaign 38: sent 21, delivered 19,
  seen 12, replied 4, interested 2, opportunities 0.
- 3 sectors: قطاع المستشفيات, قطاع الصيدليات, قطاع الأعمال (+ بلا قطاع).
- 8 products: الإجازات المرضية (18,000 ر.س/سنة, target 34,000, open 4,200,
  readiness 80%), التقارير الطبية (68%), الشهادات الصحية (45%),
  تكامل الأنظمة HIS/ERP (45%), خدمات التطعيمات (45%), سجل التطعيمات الوطني
  (20,000 ر.س/سنة, 90%), صحة أعمال Plus (0%, not sold by the assistant),
  فحص الموظفين (73%). Four have an INFERRED sector needing confirmation.
- 7 stages: تواصل أولي(4) · اكتشاف الحاجة(1) · عرض المنتج(0) · التقييم التقني(0)
  · عرض السعر(1, 4,200) · التفاوض والاعتماد(0) · رابح(0) / خاسر(0).
- Knowledge has 8 weighted sections; الاعتراضات and المنافسون and الامتثال are 0%.

**The near-empty state IS the product's real state and will be for months.
A design that only looks right once the database is full is the wrong design.**

## What exists in this folder
- massar.css — the design system (one card, one row, one chip, one button,
  variants as modifiers). Table/input/select/checkbox/badge/tooltip geometry
  was PORTED FROM MEASURED VALUES off coss.com/ui and beui.dev.
- shell.js — animated side menu (256px <-> 68px, measured off beui.dev:
  label enters 200ms after an 80ms delay, exits 120ms) + sub-tab strip + dialogs.
- 26 screens mirroring the live app's routes exactly:
  home · opps/board/triage/pipeline · accounts/customers/indicators/tasks/notes
  · products/knowledge/perf/org · kmon/aimkt/targets/partners · reports
  · settings/divisions/team/users/audit · product · account
- gen.py generates all screens from one data model.

## YOUR TASK
Read massar.css, shell.js, home.html, products.html, product.html, opps.html,
reports.html. Then deliver a CONCRETE, OPINIONATED redesign that is clearly
better. Specifically:

1. **Diagnose what still makes this read as AI-generated rather than
   human-designed.** Be brutal and specific — name selectors, values, spacing,
   type sizes, the rhythm, the copy. "Looks generic" is not useful; "the card
   padding is uniform 24px everywhere, so nothing has weight" is.

2. **Fix the information architecture of HOME.** It currently stacks: money
   card -> quarters -> indicators (arcs/matrices/heat) -> funnel -> decisions
   -> board. That is six sections of equal weight. What should actually lead,
   what should be secondary, what should be removed entirely? The founder said
   "the indicators and the home page must be combined, they are not separate".

3. **Give exact CSS.** Token values, type scale with line-heights and tracking,
   the spacing rhythm, the card treatment, the grid. Write real CSS I can paste.

4. **Design the empty/near-empty state as the PRIMARY state**, not a fallback.

5. **Say what to delete.** The single most common failure here has been adding.

Anti-slop rules: no purple gradient palette, no 3-column feature grid, no
centred everything, no decorative blobs, no nested cards, no kicker above every
heading, no icon tile above every heading, no dark-mode glow.

Be specific. Be opinionated. Own the direction. Do not hedge.
