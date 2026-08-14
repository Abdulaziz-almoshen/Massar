# ADR 0002 — Campaign attribution needs per-campaign status rows

**Date:** 2026-08-13 · **Status:** Accepted (constraint recorded; fix deferred)
**Owed to:** reviewer, three consecutive passes on the campaign-scoping work.

## The problem, as the founder met it

He launched a campaign and the tracker immediately reported «ردّوا ٢ · شوهدت ٢ · جهات مهتمة ١»
on two customers who had not opened it — and «فشل ٠» while both sends had in fact failed. His
words: *"just sent a campaign why this data is not real? the user hasnt seen it"*.

## Why it happened

`Contact.statusTimes` is `Record<string, number>` — **one latest timestamp per status, per contact,
for all time**. `tags` and `outcome` carry no campaign association at all. So a campaign's numbers
were read from lifetime state and every past success was credited to the newest send.

## What we did

Windowed every campaign number to that campaign's launch (`campWin`), and computed replies from
customer turns after the send rather than from the single lifetime timestamp.

## What that does NOT fix, and cannot

The window has a **start but no end**. A customer who replies 48 hours after a NEW campaign also
satisfies the window of every OLDER campaign that targeted them, so older campaigns silently
inflate on every new launch. This is not a patch away:

- `repliedIn` is bounded-fixable today, because the transcript has a per-message timestamp.
- `delivered` / `read` / `failed` are **structurally unbounded** — with one last-write-wins value
  per status there is no information in the ledger that distinguishes campaign A's delivery from
  campaign B's. Adding an end-bound would trade over-counting for under-counting, not fix it.

We deliberately did not add an end-bound for that reason. A wrong number that is wrong in a new
direction is not progress.

## The real fix, when campaign performance starts driving decisions

Per-campaign status rows: `campaign_contacts(campaign_id, phone, sent_at, delivered_at, read_at,
replied_at, failed_at, failure_reason)`. Statuses map by `destination` today, so the webhook handler
must resolve the open campaign for that contact and write the row. Then every campaign number is a
read of its own rows and no window arithmetic is needed anywhere.

## Until then

- Campaign numbers are **directionally right and bounded below**: a fresh campaign can no longer
  inherit an older reply. An older campaign may over-count.
- `scripts/check-campaign-scope.mjs` pins the behaviour, executing the shipped code against the real
  `created_at` shape (BIGINT returned as a digit string — the detail that made the first fix a
  silent no-op).
- **Do not add another window heuristic before this ADR is implemented.** Three rounds of patching
  this surface produced three new defects; the next change here should be the schema.
