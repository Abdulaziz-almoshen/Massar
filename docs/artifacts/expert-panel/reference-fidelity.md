# Reference-Fidelity Audit — founder's 5 references vs Massar dashboard

**Date:** 2026-08-11 · **Auditor:** reference-fidelity panel
**Founder's instruction:** "I want you to mimic, copy, do the same." Target: ≥90% visual fidelity, keeping RTL + Massar navy sidebar.

**References**
1. `image-cache/…/14.png` — CXP customer-prediction cards (3-month progression, context rail)
2. `image-cache/…/15.png` — HALO customer-360 (history timeline, chat resolution, prediction feed)
3. `image-cache/…/16.png` — Tableau marketing dashboard (KPI row, funnel trapezoid, scatter, columns, treemap)
4. `image-cache/…/17.png` — Emaily campaigns list (pill tabs, toolbar, table anatomy, pagination)
5. `image-cache/…/13.png` — WhatsApp: opener + PDF as two bubbles (complaint; server-side already fixed — note only)

**Ours** — `docs/artifacts/intel-slice/actual-{home-charts,kmonlist3,profile,customers2}-1440x900.png`
**Code** — everything lives in `/Users/abdulaziz/Projects/Massar/massar-engine/src/dashboard.ts` (single-file SPA: CSS lines 18–165; `vKmon` ≈405, `vHome` ≈514, `vCustomers` ≈922, `funnelSvg` ≈974, `colChart` ≈991, `treemapTiles` ≈999, `dailyActivitySvg` ≈1015, `vHomeCharts` ≈1036, `vCustomer` ≈1077, `vAimkt` ≈646, convo drawer `renderConvo` ≈355).

**Caveat honored:** the screenshots are one CSS iteration behind (cards/shadows already lightened; `funnelSvg` trapezoid and value-top KPIs already exist in code). Items already fixed in code are tagged **[in code]**. Everything else is structure/anatomy that CSS polish alone will not fix.

---

## Verdict (one paragraph)

Our shell is competent Untitled-UI, but the references are a different dialect: **bigger, rounder, calmer**. They run on 44px pill controls, 28px icon-chips, floating rounded rows, one accent color at a time, tiny colored kickers over bold titles, big neutral numbers, and metric values promoted into **white sub-cards inside tinted panels**. We currently compress everything (30–38px controls, 11–13px type, borders instead of air), colorize raw numbers instead of chips, carry semantics in text-only chips without icons, and lack five signature components entirely: floating table rows with checkbox/toggle/kebab/pagination, the scatter quadrant chart, per-dimension column cards, the edge-mounted context rail, and the connected prediction-feed timeline. Closing those is ~2 days of work in one file.

---

## 0 · Global temperature gaps — apply these tokens FIRST

### (a) Gap table — tone & scale

| Dimension | References (all 4) | Ours today | Gap |
|---|---|---|---|
| Page bg | flat near-white `#F1F2F4`–`#F7F7FB` (Emaily adds faint lavender gradient) | `#F4F6FA` | ✔ close — keep |
| Card radius | 16–24px (Emaily table card 20, CXP cards 24) | 16px | ↑ to 16/20 two-step |
| Card padding | 24–32px | 24px | ✔ / header cards → 28 |
| Control height | inputs/selects **44–46px**, tabs **44px**, buttons 44px | inputs ~38, tabs ~34, buttons ~40 | **+8–10px everywhere** |
| Chip anatomy | 28px tall, **leading 14px glyph**, 13px 600 text, 1px border, radius 999 | 22–24px, **no icon**, 11.5px | icons + scale |
| Row style (tables) | **floating rounded bands** `#F7F7F9` r12, 8px white gaps, h≈60 | flat rows, 1px bottom border, h 52–62 | signature look missing |
| Numbers in cells | plain `#111` 15px; **color lives only in chips/bars** | 12.5px **colored** (teal/navy) per column | de-colorize numbers |
| Kicker idiom | 9–11px 700 uppercase letter-spaced micro-label above titles | none | add (Arabic: 10px/700 colored, **no letter-spacing** — connected script; keep `letter-spacing:.8px` only for Latin/digits) |
| Titles | page h1 in content, 32–34px 700; card titles 13px 700 grey | title only in 76px topbar (21px) | add in-content title block |
| Accent discipline | ONE accent per surface (violet OR black OR brick) | navy+teal+gold+green mixed per screen | one accent per surface: teal for actions, navy for data, warm ramp for analytics |
| Shadows | `0 1px 2px rgba(0,0,0,.04), 0 12px 32px -16px rgba(0,0,0,.10)` soft & wide | `0 1px 3px …` tight | widen |

### (b) BUILD SPEC — token block (replace/extend `<style>` head, lines 18–24)

