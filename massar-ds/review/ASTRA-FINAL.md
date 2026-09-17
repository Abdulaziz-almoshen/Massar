codex
**Massar should feel like a founder’s revenue ledger: one unmistakable number, an honest statement of what it means, and the work that can change it.**

The current page spends its attention budget drawing the database. It needs to spend that budget interpreting it.

**1. The diagnosis**

The most serious problems are factual. Visual polish currently makes them more convincing.

| Severity | Location | Before | Required change |
|---|---|---|---|
| HIGH | [home.html:97](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:97), `MONTHLY`, `sum()`, `paintQuarters()` | `TARGET / 12` distributes a **Q3-only, single-product target** across the year. Initial rendering changes the displayed requirement to **24,178**, and quarters receive **8,500** each. | Delete this allocation. Show **34,000 ر.س · الإجازات المرضية · الربع الثالث**. Other periods have **no target recorded**, not zero targets. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-matrix`, `.m-key` | All six lines are labelled **على المسار**, while all have been stationary for 29–35 days. | Replace the entire widget with **ستة بنود بلا حركة منذ 29–35 يومًا** beside the opportunity list. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-funnel` | Four records in one stage and one in another become a **75% loss**. These are current stage populations, not a tracked conversion cohort. | Delete the leakage claim and percentage. Preserve stage counts as counts. |
| HIGH | [reports.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/reports.html:33) | **3,360** “weighted expected” revenue has no supported probability model in the brief. “Six lines aged 30+ days” includes the 29-day line. | Remove the forecast. Show the actual **29–35-day range**; only five meet a 30-day threshold. |
| HIGH | [shell.js:11](/Users/abdulaziz/Projects/Massar/massar-ds/shell.js:11), Home decisions, Products summary | Navigation says six products; Home says five of six lack targets; reality is eight products, seven without targets. Products says one lacks published pricing, while six rows say otherwise. | Compute summaries from the same records as their tables. No separately maintained counts. |

The visual system then compounds those errors:

| Severity | Location | Before | After and why |
|---|---|---|---|
| MEDIUM | [massar.css:391](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:391), `.m-card`, `.m-grid--3` | Every secondary story gets a white surface, **24px padding**, **16px radius**, the same shadow and a **19px heading**. Equal treatment makes everything equally urgent. | Two substantial surfaces on Home: revenue and opportunities. Decisions and supporting evidence use plain rows. |
| MEDIUM | [massar.css:60](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:60), type tokens | Eight sizes, including **11px** and **12.5px**, push material qualifications into miniature grey text. | Five principal levels: **72, 28, 20, 15, 13px**. Target coverage must be readable body text. |
| MEDIUM | `.m-h1`, `.m-card__t`, `.m-lead__v` | Arabic titles inherit **−1px / −.3px tracking**; the monetary figure and currency share display treatment. | Arabic tracking **0**. Tighten Western display numerals only. Give Cairo room vertically. |
| MEDIUM | [massar.css:273](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:273) and [massar.css:540](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:540), `.m-chip` | The same component is defined twice: first **12.5px, 6px radius, 1px 7px padding**, later **11px, pill radius, 3px 9px**. | One definition: **13/22px**, pill, used only for actual statuses. The cascade should not make design decisions. |
| MEDIUM | `.m-chart`, `.m-arc`, `.m-heat`, `.m-fstep` | A **900×280** chart, **200px** gauge, **34px** heat cells and **30px** funnel bars illustrate mostly zeros and unsupported subdivisions. | Remove them from Home. Their area exceeds their information. |
| MEDIUM | `.m-col`, `.m-col--rail`, `.m-deal` | **252px columns**, **44px rotated empty rails**, cards inside columns inside a card. Six records require horizontal exploration. | One six-row table. Empty stages remain accessible in the pipeline workspace. |
| MEDIUM | `.m-side__logo`, `.m-insight`, `.m-fstep__b i`, `.m-meter i` | Blue–violet gradients assign decorative excitement to unrelated things. | One blue accent. Status colours carry meaning and readable labels. |
| MEDIUM | `.m-empty`, `.m-q__v.nil`, `.m-stat--mut` | Empty content is centred; zeros become faint. | Align to inline-start. **Booked zero stays black.** Absence is the principal finding. |
| MEDIUM | [products.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/products.html:33) | An implementation ZIP filename interrupts product management; another row literally says **hello**. | Remove both. Product copy describes the business record and its next action. |
| MEDIUM | [product.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/product.html:33) | Global product navigation sits above five record tabs; summary tiles give campaign mentions equal weight to open revenue. | Record page gets a breadcrumb and one record-level tab strip. Overview leads with this product’s revenue, scoped target and two opportunity lines. |
| MEDIUM | Motion rules and `shell.js` | **700ms** chart growth, **900ms** gauges, multiple easing curves, press scales **.98/.985**, and a dialog that closes immediately despite comments promising an exit. | Static charts; one curve; **180ms enter / 120ms exit / 100ms press**, **.97** press scale. Implement the dialog exit before calling `close()`. |

There is also interaction theatre: `.m-search` is a `div` advertising `⌘K`; several “فتح” buttons have no handler; `cursor:grab` suggests dragging that the supplied scripts do not implement. These controls should either work or disappear.

**2. The fixed Home**

Use the brief’s snapshot date: **16 September 2026**.

The page has three parts, in this reading order.

**A. Revenue and its limits**

A compact page header:

> **الأداء التجاري**  
> السنة المالية 2026 · حتى 16 سبتمبر

No breadcrumb saying “الرئيسية” directly above it. No five-way date switch. Historical ranges belong in Reports.

One full-width revenue surface, internally divided into a dominant right column and a quieter left column:

| Right: dominant | Left: supporting |
|---|---|
| الإيراد المحقق | المستهدف المسجّل |
| **0 ر.س** | **34,000 ر.س** |
| لا صفقات رابحة حتى 16 سبتمبر | الإجازات المرضية · الربع الثالث فقط |
| **● لا توجد إيرادات محققة حتى الآن** | **سبعة منتجات بلا مستهدف. لا يمكن تقييم تحقيق مستهدف الشركة.** |
| Primary action: **مراجعة العرض المسعّر** | Secondary link: **استكمال المستهدفات** |
|  | قيمة البنود المفتوحة المسعّرة: **4,200 ر.س** |
|  | بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير |

That is the five-second answer. No invented probability, no company attainment percentage, no red downward arrow pretending a target gap is a period-over-period delta.

The reference’s large number and pill remain. The pill communicates a supported status.

**B. The work that changes the number**

Below the hero, use an asymmetric two-column layout.

The larger **right-hand column** contains the six opportunity lines. Put the priced quotation first because it is the only known money currently available to pursue.

Heading:

> **فرص البيع المفتوحة**  
> ستة بنود بلا حركة منذ 29–35 يومًا · آخر حركة في 18 أغسطس

Columns, in RTL order:

| العميل / المنتج | المرحلة | القيمة | بلا حركة |
|---|---|---:|---:|
| DL000 / الإجازات المرضية | عرض السعر | 4,200 ر.س | 29 يومًا |
| العمدة / الإجازات المرضية | اكتشاف الحاجة | لم يُسعّر | 35 يومًا |
| ابرهيم / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |
| ابرهيم / سجل التطعيمات الوطني | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / خدمات التطعيمات | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |

Use one explicit record link per row. No repeated pill-shaped “فتح” buttons.

The smaller **left-hand column** is an unboxed action list titled **ما يعطّل البيع**:

1. **خمسة بنود بلا تسعير** — action: **استكمال التسعير**.
2. **16 حسابًا بلا مسؤول وبلا جهة اتصال مرتبطة** — action: **تعيين المسؤولين وربط جهات الاتصال**.
3. **جهتان مهتمتان دون فرصة من الحملة 38** — action: **مراجعة المهتمين**.

Each action opens the relevant filtered records. Do not send the founder to an unfiltered landing page.

Target incompleteness is already beside the target. Staleness is already beside the pipeline. Do not repeat either as another warning card.

**C. Supporting evidence**

One unboxed disclosure titled **تفاصيل المؤشرات**. Closed initially. Its summary reads:

> اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات

Inside, use four plain rows, not four cards:

- **Accounts:** 16 approved accounts; none has an owner or linked contact; seven have a sector and seven have a city. The 21 contacts are a separate entity count, not evidence of account linkage.
- **Campaign 38:** sent 21 → delivered 19 → seen 12 → replied 4 → interested 2 → opportunities 0. Render the sequence from right to left with labels and counts.
- **Activity totals:** 21 contacts, 359 messages, 1,233 events. Label these as recorded totals; do not imply they are today’s activity or revenue.
- **Knowledge:** eight weighted sections; objections, competitors and compliance are each 0%. Link to the named sections. Do not manufacture an overall readiness score from undocumented weights.

**This is the Home/indicators merger:** relevant indicators explain the revenue and actions; the rest remain available in one subordinate disclosure. Remove “مؤشرات الاستخدام” as a separate navigation destination and redirect its existing route to this disclosure.

Keep all eight products and their supplied readiness values in Products. Retain both published annual prices, the four inferred-sector labels, all three sectors plus “بلا قطاع”, and the explicit “لا يبيعه المساعد” status for صحة أعمال Plus. These facts do not need eight widgets on Home.

**3. Pasteable CSS**

Paste this **after the existing stylesheet** while replacing Home’s body content with the structure above. It overrides shared foundations and supplies the new Home layout. CSS cannot repair the target calculation or remove the old sections; those changes are mandatory.

Use this structure:

```html
<main class="m-page m-home">
  <header class="m-home__head">
    <h1 class="m-h1">الأداء التجاري</h1>
    <p class="m-meta">
      السنة المالية <bdi class="m-n">2026</bdi>
      · حتى <bdi class="m-n">16</bdi> سبتمبر
    </p>
  </header>

  <section class="m-card m-card--revenue"
           aria-labelledby="revenue-title">
    <div class="m-revenue__main">
      <h2 class="m-label" id="revenue-title">الإيراد المحقق</h2>
      <p class="m-revenue__value">
        <bdi class="m-n">0</bdi><span>ر.س</span>
      </p>
      <p class="m-body">لا صفقات رابحة حتى 16 سبتمبر</p>
      <p class="m-status m-status--warn">
        لا توجد إيرادات محققة حتى الآن
      </p>
      <div class="m-actions">
        <a class="m-btn m-btn--primary" href="#priced-line">
          مراجعة العرض المسعّر
        </a>
      </div>
    </div>

    <div class="m-revenue__context">
      <dl class="m-facts">
        <div>
          <dt>المستهدف المسجّل</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">34,000</bdi> ر.س
          </dd>
          <dd>الإجازات المرضية · الربع الثالث فقط</dd>
        </div>
        <div>
          <dt>قيمة البنود المفتوحة المسعّرة</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">4,200</bdi> ر.س
          </dd>
          <dd>بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير</dd>
        </div>
      </dl>
      <p class="m-revenue__qualification">
        سبعة منتجات بلا مستهدف.
        لا يمكن تقييم تحقيق مستهدف الشركة.
      </p>
      <a class="m-link" href="perf.html">استكمال المستهدفات</a>
    </div>
  </section>

  <div class="m-home__work">
    <section class="m-card m-card--ledger"
             aria-labelledby="pipeline-title">
      <header class="m-section-head">
        <h2 class="m-h2" id="pipeline-title">فرص البيع المفتوحة</h2>
        <p class="m-meta">
          ستة بنود بلا حركة منذ <bdi class="m-n">29–35</bdi> يومًا
          · آخر حركة في <bdi class="m-n">18</bdi> أغسطس
        </p>
      </header>
      <!-- .m-tablewrap > table.m-table.m-ledger
           Use the six rows above.
           Give the priced row id="priced-line" and tabindex="-1". -->
    </section>

    <aside class="m-home__decisions" aria-labelledby="decisions-title">
      <h2 class="m-h2" id="decisions-title">ما يعطّل البيع</h2>
      <!-- Three .m-decision blocks:
           h3.m-decision__title, p.m-meta, a.m-link -->
    </aside>
  </div>

  <details class="m-evidence" id="indicators">
    <summary>
      <span class="m-h2">تفاصيل المؤشرات</span>
      <span class="m-meta">
        اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات
      </span>
    </summary>
    <!-- Four .m-evidence__row blocks with the exact facts above. -->
  </details>
</main>
```

