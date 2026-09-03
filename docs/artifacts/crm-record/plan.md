# Plan — enrichable client record (`#customer/<phone>`)

Cycle `crm-record` · task #16 · `[planner]` · baseline `35a9e07` · contract: `requirements.md`
Correction carried: the read route is **`GET /admin/customer/:phone`** (`index.ts:338`), not `/api/contact/`.
`props` rides the `contact` object it already returns, so **AC-1's read half needs no new route.**

## 1. Slices (sequenced by risk-burndown, not by layer)

**S1 · Storage + the upsert trap.** `db.ts`: `ALTER TABLE contacts ADD COLUMN IF NOT EXISTS props JSONB
NOT NULL DEFAULT '{}'::jsonb;` (place immediately after the `contacts` CREATE — §90's warning: one ALTER
on a missing table aborts every later statement); `HydratedContact.props`; `loadAll` is `SELECT *` so it
comes free. `tracker.ts`: `PROP_KEYS`, `Prop`, `Contact.props`, `hydrate()` reads it back. **`props` is
never a parameter of `upsertContact` and never appears in its SQL** — not even COALESCE'd; not riding the
shared upsert is what makes the trap unreachable. AC-5. *Proof:* `node -e` on `dist/`: write props →
`recordInbound` + `recordStatus` → assert identical; plus a grep asserting the `upsertContact` SQL body
contains no `props`.

**S2 · `writeProp` + the gate (§2/§4 below).** `tracker.ts` only. AC-2, AC-3, AC-11. Ships *before* any
caller exists, so nothing can be written by a path the guard does not own. *Proof:* `npm run
check:props`, wired into `npm run check` in this slice and appended to by every later slice.

**S3 · The human write path.** `index.ts`: `POST /admin/contact/props` — same shape and auth as its three
siblings (`app.post`, `adminOk`, `{phone, props}` body, digit-stripped phone, 404 on unknown phone). BR-3
mapping to `outcome`/`outcomeReason` (never `opted_out`). Existing `/admin/contact/tags` re-routes through
`writeProp(..., {tags})`. AC-1, AC-4, AC-7, AC-10, AC-11, AC-12, NFR-1/2/3. *Proof:* boot locally with
`ADMIN_TOKEN` set and **`DATABASE_URL` unset** → PATCH must return `503 persisted:false`; boot with a
local Postgres → 200, then `GET /admin/customer/<phone>` shows the six keys and a seventh is rejected.
Curl only; no WhatsApp, no real number (use `9665000009xx`).

**S4 · The agent path.** `agent.ts` call sites re-routed (§2). BR-7d: human facts injected into context as
grounded truth. AC-2, AC-3, AC-6. *Proof:* gate's structural half + a send-spy run (stub `gupshup.send*`
to throw) asserting **zero** outbound on a full PATCH and on a rejected agent write.

**S5 · The panel.** `dashboard.ts`, anchored replacements only. Designer owns pixels; this plan fixes only
the seam: **do not rewrite `vCustomer` (1937–~2153, 216 lines).** Add a new sibling `vFactsPanel(d)` and
splice it in with ONE anchored concat above the `CRM STATUS REGION` marker. AC-9, AC-13. *Proof:*
`grep -c '^function \|^  function ' src/dashboard.ts` before/after (delta = exactly the new helpers),
`npm run check:numerals`, `npm run smoke`, RTL screenshots at 390 px and 1440 px.

**S6 · The dividend.** Confirmation-rate read (`prior` present ∧ value unchanged), test contacts excluded
(BR-6). Only after S1–S5 are green.

## 2. The `writeProp` guard (BR-7 — the highest-risk requirement)

```ts
export async function writeProp(
  phone: string, key: PropKey, value: unknown,
  source: "human" | "agent", by: string, opts?: { tags?: Tag[] },
): Promise<{ applied: boolean; persisted: boolean; reason?: PropReject; prop?: Prop }>
```
`PropReject = 'unknown_property'|'not_agent_writable'|'unknown_phone'|'too_long'|'human_value_wins'|'not_persisted'`.
Rejections evaluated in this order, each returning a *readable* value, never a silent no-op:
1. key ∉ `PROP_KEYS` → `unknown_property`, nothing written (NFR-2).
2. `source==='agent'` ∧ key ∈ {`note`, `orgProfile`} → `not_agent_writable` (AC-3).
3. contact unknown → `unknown_phone` (never manufactures a contact — `replaceTags` precedent).
4. NFR-1 length/date bounds → `too_long`.
5. stored `source==='human'` ∧ incoming `source==='agent'` ∧ value differs → `human_value_wins`; value/
   source/by/ts untouched, `contested` overwritten (latest only), `logEvent('prop_rejected:<key>')`.
   Identical re-inference → same reason, **no** `contested` churn.
6. empty/whitespace from a human → delete the key back to «ناقص», logged.

**Bypass-proofing, three layers.** (a) `Contact.props` is typed `Readonly<Record<PropKey, Readonly<Prop>>>`
so `c.props.note = …` is a *tsc error* outside `tracker.ts`, which mutates via a module-local cast.
(b) `props` absent from `upsertContact`. (c) The gate's structural half (§4).

