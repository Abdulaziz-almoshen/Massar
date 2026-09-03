# TODOS

## Work queue (slice A)

### Fold the customer's own stated time into the queue exit rule

**What:** When a contact filed as `later` carries `scheduledAt` (the agent's reading of the customer's words), hide the queue row until that time and show `scheduledSaid` verbatim as the reason.

**Why:** Slice A adds a rep-set follow-up store (`tasks.due_at`) beside one that already exists on the contact. The exit rule reads only the new one, so an AI-managed chat where the customer said «كلمني الأحد» resurfaces in the rep's queue too early.

**Context:** `massar-engine/src/tracker.ts` stores `scheduledSaid` verbatim and `scheduledAt` as an advisory reading, never shown as if the customer typed a date. The exit rule lives in `massar-engine/src/workqueue-domain.ts` (slice A) and takes the last tap and the follow-up date as inputs; this is one more input and one branch. Surface the phrase, never a bare date. Raised by the outside-voice review on 2026-09-03 (point 3).

**Effort:** S
**Priority:** P2
**Depends on:** slice A's `workqueue-domain.ts` exit rule shipped.

### Let the team stop maintaining the shared sheet

**What:** After the pilot, give the team a concrete reason to close the shared spreadsheet: either Massar writes seriousness, last contact, and next action back into the sheet's columns, or the sheet is retired once the CEO's pipeline view exists.

**Why:** Slice A imports the sheet into Massar but nothing flows back, so the sheet stays the team's source of truth and Massar is a second place to record. The weekly check-in question «هل فتحت الجدول؟» will be yes for structural reasons, not adoption ones.

**Context:** Write-back was Approach C in the 2026-09-03 office hours (declined as the whole product, still the cheapest bridge). A Google Sheets connector is a new dependency and a new credential; retiring the sheet needs the CEO reports that `docs/designs/massar-commercial-platform.md` gates on non-zero adoption. This TODO is the trigger for that gate. Raised by the outside-voice review (point 13).

**Effort:** M
**Priority:** P2
**Depends on:** slice A live for two weeks and the adoption count read once.

### Let a task link to an opportunity line

**What:** Extend `tasks.ref_kind` (CHECK constraint in `massar-engine/src/db.ts` and `REF_KIND`) to accept `opportunity`, and show line-linked tasks on the card in «فرص البيع».

**Why:** Slice A attaches follow-up tasks to the contact by phone because the constraint allows only `contact` or `campaign`. A follow-up about one product line of a two-line account is therefore account-level, and the board cannot show «الخطوة التالية: الثلاثاء» on the right card.

**Context:** The schema comment says a third kind must add a constraint, not a convention; this is that constraint. One migration (`ALTER TABLE tasks DROP CONSTRAINT … ADD CONSTRAINT …`) on a live schema in a public repo, plus a third link label on the tasks screen. Only matters once accounts carry several products. Raised in the 2026-09-03 engineering review (findings 7 and 12).

**Effort:** S
**Priority:** P3
**Depends on:** slice A shipped.

## Completed
