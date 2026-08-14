# [reviewer] Technical review — audience slice (874a130 + 0eafcd3, base bbe40dd)

> **Superseded verdict — see "Re-review @48bba0c" at the bottom: 8.5/10 PASS.**
> Original review kept intact below for the record.

**Score: 7/10 — FAIL vs the ≥8 bar → BLOCKED (2 must-fixes, both small)**

Technical review: 12 issues (2 critical, 10 informational) · quality 7/10
Scope check: the diff builds exactly what was asked (file import → schemaless attrs → derived
segment picker → capped previews → template download), no creep. All three round-6 folds present
and correct. Everything below was verified against the code or by live repro against the
installed `xlsx@0.18.5` and the compiled `dist/` — repro commands run in-repo, tsc exit 0.

---

## MUST-FIX (blockers)

### 1. Numeric Excel phone cells import silently corrupted (scientific notation) — CRITICAL, confidence 10/10 (live repro)
`src/audience.ts:67` reads with `raw: false`, which hands the parser the *formatted* cell text.
A phone typed as a plain number in Excel — `966512345678`, General format, i.e. the default when
a KSA user types the full international form without a leading apostrophe (and what `+9665…`
becomes, since Excel eats the `+` as a formula) — is formatted as **`"9.66512E+11"`**.
Then `src/audience.ts:33` strips non-digits → **`"96651211"`** → 8 digits → **passes** the
`phone.length < 8` gate at `src/audience.ts:90` → imported with zero skip reason.

Repro (run against dist, exact output):
```
formatted grid row: ["عميل رقم-966 كرقم","9.66512E+11","الرياض"]
parsed row:        {"name":"عميل رقم-966 كرقم","phone":"96651211", ...}   skipped: []
```
This is the primary onboarding path, and corrupt rows are indistinguishable after import — at
400k-file scale the ledger silently accumulates permanently unreachable contacts. (The 05-typed
variant is fine: Excel drops the leading 0 → 9 digits starting 5 → rescued by the bare-5 rule.
Text cells are fine. Only number-typed full-international corrupts — the common case.)

**Required fix (small):** read the sheet a second time with `{ header: 1, defval: "", raw: true }`
and take the *phone cell only* from the raw grid (`String(966512345678)` is exact, < 2^53);
belt-and-braces: any formatted phone value matching `/\d[eE]\+\d/` gets skipped with a reason
instead of normalized.

### 2. Paste quick-add bypasses phone normalization while phone is now the upsert identity — CRITICAL (data integrity), confidence 9/10
`src/index.ts:101`: `const phone = (parts[1] ?? "").replace(/\D/g, "");` — no KSA rewrite, no
Arabic-digit mapping. The file path stores `966512345678`; pasting the same customer as
`0512345678` stores `0512345678`. With `ON CONFLICT (phone)` as the identity (`src/db.ts:224`)
that is **two rows for one human** — double-targeted by campaigns, split tracking, and one of the
two is an invalid send destination. The dropzone card shipped in this diff promises the opposite
in the same breath (`src/dashboard.ts:787`: «أرقام 05 تُحوَّل تلقائيًا إلى صيغة 966») and the
paste `<details>` sits inside that same card. (Arabic-digit paste lines at least fail visibly
into `bad[]`; `05…` lines corrupt silently.)

**Required fix (one line + import):** use `audience.normalizePhone(...)` in the paste handler.

---

## SHOULD-FIX

3. **Greedy header candidate `"رقم"` mis-maps CR-number columns** — repro: headers
   `["الاسم","رقم السجل","الواتساب"]` → phone column = **رقم السجل** (CR numbers like
   `1010456789` pass the ≥8 gate and import as phones) while the real WhatsApp column is demoted
   to a segment attr. Cause: substring pass at `src/audience.ts:24-27` scans candidates in
   PHONE_HEADERS order and bare `"رقم"` (index 5) precedes `"واتساب"` (index 6). Mitigated by the
   detected-columns echo in the import summary, but Saudi B2B sheets carry «رقم السجل/رقم
   السجل التجاري» routinely. Fix: move specific candidates before bare `"رقم"` in the substring
   pass, or sanity-check that the chosen column's values mostly normalize to plausible phones.
4. **`9660512345678` (966+05 double-prefix, a common KSA data-entry mistake) passes through
   unchanged** (`src/audience.ts:34-37`, probed) → garbage destination that looks valid. Add
   `96605…→9665…`. Same family: leading-0 non-05 numbers (`0112345678` landline) import as-is
   with the leading zero.
5. **5000 sequential single-row upserts** (`src/db.ts:220-233`): ≈5000 DB round-trips per import
   (est. 5–15s Fly↔PG) behind a static spinner, non-transactional (a mid-file DB failure leaves a
   partial import with no marker — remaining rows counted as `skipped`). Parse itself is fast
   (measured 159ms/5000 rows, 956KB file). Fix: multi-row `VALUES` chunks (e.g. 500/statement)
   inside a transaction; also surfaces progress less badly by finishing in <1s.
6. **Stale invisible filter**: `entFilters[key]` persists after its chip group leaves the top-6
   slice (`src/dashboard.ts:464`) or its carriers are deleted; `entMatches` still applies it
   (`src/dashboard.ts:473`) with no visible chip to clear → audience counts silently shrink.
   Multi-file imports accumulate attr keys (merge semantics), so >6 keys is a matter of time.
   Fix: on render (or in entMatches), drop entFilters keys not present in current segGroups().
7. **API naming/visibility**: import response carries both `skipped` (DB failures, from
   `...res`) and `skippedCount` (parse skips) — near-identical names, different meanings
   (`src/index.ts:120-126`); the UI shows only `skippedCount`, so DB-level failures are invisible,
   and `catch { skipped++; }` (`src/db.ts:232`) discards the cause. Rename (`dbErrors`) + surface.

