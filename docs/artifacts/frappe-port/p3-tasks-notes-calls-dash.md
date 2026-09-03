# frappe-port P3 — Tasks · Notes · Call Logs · Calendar · Dashboard · Welcome · Data Import

Source read: `frontend/src/pages/{Tasks,Notes,CallLogs,Calendar,Dashboard,Welcome,DataImport}.vue`,
`components/ListViews/{TasksListView,CallLogsListView}.vue`, `components/Dashboard/{DashboardGrid,DashboardItem,AddChartModal}.vue`,
`crm/api/dashboard.py`, `crm/fcrm/doctype/{crm_task,crm_call_log,fcrm_note,crm_dashboard}/*.py`.

## Tasks.vue
Regions: LayoutHeader (breadcrumbs | CustomActions + **Create**) → ViewControls (`doctype: CRM Task`, views `list|kanban`) → KanbanView **or** TasksListView → EmptyState.
Actions: create (defaults `status: Backlog`, `priority: Low`; kanban column presets the column field) · open via row click or `?open=` · edit in modal · delete (`frappe.client.delete`) · jump to parent Deal/Lead · kanban drag→`updateKanbanSettings` · cell-click filter · like · bulk select · load more · column resize.
Default columns (`crm_task.py`): Title · Status · Priority · Due Date · Assigned To · Last Modified. Kanban: column=status, title=title, fields=[description, priority, creation].
**DROP** — missing: task entity, user table (`assigned_to`), due-date/reminder engine. This is a new entity, not a port.

## Notes.vue
Regions: header + Create → ViewControls (`FCRM Note`, columns button hidden) → 4-col card grid (h-56: title, sanitized HTML body, owner avatar + name, timeAgo) → ListFooter → EmptyState. Actions: create · edit (card or dropdown) · delete · `?open=` · load more. Rows: name,title,content,reference_doctype,reference_docname,owner,modified; **columns: []** (card view has none).
**DROP as an entity** (no note entity, no author). **PORT ADAPTED as a layout**: the card grid is the right shell for **معرفة الخدمة** (KB entries already exist) — strip the owner avatar, one operator.

## CallLogs.vue + CallLogsListView.vue
Regions: header + Create → ViewControls (`CRM Call Log`) → CallLogsListView → EmptyState + CallLogDetailModal.
Actions: create · row click → modal via `crm_call_log.get_call_log` · cell-click filter · like · bulk actions (`hideEdit`, `hideAssign`) · load more · resize · `?open=`.
Default columns: Caller · Receiver · Type · Status · Duration · From (number) · To (number) · Created On (rows also carry note, recording_url, reference_doctype/docname). Renderers: Avatar for caller/receiver, icon for type/duration, **Badge for status**, heart for `_liked_by`.
**PORT ADAPTED** — substitute: the `tracker.ts` message/status ledger. Type→inbound/outbound, Status→sent/delivered/read/failed, From/To→numbers, reference→campaign. Duration and recording_url **DROP** (no telephony). Best structural steal on this page set.

## Calendar.vue
Regions: header + Create (Mod+E) → frappe-ui Calendar (Day/Week/Month, month-year DatePicker, prev/Today/next, user Link filter) → 352px slide-in CalendarEventPanel. Actions: click→details, dbl-click→edit, cell-click→new, drag/resize→update, create/update/delete/duplicate/sync, range-change refetch, auto-creates Contacts for unknown participant emails. Data: `Event` doctype, `status=Open` + window filters, orFilters owner|participant email.
**DROP** — missing: event entity, participants/user table, email/calendar sync. `insights.best_time` is a reading, not a booking.

## Dashboard.vue — widgets
Regions: header (Refresh · Edit (admin) · in edit: +Chart, Reset to Default, Cancel, Save) → filter bar (preset dropdown 7/30/60/90 days + Custom Range picker; **Sales User** Link, manager/admin only) → DashboardGrid (frappe-ui GridLayout, 20 cols, rowHeight 42, drag/resize + hover-trash while editing) → AddChartModal.
**Widget types: exactly four** — `number_chart` (NumberChart + tooltip), `axis_chart` (line/bar; `swapXY:true` is how the funnel is drawn), `donut_chart`, `spacer`.
Config: item = `{name, type, layout:{x,y,w,h,i}, data}`; the array is persisted as JSON to `CRM Dashboard / "Manager Dashboard" . layout` via `frappe.client.set_value` (data stripped first); `reset_to_default` restores the 17-item default layout.
Data: `get_dashboard(from,to,user)` loads the layout then dispatches per item to `get_<name>` in `crm/api/dashboard.py` — **no generic query builder; every widget is a hand-written SQL function**. Number charts return `{title,tooltip,value,delta,deltaSuffix}`, delta = % vs the immediately preceding equal-length period.

