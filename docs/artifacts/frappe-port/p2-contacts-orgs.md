# P2 — Contacts & Organizations (Frappe CRM → Massar العملاء)

Read from source in the clone: `frontend/src/pages/{Contacts,Contact,Organizations,Organization}.vue`,
`components/ListViews/{Contacts,Organizations}ListView.vue`, `components/Modals/{Contact,Organization}Modal.vue`,
`components/{SidePanelLayout,ListBulkActions,ViewControls}.vue`, `composables/useContactFields.ts`,
`crm/api/contact.py`, `crm/install.py` (default layouts).

## 1. Contacts.vue — list

Regions: `LayoutHeader` (left `ViewBreadcrumbs`, right `CustomActions` from list scripts + solid **Create**) → `ViewControls doctype="Contact"` → `ContactsListView` / `EmptyState` → `ContactModal`. The page fetches nothing; **ViewControls owns the resource** and hands back `contacts.data` (`data`, `rows`, `columns`, `row_count`, `total_count`, `page_length_count`).

Actions: Filter · GroupBy · SortBy · ColumnSettings · quick filters (`install.py:501` → Contact = `status, email_id, phone`) · saved views (create/rename/duplicate/pin) · load-more · resize columns. Row cells are formatted client-side by `getMeta('Contact')` (Date/Datetime/Currency/Float/Percent); `full_name`→`{label,image}`, `company_name`→`{label,logo}` via `organizationsStore`, `modified`/`creation`→`timestampCell`.

Verdicts: filter/sort/search **PORT ADAPTED** (fixed filter chips over real fields, existing `custQ` search); saved views + ColumnSettings + GroupBy **DROP** (no user table, one operator, no per-user view storage); `_liked_by` heart column **DROP** (no user); Create **PORT ADAPTED** → the existing `entFileUpload` / `entManualSave` import path, not a doctype modal.

## 2. ContactsListView.vue

`ListView` with `getRowRoute → Contact/:contactId`. Prefixes: Avatar on `full_name`, Avatar(logo) on `company_name`, `PhoneIcon` on `mobile_no`. Clicking any cell emits `applyFilter` (filter-by-cell-value). `Check`→ disabled checkbox, `Rating`→ RatingInput, `_liked_by`→ heart toggle. `ListSelectBanner` → dropdown of `ListBulkActions.bulkActions()` with `hideAssign: true` ⇒ only **Edit** (`EditValueModal`, bulk set one field) and **Delete** (1 → `DeleteLinkedDocModal`, n → `BulkDeleteLinkedDocModal`) plus script-defined custom actions. `ListFooter` = page length + loadMore.

Verdicts: click-cell-to-filter **PORT AS-IS**. Bulk edit **PORT ADAPTED** (only legal bulk write in Massar is a prop write through `decideProp`; nothing else may be mass-set). Bulk delete **DROP** (contacts are conversation ledgers; deletion is not reversible and no such route exists). Assign/Clear-assignment **DROP** — missing dependency: user table.

## 3. ContactModal.vue

Dialog + `FieldLayout` from `crm_fields_layout.get_fields_layout(type='Quick Entry')`; `first_name` forced `reqd`; validates required fields, `@` in email, numeric mobile; converts `email_id`→`email_ids[{is_primary}]` and `mobile_no`→`phone_nos[{is_primary_mobile_no}]`; `frappe.client.insert`; redirects to the record. Managers can edit the layout. **DROP** (admin-configurable layouts need a doctype meta layer Massar does not have); manual add stays as today's `manualRowsHtml` two-field row.

## 4. Contact.vue — the record (closest analogue)

Two regions: a resizable **left panel** and a **tab area**.

- **Identity block** (left, top): `FileUploader` wrapping a 3xl `Avatar(label=full_name, image)`, hover camera overlay; with an image it becomes a Dropdown (Change / Remove). `changeContactImage` writes `contact.doc.image` then `contact.save.submit()`. Title = `salutation + full_name`; `company_name` beneath. Buttons: **Make Call** (`callEnabled && mobile_no`), **Delete** (`permissions.delete` → `DeleteLinkedDocModal`).
- **Side panel** (left, bottom): `SidePanelLayout` fed by `get_sidepanel_sections('Contact')`. Default = one section *Details*: `salutation, first_name, last_name, email_id, mobile_no, gender, company_name, designation, address`. **Every field is inline-editable** — ghost inputs, change → `document.save.submit()`. `useContactFields` rewrites `email_id`/`mobile_no` into `Dropdown` (PrimaryDropdown over the `Contact Email`/`Contact Phone` child tables) with add / edit / delete / set-primary via `crm.api.contact.create_new`, `set_as_primary`, `frappe.client.set_value`, `frappe.client.delete`, validated by `validateEmail`/`validatePhone`. `address` is a Link whose create/edit opens the Address modal. Managers get a pencil → `SidePanelModal`.
- **Tabs** (right): exactly **one** — *Deals*, count badge, `crm.api.contact.get_linked_deals`, rendered as a non-selectable `DealsListView` (organization, amount, status, email, mobile, deal owner, modified).
- **Finding:** Contact.vue presents **no activity, communication, email, comment, note, task, call or WhatsApp history at all**. Those tabs exist only on Lead/Deal. The contact record is identity + one linked-document list.

Verdicts: inline-edit-in-place side panel **PORT AS-IS** (shape only) — Massar's `vFactsPanel` already is this, with provenance the original lacks. Avatar upload **DROP**: no file store, no supplied images, and the monogram was already deleted from `vCustomer` as noise. Make Call **DROP** (no telephony). Delete **DROP**. Linked-documents tab **PORT ADAPTED** → *المحادثة* (`transcript[]`) + *الحملات* (`d.campaigns`).

## 5. Organizations.vue / Organization.vue

Identical skeleton; the record adds `EnrichFromWebsite`, open-website, logo upload, rename-on-edit (`beforeFieldChange` → `frappe.client.rename_doc` + route push) and two tabs (Deals, Contacts) via `createListResource` filtered on `organization` / `company_name`. Side panel: `organization_name, company_description, website, territory, industry, no_of_employees, address, linkedin, twitter, facebook`.
**DROP the whole entity** — missing dependency: Massar has no organization record. Substitute already present: the `orgProfile` prop (human-writable, import-seeded) plus the imported entity's `attrs`, which is also what feeds segments.

## 6. Proposed Massar structure (fields that exist today)

**قائمة العملاء** — header (title · count) · search (`custQ`, name/phone) · filter chips over real fields only: النتيجة (`outcome`, its 8 values), أوقف (`optedOut`), بيد البشر (`human`), تجريبي (`test`). Row: name (`waName` → entity name → «غير معروف») · `interestChips(tags)` · outcome chip · last delivery state from `statusTimes` · `lastEventAt` · phone (LTR). Row → `#customer/<phone>`. No bulk bar, no avatars, no like column.

**سجل العميل** (`#customer/<phone>`) — four regions:
A · الهوية: `waName`, phone, chips (`test`, `human`), `lastEventAt`, campaign-provenance line, whose-turn line.
B · ملف العميل: the six props with `source`/`by`/`ts` badge (حقيقة · قراءة · مستورد · ناقص), per-row pencil, `contested` line, disabled-with-reason when `propsWritable === false`.
C · الحالة: `outcome` + `outcomeEvidence` quote + `scheduledSaid` verbatim (`scheduledAt` marked advisory) + `tags` + the `statusTimes` timeline.
D · تبويبان: المحادثة (`transcript[]`) · الحملات. No third tab, no field that has no writer.