```css
/* MASSAR — revised foundations and revenue-first Home */
:root {
  /* Near-white ground; blue reserved for action and selection. */
  --m-page: #F6F7F5;
  --m-paper: #FFFFFF;
  --m-sunk: #EEF1EE;
  --m-line: #E3E7E3;
  --m-line-2: #CDD4CE;
  --m-dot: #D9DFDA;

  --m-ink: #17201F;
  --m-ink-2: #46504D;
  --m-mut: #646D69;
  --m-faint: #646D69;

  --m-ac: #245BD6;
  --m-ac-deep: #1947AF;
  --m-ac-dim: #EEF3FF;
  --m-ac-line: #BCCDF7;

  --m-ok: #17603D;
  --m-ok-dim: #EDF6F0;
  --m-ok-line: #BEDBC8;
  --m-warn: #8A4B08;
  --m-warn-dim: #FFF4E5;
  --m-warn-line: #E8CFAB;
  --m-bad: #B42318;
  --m-bad-dim: #FEF0ED;
  --m-bad-line: #F1C5BE;
  --m-idle: #646D69;
  --m-idle-dim: #EEF1EE;
  --m-idle-line: #CDD4CE;

  /* Compatibility for retained views: no violet palette. */
  --m-vi: var(--m-ac);
  --m-vi-dim: var(--m-ac-dim);

  /* Five principal type levels. Supporting figures use 28px. */
  --m-t-micro: 13px;
  --m-t-cap: 13px;
  --m-t-body: 15px;
  --m-t-sub: 15px;
  --m-t-h: 20px;
  --m-t-fig: 28px;
  --m-t-display: 28px;
  --m-t-hero: 72px;

  --m-leading-meta: 22px;
  --m-leading-body: 26px;
  --m-leading-section: 32px;
  --m-leading-title: 44px;
  --m-leading-figure: 40px;
  --m-leading-hero: 80px;

  --m-tracking-text: 0;
  --m-tracking-figure: -0.02em;
  --m-tracking-hero: -0.035em;

  /* 4px rhythm; 24 between groups, 32 between major regions. */
  --m-1: 4px;
  --m-2: 8px;
  --m-3: 12px;
  --m-4: 16px;
  --m-5: 24px;
  --m-6: 32px;
  --m-7: 48px;

  --m-r-chip: 999px;
  --m-r-ctl: 10px;
  --m-r-card: 16px;
  --m-r-band: 20px;

  --m-hair: 0 0 0 1px var(--m-line);
  --m-low: 0 1px 2px rgb(0 0 0 / 3%);
  --m-soft: 0 2px 8px rgb(0 0 0 / 3%);
  --m-lift: 0 8px 24px rgb(0 0 0 / 10%);
  --m-focus: 0 0 0 3px var(--m-ac-line);

  --m-ease: cubic-bezier(.16, 1, .3, 1);
  --m-move: var(--m-ease);
  --m-press: 100ms;
  --m-swap: 120ms;
  --m-in: 180ms;
  --m-out: 120ms;
}

body {
  font-family: Cairo, system-ui, sans-serif;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
  color: var(--m-ink-2);
  background: var(--m-page);
  direction: rtl;
  font-variant-numeric: lining-nums tabular-nums;
}

.m-n {
  display: inline-block;
  direction: ltr;
  unicode-bidi: isolate;
  font-variant-numeric: lining-nums tabular-nums;
  font-feature-settings: "lnum" 1, "tnum" 1;
}

.m-h1,
.m-greet__t {
  margin-block: 0;
  font-size: var(--m-t-display);
  line-height: var(--m-leading-title);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-h2,
.m-card__t {
  margin-block: 0;
  font-size: var(--m-t-h);
  line-height: var(--m-leading-section);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-body,
.m-label {
  margin-block: 0;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
}

.m-label { font-weight: 600; }

.m-meta,
.m-cap,
.m-stat__s,
.m-item__s,
.m-q__s,
.m-hint {
  margin-block: 0;
  font-size: var(--m-t-cap);
  line-height: var(--m-leading-meta);
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-stat__v,
.m-q__v {
  font-size: var(--m-t-fig);
  line-height: var(--m-leading-figure);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-stat__v .m-n,
.m-q__v .m-n {
  letter-spacing: var(--m-tracking-figure);
}

/* A known zero is ordinary data, not disabled content. */
.m-q__v.nil,
.m-stat--mut .m-stat__v {
  color: var(--m-ink);
}

/* Shared shell. */
.m-shell { min-block-size: 100dvh; }

.m-side {
  inline-size: 224px;
  block-size: 100dvh;
  border-inline-start: 0;
  border-inline-end: 1px solid var(--m-line);
  transition-duration: var(--m-in);
}

.m-side[data-collapsed] {
  inline-size: 68px;
  transition-duration: var(--m-out);
}

.m-side__logo { background: var(--m-ac); }

.m-side__grp { letter-spacing: 0; }

.m-nav {
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  border-radius: var(--m-r-ctl);
}

.m-side__w,
.m-nav span {
  transition: opacity var(--m-in) var(--m-ease);
  transform: none;
}

.m-side[data-collapsed] .m-side__w,
.m-side[data-collapsed] .m-nav span {
  transform: none;
  transition: opacity var(--m-out) var(--m-ease);
}

/* Use accessible link names; remove the clipped pseudo-flyout. */
.m-nav::after { content: none; }

.m-page {
  inline-size: 100%;
  max-inline-size: 1264px;
  margin-inline: auto;
  padding-inline: var(--m-6);
  padding-block: var(--m-6) var(--m-7);
}

.m-bar {
  position: static;
  padding-inline: var(--m-6);
  padding-block: var(--m-3);
  background: transparent;
  border-block-end: 0;
}

/* Home has its own useful header; delete its old toolbar markup. */
body[data-nav="home"] .m-bar { display: none; }

/* Shared surfaces: quiet structure, no hover elevation. */
.m-card {
  min-inline-size: 0;
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  background: var(--m-paper);
  border: 1px solid var(--m-line);
  border-radius: var(--m-r-card);
  box-shadow: none;
}

.m-card--pad0,
.m-card--ledger {
  padding-inline: 0;
  padding-block: 0;
}

.m-card--revenue {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: var(--m-6);
  padding-inline: var(--m-6);
  padding-block: var(--m-6);
  border-radius: var(--m-r-band);
  box-shadow: var(--m-soft);
}

/* Home composition. DOM order is also the mobile reading order. */
.m-home {
  display: grid;
  gap: var(--m-6);
}

.m-home__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--m-2) var(--m-5);
}

.m-revenue__main { min-inline-size: 0; }

.m-revenue__value {
  display: flex;
  align-items: baseline;
  gap: var(--m-3);
  margin-block: var(--m-2);
  color: var(--m-ink);
}

.m-revenue__value > .m-n {
  font-size: var(--m-t-hero);
  line-height: var(--m-leading-hero);
  font-weight: 700;
  letter-spacing: var(--m-tracking-hero);
}

.m-revenue__value > :not(.m-n) {
  font-size: 20px;
  line-height: 32px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-revenue__context {
  min-inline-size: 0;
  padding-inline-start: var(--m-6);
  border-inline-start: 1px solid var(--m-line);
}

.m-facts {
  display: grid;
  gap: var(--m-5);
  margin-block: 0;
}

.m-facts dt {
  font-size: 13px;
  line-height: 22px;
  color: var(--m-mut);
}

.m-facts dd {
  margin-inline: 0;
  margin-block: var(--m-1) 0;
  font-size: 13px;
  line-height: 22px;
}

.m-facts .m-facts__value {
  font-size: 20px;
  line-height: 32px;
  font-weight: 600;
  color: var(--m-ink);
}

.m-revenue__qualification {
  margin-block: var(--m-5) var(--m-2);
  font-size: 15px;
  line-height: 26px;
  color: var(--m-ink);
}

.m-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--m-2);
  margin-block-start: var(--m-5);
}

.m-home__work {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: var(--m-6);
  align-items: start;
}

.m-section-head {
  display: grid;
  gap: var(--m-1);
  padding-inline: var(--m-5);
  padding-block: var(--m-5) var(--m-4);
}

.m-home__decisions {
  min-inline-size: 0;
  padding-block-start: var(--m-2);
}

.m-decision {
  display: grid;
  gap: var(--m-2);
  padding-block: var(--m-4);
  border-block-end: 1px solid var(--m-line);
}

.m-decision:last-child { border-block-end: 0; }

.m-decision__title {
  margin-block: 0;
  font-size: 15px;
  line-height: 26px;
  font-weight: 600;
  color: var(--m-ink);
}

/* One readable table, including when records are sparse. */
.m-tablewrap {
  overflow: auto;
  border-radius: 0 0 var(--m-r-card) var(--m-r-card);
}

.m-table th {
  block-size: 44px;
  padding-inline: var(--m-4);
  padding-block: var(--m-2);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  text-align: start;
  color: var(--m-mut);
  background: var(--m-paper);
}

.m-table td {
  padding-inline: var(--m-4);
  padding-block: 10px;
  font-size: 15px;
  line-height: 24px;
  font-weight: 400;
  color: var(--m-ink-2);
}

.m-ledger { min-inline-size: 560px; }

.m-ledger .m-item__s {
  margin-block-start: 2px;
  font-size: 13px;
  line-height: 20px;
}

.m-table td.m-td-v,
.m-table th.num {
  text-align: end;
  color: var(--m-ink);
}

.m-table td.m-td-n {
  font-weight: 600;
  color: var(--m-ink);
}

.m-ledger__unpriced {
  color: var(--m-warn);
  font-size: 13px;
  line-height: 22px;
  white-space: nowrap;
}

#priced-line { scroll-margin-block-start: var(--m-5); }

#priced-line:target { background: var(--m-ac-dim); }

/* Status: readable words plus a dot; never colour alone. */
.m-chip,
.m-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-inline: 10px;
  padding-block: 3px;
  min-block-size: 28px;
  border-radius: var(--m-r-chip);
  background: var(--m-idle-dim);
  color: var(--m-idle);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  letter-spacing: 0;
  white-space: normal;
}

.m-status { margin-block: var(--m-4) 0; }

.m-chip::before,
.m-status::before {
  content: "";
  inline-size: 6px;
  block-size: 6px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: currentColor;
}

.m-status--warn,
.m-chip--warn {
  background: var(--m-warn-dim);
  color: var(--m-warn);
}

.m-chip--bad {
  background: var(--m-bad-dim);
  color: var(--m-bad);
}

.m-chip--ok {
  background: var(--m-ok-dim);
  color: var(--m-ok);
}

.m-chip--ac {
  background: var(--m-ac-dim);
  color: var(--m-ac-deep);
}

/* Controls: one geometry, real hit areas. */
.m-btn {
  min-block-size: 44px;
  justify-content: center;
  padding-inline: var(--m-4);
  padding-block: 9px;
  border: 1px solid var(--m-line-2);
  border-radius: var(--m-r-chip);
  box-shadow: none;
  font-size: 14px;
  line-height: 24px;
  text-decoration: none;
  transition:
    background-color var(--m-out) var(--m-ease),
    transform var(--m-press) var(--m-ease);
}

.m-btn--primary {
  border-color: var(--m-ac);
  background: var(--m-ac);
  color: #FFFFFF;
  box-shadow: none;
}

.m-btn--quiet {
  border-color: transparent;
  background: transparent;
  color: var(--m-ac-deep);
}

.m-btn--icon {
  inline-size: 44px;
  block-size: 44px;
}

.m-link {
  display: inline-flex;
  align-items: center;
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  color: var(--m-ac-deep);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.m-input,
.m-select {
  min-block-size: 44px;
  font-size: 15px;
  line-height: 24px;
  transition: box-shadow var(--m-out) var(--m-ease);
}

/* Restore native select indicator; delete physical background-position. */
.m-select {
  appearance: auto;
  background-image: none;
  padding-inline: var(--m-3);
}

:where(a, button, input, select, textarea, summary):focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

/* Specificity overrides old focus rules. */
.m-btn:focus-visible,
.m-nav:focus-visible,
.m-tab:focus-visible,
.m-input:focus-visible,
.m-select:focus-visible,
.m-range input:focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

.m-btn:not(:disabled):active,
.m-nav:active,
.m-side__t:active,
.m-seg button:active,
.m-x:active {
  transform: scale(.97);
}

.m-btn:disabled:active { transform: none; }

@media (hover: hover) and (pointer: fine) {
  .m-btn:not(:disabled):hover { background: var(--m-page); }
  .m-btn--primary:not(:disabled):hover {
    background: var(--m-ac-deep);
  }
  .m-table tbody tr:hover { background: #F8FAF8; }
  .m-link:hover { color: var(--m-ac); }
}

/* Supporting evidence is a document section, not another dashboard. */
.m-evidence {
  border-block-start: 1px solid var(--m-line-2);
}

.m-evidence > summary {
  padding-block: var(--m-4);
  cursor: pointer;
  min-block-size: 44px;
}

.m-evidence > summary .m-meta {
  display: block;
  margin-block-start: var(--m-1);
}

.m-evidence__row {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: var(--m-4);
  padding-block: var(--m-4);
  border-block-start: 1px solid var(--m-line);
}

.m-evidence__row > * { margin-block: 0; }

/* A genuine empty record list: ordinary editorial content. */
.m-empty {
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  text-align: start;
}

.m-empty__t {
  font-size: 15px;
  line-height: 26px;
}

.m-empty__d {
  max-inline-size: 60ch;
  margin-inline: 0;
  font-size: 13px;
  line-height: 22px;
}

/* No drawing animations or blurred text swaps. */
.m-chart__grow,
.m-arc__fill,
.m-fstep__b i {
  animation: none;
}

.m-fstep__b i,
.m-meter i {
  background: var(--m-ac);
}

.m-view__p,
.m-view__p[data-enter] {
  opacity: 1;
  transform: none;
  filter: none;
  transition: none;
}

.m-input,
.m-select,
.m-tip2,
.m-table tbody tr,
.m-th-sort svg,
.m-cb {
  transition-timing-function: var(--m-ease);
}

.m-dlg__p {
  animation: m-dialog-enter var(--m-in) var(--m-ease);
}

dialog.m-dlg::backdrop {
  animation: m-fade var(--m-in) var(--m-ease);
}

dialog.m-dlg[data-closing] .m-dlg__p {
  animation: m-dialog-exit var(--m-out) var(--m-ease) both;
}

dialog.m-dlg[data-closing]::backdrop {
  animation: m-fade var(--m-out) var(--m-ease) reverse both;
}

@keyframes m-dialog-enter {
  from { opacity: 0; transform: scale(.97); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes m-dialog-exit {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(.97); }
}

@media (max-width: 1200px) {
  .m-home__work { grid-template-columns: minmax(0, 1fr); }
}

/* Reachable mobile navigation without the existing unopened drawer. */
@media (max-width: 900px) {
  .m-shell { display: block; }

  .m-side,
  .m-side[data-collapsed] {
    position: static;
    inline-size: 100%;
    block-size: auto;
    transform: none;
    overflow: visible;
    border-inline-end: 0;
    border-block-end: 1px solid var(--m-line);
    transition: none;
  }

  .m-side__b,
  .m-side__f { display: none; }

  .m-side__nav {
    display: flex;
    overflow: auto;
    padding-inline: var(--m-4);
    padding-block: var(--m-2);
  }

  .m-nav { flex: 0 0 auto; }

  .m-side[data-collapsed] .m-nav span,
  .m-side[data-collapsed] .m-nav b {
    opacity: 1;
    transform: none;
  }

  .m-page,
  .m-bar { padding-inline: var(--m-4); }
}

@media (max-width: 700px) {
  :root {
    --m-t-hero: 56px;
    --m-leading-hero: 64px;
  }

  .m-home { gap: var(--m-5); }

  .m-card--revenue {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-5);
    padding-inline: var(--m-5);
    padding-block: var(--m-5);
  }

  .m-revenue__context {
    padding-inline-start: 0;
    padding-block-start: var(--m-5);
    border-inline-start: 0;
    border-block-start: 1px solid var(--m-line);
  }

  .m-evidence__row {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-2);
  }

  .m-input,
  .m-select { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }

  .m-btn:active,
  .m-nav:active,
  .m-side__t:active,
  .m-seg button:active,
  .m-x:active {
    transform: none;
  }
}
```

