# P4 — merging frappe_whatsapp with the Massar campaign engine

Read from source: `crm/api/whatsapp.py`, `crm/hooks.py:182`, `components/Activities/WhatsAppArea.vue`,
`WhatsAppBox.vue`. The `WhatsApp Message` doctype itself lives in the EXTERNAL `frappe_whatsapp`
app (credited in the README, never vendored); the CRM only renders and links it.

## The two systems are not competitors — they solve different halves

| | Frappe CRM + frappe_whatsapp | massar-engine |
|---|---|---|
| Unit of work | ONE message to ONE record | a CAMPAIGN to a cohort |
| Who writes the reply | a human, in a composer | an Arabic AI agent, autonomously |
| Sending | `create_whatsapp_message` / `send_whatsapp_template`, one row at a time | outbox + pacer, template launch, frequency caps |
| Consent | none in the CRM layer | opt-out enforced in code, «إيقاف» sacred, turn caps, 24h window |
| Delivery truth | `status` per message row | `statusTimes{sent,delivered,seen,failed}` per contact + campStats |
| Linking | `get_contact_lead_or_deal_from_number` resolves a phone to a record | contact IS the phone |

**Verdict: our engine is strictly ahead on everything that makes a campaign safe** — pacing,
opt-out, caps, the agent, delivery aggregation. Frappe has no campaign concept at all.
**Their message MODEL is ahead of ours**, and that is the merge.

## What to take — four concrete items, all data-model, none UI

1. **Per-message identity (`message_id`) and per-message `status`.**
   Ours: `transcript[] = {role, text, ts}` with delivery status held at CONTACT level. So we cannot
   say which message was delivered, only that something was. Theirs carries id + status per row.
   *Take it:* add `id` and `status` to transcript items. Unlocks per-bubble tick marks (single =
   sent, double = delivered, blue = read) instead of one contact-level chip.
   *Cost:* a tracker write path change + a migration for existing rows (backfill `status: null`,
   never invent a status we did not observe).

2. **`reply_to_message_id` → quoted replies.**
   Theirs resolves threading SERVER-side and injects `reply_message`/`reply_to`. Ours has no notion
   of a reply target, so a customer answering an older question reads as a non-sequitur in the
   transcript. *Take the field and the server-side resolution.* Requires (1) to be useful.

3. **Template as a first-class message type.**
   Theirs: `message_type: "Template"`, `use_template`, `template`, `template_parameters`,
   `template_header_parameters`, rendered as header/body/footer. Ours SENDS templates but STORES
   and renders the rendered text flat, so the campaign record cannot show which template was used
   or which variables were substituted. *Take the shape* — it makes «شريط الإطلاق» show the real
   template structure rather than one interpolated string.

4. **Auto-link a number to a record on inbound** (`crm/api/whatsapp.py:validate` →
   `get_contact_lead_or_deal_from_number`). We already do this implicitly (contact IS the phone),
   so this is **already satisfied** — recorded here so nobody ports it twice.

## What NOT to take

- **`WhatsAppBox` composer** — a free-text send affordance. The standing rule is ZERO sends; a
  composer in the UI is the single most dangerous thing in this repo to port. DROP.
- **`react_on_whatsapp_message`** — reactions are a real WhatsApp feature but nothing in Massar
  reads them, and adding an outbound reaction is an outbound message. DROP.
- **`ALLOWED_WHATSAPP_ROLES` / permission gating** — Massar has one operator and one admin token.
  Porting a role system to guard a single user is ceremony. DROP.
- **`formatWhatsAppMessage`** — regex-to-HTML over message text. On Arabic/RTL this is both a
  sanitiser hazard and a bidi hazard, and we already strip `**` on the way out. DROP.
- **`frappe_whatsapp` itself** — it is a Frappe app on Python/MariaDB talking to Meta directly.
  Massar goes through Gupshup with its own wire format in `src/gupshup.ts`. Adopting the app means
  a second stack and a second BSP path. DROP; take the model, not the app.

## Order

(1) per-message id + status → (3) template shape → (2) reply threading. Each is independently
useful; (2) is the only one that needs another to land first. All three are ledger changes with a
UI consequence, so each needs a migration that backfills honestly — an unknown status stays
unknown, never a guessed «delivered».
