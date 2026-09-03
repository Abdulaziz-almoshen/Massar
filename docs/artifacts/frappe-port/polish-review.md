# Massar portal — polish review vs Frappe CRM

**Verdict.** We ported Frappe's *information architecture* and skipped its *response model*. Frappe
answers every pointer, key and state change within 150ms; our portal answers almost nothing. Nine of
our interactive classes have no `:hover`, no `:focus-visible` and no `transition` at all. That, plus
placeholder sidebar icons, is the whole of "really horrible".

---

## 1. The ten things, ranked by feel-per-unit-work

| # | Thing | Frappe | Ours |
|---|---|---|---|
| 1 | **Sidebar icons are placeholder geometry.** 8 abstract shapes (`.g-sq/.g-ci/.g-tr/.g-ba/.g-tb/.g-ri/.g-di/.g-tree`) span 15 nav items — `g-ri` used 3×, so العملاء and شركاء المبيعات are the same grey circle. | `components/Icons/` — ~90 per-doctype SVGs | `dashboard.ts:70-77, 416-420`. We already ship 15 real symbols (`i-users`, `i-send`, `i-book`, `i-chart`…) used everywhere **except** the sidebar. ~10 lines. Biggest first-impression delta in the file. |
| 2 | **`.rise` replays on every keystroke.** `render(false)` rewrites `#body.innerHTML`, so every `.rise` container re-runs a 420ms `translateY(12px)` slide. Click a filter pill, type in search → the whole table jumps. | Vue patches rows; lists never re-animate on filter | `dashboard.ts:242-252, 2801`. Gate `.rise` to first paint only (route-change flag). One line, removes most of the perceived jank. |
| 3 | **Hover is a no-op on the main buttons.** `.btn:hover { filter: brightness(1.04) }` — `.btn-ghost` is `#fff`; brightness on white is white. تصدير CSV, رجوع, every ghost button: zero feedback. | `EventNotifications.vue:4` — `transition-colors · hover:border-outline-gray-3 · active:bg-surface-gray-4 · focus-visible:ring-outline-gray-3` | `dashboard.ts:219` |
| 4 | **`.qpill`, `.vtog button`, `.crmsel` have no hover, no transition, no focus-visible.** These are the *primary* controls on every list screen. | `PrimaryDropdown.vue:6`, `ColumnSettings.vue:27` — `transition-colors hover:bg-surface-gray-2` | `campaigns-crm.ts:36-44` |
| 5 | **List rows are un-focusable divs.** `<div class="crow" onclick="location.hash=…">` — no `tabindex`, no `role`, no `href`. Not keyboard-reachable, no middle-click, no browser status bar. | `LeadsListView.vue:6-11` `getRowRoute` → real routed links | `customers-crm.ts:103`, `tasks-crm.ts:84` |
| 6 | **The list doesn't fill the viewport and the header isn't a header.** At 1440 the campaigns list is 2 rows + 550px of nothing; `.crmflat` header is white-on-white, 12px/500 — identical weight to a row. | `ListRows.vue` `h-full overflow-y-auto` + tinted `ListHeader` | `campaigns-crm.ts:123`, `customers-crm.ts:126` |
| 7 | **Collapse animates the chevron and snaps the content.** `.rsechd .cv { transition: transform .12s }` next to `.rsec.shut > * { display:none }`. The one moving part is the arrow. | `CollapsibleSection.vue:39-46` — `max-h` transition, `duration-300 ease-in` | `record-tabs.ts:42-43` |
| 8 | **Reveal-on-hover exists once and is inconsistent.** `.krow .selcell { opacity:0 }` is the only `group-hover` we have; the *header* checkbox stays at `opacity:1`, so a static screen shows one orphan checkbox above an empty column. Frappe uses this pattern 14×, always paired. | `KanbanView.vue:59`, `Resizer.vue:5`, `PrimaryDropdownItem.vue:48` | `campaigns-crm.ts:49-51`, `customers-crm.ts:127` |
| 9 | **Mobile control bar is 5 wrapped rows, ~200px of chrome before any data** (`cus-list@375x812.png`). | filters collapse behind one icon | `customers-crm.ts:143-177` |
| 10 | **Tab switch is instant.** `recPaint` toggles `display`. Frappe crossfades panels. Cheapest possible: 120ms opacity on `.rpanel`. | `EmailArea.vue:3` | `record-tabs.ts:311-318` |

