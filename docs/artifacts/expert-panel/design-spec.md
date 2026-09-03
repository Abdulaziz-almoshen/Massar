# Massar Marketing Module — Production Design Spec (cm.com-class)

> **Author:** design lead · **Date:** 2026-08-11
> **Target file:** `massar-engine/src/dashboard.ts` (single served HTML, one `<style>` block, IBM Plex Sans Arabic only, RTL).
> **References researched:** the founder's three reference boards in `_مسار/uploads/` (Smart-Campaigns center, partner-tracking analytics, 6-page wizard + monitor), cm.com Mobile Marketing Cloud (white canvas, hairline cards, committed dark CTAs, airy sections), Bird (recessive chrome, semantic status colors, monospace-feel numerics in tables). Chart rules follow the dataviz method; the categorical palette below was **validated by script** (CVD ΔE 15.6 worst pair — PASS; contrast WARN → every chart mark must carry a visible ink label, mandated in §3).
> **Identity is non-negotiable:** navy sidebar `#2F5F94→#1F4470`, teal accent `#3FB6B0`, gold moments `#C9A227`. The reference boards' indigo/green CTAs translate to Massar deep teal; their structure translates 1:1.

---

## 1 · Design-language delta — token by token

The current CSS is *half-migrated*: the `<style>` block already speaks a modern gray scale (`#101828/#475467/#667085/#98A2B3/#EAECF0/#F2F4F7/#F9FAFB`) while every view function still sprays a second, older scale inline (`#13294b/#3b4657/#5b6678/#7b8597/#9aa4b4/#e9edf3/#eef1f5/#f3f5f8/#f8fafc`). Two neutral systems on one screen is the #1 thing separating us from the cm.com bar. Everything below assumes **one token block at the top of `<style>`** and inline styles migrated to classes.

### 1.1 Canvas & surfaces

| Token | Current | Target | Why |
|---|---|---|---|
| `--canvas` | `#F4F6FA` | **keep `#F4F6FA`** | just decided; matches reference near-white canvas |
| `--surface` | `#fff` | `#FFFFFF` | cards/tables/panels |
| `--surface-2` | `#F9FAFB` (partial) | `#F9FAFB` | table headers, row hover, footers, quiet wells |
| Card elevation | shadow-only `0 1px 3px rgba(16,24,40,.07), 0 1px 2px …` | **border-first:** `border:1px solid #EAECF0; box-shadow:0 1px 2px rgba(16,24,40,.04)` | the reference boards and cm.com are hairline-bordered with a whisper shadow — shadow-only reads soft/prototype |
| Hover elevation (interactive cards only) | none | `box-shadow:0 4px 12px rgba(16,24,40,.08); border-color:#D8DEE7; transition:.15s` | list rows/product cards that navigate |
| Modal/panel elevation | ad-hoc | `--shadow-overlay: 0 20px 48px rgba(16,24,40,.22)` | one value for convo panel + launch modal |

### 1.2 Neutrals — ONE scale (the migration map)

```css
--ink-900:#101828;  /* titles, values, row titles */
--ink-700:#344054;  /* strong body, chart category labels */
--ink-600:#475467;  /* body, card h3, form labels */
--ink-500:#667085;  /* secondary text, axis ticks, table headers (AA 4.97:1) */
--ink-400:#98A2B3;  /* meta/timestamps ONLY — never sentences (2.58:1) */
--line-300:#D0D5DD; /* input borders idle, dashed dropzones */
--line-200:#EAECF0; /* card borders, dividers, table header rule */
--line-100:#F2F4F7; /* row dividers, chip fills, meter tracks */
--bg-50:  #F9FAFB;  /* thead, hover, wells */
```

**Search-and-destroy map (legacy → token):** `#13294b→#101828` · `#2b3648/#3b4657→#344054` · `#5b6678→#475467` · `#7b8597→#667085` · `#8a94a4/#9aa4b4/#b6bfcc→#98A2B3` · `#c2cad6/#c9d2df/#cdd4de/#d5dae2→#D0D5DD` · `#e0e5ec/#e9edf3→#EAECF0` · `#eef1f5/#f0f2f6/#f3f5f8/#f4f6f9→#F2F4F7` · `#f8fafc/#fafbfc/#fafbfd→#F9FAFB`. Mechanical, zero-risk, transforms every screen at once.

### 1.3 Brand roles (who is allowed to be colored)

```css
--navy-800:#1F4470; --navy-700:#2F5F94;            /* structure: sidebar, links, info chips, chart slot 1 */
--teal-500:#3FB6B0; --teal-600:#2E8F89;            /* live/positive marks, focus rings, chart slot 2 */
--act-700:#1F7A73;  --act-800:#176B65;             /* THE primary action color (white text 5.1:1 / 6.3:1) */
--teal-ink:#2E7D77; --teal-tint:#E9F7F6;           /* teal text-on-tint (4.4:1) */
--gold-500:#C9A227; --gold-ink:#8A6D10; --gold-tint:#FBF3DC;  /* MOMENTS: retarget, test badges, best-of highlights, active nav */
```

