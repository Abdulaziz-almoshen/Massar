# Design plan — Frappe CRM list + record UX on the campaigns module (RTL)

Cycle `campaigns-crm` · `[designer]` · gate **B** (Massar style already approved: `DESIGN.md` +
`massar-design-language.md`). Read: *a system of record for one operator who must hand a rep a named
list today.* Dials: variance 3 · motion 2 · density 8. `taste_skill_scope: excluded` (operational
product UI — no marketing-layout or cinematic-motion recipes). Palette is Massar's; only Frappe's
**patterns** are ported (user-model Rule 3). Every count renders through `fmtN()` (ar-SA).

Detail-pane compositions compared: `A` Frappe rail mirrored to the left · `B` full-width tabs + spec
strip · **`C` = B with the hero and spec strip page-level, tabs below ← chosen**. `A` is dead on the
field census (§2.0). Capture C as an openable HTML prototype before Builder starts; QA baseline =
that prototype at 375×812 · 768×1024 · 1440×900, routes `#kmon` and `#kmon/<id>`.

---

## 1 · The list screen (`#kmon`)

### 1.1 Control bar — one bar, not two

Today's `.ptab` row and the `.ttoolbar` inside `.tblwrap` are **merged**; nothing is duplicated,
everything moves. Order, RTL (start = right → end = left):

`[بحث pill, 320px, .inp h=42 radius 999]` · `[segmented view toggle: قائمة | تجميع | كانبان]` ·
`[quick-filter pills: الكل · فعلية · تجريبية]` · `flex:1` · `[1px×22 hairline #EAECF0]` ·
`[الترتيب: الأحدث ▾]` · `[context control]` · `[تحديث]` · `[.cntpill ٦ حملة]`

The quick-filter pills are today's `.ptab`s, unchanged in behaviour — they are Frappe's quick
filters and they are keyed on the one real boolean, `camp.test`. **Context control** swaps with the
view type: `الأعمدة` (قائمة) / `التجميع حسب: الخدمة ▾` (تجميع) / `إعدادات اللوحة` (كانبان).
The `ptitle` band above keeps تصدير CSV (ghost) + إنشاء حملة (dark) — Frappe's one-solid-Create rule.

≤900px: bar wraps to two rows — row 1 search full-width, row 2 view toggle + `⋯` overflow holding
sort/columns/refresh. The pill strip is its own `.ms-scroll` (`overflow-x:auto`, masked edges), so it
never produces page scroll. `inset-inline`/`padding-inline` only; no `left`/`right`.

### 1.2 View types — keyed on fields that exist

There is no stage, owner, value or close date. Keys are therefore:

| Key | Backed by | Columns | Drag |
|---|---|---|---|
| **التصنيف** (kanban default) | `camp.test` | فعلية · تجريبية | **Yes** — drop calls the existing `setCampClass` (`POST /admin/campaign/test`), the one writable field, with its existing `alertBar` copy |
| **الخدمة** | `camp.product` | one per distinct product + «بلا خدمة» | No — immutable after launch; header carries «تُحدَّد عند الإطلاق» and no drop zones render |
| **شهر الإطلاق** (تجميع only) | `camp.created_at` | one per month, newest first | n/a |
| **حالة الأداء** | derived by `campStats`, identically to today's row chip (تجريبية / جارية / مكتملة) | 3 | No — header reads «محسوبة من أرقام التسليم» so it is never read as a stage |

Kanban card = name · `fmtD(created_at)` · product chip · الجمهور / مشاهدة٪ / ردود٪ · the existing
6px progress bar. Group headers: label + count pill + chevron at inline-end; a zero option renders
**collapsed with ٠, never hidden** — a missing group is a fact.

### 1.3 Selection + bulk bar

40px checkbox cell at inline-start of `.thead`/`.trow`; `opacity:0` until row hover/focus-within,
always visible on coarse pointers and whenever anything is selected; `event.stopPropagation()`
(rows navigate on click). Shift-click selects a range. Selected row: `#F4F6FA` +
`box-shadow: inset 3px 0 0 #1F7A73` (inline-start). Changing tab/search/view **clears** selection
with one line: «أُلغي تحديد ٧ عند تغيير التصفية» — a hidden selection must never reach a bulk action.

