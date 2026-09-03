# Requirements — enrichable client record (`#customer/<phone>`)

Cycle `crm-record` · task #14 · `[business-analyst]` · source: `discovery.md` §3, CPO ask
"yes CRM like hubspot please redesign it and add better indicators for users to enrich them".

## 1. The property set — exactly six (FR-1…FR-6)

One shared type: `Prop = { value, source:'human'|'agent', by, ts, prior?: {value,by,ts}, contested?: {value,by,ts} }`.
Stored in ONE new `contacts.props JSONB` column keyed by the six keys below. No seventh key.

| ID | key | Arabic label | type | agent may write | maps to |
|----|-----|--------------|------|-----------------|---------|
| FR-1 | `decisionMaker` | صاحب القرار | short text (name + role, one line) | YES (reading from transcript) | new; no existing source |
| FR-2 | `orgProfile` | المنشأة (فروع/حجم) | NO — import only | short text | `entities.attrs` (size/city/sector), reading with `by:'import'` |
| FR-3 | `productInterest` | الاهتمام | enum-set: catalogue product × `hot\|warm\|cold` | YES | `c.tags` (`addTag` writes, `replaceTags` corrects) |
| FR-4 | `nextStep` | الخطوة التالية | short text + optional date | YES | `c.scheduledSaid` (verbatim) + `c.scheduledAt` (reading) |
| FR-5 | `note` | ملاحظة | long text | NO — human only | new |
| FR-6 | `disqualifyReason` | سبب الاستبعاد | enum (`price\|no_need\|wrong_contact\|competitor\|no_response\|other`) + optional short text | YES | `c.outcome` ∈ {`not_interested`,`stopped`} + `c.outcomeReason` |

