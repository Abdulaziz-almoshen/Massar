# Requirements — Frappe-style list/detail on the campaigns module (`#kmon`)

Cycle `campaigns-crm` · `[business-analyst]` · founder: "exact design and UX and functionality on top
of our campaigns module for whatsapp". Verified against `dashboard.ts` (campStats 428, vKmon 566,
vKmonDetail 683, `LIST_CAP=60` 275) and `db.ts` (campaigns/campaign_targets 87–104).

## Actors
- **A1 مدير المبيعات** — the only operator. One admin token, no user table → **no owner, assignee,
  "my campaigns", @mention or permission column anywhere** (F).
- **A2 المساعد الآلي** — writes contact-level readings (`insights.stage`, `deal_state`, `intent`);
  never writes campaign fields. Its output renders as «قراءة», never as a fact.
- **A3 the gates** — `check:numerals`, `check:campaigns`, `smoke` produce the acceptance evidence.

## Fields that exist (nothing else may be rendered)
`campaign{id,name,product,message,created_at,test}` + `targets[{phone,name}]`;
`campStats → targeted,sent,delivered,seen,replied,interested,failed`; contact `statusTimes`,
`transcript`, `tags`, `outcome`; **cached** insights (`/admin/insights` returns only computed rows →
partial coverage, F).
**Absent, therefore dropped from the port:** campaign stage, owner, close date, deal value, comments,
notes, tasks, calls, attachments, server-side saved views, campaign rename/edit (no PATCH exists;
the only campaign mutation is `POST /admin/campaign/test`).

## FR — campaigns LIST
- **FR-1 ViewControls bar** replaces today's tabs+search+sort: `فلترة · ترتيب · تجميع · الأعمدة` +
  view toggle `قائمة | تجميع | لوحة`. The three existing tabs (الكل/فعلية/تجريبية) survive as the
  `التصنيف` filter's shortcut chips; nothing that exists today is removed.
- **FR-2 Filter** builds conditions only over: `name`(contains), `product`(=), `التصنيف`(test|real),
  `created_at`(range), and any campStats counter (`≥ n`). Multiple conditions AND-ed; each removable.
- **FR-3 Sort** over: created_at, replied, seen, delivered, interested, targeted, name — asc/desc.
  Today's three sort options are the defaults, not the ceiling.
- **FR-4 Group-by / كانبان** over **only** `product`, `التصنيف`, `شهر الإطلاق` (month of created_at),
  `حالة الردود` (BR-2). Each column header shows its Arabic-Indic count.
- **FR-5 Column settings** — choose/reorder from the closed set of real fields (name, product,
  created_at, targeted, sent, delivered, seen, replied, interested, failed, التصنيف, progress %).
  Persisted in `localStorage` only; labelled per-browser, not per-user.
- **FR-6 Row selection** — per-row checkbox, header select-page, and **«تحديد المطابقين»** which
  selects *all filter matches*, not only the rendered `LIST_CAP` (mirrors `entAllMatching`).
- **FR-7 Bulk actions** — exactly three: `نقل إلى التجريبية` / `إعادة إلى الفعلية` (existing endpoint,
  per-id, partial failure reported with the failed count), and `تصدير المحدد CSV`. **No launch, no
  resend, no delete** (BR-5, §8).

## FR — campaign DETAIL
- **FR-8 Tabbed detail**: `نظرة عامة` (existing verdict card + stat grid + next-move cards),
  `جهات الاستهداف` (existing filtered table, unchanged semantics), `نص الرسالة` (renders
  `camp.message` — a stored field never shown today), `الأحداث` (timeline derived from targets'
  `statusTimes` inside the campaign window). No comments/notes/tasks/attachments tab.
- **FR-9 Side field panel**: الاسم · الخدمة · تاريخ الإطلاق · التصنيف · عدد الجهات · معرّف الحملة.
  **Only التصنيف is editable**; the rest render read-only with no disabled-looking input that implies
  a save path that does not exist.
- **FR-10 (optional, CPO decision D-2)** kanban of a campaign's targets by `insights.stage`
  (closed list `SALES_STAGES`) — permitted only with the «قراءة» marker on every card and a
  first column «لم يُقرأ بعد» for contacts with no cached insight.

## BR — business rules
- **BR-1 (hard, Rule 2).** Every column, chip, group header and card value maps to a stored field or
  a `campStats` derivation. A control with no backing field is dropped, not stubbed.
- **BR-2 (what backs kanban columns — no stage field exists).** Campaigns have no stage. The kanban
  therefore groups by a **stated predicate**, not an invented lifecycle. `حالة الردود` columns are
  `تجريبية` (`test===true`) · `فيها ردود` (`replied>0`) · `بلا ردود بعد` (`replied===0`). The current
  chip label **«مكتملة» is retired**: `replied>0` does not mean completed, and one function must emit
  both the chip and the column so they can never disagree.
- **BR-3.** Drag-and-drop is enabled **only** on the `التصنيف` board, where a drop maps to the real
  `POST /admin/campaign/test`. Boards over product / month / حالة الردود are read-only — a card
  cannot be dragged into a state nothing can write.