For dialog dismissal, `shell.js` must apply `data-closing`, wait for the panel’s exit, then call `close()`. Route the close button, Escape and backdrop through that function. Reduced motion closes immediately. CSS alone cannot delay the existing `close()` calls.

Western numerals also require formatting at the data boundary; `.m-n` does not convert digits:

```js
const formatNumber = new Intl.NumberFormat("ar-SA-u-nu-latn");
```

Counted nouns need authored plural forms. Use **لا بنود، بند واحد، بندان، ثلاثة بنود، 11 بندًا** according to the count and grammatical context. Do not construct Arabic prose with `${n} + noun`.

**4. The near-empty state is the design**

Keep these distinctions explicit:

| Data condition | Display |
|---|---|
| Known booked revenue is zero | **0 ر.س**, full-strength ink |
| An opportunity exists without pricing | **لم يُسعّر** |
| A target has not been configured | **لم يُحدّد** |
| No opportunity lines exist | **لا بنود مفتوحة** |
| A future period has not happened | **لم يبدأ بعد** |
| A value cannot be calculated from available evidence | **غير متاح** plus the specific reason |

Never substitute `—` for all six meanings.

Home remains visually complete with zero revenue because its composition depends on **a number, an explanation and real records**. It does not depend on a chart becoming interesting.

If the opportunity list reaches zero records, retain its heading and replace the rows with:

> **لا توجد فرص بيع مفتوحة**  
> لم تتحول أي جهة مهتمة من الحملة 38 إلى فرصة.  
> **مراجعة المهتمين**

Show that campaign sentence only while that condition remains true. No illustration, dashed drop zone, onboarding confetti or artificially tall blank panel.

Do not render the reference’s gradient bars now. There is no supported monthly target series to plot. When actual booked revenue exists, a compact historical chart can use blue gradient bars with matching cap dots, January at the right, and clearly distinct future periods. The current zero does not need twelve decorative columns.

**5. Explicit delete list**

Delete from **Home**:

- `#vChart`, `#vList`, their chart/list switch and `#quarters`.
- `MONTHLY`, prorated target arithmetic and the fabricated monthly target series.
- The five date presets and custom range controls.
- The readiness arc, account dot matrix, pipeline-health matrix and heat strip.
- Both funnels and every inferred stage-loss percentage.
- The entire embedded Kanban board, including rotated empty-stage rails.
- The standalone four-item decision card; replace it with the three contextual action rows.
- The separate indicators destination.
- The old toolbar, fake search shortcut and duplicate “الرئيسية” breadcrumb.

Delete or replace across **the system**:

- `.m-insight` and its decorative gradient, nested cards and carousel dots.
- Duplicate `.m-chip`, `.m-search`, `.m-crumb` and `.m-form` definitions.
- Negative tracking on Arabic text.
- `700ms`/`900ms` chart animations, text blur swaps and the second easing curve.
- Grab cursors and focusable cards without implemented actions.
- Physical direction declarations such as `background-position:left` and asymmetric physical padding.
- Hard-coded navigation counts.
- “hello”, ZIP filenames and skill-installation copy in product workflows.
- The unsupported weighted forecast and unsupported response-time statistic in Reports.
- The “توزيع بالتساوي” shortcut that silently suggests changing a deliberately Q3-scoped target.
- Repeated product campaign buttons and the second navigation strip on a product record.

Keep Reports for dated analysis and export. Keep the pipeline workspace for stage management. Keep Products for product readiness and configuration. Home owns the executive answer.