## 2. Genuinely wrong, not merely unpolished

- **`#customers`, nameless contact → phone printed twice.** `nm = c.waName || c.phone` (`customers-crm.ts:102`) then the phone renders again at line 108. Visible in `cus-list@1440x900.png` row 3: `966500001003  966500001003`, two weights, same value.
- **`#kmon` renders an empty progress meter for unsent campaigns.** Two rows, two grey tracks, `٠٪`. A campaign that hasn't sent should render no meter, not a zeroed one — it reads as a failed load (`list-default@1440x900.png`).
- **The mobile row is three dots.** Three stacked lines each open with a coloured dot at the start edge; it scans as a bullet list, not a record. Worse, `.thead-narrow` announces two columns (العميل | الحالة) over a three-line body — the header describes a layout that isn't there.
- **The control bar has no grammar.** Ten controls, four shapes, one row, all equal weight; the count pill «٣ جهة» is visually identical to the filter pills that *also* carry counts. Frappe splits: view toggle · quiet icon-buttons · quick filters.
- **`.tfoot` provenance band is heavier than the content it annotates** under a 2–3 row list.
- **Five chromatic hues violate the zero-chroma constraint.** `CUS_OUTCOME`/`TSK_ST` ship `#027A48 #2F5F94 #B54708 #B42318` alongside teal. Carry state by *shape* + label; keep teal as the only hue.

## 3. Loading and empty states

**Frappe.** Loading = `Icons/LoadingIndicator.vue` (`animate-spin` SVG) placed *inside the region that
will fill*, never as page text. Empty = `ListViews/EmptyState.vue`: icon + title + one sentence,
`top:35%`, `w-4/12`, ink-gray-5/8/6. Critically, `Leads.vue:258` guards it as
`v-else-if="leads.data && !rows.length"` — the empty state can never flash before data arrives.

**Ours.** `record-tabs.ts:197` and `:240` print «جارٍ التحميل…» / «تعذّر تحميل السجلات.» as bare
`textContent`, left-aligned, 13px grey — inside a tab that then jumps when rows land. The in-list
empties (`customers-crm.ts:187`, `tasks-crm.ts:125`) are padded strings with no icon and no action.

**Should be.** `crmSkeleton()` already exists (`campaigns-crm.ts:881`) and is used on 2 of 6 screens.
Use it everywhere a list will appear, including the record tabs. Route every empty through the
existing `.empty` block (icon + title + one sentence + one teal link) and guard it on
`rows !== null` so it never flashes. Add the spin SVG for in-place actions only (buttons, tab loads).

## 4. Not worth copying

1. `duration-300 ease-in-out` on hover/card states (`EmailArea.vue:3`) — sluggish at our density. Use 120–150ms; keep 300ms only for collapse/expand.
2. `hover:opacity-70` (10 uses) — dimming text on hover fails our contrast floor, badly at Cairo 450.
3. Column resize + column picker (`Resizer.vue`, `ColumnSettings.vue`) — large surface, six real fields, one operator.
4. Their colour system (`surface-red-7`, `fill-red-500`, avatar colour hashing) — pulls chroma straight back in.
5. Avatars / `_liked_by` hearts / assignment / @mentions — no owner field exists in the ledger.
6. `EventNotificationPopup.vue:134-152` overshoot bounce `cubic-bezier(.175,.885,.32,1.275)` — toy motion in an operations tool.

**QA baseline for this pass:** `docs/qa/campaigns-crm/*@{375x812,768x1024,1440x900}.png` +
`.orbit/qa/baselines/customer-966535106365-*.png`, re-captured on `#kmon · #customers · #tasks ·
#notes · #pipeline · #customer/966535106365` at all three viewports.