- **BR-4 (zero-denominator).** `targeted===0` → every rate renders «—», never ٠٪. Today's
  `base=Math.max(1,targeted)` would print a fabricated ٠٪.
- **BR-5 (§8).** No list or detail control may enqueue, send or schedule a WhatsApp message.
  «إعادة استهداف» stays a wizard-cohort handoff that halts before launch.
- **BR-6.** Filter/sort/group/columns/selection are client state over the already-fetched
  `campaigns` array; no new endpoint, no schema change.
- **BR-7 (ADR-0001).** All `dashboard.ts` edits are anchored string replacements.

## NFR
- **NFR-1** Arabic-Indic numerals everywhere incl. column counts, selection counter, filter values
  (`check:numerals`). **NFR-2** RTL; the kanban board is the only horizontal scroller (`ms-scroll`),
  the page never scrolls horizontally at 375/768/1440. **NFR-3** Re-render of 400 campaigns under
  200 ms; grouping computed once per render. **NFR-4** `npm run build` strict-clean; all 13 checks +
  smoke green.

## Edge cases
| case | required behaviour |
|---|---|
| 0 campaigns | existing empty state only; ViewControls hidden (not an empty filter bar over nothing) |
| 1 campaign | no cap footer, no pager, no "٠ أخرى"; kanban shows one column, others hidden |
| 400+ | `LIST_CAP` applies **per view** — per kanban column too — each with its own declared remainder; select-all-matching counts all matches and the bulk confirm states that number |
| campaign with 0 targets | BR-4; progress bar renders empty with «لا جهات استهداف», not ٠٪ |
| all campaigns test | فعلية tab keeps its explainer; kanban renders the single تجريبية column; no KPI reads as production |

## AC — acceptance criteria (each with its proof)
1. **AC-1 (FR-1..3)** Filter `الخدمة = X` + sort `الأكثر ردودًا` yields only X rows in descending
   replied order — *screenshot + row count vs. a node assertion over `/admin/campaigns`*.
2. **AC-2 (BR-1)** Every rendered column key ∈ the FR-5 closed set — *unit test enumerating column
   defs against the allowed list; fails on a new key*.
3. **AC-3 (BR-2)** No string «مكتملة» remains in `dashboard.ts`; chip and kanban column derive from
   one function — *grep + unit test asserting identical membership for 50 fixture campaigns*.
4. **AC-4 (BR-3)** A drag on the product board is refused with no network call; a drag on التصنيف
   issues exactly one `POST /admin/campaign/test` — *fetch spy*.
5. **AC-5 (FR-6/edge 400+)** With 400 seeded campaigns and a filter matching 137, «تحديد المطابقين»
   reports ١٣٧ while ٦٠ rows render — *fixture + screenshot of the counter*.
6. **AC-6 (FR-7, BR-5)** Bulk reclassify of 5 fires 5 `campaign/test` calls and **zero** Gupshup
   calls; a partial failure shows the failed count — *send-spy asserting 0 outbound, forced-500 run*.
7. **AC-7 (BR-4)** A zero-target campaign renders «—» for every rate and no ٠٪ — *fixture screenshot*.
8. **AC-8 (FR-8)** Detail shows four tabs; `نص الرسالة` renders `camp.message` verbatim (escaped) —
   *screenshot vs. DB row*.
9. **AC-9 (FR-9)** Only التصنيف is editable in the side panel; no other field exposes a save control
   — *DOM assertion in smoke*.
10. **AC-10 (FR-10)** If built: every stage card carries «قراءة» and uncached contacts appear only in
    «لم يُقرأ بعد» — *fixture with 3 cached / 7 uncached contacts*.
11. **AC-11 (NFR-1)** `npm run check:numerals` exits 0 — *gate output*.
12. **AC-12 (NFR-2)** `document.scrollingElement.scrollWidth <= clientWidth` at 375/768/1440 on
    `#kmon` in list, group and board views — *smoke assertion + 3 captures*.
13. **AC-13 (NFR-4)** `npm run check && npm run build` exit 0; smoke 7/7 — *CI log*.
14. **AC-14 (edge 0/1)** Empty and single-campaign fixtures render no ViewControls bar / no cap
    footer — *two screenshots*.

## Assumptions & decisions
- **D-1 (recommend: accept)** «مكتملة» → «فيها ردود». Changes an existing visible label; reversible,
  required by Rule 2. Owner: CPO.
- **D-2** FR-10 (contact-stage kanban) in or out this cycle. Owner: CPO. Non-blocking — default out.
- **A-1** "exact design and UX" means the *interaction model* (ViewControls, selection, tabbed detail),
  not Frappe's Latin/LTR visual system; the Massar design language governs (`massar-design-language.md`).
- **A-2** Saved views are per-browser `localStorage`; a server-side view store needs a schema change
  and is out of scope.

**Out of scope:** any schema change, campaign rename/edit endpoint, deletion, notes/comments/tasks,
multi-user or ownership, and every form of outbound send.

**Gate: READY for planning** — no unresolved item changes data, permissions or outward behaviour.