**Call sites that must re-route:** `agent.ts:870` (addTag → also `productInterest`), `:894` (setSchedule →
`nextStep`), `:909`, `:928`, `:1079` (→ `disqualifyReason`); any new `decisionMaker` inference in
`insights.ts`; `index.ts:406` (human outcome → `disqualifyReason`, `source:'human'`), `index.ts:422`
(tags → `writeProp(..., {tags})`). **Explicitly NOT prop writers:** `agent.ts:1050` (opt-out is the
customer's right, BR-3) and `:1251` (turn-cap handoff is not a disqualification).

## 3. Persistence (NFR-3) — the divergence from `fire()`

```ts
export class NotPersisted extends Error {}   // db.ts
export async function upsertProps(phone: string,
  set: Record<string, Prop>, del: string[], tags?: Tag[]): Promise<void>
```
`if (!pool || !connected) throw new NotPersisted(enabled() ? "db_unreachable" : "no_database_url")` —
**it must throw, not return early as `replaceTags` does**, or the local-dev path pretends success. One
client, `BEGIN` → `UPDATE contacts SET props = (COALESCE(props,'{}'::jsonb) || $2::jsonb) - $3::text[]
WHERE phone=$1` → if `tags`, the `replaceTags` DELETE+INSERT body **inside the same transaction** →
`COMMIT`, `ROLLBACK` on throw. One commit is what makes BR-2 real: a crash between two commits would
leave tags corrected and provenance missing — a human fact rendering as a machine reading.
`rowCount===0` → `unknown_phone`.

DB first, memory second: on throw, memory is untouched, so a re-`GET` reads «ناقص» consistently rather
than showing a value that does not exist. Human write → `503 {ok:false, persisted:false, reason}`; UI
keeps the editor open with «لم يُحفظ — أعد المحاولة». **Agent writes are asymmetric:** a `NotPersisted`
is logged and swallowed — a conversation must never stall on the ledger (D2 below).
The `/admin/customer/:phone` payload gains `propsWritable = db.enabled() && db.isConnected()`; false →
editors render **disabled** with the reason stated. No `DATABASE_URL` locally is a visible disabled state,
never a green save.

## 4. New gate — `massar-engine/scripts/check-props.mjs` → `check:props`

Idiom of `check-optout.mjs`: behaviour half against `dist/`, **structure half against `src/`**.
The ONE thing it must falsify is the **single-door property**, structurally: *no module other than
`tracker.ts` writes `props`.* Chosen over the upsert trap and over the rejection matrix because a
behavioural test of `writeProp` passes at full green while `agent.ts` writes `c.props` directly — and
this repo has that exact defect, open and documented, in `check-optout.mjs`'s own closing NOTE ("~13
other call sites reach Gupshup directly"). The other two failure modes are *visible*: a nulled prop reads
«ناقص», a broken matrix fails AC-2/3. A bypass leaves a plausible value with the wrong provenance —
invisible on screen, and it makes the confirmation-rate metric circular, destroying the one honest number
this increment exists to produce.

Asserts: (a) behaviour — the six rejection conditions, a human value surviving an agent re-infer with
`ts` unchanged, `prior` populated on أكّد, plus a **negative control** (an agent write to a «ناقص» key
*is* applied); (b) structure — `src/` contains no `\.props\s*=` or `upsertProps(` outside `tracker.ts`;
`upsertContact`'s SQL contains no `props`; each named call site in `agent.ts`/`index.ts` contains
`writeProp`; the props route body contains no `gupshup.`/`agent.` (BR-4, AC-6); an `[inert]` FAIL if
`dist/tracker.js` exports no `writeProp`.

## 5. Risks, in the order that burns them down

| # | Risk | Burned down by |
|---|---|---|
| R1 | Agent silently overwrites a typed fact | S2 before any caller; gate's structural half |
| R2 | Props nulled by an unrelated event | S1: `props` never rides `upsertContact` |
| R3 | Local dev pretends a save succeeded | S3: `NotPersisted` throws; `propsWritable` disables editors |
| R4 | `dashboard.ts` ships blank | S5 last; ADR-0001 — anchored replacements, **no backticks**, doubled `\\` inside the template literal, definition-count audit, `npm run smoke` |
| R5 | `vCustomer` rewrite (216 lines) | Not rewritten: one anchored concat + a new sibling function |
| R6 | **`check-outcomes.mjs:123` slices 5200 chars from `CRM STATUS REGION`** | Insert the panel *above* that marker; a panel inside it pushes pinned assertions past the window and fails a green gate spuriously |
| R7 | Any send | BR-4 grep + send-spy; §8 stands — zero WhatsApp in this increment |

## 6. Non-goals (discovery §4)

Deal pipeline with amounts/probability/forecast · numeric lead score · email/calendar sync · workflow
builder · custom-property admin UI (the six are hardcoded; no seventh key) · assignment, permissions,
teammate activity feed · duplicate merge and company hierarchy · third-party enrichment. The 6-step
مرحلة البيع chip **shrinks, never grows**.

## 7. Decision briefs

**D1 — BR-2 as one transaction.** Stakes: a fact that renders as a guess. (a) `writeProp` takes
`opts.tags` and commits both in one tx — Completeness high, one new seam. (b) Route calls `replaceTags`
then `writeProp` — simpler, but a crash between them is silently wrong. **Recommend (a).** Net: +1
optional parameter for an atomicity guarantee the panel's entire credibility rests on.

**D2 — Failure asymmetry.** Human write → `503`. Agent write → log and continue. Rationale: a refused or
unpersisted agent inference is normal operation (BR-7c: "not an incident"); blocking a live Arabic
conversation on a ledger write is a customer-visible regression. **Recommend the asymmetry, stated in
code comments at both sites.**

## 8. Open questions (Orchestrator)

- OQ-1: `decisionMaker` is the only *new* agent inference (FR-1 has no existing source). Is adding a new
  LLM inference in the same increment that exists to distrust inferences the right order — or ship
  `decisionMaker` human-only in S1–S5 and add the reading in S6? *Planner leans: human-only first.*
- OQ-2: Independent-QA manifest `crm-record-props.json` is written but `armed:false` — needs the
  founder/approver record before it binds.
