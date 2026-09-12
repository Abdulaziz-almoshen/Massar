# «فرص البيع» — synthesized redesign spec (Claude main + Codex + Claude subagent)

## Agreed by all three voices
- ONE navigation row. The shell's door tabs become «الفرص · فرز الردود · لوحة المتابعة» (triage
  becomes a real route under the same door). The in-page «الفرص/فرز الردود» toggle is deleted.
- The nine stage cards are deleted. The cards view is deleted (list + kanban only).
- One summary panel, one ledger panel, one drawer. Detail AND create use the same drawer.
- Flush table, full SAR values in rows («٤٬٢٠٠ ر.س»), unpriced never zero.
- WhatsApp "interested, no opportunity" band lives INSIDE the ledger panel as an action row.
- One blue primary button. No black button. No filled grey chips for state.
- No probability, no expected-close-date column (neither is recorded).

## Page anatomy (RTL; start = right)
1. Shell header (existing): title «فرص البيع», subtitle «كل بند من أول تواصل حتى الإغلاق»; ONE
   underline tab row.
2. Summary panel — paper, 1px --line, r-lg, 24px padding, no shadow. Start: label «القيمة المفتوحة»
   12/500 muted, figure 28/600 ink (compact money with correct counted noun), then an 8px stage
   distribution bar across the 6 open stages (segment width = priced open value per stage, single
   blue ramp encoding ORDER only, 2px gaps, each segment a button with an accessible name
   «عرض السعر · ٤٬٢٠٠ ر.س»; clicking filters). Under the bar, a legend line naming the non-empty
   stages. End: three filter metrics separated by hairlines, 22/600 figure + 12 muted label:
   «بنود مفتوحة» · «متوقفة» (warn glyph when >0) · «لم تُسعَّر». Selected metric = accent-tint ground
   + check glyph. Summary follows search/source/owner filters. Empty → «—».