```css
:root{
  --bg:#F5F6F8; --card:#fff; --line:#EAECF0; --line-soft:#F2F4F7;
  --ink:#101828; --ink-2:#475467; --ink-3:#667085; --ink-4:#98A2B3;
  --accent:#2E8F89; --accent-strong:#2E7D77; --accent-tint:#E9F7F6; --accent-border:#C4E8E5;
  --navy:#1F4470; --navy-2:#2F5F94; --navy-tint:#EFF4FB;
  --band:#F7F8FA;                    /* floating row bands */
  --warm-1:#F4553C; --warm-2:#D9473A; --warm-3:#A63E36; --warm-4:#7E3A33;  /* analytics ramp (ref 16) */
  --r-sm:10px; --r-md:12px; --r-lg:16px; --r-xl:20px;
  --sh-card:0 1px 2px rgba(16,24,40,.04), 0 12px 32px -16px rgba(16,24,40,.10);
  --h-control:44px;
}
.card,.tblwrap,.kpi,.step{ box-shadow:var(--sh-card); }
.kicker{ font-size:10px; font-weight:700; color:var(--ink-4); margin-bottom:4px; }
.kicker.acc{ color:var(--accent-strong); }
.pagehead{ display:flex; align-items:center; gap:14px; margin:2px 0 20px; }
.pagehead h1{ margin:0; flex:1; font-size:27px; font-weight:700; color:var(--ink); }
.chip{ height:28px; padding:0 12px; gap:6px; font-size:12px; }        /* was 11.5px, thin */
.chip .gi{ font-size:13px; line-height:1; }                            /* leading glyph slot */
.ptab{ height:44px; padding:0 24px; font-size:13.5px; border-radius:999px; }
.ptab.on{ background:#101828; color:#fff; }                            /* already black — keep */
.inp{ height:44px; border-radius:999px; padding:0 18px; font-size:13.5px; }
.sel{ height:44px; border-radius:999px; padding:0 40px 0 18px; }       /* RTL: chevron sits left */
```

Topbar stays (live chip home), but every screen gains a `pagehead` block as first content child:
`<div class="pagehead"><h1>الحملات</h1><button class="btn btn-ghost">⬇ تصدير CSV</button><a class="btn btn-dark">+ إنشاء حملة</a></div>`
`btn-dark { background:#101828; color:#fff; height:44px; border-radius:999px; padding:0 24px; }` — the Emaily "Create Campaign" black pill.
`btn-ghost { background:#fff; border:1px solid var(--line); color:var(--ink-2); height:44px; border-radius:999px; }`

---

## 1 · Ref 17 — Emaily campaigns list ↔ «متابعة الحملات» (`vKmon`, line 405) — **biggest gap**

### (a) Gap table

| Element | Emaily reference (exact) | Ours (`actual-kmonlist3` + code) | Gap |
|---|---|---|---|
| Page title | in-content "Campaigns" ~34px 700 + right: Export CSV (white pill + icon) & Create Campaign (black pill 44px) | title only in slim topbar; small teal «+ إنشاء حملة» inside toolbar row | title block + 2 page actions missing |
| Status tabs | separate row ABOVE card: 5 pills All/Drafts/Scheduled/Sending/complete, h44, r999, pad 12×28, active = solid black + white text | 3 small pills (h~30, 12px) mixed into same row as search/sort; active = navy `#13294b` | scale ×1.4, own row, black active, 5 states |
| Toolbar | INSIDE table card, own row: wide pill search (h46, leading 🔍, ~40% width) + 3 pill selects: "All statuses", "Last 30 days", "Sort by: Date Created" | 190px search + 1 bare select, floating outside card | move into card; add status + date-range selects; widths search flex-1 |
| Table container | white card r20, toolbar row + header + rows + footer all inside | `tblwrap` r16, note line orphaned BELOW card | one container owns everything incl. footer |
| Header row | 14px `#6B7280` 500, per-column **leading icons**, sort glyphs ⇅ on Campaign/Type/Status/Revenue/Progress | 11px 700 `#7b8597`, no icons, no sort affordance | +3px, icons, ⇅ |
| Row band | each row a **rounded r12 `#F7F7F9` band, h≈60, 8px white gap** between rows | flat rows, 1px `#f3f5f8` bottom border | signature "floating rows" missing |
| Col 1 | ◯ circle checkbox (20px, 1.5px `#D1D5DB` border) | none | add — feeds bulk «إعادة استهداف المحدد» |
| Col 2 | iOS toggle 40×24 (on=`#3B82F6`, knob 20 white) then campaign name 15px 600 `#111` | name 12.5px 700 + date squeezed under | toggle (ours teal `#2E8F89`) + name 14.5px; date moves to its own شعور? keep as 11px `--ink-4` second line |
| Type col | outlined chip w/ glyph: 🏷️ Promotion · 📦 Stock out · 📰 Newsletter · ⚙️ Automation — grey 1px border, white bg | plain text `المنتج` 11.5px | product chip: `<span class="chip c-grey"><span class="gi">🏷️</span>الإجازات المرضية</span>` |
| Status col | tinted chip w/ glyph + border: ✅ Completed (green `#ECFDF3/#12B76A`), 📝 Draft (pink `#FEF3F2/#F04438`), 📤 Sending (amber `#FFFAEB/#F79009`), 📅 Scheduled (blue `#EFF8FF/#2E90FA`) | 2 states only (تجريبية gold / جارية green), no glyph | 4-state map: جارية=📤 amber→or keep green ✓; مكتملة=✅ green; مجدولة=📅 blue; تجريبية=🧪 gold — glyph in `.gi` |
| Numbers (Audience/Open/Click) | plain 15px `#111` regular; **no color** | 12.5px 700 colored (teal/navy per column) | 14px 500 `--ink`, color removed |
| Revenue col | €1,240 | (no revenue data) | → **«مهتمون»** count (interest), plain number |
| Progress col | 4px flat blue line ~110px on `#E5E7EB` track + "80%" right, 13px | 6px gradient teal + 10.5px % | 4px solid `--navy-2`, track `#EEF1F5`, % 12.5px `--ink-3` **[close in code]** |
| Row end | ⋯ kebab 24px | none | add (menu: فتح · إعادة استهداف · تصدير) |
| Footer | inside card: left meta "Metrics update every 15 minutes…" w/ icon · right pagination ‹ 1 **2** 3 4 … › — 40px white r10 squares, active = black **circle** white text | note orphaned under card; no pagination | move note into footer; paginate 25/page |
| RTL column order | LTR: ☑ · toggle+Campaign · Type · Status · Audience · Open · Click · Revenue · Progress · ⋯ | — | RTL mirror: ☑ · مفتاح+الحملة · المنتج · الحالة · الجمهور · مشاهدة · ردود · **مهتمون** · التقدّم · ⋯ |