## NICE-TO-HAVE

8. Persian/Urdu digits (U+06F0–06F9) collapse to `""` → row skipped *with* a visible reason
   (probed) — mapping them is one more range in the same replace (`src/audience.ts:33`).
9. Template example rows import as real entities if the user forgets to delete them (round-trip
   probed: 3 rows, `966512345678` etc. — plausibly real numbers). Skip rows whose name contains
   «مثال», or use reserved-invalid phones in the template (`src/audience.ts:44-46`).
10. Legacy cp1256 Arabic CSV fails **loudly** with the mojibake header echo (probed — good), but
    the 422 could append a hint: «احفظ الملف بصيغة CSV UTF-8».
11. Launch modal warns at >50 but the confirm button stays enabled → server 400 surfaces an
    English error via alertBar (`src/dashboard.ts:515` + `src/index.ts:148`). Disable confirm
    above the cap (or slice at 50 client-side with a note).
12. `esc()`d strings are passed into `alertBar`, which uses `textContent`
    (`src/dashboard.ts:515,525`) — special chars in server errors display as literal `&…;`
    entities. Drop the esc there (textContent is already safe).

---

## Verified-pass evidence (what was checked and held)

- **XSS — every file-derived sink escapes** (checked one by one): attr chip value + `title`
  (`dashboard.ts:481`), wizard group labels (`:548`), chipBtn labels incl. file values+counts
  (`:487`, `:550`), customers meta segment names (`:802`), import summary columns/attrs
  (`:764-765`), skipped-row reasons which embed raw cell values (`:768`, escaped at render),
  entity name/phone in picker and customers rows (`:567-569`, `:809-813`), campMsg preview
  escaped *after* `{name}` substitution (`:581`), `alertBar` uses `textContent` (`:525`),
  `entImportSummary` re-injected HTML is built exclusively from esc'd pieces (`:761-770`).
  No unescaped sink found.
- **Template-literal hazards: none.** Zero `${` and zero interior backticks in the whole
  literal (grep), extracted page JS (58,081 bytes) passes `node --check`, `npm run build` exit 0.
- **onclick index round-trip is deterministic**: render and click both recompute `segGroups()`
  from the same in-memory `entities`; stable ES sort + Map insertion order (server `ORDER BY
  name`); `entities` is only replaced synchronously-then-rerendered (`:751-777`), and the 5s
  poll does not touch `entities` on `#aimkt` (`:883-887`). Guard `if (!g) return` covers the
  empty case (`:492`).
- **attrs merge semantics** (`db.ts:228` `entities.attrs || EXCLUDED.attrs`): new values win on
  conflict, absent keys persist (accumulative by design — means re-imports can never *remove* an
  attr; only entity delete resets. Accepted, noted for the ledger). Legacy size/city fold at read
  with file attrs taking precedence (`db.ts:206-213`) — consistent both ways.
- **`xmax = 0` insert-detection** (`db.ts:229`) is valid on stock Postgres; added/updated counts
  correct (dup phones *within* one file count the second row as "updated" — cosmetic).
- **Launch cap enforced server-side** (`index.ts:148`, `> 50 → 400`), modal warning consistent
  with it; sends remain human-confirmed; opt-out check intact in the launch loop
  (`index.ts:161`).
- **Resource bounds**: multipart capped 25MB/1 file (`index.ts:15`); row cap 5000 applied before
  the DB loop (`audience.ts:82`); realistic-cap parse 159ms (measured) — the sync `XLSX.read`
  event-loop stall is only reachable via a pathological ≤25MB file on an admin-token surface
  (informational; the 5s state poll + full-entity refetch is the already-sanctioned
  pagination debt, untouched here).
- **Round-6 folds verified**: convoSig now includes statusTimes keys + tags (`dashboard.ts:
  338-339`); setHuman guards `res.ok` + network catch before refresh (`:320-327`); exactly one
  `window.pick` remains (`:502`).

## Verdict

**BLOCKED — 7/10.** The slice is well-shaped: tight scope, data-driven segmentation with a
sound index-only onclick contract, disciplined escaping (a full sink audit found nothing), the
capped-preview pattern is the right MVP step for scale, and the whole flow carries live browser
evidence. But the feature's core promise — "upload your file as-is and every contact becomes
reachable" — has a verified silent-corruption path for the most common way Saudi users type
international phone numbers in Excel (number-formatted cells → scientific notation → 8-digit
garbage that passes validation), and the paste path undermines the new upsert-by-phone identity
with un-normalized numbers while the same card promises normalization. Both fixes are small and
surgical (a raw-grid read for the phone column + one normalizePhone call); with them landed and
a one-file re-import spot-check, this re-scores comfortably ≥8.5 and hands to QA clean.

---

# Re-review @48bba0c (HEAD 120058c) — 2026-08-11

**Score: 8.5/10 — PASS (≥8). No remaining blockers on the audience slice.**

All four claimed fixes independently re-verified: I read the diff (`git show 48bba0c --
src/audience.ts src/index.ts`), rebuilt (`tsc` exit 0), and re-ran my original repros **plus
new probes targeting the fix code itself** against the fixed `dist/`. I did not rely on the
builder's recorded outputs.

## Fix verification (all confidence 10/10, live repro)

1. **MUST-1 fixed — numeric-cell sci-notation corruption.** `src/audience.ts:75-77` adds a
   second `raw: true` grid; `:97-104` takes the phone from the raw cell when it is a finite
   number (`String(Math.round(raw))` — exact for integers < 2^53) and skips any phone source
   matching `SCI_NOTATION` with reason «جوال بصيغة رقمية تالفة (…) — نسّق العمود كنص».
   Re-run: numeric-typed `966512345678` → `"966512345678"` exact (was `"96651211"`); literal
   text `"9.66512E+11"` → 0 rows, skip reason as specified; numeric 05-lost-zero `512345678`
   still rescued; text cells untouched (leading zero preserved — the raw path correctly applies
   only to number-typed cells).
   *Fix-specific probes that also held:* blank row between data rows does **not** desync the
   two grids (both `header:1` reads include blank rows identically — R2 repro); a ≥1e21
   pathological number stringifies to `"1e+21"` and is caught by the same guard; a date-typed
   phone cell becomes a short serial → skipped by the length gate with the formatted value in
   the reason.