3. Ledger panel — paper, 1px --line, r-lg, overflow hidden.
   a. Toolbar 64px, 16px padding, 8px gaps, 36px controls: search (ring, 280px) · المرحلة ▾ ·
      المصدر ▾ · المسؤول ▾ · ترتيب ▾ · flex · list/kanban segmented icons · primary «إضافة فرصة»
      (blue). Active filter controls use accent-tint + accent-deep. A «مسح التصفية» text action appears
      only when any filter is active. Selection swaps the toolbar content at the same height:
      «٣ بنود محدّدة · نقل إلى مرحلة ▾ · أسنِد إلى ▾ · إلغاء».
   b. WhatsApp action row (only when non-empty) 48px, accent-bar ground, accent-deep text:
      chat glyph · «جهتان مهتمّتان عبر واتساب بلا فرصة» · flex · «عرض» chevron. Expands (accordion)
      into flush rows in the same panel: name · service read · «فتح فرصة» (opens create drawer
      prefilled) — plus «كل الردود في فرز الردود ←».
   c. Table header 40px, --surface, 12/600 muted. Columns start→end:
      ☐ 44 · الجهة flex(min 180) · المنتج 1fr · المرحلة 180 · القيمة 130 (end-aligned, bdi) ·
      المصدر 120 · المسؤول 130 · الخطوة التالية 1.2fr · › 36
   d. Rows 56px, --line-soft dividers, no radius/shadow. Hover accent-wash. Selected accent-tint.
      Row open in drawer: accent-tint + 3px inset accent bar at inline-start.
      - الجهة: 14/600 ink, truncates; a «تلقائي» outlined mini-badge if created by the assistant.
      - المرحلة: 8px dot (open = accent-mark, won = issued, lost = fail) + full label; second line
        12 muted «منذ ٤ أيام»; stalled → warn outlined pill «متوقفة · ١٦ يومًا».
      - القيمة: full «٤٬٢٠٠ ر.س» 14/600 ink; unpriced «لم تُسعَّر» 14/450 muted.
      - المصدر: 16px glyph + word; whatsapp source links to the conversation (#customer/phone).
      - المسؤول: name 14/450; empty «بلا مسؤول» muted.
      - الخطوة التالية: text 14/450 ink truncated; empty «لم تُحدَّد» muted with dashed underline.
      - ›: 24px chevron affordance, aria-hidden; row is the button (tabindex 0, Enter/Space opens).
   e. Footer 52px: range «١–٢٥ من ٦٢ بندًا» + pager · live value «قيمة المعروض … · دون الخسارة».
   f. Empty / loading / failed / filtered-empty each named in words.
4. Kanban (same summary + toolbar): 8 columns 280px, 16px gaps, horizontal scroll inside the panel
   body. Column = --surface ground r-lg; header: dot + stage name 14/600 + count; second line
   compact total + «· ١ لم تُسعَّر». Records: paper cards r-md, 1px --line, 12px padding: account
   14/600, product 12 muted, value 14/600, owner + stall warn. Drag changes stage via the one PATCH;
   click opens the drawer. Empty column: «لا بنود».

## Drawer (detail + create) — one component
- 520px, full height, enters from inline-start (right edge, DESIGN.md §4 and the existing
  .mo-panel pattern) over a light scrim. Header/footer fixed, body scrolls. Esc closes; focus moves
  to the drawer heading and returns to the row that opened it; Tab trapped.
- Detail header 72px: account 18/600, product 14 muted, close button. Save status slot
  «حُفظ» / «جارٍ الحفظ…» / «تعذّر الحفظ» at reserved width.
- Section «المرحلة»: a 6-segment stage track (open stages; current = solid accent + label, passed =
  accent-tint, ahead = hatched); two outlined outcome buttons «أُغلقت ربحًا» / «أُغلقت خسارة»;
  a line «في هذه المرحلة منذ ٤ أيام» (warn when stalled).
- Section «القيمة»: figure 22/600 + formula line muted «٦٠٬٠٠٠ × ١ سنة × ١ × (١ − ٩٣٪)»; four
  labelled fields in a 2×2 grid; discount > ٥٠٪ shows an inline warn message (not blocking).
- Section «المتابعة»: المسؤول and الخطوة التالية fields.
- Section «التفاصيل»: label:value rows (120px label col): المصدر (linked campaign/conversation),
  سجّلها, أُنشئت, آخر تحديث.
- Section «بنود أخرى لهذه الجهة» (when any): flush rows product · stage · value; click switches.
- Footer: «ملف العميل ←» ghost · flex · press-and-hold «حذف البند» (DESIGN.md §3.13).
- Editing = autosave per field on change through the one PATCH path, with the save-status slot.
  No edit mode and no second primary button (the current product already autosaves; a modal
  edit/save step would add a click to every stage move).
- Create mode: header «إضافة فرصة»; fields الجهة (with suggestions) · الجوال · مصدر الفرصة
  (segmented) · الحملة (only for whatsapp) · المسؤول; «المنتجات» blocks (product select + 2×2 price
  grid + live value, «إزالة»), «+ منتج آخر»; total row; footer primary «إنشاء الفرصة» + «إلغاء».
  Errors inline above the footer.

## Acceptance checklist (pass/fail)
1. One tab row; no in-page view toggle for triage; nothing clipped at 1280/1440.
2. Exactly one blue primary button visible per state; no black buttons on the page.
3. No stage-card grid and no cards view; one leading 28px figure; bar geometry = priced open value.
4. Flush table: 56px rows, dividers, no per-row radius/shadow; hover accent-wash.
5. Stage state = dot + word (+ outlined warn pill when stalled); no filled grey chips.
6. Rows show full SAR amounts with Arabic-Indic digits; unpriced says «لم تُسعَّر»; no «٤ ألف».
7. Row click / Enter opens the drawer; table stays behind; Esc closes; focus returns to the row.
8. Create uses the same drawer and the same field grammar as detail.
9. WhatsApp band sits inside the ledger panel; «فتح فرصة» opens the prefilled create drawer.
10. Account → customer record, WhatsApp source → conversation, drawer → other lines of the account.
11. Kanban uses the same toolbar, summary, value format and drawer.
12. Bulk selection swaps the toolbar content with no height change.
13. Delete is press-and-hold; keyboard two-step.
14. Loading, empty, filtered-empty and failed states are distinct and worded.
15. Contrast gate (`scripts/check-design.mjs`) green; no page-wide horizontal overflow at 1280,
    1440 or 390px.

## Addendum v2 — resolving Codex MUST-FIX 1–8
1. RESPONSIVE. ≥1100px: layout as specified. 900–1099px: toolbar wraps to two rows (search +
   primary on row 1, filter selects + view switch on row 2); summary metrics wrap under the bar.
   <900px: table becomes stacked rows inside the same panel (account + value on line 1, product,
   stage, next step below; no horizontal page scroll); summary stacks (figure, bar, metrics in a
   3-up row). <560px: drawer is full-width (100vw), 16px gutters. Under pointer:coarse every
   control, row trigger, bar segment and checkbox has a ≥44px hit area (padding/::after, marks
   unchanged).
2. AUTOSAVE CONTRACT. Text fields commit on change (blur/Enter); number fields validate in the
   element (min/max) AND before the write; an invalid value is not sent and the field shows an
   inline error with aria-invalid. Writes go through the one PATCH; each field has its own state:
   pending (muted «جارٍ الحفظ…» under the field), saved (a 900ms «حُفظ ✓»), failed (persistent
   «تعذّر الحفظ — أعد المحاولة» with a retry action, the typed value kept in the field, the row
   NOT updated). Ordered writes: a second change to the same field waits for the first response.
   Closing or switching records while a write is pending lets it finish (the request is not
   cancelled) and shows its outcome as a toast; a failed write keeps the drawer open with the
   error visible. Concurrency: the server row returned by PATCH replaces the local row (last write
   wins; the ledger has no version column — named limit, not silent).
3. SEMANTICS. Filters AND-combine: search × stage × source × owner × summary shortcut. The summary
   reflects search/source/owner but NOT the stage filter or shortcut (it is the navigator for
   them). Footer total = all filtered rows, not the page, and says «دون الخسارة» when lost lines are
   in the set; «لم تُسعَّر» lines are counted and never summed. A priced zero shows «٠ ر.س». Stall
   rule: open line in التقييم التقني or التفاوض والاعتماد whose days since stage_at (stage entry;
   not last edit) are ≥ 14. The drawer's stage track marks ONLY the current stage (solid) and draws
   the others as ordered neutral cells — no "passed" claim. A won/lost line shows its outcome
   state and a «إعادة فتح» action that moves it back to التفاوض والاعتماد.
4. ACCESSIBILITY. Rows remain grid rows with role="row"; the dedicated detail trigger is a real
   <button> in the last cell («فتح تفاصيل البند»); row click is a pointer convenience only.
   Checkbox, account link and source link stop propagation. Stage movement is available by
   keyboard in the drawer (the track is a radiogroup, arrows move focus, Enter commits) and in the
   bulk toolbar. Focus returns to the exact trigger that opened the drawer. Bar segments get a
   ≥24px hit area; zero-value stages are not drawn but appear in the visible legend («عرض المنتج ٠»),
   which also shows each non-empty stage's amount in text.
5. CREATE CONTRACT. Required: account name, ≥1 product line with a product. Price fields optional
   (blank = unpriced, allowed; 0 = priced zero); years 1–20, qty ≥1, discount 0–100. One POST
   creates all lines (server is atomic per request). The primary is disabled while submitting
   («جارٍ الحفظ…» at reserved width) so it cannot double-submit; on failure every field keeps its
   value and the server's named field error shows inline above the footer. On success the drawer
   closes, a toast confirms, and if the new lines are hidden by current filters the toast says
   «أُنشئت خارج التصفية الحالية» with «عرض» that clears filters. The toolbar's «إضافة فرصة» is
   disabled (aria-disabled) while the create drawer is open.
6. CONNECTED. Lines created from the WhatsApp band carry phone, source=whatsapp and the campaign
   id; that contact leaves the band immediately (it is derived from «has a line with this phone»).
   Every mutation updates the single oppRows store and re-renders row, drawer, summary, kanban and
   footer from it. Filters, sort, view, page and scroll survive opening/closing the drawer.
   Shareable record URL: #opps/<id> opens that line's drawer; closing returns to #opps.
7. BULK + SCALE. Header checkbox = current page; a «تحديد كل المطابِق (٦٢)» text action appears when
   the page is fully selected. Selection is intersected with the visible filter on every write and
   cleared on view change. Bulk writes report «نُقلت ٩ · تعذّر ٢» and keep the failed ones
   selected. Kanban column headers count and sum the complete filtered column; each column renders
   the first 50 and states «تُعرض ٥٠ من ١٢٠» with «عرض الكل في القائمة».
8. STATES. Loading: 5 skeleton rows at row height inside the panel, summary shows skeleton blocks.
   Failed load: panel body says «تعذّر تحميل الفرص» with «أعد المحاولة»; stale data, if any, stays
   visible under an inline warning. Empty ledger: sentence + «إضافة فرصة». Filtered-empty: «لا بند
   يطابق التصفية» + «مسح التصفية». Failed kanban move: the card stays in its original column (the
   store only changes on success) and a persistent error toast names the account. Failed delete:
   drawer stays open with the error. Reduced motion: drawer appears without translate; hold-to-
   delete falls back to the two-step keyboard path.

## Addendum v3 — closing the second review
1. MOBILE TOOLBAR (<900px container): row 1 = search (flex) + primary «إضافة فرصة»; row 2 = a
   horizontally scrollable strip INSIDE the toolbar holding المرحلة · المصدر · المسؤول · ترتيب and the
   view switch (the page never scrolls sideways). Selection mode on mobile: row 1 count + «إلغاء»,
   row 2 the two bulk controls.
   VISIBLE FOCUS: every control uses DESIGN.md §3.8 — 2px --accent outline, 2px offset, on
   :focus-visible only; on the blue primary the ring inverts to paper + 4px accent halo; the row
   trigger, kanban card, bar segment, legend item and metric all get the same ring.
   LEGEND AS THE OPERABLE ALTERNATIVE: under the bar, the legend lists ALL six open stages in
   order as buttons «● عرض السعر ٤٬٢٠٠ ر.س · ١» (zero stages included, muted, still operable —
   they filter to an empty, worded state). The bar segments are pointer shortcuts only
   (aria-hidden, tabindex -1), so tiny/zero segments never need a target of their own.
2. SAVE FAILURE AFTER DISMISSAL: a failed write is kept in a per-line «unsaved» store. The row
   shows a fail-text glyph «لم يُحفظ تعديل» in its next-step cell; reopening the drawer shows the
   typed value in the field with «تعذّر الحفظ — أعد المحاولة» and «تجاهل». The toast that reports
   the failure carries «فتح البند» which reopens that drawer. Nothing unsaved is silently dropped
   until the user chooses «تجاهل» or the save succeeds; a page reload is the only loss (named).
3. —
4. See 1 (focus + legend).
5. PRICING VALIDATION: sale_price blank = unpriced, else a number ≥ 0 with at most 2 decimals;
   years integer 1–20; qty integer ≥ 1; discount number 0–100. A line with a price but blank
   years/qty uses the defaults 1/1 (shown in the fields, not hidden). Partial pricing is therefore
   impossible to store: a line is either unpriced (no price) or fully priced. Invalid values show
   inline and block that write / the create submit, with focus moved to the first invalid field.
   PRIMARY DEMOTION: while the create drawer is open, the toolbar button renders as a ghost
   button with aria-disabled — the drawer's «إنشاء الفرصة» is the only blue primary in the DOM.
   While the detail drawer is open the toolbar primary stays but is under the scrim (inert).
6. RELATIONSHIP IDS: in this data model the phone IS the contact id and the conversation key
   (conversations are keyed by phone), the account is account_name+phone (accountKey), and the
   campaign is source_ref. All four are written on create-from-WhatsApp and never rewritten by an
   edit (the PATCH does not accept phone/source/source_ref). NAVIGATION STATE: view, filters,
   search, sort, page and the open line live in module state that survives route changes, so
   going to «ملف العميل» or a conversation and pressing Back restores the board exactly, including
   #opps/<id> re-opening the drawer.
7. SELECTION ON FILTER CHANGE: any change to search, stage, source, owner, shortcut, sort or view
   clears the selection and says so («أُلغي تحديد ٣ عند تغيير التصفية») — the rule the campaigns
   and customers lists already use. KANBAN BEYOND 50: each column shows 50 and a «عرض ٥٠ أخرى»
   button that extends that column (per-column cap in state); the header count/total is always
   the whole filtered column. SCALE CHECK: `npm run qa:scale` fixture plus a manual pass with a
   60-character Arabic account name and a 40-character product; no row height change, no
   overflow.
8. TWO-STEP DELETE (the shared HOLD_JS contract): keyboard Enter/Space on «حذف البند» ARMS it —
   label becomes «اضغط مرة أخرى للحذف», aria-pressed=true, fail-soft ground; a second Enter/Space
   commits; moving focus away (Tab, click elsewhere) or Escape disarms and restores the label.
   Reduced motion uses the same arm/commit path for pointer. Failed delete: the drawer stays,
   the button returns to idle, and an inline fail-text line «تعذّر الحذف — أعد المحاولة» sits
   above the footer. Failed kanban move: card stays, toast «تعذّر نقل <الجهة>» with «أعد المحاولة»
   that re-sends the same PATCH.
