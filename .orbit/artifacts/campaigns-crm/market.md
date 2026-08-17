# Prior-art scan — Frappe CRM (read from source, shallow clone)

Source of every claim below: the cloned tree at `scratchpad/frappe-crm`. No web claims.

## 1. WhatsAppArea.vue / WhatsAppBox.vue — transcript + composer

**Area** = the transcript renderer. `v-for` over `messages`, one bubble each; `type == 'Outgoing'`
flips the row (`flex-row-reverse`). Per-bubble: failed badge; quoted-reply block (click →
`scrollToMessage`, smooth-scroll + 1s yellow highlight); a `content_type` switch
(text / button / image / document / audio / video) plus a `message_type == 'Template'` branch that
renders header/body/footer; hover dropdown (Reply — Forward/Delete commented out); emoji reaction
pinned below the bubble; time + tick state (`sent`→single, `delivered|read`→double, blue on read).
`formatWhatsAppMessage` re-implements WhatsApp markup (`_i_ *b* ~s~ ```code``` > quote`, bullets,
`\n`→`<br>`) then `sanitizeHTML`.

**Data shape** (from `crm/api/whatsapp.py:get_whatsapp_messages`): flat array of `WhatsApp Message`
rows — `name, type(Incoming|Outgoing), to, from, content_type, message_type, attach, template,
use_template, message_id, is_reply, reply_to_message_id, creation, message, status,
reference_doctype, reference_name, template_parameters, template_header_parameters`. Threading is
resolved **server-side** by matching `reply_to_message_id → message_id`, injecting
`reply_message/reply_to/reply_to_type/reply_to_from`; reactions are messages with
`content_type == 'reaction'` folded onto their target and filtered out of the return.

**Box** = composer: attachment dropdown (document/image/video), emoji picker, autogrow textarea,
Enter-to-send, reply banner. Posts `crm.api.whatsapp.create_whatsapp_message`.

**Verdict — reuse the model, build the code.** Massar's `renderConvo` items are
`{role, text, ts}` — no `message_id`, no per-message `status`, no `content_type`, no reply link.
Three concepts are worth copying into the ledger, not the Vue: (a) stable per-message id +
`reply_to_message_id` so quoting/threading is possible at all; (b) per-message delivery status
rendered as ticks rather than a contact-level status; (c) template messages rendered as
header/body/footer with parameters substituted server-side — Massar sends templates and today shows
them as plain text. **Do not** port `formatWhatsAppMessage` (regex HTML on an RTL/Arabic string is a
sanitiser and bidi hazard) or the composer (§8: no sends).

## 2. ViewControls.vue — the exact UX contract

**Route is the state.** `route.params.viewType ∈ {list, group_by, kanban}`, `route.query.view` =
saved-view id. Switching type = `router.push(params.viewType)`; picking a saved view pushes both.
Deep-linkable, back-button correct, zero local view state.

**Desktop bar, left→right:** quick-filter chips (scrollable) │ divider │ [Cancel][Save Changes]
(only when dirty **and** a saved view is active **and** (private or manager)) │ Refresh │ GroupBy
(group_by only) │ Filter │ Sort (hidden on kanban) │ KanbanSettings *or* ColumnSettings │ ⋯ (Import,
Export, Customize Quick Filters). Mobile = same controls, two rows. A third mode replaces the whole
bar: manager-only quick-filter customiser (draggable chips + Add Filter + Save/✕).

**The view picker is not in this component** — `defineExpose` hands `viewsDropdownOptions`,
`currentView`, `viewActions` to `ViewBreadcrumbs` in the page header. Groups: Standard / Saved /
Public / Pinned / Create View. Per-view: Set as Default, Duplicate, Edit, Pin, Make Public, Delete.

**A saved view stores** (`CRM View Settings`): `label, icon, user, is_standard, is_default,
type, dt, route_name, pinned, public, filters(JSON), order_by("modified desc"),
load_default_columns, columns(JSON), rows(JSON), group_by_field, column_field, title_field,
kanban_columns, kanban_fields`.

**Dirty rule (the subtle part):** every update* sets `viewUpdated`. With **no** `?view=`, changes are
auto-persisted per-user via `create_or_update_standard_view` — silent, no prompt. With a saved view,
the Save/Cancel pair appears; Save opens ViewModal in `edit` mode; column edits on a *private* view
auto-persist anyway.

**One data endpoint:** `crm.api.doc.get_data` returns `{data, columns, rows, fields, column_field,
title_field, kanban_columns, kanban_fields, group_by_field, page_length, page_length_count,
is_default, views, total_count, row_count, view_type}`. `columns` = display meta
(`label,type,key,width,align,options`), `rows` = fieldnames to fetch. Cache key
`[doctype, ?view, viewType]`. Filters serialise as `{field: value}` or `{field: [op, value]}`;
`like` auto-wraps `%…%`, `in` splits on comma, `between` is a pair, `timespan` is named.
group_by is **not** a renderer — same list, server appends the field to `rows`.

**Verdict — build, port the contract.** Vue/frappe-ui/DocType meta is unusable in Massar's
server-rendered `dashboard.ts`. Port: route-as-state, control order, the single `get_data`-shaped
payload, the `columns`/`rows` split, the filter serialisation, and the standard-vs-saved dirty rule.
RTL flips the order and `flex-row-reverse` must be dropped, not mirrored.

## 3. Campaigns / bulk messaging — no.

There is **no** campaign, broadcast, sequence, or bulk-send concept. `ListBulkActions.vue` offers
Edit, Delete, Assign To, Clear Assignment, Convert to Deal — nothing outbound.
`composables/useBroadcast.js` is a `window`-event/localStorage bus, not messaging. WhatsApp sends are
strictly one message to one record.

`frappe/whatsapp` **is** referenced but never vendored: README credits
`https://github.com/shridarpatil/frappe_whatsapp`; `crm/api/whatsapp.py` guards on
`"frappe_whatsapp" not in frappe.get_installed_apps()` and on `frappe.db.exists("DocType",
"WhatsApp Message")`; `crm/hooks.py:182` hooks `WhatsApp Message` doc events. So the doctype, the
BSP wire format and templates all live in the external app — the CRM only renders and links.

**Verdict — nothing to reuse for campaigns.** Massar's engine is ahead of Frappe CRM here; the gap
is real and this repo is not a substitute. Its value to us is the view layer only.
