# 0001 — Edits to `dashboard.ts` are anchored replacements, never ranges

**Date:** 2026-08-12 · **Status:** binding · **Scope:** `massar-engine/src/dashboard.ts`

## Context

`dashboard.ts` is a ~1700-line server-rendered client bundle: the browser-side code lives inside
a TypeScript template literal, so **`tsc` and `node --check` both compile a file whose helper
functions have been deleted.** On 2026-08-12 a range-based edit (replace lines X..Y) removed five
helpers — `campStats`, `contactByPhone`, `seenOf`, `interestedOf`, `fmtD` — and the campaign detail
page shipped **blank to production**. Both static checks passed. Only a screenshot caught it.

The same class recurred a second time within the same day, which is what makes this a rule rather
than a postmortem note.

## Decision

1. **Anchored string replacements only.** Every edit to `dashboard.ts` matches an exact unique
   string and replaces it. No line-range rewrites, no regex substitutions across the file, no
   "rewrite the section from here to there". If an edit cannot be expressed as an anchored
   replacement, it is too big — split it.
2. **Definition-count audit on every commit that touches the file.** Count function definitions
   before and after; the delta must be exactly what the change intends. Record it in the commit's
   evidence:
   ```bash
   grep -c '^function \|^  function ' src/dashboard.ts
   ```
3. **`npm run smoke` after any deploy that touched it** — the render assertion is the only check
   that catches this class.
4. **No backticks anywhere in this file's comments or strings.** The client code sits inside a
   TypeScript template literal, so a backtick in a prose comment — e.g. writing `` `test` `` to
   mean the field named test — closes the literal and the file stops parsing. This happened on
   2026-08-12 and failed a deploy at the Docker build step (`TS1005: ',' expected`). Use «» or
   plain words instead. Unlike a deleted helper, `tsc` DOES catch this one — but only after a
   full image build, so it costs a deploy cycle.

## Consequences

Edits are slower and more numerous. That is the intended trade: the failure mode is a silently
blank production page on a screen the founder demos, and neither of the two automated checks in
the build can see it.
