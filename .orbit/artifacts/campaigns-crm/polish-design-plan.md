# Polish design plan — campaigns-crm F1 (S1 · S3 · S4 · N1)

Gate **B** (Massar style already approved). Impact **HEAVY** — S1 is a layout change. Read: *he demos
from his phone; at 375 the list must answer "which campaign, did it work" without a sideways drag.*
Dials: variance 2 · motion 1 · density 8 (phone 6). `taste_skill_scope: excluded` (operational UI).
No new statistic: every value below already exists in `campStats` / `campPerfState` / `crmRate`.
Grounded in the round-32 captures read at all three viewports (`list-default` 375/768/1440,
`list-kanban@375`, `list-empty@375`, `detail-targets@375`, `detail-next@375`).

## S1 — the phone row

**Precondition.** `CRM_GRID` is an inline `style` on every row and header; `min-width:940px` is an
inline style on the wrapper. A media query cannot override either. Move both into
`CAMPAIGNS_CRM_CSS` first — `.crow` (the 9-col grid) and `.crmgrid` (the min-width), used by both
`crmListView` and `crmGroupView`. Do not reach for `!important`.

**≥600px: unchanged.** Nine columns, 940 min-width, `.ms-scroll` inside `.tblwrap`. Tablet keeps its
in-table sideways scroll; its masked edge must survive so the scroller stays discoverable.

**What the 375 capture actually shows today:** name, date, and a clipped الخدمة — الحالة, الجمهور,
مشاهدة, ردود and التقدّم are all past the fold. So the stacked row must recover exactly those five,
and nothing that is not already on the 1440 row.

**≤599px: `.crow` becomes `grid-template-columns:40px 1fr`, three block rows,** ~92px tall,
`.krow`/`.trow` unchanged:

1. status dot (9px, existing colours) · name 14px/700, one line, ellipsis · the action button (N1) at
   inline-end.
2. `fmtD` · `product` · the state `.chip` (`flex:none`; product ellipsizes first). 11px `#98A2B3`.
3. the figures in the kanban card's own idiom, which already reads correctly at 375 in
   `list-kanban@375` — «الجمهور ٦٠ · مشاهدة ٤٠٪ · ردود ١٢٪». Promote `.kcard .fig` to a shared
   `.fig` used by both surfaces; do not fork it.

**التقدّم without a 940px track:** it leaves the text rows and becomes a **3px full-bleed meter on the
row's block-end edge**, `#1F7A73` on `#EAECF0`, no number, `role="img"` +
`aria-label="التقدّم ٦٠٪"` (Arabic-Indic via `fmtN`). Stacked rows turn the bars into a scannable
column. `prog === null` → **no bar**; the «بلا جمهور» chip on line 2 already says why. `prog === 0`
is **not** null — the track renders with a zero-width fill. Both fixtures are never-sent, so an empty
meter is the common case at 375; the «لم تُرسل بعد» chip is what carries that, and S6's ruling stands
(a progress meter is not an outcome rate).

**Checkbox** — the 40px `.selcell` spans all three grid rows (`grid-row:1/4`): a 40×92 tap target,
which is what stops a phone checkbox being fiddly. `pointer:coarse` visibility, `stopPropagation`
and `.krow.sel`'s `border-inline-start` all stay as shipped.

**Header** — at ≤599 the nine-column header cannot render and must not be faked; the stacked row
labels its own figures. It collapses to one 44px strip: select-all + «تحديد المعروض» · spacer ·
«تحديد المطابقين (٨٤)» when `nOver>0`. One emitter (`crmHeaderRow`) with a narrow branch.

**States.** Filtered-to-empty: `crmEmptyList` renders inside the 940 box today, so at 375 its centred
text is structurally off-viewport — capture it, then `.crmgrid` fixes it. Group view uses the same
`.crow`; footers unchanged. When a selection exists, the list wrapper takes `padding-block-end:96px`
so the fixed `.bulkbar` (two lines at 375) never parks on the last row.

**Must NOT:** `display:none` columns on the existing grid · a parallel `.crow-mobile` · drop the chip
or the checkbox to save height · add a "عرض المزيد" expander · physical `left/right` · shrink the
track into a 40px stub with a label beside it · produce page-level horizontal scroll (`.kboard`
stays the only horizontal scroller).

## S3 — expand link on real overflow

Keep the link in the DOM, hidden, and unhide after measurement. `crmMeasureMsg()`: on the clamped
`.bub2`, show only if `scrollHeight > clientHeight + 1`. When `crmMsgOpen`, «طيّ النص» always shows —
no measurement. Run it (a) post-render via `setTimeout(...,0)` from `vKmonDetailCrm`, so dashboard.ts
is untouched; (b) on `document.fonts.ready` — the webfont swap is the real reason a length proxy was
reached for; (c) on debounced `resize`. Delete `msg.length > 90`. Null-message case unchanged.
**Must NOT:** measure the unclamped node, reserve space with a placeholder, or re-render to toggle.

## S4 — one next move under the hero

Hoist the `moves` computation above `crmSpecStrip`. Show `moves[0]`; the array is already ordered
hot → silent → failed → cause — **invent no score**. One line between hero and launch strip: the
move's own tint (`m[3]`/`m[2]`), `.card` radius, `[headline]` + `[افتح هذه الفئة]` (only when `m[4]`
exists — the cause move has none) + «كل الخطوات (٣)» linking to the tab. The tab keeps the full set
and its count.

**Zero moves → no strip.** A strip announcing nothing is chrome; the count-less tab label plus the
panel's «لا توصية الآن» is the signpost — the rule that killed the fake pager and the one-item sort.
**Must NOT:** a disabled/placeholder strip, a second copy of the hero's rates, or an action the tab
does not have.

## N1 — icons, and the caption said once

Both directions are one boolean, so it is **one icon with state, not two glyphs**: `ic("target",17,…)`
— `#1F7A73` on a فعلية row (click removes it from the measured set), `#D0D5DD` on a تجريبية row
(click restores it). Those are the row's own status-dot colours, so the row above teaches the
mapping. Keep the existing `title`/`aria-label` verbatim: they are directional, and they are the a11y
floor for an icon-only button. Do not add a symbol to dashboard.ts (only 15 exist; `target` is in
the set).

Caption: delete `.kcolh .why`, the group-header caption, and the board's trailing «للعرض فقط» note.
Emit once in `crmControlBar` as a `flex-basis:100%` line beside the group selector —
«الخدمة — تُحدَّد عند الإطلاق ولا تتغيّر», plus «هذه اللوحة للعرض فقط.» when
`crmActiveKey() !== "class"`. Three repeats collapse to one string.

## Judged not worth doing

- A second breakpoint fitting nine columns at 600–939: it requires dropping a column, which is FR-5's
  cancelled column picker by the back door. Tablet keeps the in-table scroller.
- A phone filter/sort sheet: three campaigns; the pills and the select already wrap.
- Animating the edge meter (motion dial 1).

## QA baseline

Prototype the phone row at `.orbit/design/previews/crm-phone-row.html` before Builder starts (gate B,
R98). Routes `#kmon` (list · تجميع · كانبان) and `#kmon/<id>` (three tabs) at 375×812 · 768×1024 ·
1440×900, plus filtered-empty at 375 and a no-audience row. 1440 must diff ≈0 against the accepted
round-32 captures — this cycle changes nothing above 600px.
