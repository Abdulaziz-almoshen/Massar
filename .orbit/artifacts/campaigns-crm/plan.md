# Plan — campaigns-crm

Cycle `campaigns-crm` · `[planner]` · baseline `massar-engine@35a9e07` · rulings R1–R4 taken as settled.

## The seam (read before any slice)

New file **`massar-engine/src/campaigns-crm.ts`** exports `CAMPAIGNS_CRM_JS: string`, injected by **one**
anchored `${CAMPAIGNS_CRM_JS}` immediately before `</script>` (dashboard.ts:2327) — the file's first and
only interpolation. Because `<script>` (259) → `</script>` (2327) is **one scope**, the module calls
`campStats` / `campWin` / `atOrAfter` / `seenOf` / `repliedIn` / `interestedOf` / `fmtN` / `esc` **directly
as the existing declarations** — no import, no copy, single source. That is the whole mechanism.
Module rules: no backtick, no `${`, `\\'` escaping identical to dashboard.ts (ADR-0001 §4).
**Runtime assertion** (ADR-0001's blind spot): the module ends with `crmBoot()`, which throws when any of
the six is not a function → `pageerror` → `smoke.py` FAILs. Every slice also records the ADR-0001
definition-count delta.

## Slices

**S1 · Truth defects + one status function** (R3, BR-2, BR-4). `dashboard.ts` only.
Anchors: (a) after `function campIsTest(cp) { return cp.test === true; }` → add `campReplyState(cp, st)`
returning `{key,label,tone}` over the three BR-2 predicates; (b) replace the exact two-line chip ternary at
**619** (`st.replied ? …مكتملة…` + the `جارية` line) — that anchor string does **not** occur at 1472, so the
readiness card is untouched; (c) replace `const base = Math.max(1, st.targeted);` + `const pct =` with
`pctTxt(v)` → `«—»` when `targeted===0`, then its 2 stat-grid call sites and the verdict-card rate triple.
Proof: **AC-3** (`check-crm.mjs`: zero chip-form «مكتملة», exactly one occurrence in the file, `campReplyState`
defined once with ≥2 call sites), **AC-7** (zero-target fixture screenshot), **AC-11**.
Rollback: revert 6 anchored strings.

**S2 · The seam, empty.** New `campaigns-crm.ts` (state + `crmBoot` + stubs returning `""`), the one
insertion. Ships behaviour-neutral so the seam is proven alone. Proof: **AC-13**, smoke 7/7, definition
count unchanged.  Rollback: delete the `${…}` line.

**S3 · ViewControls + filter/sort/columns** (FR-1/2/3/5). Anchors in `vKmon`: after the tabs `.join("") +
"</div>";` → `h += crmBar();`; replace the `let list = campaigns.filter(…)` expression → `crmFilter(...)`;
replace the 3-branch sort → `crmSort(withStAll)`; **wrap** (two insertions, not a range) the `withSt.forEach`
block in `if (typeof crmRowsHtml === "function") { h += crmRowsHtml(withSt); } else { …existing loop… }`.
The old loop stays live as the blank-page fallback — stated debt, deleted next cycle.
Proof: **AC-1** (screenshot + node assertion over `/admin/campaigns`), **AC-2** (`check-crm.mjs` enumerates
column keys against FR-5's closed set).  Rollback: the `else` branch already is the rollback.

**S4 · Selection + bulk** (FR-6/7, BR-5). Module-only + the S3 row renderer. Three actions, no send path.
Proof: **AC-5** (400-campaign fixture, filter matching 137 → «تحديد المطابقين» reads ١٣٧ while ٦٠ render),
**AC-6** (`window.fetch` spy: exactly 5 `POST /admin/campaign/test`, zero other requests, one forced 500 →
failed-count line). Spy-stubbed, so **zero production writes**.  Rollback: `crmBulk=false`.

**S5 · Group / kanban** (FR-4, BR-2/3) — **riskiest, see below**. One anchor: before
`h += '<div class="tblwrap rise">';` → `if (crmMode() !== "list" && typeof crmBoardHtml === "function") { try { return h + crmBoardHtml(withStAll); } catch (e) { alertBar(…) } }`.
Columns come from `campReplyState` (same function as the chip). DnD only on التصنيف.
Proof: **AC-3** (browser harness compares each row's `data-state` to its board column over 50 fixtures),
**AC-4** (fetch spy: product board drag = 0 requests; التصنيف drag = exactly 1 POST), **AC-12** (`scrollWidth
<= clientWidth` at 375/768/1440 × list/group/board), **AC-14**.  Rollback: `crmMode()` pinned to `"list"`.

**S6 · Detail spec strip** (R2; FR-9 collapsed, FR-8 partial). One insertion after the ptitle block in
`vKmonDetail` → `crmSpecStrip(camp, st)`: معرّف · التصنيف · تاريخ الإطلاق · عدد الجهات · **`camp.message`**
(escaped, `pre-wrap`, labelled «نص مُرسَل — غير قابل للتعديل»), zero inputs, zero save affordance.
`message` is already on the client (`db.listCampaigns` → `/admin/campaigns`) — no API change.
Proof: **AC-8** (screenshot vs the `/admin/campaigns` row), **AC-9** (smoke DOM assertion: no
`input`/`textarea`/save control in the strip; التصنيف toggle is detail's only mutation control).
Tabs (`نظرة عامة | نص الرسالة | جهات الاستهداف`) are optional in this slice; the strip is required.

**S7 · Gates + evidence.** `scripts/check-crm.mjs` wired into `npm run check` (→ 14 checks) and
`scripts/qa-crm.py` (fixture injection `campaigns = FIXTURE; render(false)`, spies, 3-viewport captures).
Then `npm run deploy` → smoke 7/7 → `/health` `ok:true`.  Proof: **AC-13**, §3 completeness.

## Riskiest slice — S5

It is the only slice that **early-returns from `vKmon`**: a fault there blanks the campaigns list — precisely
ADR-0001's production failure, on the screen the founder demos. It also carries the cycle's only mutating
gesture (drag → real POST) and the only horizontal scroller. Hence: build it **last**, behind a
`typeof` guard, inside `try/catch` that degrades to the list, with the mode pinned by a one-line rollback.

## Flagged ACs

- **AC-6** «zero Gupshup calls» is provable only as *zero client requests other than `/admin/campaign/test`*.
  A server-side send-spy would require a send — forbidden (§8, NO-SEND). Stated as a scope limit, not a pass.
- **AC-5 / AC-7 / AC-14** need 400-campaign, zero-target and empty states that production lacks. Proven by
  **client-side fixture injection**, honest evidence for client-only state (BR-6); seeding them server-side
  would be a write we are not taking.
- **AC-10** — N/A this cycle (D-2 out).
- FR-8's «الأحداث» tab — deferred: it re-derives `statusTimes` already rendered in the targets table.

## D-3 (decision, recommend as written)

View mode persists in **`localStorage`**, not the route. Market §2's "route is the state" is the better
contract, but `#kmon/<id>` is already the detail route and a second path segment risks colliding with it.
Net: cheaper, reversible, costs deep-linkability of a board. Revisit when the router is rewritten.

**Acceptance manifest:** `.orbit/review-requests/campaigns-crm.json`, unarmed. If `crm-record-props` lands
first, re-stamp `baseline_commit` **before** arming.