(FR-2's type is short text; `by:'import'` uses `source:'agent'` — the enum stays two-valued, `by` names the writer.)

## 2. Provenance state machine (FR-7)

States per property: **حقيقة** (`source:'human'`) · **قراءة** (`source:'agent'`) · **ناقص** (key absent).

- `ناقص → حقيقة` — operator types a value (PATCH; `source` forced to `human`, `by`=admin, `ts`=now).
- `ناقص → قراءة` — agent tool or import supplies a value.
- `قراءة → حقيقة` (أكّد) — value unchanged; `source:'human'`, `prior` = the agent reading. `prior` is
  what makes the confirmation-rate metric (discovery §3 dividend) computable.
- `قراءة → حقيقة` (صحّح) — new human value; `prior` = the rejected reading. Counts as a correction.
- `حقيقة → حقيقة` — human overwrite allowed; `prior` = the previous human value.
- **`حقيقة` + agent re-infers a different value → the write is REFUSED.** value/source/by/ts unchanged.
  The disagreement is stored once as `contested` (latest only, never a growing list) and rendered as a
  passive «قراءة مختلفة» line the operator may accept. *Justification:* (a) every accepted correction
  in this repo is the same defect — a machine asserting over a fact (discovery §2); (b) insights re-run
  on every refresh, so last-writer-wins makes typed facts evaporate non-deterministically; (c) if the
  AI can rewrite the label, the agreement rate is circular and the free eval set is worthless.
- **Any `upsertContact` from an unrelated event → props unchanged.** `props` is NOT a parameter of
  `upsertContact` and MUST NOT appear in its `ON CONFLICT DO UPDATE` clause; it is written only by
  `db.upsertProps(phone, props)`. `scheduled_said` needed COALESCE because it rides the shared upsert;
  props avoid the trap by never riding it. `hydrate()` reads `props` back into memory.

## 3. Business rules (each independently testable)

- **BR-1 (hard invariant).** No human-sourced value is ever replaced, cleared or reordered by a
  non-human writer. Only a request with the admin token and `source:'human'` may change one.
- **BR-2.** A human correction of FR-3 calls `replaceTags` with the full desired set — sufficient as a
  tag write (transactional, DB-before-memory, keeps unchanged products' `ts`). NOT sufficient for
  provenance: the same request must also write `props.productInterest` with `source:'human'`, else the
  panel cannot show حقيقة vs قراءة. Both, one request, DB first.
- **BR-3.** A human `disqualifyReason` sets `c.outcome='not_interested'` (`'stopped'` only when the
  reason is a customer-stated refusal) and `c.outcomeReason` = enum label + free text. It never sets
  `opted_out` — disqualification is our judgement; opt-out is the customer's right.
- **BR-4 (hard invariant, §8).** No enrichment path may send WhatsApp. The property route must not
  import or transitively call `gupshup.send*` / `agent.*`; checkable by grep plus a send-spy test
  asserting zero outbound calls for a full PATCH.
- **BR-5.** Every accepted write appends one `logEvent('prop:<key>', phone, …)` to the timeline.
- **BR-6.** Test contacts (`c.test`) accept props but are excluded from the confirmation-rate metric.
- **BR-7 (enforcement seam — where BR-1 actually lives).**
  (a) A single `tracker.writeProp(phone, key, value, source, by)` is the ONLY writer; `agent.ts` calls
  it and performs no source check of its own, so no future tool can bypass the rule. The guard is in
  code, never in the prompt (CLAUDE.md §4).
  (b) `writeProp` rejects when: stored `source==='human'` and incoming `source==='agent'`; or the key
  is human-only (FR-5) / import-only (FR-2) and `source==='agent'`. Rejection returns
  `{applied:false, reason:'human_value_wins'|'not_agent_writable'}` — a value the caller can read, not
  a silent no-op.
  (c) On rejection it writes `contested` (case one only) and logs
  `logEvent('prop_rejected:<key>', phone, reason)`; agent tool output receives the same reason so the
  model stops retrying. No alert/page — a refusal is normal operation, not an incident.
  (d) Human facts are injected into the agent's context as grounded truth, so the agent stops
  re-asking what the operator already answered.

## 4. Validation + failure modes (NFR)

- **NFR-1.** Short text ≤ 120 chars; `note` ≤ 2000; FR-6 free text ≤ 200; `nextStep.due` epoch ms in
  `[now − 1y, now + 2y]`. Over-limit → `400 {error:'too_long', key, max}`, no write. Empty/whitespace
  → explicit delete back to `ناقص`, logged; never a stored empty string.
- **NFR-2.** Unknown key → `400 {ok:false, error:'unknown_property', key}` with no partial write of the
  other keys in the body. Never silently dropped (emitted-values-must-be-readable).
- **NFR-3.** Silent failure is NOT acceptable here. `fire()` is fire-and-forget — correct for status
  telemetry, wrong for a typed fact, which is unreproducible: losing it makes the field read «ناقص»
  after the next hydrate and destroys the trust this panel exists to earn. Property writes use an
  awaited query, DB before memory (as `replaceTags` does), and return `200` only after commit. DB
  down/absent → `503 {ok:false, persisted:false}`; the UI keeps the editor open with
  «لم يُحفظ — أعد المحاولة». With no `DATABASE_URL`, editors render disabled with that reason stated.

## 5. Acceptance criteria (QA traceable)

1. **P0** (FR-1…6) `GET /api/contact/<phone>` returns `props` with only the six keys; a seventh key in a PATCH is rejected per NFR-2. Curl.
2. **P0** (BR-1/BR-7) PATCH `decisionMaker` as human, then run the agent inference path: value, `source:'human'` and `ts` unchanged; `contested` populated; one `prop_rejected` event. FAIL if the value changed.
3. **P0** (BR-7b) An agent-sourced write to `note` or `orgProfile` returns `applied:false, reason:'not_agent_writable'` and stores nothing.
4. **P0** (FR-7) Confirm a reading → `source:'human'`, `prior` holds the agent value/by/ts.
5. **P0** (upsert trap) After a PATCH, fire an inbound + status event, restart-hydrate, re-`GET`: all six props identical. FAIL on any nulled key.
6. **P0** (BR-4) Grep the route for `send`/`gupshup`; send-spy shows zero outbound calls on a full PATCH.
7. **P0** (BR-2) Human FR-3 correction rewrites `interest_tags`, preserves unchanged products' `ts`, and the chip renders حقيقة.
8. **P0** (NFR-3) With DB unreachable the PATCH returns `503 persisted:false` and the UI shows the retry line; nothing claims success.
9. **P0** (RTL) Panel renders `dir=rtl`: labels lead right, phone/date runs LTR-isolated with no bracket flipping, Arabic-Indic numerals pass `check:numerals`, no horizontal scroll at 390 px and 1440 px. Screenshot.
10. (BR-3) Human `disqualifyReason` sets `outcome`/`outcomeReason`; `opted_out` stays false.
11. (NFR-1) 121-char short text → `400 too_long`; empty value → key removed, field renders «ناقص».
12. (BR-5) Each accepted write appears once in the timeline naming key + writer.
13. (Discovery §3) A contact with all six missing shows six visible «ناقص» holes, each tappable — replacing the unrendered `contextScore` as the "what we're missing" indicator.

## Assumptions (unresolved, non-blocking)

- A-1 `orgProfile` stays free text; the org-hierarchy model is deferred (discovery §4). Verify: CPO.
- A-2 FR-6's six enum reasons are inferred from the existing outcome vocabulary, not stated by the
  founder; «other» free text is the escape hatch that will reveal a gap. Verify: first week of use.
- A-3 One operator → no per-user permissions; the admin token is the only authorization. Verify: CPO.