Bulk bar: fixed, `inset-block-end:18px; inset-inline:0; justify-content:center`, ink `#101828` pill,
`max-width:92vw`, wraps at 375. RTL order: `[٣ محدَّدة]` · تصدير المحدد CSV · نقل إلى التجريبية /
إعادة إلى الفعلية (mixed selection ⇒ two buttons, each with its own count) · دمج جماهير المحدد في
شريحة (stages the union of `targets[]` into the wizard — §8 human gate, never a send) · `✕`.

---

## 2 · The detail screen (`#kmon/<id>`)

### 2.0 The rail is deleted, and why

Field census: the campaign has six fields; the header already renders four; `targets[]` is already
the table and a stat card. **One** substantive field is unrendered: `camp.message`. Discovery's
threshold was ≥5. A four-section rail would restate the header and make an immutable past event look
editable. Dropped. The 344px goes to the targets table.

### 2.1 Page-level, above the tabs (never hidden)

1. `→ كل الحملات` · title · `product · واتساب · date` · status chip · actions.
2. **حكم الحملة** hero — unchanged navy gradient, verdict sentence + the three rates.
3. **شريط الإطلاق** — new, full-width, `#F9FAFB` + `#EAECF0` hairline, radius 13. Left/start: the
   sent text in the WhatsApp bubble idiom (`#DCF8C6`, wallpaper `#E5DDD4`), clamped to two lines
   with «عرض النص كاملًا». Right/end: three inline facts — الخدمة · حجم الجمهور · التصنيف. Footer
   line, `11px #98A2B3`: «هذا نصّ ما أُرسل فعليًا. لا يقبل التعديل بعد الإطلاق.» Read-only styling is
   the point: no input borders, no pencils, no hover affordance.

### 2.2 Tabs (3, and we refuse to pad to Frappe's 10)

- **جهات الاستهداف (٤٠)** — default. Today's six filter chips + search + the table, now full width,
  with §1.3 selection.
- **الأداء** — the six `.statc` cards + `%` bars + the honest «شوهدت = قُرئت ∪ ردّت» note.
- **الخطوة التالية (٣)** — today's move cards, count in the tab label. Each card gets one action that
  switches to tab 1 **with its filter applied and its rows pre-selected**, closing the loop.

Nothing is lost: the hero is page-level; the moves count is on the tab; tab 1's chips already carry
seen/replied/interested/silent/failed, so only `sent` and `delivered` live solely in الأداء.

### 2.3 Detail bulk bar

`[١٢ محدَّدة]` · **إعادة استهداف المحدد (١٢)** (teal primary — replaces `startRetarget()`'s
whole-filter `lastDetailCohort` with the explicit subset) · تصدير المحدد CSV · `✕`.
«حفظ كشريحة» is **not** shown: no segments table exists; the retarget staging is its honest stand-in.

---

## 3 · Empty · sparse · one-item

- No campaigns → today's `.empty`, in every view type (kanban shows no phantom columns).
- تجميع, one non-empty group → group renders plus `.sparse`: «كل الحملات في مجموعة واحدة — التجميع
  لا يضيف شيئًا هنا.» + «→ عد إلى القائمة». No qualifying field (every field single-valued) → the
  تجميع toggle is disabled with «لا يوجد حقل يفرّق بين الحملات الحالية».
- كانبان, one card → the empty column is a dashed drop zone: «اسحب حملة هنا لإخراجها من أرقام الأداء».
- Exactly one campaign → the sort control is **hidden**; a control that cannot move is worse than none
  (same rule that killed the fake pager).
- Nothing selected → no bar at all (never a disabled bar). All visible selected **and** `LIST_CAP`
  truncated → «كل الـ ٦٠ المعروضة محدَّدة — تُعرض ٦٠ من ٨٤، والباقي غير مشمول.»
- `camp.message` null (pre-ledger launch) → «لم يُحفظ نص هذه الحملة.» in `#98A2B3`. Never a
  reconstructed body. `product` null → «غير محددة».
- No moves → tab label has no count and the panel reads «لا توصية الآن: لم يُسجَّل حدث بعد الإطلاق.»

## 4 · Deliberately not ported

Right-hand field rail (§2.0 census) · Create modal for campaigns (creation is a gated wizard; a
one-click Create that can blast is the worst port available) · assignment, owner, `_assign` avatars,
@mentions, roles (one operator) · Tasks/Notes/Emails/Calls/Attachments tabs (no such records) ·
`WhatsAppBox` composer (a send affordance under the standing NO-SEND rule) · doc-id/naming-series row
· `_liked_by` heart, column resize, saved public views, custom-field admin (ceremony for six fields)
· Frappe's palette, Espresso chrome and iconography — pattern only.
