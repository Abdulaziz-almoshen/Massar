# Massar–Frappe shell (cycle V2)

Extends V1 (`frappe-visual-system.md`) + `DESIGN.md`; V1 tokens stay live. V2 adds four surfaces and
**overturns one V1 decision** on founder instruction. V1 §7 correctness invariants carry forward
unchanged and are not restated.

## 0. The overturned decision — DESIGN.md amendment

V1 §3 kept the navy/gold sidebar as "264px of permanent brand". The screenshot is **light**.

**Amend invariant 3's final clause:** «gold `#C9A227` and the navy gradient are sidebar-only» →
**both retired from the product.** With no dark surface left they have no legal home, and leaving
them defined invites reintroduction.

**What survives as Massar:** the **28px teal `م` mark** (chip-sized, so invariant 3 holds — now the
only saturated pixel in the chrome); the wordmark **«مسار» Cairo 700** (invariant 4's one exemption);
**RTL Arabic itself**, the strongest and least copyable signal on screen; teal as the single content
accent. Identity moves from *area* to *placement*: one mark, one direction, one accent.

## 1. Sidebar (light)

`aside`: **250px**, `background #F8F8F8`, **`border-inline-end: 1px solid #EDEDED`** — today's
`border-left` is physical and violates DESIGN.md; fix here. No gradient.

| element | spec |
|---|---|
| switcher | 52px, padding 10/12, `border-bottom 1px #EDEDED`. 28px radius-6 teal-gradient `م` tile · «مسار» 13px/600/`#171717` over «عبدالعزيز المحسن» 11px/450/`#7C7C7C` · chevron 12px `#C7C7C7` inline-end. **Replaces `.brand` + `.userbox`**; bottom userbox deleted. |
| `.nv` | 32px, padding-inline 10, gap 10, radius **6**, 13px/450/`#525252`, icon 16px `#999999`. Hover `#F3F3F3`. **Active `#EDEDED` + `#171717` + 500 + icon `#525252`** — no teal, no gold (invariant 3 does not list nav rows). Delete `.nv .dot`. |
| `.grp` | 11px/500/`#999999`, padding 6/10, margin-block-start 12; no border-top, no letter-spacing. Chevron 12px `#C7C7C7` inline-end; the header is a `<button aria-expanded>` collapsing its group. Five existing groups. |
| collapse | bottom row 32px, `border-top 1px #EDEDED`, icon 16px `#999999` + «طيّ القائمة» 12px `#7C7C7C`, radius 6, hover `#F3F3F3`. Arrow points **inline-start** (mirrors in RTL). Collapsed = 56px, icons only, labels via `title`+`aria-label`, `.grp` → 1px rule. Persist both in `localStorage` (preference, not data). |

## 2. Breadcrumb bar — replaces `header` (76px) **and** `.ptitle`

One **48px** bar: `#fff`, `border-bottom 1px #EDEDED`, padding-inline 20, gap 8. Reclaims ~158px.

- **inline-start:** «الحملات» 14px/500/`#171717` → list · `/` 13px `#C7C7C7` · **view button** 16px
  icon + «كانبان» 13px/450/`#525252` + chevron, radius 6, hover `#F3F3F3`.
- **menu, two sections:** **العرض** (قائمة · تجميع · كانبان) and **اللوحة** (the four `CRM_KEYS`),
  each option carrying its own `kd[3]` explainer. Absorbs `.vtog`, `.crmsel`, the floating helper line.
- **inline-end:** one solid **«+ إنشاء حملة»**, 32px, radius 6, 13px/500, white on **teal `#1F7A73`**.
  *Named divergence:* Frappe's is near-black; teal stays as the one primary action per screen
  (invariant 3). Going black would delete the last accent for no gain.
- **تصدير CSV** moves to §3, not here.

## 3. Quick-filter row — ONE row, 44px

`#fff`, `border-bottom 1px #EDEDED`, padding-inline 20, gap 8, controls 28px/radius 6 (V1 §5).

**inline-start:** search, restyled 38px/radius-999 → **28px/radius-6** (outstanding V1 debt). Then
**dropdown pills, one per `CRM_KEY`**: التصنيف · الخدمة · شهر الإطلاق · حالة الأداء. Inactive = white
on `#EDEDED`, placeholder `#999999`, chevron. Active = `#F3F3F3` + `#C7C7C7` + `#171717`, reads
«التصنيف: فعلية», `×` clears. Options and counts come from `crmGroups()`'s existing key functions —
**no new field invented**; filter and board finally share one vocabulary. Below 640 the pills scroll
horizontally (`ms-scroll`), never wrap.

**inline-end:** «مُحدَّث ٩:٤١» 12px `#7C7C7C` (rescues the deleted `livechip`; its `#DCF1EF` fill dies)
· refresh · **«تصدير CSV»**. Total count → plain 12px `#7C7C7C`, no pill.

**Merges:** the three class tabs collapse into the التصنيف pill; `.vtog`/`.crmsel` go to §2.
**Verify `exportCampaigns()` scope** — on the filter row it must export `crmFiltered()`, or be
relabelled «تصدير الكل CSV». Bulk bar keeps «تصدير المحدد CSV» (never co-visible).

## 4. Kanban card — Massar's honest zones

`#fff`, radius **10**, `border 1px #EDEDED`, padding 12, gap 6, no shadow. Hover `border-color
#C7C7C7` only. Focus `outline 2px #1F7A73, offset -2px`. Must be an `<a>` or `role="link"
tabindex="0"` with Enter/Space — today's `onclick` div is not keyboard reachable.

| Frappe zone | Massar |
|---|---|
| avatar + title | **8px status dot + name** 14px/500/`#171717`; dot reuses the row mapping (فعلية `#1F7A73` / تجريبية `#E2E2E2`). 500 sits one step above the 450 list row because a card has no column header to carry hierarchy. |
| field lines | **two stacked lines** 13px/450/`#525252`: `c.product` or «بلا خدمة» · `fmtD(c.created_at)`. A card has room a 36px row does not. |
| assignee | **DROP** — no owner field exists. |
| relative time | **DROP** — duplicates the date; no Arabic relative formatter exists. Revisit only if `fmtRel` ships. |
| hairline | keep: `border-top 1px #EDEDED`, margin-block-start 10, padding-block-start 8. |
| icon+count footer | **label+figure pairs**, middot-separated: «الجمهور `fmtN(targeted)`» · «شوهدت `crmPctD(seen)`» · «ردّوا `crmPctD(replied)`» · «مهتمة `crmPctD(interested)`». Labels 12px `#7C7C7C`, figures 13px/500/`#171717`; `null` → «—». **If `!st.targeted` the footer collapses to «بلا جمهور»** — no zeros. `failed > 0` appends «تعذّر N» `#B42318`; zero renders nothing (a zero failure is a default state, unlike an empty *group*, which is a vocabulary slot). **Icons dropped** — مشاهدة/ردود have no honest glyph, and a wrong icon is worse than a word. |
| footer `+` | **DROP** — no per-campaign create action. |

## 5. Column header

`dot + name + count`. Name 13px/500/`#171717`; count **plain 12px `#7C7C7C`**, kept against the
screenshot because the empty-group rule («تجريبية ٠») depends on it being visible.

**Dot only where it means state:** التصنيف and حالة الأداء (`CRM_PERF` colours). **Omit on الخدمة and
شهر الإطلاق** — a product and a month are not states, and a neutral bullet reads as one. The boards
genuinely differ; consistency that lies is worse.

**`+`:** omit on التصنيف (class is set post-launch), شهر الإطلاق (`created_at` not choosable), حالة
الأداء (computed). الخدمة **only if** `#aimkt` accepts a preselected product → «أنشئ حملة لهذه
الخدمة»; otherwise omit everywhere. The data model does not earn this affordance.

**Column wash:** `#F3F3F3` on drag-over, **التصنيف only** — the sole drop target; other boards get
none because nothing can receive. Track 280px, gap 12.

## 6. Dropped, consolidated

Notifications + badge (no such system; the count would be invented) · emoji (no saved views;
unreliable in Arabic rows) · Public/Pinned views (no persistence) · avatar · assignee · relative time
· card `+` · @mention/note/task/comment counts (no such entities) · ⚙ Filter (the pills *are* the
filter) · ▤ Kanban Settings (none exist) · column `+` on three boards · navy + gold · `.vtog` ·
`.crmsel` · helper line · count pills · 76px header · `.ptitle` · `livechip` fill · footer icons ·
near-black Create (kept teal).

## 7. Migration order — visible shift per risk

1. **S5 sidebar.** One CSS block + one static-markup merge; touches every screen; largest shift,
   contained risk. Includes the `border-left` → `border-inline-end` fix. **Ship first.**
2. **S6 breadcrumb. Highest risk — ADR-0001 trap:** `nav()` writes `#pt`/`#ps`/`#live` by id;
   deleting the header deletes those ids and blanks every screen. `nav()` must change in the same
   commit.
3. **S7 filter row, subset.** Search restyle + التصنيف pill + inline-end controls. No new state.
4. **S8 card + column header.** Contained to `crmKanbanView`.
5. **S9 the other three pills.** New `crmFilters` + `crmFiltered()` — real logic, least visible shift
   per unit risk. Last.

Each gated by `npm run check` + `npm run smoke`. **QA baseline, capture before S5:** `#kmon` list
**and** kanban at **1440×900, 768×1024, 375×812**. Re-verify 375/768 after S5 (264→250, collapse) and
S7 (pill overflow).