Rules: navy = structure and information; teal = action and life; gold appears at most **once or twice per screen** (that's what makes it a moment). Everything else is ink on white.

### 1.4 Type scale — 7 sizes, no half-pixels, Arabic-safe

Current file uses ~20 sizes (9.5→32 incl. .5 steps). Collapse to:

| Token | Size/weight | Use |
|---|---|---|
| `--t-meta` | 11px / 600–700 | overlines, table headers, timestamps, axis ticks |
| `--t-caption` | 12px / 400–600 | secondary cells, helper text, chip text (chips 11px/700) |
| `--t-body` | 13px / 400–600 | default UI text, table cells, inputs |
| `--t-emph` | 14px / 700 | row titles, buttons, tab labels |
| `--t-card` | 16px / 700 | card titles, panel headers |
| `--t-title` | 18px / 700 | identity blocks, modal titles |
| `--t-page` | 22px / 700 | page title (header) |
| KPI value | 28px / 700 | stat tiles (32px only for the single hero number on Home) |

- `body { font-size:13px; line-height:1.7 }` — Arabic needs ≥1.6; dense table cells may drop to 1.5.
- **`letter-spacing: 0` on ALL Arabic text.** Tracking breaks connected Arabic script. Delete `letter-spacing:.6px` from `.grp` and `-.2px` from `header .t`. Tracking is permitted only on Latin/digit-only runs (e.g. `+9665…`).
- **Digits policy (unify — currently mixed):** Western digits everywhere for data. Replace every `toLocaleString("ar-SA")` / `toLocaleDateString("ar-SA",…)` / `toLocaleTimeString("ar-SA",…)` with the **`"ar-SA-u-nu-latn"`** locale — Arabic month/day names stay, digits become Latin (matches all three reference boards). One percent sign: `%` (drop `٪`), rendered inside a `dir="ltr"` span when adjacent to Arabic.
- `font-variant-numeric: tabular-nums` **only** where numbers align vertically (table numeric cells, axis ticks). **Remove it from `.kpi .v`** — proportional figures on display sizes (dataviz rule; `121` looks loose in tabular).

### 1.5 Spacing scale — 4px grid

`4 / 8 / 12 / 16 / 20 / 24 / 32 / 40`. Concretely: card padding **20px** (24px for hero cards), grid gaps **16px**, section gap **24px**, page gutter **32px** (keep), table cell padding **12px 20px**, toolbar padding **14px 20px**. Kill the 7/9/11/13/14/15/17/18/22/26-px ad-hoc values as views migrate.

### 1.6 Radii

```css
--r-sm:8px;   /* chips-with-dot inner, small icon buttons */
--r-md:10px;  /* buttons, inputs, selects, nav items */
--r-lg:12px;  /* inner containers, wells, chat bubbles, dropzones */
--r-xl:16px;  /* cards, tables, panels (keep — just shipped) */
--r-full:999px; /* pills, avatars, dots, meters */
```

Buttons/inputs go 12→**10px** (current 12px on a 13px-text button reads bubbly). Everything else keeps its just-shipped value.

### 1.7 Icons — the single biggest de-prototyper

The nav's CSS-shape glyphs (`.g-sq`, `.g-ci`, `.g-tr` triangles…) and text emoji (`⬆ 🔔 📎 ⟲ ↻ ⁂ ×`) are the loudest prototype tells. Replace with an **inline SVG sprite** at the top of `<body>` (zero external assets — fully within constraints):

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="i-home" viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5M5 9.5V21h5v-6h4v6h5V9.5"/></symbol>
  <symbol id="i-megaphone" viewBox="0 0 24 24"><path d="M3 10v4m4-6 11-5v18l-11-5H4a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1h3Zm2 7v3a2 2 0 0 0 4 0v-2"/></symbol>
  <symbol id="i-pulse" viewBox="0 0 24 24"><path d="M3 12h4l2.5-7 5 14L17 12h4"/></symbol>
  <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.6a3.5 3.5 0 0 1 0 6.8M21.5 20a6.5 6.5 0 0 0-4.5-6.2"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h14v18H6a2 2 0 0 0-2 2V5Zm16 13H6a2 2 0 0 0-2 2"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></symbol>
  <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s3.5-6.5 10-6.5S22 12 22 12s-3.5 6.5-10 6.5S2 12 2 12Z"/><circle cx="12" cy="12" r="2.8"/></symbol>
  <symbol id="i-reply" viewBox="0 0 24 24"><path d="M21 17a8 8 0 0 0-8-8H5m0 0 4-4M5 9l4 4"/></symbol>
  <symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 2l1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8L12 2ZM19 16l.9 3.1L23 20l-3.1.9L19 24l-.9-3.1L15 20l3.1-.9L19 16Z"/></symbol>
  <symbol id="i-refresh" viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.3-5.6M20 3v4h-4"/></symbol>
  <symbol id="i-retarget" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/><path d="M12 1v4M23 12h-4"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="m4.5 12.5 5 5 10-11"/></symbol>
  <symbol id="i-x" viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></symbol>
  <symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 16V4m0 0-4.5 4.5M12 4l4.5 4.5M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M6 2h8l6 6v14H6V2Zm8 0v6h6"/></symbol>
  <symbol id="i-kebab" viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="12" cy="19" r="1.6"/></symbol>
  <symbol id="i-arrow-l" viewBox="0 0 24 24"><path d="M20 12H4m0 0 6-6m-6 6 6 6"/></symbol>
  <!-- also: i-target, i-chart, i-box, i-flag, i-org, i-bell, i-help, i-filter, i-export, i-whatsapp -->
</svg>
```

```css
.ic { width:20px; height:20px; flex:none; fill:none; stroke:currentColor; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
.ic-s { width:16px; height:16px; }
```

Usage: `<svg class="ic"><use href="#i-megaphone"/></svg>`. One stroke weight (1.8), always `currentColor`, 24 viewBox. Nav icons inherit the sidebar ink; active state inherits teal automatically.

### 1.8 The tinted icon circle (reference-board signature)

Every KPI tile, insight row and section header on the boards leads with a **40px circle, 10%-tint of a brand hue, containing a 20px line icon**:

```css
.icirc { width:40px; height:40px; flex:none; border-radius:999px; display:flex; align-items:center; justify-content:center; }
.ic-navy{ background:#EFF4FB; color:#2F5F94; } .ic-teal{ background:#E9F7F6; color:#2E7D77; }
.ic-gold{ background:#FBF3DC; color:#8A6D10; } .ic-ok{ background:#ECFDF3; color:#027A48; }
.ic-warn{ background:#FFFAEB; color:#B54708; } .ic-bad{ background:#FEF3F2; color:#B42318; }
```

### 1.9 Status chips — canonical set + live dot

Keep the existing `.chip .c-*` palette (all verified ≥4.4:1 on their tints). Normalize **every** hand-rolled inline chip to these classes. Additions:

```css
.chip { gap:6px; font-size:11px; font-weight:700; border-radius:999px; padding:4px 10px; border:1px solid transparent; }
.chip .d { width:6px; height:6px; border-radius:999px; background:currentColor; }   /* live/scheduled states */
.c-gold { background:#FBF3DC; color:#8A6D10; border-color:#EED9A0; }               /* تجريبية / gold moments — replaces 6 inline copies */
```

Campaign states (one vocabulary everywhere): `جارية` = c-ok + dot · `مجدولة` = c-blue + dot · `مسودة` = c-warn · `مكتملة` = c-grey · `تجريبية` = c-gold. Contact states keep `chipRow()` mapping but always through classes.

### 1.10 Buttons — a committed hierarchy

Current primary (`.btn-teal` = light `#3FB6B0` + dark text) reads pastel next to the boards' solid CTAs. Target:

```css
.btn { font:700 13px/1 inherit; border:none; border-radius:10px; padding:11px 18px; cursor:pointer;
       display:inline-flex; align-items:center; gap:8px; transition:background .15s, box-shadow .15s; }
.btn-pri  { background:#1F7A73; color:#fff; box-shadow:0 1px 2px rgba(16,24,40,.1); }   /* 5.1:1 */
.btn-pri:hover { background:#176B65; }
.btn-sec  { background:#fff; color:#344054; border:1px solid #D0D5DD; }                 /* toolbar: تصدير، فلاتر */
.btn-soft { background:#EFF4FB; color:#1F4470; }                                        /* quiet secondary */
.btn-ghost{ background:transparent; color:#475467; }
.btn-danger-soft { background:#FEF3F2; color:#B42318; }
.btn-lg { padding:13px 26px; font-size:14px; }                                          /* wizard launch */
.btn:disabled, .btn-dis { background:#F2F4F7; color:#98A2B3; cursor:not-allowed; box-shadow:none; }
.btn:focus-visible, .inp:focus { outline:none; box-shadow:0 0 0 3px rgba(63,182,176,.25); }
```

One primary per view region. `#3FB6B0` stops being a button fill and returns to what it is: the accent (marks, focus, live dots).

### 1.11 Page header & topbar

Keep the 76px white topbar but complete its anatomy per the boards: title block (right) · live chip · **actions cluster (left):** bell icon-button with count badge, help icon-button, divider, then the user identity (move `userbox` avatar+name here at ≥1200px; sidebar keeps a compact version). Icon buttons:

```css
.icbtn { width:38px; height:38px; border-radius:10px; background:#fff; border:1px solid #EAECF0; color:#475467;
         display:inline-flex; align-items:center; justify-content:center; cursor:pointer; position:relative; }
.icbtn .badge { position:absolute; top:-5px; inset-inline-end:-5px; min-width:17px; height:17px; border-radius:999px;
                background:#B42318; color:#fff; font-size:10px; font-weight:700; display:flex; align-items:center;
                justify-content:center; padding:0 4px; border:2px solid #fff; }
```

Every data screen adds a **last-updated affordance** (boards show it on all three): `آخر تحديث: 10:30 ص` + `i-refresh` ghost button — generalize the existing `livechip`.

### 1.12 Motion

One system: `transition: .15s ease` on background/border/shadow; panel slide-in `.18s` (exists); content swaps fade `.12s`. **Refresh must never blank:** on the 5s poll, re-render in place (already signature-guarded for convo — extend the idea: never innerHTML-swap an unchanged view; at minimum never show empty/skeleton between polls). `@media (prefers-reduced-motion: reduce)` disables all of it.

---

## 2 · Per-screen blueprints

DOM is written as the string-concat structures the file already uses; class-first, near-zero inline styles.

### 2.1 CAMPAIGN DETAIL (`vKmonDetail`) — full blueprint

The screen becomes four bands: **page head → KPI tiles → funnel + conversion → contact table**, with the conversation side panel unchanged in role, refined in skin.

```
.pagehead
├─ a.backlink            (svg i-arrow-l + «كل الحملات»)
├─ .pagehead-main
│  ├─ .icirc.ic-teal     (svg i-megaphone)
│  └─ div
│     ├─ h2.ph-title     campaign name  + span.chip.c-ok[.d] «جارية»
│     └─ .ph-meta        product · واتساب · launch date · «آخر تحديث 10:30 ص»
└─ .pagehead-actions
   ├─ button.btn-sec     (i-export) تصدير
   ├─ button.btn-sec.gold-moment (i-retarget) إعادة استهداف   ← gold text/border variant
   └─ button.icbtn       (i-kebab)

.kpis.kpis-6             ← 6 stat tiles, reference anatomy (§2.3 .kpi spec)
   المستهدفون · أُرسلت · وصلت · شوهدت · ردّوا · مهتمون
   each: .icirc + label + value(28px) + sub «74% من المستهدفين» + .meter

.grid-detail             (grid-template-columns: 1.6fr 1fr; gap:16px)
├─ .card  «قمع الحملة»
│  └─ .funnel            ← stage bars, §3.2 (NOT the symmetric polygon)
└─ .card  «التحويل»
   ├─ .ring svg          ← 64px conversion ring: مهتمون/مستهدفون, hero % in center
   └─ .fun-drops         per-stage drop-off list: «شوهدت → ردّوا −38%» rows

.tblwrap                 ← the contact tracker
├─ .toolbar
│  ├─ .tb-title  «المستهدفون»  + .tb-count «42 من 96»
│  ├─ .tb-spacer
│  ├─ .fchip×5   الكل | شوهدت | ردّوا | مهتمون | فشل الإرسال     (count in each)
│  ├─ .inp.inp-search (i-search) «بحث…»
│  └─ button.btn-sec.gold-moment  ⟲ إعادة استهداف هذه الفئة (42)   ← appears when filtered
├─ .thead  (grid 1.6fr 1.6fr 1.5fr 1.4fr .7fr .8fr — keep)
│   العميل · الحالة · الاهتمام والجدية · آخر رسالة · الوقت · [محادثة]
├─ .trow ×N   (existing contactRowsHtml, token-migrated; hover via CSS)
└─ .tfoot   «عرض 42 من 96» + (pager pills when a real pager lands)
```

New CSS (add to `<style>`):

```css
.pagehead { display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin-bottom:20px; }
.backlink { display:inline-flex; align-items:center; gap:6px; font-size:12px; font-weight:700; color:#667085; text-decoration:none; }
.backlink:hover { color:#101828; }
.pagehead-main { display:flex; align-items:center; gap:14px; flex:1; min-width:260px; }
.ph-title { margin:0; font-size:18px; font-weight:700; color:#101828; display:flex; align-items:center; gap:10px; }
.ph-meta { font-size:12px; color:#667085; margin-top:4px; display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.pagehead-actions { display:flex; gap:8px; align-items:center; }
.gold-moment { color:#8A6D10; border-color:#EED9A0; background:#FFFDF5; }

.kpis-6 { grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); }
.meter { height:4px; background:#F2F4F7; border-radius:999px; overflow:hidden; margin-top:10px; }
.meter i { display:block; height:100%; border-radius:999px; background:#3FB6B0; }

.grid-detail { display:grid; grid-template-columns:1.6fr 1fr; gap:16px; align-items:start; margin-bottom:16px; }
@media (max-width:1100px){ .grid-detail { grid-template-columns:1fr; } }

.toolbar { display:flex; align-items:center; gap:8px; flex-wrap:wrap; padding:14px 20px; border-bottom:1px solid #EAECF0; }
.tb-title { font-size:14px; font-weight:700; color:#101828; }
.tb-count { font-size:11px; font-weight:600; color:#667085; background:#F2F4F7; border-radius:999px; padding:3px 9px; }
.tb-spacer { flex:1; }
.fchip { font:700 11px/1 inherit; border-radius:999px; padding:7px 12px; cursor:pointer; background:#fff; color:#475467; border:1px solid #EAECF0; }
.fchip.on { background:#E9F7F6; color:#2E7D77; border-color:#3FB6B0; }
.inp-search { border-radius:999px; padding:8px 14px; width:170px; background:#F9FAFB; }
.tfoot { display:flex; align-items:center; justify-content:space-between; padding:12px 20px; font-size:11px; color:#667085; background:#F9FAFB; border-top:1px solid #EAECF0; }
.trow:hover { background:#F9FAFB; }   /* exists — DELETE all onmouseover/onmouseout JS handlers in vKmon */
```

Conversation panel (skin only): header uses `.icirc.ic-navy` avatar + name + `dir=ltr` phone; chips row keeps `chipRow()`; **keep the WhatsApp beige `#E5DDD4` message area** (authentic transcript context — the one intentionally non-neutral surface in the product); footer buttons become `.btn-pri` (استئناف) / `.btn-danger-soft` (إيقاف) / `.btn-sec.gold-moment` (تجريبي). Close button = `.icbtn` with `i-x`.

### 2.2 CAMPAIGN WIZARD (`vAimkt`) — full blueprint

The boards show a paged wizard with a numbered dot-rail. Translate to 4 steps (our real flow), one visible at a time, with a **sticky summary/launch bar** (already exists — keep, refine skin). State: `let wizStep = 1;` + `window.wizGo = (n) => { if (n < wizStep || stepDone(n-1)) { wizStep = n; render(false); } }`.

```
.wizhead (card)
├─ .wiz-title   «إنشاء حملة»  + .wiz-sub «أربع خطوات — والمساعد يتولى البقية»
└─ .steps       (RTL rail: 1 → 4 right-to-left)
   ├─ .stp.done    (svg i-check in circle)  «المنتج»
   ├─ .stp.on      (number)                 «الجمهور»
   ├─ .stp         (number)                 «الرسالة»      + .stp-line connectors
   └─ .stp         (number)                 «المراجعة والإطلاق»

step 1 · .card «أي منتج يبيعه المساعد؟»
   .prods grid → .prod refined: .icirc.ic-navy (i-box) + name + readiness bar+% (keep logic)
   + .prod-radio corner: 18px circle, border line-300 → on: act-700 fill + white i-check

step 2 · .card «من يتواصل معهم؟»
   count pill (top-left, teal tint — keep) · retarget gold band (keep, tokens)
   segment chip groups (.fchip) · search .inp-search · «تحديد المطابقين» .btn-soft
   list in .subtbl (border line-200, r-12, rows 40px, checkbox = .prod-radio 16px)

step 3 · .card «رسالة الافتتاح»  (grid 1fr 1fr)
   right: campaign-name .inp (moved from its own card) + textarea .inp + var hint «{name}»
   left:  .wa-prev refined — bubble r-12, PDF attachment row w/ i-file, reply buttons;
          caption: «معاينة واتساب — تصل رسالة واحدة»

step 4 · .card «المراجعة والإطلاق»
   .review rows (label ink-500 / value ink-900 700, divider line-100):
     المنتج · الجمهور (42 جهة — الشريحة) · الملف المرفق · الرسالة (preview well bg-50 r-12)
   .note (sandbox reality — keep) · human-approval sentence stays VERBATIM:
     «هذه الخطوة هي موافقتك البشرية على الإرسال»

.wizbar (sticky bottom card; exists — reskin)
├─ summary  «42 مستهدف · الإجازات المرضية · الملف مضمّن»  + sandbox caption
├─ .tb-spacer
├─ button.btn-ghost  السابق          (steps ≥2)
└─ step<4: button.btn-pri  التالي ←   |   step4: button.btn-pri.btn-lg  إطلاق الحملة ←
   → opens existing confirm modal (keep top teal rule; .btn-pri confirm)
```

```css
.steps { display:flex; align-items:center; gap:0; margin-top:16px; }
.stp { display:flex; align-items:center; gap:8px; font-size:12px; font-weight:700; color:#98A2B3; flex:none; }
.stp .n { width:28px; height:28px; border-radius:999px; display:flex; align-items:center; justify-content:center;
          background:#F2F4F7; color:#667085; font-size:12px; font-weight:700; border:1.5px solid transparent; }
.stp.on { color:#101828; }  .stp.on .n { background:#1F7A73; color:#fff; }
.stp.done { color:#2E7D77; cursor:pointer; }
.stp.done .n { background:#E9F7F6; color:#2E7D77; border-color:#3FB6B0; }
.stp-line { flex:1; height:2px; background:#EAECF0; margin:0 10px; min-width:24px; }
.stp-line.done { background:#3FB6B0; }
.prod { position:relative; border:1.5px solid #EAECF0; border-radius:16px; padding:18px; background:#fff; }
.prod .prod-radio { position:absolute; top:14px; inset-inline-end:14px; width:18px; height:18px; border-radius:999px;
                    border:1.5px solid #D0D5DD; display:flex; align-items:center; justify-content:center; color:#fff; }
.prod.on { border-color:#3FB6B0; background:#F6FCFB; box-shadow:0 0 0 3px rgba(63,182,176,.12); }
.prod.on .prod-radio { background:#1F7A73; border-color:#1F7A73; }
.review { display:flex; flex-direction:column; }
.review > div { display:flex; gap:16px; padding:12px 0; border-bottom:1px solid #F2F4F7; }
.review .rl { flex:none; width:130px; font-size:12px; font-weight:600; color:#667085; }
.review .rv { flex:1; font-size:13px; font-weight:700; color:#101828; line-height:1.8; }
.wizbar { position:sticky; bottom:14px; z-index:5; display:flex; align-items:center; gap:14px; flex-wrap:wrap;
          background:#fff; border:1px solid #EAECF0; border-radius:16px; padding:16px 20px;
          box-shadow:0 12px 32px rgba(16,24,40,.14); }
```

Safety invariants (unchanged by design): the launch modal stays the human checkpoint; the >50 batch warning stays; failed-send transparency copy stays.

### 2.3 HOME (`vHome`) — refinements

1. **KPI tiles → reference anatomy** (kills the centered/column-reverse look):
```css
.kpi { display:flex; flex-direction:row; align-items:center; gap:14px; text-align:start;
       background:#fff; border:1px solid #EAECF0; border-radius:16px; padding:18px 20px;
       box-shadow:0 1px 2px rgba(16,24,40,.04); }
.kpi .icirc { order:2; margin-inline-start:auto; }          /* icon at the far (left) edge in RTL */
.kpi .k { font-size:12px; color:#667085; font-weight:600; }
.kpi .v { font-size:28px; font-weight:700; color:#101828; line-height:1.1; margin-top:4px; }  /* NO tabular-nums */
.kpi .delta { font-size:11px; font-weight:700; margin-top:6px; }
.kpi .delta.up { color:#027A48; } .kpi .delta.dn { color:#B42318; } .kpi .delta.flat { color:#98A2B3; }
```
   Tiles: الحملات الحقيقية (ic-navy/i-megaphone) · المستهدفون (ic-navy/i-users) · وصلت (ic-teal/i-check) · ردّوا (ic-teal/i-reply) · مهتمون وجادّون (ic-ok/i-spark). Values in ink-900 — **stop coloring KPI numbers** (color moves to the icon circle). Delta line vs previous 7 days when computable, else the base caption.
2. **«رؤى المساعد» card** (reference board's AI-insights panel, Massar-ified): teal-tint card (`#F6FCFB`, border `#B9E4E0`), `.icirc.ic-teal` + `i-spark`, 3 computed rows — أفضل حملة (highest replied%), أعلى منتج اهتمامًا (tag counts), حملة تحتاج متابعة (lowest seen%, gold `i-flag` row) — each linking into its screen. Pure client-side derivation from `campaigns`+`campStats`; no new backend.
3. Quick actions: «+ إنشاء حملة» becomes the page's single `.btn-pri`; استيراد/معرفة become `.btn-sec` with icons, moved into the section header row.
4. Charts band: retitle per §3; every chart card gets the `.tb-count`-style meta pill; treemap replaced (§3.6).
5. Best-opportunities rows: avatar becomes `.icirc.ic-navy` initial; «الملف ←» becomes a `.btn-ghost` chevron; row hover `bg-50` via class.

### 2.4 CAMPAIGNS LIST (`vKmon`) — refinements

Move the strip of controls INTO the table card as a `.toolbar` (title+count → tabs الكل/حقيقية/تجريبية as `.fchip` → spacer → search → sort select → `.btn-pri` + إنشاء حملة). Columns: **الحملة** (`.icirc.ic-teal` `i-megaphone` + name + date second line) · **المنتج** · **الحالة** (chip vocabulary §1.9) · **الجمهور** · **مشاهدة%** · **ردود%** · **التقدّم** (`.meter` 6px + % in ink-500, bar solid `#3FB6B0` — no gradient) · kebab. Numeric cells `tabular-nums`, center-aligned. Row height 60px, CSS hover, whole row navigates. Footer `.tfoot`: «عرض 5 من 36» (+ page pills `.pgpill` when list grows past ~25: 30px squares, active = navy fill/white text). Empty state gets `.icirc` 56px `ic-teal` + `i-megaphone` instead of the dashed square.

### 2.5 CUSTOMER PROFILE (`vCustomer`) — refinements

- Identity card: keep navy square avatar (56px, r-14, navy-800 bg, teal initial — it's distinctive); name 18px; chips normalized; phone `dir=ltr` ink-400. **Context completeness: replace the 110px vertical thermometer with a 64px SVG ring** (§3.5) + «اكتمال السياق 72%» + missing-parts list under it — matches the boards' ring language.
- Action row: فتح المحادثة = `.btn-pri`; تحديث قراءة المساعد = `.btn-sec` with `i-refresh` (spin animation while loading, no «جارٍ…» label swap).
- «فهم المساعد» card: keep teal-tint identity; `⁂` → `.icirc.ic-teal` + `i-spark`; intent badge = `.chip` variants; «الخطوة التالية» well keeps the 3px teal inline-start rule (good pattern — promote to class `.next-well`).
- Timeline: add a connecting rail — `.tl { position:relative }` with `::before { inset-inline-start:4px; top:8px; bottom:8px; width:2px; background:#F2F4F7 }`; dots 10px with 2px white ring sit on the rail; each row: title 13px ink-700, meta 11px ink-400. Kind→color via existing `tlDot` mapped to tokens (in=navy-700, out=teal-500, camp=teal-600, tag=gold-500, file=warn, st/sys=line-300).
- Layout: `grid-template-columns: 1fr 1.4fr` at ≥1100px (understanding | timeline), stacking below.

### 2.6 AUDIENCE LIST (`vCustomers`) — refinements

Import card collapses into a compact header card: title + one-line explainer, `.btn-pri` رفع ملف (i-upload) + `.btn-soft` القالب الجاهز; paste-mode stays inside `<details>`. The list becomes a real `.tblwrap` with `.toolbar` (title + count pill + segment-key chips + search) + `.thead` (المنشأة · الشرائح · الجوال · [حذف]) + rows (avatar `.icirc.ic-navy` initial + name + «ملف ←» ghost link when a conversation exists) + `.tfoot` cap band. Delete = `.icbtn` 28px with `i-x` in bad-tint, `event.stopPropagation()` kept.

---

## 3 · Chart styling spec (SVG/CSS, single-file)

**Palette (validated):** categorical order is FIXED — slot1 `#2F5F94` navy · slot2 `#3FB6B0` teal · slot3 `#C9A227` gold · slot4 `#8A63B8` violet — never cycled, never rank-assigned; a 5th series folds into «أخرى». Sequential (funnel/intensity): teal ramp `#D9F0EE → #A7DEDA → #6FC7C1 → #3FB6B0 → #2E8F89 → #237069`. Status marks: ok `#12B76A` · warn `#F79009` · bad `#F04438` — reserved for state, never used as a series color. **Because teal/gold sit below 3:1 on white (validator WARN), every mark must carry a visible ink value-label or a table twin — no color-only reading.**

**Anatomy (all charts):**
- **Axis/gridlines:** solid hairline 1px, NEVER dashed. Baseline `#EAECF0`; horizontal gridlines max 3–4 at `#F2F4F7`. No vertical gridlines, no axis line on the value axis, no tick marks.
- **Labels:** category/axis ticks 10.5–11px `#667085`, `tabular-nums`; values 11px/700 **`#101828` — text never wears the series color** (identity lives in the mark or a swatch beside the text). Label selectively: caps/ends/extremes, not every point when ≥8 marks.
- **Bars/columns:** thickness **≤24px** (fix `colChart` max-width 46→24), radius **4px on the data end only, square at the baseline** (`rx=4` top / 0 bottom — fix the current `7px 7px 3px 3px`), single baseline.
- **Stacked bars:** a **2px surface (white) gap** between segments — in `dailyActivitySvg` shift the upper `rect` up 2px; no strokes around marks, ever.
- **Lines/sparklines:** 2px, round cap/join; markers ≥8px with a 2px white ring where they overlap.
- **Containers:** every plot in `dir="ltr"`; height includes the x-label band (never a nested scroll); numbers via `ar-SA-u-nu-latn`.

Per chart:

1. **Sparkline (campaigns-list rows, KPI trends):** 56×20 viewBox, `<path fill="none" stroke-width="2">`, teal `#3FB6B0`; last point 3px dot. Trend semantics only — no axis, no labels. Title-attr tooltip.
2. **Funnel (`funnelSvg` — REPLACE the symmetric polygon):** RTL stage-bar list, one row per stage: label (12px/600 ink-700, fixed inline-start column) · track (`#F2F4F7`, 10px, r-full) · fill (sequential teal ramp step *i*, min-width 3%) · value at bar end 12px/700 ink-900 + share «64%» 11px ink-500. Between rows, a drop-off whisper: «↓ −38%» 10.5px ink-400 (gold `#8A6D10` when the drop exceeds 60% — the gold moment). White-on-teal labels inside polygons (2.5:1) disappear with the polygon.
3. **Columns (`colChart`, size/sector):** bar 24px teal (single series = one color — no per-bar hues), value on the cap 11px/700 ink-900, category 10.5px ink-500 below, baseline hairline. ≤6 categories.
4. **Stacked daily activity:** in-messages `#2E8F89`, out `#C6D8EE` (navy-100 de-emphasis — correct as is), 2px white gap between segments, bars ≤24px, baseline `#EAECF0`, day labels 10.5px `#667085` (raise from 8.5px `#9aa4b4` — too small/faint), legend swatches 10px r-3 + 11px ink-500 text. Label only the max day + today; title-attr tooltips carry the rest.
5. **Ring/donut (conversion ring, context-completeness; channels donut when multi-channel arrives):** two `<circle>`s — track `#F2F4F7`, arc stroke 8px round-cap via dasharray; center value 20px/700 ink-900 + 10.5px ink-500 caption. Donut only for part-to-whole with ≤4 clearly-different segments (else h-bars); always a legend with value+% — never color-only.
6. **Treemap (`treemapTiles`) — DELETE.** The brown ramp is off-palette, and darker-where-bigger on nominal cities is a double-encode anti-pattern. Cities become `hbarRows` (label + count + single-hue navy `#2F5F94` bars on `#F2F4F7` tracks) — consistent with «الاهتمام حسب المنتج».
7. **Meters/progress:** fill = one semantic hue (teal progress / status hue when it IS a status); track = `#F2F4F7`; 4px (KPI) / 6px (table); no gradients inside data fills (`linear-gradient(90deg,#3FB6B0,#2E7D77)` in list progress + profile gauge → flat `#3FB6B0`).

---

## 4 · Do-NOT list — patterns that read cheap (enforceable in review)

**Color & chrome**
1. NO second neutral scale — any hex outside §1.2/§1.3 in a view function fails review.
2. NO gradients on content (data fills, meters, buttons, chips). Gradients live in exactly one place: the navy sidebar.
3. NO coloring text with series/accent colors for decoration — values/labels are ink; color enters via icon circles, marks, chips.
4. NO indigo/purple UI accents (reference board #1's CTA is *their* brand, not ours) — Massar primary is deep teal `#1F7A73`.
5. NO gold beyond 1–2 moments per screen; NO teal `#3FB6B0` as a text color or as white-text button fill (2.4:1).
6. NO shadow-only cards, NO stacked heavy shadows, NO borders + strong shadow together (hairline + whisper only).

**Type & Arabic**
7. NO letter-spacing on Arabic script — ever (breaks joining). No half-pixel font sizes. No new sizes outside §1.4.
8. NO mixed numerals (٤٢٠ vs 420) or mixed ٪/% — `ar-SA-u-nu-latn` + `%` everywhere.
9. NO `tabular-nums` on KPI/hero values; no display/serif face anywhere (IBM Plex Sans Arabic only).
10. NO ALL-CAPS-style faux emphasis via tracking on the nav group labels; weight + tone (`700` / `#A9C2E0`) does the work.

**Components**
11. NO emoji as UI icons (⬆ 🔔 📎 ⟲ ↻ ⁂ ✓ ×) and NO CSS-shape glyphs — sprite icons only. (Emoji stay legitimate inside chat *content*.)
12. NO JS hover handlers (`onmouseover` style swaps) — `:hover` classes only.
13. NO centered-text KPI cards; no bare tables outside `.tblwrap`; no filter controls floating outside the table card's toolbar; no per-chart filter rows (one filter row scopes everything below it).
14. NO dashed gridlines/axes; dashed borders ONLY for dropzones/empty affordances.
15. NO white-on-light-teal labels inside marks; no value on every point past 7 marks; no dual-axis charts; no rainbow/multi-hue ramps for magnitude; no recolor-on-filter (a campaign keeps its hue when the list is filtered).
16. NO skeleton flash on the 5s poll — hold the previous render.
17. NO new modal patterns — one modal skin (launch confirm), one side-panel skin (convo).
18. NO copy in `#98A2B3` longer than a timestamp/meta fragment (fails contrast for body text).

---

## 5 · Implementation order (each step ships green on its own)

1. **Tokens + neutral migration** (§1.2 map — mechanical find/replace in views) → instant coherence.
2. **Card/border/shadow + buttons + chips + focus** (§1.1, 1.9, 1.10).
3. **Icon sprite + nav/topbar anatomy** (§1.7, 1.11) — de-prototypes every screen at once.
4. **KPI anatomy + digits policy** (§2.3, §1.4).
5. **Table anatomy on list + detail** (§2.1, 2.4) with toolbar/tfoot/fchips.
6. **Chart pass** (§3: funnel bars, treemap→hbars, mark caps, gaps, labels).
7. **Wizard step-rail** (§2.2) and **profile ring/timeline** (§2.5).
8. QA gate: RTL sweep at 1280/1440/900w, contrast spot-checks, reduced-motion, and the §4 checklist as the review rubric.
