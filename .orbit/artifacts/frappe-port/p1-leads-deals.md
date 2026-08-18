# P1 — Leads / Lead / Deals / Deal (Frappe CRM source read)

Source: `frontend/src/pages/{Leads,Lead,Deals,Deal}.vue`, `components/ListViews/{Leads,Deals}ListView.vue`,
`components/Activities/Activities.vue`, `ViewControls.vue`, `SidePanelLayout.vue`, `ListBulkActions.vue`,
`crm/fcrm/doctype/crm_{lead,deal}/*.py` (`default_list_data`), `crm/install.py` (side-panel layouts).

## 1. Leads.vue (list)

**Layout (top→bottom):** `LayoutHeader` [left: `ViewBreadcrumbs` = view switcher; right: `CustomActions` +
solid **Create**] → `ViewControls` (row of quick-filter fields, divider, then Refresh · GroupBy (group_by view
only) · Filter · SortBy (non-kanban) · KanbanSettings|ColumnSettings · "More" dropdown = Import/Export/
Customize Quick Filters; a Cancel/Save-Changes pair appears when the view is dirty) → body: `KanbanView` when
`route.params.viewType == 'kanban'`, else `LeadsListView`, else `EmptyState` → `LeadModal`.

**Functionality.** Real writes: create lead (modal); kanban drag (emits `update` → `updateKanbanSettings`,
persists `status`); like/unlike (`frappe.desk.like.toggle_like`); per-card dropdown New Note / New Task
(`showModal` → FCRM Note / CRM Task insert); bulk-select → `ListBulkActions` = Edit (bulk field set), Delete,
Assign To, Clear Assignment, **Convert to Deal**; column resize + save view; Import/Export. Navigation-only:
row click → `Lead`, filter/sort/group/quick-filter (server re-query), cell click → `applyFilter`.

**State/data.** One resource: `crm.api.doc.get_data` (doctype `CRM Lead`, forced filter `converted: 0`),
cached per `[doctype, view, viewType]`; returns `{data, columns, rows, view_type, group_by_field,
row_count, total_count, page_length_count}` and `_email_count/_note_count/_task_count/_comment_count`.
Default columns: **lead_name · organization · status · email · mobile_no · _assign · modified**.
Kanban defaults: column=`status`, title=`lead_name`.

**VERDICT — PORT ADAPTED.** The chassis (header + control bar + list/kanban/group-by switch + bulk bar) is
data-agnostic and maps onto contacts. Substitutions: `lead_name`→`waName || phone`; `organization`→**product**
(campaign's product); `status`→derived delivery state from `statusTimes` (sent/delivered/read/replied/failed) —
already computed in `dashboard.ts`; `email`→**tags**; `mobile_no`→`phone`; `modified`→last transcript turn.
**DROP** columns/actions: `_assign`, Assign To / Clear Assignment, `_liked_by`, SLA, Convert to Deal — no user
table, no second entity. Kanban columns must be `statusTimes`-derived or `outcome`, never an invented stage.

## 2. Lead.vue (record)

**Layout:** `LayoutHeader` [breadcrumbs | CustomActions · EnrichFromWebsite · **AssignTo** · **status
Dropdown** (IndicatorIcon + label) · **Convert to Deal**] → two panes: left `Tabs` whose single `#tab-panel`
renders `Activities`; right `Resizer` = (a) copy-id strip, (b) avatar block via `FileUploader` (image
upload/remove = real write) + title + icon row [Call · Email · Website · Attach · Delete], (c) `SLASection`,
(d) `SidePanelLayout`.

**Tabs:** Activity · Emails · Comments · Data · Events · Calls · Tasks · Notes · Attachments · WhatsApp
(`whatsappEnabled` only). **Side-panel sections** (`get_sidepanel_sections`, seeded in install.py):
*Details* (organization, company_description, website, territory, industry, no_of_employees, job_title,
source, lead_owner, linkedin, twitter, facebook) and *Person* (salutation, first_name, last_name, email,
mobile_no). Every field is **inline-editable** — `fieldChange` → `document.save.submit`, optimistic with
rollback + toast on error. Read-only: the id strip, timeline entries. Status dropdown writes `status` via
`triggerOnChange` then `setLostReason` (Lost → `LostReasonModal`).

**Activity timeline event types** (`crm.api.activities.get_activities` → `[versions, calls, notes, tasks,
attachments]`): `creation`, `added`, `removed`, `changed` (field_label, old→new, collapsible
"+N changes from X"), `comment`, `communication` (email), `incoming_call`/`outgoing_call`, `attachment_log`,
`event`. WhatsApp tab is a separate resource (`get_whatsapp_messages` + socket `whatsapp_message`) rendered
as a chat (`WhatsAppArea`) with a composer and template sender.

**VERDICT — PORT ADAPTED (the highest-value one).** Keep: three-region shell, tab set collapsed to
**المحادثة (WhatsApp transcript) · النشاط (timeline) · البيانات**, the inline-edit-saves-immediately side
panel, socket-driven refresh, the WhatsApp chat pane. Substitute side-panel sections with real fields:
*الجهة* (phone, waName, tags, outcome) and *الحملة* (campaign name, product, targeting time). Timeline events
become the real ledger: sent/delivered/read/replied/failed from `statusTimes`, tag changes, outcome changes.
**DROP:** AssignTo, lead_owner, Convert to Deal, SLA, Enrich-from-Website, email/call buttons, avatar image
upload, the whole Person/org field block. The status dropdown must **not** ship as a free-write control —
delivery state is observed, not chosen; only `outcome`/tags are operator-writable.

## 3. Deals.vue (list)

Structurally identical to Leads.vue (same header/ViewControls/Kanban/List/EmptyState/Modal), minus the
`converted` filter. Default columns: **organization · annual_revenue (Currency) · status · email ·
mobile_no · _assign · modified**; kanban title=`organization`, fields include `annual_revenue`.

**VERDICT — DROP.** Its distinguishing content is `annual_revenue`/`currency`, deal status pipeline, and
`deal_owner` — Massar has no deal value, no pipeline, no owner. Porting it means inventing a money column.
Anything worth keeping is already the Leads chassis.

## 4. Deal.vue (record)

Same shell as Lead.vue, with: no Convert button, an **organization-logo** avatar (read-only), and a
`contacts_section` in the side panel — a `Link` picker (+) and per-contact `CollapsibleSection` (avatar,
Primary badge, email, mobile) with dropdown Remove / Set as Primary, backed by real writes
`crm_deal.add_contact / remove_contact / set_primary_contact` and resource `get_deal_contacts`.

**VERDICT — PORT ADAPTED, narrow.** Only the **contacts_section pattern** ports: a record that owns a
collapsible list of related contacts = **campaign → targets[]**, with expand to show phone/tags/outcome and
a row action to open the contact. `set_primary_contact` has no analogue → DROP. Everything else (organization
details, annual_revenue, probability, next_step, closed_date, deal_owner) → **DROP**.

## Recommendation

**`Lead.vue` is the template for العملاء.** It is the only one of the four whose core is a *single
identity + an append-only conversation + a small editable field panel* — exactly a Massar contact
(`phone/waName` + `transcript[]` + `tags/outcome`). Deals adds money and pipeline (invented value); the two
list pages are the same chassis, and Leads' is the cleaner copy. Ported with the drop-list above, no screen
region requires a field Massar lacks.