### (b) BUILD SPEC — apply in this order

1. **Pagehead** (before tabs): `<div class="pagehead"><h1>الحملات</h1> <button class="btn btn-ghost" onclick="exportCampaignsCsv()">⬇ تصدير CSV</button> <a href="#aimkt" class="btn btn-dark">+ إنشاء حملة</a></div>`. `exportCampaignsCsv()` = client-side blob from `campaigns`+`campStats` (no backend needed).
2. **Tabs row** (own line, `margin-bottom:16px`): use upgraded `.ptab` (h44). States: الكل / حقيقية / تجريبية / مكتملة / مجدولة (last two render disabled-grey until backend states exist; keep counts suffix `(3)`).
3. **Table card**: one `tblwrap` `border-radius:var(--r-xl)`; first child toolbar:
   ```html
   <div class="tb-toolbar"> <!-- display:flex; gap:12px; padding:20px; border-bottom:1px solid var(--line-soft); -->
     <input class="inp" style="flex:1;min-width:260px" placeholder="ابحث في الحملات…">   <!-- leading 🔍 via background-image or wrapper -->
     <select class="sel">كل الحالات…</select>
     <select class="sel">آخر ٣٠ يومًا / آخر ٧ أيام / الكل</select>
     <select class="sel">ترتيب: الأحدث / الأكثر ردودًا / الأكثر مشاهدة</select>
   </div>
   ```
4. **Grid template** (header + rows share): `grid-template-columns: 24px 1.9fr 1.1fr 1fr .7fr .6fr .6fr .6fr 1fr 28px; gap:12px;`
   Header: `padding:12px 20px; font-size:13px; font-weight:600; color:#6B7280; background:#fff; border:none;` — each label `<span class="gi">…</span>` + ⇅ `<span style="font-size:10px;color:#C0C6D0">⇅</span>` on الحملة/المنتج/الحالة/التقدّم.
5. **Floating rows**: wrap rows in `padding:8px 12px 12px; display:flex; flex-direction:column; gap:8px;` container; each row:
   ```css
   .rowband{ display:grid; grid-template-columns:/* same */; align-items:center;
     background:var(--band); border-radius:12px; min-height:60px; padding:0 12px; cursor:pointer; }
   .rowband:hover{ background:#F1F3F6; }
   ```
