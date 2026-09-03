# Audience slice — file-based onboarding + column-derived segment launch
2026-08-11 · request R18: "onboarding users should be through file, then this file can be
segmented — when I launch I choose segments or by names or by city etc. Current flow is not ok."

## Discovery (product-discovery)
Real goal: onboard target lists the way they actually exist in Lean's world — Excel/CSV
exports (CRM dumps, hand-built clinic lists). Paste-import loses structure and can't scale
past a handful of rows. Segmentation must derive from the FILE'S OWN COLUMNS so any list
works with zero configuration ("by city … etc" = arbitrary columns, not just the two we
hardcoded). Right bet: yes — this is the audience foundation every real launch depends on.
Anti-overbuild guard: no saved-segments engine (Klaviyo-style) — filter-at-launch from
column values is exactly what he described. Load-bearing insight: entities need a
schemaless `attrs` store; without it this is just a re-skinned paste flow.

## Business rules (business-analyst)
- Accept .xlsx/.xls/.csv (≤25MB, first sheet, header row required, row cap 5,000).
- Auto-map headers — name: اسم/الاسم/الجهة/جهة/العميل/الشركة/name/company/entity;
  phone: جوال/الجوال/هاتف/الهاتف/رقم/phone/mobile/whatsapp. All other non-empty columns
  → attributes (key = trimmed header). Detected mapping echoed in the import summary.
- KSA phone normalization: strip non-digits; 05XXXXXXXX→966XXXXXXXXX; 5XXXXXXXX(9)→966…;
  ≥8 digits otherwise kept as-is; else row skipped with reason.
- Dedupe = upsert by phone (update name, merge attrs). Report {added, updated, skipped[], columns}.
- Launch unchanged: cap 50, opted-out skip, confirm modal, real-customer sends human-gated.
- Picker: chip group per attribute key (≤6 keys by coverage, ≤12 values by count, counts shown);
  OR within a key, AND across keys; composable with name/phone search; checkboxes override;
  "select matching" honors active filter; live selected count.
- Acceptance: AC1 real Arabic xlsx w/ extra columns → entities + dynamic columns visible;
  AC2 re-import → updated not duplicated; AC3 chips derived w/ counts; AC4 combined
  city+size filter → correct count → select-matching → modal n correct; AC5 bad rows
  skipped w/ reasons; AC6 05-numbers normalized; AC7 401 w/o token; AC8 build+gate green,
  3-viewport pixels, 0 console errors.

## Prior art (market-researcher)
Mailchimp (CSV → column map → merge fields; segments = field conditions), Klaviyo
(profile properties → segments w/ LIVE COUNTS — the trust device), HubSpot lists,
Intercom auto-detected attributes. Distilled for MVP scale: skip the manual mapping
screen (auto-detect + echo the mapping — Arabic lists are consistent; mistakes stay
visible), schemaless attributes, VALUE CHIPS not a condition builder (right for ≤5k
contacts), counts on every chip. Reuse: SheetJS `xlsx` for parsing (xlsx/xls/csv, Arabic
safe, no native deps) — never hand-roll CSV (quoting/BOM/RTL pitfalls).

## Plan (planner)
1. db.ts: entities + `attrs JSONB DEFAULT '{}'`; addEntities merges attrs on phone
   conflict; listEntities merges legacy size/city into attrs for a uniform UI read.
2. `npm i xlsx`; index.ts: POST /admin/entities/import (multipart) → parse → map →
   normalize → upsert → report. Paste endpoint stays (secondary quick-add).
3. dashboard.ts العملاء: file dropzone primary + import summary (added/updated/skipped/
   columns) + dynamic attr columns (top 3 by coverage @1440, hidden ≤900) + delete;
   paste demoted to a collapsed secondary card.
4. dashboard.ts wizard step-2: data-driven chip groups (replace hardcoded segments);
   search/checkboxes/select-matching/live count preserved.
5. Fold round-6 next-touch orders (same file): convoSig += statusTimes+tags; setHuman
   res.ok check; remove duplicate window.pick.
6. Prove: build + node --check → deploy → generate REAL Arabic xlsx (clinics w/ المدينة/
   الحجم/القطاع) → import via API → real-browser QA + 3-viewport pixels → evidence →
   gate @commit → CPO round-7 → reporter.
Safety scope: import is data-in only; no send-path changes; sandbox self-test only.

## Design treatment (designer — massar-design-language)
Dropzone: dashed 2px border card, tint bg, icon + «اسحب ملف Excel أو CSV هنا أو اضغط
للاختيار», helper line naming auto-detected columns. Import summary via alertBar idiom +
«الأعمدة المكتشفة: …». Chip groups: existing chip idiom + count badge; group label =
small muted key. Dynamic columns: prototype table idiom; mobile keeps name+phone+chips.
