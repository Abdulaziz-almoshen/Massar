# مسار: make the limits visible

**Organising idea.** Answer “هل سنحقق الرقم؟” before asking the founder to interpret a chart: no revenue has closed, and incomplete pricing and targets prevent a coverage judgment. A compact summary gives the three distinct facts: all-time won revenue, the sole product-quarter target, and the uncertainty. Six cards underneath read three across in RTL; they stack into one column on a narrow screen.

**Graphs and their records.**

- **Stages:** three bars at 4/1/1 for تواصل أولي / اكتشاف الحاجة / عرض السعر, plus five explicitly empty stage cells. All eight rungs are accounted for. The five other names and their positions were not supplied, so they are not invented. Bars share one scale.
- **Time without movement:** independent columns at 3/9/16/21/24/24 days, increasing from the right. Blue identifies the observed maximum, not an invented overdue threshold. The columns are not a time series, and no line identities or stage-to-duration joins are assumed.
- **Campaign 38:** six columns at 21/19/12/4/2/0, following the same cohort from sending at the right to opportunities at the left. Zero is a baseline marker, not a minimum-height bar. No conversion rates.
- **Targets:** eight product cells, one recorded and seven hatched as missing; four equal quarter cells, Q1 at the right through Q4 at the left. Only Q3 carries 34,000 ر.س, for الإجازات المرضية. These encode recording coverage, never achievement or monetary magnitude.
- **Pricing and ownership:** six pricing cells distinguish one priced line (4,200 ر.س) from five unknown amounts; sixteen unassigned account cells trace to the sixteen approved accounts. The sector list retains 4 hospital lines, two pharmacy lines, and genuinely no business lines; hospitals are the only targeted sector.
- **Knowledge:** a ring uses the supplied 34/100 score. The separately supplied 3/8 completed sections are stated alongside it; the score is not derived from that fraction.

**Refused.** No revenue trend, forecast, required-to-date line, annualised target, invented quarter/month allocation, pipeline-to-target ratio, synthetic record identifiers, or attribution of existing opportunities to the campaign. The records do not support them. No percentage hides a denominator; counts and stated scores suffice.

**Semantics and interaction.** Blue marks recording, maximum age, or attention/action status; other observations are neutral. Missing numbers use `m-nil--owed`, unassigned ownership uses `m-nil--unset`, and legitimate absence uses `m-nil--none`. Western numerals isolate direction, including currency and fractions. Navigation and evidence dialogs work locally. Only infrequent pointer-opened dialogs animate: 180ms in, 120ms out; press is 100ms at scale(.97), with one curve. Keyboard and reduced-motion interactions are instant. CSS uses logical dimensions and positioning. Google Fonts is optional, with local fallbacks.

**Verified.** Chromium at 1440px and 400px, including blocked font requests: no horizontal overflow, correct column stacking, RTL chart order, isolated numbers, and corrected fraction/axis direction. All seven dialogs, keyboard opening, Escape, focus return, backdrop dismissal, navigation, and reduced motion passed.

**Weakest point.** This is a static decision surface, not a forecast or connected work queue. Without line identities, product links, or timestamps, it can identify missing information but cannot direct the founder to a specific stalled deal. Mobile preserves all evidence at the cost of a longer scroll. Real-device touch and safe-area behavior require hardware verification.