**Current design verdict: Block.** The source and proposed text-colour contrast were checked; the proposed layout has not been browser-rendered. No files were modified.
tokens used
84,667
**Massar should feel like a founder’s revenue ledger: one unmistakable number, an honest statement of what it means, and the work that can change it.**

The current page spends its attention budget drawing the database. It needs to spend that budget interpreting it.

**1. The diagnosis**

The most serious problems are factual. Visual polish currently makes them more convincing.

| Severity | Location | Before | Required change |
|---|---|---|---|
| HIGH | [home.html:97](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:97), `MONTHLY`, `sum()`, `paintQuarters()` | `TARGET / 12` distributes a **Q3-only, single-product target** across the year. Initial rendering changes the displayed requirement to **24,178**, and quarters receive **8,500** each. | Delete this allocation. Show **34,000 ر.س · الإجازات المرضية · الربع الثالث**. Other periods have **no target recorded**, not zero targets. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-matrix`, `.m-key` | All six lines are labelled **على المسار**, while all have been stationary for 29–35 days. | Replace the entire widget with **ستة بنود بلا حركة منذ 29–35 يومًا** beside the opportunity list. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-funnel` | Four records in one stage and one in another become a **75% loss**. These are current stage populations, not a tracked conversion cohort. | Delete the leakage claim and percentage. Preserve stage counts as counts. |
| HIGH | [reports.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/reports.html:33) | **3,360** “weighted expected” revenue has no supported probability model in the brief. “Six lines aged 30+ days” includes the 29-day line. | Remove the forecast. Show the actual **29–35-day range**; only five meet a 30-day threshold. |
| HIGH | [shell.js:11](/Users/abdulaziz/Projects/Massar/massar-ds/shell.js:11), Home decisions, Products summary | Navigation says six products; Home says five of six lack targets; reality is eight products, seven without targets. Products says one lacks published pricing, while six rows say otherwise. | Compute summaries from the same records as their tables. No separately maintained counts. |

The visual system then compounds those errors:

| Severity | Location | Before | After and why |
|---|---|---|---|
| MEDIUM | [massar.css:391](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:391), `.m-card`, `.m-grid--3` | Every secondary story gets a white surface, **24px padding**, **16px radius**, the same shadow and a **19px heading**. Equal treatment makes everything equally urgent. | Two substantial surfaces on Home: revenue and opportunities. Decisions and supporting evidence use plain rows. |
| MEDIUM | [massar.css:60](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:60), type tokens | Eight sizes, including **11px** and **12.5px**, push material qualifications into miniature grey text. | Five principal levels: **72, 28, 20, 15, 13px**. Target coverage must be readable body text. |
| MEDIUM | `.m-h1`, `.m-card__t`, `.m-lead__v` | Arabic titles inherit **−1px / −.3px tracking**; the monetary figure and currency share display treatment. | Arabic tracking **0**. Tighten Western display numerals only. Give Cairo room vertically. |
| MEDIUM | [massar.css:273](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:273) and [massar.css:540](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:540), `.m-chip` | The same component is defined twice: first **12.5px, 6px radius, 1px 7px padding**, later **11px, pill radius, 3px 9px**. | One definition: **13/22px**, pill, used only for actual statuses. The cascade should not make design decisions. |
| MEDIUM | `.m-chart`, `.m-arc`, `.m-heat`, `.m-fstep` | A **900×280** chart, **200px** gauge, **34px** heat cells and **30px** funnel bars illustrate mostly zeros and unsupported subdivisions. | Remove them from Home. Their area exceeds their information. |
| MEDIUM | `.m-col`, `.m-col--rail`, `.m-deal` | **252px columns**, **44px rotated empty rails**, cards inside columns inside a card. Six records require horizontal exploration. | One six-row table. Empty stages remain accessible in the pipeline workspace. |
| MEDIUM | `.m-side__logo`, `.m-insight`, `.m-fstep__b i`, `.m-meter i` | Blue–violet gradients assign decorative excitement to unrelated things. | One blue accent. Status colours carry meaning and readable labels. |
| MEDIUM | `.m-empty`, `.m-q__v.nil`, `.m-stat--mut` | Empty content is centred; zeros become faint. | Align to inline-start. **Booked zero stays black.** Absence is the principal finding. |
| MEDIUM | [products.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/products.html:33) | An implementation ZIP filename interrupts product management; another row literally says **hello**. | Remove both. Product copy describes the business record and its next action. |
| MEDIUM | [product.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/product.html:33) | Global product navigation sits above five record tabs; summary tiles give campaign mentions equal weight to open revenue. | Record page gets a breadcrumb and one record-level tab strip. Overview leads with this product’s revenue, scoped target and two opportunity lines. |
| MEDIUM | Motion rules and `shell.js` | **700ms** chart growth, **900ms** gauges, multiple easing curves, press scales **.98/.985**, and a dialog that closes immediately despite comments promising an exit. | Static charts; one curve; **180ms enter / 120ms exit / 100ms press**, **.97** press scale. Implement the dialog exit before calling `close()`. |

There is also interaction theatre: `.m-search` is a `div` advertising `⌘K`; several “فتح” buttons have no handler; `cursor:grab` suggests dragging that the supplied scripts do not implement. These controls should either work or disappear.

**2. The fixed Home**

Use the brief’s snapshot date: **16 September 2026**.

The page has three parts, in this reading order.

**A. Revenue and its limits**

A compact page header:

> **الأداء التجاري**  
> السنة المالية 2026 · حتى 16 سبتمبر

No breadcrumb saying “الرئيسية” directly above it. No five-way date switch. Historical ranges belong in Reports.

One full-width revenue surface, internally divided into a dominant right column and a quieter left column:

| Right: dominant | Left: supporting |
|---|---|
| الإيراد المحقق | المستهدف المسجّل |
| **0 ر.س** | **34,000 ر.س** |
| لا صفقات رابحة حتى 16 سبتمبر | الإجازات المرضية · الربع الثالث فقط |
| **● لا توجد إيرادات محققة حتى الآن** | **سبعة منتجات بلا مستهدف. لا يمكن تقييم تحقيق مستهدف الشركة.** |
| Primary action: **مراجعة العرض المسعّر** | Secondary link: **استكمال المستهدفات** |
|  | قيمة البنود المفتوحة المسعّرة: **4,200 ر.س** |
|  | بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير |

That is the five-second answer. No invented probability, no company attainment percentage, no red downward arrow pretending a target gap is a period-over-period delta.

The reference’s large number and pill remain. The pill communicates a supported status.

**B. The work that changes the number**

Below the hero, use an asymmetric two-column layout.

The larger **right-hand column** contains the six opportunity lines. Put the priced quotation first because it is the only known money currently available to pursue.

Heading:

> **فرص البيع المفتوحة**  
> ستة بنود بلا حركة منذ 29–35 يومًا · آخر حركة في 18 أغسطس

Columns, in RTL order:

| العميل / المنتج | المرحلة | القيمة | بلا حركة |
|---|---|---:|---:|
| DL000 / الإجازات المرضية | عرض السعر | 4,200 ر.س | 29 يومًا |
| العمدة / الإجازات المرضية | اكتشاف الحاجة | لم يُسعّر | 35 يومًا |
| ابرهيم / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |
| ابرهيم / سجل التطعيمات الوطني | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / خدمات التطعيمات | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |

Use one explicit record link per row. No repeated pill-shaped “فتح” buttons.

The smaller **left-hand column** is an unboxed action list titled **ما يعطّل البيع**:

1. **خمسة بنود بلا تسعير** — action: **استكمال التسعير**.
2. **16 حسابًا بلا مسؤول وبلا جهة اتصال مرتبطة** — action: **تعيين المسؤولين وربط جهات الاتصال**.
3. **جهتان مهتمتان دون فرصة من الحملة 38** — action: **مراجعة المهتمين**.

Each action opens the relevant filtered records. Do not send the founder to an unfiltered landing page.

Target incompleteness is already beside the target. Staleness is already beside the pipeline. Do not repeat either as another warning card.

**C. Supporting evidence**

One unboxed disclosure titled **تفاصيل المؤشرات**. Closed initially. Its summary reads:

> اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات

Inside, use four plain rows, not four cards:

- **Accounts:** 16 approved accounts; none has an owner or linked contact; seven have a sector and seven have a city. The 21 contacts are a separate entity count, not evidence of account linkage.
- **Campaign 38:** sent 21 → delivered 19 → seen 12 → replied 4 → interested 2 → opportunities 0. Render the sequence from right to left with labels and counts.
- **Activity totals:** 21 contacts, 359 messages, 1,233 events. Label these as recorded totals; do not imply they are today’s activity or revenue.
- **Knowledge:** eight weighted sections; objections, competitors and compliance are each 0%. Link to the named sections. Do not manufacture an overall readiness score from undocumented weights.

**This is the Home/indicators merger:** relevant indicators explain the revenue and actions; the rest remain available in one subordinate disclosure. Remove “مؤشرات الاستخدام” as a separate navigation destination and redirect its existing route to this disclosure.

Keep all eight products and their supplied readiness values in Products. Retain both published annual prices, the four inferred-sector labels, all three sectors plus “بلا قطاع”, and the explicit “لا يبيعه المساعد” status for صحة أعمال Plus. These facts do not need eight widgets on Home.

**3. Pasteable CSS**

Paste this **after the existing stylesheet** while replacing Home’s body content with the structure above. It overrides shared foundations and supplies the new Home layout. CSS cannot repair the target calculation or remove the old sections; those changes are mandatory.

Use this structure:

```html
<main class="m-page m-home">
  <header class="m-home__head">
    <h1 class="m-h1">الأداء التجاري</h1>
    <p class="m-meta">
      السنة المالية <bdi class="m-n">2026</bdi>
      · حتى <bdi class="m-n">16</bdi> سبتمبر
    </p>
  </header>

  <section class="m-card m-card--revenue"
           aria-labelledby="revenue-title">
    <div class="m-revenue__main">
      <h2 class="m-label" id="revenue-title">الإيراد المحقق</h2>
      <p class="m-revenue__value">
        <bdi class="m-n">0</bdi><span>ر.س</span>
      </p>
      <p class="m-body">لا صفقات رابحة حتى 16 سبتمبر</p>
      <p class="m-status m-status--warn">
        لا توجد إيرادات محققة حتى الآن
      </p>
      <div class="m-actions">
        <a class="m-btn m-btn--primary" href="#priced-line">
          مراجعة العرض المسعّر
        </a>
      </div>
    </div>

    <div class="m-revenue__context">
      <dl class="m-facts">
        <div>
          <dt>المستهدف المسجّل</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">34,000</bdi> ر.س
          </dd>
          <dd>الإجازات المرضية · الربع الثالث فقط</dd>
        </div>
        <div>
          <dt>قيمة البنود المفتوحة المسعّرة</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">4,200</bdi> ر.س
          </dd>
          <dd>بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير</dd>
        </div>
      </dl>
      <p class="m-revenue__qualification">
        سبعة منتجات بلا مستهدف.
        لا يمكن تقييم تحقيق مستهدف الشركة.
      </p>
      <a class="m-link" href="perf.html">استكمال المستهدفات</a>
    </div>
  </section>

  <div class="m-home__work">
    <section class="m-card m-card--ledger"
             aria-labelledby="pipeline-title">
      <header class="m-section-head">
        <h2 class="m-h2" id="pipeline-title">فرص البيع المفتوحة</h2>
        <p class="m-meta">
          ستة بنود بلا حركة منذ <bdi class="m-n">29–35</bdi> يومًا
          · آخر حركة في <bdi class="m-n">18</bdi> أغسطس
        </p>
      </header>
      <!-- .m-tablewrap > table.m-table.m-ledger
           Use the six rows above.
           Give the priced row id="priced-line" and tabindex="-1". -->
    </section>

    <aside class="m-home__decisions" aria-labelledby="decisions-title">
      <h2 class="m-h2" id="decisions-title">ما يعطّل البيع</h2>
      <!-- Three .m-decision blocks:
           h3.m-decision__title, p.m-meta, a.m-link -->
    </aside>
  </div>

  <details class="m-evidence" id="indicators">
    <summary>
      <span class="m-h2">تفاصيل المؤشرات</span>
      <span class="m-meta">
        اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات
      </span>
    </summary>
    <!-- Four .m-evidence__row blocks with the exact facts above. -->
  </details>
</main>
```