2. **MUST-2 fixed — paste path shares the identity rules.** `src/index.ts:103` now calls
   `audience.normalizePhone(parts[1] ?? "")` (comment states the upsert-key rationale). Paste
   `0512345678` ≡ file-imported `966512345678` — one row per human; Arabic-digit paste lines
   normalize instead of collapsing to invalid.
3. **SHOULD-3 fixed — greedy «رقم» demoted.** `src/audience.ts:10-12`: bare `"رقم"` moved
   last with an explanatory comment. Repro: `[الاسم, رقم السجل, الواتساب]` → phone column =
   **الواتساب**, `رقم السجل` lands as a segment attribute. Probe: a sheet whose only phone
   column is literally «رقم» still maps via the exact pass (unaffected by candidate order).
4. **SHOULD-4 fixed — 9660 double-prefix.** `src/audience.ts:36-37`: 00-strip is now
   unconditional and first, then the 13-digit `9660…` rule. Probes: `9660512345678` →
   `966512345678`; chaining `009660512345678` → `966512345678`; landline-form
   `9660112345678` → `966112345678` (sensible); full regression matrix (05/bare-5/Arabic
   digits/`00966`/`+966`/short-code) unchanged — and `005XXXXXXXX` now *improves* to
   `9665XXXXXXXX` (old code returned it unprefixed).

Hygiene at HEAD (120058c — home-card footer + `notifyNumber` on `/admin/state` only, confirmed
by full diff): `npm run build` exit 0; served page JS (66,313 bytes) passes `node --check`;
still zero `${` inside the dashboard template literal; template round-trip still clean.

## Deferral ruling on the remaining items — CONFIRMED, with one caveat

- **SHOULD-5 (batch upserts)** — defer OK: import is admin-only/infrequent, bounded at 5000
  rows; tie it to the server-side segmentation/pagination epic (same "400k answer" work).
- **SHOULD-6 (stale invisible `entFilters` key)** — defer OK, **with a caveat**: the growth
  slice's retargeting cohort-lock adds more filter-like state to the same picker; whoever
  reviews the growth slice should re-check this interaction rather than letting the debt
  compound silently.
- **SHOULD-7 (`skipped` vs `skippedCount` naming, DB-failure visibility)** + nice items
  (Persian digits, template example rows, cp1256 hint, >50 confirm-disable, esc-into-
  textContent) — defer OK; portal-internal polish. Residual known limits, unchanged and
  accepted: leading-0 non-05 numbers (landlines) import as-is; a sheet with *no* phone column
  can still mis-map to whatever candidate matches (the detected-columns echo is the mitigation).

## Scope note (not scored here)

48bba0c bundles the reviewer musts with a **new growth slice** (agent `notifyLead` WhatsApp
alerts, quick-reply launch ladder, retargeting cohorts, vHome rebuild). That slice needs its
own review cycle; two things I noticed in passing for it: (a) the launch fallback ladder
(`catch { await gupshup.sendDocument(...) }`, `src/index.ts:166-185`) can double-send if the
rich call fails *after* Gupshup accepted it (ambiguous network failure) — worth a
dedupe/idempotency thought; (b) `notifyLead` sends WhatsApp autonomously — fine under §8 only
while NOTIFY_NUMBER is the PM's own opted-in number; the safety-gate should pin that
assumption explicitly.

## Verdict

**PASS — 8.5/10.** Both criticals are gone, verified by re-running the exact repros that found
them plus adversarial probes against the fix code (grid alignment, guard bypass attempts,
normalization chaining); two should-fixes landed as specified; the remainder is sanctioned,
ledgered debt. The audience slice hands to QA/CPO clean.

---

# Growth-slice review @987168e (48bba0c + 120058c + 51a78d7 + 987168e) — 2026-08-11

**Score: 8/10 — PASS (≥8) · DONE_WITH_CONCERNS. No blocking must-fix; one required
follow-up (one line) + two small should-fixes.**

Technical review: 9 issues (0 critical-blocking, 1 required follow-up, 2 should, 6 informational).
Method: read all four diffs + the support code the new paths lean on (`gupshup.ts postForm`,
`tracker.ts persist/hydrate/recordInbound`, `db.ts fire/loadAll/MIGRATION`); tsc exit 0 at HEAD;
served page JS (69,225 bytes) passes `node --check`; zero `${` in the template literal. Browser/
live behavior accepted from the delivery gate per orchestrator instruction — code judged here.

## Ruling the orchestrator asked for

**Stale-entFilters × cohort-lock: NO interaction — the caveat is discharged for this slice.**
While `retargetCohort` is set, step-2 renders ONLY the gold cohort card (`dashboard.ts:630` —
the chips/search/preview sit in the `else` branches), and `launchTargets()` (`:592`) returns
`retargetCohort.targets`, bypassing `entSel`/`entFilters` entirely. After «مسح والاختيار
يدويًا», manual mode returns with the same pre-existing trap — unchanged, not worsened; the
SHOULD-6 deferral stands on the ledger as-is.

**Double-send concern (my prior handoff note): 90% addressed — one structural residual.**
See follow-up F1 below. Credit where due: `postForm` also throws the marker on 200-with-
`status:"error"` (a true app-level rejection, `gupshup.ts:56-58`), `baseParams`'s
"outbound not ready" carries no marker so it correctly rethrows, fetch/transport errors carry
no marker, and `GUPSHUP_API_KEY missing` cannot false-match `includes("gupshup ")`. The
discriminator is right for every case except one:

## REQUIRED FOLLOW-UP (non-blocking, next commit)

- **F1 · `src/index.ts:172` + `src/gupshup.ts:57` — a Gupshup 5xx still triggers the fallback,
  and 5xx is not a shape rejection** (confidence 10/10 on mechanics, low expected frequency).
  `rejectedShape = (e) => String(e).includes("gupshup ")` matches `gupshup 500:`/`502:`/`504:`
  — server-side failures where the message MAY have been enqueued before the error — so the
  ladder can still double-deliver in exactly the ambiguous case the commit message claims is
  excluded ("Gupshup answered and rejected the shape" — a 5xx answer is neither). The code
  comment asserts a guarantee the code doesn't have. Fix is one line:
  `const rejectedShape = (e: unknown) => /gupshup 4\d\d:/.test(String(e));`
  (4xx = definitively rejected, not delivered; 5xx joins transport errors in the rethrow path,
  where the outer catch already records a transparent «فشل الإرسال».)

## SHOULD-FIX

- **S1 · `NOTIFY_NUMBER` format is load-bearing in two places with no normalization at the
  boundary.** The self-alert guard (`agent.ts:308` `contact.phone === cfg.notifyNumber`) and
  the PM auto-test-flag (`index.ts:307` `tracker.setTestNumbers([cfg.notifyNumber])`) both
  exact-match against tracker phones, which are always `\D`-stripped webhook digits
  (`gupshup.ts:184,234` — verified). A `+`/spaced/05-form secret silently disables BOTH
  behaviors (alerts about the PM's own chat; PM traffic pollutes real KPIs). Works today
  because the current secret happens to be digit-only. Fix: strip at config read
  (`(process.env.NOTIFY_NUMBER || "").replace(/\D/g, "")`) — one line hardens both.
- **S2 · `agent.ts:358` tag level is cast, not validated**: `(args.level ?? "warm") as
  "hot" | "warm" | "cold"`. An LLM emitting `"Hot"`/`"HOT"` stores a rogue level → the
  `tagLevel === "hot"` alert check misses (a genuinely hot lead sends no PM card) and chip
  styling falls back to warm. One `.toLowerCase()` + whitelist normalize.

## INFORMATIONAL (ledger)

- `dashboard.ts:503` — vHome hot-leads onclick interpolates **raw `c.phone`** where
  `contactRowsHtml` uses `esc(c.phone)` (`:313`). Not exploitable (webhook `from` is
  digit-stripped at both v2/v3 parse points — verified), but it breaks the every-sink-escaped
  convention that made the last audit cheap. Make it `esc()` for uniformity.
- Campaign-detail stats aren't test-aware: `campStats`/`funnelData`/`vKmonDetail` count test
  contacts inside mixed campaigns; R23's filtering covers Home KPIs, hot-leads, and the organic
  list, and all-test campaigns get the chip. Acceptable scope for R23 — note it so nobody
  mistakes detail-page numbers for real-only.
- `clearRetarget()` wipes `campName` unconditionally — including a name the user typed manually
  before locking a cohort. Cosmetic.
- Lead-alert throttle is in-memory: one possible duplicate alert after a restart — the code
  comment says so honestly (`agent.ts:305`). Fine at this stage.
- `tag_interest`/`request_human_handoff` fire `void notifyLead(...)` — audited the whole
  pre-`try` section for unhandled-rejection crash paths: transcript/tags are always initialized
  (`getContact`, `hydrate` — verified), `db.insertEvent` → `fire()` catches internally
  (`db.ts:117-121`). No crash path.
- Alert card embeds a 120-char slice of the customer's last message into the PM's WhatsApp —
  internal destination, fine; be aware it's untrusted text traveling to a human channel.

## Verified-pass evidence (adversarial checks that held)

- **R23 persistence chain end-to-end**: `ALTER TABLE contacts ADD COLUMN IF NOT EXISTS test`
  (migration) → `upsertContact` writes `Boolean(c.test)` ($10) → `persist(c)` passes the full
  contact → `loadAll` uses `SELECT * FROM contacts` → `hydrate` ORs with `testNumbers`
  (`tracker.ts:166`) → manual flags survive restart, PM flag survives even a false column.
  `setTestNumbers` runs before `hydrate` in boot order (`index.ts:307-309`). `convoSig`
  includes `test` (`dashboard.ts:349`); `/admin/contact/test` normalizes the phone.
- **Retarget correctness**: `lastDetailCohort` snapshots at render time = exactly the visible
  filtered rows; `startRetarget` guards empty cohorts; `openLaunch` gates on
  `launchTargets().length`; the >50 modal warning keys on the same count so it covers cohorts;
  `confirmLaunch` clears the cohort only on success; server-side re-normalization, opt-out
  skip, and the 50-cap all still apply to cohort posts (`index.ts:148,155,161`).
- **XSS on every NEW sink**: hub product names in wizard cards `esc(x.name)` — these are
  user-derived from uploaded decks, so this one matters — cohort card `esc(label)` +
  `esc(campaign)`, preview `esc(selAsset.filename)`, hot-leads `esc(waName)`/`esc(tg.product)`/
  `esc(last.text)`, notifyNumber footer `esc`'d, test chips static. Sole exception is the
  `:503` phone above.
- **Ladder bookkeeping**: each rung records its own accurate transcript marker (`مرفق`/`أزرار`
  only when that shape was the one sent); fallback failure rethrows to the outer catch →
  `recordSystem` + transparent failed result. `sendDocument` accepts the caption 4th arg
  (`gupshup.ts:121`) so the fallback keeps the opener text — no silent content loss.
- **notifyLead throttle discipline**: set-before-send, delete-on-failure; per-contact turns are
  serialized by the queue, so no release race. Map growth bounded by contact count.
- `wizProducts()` registry: `selProd` re-clamped (`if (selProd >= reg.length) selProd = 0`);
  registry ordering deterministic between render and click (fixed PRODUCTS + `ORDER BY
  product` hub extras).

## Verdict

**DONE_WITH_CONCERNS — 8/10, passes the gate.** The slice is coherent and defensively built:
the R23 separation is correct through every layer down to `SELECT *`, the retarget lock cleanly
sidesteps the picker's known filter debt, escaping discipline held on all new user-derived
sinks, and the double-send fix is genuinely most of the way there with honest bookkeeping
around it. The concerns are narrow and cheap: F1 is a one-line discriminator tightening whose
absence contradicts the fix's own comment (do it in the next commit — I will look for it),
S1/S2 are one-liners that harden config and LLM-output boundaries. Nothing here requires
re-opening the slice; hand to QA/CPO with F1 on the very next commit's manifest.

---

# Intel-slice review @ef6353a (9d99ea5 + 38e88df + ef6353a) — 2026-08-11

**Score: 7.5/10 — FAIL vs the ≥8 bar → BLOCKED. Two must-fixes, both small (~10 lines each).**

Technical review: 10 issues (2 critical-blocking, 1 should, 7 informational). Method: full read
of `src/insights.ts` + all three diffs + the support code the routes lean on (`tracker.snapshot`,
`db.loadAll` caps, `fire`); tsc exit 0 at HEAD; served page JS (84,804 bytes) passes
`node --check`; zero `${` in the template. Live proofs accepted per orchestrator — and the key
defect below is exactly the kind a live proof on a short transcript cannot show.
Loop-closure first: **16defb6 verified** — F1 (`/gupshup 4\d\d:/`), S1 (digit-strip at config),
S2 (level whitelist), esc-uniformity all landed exactly as specified.

## MUST-FIX (blockers)

### M1 · Insights cache permanently stale once a contact passes 30 transcript entries — CRITICAL (silent correctness), confidence 10/10
The customer route builds its contact from `tracker.snapshot()`, and snapshot caps transcripts:
- `src/tracker.ts` (snapshot): `transcript: c.transcript.slice(-30)`
- `src/index.ts` (/admin/customer/:phone): `const contact = (snap.contacts || []).find(...)`
- `src/insights.ts:74`: `const turns = (c.transcript || []).length;` → **plateaus at 30**
- `src/insights.ts:81`: `if (cached && cached.turns_at === turns) return cached.data`

Repro (no LLM needed): any contact with >30 transcript entries → open profile (computes, saves
`turns_at = 30`) → customer sends new messages → open profile again → `turns` is still 30 →
cached row returned. From that point «فهم المساعد», the home «أفضل الفرص» next-actions, and the
tracker-row next-actions show a frozen reading **forever** unless a human clicks تحديث ↻ — the
watermark design defeats itself precisely for the most active (most valuable) customers. The
live proof ("38-event" timeline) doesn't catch it because timeline events ≠ transcript entries;
the transcript was ≤30. Same root cause silently truncates the profile timeline (labeled «كل
نقاط التماس») to the last 30 messages and can flip contextScore part 8 (file-received marker
scrolls out of the window).

**Fix (small):** export a find-only accessor — e.g. `tracker.findContact(phone): Contact |
undefined` (no create) — and use the live contact in the route (keep the 404 semantics).
Watermark then grows monotonically between restarts; after a restart, hydrate's 50-per-phone cap
(`db.ts:183`) re-bases the length, `===` mismatches once, and one recompute self-heals — same
pattern as today, no staleness. (A `length + lastCustomerTs` key would be restart-proof; not
required.)

### M2 · LLM failure path: the profile 500s and the refresh button sticks — CRITICAL (availability of the new core screen), confidence 9/10
No try/catch around `client.chat.completions.create` (`src/insights.ts:87-95`) and none around
`insights.getInsights(...)` in the route (`src/index.ts`, customer handler) — an OpenAI error
turns the whole profile into a 500 even though identity, timeline, context score, and campaigns
are all local; no timeout is configured (SDK default is 600s, so a hung upstream holds the admin
GET for minutes). Client side, `refreshInsights` handles only network errors: on HTTP `!pr.ok`
(`if (pr.ok) {...}` with no else) the button stays «جارٍ القراءة…» with no feedback — and a 500
here is not hypothetical, it is exactly what M2's server half produces during any OpenAI hiccup.
**Fix (~8 lines):** wrap the completion in try/catch returning a degraded `Insights` («قراءة
المساعد غير متاحة مؤقتًا — السجل والسياق أدناه كاملان», intent "none", empty arrays, no cache
write); pass `timeout` (e.g. 20s) to the OpenAI client; add the else-branch reset + alertBar in
`refreshInsights`.

## SHOULD-FIX

- **S1 · Per-profile full scans where indexed queries exist** (`src/index.ts` customer handler):
  `(await db.listEntities()).find((e) => e.phone === phone)` loads **every entity** per click —
  this is the ledgered 400k client-fetch debt newly landing server-side — and
  `(await db.listCampaigns()).filter(...targets.some...)` scans all campaigns+targets.
  `entities.phone` is UNIQUE (index exists) → `SELECT ... WHERE phone = $1`; membership lives in
  `campaign_targets (campaign_id, phone) PRIMARY KEY` → one indexed join. Both one-liners in db.ts.

## INFORMATIONAL (ledger)

- Watermark race (orchestrator's question): two concurrent misses both compute and both upsert —
  last write wins, identical-ish data, cost = one duplicate LLM call on an admin-only route.
  **Acceptable; no fix needed.** Same for unthrottled `?refresh=1` (admin-gated).
- `refresh()` on every `#customer` hashchange refetches entities/kb/campaigns/insights wholesale —
  the existing fetch-all debt amplified by navigation frequency; fold into the pagination epic.
- `contextScore` part 5 label «ردّ على حملة» is true for ANY inbound (`replied || inbound >= 1`)
  — label promises more than the logic checks; cosmetic honesty nit.
- The city chart keys on the literal header «المدينة» only; other spellings feed nothing — the
  empty state says so honestly. Fine for now.
- Profile fetch interpolates the hash segment into the URL un-encoded (`/admin/customer/" + ph`);
  digits in practice, server `\D`-strips — cosmetic.
- Learning-state contacts (<2 inbound) are never cached, so list rows correctly fall back to
  last-message — verified intentional and correct.
- Leftover ⭐ is inside the cohort-label sanitizer regex (`dashboard.ts:464`) — legacy stripping,
  harmless; the emoji-chip sweep itself is complete (remaining glyphs are functional: 📎⬆🔔↻⁂⟲).

## Verdict on the LLM-text-into-HTML sink discipline (asked explicitly)

**Clean — two independent layers, verified end to end.**
*Server coercion (`insights.ts:96-109`):* every field is hard-coerced — `String()` + slice caps
(200/120/160/200/100), `intent` via array whitelist, product levels via `lvl()` lookup (never
passthrough), arrays capped at 5/5/4, non-strings collapse to harmless `"[object Object]"`.
*Client escaping:* all nine LLM-derived render paths go through `esc()` — summary (both
branches), each signal, each objection, next_action (profile card + tracker rows + home rows),
why, best_time, product names via `toneBadge` (esc inside), intent via static `INTENT_META`
lookup, timeline `title`/`meta`. Chart labels esc'd including file-derived city names; SVG
`<text>` content is locale-generated digits only. **No unescaped sink found.**
*Blast-radius:* `insights.ts` imports OpenAI/config/db/types only — **no gupshup import, zero
outbound capability**; the completion carries **no tools**; the output is consumed by rendering
only (nothing machine-actionable reads it). Prompt-injection residual = misleading Arabic text
shown to a human inside a card labeled as the assistant's reading — inherent to the feature and
acceptable; a one-line system instruction to ignore in-transcript directives would shave it
further (nice-to-have).

## Verdict

**BLOCKED — 7.5/10.** This is a well-built slice: the sink discipline is the cleanest yet, the
learning gate is honest, coercion is a real whitelist, the charts guard their math and escape
their labels, and R28 respects the test toggle throughout. But the slice's own core mechanism —
the transcript watermark — silently self-destructs at 31 messages because the route reads
snapshot-capped contacts (M1), and the new screen's availability hangs on OpenAI with no
degradation or timeout (M2). Both fixes are surgical; with them landed and one >30-message
spot-check (compute → new inbound → profile shows fresh reading), this re-scores ≥8.5. S1 should
ride the same commit if convenient.

---

# Re-review @4a40ab9 (c27a3a7 musts + a3617ab R29 + 4a40ab9 R30) — 2026-08-11

**Score: 8.5/10 — PASS (≥8). No remaining blockers.**

Method: full diffs of all three commits read; fix mechanics verified against the support code;
tsc exit 0 at HEAD; served page JS (92,655 bytes) passes `node --check`; zero `${` in the
template. The builder's live spot-check matches the one I prescribed; the code chain is verified
independently below.

## Must-fix verification

- **M1 FIXED (verified).** `tracker.findContact` is a true read-only lookup
  (`contacts.get(phone)` — no create, no touch); the customer route now builds from the LIVE
  contact with the 404 semantics intact, and the in-code comment records the why. Watermark now
  tracks the full transcript (grows monotonically between restarts; hydrate's 50-cap re-base
  causes exactly one self-healing recompute — as designed). Timeline and contextScore part 8 are
  no longer snapshot-capped. The live proof (5→6 turns → fresh compute `{"turns":6}` reading the
  new message; PM recompute once at live length 29) is exactly the prescribed spot-check.
- **M2 FIXED (verified).** OpenAI client now `timeout: 20_000, maxRetries: 1`; the completion is
  wrapped in try/catch returning an honest degraded `Insights` («قراءة المساعد غير متاحة
  مؤقتًا…», tags-derived product_interest kept) that renders through the existing esc'd sinks;
  **provably uncached** — the single `db.saveInsights` call site (`insights.ts:122`) sits after
  the catch's return. `refreshInsights` resets the button in BOTH the `else` (with HTTP status
  in the alert) and the `catch`.

## S1 deferral ruling — CONFIRMED

Per-profile full scans (`listEntities().find` + `listCampaigns().filter`) ride the ledger with
the batch-upserts/pagination epic. Bounded by current dataset size on a human-paced admin route;
the indexed one-liners are specified in the intel review when that epic opens.

## New work scored in (R29 + R30)

**SHOULD-FIX (next commit, one-liner):**
- **`src/dashboard.ts:980` — stray `</svg-fix>` inside `funnelSvg`'s markup string**, directly
  after the `<svg …aria-label="قمع الحملات">` opening tag. It renders correctly today only by
  HTML-parser error recovery: an unmatched foreign-content end tag falls through to the in-body
  "any other end tag" rule and is **ignored** (svg stays open, the polygons/text land inside it,
  `</svg>` closes it) — deterministic per spec and consistent with the passing gate, but it is
  invalid markup left in the string and a trap for the next edit. Delete the token.

**INFORMATIONAL:**
- Campaigns list filtered to zero (tab/search) renders the header row with no «لا نتائج» line —
  small UX gap, the customers/picker lists both have one.
- Funnel side-labels column approximates row alignment (fixed 40px vs `segH+gap` with
  `space-between`) — cosmetic, verified live.
- Distribution charts key on literal headers «الحجم»/«القطاع» like the city chart — same known
  family, honest empty states.

**Verified-pass evidence (new sinks and math):**
- `pct` guards division at both definition sites (`:425`, `:955` — `b ? … : 0`); ratesStrip's
  fallback denominator (`agg.sent || agg.targeted`) is sensible; funnel min-width floor
  `Math.max(0.16, …)` + `Math.max(1, …)` maxima; colChart height floor; treemap total floor and
  flex-ratio floor. No NaN/zero path found.
- **File-derived strings esc'd at every new sink**: colChart size/sector values
  (`esc(String(r[0]))`), treemap city names, funnel side labels, campaigns search input value,
  campaign name/product in the reworked rows. SVG `<text>` contents are locale digits only.
- R30 mechanics: the tab filter boolean (`(campTab === "test") === campIsTest(c)`) is correct
  for all three tabs; sort keys whitelisted by comparison with a safe default; distinct debounce
  timer (`__cq2`) — no collision with the customers search; row onclick uses numeric `c.id`.
- Emoji/glyph state unchanged from the sweep; no new `${`/backtick hazards.

## Verdict

**PASS — 8.5/10.** Both blockers are verifiably gone — the watermark now reads the live ledger
and the intelligence layer degrades instead of failing — and the two visual slices are built
with the same guard-and-escape discipline the codebase has now made habitual. What remains is
one mechanical markup wart (`</svg-fix>`, works only by parser forgiveness — remove it next
commit) and two cosmetic nits, none gating. The customer-intelligence pivot is clean to hand to
QA/CPO.

---

# Overnight-mission review @43a5015 (4a40ab9 → 43a5015, 15 commits) — 2026-08-11

**Score: 6.5/10 — FAIL vs the ≥8 bar → BLOCKED. Three must-fixes (each ≤ ~10 lines) — two are
§8/dead-air class, one is demo-visible. All fixable well inside the 5-hour demo window.**

Technical review: 12 issues (3 critical, 6 should, 3 informational). Method: full cumulative
diff read (587 insertions across agent/insights/index/dashboard), opt-out matcher probed with
the real regexes (13-case matrix), tsc exit 0 at HEAD, served page JS (109,509 bytes) passes
`node --check`, zero `${`, BOM emission verified correct. Live captures accepted — note that
two of the three criticals are invisible in static captures by nature.

## MUST-FIX (blockers — and demo-risky)

### M1 · Opt-out matcher now MISSES natural Arabic opt-outs — §8 sacred, confidence 10/10 (probed)
The re-anchor (84ac266) correctly kills the «كيف أوقف التزوير؟» false positive — but the new
two-tier matcher (`agent.ts:392-401`: bare-command `^…$` + explicit-request list) has no tier
for **command + messaging-object**, the most natural phrasing. Probe results against the real
regexes — all of these KEEP MESSAGING a customer who asked to stop:
`«أوقف الرسائل» MISS · «أوقفوا الرسائل» MISS · «وقفوا الرسائل عني» MISS · «توقفوا عن مراسلتي»
MISS · «لا أريد رسائلكم» MISS · «كفى رسائل» MISS · «stop all messages» MISS` (false positive
stays fixed ✓). The matcher is the ONLY opt-out line of defense (no LLM fallback path sets
opted_out). **Fix: add a proximity tier** — opt-out verb stem within ~15 chars of a messaging
noun + a want-negation form, e.g.:
`/(إيقاف|ايقاف|أوقف|اوقف|وقف|توقف|كفى|بلا)[^\n]{0,15}(رسائل|الرسائل|مراسل|المراسل)/` and
`/(لا|ما)\s*(أريد|اريد|أبي|ابي|أبغى|ابغى)[^\n]{0,12}رسائل/` and `/\bstop\b[^\n]{0,12}messag/i`.
None of these can re-trigger on «أوقف التزوير» (no messaging noun). Re-run the 13-case matrix
after — it should be 13/13.

### M2 · Single-bubble suppression can silence a live lead entirely — confidence 9/10
`agent.ts:466` sets `sentOwnBubble = true` for `send_asset`/`send_buttons` **before**
`execTool` runs — but `send_asset` has two no-send paths that RETURN WITHOUT SENDING
(`"لا يوجد ملف لهذا المنتج — تابع بدون ملف."`). Repro: customer asks for the file of a product
with no uploaded asset → model calls `send_asset` → not found, nothing sent → model writes the
text fallback the tool result told it to write → `agent.ts:477` suppresses it → **the customer
gets nothing at all for that turn** (logged, invisible to them). Directly demo-risky: a file
request for any product without an intro PDF produces dead air on stage. **Fix:** derive the
flag from the outcome, not the intent — set `sentOwnBubble` only when the tool actually sent
(e.g. `execTool` result starts with `"أُرسل"`, or return a `{sent}` signal); keep it
unconditional for `send_buttons` if that path always sends.

### M3 · Home/kmon KPI numbers re-animate from 0 every 5 seconds — demo-embarrassing, confidence 9/10
`countUp()` (`dashboard.ts:1402-1424`) keys "already animated" on a `WeakSet` of DOM nodes —
but the 5s poll (`setInterval` → `refresh()` → `render(true)` → `b.innerHTML = …`) rebuilds the
view, so every tick creates FRESH nodes the WeakSet has never seen → every `.kpi .v`/`.statc
.v` with ASCII digits re-runs the 0→N ease **every 5 seconds** on exactly the screens the
founder will project (home, campaign detail). Static captures cannot show this; 0 console
errors says nothing about it. **Fix (3 lines):** stamp the element instead —
`if (el.dataset.counted === raw) return; el.dataset.counted = raw;` — animates on first paint
and again only when the VALUE changes (which is the nice case).

## SHOULD-FIX (post-demo acceptable, cheap)

- **S1 · Attachment-marker drift breaks file detection everywhere downstream.** Producers now
  write `[مرفق في نفس الرسالة:` (`agent.ts:350`, `index.ts:178`) while both consumers match
  `[مرفق:` (`insights.ts:60` contextScore part 8, `:71` timeline file-kind). Every new file
  send is invisible to the context score and typed as plain text in the timeline. One-line fix:
  match `"[مرفق"` (drop the colon) in both consumers.
- **S2 · winLossBoard aggregates TEST contacts' verdicts** (`insights.ts` winLossBoard reads
  `db.listInsights()` with no test filter): the PM's own demo conversations become «لماذا
  نخسر» rows on the real board — undercuts R23's separation promise the moment real traffic
  exists. Filter phones whose tracker contact is `test` (or pass a test-set from the route).
