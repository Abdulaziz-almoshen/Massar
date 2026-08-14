# Massar Design Language — domain skill (dashboard / UI work)

Load for any Massar UI work (the upcoming Next.js dashboard, artifacts, mockups). The
prototype **is the spec** — match it, don't reinvent it.

## 1. Sources of truth
- `_مسار/مسار.dc.html` — the full interactive prototype (sidebar, dashboards, customers,
  opportunities, pipeline, marketing module). Marketing screens: `aimkt` (campaign wizard),
  `kmon` (campaign command center + funnel), `kb` (معرفة المنتج editor), `partners`.
- `_مسار/uploads/` — design brief (`موجز-تصميم-نظام-المبيعات.md`), stage reference, campaign
  mockup PNGs. Architecture doc §8 defines the campaign tracker UI contract.

## 2. Fundamentals
- **Arabic-first, full RTL** (`dir="rtl"`), font **IBM Plex Sans Arabic** (400/500/600/700;
  Google Fonts). Numbers formatted `toLocaleString('en-US')` (Western digits) per prototype.
- Light, flat, institutional: white surfaces on `#eef0f4` ground, 1px `#e3e7ee` borders,
  border-radius 14px cards / 999px chips, no heavy shadows.

## 3. Palette (from the prototype — reuse exactly)
- Navy ink `#13294b` · deep navy surfaces `#1F4470` (hero/panels) · sidebar gradient
  `#2F5F94 → #1F4470`.
- Teal accent `#3FB6B0`, dark teal `#2E8F89`, accent-ink `#2E7D77`, accent-soft `#DCF1EF`.
- Muted text `#5b6678` / `#7b8597` / `#9aa4b4`; hairlines `#eceff4`/`#f3f5f8`.
- Semantic: ok `#1f8a52` on `#E6F4EC` · warn `#b5810f` on `#FBF2DD` · bad `#c43d3d` on
  `#FBE9E9` · info `#2F5F94` on `#E3ECF8`.
- Achievement coloring rule: ≥70% green · 50–69% amber · <50% red (used everywhere).

## 4. Component idioms
- KPI card: small muted label above, 28–30px/800 number, unit in 12px muted.
- Status chip: 11px/700, pill, tinted bg + colored dot. State machine chips (campaign):
  مسودة grey · مجدولة blue · جارية green · متوقفة amber · تحتاج تدخل red · مكتملة slate.
- Funnel bars: label + count/pct row, 9px rounded track `#eef0f4`, fill colored by depth
  (navy → teal → green).
- WhatsApp preview: wallpaper `#E5DDD4`, outgoing bubble `#DCF8C6` with 3px top-start
  radius notch, 12–13px text, line-height 2.
- Tables: uppercase-ish 11.5px/700 muted headers on `#f6f8fb`, 1px row hairlines, hover
  `#fafbfd`; wide tables scroll inside their own container.
- Sidebar nav: grouped labels (نظرة عامة · دورة البيع · التسويق · التخطيط والأداء ·
  المنشأة), active item = white text + teal dot.

## 5. Marketing-module UI contracts (build to these)
- Campaign wizard = 4 numbered steps (product w/ readiness score & gaps → audience chips
  w/ live count → timing → message preview + approve) + sticky ملخّص الحملة card + launch
  button that stays disabled until product+audience+message are approved.
- Campaign detail = funnel (targeted→sent→read→replied→interested→qualified→meetings→sales)
  + contact table (WhatsApp name, status chips, tag chips, last message, transcript drawer,
  takeover button) + honest "seen = read ∪ replied" tooltip.
- Every filtered contact view gets one primary action: **حفظ كشريحة** (save as audience).

## 6. Voice
Formal-friendly Saudi business Arabic (فصحى مبسطة). Short labels, verb-first buttons
(اعتماد، إطلاق، حفظ كشريحة). No Latin jargon in UI copy where an Arabic term exists.
