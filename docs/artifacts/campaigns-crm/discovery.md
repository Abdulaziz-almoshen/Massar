# Discovery — the campaigns module inside the Frappe CRM shell

Cycle `campaigns-crm` · `[product-discovery]`

## 1. Outcome

Not "look like Frappe." **The operator goes from the campaign list to a named sub-cohort and its next
action without leaving the module — and every number he hands a rep is one the engine measured.**
Metric: share of retargets that start from an explicitly selected subset rather than an all-or-nothing
filter. Today that share is structurally 0% (§3).

## 2. Job to be done

**When a campaign has run and I open it, I want to see exactly what we sent and who did what with it,
so I can hand a rep a specific list today — without being embarrassed by a number the screen
invented.** Emotional half: the CRM shell is bought for *legitimacy*; it must read like a system of
record, not a dashboard.

## 3. Evidence (repo-inferred, honestly labelled)

- `vKmonDetail` (dashboard.ts:683–766) renders name, product, date, six stat cards, next-move cards, a
  6-filter targets table. **It never renders `camp.message`** — `campMsg` is wizard-only state (line
  885). You cannot see the text you sent from the screen reporting on it.
- `startRetarget()` acts on `lastDetailCohort` = the *whole current filter* (749–757). Picking 12 of 40
  «شوهدت دون ردّ» is impossible.
- `#kmon` already has tabs, search, 3-way sort, CSV, `LIST_CAP` with declared remainder (566–651). The
  list is not the weak surface; the campaign **record** is.
- A campaign is 6 fields (id, name, product, message, created_at, test) + derived `campStats`.

## 4. Port these three

1. **`ListBulkActions` — row selection + bulk actions.** Highest value: turns the targets table from a
   report into a work queue. Every bulk action routes through the §8 approval gate — bulk *is* blast
   radius, and NO-SEND still holds.
2. **`Deal.vue` tabs-in-main + resizable rail — on the CONTACT record.** On campaign detail the rail
   holds only the immutable launch spec: message body, product, audience, date, test flag. Fixes hole one.
3. **`LayoutHeader` breadcrumbs + one solid Create** — cheap, and settles today's competing
   ghost-CSV/dark-Create header.

## 5. Do NOT port

Kanban or `group_by` of campaigns (no stage lifecycle; a board of a few dozen launches is a toy) ·
`WhatsAppBox.vue`'s composer (a send affordance under NO-SEND) · doc-id row · assignment, owner,
@mentions, permissions (one operator) · Tasks/Notes/Email tabs · custom-field admin · a quick-entry
Create modal (creation is a gated wizard; one-click Create that can blast is the worst possible port) ·
and per Rule 3, none of Frappe's palette or frappe-ui chrome — pattern only, re-expressed navy/teal/gold
RTL. **Do not re-implement `campStats`/`campWin`/`seenSilent` in Vue** — extract and import. Round-22
killed invented numbers once; a parallel reimplementation brings them back.

## 6. Riskiest assumption

**That a campaign is a *record*.** Frappe's shell assumes an editable doc with many properties; a
campaign is an immutable past event with a cohort. Ported literally we ship a rail of fields that look
writable and aren't — the "emitted values must be readable" defect, inverted. The bet: **the contact is
the record; the campaign is a cohort plus a report.**

## 7. Cheapest test (before any Vue)

**Field census — 20 minutes, zero code.** List every campaign field the API returns; strike those already
in the header and every derived stat. **PASS** at ≥5 real fields left → build the rail. **FAIL** (<5) →
the rail is decoration; ship a collapsed spec strip and give the width to the targets table. Then one row
test: one real campaign in the mirrored shell beside today's `#kmon/<id>`; PASS if the founder names ≥1
rail field he would act on.

**Surprise dividend:** bulk selection makes the cohort a first-class, named, exportable object — "أعد
استهداف ٤٠ جهة" becomes an auditable list with a decision attached, the prerequisite for ever trusting an
18,000-contact blast.

*Rejected en route:* forking Frappe's Python backend · widgets bolted onto #kmon · a token-only reskin ·
Kanban-first campaign board.