- **S3 · Time-decayed deal_state can never materialize from cache**: "stalled" is defined by
  silence (>2 days) but the cache invalidates only on transcript growth — silence produces no
  recompute, so `active` rows rot as active forever (board undercounts stalled; the «صفقة
  متجمّدة» action items only ever see manually-refreshed profiles). Cheap: in `getInsights`,
  also recompute when cached `deal_state === "active"` and `computed_at` is older than ~48h
  with no newer activity (`getInsightsRow` already returns `computed_at`).
- **S4 · CSV formula injection** (`dashboard.ts:529-537`): quoting/BOM are correct (verified,
  including the `\\ufeff`→`﻿` template emission), but fields starting `=`/`+`/`-`/`@`
  (campaign or deck-derived product names) execute as formulas in Excel. Standard guard: prefix
  `'` (or a tab) when the first char is one of those.
- **S5 · First free-text string in the onclick-JS-string context** (`dashboard.ts:960`):
  `onclick="launchWithProduct(\'' + esc(name) + '\')"` — `esc()` emits `&#39;`, the attribute
  parser decodes it back to `'` inside the JS source, so a hub product name containing an
  apostrophe breaks out of the JS string (button dead; theoretical self-XSS on the admin's own
  portal). Every prior onclick site passed digits or static keys — this is the first free-text
  one. Use the data-attribute pattern: `data-p="' + esc(name) + '" onclick="launchWithProduct(this.dataset.p)"`.