```css
/* MASSAR — revised foundations and revenue-first Home */
:root {
  /* Near-white ground; blue reserved for action and selection. */
  --m-page: #F6F7F5;
  --m-paper: #FFFFFF;
  --m-sunk: #EEF1EE;
  --m-line: #E3E7E3;
  --m-line-2: #CDD4CE;
  --m-dot: #D9DFDA;

  --m-ink: #17201F;
  --m-ink-2: #46504D;
  --m-mut: #646D69;
  --m-faint: #646D69;

  --m-ac: #245BD6;
  --m-ac-deep: #1947AF;
  --m-ac-dim: #EEF3FF;
  --m-ac-line: #BCCDF7;

  --m-ok: #17603D;
  --m-ok-dim: #EDF6F0;
  --m-ok-line: #BEDBC8;
  --m-warn: #8A4B08;
  --m-warn-dim: #FFF4E5;
  --m-warn-line: #E8CFAB;
  --m-bad: #B42318;
  --m-bad-dim: #FEF0ED;
  --m-bad-line: #F1C5BE;
  --m-idle: #646D69;
  --m-idle-dim: #EEF1EE;
  --m-idle-line: #CDD4CE;

  /* Compatibility for retained views: no violet palette. */
  --m-vi: var(--m-ac);
  --m-vi-dim: var(--m-ac-dim);

  /* Five principal type levels. Supporting figures use 28px. */
  --m-t-micro: 13px;
  --m-t-cap: 13px;
  --m-t-body: 15px;
  --m-t-sub: 15px;
  --m-t-h: 20px;
  --m-t-fig: 28px;
  --m-t-display: 28px;
  --m-t-hero: 72px;

  --m-leading-meta: 22px;
  --m-leading-body: 26px;
  --m-leading-section: 32px;
  --m-leading-title: 44px;
  --m-leading-figure: 40px;
  --m-leading-hero: 80px;

  --m-tracking-text: 0;
  --m-tracking-figure: -0.02em;
  --m-tracking-hero: -0.035em;

  /* 4px rhythm; 24 between groups, 32 between major regions. */
  --m-1: 4px;
  --m-2: 8px;
  --m-3: 12px;
  --m-4: 16px;
  --m-5: 24px;
  --m-6: 32px;
  --m-7: 48px;

  --m-r-chip: 999px;
  --m-r-ctl: 10px;
  --m-r-card: 16px;
  --m-r-band: 20px;

  --m-hair: 0 0 0 1px var(--m-line);
  --m-low: 0 1px 2px rgb(0 0 0 / 3%);
  --m-soft: 0 2px 8px rgb(0 0 0 / 3%);
  --m-lift: 0 8px 24px rgb(0 0 0 / 10%);
  --m-focus: 0 0 0 3px var(--m-ac-line);

  --m-ease: cubic-bezier(.16, 1, .3, 1);
  --m-move: var(--m-ease);
  --m-press: 100ms;
  --m-swap: 120ms;
  --m-in: 180ms;
  --m-out: 120ms;
}

body {
  font-family: Cairo, system-ui, sans-serif;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
  color: var(--m-ink-2);
  background: var(--m-page);
  direction: rtl;
  font-variant-numeric: lining-nums tabular-nums;
}

.m-n {
  display: inline-block;
  direction: ltr;
  unicode-bidi: isolate;
  font-variant-numeric: lining-nums tabular-nums;
  font-feature-settings: "lnum" 1, "tnum" 1;
}

.m-h1,
.m-greet__t {
  margin-block: 0;
  font-size: var(--m-t-display);
  line-height: var(--m-leading-title);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-h2,
.m-card__t {
  margin-block: 0;
  font-size: var(--m-t-h);
  line-height: var(--m-leading-section);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-body,
.m-label {
  margin-block: 0;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
}

.m-label { font-weight: 600; }

.m-meta,
.m-cap,
.m-stat__s,
.m-item__s,
.m-q__s,
.m-hint {
  margin-block: 0;
  font-size: var(--m-t-cap);
  line-height: var(--m-leading-meta);
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-stat__v,
.m-q__v {
  font-size: var(--m-t-fig);
  line-height: var(--m-leading-figure);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-stat__v .m-n,
.m-q__v .m-n {
  letter-spacing: var(--m-tracking-figure);
}

/* A known zero is ordinary data, not disabled content. */
.m-q__v.nil,
.m-stat--mut .m-stat__v {
  color: var(--m-ink);
}

/* Shared shell. */
.m-shell { min-block-size: 100dvh; }

.m-side {
  inline-size: 224px;
  block-size: 100dvh;
  border-inline-start: 0;
  border-inline-end: 1px solid var(--m-line);
  transition-duration: var(--m-in);
}

.m-side[data-collapsed] {
  inline-size: 68px;
  transition-duration: var(--m-out);
}

.m-side__logo { background: var(--m-ac); }

.m-side__grp { letter-spacing: 0; }

.m-nav {
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  border-radius: var(--m-r-ctl);
}

.m-side__w,
.m-nav span {
  transition: opacity var(--m-in) var(--m-ease);
  transform: none;
}

.m-side[data-collapsed] .m-side__w,
.m-side[data-collapsed] .m-nav span {
  transform: none;
  transition: opacity var(--m-out) var(--m-ease);
}

/* Use accessible link names; remove the clipped pseudo-flyout. */
.m-nav::after { content: none; }

.m-page {
  inline-size: 100%;
  max-inline-size: 1264px;
  margin-inline: auto;
  padding-inline: var(--m-6);
  padding-block: var(--m-6) var(--m-7);
}

.m-bar {
  position: static;
  padding-inline: var(--m-6);
  padding-block: var(--m-3);
  background: transparent;
  border-block-end: 0;
}

/* Home has its own useful header; delete its old toolbar markup. */
body[data-nav="home"] .m-bar { display: none; }

/* Shared surfaces: quiet structure, no hover elevation. */
.m-card {
  min-inline-size: 0;
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  background: var(--m-paper);
  border: 1px solid var(--m-line);
  border-radius: var(--m-r-card);
  box-shadow: none;
}

.m-card--pad0,
.m-card--ledger {
  padding-inline: 0;
  padding-block: 0;
}

.m-card--revenue {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: var(--m-6);
  padding-inline: var(--m-6);
  padding-block: var(--m-6);
  border-radius: var(--m-r-band);
  box-shadow: var(--m-soft);
}

/* Home composition. DOM order is also the mobile reading order. */
.m-home {
  display: grid;
  gap: var(--m-6);
}

.m-home__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--m-2) var(--m-5);
}

.m-revenue__main { min-inline-size: 0; }

.m-revenue__value {
  display: flex;
  align-items: baseline;
  gap: var(--m-3);
  margin-block: var(--m-2);
  color: var(--m-ink);
}

.m-revenue__value > .m-n {
  font-size: var(--m-t-hero);
  line-height: var(--m-leading-hero);
  font-weight: 700;
  letter-spacing: var(--m-tracking-hero);
}

.m-revenue__value > :not(.m-n) {
  font-size: 20px;
  line-height: 32px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-revenue__context {
  min-inline-size: 0;
  padding-inline-start: var(--m-6);
  border-inline-start: 1px solid var(--m-line);
}

.m-facts {
  display: grid;
  gap: var(--m-5);
  margin-block: 0;
}

.m-facts dt {
  font-size: 13px;
  line-height: 22px;
  color: var(--m-mut);
}

.m-facts dd {
  margin-inline: 0;
  margin-block: var(--m-1) 0;
  font-size: 13px;
  line-height: 22px;
}

.m-facts .m-facts__value {
  font-size: 20px;
  line-height: 32px;
  font-weight: 600;
  color: var(--m-ink);
}

.m-revenue__qualification {
  margin-block: var(--m-5) var(--m-2);
  font-size: 15px;
  line-height: 26px;
  color: var(--m-ink);
}

.m-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--m-2);
  margin-block-start: var(--m-5);
}

.m-home__work {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: var(--m-6);
  align-items: start;
}

.m-section-head {
  display: grid;
  gap: var(--m-1);
  padding-inline: var(--m-5);
  padding-block: var(--m-5) var(--m-4);
}

.m-home__decisions {
  min-inline-size: 0;
  padding-block-start: var(--m-2);
}

.m-decision {
  display: grid;
  gap: var(--m-2);
  padding-block: var(--m-4);
  border-block-end: 1px solid var(--m-line);
}

.m-decision:last-child { border-block-end: 0; }

.m-decision__title {
  margin-block: 0;
  font-size: 15px;
  line-height: 26px;
  font-weight: 600;
  color: var(--m-ink);
}

/* One readable table, including when records are sparse. */
.m-tablewrap {
  overflow: auto;
  border-radius: 0 0 var(--m-r-card) var(--m-r-card);
}

.m-table th {
  block-size: 44px;
  padding-inline: var(--m-4);
  padding-block: var(--m-2);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  text-align: start;
  color: var(--m-mut);
  background: var(--m-paper);
}

.m-table td {
  padding-inline: var(--m-4);
  padding-block: 10px;
  font-size: 15px;
  line-height: 24px;
  font-weight: 400;
  color: var(--m-ink-2);
}

.m-ledger { min-inline-size: 560px; }

.m-ledger .m-item__s {
  margin-block-start: 2px;
  font-size: 13px;
  line-height: 20px;
}

.m-table td.m-td-v,
.m-table th.num {
  text-align: end;
  color: var(--m-ink);
}

.m-table td.m-td-n {
  font-weight: 600;
  color: var(--m-ink);
}

.m-ledger__unpriced {
  color: var(--m-warn);
  font-size: 13px;
  line-height: 22px;
  white-space: nowrap;
}

#priced-line { scroll-margin-block-start: var(--m-5); }

#priced-line:target { background: var(--m-ac-dim); }

/* Status: readable words plus a dot; never colour alone. */
.m-chip,
.m-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-inline: 10px;
  padding-block: 3px;
  min-block-size: 28px;
  border-radius: var(--m-r-chip);
  background: var(--m-idle-dim);
  color: var(--m-idle);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  letter-spacing: 0;
  white-space: normal;
}

.m-status { margin-block: var(--m-4) 0; }

.m-chip::before,
.m-status::before {
  content: "";
  inline-size: 6px;
  block-size: 6px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: currentColor;
}

.m-status--warn,
.m-chip--warn {
  background: var(--m-warn-dim);
  color: var(--m-warn);
}

.m-chip--bad {
  background: var(--m-bad-dim);
  color: var(--m-bad);
}

.m-chip--ok {
  background: var(--m-ok-dim);
  color: var(--m-ok);
}

.m-chip--ac {
  background: var(--m-ac-dim);
  color: var(--m-ac-deep);
}

/* Controls: one geometry, real hit areas. */
.m-btn {
  min-block-size: 44px;
  justify-content: center;
  padding-inline: var(--m-4);
  padding-block: 9px;
  border: 1px solid var(--m-line-2);
  border-radius: var(--m-r-chip);
  box-shadow: none;
  font-size: 14px;
  line-height: 24px;
  text-decoration: none;
  transition:
    background-color var(--m-out) var(--m-ease),
    transform var(--m-press) var(--m-ease);
}

.m-btn--primary {
  border-color: var(--m-ac);
  background: var(--m-ac);
  color: #FFFFFF;
  box-shadow: none;
}

.m-btn--quiet {
  border-color: transparent;
  background: transparent;
  color: var(--m-ac-deep);
}

.m-btn--icon {
  inline-size: 44px;
  block-size: 44px;
}

.m-link {
  display: inline-flex;
  align-items: center;
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  color: var(--m-ac-deep);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.m-input,
.m-select {
  min-block-size: 44px;
  font-size: 15px;
  line-height: 24px;
  transition: box-shadow var(--m-out) var(--m-ease);
}

/* Restore native select indicator; delete physical background-position. */
.m-select {
  appearance: auto;
  background-image: none;
  padding-inline: var(--m-3);
}

:where(a, button, input, select, textarea, summary):focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

/* Specificity overrides old focus rules. */
.m-btn:focus-visible,
.m-nav:focus-visible,
.m-tab:focus-visible,
.m-input:focus-visible,
.m-select:focus-visible,
.m-range input:focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

.m-btn:not(:disabled):active,
.m-nav:active,
.m-side__t:active,
.m-seg button:active,
.m-x:active {
  transform: scale(.97);
}

.m-btn:disabled:active { transform: none; }

@media (hover: hover) and (pointer: fine) {
  .m-btn:not(:disabled):hover { background: var(--m-page); }
  .m-btn--primary:not(:disabled):hover {
    background: var(--m-ac-deep);
  }
  .m-table tbody tr:hover { background: #F8FAF8; }
  .m-link:hover { color: var(--m-ac); }
}

/* Supporting evidence is a document section, not another dashboard. */
.m-evidence {
  border-block-start: 1px solid var(--m-line-2);
}

.m-evidence > summary {
  padding-block: var(--m-4);
  cursor: pointer;
  min-block-size: 44px;
}

.m-evidence > summary .m-meta {
  display: block;
  margin-block-start: var(--m-1);
}

.m-evidence__row {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: var(--m-4);
  padding-block: var(--m-4);
  border-block-start: 1px solid var(--m-line);
}

.m-evidence__row > * { margin-block: 0; }

/* A genuine empty record list: ordinary editorial content. */
.m-empty {
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  text-align: start;
}

.m-empty__t {
  font-size: 15px;
  line-height: 26px;
}

.m-empty__d {
  max-inline-size: 60ch;
  margin-inline: 0;
  font-size: 13px;
  line-height: 22px;
}

/* No drawing animations or blurred text swaps. */
.m-chart__grow,
.m-arc__fill,
.m-fstep__b i {
  animation: none;
}

.m-fstep__b i,
.m-meter i {
  background: var(--m-ac);
}

.m-view__p,
.m-view__p[data-enter] {
  opacity: 1;
  transform: none;
  filter: none;
  transition: none;
}

.m-input,
.m-select,
.m-tip2,
.m-table tbody tr,
.m-th-sort svg,
.m-cb {
  transition-timing-function: var(--m-ease);
}

.m-dlg__p {
  animation: m-dialog-enter var(--m-in) var(--m-ease);
}

dialog.m-dlg::backdrop {
  animation: m-fade var(--m-in) var(--m-ease);
}

dialog.m-dlg[data-closing] .m-dlg__p {
  animation: m-dialog-exit var(--m-out) var(--m-ease) both;
}

dialog.m-dlg[data-closing]::backdrop {
  animation: m-fade var(--m-out) var(--m-ease) reverse both;
}

@keyframes m-dialog-enter {
  from { opacity: 0; transform: scale(.97); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes m-dialog-exit {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(.97); }
}

@media (max-width: 1200px) {
  .m-home__work { grid-template-columns: minmax(0, 1fr); }
}

/* Reachable mobile navigation without the existing unopened drawer. */
@media (max-width: 900px) {
  .m-shell { display: block; }

  .m-side,
  .m-side[data-collapsed] {
    position: static;
    inline-size: 100%;
    block-size: auto;
    transform: none;
    overflow: visible;
    border-inline-end: 0;
    border-block-end: 1px solid var(--m-line);
    transition: none;
  }

  .m-side__b,
  .m-side__f { display: none; }

  .m-side__nav {
    display: flex;
    overflow: auto;
    padding-inline: var(--m-4);
    padding-block: var(--m-2);
  }

  .m-nav { flex: 0 0 auto; }

  .m-side[data-collapsed] .m-nav span,
  .m-side[data-collapsed] .m-nav b {
    opacity: 1;
    transform: none;
  }

  .m-page,
  .m-bar { padding-inline: var(--m-4); }
}

@media (max-width: 700px) {
  :root {
    --m-t-hero: 56px;
    --m-leading-hero: 64px;
  }

  .m-home { gap: var(--m-5); }

  .m-card--revenue {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-5);
    padding-inline: var(--m-5);
    padding-block: var(--m-5);
  }

  .m-revenue__context {
    padding-inline-start: 0;
    padding-block-start: var(--m-5);
    border-inline-start: 0;
    border-block-start: 1px solid var(--m-line);
  }

  .m-evidence__row {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-2);
  }

  .m-input,
  .m-select { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }

  .m-btn:active,
  .m-nav:active,
  .m-side__t:active,
  .m-seg button:active,
  .m-x:active {
    transform: none;
  }
}
```