6. **Checkbox** `20px; border-radius:999px; border:1.5px solid #D1D5DB; background:#fff;` → checked: `background:#101828; border-color:#101828;` white ✓ 11px. State: `campSel = new Set()`; bulk bar appears above table when >0: «إعادة استهداف المحدد (N)».
7. **Toggle** (visual parity now, pause-wire later): `.tgl{ width:40px;height:24px;border-radius:999px;background:#E5E7EB;position:relative;flex:none;} .tgl.on{background:var(--accent);} .tgl i{position:absolute;top:2px;inset-inline-start:2px;width:20px;height:20px;border-radius:999px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.15);transition:.15s;} .tgl.on i{inset-inline-start:18px;}` — on = campaign جارية. Title `متابعة المساعد` ; clicking shows «إيقاف الحملة يأتي مع محرك الحملات» toast until backend flag exists.
8. **Chips**: product chip `c-grey` + glyph 🏷️/📦 per product family; status per map above; all `height:28px`.
9. **Numbers**: `font-size:14px; font-weight:500; color:var(--ink); font-variant-numeric:tabular-nums; text-align:center;` — delete the teal/navy colored percents (`vKmon` lines 443–444).
10. **مهتمون column** replaces Revenue slot: `st.interested` plain count.
11. **Kebab**: `width:28px;height:28px;border-radius:8px;color:#98A2B3;` hover `background:#EDEFF2`; menu = positioned card (فتح اللوحة / ⟲ إعادة استهداف / تصدير الصف).
12. **Footer** (inside card): `display:flex;align-items:center;padding:16px 20px;border-top:1px solid var(--line-soft);`
    - start: `📈 الأرقام تتحدّث لحظيًا من حالات تسليم واتساب — لا تقديرات.` 12.5px `--ink-3` (move existing orphan line here, delete line 448's div).
    - end: pagination `‹ ١ ٢ ٣ … ›` — `.pg{width:40px;height:40px;border-radius:10px;background:#fff;border:1px solid var(--line);color:var(--ink-2);} .pg.on{background:#101828;color:#fff;border-radius:999px;border-color:#101828;}` — page size 25 (also replaces `LIST_CAP` truncation note pattern in `vCustomers` and target-picker).
13. **«محادثات خارج الحملات» section** below inherits identical anatomy (header icons, floating rows, chips w/ glyphs).

**Same anatomy propagates to** `vCustomers` (line 922) — checkbox column, floating rows, chip glyphs (📍 city, 🏥 sector, 📏 size), pagination instead of «+N آخرون», pagehead with «⬆ رفع ملف» (teal) + «القالب الجاهز» (ghost).

---

## 2 · Ref 16 — Tableau marketing dashboard ↔ «الرئيسية» (`vHome` 514 + `vHomeCharts` 1036)

### (a) Gap table

| Element | Tableau reference (exact) | Ours | Gap |
|---|---|---|---|
| KPI strip | **ONE row, 6 cards**: big value ~28px 700 TOP, label 13px grey BOTTOM, centered, white r12, h≈130 | TWO strips (5 counts + section title + actions row + 4 rates) | merge into one 6-card row **[value-top already in code via `column-reverse`]** |
| KPI content | # Campaigns · CTR · Engagement · Conversion · CPC · Total Costs | counts + rates split | map (no CTR/CPC/€): الحملات · المستهدفون · نسبة الوصول · نسبة المشاهدة · نسبة الردود · نسبة الاهتمام |
| Row 2 layout | funnel card ~38% + scatter card ~62%, aligned heights ≈420px | auto-fit minmax(300px) soup — 5 cards flow arbitrarily | explicit grid `grid-template-columns:5fr 7fr` |
| Funnel | 4 stacked **trapezoids**, warm single-hue ramp `#F4553C→#D9473A→#A63E36→#7E3A33`, white values ~15px 700 inside, ~3px white seams, slight shadow; stage labels in right column 13px 700 dark aligned per band | `funnelSvg` **[trapezoid + right labels in code]** but 6 bands, mixed blue/teal/green, 5px gaps, 16% min-width floor, 12.5px values | recolor to `--warm-1..4` ramp (6 stops: interpolate `#F4553C #E04D3B #C44538 #A63E36 #8F3B34 #7E3A33`), gap 3px, floor 10%, segH 52, value 14px, `filter:drop-shadow(0 1px 2px rgba(0,0,0,.15))` |
| Scatter | "CPA vs. Conversion-Rate": bubbles (rings) classed 4 colors — green Top Performer / orange Expensive-but-Effective / red Need for Action / slate Low Cost Low Effect; average crosshair lines + "Average" tag; legend top-corner squares 10px + 12px labels; axes % and $ ticks 11px grey | **absent** | new chart (spec below) |
| Row 3 layout | 3 cards: col-chart Age ~25% · col-chart Gender ~25% · treemap Location ~45% | one combined «الحجم والقطاع» card + treemap in the flow | 3 cards `grid-template-columns:1fr 1fr 1.4fr` |
| Column charts | title "# Conversion by Age Group" 13px 700 grey; maroon `#A63E36` flat bars (w≈56, r≈2), value ON TOP 12px 700 `#333`, x labels 11px grey, baseline hairline | `colChart` similar skeleton but 46px teal/navy rounded-7 bars, two charts crammed in one card | split cards: «التوزيع حسب الحجم» + «التوزيع حسب القطاع»; bars `--warm-3`, radius 2, width 56, height 150, values 12px 700 |
| Treemap | proportional 2-row grid, ~2px gaps, radius 0–2, sequential ramp **dark→light by rank**, tiles: name 12px 700 top + value 12px under; **light tiles switch to dark text** | `treemapTiles`: flex-wrap, 6px gaps, r10, fixed tone by index, always white text, min-h 74 | grid rows, gap 2, r2, rank-ramp `#8A4A40 #9E5A4E #B2705F #C08876 #CFA090 #DDB8AA #E8CCC1 #F0DDD5`, text auto: ranks 0–3 white / 4+ `#5B3A33`; fill card height ≈260px |
| Card titles | 13px 700 `#666` top-right(LTR left) + no sub | h3 14px + tiny sub right | ✔ keep, add kicker option |

### (b) BUILD SPEC

1. **KPI row** (replace lines 523–528 + `ratesStrip` call): 6 `.kpi` cards, `grid-template-columns:repeat(6,1fr)` (wraps ≤1100px to 3+3). `.kpi .v{font-size:28px}` `.kpi{padding:24px 16px; min-height:118px}`. Values: `realCampaigns.length`, `entities.length`, `pct(delivered,sent)٪`, `pct(seen,delivered)٪`, `pct(replied,delivered)٪`, `pct(interested,replied)٪`. Rates get NO per-card accent colors — neutral `--ink` (Tableau is monochrome); delete `ratesStrip` (961–973).
2. **Actions row** («+ إنشاء حملة» etc.) moves under pagehead, above KPIs.
3. **Analytics grid A**: `<div style="display:grid;grid-template-columns:5fr 7fr;gap:16px;">` — funnel card + scatter card; both `min-height:420px`. (≤980px: 1 column.)
4. **Funnel recolor** (`funnelSvg` 974–990): `fills = ["#F4553C","#E04D3B","#C44538","#A63E36","#8F3B34","#7E3A33"]` (replace `fills` line 275 usage for funnel only); `segH=52, gap=3`, floor `0.10`, value `font-size 14`, add `<polygon … style="filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.18))">`; label column: `height:52px; font-size:13px; font-weight:700; color:#3b4657;`.
5. **NEW `scatterSvg(campaigns)`** — «المشاهدة مقابل الردود لكل حملة»:
   - x = read-rate %, y = reply-rate %, r = `6 + sqrt(audience)` capped 16; `fill:none; stroke-width:2.5` rings (Tableau look).
   - class colors: both ≥ avg → `#2E7D32` «أداء عالٍ»; x≥avg,y<avg → `#F59E0B` «وصول بلا ردود»; x<avg,y<avg → `#C62828` «بحاجة لتدخّل»; else `#64748B` «هادئة».
   - avg crosshair: `stroke:#C7CDD6 1px` + grey tag «المتوسط» 10.5px.
   - legend top-inline-end inside card: rows of 10px squares + 12px labels.
   - axes: 11px `#98A2B3` ticks every 25%; plot border `1px #E3E7EE`. `dir="ltr"` svg wrapper like `funnelSvg`.
   - Until ≥4 campaigns exist, show alongside a هادئ empty hint (keeps layout).
6. **Analytics grid B**: `grid-template-columns:1fr 1fr 1.4fr` → `chartCard("التوزيع حسب الحجم", …, colChart(sizeRows,"var(--warm-3)"))` · same for القطاع · treemap card «المستهدفون حسب المدينة».
7. **`colChart` restyle** (991–997): bar `max-width:56px; border-radius:2px; background:#A63E36;` height map to 150px; value `font-size:12px;font-weight:700;color:#333;` label `font-size:11px;color:#6B7280;`; add baseline `border-bottom:1px solid #E9EDF3` on the flex container.
8. **`treemapTiles` rewrite** (999–1005): squarified-lite = two rows (`display:grid; grid-auto-flow:column` per row, widths = value share of row total), container `height:260px; gap:2px; border-radius:4px; overflow:hidden;` tile `border-radius:2px; padding:10px 12px;` ramp + text-color rule from table above; name 12px 700, value 12px under it.
9. **`dailyActivitySvg`** keeps its slot? Reference has no equivalent — move «نشاط الرسائل» below grid B full-width (it's ours, useful; don't delete).

---

## 3 · Ref 14 — CXP prediction cards ↔ «ملف العميل ٣٦٠» header + «فهم المساعد» (`vCustomer` 1077)

The reference's vivid indigo page-gradient is marketing-site dressing — do NOT copy to app chrome. Copy the **card anatomy**.

### (a) Gap table

| Element | CXP reference (exact) | Ours (`actual-profile`) | Gap |
|---|---|---|---|
| Stage tab | folder-tab pill riding the card's top edge: "MONTH 1" ~12px 700 uppercase, white bg, top-radius 12, sits −14px above card | tiny `تجريبي` chip beside the name | folder-tab «المرحلة: جديد / متفاعل / جاد» on header card |
| Avatar | 52px **circle**, blue gradient (`#4F46E5→#2563EB`), white letter 22px | 52px rounded-**square** r14 navy `#13294b`, teal letter | circle + gradient `linear-gradient(135deg,#2F5F94,#3FB6B0)`, white letter |
| Name / sub | 21–22px 700 near-black; sub 15px grey `Customer since 2026 · Amsterdam · €1,840 LTV` | 18px 700 navy; meta scattered over 3 small lines | name 21px `--ink`; ONE meta line 13.5px `--ink-3`: `عميل منذ ١١ أغسطس · الدمام · ١٢ رسالة` |
| Fact rows | icon-tile rows: 36px r10 pastel tile w/ colored glyph + **bold label** + ` — ` light detail, 15px, ~18px stack gap | attr **chips** row | 3 icon-tile rows: 👥 الحجم — صغير · 🏥 القطاع — clicnic · 💬 القناة — واتساب ✓ (tiles `#EFF4FB`,`#E9F7F6`,`#ECFDF3`; glyph colored) |
| Predictions panel | tinted lavender `#EDE9FE` r16 panel, header ✦ + "CXP Predictions" 17px 700 violet; interior = **WHITE sub-cards** | teal-tint `#F4FBFA` card, all free text | panel `--accent-tint` bg `--accent-border` border; header `⁂ فهم المساعد` 15px 700 `--accent-strong`; content promoted to white sub-cards ↓ |
| Metric grid | 2×2 white cards r12 p12: tiny icon-dot 22px + 2-line 11.5px 700 label + big value (82% green 20px / 18% dark / "Email" violet / "Send" violet) | none (prose) | 2×2: **نية الشراء** (مرتفعة/متوسطة/منخفضة — green/amber/grey 18px 700) · **التجاوب** (ردّ خلال س) · **القناة المفضلة** «واتساب» accent · **الخطوة التالية** (verb from `ins.next_action`, accent) |
| Recommendation card | full-width white sub-card: kicker "HALO RECOMMENDATION" 9.5px 700 violet + "Best moment to engage: **tomorrow 09:00–11:00**" 14px | «الخطوة التالية» box exists (accent-border box) **[partial in code]** | restyle: white sub-card, kicker `توصية المساعد` 10px 700 accent, body 13.5px w/ `ins.best_time` **bold** |
| Context rail | at card's outer edge: **top** big % 18px 700 indigo → vertical 8px track (full panel height, grey `#EDEFF3`, blue fill bottom-up, r999) → rotated caption "CONTEXT" 11px grey letter-spaced | inside header, 110px track, % top ✔ but label unrotated below, squeezed | move to header-card inline-end edge column, full card height (~180px), fill `linear-gradient(180deg,#3FB6B0,#2E7D77)`, caption rotated `writing-mode:vertical-rl; transform:rotate(180deg)` text «السياق» 10px 700 `--ink-4` |
| Learning state | Month-1 panel: italic grey "Learning…" + dot | `ins.learning` prose **[in code]** | style italic + pulsing dot to match |

### (b) BUILD SPEC (rewrite header card + فهم المساعد blocks, lines 1089–1129)

```html
<div class="card hdr360" style="position:relative; padding:28px; display:flex; gap:20px;">
  <span class="foldtab">المرحلة: جاد</span>                      <!-- position:absolute; top:-13px; inset-inline-start:24px;
        background:#fff; border:1px solid var(--line); border-bottom:none; border-radius:10px 10px 0 0;
        padding:5px 16px; font-size:11px; font-weight:700; color:var(--ink-2); box-shadow:var(--sh-card); -->
  <div class="av360">م</div>                                     <!-- 52px; border-radius:999px;
        background:linear-gradient(135deg,#2F5F94,#3FB6B0); color:#fff; font-size:22px; font-weight:700; -->
  <div style="flex:1;min-width:0;">
    <div style="font-size:21px;font-weight:700;color:var(--ink);">مجمع عبدالعزيز الطبي <span class="chip">تجريبي</span></div>
    <div style="font-size:13.5px;color:var(--ink-3);margin-top:4px;">عميل منذ ١١ أغسطس · الدمام · ‎+966559402621</div>
    <div class="factcol">                                        <!-- margin-top:16px; display:flex; flex-direction:column; gap:12px; -->
      <div class="fact"><span class="ftile" style="background:#EFF4FB;color:#2F5F94">👥</span><b>الحجم</b><span> — صغير</span></div>
      <div class="fact"><span class="ftile" style="background:#E9F7F6;color:#2E7D77">🏥</span><b>القطاع</b><span> — clicnic</span></div>
      <div class="fact"><span class="ftile" style="background:#ECFDF3;color:#12B76A">💬</span><b>آخر تفاعل</b><span> — شوهدت ٨:٣٦م</span></div>
    </div>                                                       <!-- .ftile: 36px; border-radius:10px; display:grid; place-items:center; font-size:16px;
                                                                      .fact: font-size:14px; b = --ink 700; span = --ink-3 -->
  </div>
  <div class="ctxrail">                                          <!-- flex:none; display:flex; flex-direction:column; align-items:center; gap:8px; -->
    <b style="font-size:18px;color:var(--accent-strong)">92%</b>
    <div class="track"><i style="height:92%"></i></div>          <!-- track: width:8px; flex:1; min-height:140px; background:#EDEFF3;
                                                                      border-radius:999px; position:relative;
                                                                      i: absolute bottom; background:linear-gradient(180deg,#3FB6B0,#2E7D77); border-radius:999px; -->
    <span class="vlab">السياق</span>                              <!-- writing-mode:vertical-rl; transform:rotate(180deg); font-size:10px; font-weight:700; color:var(--ink-4); -->
  </div>
</div>
```
Stage rule: جديد = no reply · متفاعل = replied · جاد = `interestedOf()` true.

فهم المساعد panel:
```html
<div class="predpanel">   <!-- background:var(--accent-tint); border:1px solid var(--accent-border); border-radius:16px; padding:18px; -->
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <h3 style="margin:0;font-size:15px;color:var(--accent-strong);">⁂ فهم المساعد</h3> [intent badge — keep toneBadge]
  </div>
  <div class="pgrid">     <!-- margin-top:14px; display:grid; grid-template-columns:1fr 1fr; gap:10px; -->
    <div class="pcell">…</div> ×4
  </div>                  <!-- .pcell: background:#fff; border-radius:12px; padding:12px 14px; box-shadow:0 1px 2px rgba(16,24,40,.05);
                               inside: 22px icon-dot (tinted circle) + label 11.5px 700 --ink-2 (2 lines ok) + value 18px 700 colored -->
  <div class="pcell" style="grid-column:1/-1; margin-top:10px;">
    <div class="kicker acc">توصية المساعد</div>
    أفضل لحظة للتواصل: <b>صباح يوم العمل التالي، بين ١١:٠٠ص و٢:٠٠م</b>
  </div>
  <!-- إشارات الشراء quotes stay below as today [in code] -->
</div>
```
Prose summary (`ins.summary`) stays as one 13.5px line ABOVE the grid. `ins.learning` state: `<i style="color:var(--ink-4)">يتعلّم…</i>` + 8px dot with `animation:pulse 1.6s infinite`.

---

## 4 · Ref 15 — HALO customer-360 ↔ «سجل التفاعل» + convo drawer (`vCustomer` timeline 1131–1139, `renderConvo` 355)

### (a) Gap table

| Element | HALO reference (exact) | Ours | Gap |
|---|---|---|---|
| Snapshot stats | tiny uppercase labels 9px 700 grey (`LIFETIME VALUE`, `ORDERS`, `REACHABLE ON`) + big values (€2,840 17px 700; 17) + channel icon row (WhatsApp/mail/IG outline 18px) | none — meta prose only | add 3 stat blocks to header card left column: **الرسائل** ١٢ · **الردود** ٥ · **الحملات** ٢ + «متاح عبر» + WhatsApp glyph (kicker 9.5px + value 17px 700) |
| Timeline meta | each item: colored kicker FIRST `2H AGO · WHATSAPP` 9.5px 700 (violet for active ch., grey else), then title 12px 700 dark, then detail 10.5px grey | title first 12px regular, grey meta UNDER, dot only | reorder: kicker (channel+time) → bold title → detail |
| Timeline rail | continuous 2px `#E4E0F5` vertical line; markers 16px: ◎ ring (violet 2px) for events, ● solid violet w/ white ✓ for done, ◌ **dashed** ring for predicted | disconnected 9px solid dots, color-coded | connected rail + 3 marker states |
| Highlight row | middle entry violet-tint bg + border (next best action `MARKETING · THIS THURSDAY`), mail icon right, `87% prediction confidence` grey under | none | when `ins.next_action` exists, inject synthetic first row: accent-tint band `#E9F7F6`, border `--accent-border`, kicker `الخطوة التالية · هذا الأسبوع`, + «ثقة القراءة مرتفعة» 10.5px |
| Predicted row | dashed 1.5px border row + dashed spinner marker + expected value `+€48 expected basket` | none | `ins.best_time` → dashed row «متوقَّع · الأسبوع القادم» |
| Inter-item caption | `↓ FED INTO PROFILE · "FIT-SENSITIVE BUYER"` 9px 700 violet between rows | none | when a وسم tag event follows a message: caption `↓ أُضيف للملف · «مهتم بالإجازات المرضية»` 10px 700 accent |
| Row end icon | channel glyph per row (WhatsApp/mail outline, grey 16px) inline-end | none | add 💬 (grey 15px) for wa events, 📎 file, 📣 campaign |
| Chat frame (col 2) | AI reply = tinted violet panel labeled `HALO · 09:14` 9.5px 700; customer grey bubbles; footer bar: ✅ `Resolved by HALO` 12px 700 + right grey `No agent · 3 tools called · 0.4s` | WhatsApp-green drawer, no resolution meta | keep WA styling (product truth) BUT add drawer footer meta-bar when `!c.human`: `✓ يدير المحادثة: المساعد` green 12px 700 · end: `بلا تدخّل بشري · ردّ خلال ~٣ث` grey 11px |

### (b) BUILD SPEC — timeline rewrite

```css
.tl{ position:relative; padding-inline-start:26px; }
.tl:before{ content:""; position:absolute; inset-inline-start:7px; top:8px; bottom:8px; width:2px; background:#E3EAF2; }
.tlrow{ position:relative; padding:10px 12px; margin-bottom:6px; border-radius:12px; }
.tlrow .mk{ position:absolute; inset-inline-start:-26px; top:12px; width:16px; height:16px; border-radius:999px;
            background:#fff; border:2px solid var(--navy-2); }          /* ◎ default */
.tlrow.done .mk{ background:var(--accent); border-color:var(--accent); color:#fff; }  /* ● ✓ 9px centered */
.tlrow.pred  .mk{ border-style:dashed; border-color:#9DB4CE; }
.tlrow.next{ background:var(--accent-tint); border:1px solid var(--accent-border); }
.tlrow.pred{ border:1.5px dashed #C6D2E0; }
.tl .kick{ font-size:10px; font-weight:700; color:var(--ink-4); }
.tl .kick.ch-wa{ color:var(--accent-strong); }  .tl .kick.ch-camp{ color:var(--navy-2); }
.tl .t1{ font-size:12.5px; font-weight:700; color:var(--ink); margin-top:2px; }
.tl .t2{ font-size:11px; color:var(--ink-3); margin-top:2px; }
.tl .endic{ position:absolute; inset-inline-end:10px; top:12px; font-size:15px; color:#B6BFCC; }
.tlcap{ font-size:10px; font-weight:700; color:var(--accent-strong); padding:2px 12px 8px; }
```
Row DOM: `<div class="tlrow [next|done|pred]"><span class="mk"></span><div class="kick ch-wa">قبل ساعتين · واتساب</div><div class="t1">«أبغى أعرف أسعار الإجازات المرضية»</div><div class="t2">حالة التسليم: شوهدت</div><span class="endic">💬</span></div>`
Kicker time: relative («قبل ساعتين», «أمس», else `fmtD`). Order: synthetic **next** row (from `ins`) → real events (latest 2 = `done`) → trailing **pred** row from `ins.best_time`.

Header stat blocks (goes in the header card, start column, under fact rows or beside):
`<div style="display:flex;gap:22px;margin-top:16px;"> <div><div class="kicker">الرسائل</div><b style="font-size:17px">12</b></div> …الردود …الحملات <div><div class="kicker">متاح عبر</div><span style="font-size:16px">💬</span></div> </div>`

Convo drawer footer (in `renderConvo`, before `.ft`): meta-bar `display:flex;justify-content:space-between;padding:8px 18px;background:#F8FAF9;border-top:1px solid var(--line-soft);font-size:11px;` — start `✓ يدير المحادثة: المساعد` (`color:#12B76A;font-weight:700`), end `بلا تدخّل بشري` (`--ink-4`); when `c.human`: start `⏸ المحادثة بيد البشر` amber.

---

## 5 · Ref 13 — WhatsApp single-message (note + one UI task)

**Server-side: FIXED** — opener text + PDF now go as ONE document-with-caption message (no action).
**Remaining UI parity** in the wizard preview (`vAimkt` lines 712–719): today the PDF row renders as a separate block ABOVE the `.b` bubble → visually still "two messages", contradicting the caption «رسالة واحدة: الملف مضمّن». Fix: move the doc row INSIDE `.b`:
```html
<div class="b">
  <div class="doc">…PDF badge 30×36 + filename ltr…</div>   <!-- background:rgba(255,255,255,.55); border-radius:8px; padding:8px 10px; margin-bottom:8px; -->
  نص الرسالة…
  <div class="t">الآن ✓✓</div>                               <!-- time moves inside bubble, bottom-left -->
</div>
<!-- CTA buttons: attach to bubble — margin-top:2px; each row background:#fff; first row radius 4 4 12 12?
     WhatsApp renders buttons as attached rows separated by hairlines: give the bubble border-radius 12 12 4 4
     and buttons 0 0 / last 4 4 12 12, gap:1px, color #2F5F94 700 -->
```
QA gate: next sandbox send → screenshot must show ONE bubble (doc header + caption + buttons attached).

---

## 6 · Real-data constraint map (references → Massar)

| Reference slot | We don't have | Render instead (all live today) |
|---|---|---|
| Revenue column / Total Costs / €LTV | money | «مهتمون» count; profile stat = counts (الرسائل/الردود/الحملات) |
| CTR / CPC / CPA | ad economics | نسبة الوصول (delivered/sent) · نسبة المشاهدة (read/delivered) · نسبة الردود (replied/delivered) · نسبة الاهتمام (interested/replied) |
| CPA-vs-Conversion scatter | cost axis | مشاهدة٪ (x) vs ردود٪ (y) per campaign, bubble = audience |
| Age Group / Gender columns | demographics | «الحجم» and «القطاع» from imported file columns (already derived in `vHomeCharts`) |
| Location treemap | — | المدينة column ✔ (exists) |
| Churn risk % | churn model | slot filled by «التجاوب» metric until model exists |
| Open/Click table cols | email metrics | مشاهدة٪ / ردود٪ (delivery-receipt truth — footer note already says so) |

---

## 7 · Implementation order (one file: `src/dashboard.ts`)

1. Token block + control scale-up (§0) — 30 min, touches every screen at once.
2. Campaigns list anatomy (§1 steps 1–13) — the founder's most-viewed screen, largest delta.
3. Propagate table anatomy to «قائمة المستهدفين» (§1 tail).
4. Home: merge KPI strip, explicit 2-row analytics grid, funnel recolor, colChart/treemap restyle (§2: 1,3,4,6,7,8).
5. New `scatterSvg` (§2.5).
6. Profile header card + context rail + folder tab + fact rows + stat blocks (§3).
7. فهم المساعد → tinted panel + white 2×2 metric sub-cards + recommendation card (§3).
8. Timeline rewrite + convo resolution bar (§4).
9. Wizard single-bubble preview (§5).
10. `npm run build` → deploy → screenshot the 4 screens at 1440×900 → diff against refs; gate ≥90%.

Safety: pure UI; no send paths touched; opt-out & token auth untouched.