| widget (from AddChartModal + default layout) | verdict |
|---|---|
| total_leads | ADAPTED → contacts created in range (`campStats.targeted`) |
| ongoing_deals · won_deals | ADAPTED **as readings** → `insights.deal_state` active/won, labelled «قراءة» |
| average_ongoing/won/deal_value · forecasted_revenue | **DROP** — no value/currency field exists; any number is fabricated |
| average_time_to_close_a_lead / _a_deal | **DROP** — no close event with a timestamp |
| sales_trend | ADAPTED → delivered/replied/interested per day from status times |
| funnel_conversion | **AS-IS structurally** → targeted→delivered→seen→replied→interested (`campStats`, real counters) |
| deals_by_stage_axis · deals_by_stage_donut | ADAPTED → `SALES_STAGES` (6), labelled reading |
| lost_deal_reasons | ADAPTED → `winLossBoard().loss_causes` (`LOSS_TAXONOMY`), labelled reading |
| leads_by_source · deals_by_source | ADAPTED → campaign of origin |
| deals_by_territory | **DROP** — no territory field |
| deals_by_salesperson | **DROP** — one operator, no user table |
| spacer · date presets · edit/save layout | AS-IS. Sales-User filter **DROP** |

Page verdict: **PORT ADAPTED** — keep the shell and the one-function-per-widget dispatch; replace the catalogue. 6 of 17 defaults drop outright.

## Welcome.vue
Centered: headline "Welcome {name}, lets add your first lead" + two 224px cards (Add Sample Data · Connect your Email) + ghost "Or create leads manually" → LeadModal. In this revision `name = ref('John Doe')` is hardcoded and **neither card button has a click handler** — an unwired mock.
**PORT ADAPTED** for first-run الرئيسية; **DROP** the sample-data card (the invented-value trap) and the email card. Real first action: «ارفع ملف جهات الاستهداف».

## DataImport.vue — flow
The page is a 7-line wrapper: renders `DataImport` from `frappe-ui/frappe` with `doctype`, `importName`, and a `doctypeMap` (CRM Lead, CRM Deal, Contact, CRM Task, CRM Organization, CRM Call Log → title + listRoute + pageRoute). Routes: `/data-import` (list) · `/data-import/doctype/:doctype` (new) · `/data-import/:importName` (revisit a run). Entry: ViewControls "…" → **Import** (hidden in kanban).
**The step-by-step flow is not in this repo** — it lives in frappe-ui (not vendored; node_modules absent) and Frappe's `Data Import` doctype. I did not read it and will not describe steps I did not read → **Open Question**, `DONE_WITH_CONCERNS`.
Portable from what *is* readable: (a) the doctypeMap pattern — each importable entity declares its title and where the user lands afterwards; (b) **an import is a named record you can reopen** (`/data-import/:importName`). Massar's uploader is one-shot; a re-openable import with per-row errors is what the founder's complaint points at. **PORT ADAPTED (design only, source unread)** → جهات الاستهداف.

## Verdict
- **التقارير** → `Dashboard.vue` + `crm/api/dashboard.py`. The layout-JSON + one hand-written `get_<name>` + fixed allow-list pattern makes every number traceable to one function — exactly what "no invented values" needs.
- **لوحة المتابعة** → `CallLogs.vue` + `CallLogsListView.vue`: time-ordered ledger, status Badge per row, row-click detail modal, cell-click-to-filter, bulk actions, `?open=` deep link. (Tasks' kanban is second, only if stage columns stay labelled readings.)
- **No Frappe analogue at all**: إنشاء حملة · متابعة الحملات · شركاء المبيعات · الهيكل التنظيمي (CRM Organization is an account record, not a hierarchy) · معرفة الخدمة. جهات الاستهداف has only the thin DataImport shell.