- **S6 · Turn-cap handoff promises a human but alerts no one** (`agent.ts:422-429`): the
  announce-once fix is right, but this path sets `handoff` via `tracker.setOutcome` directly —
  `notifyLead` never fires (it only fires from the `request_human_handoff` tool), so the
  customer is told «سيتولى أحد مختصينا…» and then nobody is notified while the agent goes
  permanently silent. Add `void notifyLead(contact, "handoff", …, "turn cap")` in the branch.

## INFORMATIONAL

- Arabic-Indic-digit KPIs (`toLocaleString("ar-SA")`) never animate — countUp's
  `[^\d]` strip makes them NaN → silent no-op (harmless, cosmetically inconsistent with the
  ASCII ones; moot once M3 stamps by value).
- `winLossBoard` `totals.learning` is structurally ~0 (learning reads are never cached, so
  `listInsights` cannot contain them) — dead code, and correctly NOT displayed by the card.
- Win-driver strings aggregate as free-text Map keys — near-duplicates fragment counts
  (inherent LLM-aggregation noise; the prompt's anchored examples mitigate).

## Verified-pass evidence

- **Win/loss coercion complete** (`insights.ts:164-179`): `deal_state` 4-value whitelist with
  "active" default (old cached rows without the field degrade correctly), `loss_cause` strict
  LOSS_TAXONOMY membership AND zeroed unless lost/stalled, drivers/evidence/fix capped and
  `String()`d. Aggregate counts each contact once (no double-count); per-product fan-out is
  deliberate and never presented as a total; `/admin/intel/winloss` is admin-gated and LLM-free.
- **XSS discipline on all new sinks held** — board driver/cause/example/product chips, profile
  verdict `evidence`/`fix_suggestion`, action-items card (waName/loss_cause/next_action/fix),
  hub verdict block, campaign-detail verdict strip, CSV (quoted+BOM), count-up writes via
  `textContent`. Sole exception is the S5 attribute-context subtlety.
- **Auto-reveal is correct** (orchestrator question): decides once per page load after the
  first state fetch, `toggleShowTest` sets `showTestDecided = true` so the manual toggle always
  wins; zero-contact case leaves defaults. No fight.
- **Launch single-bubble** (7db6509): document+caption is now the primary shape (native single
  bubble; matches the device reality that quick_reply+document rendered as two), ladder retained
  only for the no-asset path with the 4xx discriminator intact.
- Turn cap now counts customer turns and announces once (`outcome !== "handoff"` guard) —
  correct mechanics, see S6 for the missing alert.
- `launchWithProduct` resolves the wizard index by name at click time with a graceful miss;
  template-literal escaping in the big rewritten blocks is right (`\\ufeff`, `\\n` emit
  correctly; page JS parses).

## Verdict

**BLOCKED — 6.5/10, with all three blockers fixable in well under an hour.** The overnight
volume is genuinely impressive and most of it is disciplined: the win/loss layer is properly
coerced and cheaply aggregated, the design overhaul kept the escape-everything habit, the
single-bubble reality fix matches the device truth, and auto-reveal is exactly right. But the
two agent "hard-rule" commits each carry a sharp edge — the re-anchored opt-out matcher now
misses the most natural Arabic opt-out phrasings (probed: 7 misses — §8 calls this path sacred,
and an on-stage «أوقف الرسائل» that keeps selling is both embarrassing and a compliance
failure), and the suppression flag fires on intent rather than outcome, so a missing intro PDF
turns into dead air mid-conversation. The third blocker is pure stagecraft: the KPI band
re-counts from zero every 5 seconds on the projector. Fix M1–M3 (and ideally S1) before the
demo; S2–S6 can ride the next cycle. Re-run the 13-case opt-out matrix and one no-asset file
request as the re-review evidence.
