# WhatsApp Campaign Engineering — Massar domain skill

The core how-to for working on `massar-engine/` (the deployed WhatsApp AI campaign engine)
and its Gupshup + OpenAI integrations. Load this before touching engine code, webhooks,
the agent, or ops.

## 1. System at a glance
- Deployed: Fly.io app **massar-engine** (fra, single always-on machine) →
  `https://massar-engine.fly.dev`. Health: `GET /health` (shows model, app name, source
  number, outbound readiness, config presence).
- Code: `massar-engine/src/` — `config.ts` (env), `gupshup.ts` (the ONLY wire-format file),
  `tracker.ts` (in-memory ledger — Postgres replaces it), `agent.ts` (Arabic salesperson),
  `queue.ts` (per-phone FIFO), `index.ts` (Fastify routes).
- Architecture doc (target design, DB schema §5, pacer §6, agent §7, tracker §8):
  https://claude.ai/code/artifact/11645969-2dcd-4515-8fba-5f00c3b48abd

## 2. Gupshup wire format (self-serve API, apikey header)
**Send session text** — `POST https://api.gupshup.io/wa/api/v1/msg`, form-encoded, header
`apikey`. Params: `channel=whatsapp`, `source=<our number>`, `destination=<digits>`,
`src.name=<app name>`, `message={"type":"text","text":"…"}`. Response
`{status:"submitted", messageId}`.
**Quick replies** (≤ 3 buttons): same endpoint,
`message={"type":"quick_reply","msgid":"…","content":{"type":"text","text":body},"options":[{"title":"…"}]}`.
**Template (opener)** — `POST /wa/api/v1/template/msg`, `template={"id":"<uuid>","params":[…]}`.
**Webhooks** — our endpoint accepts BOTH formats (the app's dashboard setting decides):
- v2 Gupshup envelope: `{app, timestamp, version:2, type:"message"|"message-event", payload}`.
  `message-event` payload.type ∈ enqueued|sent|delivered|read|failed|deleted; DLR events carry
  `gsId` + WhatsApp id in `id`; failed carries `{code, reason}`.
- **v3 / Meta format (CURRENT dashboard setting)**: WhatsApp Cloud API shape
  `entry[].changes[].value` with `messages[]` (text.body / button.text /
  interactive.button_reply.title) and `statuses[]` (`status`, `recipient_id`, `errors[]`).
  `value.metadata.display_phone_number` = OUR number → the engine auto-learns it.
Statuses map to the tracker by `destination`/`recipient_id` (user phone), not message id.

## 3. WhatsApp platform rules that bind every feature
- Business-initiated = approved **template** only; free-form only inside the **24h service
  window** opened by a user reply. Track `window_expires_at` before sending session text.
- Per-message billing since Jul 2025 (marketing dearest); ~2 marketing templates/user/day
  across ALL businesses → pacer must cooldown per contact and dedupe across campaigns.
- `read` receipts are user-controlled → tracker treats **replied ⇒ read** (`seen = read ∪ replied`).
- Number quality is an SLO: instant opt-out, quiet hours (Sun–Thu 09:30–17:30 Riyadh),
  ramp-up, tier ceilings (250 unverified → 1K → 10K → …).

## 4. The agent contract (hard rules in CODE, never only prompts)
- Opt-out pre-LLM: «إيقاف/ايقاف/توقف/لا تراسلني/الغاء…», STOP/unsubscribe → confirm once,
  `opted_out`, never message again. NEVER weaken this path.
- Turn cap 12 → polite close + handoff. `human` flag silences the agent (takeover).
- Tools: `tag_interest(product, level)`, `mark_not_interested(reason)`,
  `offer_alternative(product)` (allowlist only), `request_human_handoff(reason)`,
  `close_conversation(outcome)`. Tools write the tracker; the Signal Extractor (planned)
  classifies independently.
- Grounding: the FULL approved product KB is stuffed into the system prompt (no RAG yet);
  seed KB in `agent.ts` is placeholder until the معرفة المنتج module feeds it.
- Style contract: MSA Arabic, ≤ 4 lines, one question max, self-identifies as
  «مساعد لِين الرقمي», never promises discounts/dates/client names/medical advice.
- Models: `OPENAI_MODEL=gpt-5.6-terra` pinned; boot auto-pick fallback order 5.6-terra →
  5.6 → 5.x → 4.1. Cheap classification tier (luna/mini) reserved for the extractor.

## 5. Ops runbook
```bash
cd massar-engine
npm run build                              # strict tsc — must exit 0
npm run deploy                             # = fly deploy --ha=false && npm run smoke
# ^ ALWAYS deploy this way. `tsc` and `node --check` both pass on a bundle whose helpers were
#   deleted — that shipped a blank campaign page to production. `npm run smoke` loads seven real
#   routes in a browser and exits non-zero on an empty render, a missing landmark or any console
#   error. A deploy is not finished until smoke exits 0. One-time setup: `npm run smoke:setup`.
fly logs --app massar-engine --no-tail | tail -30
fly machine restart 48e40d2a0e1598 --app massar-engine   # clears in-memory state!
fly secrets set --app massar-engine KEY=value            # then deploy/restart to apply
curl -s https://massar-engine.fly.dev/health | python3 -m json.tool
# tracker snapshot (header auth):
curl -s https://massar-engine.fly.dev/admin/state -H "x-admin-token: $ADMIN_TOKEN"
# outbound smoke test (OWN opted-in phone only — real customers need human approval):
curl -s -X POST https://massar-engine.fly.dev/admin/send-test -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'Content-Type: application/json' -d '{"to":"9665XXXXXXXX","text":"تجربة"}'
```
- Webhook URL (registered in Gupshup): `https://massar-engine.fly.dev/webhooks/gupshup?token=<WEBHOOK_TOKEN>`;
  payload format set to **Meta (v3)**. GET returns "OK" for dashboard validation.
- Secrets live in `massar-engine/.env` (local, gitignored) + `fly secrets`. Restart wipes
  the in-memory tracker + learned app-name/number — that's expected until Postgres lands.

## 6. Current Gupshup app = SANDBOX
- App name `Massar`, source **917834811114** (Gupshup shared India sandbox number).
- Sandbox recipients MUST opt in first: send any WhatsApp message from the phone to
  +91 78348 11114; that also opens the 24h window. Wallet balance is charged for tests.
- Production migration (later, T3): dedicated KSA WABA number → update
  `GUPSHUP_SOURCE_NUMBER` + `GUPSHUP_APP_NAME`/keys, submit real templates, warm the number.

## 7. Next increments (architecture §11, in order)
1. Postgres ledger (`campaigns`, `campaign_contacts`, `events`, `interest_tags`,
   `messages`, `send_outbox`) replacing `tracker.ts`; keep the same event names.
2. BullMQ + Redis: outbox drain + pacer (tier ceiling, daily cap, quiet hours, per-user
   cooldown) for template blasts; keep the per-phone FIFO discipline.
3. KB feed: replace the seed KB constant with approved معرفة المنتج items per product.
4. Campaign API (create/launch/funnel/contacts) → dashboard screens from the prototype.

## منصة صحة — the context every conversation starts from

Added 2026-08-13 from the founder's own agent prompt v2. It was absent from every prior prompt and
from this skill, yet it is where a large share of real conversations begin.

Customers open with one of these, and the agent must handle each differently:
- **«هل أنتم من منصة صحة؟»** — answer from the approved knowledge FIRST, then ask why they asked.
  Do not issue a denial or an institutional description that contradicts the approved knowledge.
- **A problem inside the platform** — collect only enough to classify it: «هل التعطل في الإجراء
  داخل منصة صحة أم في الربط مع نظام المنشأة؟». If they refuse to give detail, do not defend the
  question and do not end the conversation — reframe to type-of-need. A complaint goes to
  `request_human_handoff`, and only after that may a commercial need be explored if it surfaces
  naturally.
- **Integration** — «نبغى تكامل» is a real buying signal: `tag_interest`, then ask only what is
  needed for the next step (which HIS/ERP), then offer the ten-minute specialist call.
- Licences and health procedures, manual re-entry, price, or a direct wish to buy.

Engineering consequence: the six-service catalogue in `agent.ts` does not name منصة صحة, so the
agent answers these from `hubKb` (the approved knowledge) and from the prompt's own guidance. If a
منصة صحة knowledge document is uploaded, it takes priority over everything else by the source order
in prompt §4.

## The sales journey the agent must follow (founder-defined, 13 Aug)

He graded the agent 3/10 and named the failure precisely: «ask question → ask another question →
transfer to specialist» is a support/router bot, not a sales agent. The required journey is:

**اشرح ← أهّل ← اكتشف ← أوصِ ← التقط ← احجز** — explain, qualify, discover, recommend, capture, book.

Rules that follow from it, all now enforced in `agent.ts`:
- **A message that is only a question is forbidden.** Explain with real substance from the approved
  knowledge first, then qualify in the same message.
- **«أرسلوا التفاصيل» is a buying signal, not a support ticket.** Answering an information request
  with «أُحيل طلبكم للمختص» is banned — it ends the conversation and advertises the bot's ceiling.
- **The human enters for**: final pricing, negotiation, a serious commercial meeting, or complex
  technical requirements. Never to avoid answering.
- **The first qualifying question is buttons** that identify the speaker in one tap:
  منشأة صحية · مزوّد نظام HIS · أريد العرض التجاري.

### The button contract (13 Aug — the rule, not an anecdote)

**Every reply button the system emits must be answered by the code that receives the tap.** It was
not, twice, and both failures were invisible until a human tapped:
- A 21-character title («أرسلوا تفاصيل التكامل») makes WhatsApp reject the WHOLE message with
  `131009 Parameter value is not valid` — an error that names no field. Cap is **20**.
- «العرض التجاري» was emitted by the launch path and matched by no intent pattern, so the button
  offering pricing routed the customer back to the qualifying question.

`src/templates.ts` now owns `BUTTON_INTENT` (title → info | commercial | qualify | decline) and
`assertButtonsHandled()`, called at boot from `index.ts`. Adding a button without an intent, or one
over 20 chars, refuses to start the process. Campaign templates live in the same file and are served
by `GET /admin/templates`, so the wizard preview and the wire read one registry — `{{1}}` is the
service variable, resolved on both sides.

**The correction that followed, and the real lesson.** The first version of that contract covered
only titles written in *code*, and the review proved the headline claim false: `send_buttons` lets
the **model** compose titles at runtime, so the largest source of emitted buttons was outside the
contract — and the system prompt itself prescribes «أريد العرض التجاري», which was not
«العرض التجاري» and routed nowhere. Tapping the pricing button the prompt asks for fell back to
«أي وصف يناسبكم؟». So:

> **Enumerate every emission site before claiming a contract is closed.** Ours had four: the two
> template registries, the launch fallback literal, the client fallback literal, and the model's own
> tool. A check that covers three of four certifies a subset and the uncovered one fails exactly as
> before.

`canonicalTitle()` closes it at the **emit** site: whatever the model proposes is mapped to an
approved title before it goes on the wire, and an unmappable one is dropped in favour of plain text.
Inbound matching stays exact, so a customer's own sentence can never be mistaken for a tap. Count
button length in **UTF-16 units** — that is what the adapter truncates on; counting code points lets
a title pass the check and still be cut on the wire into a string with no intent.

`scripts/check-buttons.mjs` (in `npm run check`, so it runs before `fly deploy`) executes the real
objective block sliced from `agent.ts` and the compiled `rungOne`, and prints a MEASURED value per
case. Prefer this to a boot-time crash as the primary gate: a static invariant enforced at boot fails
where the cost is an outage of the webhook that carries «إيقاف».

### The opener must survive into turn two
The campaign marker carries the template id — `[حملة:<id>]`, written and read through one exported
regex in `templates.ts`. Rung one reads it. This exists because the high-usage upsell opens with
«لاحظنا أن لديكم استخدامًا مرتفعًا» — we have just told the customer we know them — and the generic
rung one then asked «أي وصف يناسبكم؟». Every check tested the opener; none tested the next turn.
**When a campaign asserts something about the customer, every later turn must stay consistent with
that assertion.** The upsell's rung one qualifies on implementation («من يتولى الربط لديكم؟»).

### Templates and Meta (deferred by the founder; still true for the migration)
**Founder's decision, 13 Aug: treat templates as approved — do not gate work on this.** Retained
here because it becomes live again at the production-WABA migration, not before.

`sendTemplate()` puts `template: {id, params}` on the wire — **there is no field for body text**.
Meta substitutes parameters into the approved body it already holds. So an operator-edited body has
two possible fates on a production number: silently replaced by the approved text, or degraded to a
free-text session send (illegal outside the 24h window for a cold blast). The sandbox hides this
because it sends session messages. Every comparable tool (Gupshup, Twilio, WATI, Respond.io,
360dialog) locks the body at campaign creation and allows variables only. The wizard warns when the
body diverges; the durable fix is a read-only registry with `metaTemplateId` + approval status.

### Two engineering traps found while implementing this
1. **Silence is a possible reply.** The send was conditional on the model producing text; a turn
   spent entirely on tool calls sent nothing at all. `request_human_handoff` records state and
   returns a line for the MODEL to voice — it sends nothing itself, so banning the handoff *text*
   made silence the likeliest outcome. There is now a guaranteed fallback and an error log.
2. **A discovery gate can cause the very defect it prevents.** The first version told the model to
   ask a discovery question, which produced the interrogation. The constraint must enforce ORDER
   (explain then qualify), never silence.