For dialog dismissal, `shell.js` must apply `data-closing`, wait for the panel’s exit, then call `close()`. Route the close button, Escape and backdrop through that function. Reduced motion closes immediately. CSS alone cannot delay the existing `close()` calls.

Western numerals also require formatting at the data boundary; `.m-n` does not convert digits:

```js
const formatNumber = new Intl.NumberFormat("ar-SA-u-nu-latn");
```

Counted nouns need authored plural forms. Use **لا بنود، بند واحد، بندان، ثلاثة بنود، 11 بندًا** according to the count and grammatical context. Do not construct Arabic prose with `${n} + noun`.

**4. The near-empty state is the design**

Keep these distinctions explicit:

| Data condition | Display |
|---|---|
| Known booked revenue is zero | **0 ر.س**, full-strength ink |
| An opportunity exists without pricing | **لم يُسعّر** |
| A target has not been configured | **لم يُحدّد** |
| No opportunity lines exist | **لا بنود مفتوحة** |
| A future period has not happened | **لم يبدأ بعد** |
| A value cannot be calculated from available evidence | **غير متاح** plus the specific reason |

Never substitute `—` for all six meanings.

Home remains visually complete with zero revenue because its composition depends on **a number, an explanation and real records**. It does not depend on a chart becoming interesting.

If the opportunity list reaches zero records, retain its heading and replace the rows with:

> **لا توجد فرص بيع مفتوحة**  
> لم تتحول أي جهة مهتمة من الحملة 38 إلى فرصة.  
> **مراجعة المهتمين**

Show that campaign sentence only while that condition remains true. No illustration, dashed drop zone, onboarding confetti or artificially tall blank panel.

Do not render the reference’s gradient bars now. There is no supported monthly target series to plot. When actual booked revenue exists, a compact historical chart can use blue gradient bars with matching cap dots, January at the right, and clearly distinct future periods. The current zero does not need twelve decorative columns.

**5. Explicit delete list**

Delete from **Home**:

- `#vChart`, `#vList`, their chart/list switch and `#quarters`.
- `MONTHLY`, prorated target arithmetic and the fabricated monthly target series.
- The five date presets and custom range controls.
- The readiness arc, account dot matrix, pipeline-health matrix and heat strip.
- Both funnels and every inferred stage-loss percentage.
- The entire embedded Kanban board, including rotated empty-stage rails.
- The standalone four-item decision card; replace it with the three contextual action rows.
- The separate indicators destination.
- The old toolbar, fake search shortcut and duplicate “الرئيسية” breadcrumb.

Delete or replace across **the system**:

- `.m-insight` and its decorative gradient, nested cards and carousel dots.
- Duplicate `.m-chip`, `.m-search`, `.m-crumb` and `.m-form` definitions.
- Negative tracking on Arabic text.
- `700ms`/`900ms` chart animations, text blur swaps and the second easing curve.
- Grab cursors and focusable cards without implemented actions.
- Physical direction declarations such as `background-position:left` and asymmetric physical padding.
- Hard-coded navigation counts.
- “hello”, ZIP filenames and skill-installation copy in product workflows.
- The unsupported weighted forecast and unsupported response-time statistic in Reports.
- The “توزيع بالتساوي” shortcut that silently suggests changing a deliberately Q3-scoped target.
- Repeated product campaign buttons and the second navigation strip on a product record.

Keep Reports for dated analysis and export. Keep the pipeline workspace for stage management. Keep Products for product readiness and configuration. Home owns the executive answer.

**Current design verdict: Block.** The source and proposed text-colour contrast were checked; the proposed layout has not been browser-rendered. No files were modified.
