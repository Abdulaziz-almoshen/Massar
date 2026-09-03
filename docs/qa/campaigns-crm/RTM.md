# Requirements Traceability Matrix — `campaigns-crm`

`[qa-engineer]` · target commit **`645c5d8`** · run 2026-08-17 · **report only, nothing fixed**

Oracle: `docs/artifacts/campaigns-crm/requirements.md` (AC-1..AC-14) + `plan.md`.
Evidence root: `docs/qa/campaigns-crm/rtm-evidence/` · raw assertions `rtm-evidence/probe-results.json`.

---

## 0. Evidence binding — read this first

**The pre-existing evidence was not bound to `645c5d8`.** The nested repo's working tree is dirty
against the target commit:

```
$ git -C massar-engine diff --stat HEAD
 package.json | 5 +-   src/agent.ts | 61 ++   src/campaigns-crm.ts | 1 -
 src/db.ts | 59 ++     src/index.ts | 113 ++  src/tracker.ts | 275 ++
 6 files changed, 486 insertions(+), 28 deletions(-)
```

`dist/` (built 15:45, same minute as the existing captures) contains `decideProp`,
`formatInterest`, `humanFactsBlock` — symbols that exist **only in the uncommitted diff**. So
`scripts/qa-crm.py`'s "36 assertions, 0 failures" and every capture in this directory describe the
dirty tree, not `645c5d8`.

**Correction applied.** All verdicts below were re-derived from a clean detached worktree:

```
$ git worktree add --detach <scratch>/wt645 645c5d8    # git status --porcelain: clean
$ npm run build                                        # exit 0
$ PORT=8098 node dist/index.js                         # memory-only, DATABASE_URL unset
```

Every runtime verdict below came from that engine on `:8098`. The pre-existing `:8099` engine was
not used. No fetch in this run reached a real backend: the in-page spy stubs every response, and the
probe engine has no database attached — **zero writes, zero outbound, and no WhatsApp send of any
kind occurred** (§8 / NO-SEND respected).

---

## 1. Coverage of the pre-existing gates (verified, not trusted)

| gate | claim | independently re-run @645c5d8 | verdict |
|---|---|---|---|
| `scripts/check-crm.mjs` | 18/18 | `npm run check:crm` → **exit 0**, `[check:crm] 18 passed, 0 failed` | claim holds |
| `npm run check` (14 checks) | green | **exit 0** | holds |
| `npm run build` | strict-clean | **exit 0** | holds |
| `scripts/qa-crm.py` | "36 case×viewport assertions" | true count, but each case asserts only 4 generic properties: `render_ok`, `landmark_ok`, `console_ok`, `overflow_ok` | **coverage overstated — see below** |

`qa-crm.py` is a blank-page/console/overflow gate. It contains **no fetch spy, no drag simulation,
no select-all assertion, no `٠٪` absence check, no column enumeration, no escaping check**. It
therefore contributes evidence to AC-12 and AC-14 only. Its `detail-zero` case asserts the landmark
`"—"` — an em-dash that occurs in unrelated chrome — and never asserts the **absence** of `٠٪`,
which is the actual AC-7 requirement. That assertion is close to vacuous. I replaced it with a
counting assertion (`body.count("٠٪") == 0`).

To close the gap I wrote an independent probe (`rtm-evidence/rtm-probe.py`, 59 assertions).
**Every assertion reports the node count it inspected**, so a selector matching nothing cannot be
reported as a pass — the recorded incident class this project asked to be guarded against.

---

## 2. Traceability matrix

| AC | Requirement | Verdict | Evidence (command / capture) |
|---|---|---|---|
| **AC-1** | FR-1..3 filter `الخدمة=X` + sort `الأكثر ردودًا` | **CONCERNS** | 400-campaign fixture, `campQ='التطعيمات'` + `setCampSort('replies')`: 60 rows render, **0 off-product rows**, `crmFiltered()` n=137 non-increasing in `replied`. Capture `ac1-filter-sort.png`. **But** the FR-1 bar ships `بحث · قائمة/تجميع/كانبان · الكل/فعلية/تجريبية · sort/group select` — there is **no `فلترة` condition builder and no `الأعمدة` picker**. FR-2's AND-ed removable conditions and FR-5's column chooser are unimplemented; filtering is free-text over name+product plus the class tab. The AC's literal test passes; the FR behind it is partial. |
| **AC-2** | BR-1 every column ∈ FR-5 closed set | **PASS** | Header harvested = 9 cells: `["","الحملة","الخدمة","الحالة","الجمهور","مشاهدة","ردود","التقدّم",""]`. Unexpected keys: **0**. Non-vacuity: 9 nodes inspected. |
| **AC-3** | BR-2 one function emits chip **and** column; «مكتملة» retired | **PASS** | (a) Emitted client JS contains **exactly 1** `مكتملة`, context = `'<div class="card"><h3>جاهزية الخدمة <span class="meta">' + fmtN(done) + " من " + fmtN(rows.length) + " مكتملة"` — the **service-readiness KB card** (`dashboard.ts:1486`), **not a campaign surface**. Confirmed by direct context grep, not by trusting the gate. The only other repo hit is `insights.ts:375` (server-side scoring label). At runtime, `مكتملة` occurs **0 times** on `#kmon` in any view. (b) 50-campaign fixture, chip label vs kanban column: **50 shared, 0 mismatches**; per-column cards `{بلا ردود بعد:34, تجريبية:16, فيها ردود:0}`; labels ⊆ the BR-2 three. Both surfaces read `campPerfState` (`campaigns-crm.ts:111`). Capture `ac3-board-50-all.png`. |
| **AC-4** | BR-3 drag refused on read-only boards; exactly one POST on التصنيف | **PASS** | **Fetch spy, not code reading.** التصنيف board: `.kcol=2`, `.kcard[draggable=true]=5`, `.kcol[ondrop]=2`; drag campaign 1 → **exactly 1** call: `POST /admin/campaign/test {"id":1,"test":true}`. Product board: `draggable=0`, `[ondrop]=0` over 4 rendered cards, and a **real dispatched `dragstart`/`dragover`/`drop`** gesture → **0 requests**. حالة الأداء board (columns `["بلا ردود بعد","تجريبية","فيها ردود"]`, i.e. one literally named «تجريبية»): `draggable=0`, `ondrop=0`. Captures `ac4-board-class.png`, `ac4-board-product.png`, `ac4-board-perf.png`. **Depth note (not a failure):** `crmDrop` (line 638) is not internally board-guarded — it derives `want = col === "تجريبية"` and would write if ever wired to another board. Refusal today rests solely on the `canDrag` attribute guard (line 287). Defence-in-depth gap. |
| **AC-5** | FR-6 / edge 400+: «تحديد المطابقين» reports the true match count while `LIST_CAP` renders | **FAIL** | 400-campaign fixture, filter matching exactly 137. Rendering side is correct: `crmFiltered()=137`, **`.krow`=60**, count pill reads **١٣٧ حملة**, footer declares ٤٠٠. But **«تحديد المطابقين» does not exist** — no `crmSelectAllMatching` function, no such string in the DOM. The only bulk selector is `crmTogglePage()`, which selects **60** and alerts «حُدِّدت ٦٠ المعروضة فقط — من ١٣٧، والباقي غير مشمول». So the *reporting* half of the AC is met and is honest; the *selection* control mandated by FR-6 (mirror of `entAllMatching`) is **unimplemented**. Captures `ac5-filter-137.png`, `ac5-selectpage-alert.png`. |
| **AC-6** | FR-7 / BR-5: bulk reclassify of 5 = 5 calls, **zero outbound**; partial failure reported | **PASS** | Spy over `fetch` + `XMLHttpRequest` + `sendBeacon`. 5 selected → **exactly 5 calls**, all `POST /admin/campaign/test`, ids 1/3/4/5/6; **other fetch = [], xhr = [], beacon = []**; zero gupshup/send-shaped paths. Forced-500 run: still **exactly 5** calls (no retry storm) and the UI shows «تعذّر» with the count. Captures `ac6-bulk-ok.png`, `ac6-bulk-500.png`. **The plan flagged "zero Gupshup calls" as unprovable without a send — it is provable, and I closed it structurally instead:** `index.ts POST /admin/campaign/test` → `db.setCampaignTest` → `UPDATE campaigns SET test=$2 WHERE id=$1` and **nothing else**; `db.ts` contains **zero** references to `gupshup`. Client spy + single-endpoint + update-only handler ⇒ no outbound path exists. No send was performed. |
| **AC-7** | BR-4 zero-target renders «—», never ٠٪ | **PASS** | Zero-target fixture, detail `#kmon/1`: **`٠٪` count = 0**, «—» count = 4. List row: **`٠٪` count = 0**, «لا جهات استهداف» present, `.krow`=1 (non-vacuity: a rate cell existed to be wrong). **Confirmed against the image** `ac7-detail-zero.png`: the three verdict rates (نسبة المشاهدة · نسبة الردود · جهات مهتمة لكل ١٠٠) render as long dashes; حجم الجمهور correctly shows the count ٠. `crmRate` returns `null` on a zero denominator (line 118); `Math.max(1, st.targeted)` is gone. **See Finding F2** — a truth defect on this same screen that the AC does not cover. |
| **AC-8** | FR-8 four tabs; `نص الرسالة` verbatim + escaped | **CONCERNS** | Message half **passes and was attacked**: fixture message `<img src=x onerror="window.__pwned=1"> & <b>عريض</b> مرحبًا` renders **verbatim as text**, `window.__pwned === false`, injected `img` nodes = **0**. Capture `ac8-message-escaped.png`. Tabs half **not met**: detail exposes **3** tabs `["جهات الاستهداف (٦)","الأداء","الخطوة التالية"]`, not four; `نص الرسالة` is not a tab but the always-visible spec strip. `الأحداث` was explicitly deferred in `plan.md` S6/Flagged-ACs, so this is planned descope, not drift — but AC-8 as written is unmet. |
| **AC-9** | FR-9 only التصنيف editable; no other save control | **PASS (with an FR-9 gap)** | Detail DOM: `textareas=0`, `selects=0`, save-shaped buttons (`حفظ\|تعديل\|احفظ`) = **0**, over 22 buttons inspected (non-vacuous). The single `input` is `#rq` `placeholder="بحث…" oninput="rSearch(this)"` — the **contacts search filter**, not a campaign field, and it has no save path. Spec strip carries «هذا نصّ ما أُرسل فعليًا. لا يقبل التعديل بعد الإطلاق.» The AC's risk direction — *no unbacked save affordance shipped* — is satisfied. **FR-9 gap (Finding F3):** the positive half is unmet — `setCampClass` has **0** call sites on detail, so التصنيف is **read-only there**; and `تاريخ الإطلاق` / `معرّف الحملة` are not rendered as fields. Strip shows الخدمة · حجم الجمهور · التصنيف only. |
| **AC-10** | FR-10 contact-stage kanban | **WAIVED** | D-2 decided out this cycle (`plan.md` Flagged-ACs: "N/A this cycle"). Not built, correctly not stubbed. Confirmed absent. |
| **AC-11** | NFR-1 `check:numerals` exits 0 | **PASS** | `npm run check:numerals` → **exit 0** at the clean worktree. Arabic-Indic numerals confirmed visually in every capture (٤٠٠، ١٣٧، ٦٠، ٠٪). |
| **AC-12** | NFR-2 no horizontal page overflow, 3 viewports × list/group/kanban | **PASS (with an NFR-2 gap)** | 9/9 combinations, 400-campaign fixture: `scrollingElement.scrollWidth - clientWidth = **0px**` and `body` overflow `0px` at 375/768/1440 in list, group and kanban. Added a non-vacuity guard the original harness lacked: count of **non-fixed elements whose `getBoundingClientRect().right` exceeds `clientWidth`** = **0** in all 9. Captures `ac12-{list,group,kanban}@{375x812,768x1024,1440x900}.png`, **all visually inspected**. **NFR-2 clause 2 not met (Finding F4):** "the kanban board is the only horizontal scroller" is false — the list and group tables set `min-width:940px` inside `overflow-x:auto .ms-scroll` (lines 221, 272), so at 375/768 they scroll sideways too. Visible in `ac12-group@768x1024.png`: the التقدّم column and the reclassify button are clipped and reachable only by swiping the card. Page-level overflow stays 0, so the AC passes; the NFR sentence does not. |
| **AC-13** | NFR-4 `npm run check && npm run build` exit 0; smoke 7/7 | **CONCERNS — half structurally unprovable** | `npm run check` → **exit 0** (14 checks) and `npm run build` → **exit 0**, both at the clean `645c5d8` worktree. **Smoke was not run and cannot be run against this commit**: `scripts/smoke.py` asserts against the **deployed** `massar-engine.fly.dev`, and `645c5d8` is neither deployed nor equal to the working tree. Proving "smoke 7/7 @645c5d8" requires deploying this exact commit — an outward-facing action I did not take and will not take autonomously (§8). Declared, not passed. |
| **AC-14** | edge 0/1: no ViewControls, no cap footer | **PASS** | Empty fixture: `.crmbar` = **0**, empty state «لا حملات بعد» rendered (499 chars) — `ac14-empty.png` visually confirms a clean empty screen with no filter bar over nothing. Single fixture: `.krow` = **1**, cap footer «ضيّق بالبحث» **absent**; board renders **1** column with the "grouping adds nothing here" degradation notice — `ac14-one.png`, `ac14-one-board.png`. |

---

## 3. Structurally unprovable — declared, not passed

Per instruction, these are named rather than quietly passed:

1. **AC-13 (smoke 7/7)** — unprovable at `645c5d8` without deploying that commit. `smoke.py` targets
   the deployed URL by design. **Requires a deploy to close.**
2. **AC-6, in its strongest form** — a wire-level assertion that Gupshup received nothing would
   require a send, forbidden by §8 / NO-SEND. I did **not** leave it unproven: I closed it with a
   client-side spy over fetch/XHR/beacon **plus** the server path (`campaign/test` → `setCampaignTest`
   → single `UPDATE`; `db.ts` has no gupshup reference). That is proof by exhausted code path, and it
   is stated as such.
3. **No AC in this cycle requires a schema change to prove.** BR-6 holds: filter/sort/group/selection
   are client state over the fetched `campaigns` array; the fixtures are client-injected, which is
   honest evidence for client-only state.

---

## 4. Findings (none fixed)

| id | sev | finding |
|---|---|---|
| **F1** | **P1** | **FR-6 «تحديد المطابقين» unimplemented** (AC-5 FAIL). Select-page tops out at `LIST_CAP`=60. Mitigated by an honest disclosure alert and a true ١٣٧ count pill, so no operator is misled — but the requirement is not delivered. |
| **F2** | **P2 (truth)** | **Zero-target campaign asserts it was sent.** `ac7-detail-zero.png`: verdict headline reads «أُرسلت، وبانتظار الرد الأول.» for a campaign with `targeted=0` — nothing was sent. AC-7 fixed the fabricated ٠٪ but the verdict *sentence* on the same card still claims an event that did not occur. Same defect class as «مكتملة» (Rule 2 / BR-1); outside AC-7's literal wording, so it passes the gate while contradicting its intent. |
| **F3** | **P2** | **FR-9 side panel incomplete.** التصنيف renders read-only on detail (0 `setCampClass` call sites there); `تاريخ الإطلاق` and `معرّف الحملة` are absent. Reclassification is reachable only from the list kebab and the kanban drag. Fails safe (no unbacked save path), so AC-9 still passes. |
| **F4** | **P2 (visual)** | **NFR-2 "kanban is the only horizontal scroller" is false.** List and group tables carry `min-width:940px` inside `.ms-scroll`; at 375/768 the التقدّم column and reclassify button are off-card and reachable only by swiping. Page overflow remains 0px, so AC-12 passes. |
| **F5** | **P2 (visual)** | **Alert bar occludes the bulk action bar.** `alertBar` is `position:fixed; bottom:22px; right:290px; z-index:99` (`dashboard.ts:1140`); `.bulkbar` is `position:fixed; inset-block-end:18px` with **no z-index** (`campaigns-crm.ts:47`). They share the bottom band, so the alert covers the bulk buttons for its full 3800 ms. Deterministic on the AC-5 path (select-page over a capped list *always* alerts). Visible in `ac5-selectpage-alert.png`: «تصدير المحدد CSV» is half-hidden behind «حُذفت ٦٠ المعروضة فقط…». Self-heals after 3.8 s; no data risk. **Caught only by looking at the capture — every numeric assertion on that screen was clean.** |
| **F6** | **P3** | `crmDrop` is not internally board-guarded (AC-4 depth note). Also `contactRowsHtml` is called once for the whole list and then once per row in `crmTargetRows` (line ~490) — an N+1 that the *uncommitted* working tree already deletes. Measured cost at 300 targets: median **3.5 ms**, so it is hygiene, not a performance defect. |

**NFR-3 (not an AC, measured anyway):** re-render of 400 campaigns — list **4.6 ms**, group **9.3 ms**
(max 15.7), kanban **3.1 ms**, against a 200 ms budget. Comfortably met. Zero `pageerror`s across
all 59 probe assertions.

---

## 5. Score

Weighting per `qa-validation.md` (P0 40 · P1 30 · P2 15 · visual 15). Any P0 FAIL ⇒ 0.

| band | ACs | result | points |
|---|---|---|---|
| **P0** (safety / truth / build) | AC-3, AC-4, AC-6, AC-7, AC-11 PASS; AC-13 half-provable | **no P0 FAIL** | **36.7 / 40** |
| **P1** (core function) | AC-2, AC-9, AC-14 PASS (5 ea); AC-1, AC-8 CONCERNS (2.5 ea); **AC-5 FAIL (0)** | 1 FAIL | **20 / 30** |
| **P2** | AC-10 WAIVED (D-2, correctly descoped); no P2 AC failing | — | **15 / 15** |
| **visual** | AC-12 9/9 clean and image-confirmed; −3 for F5 occlusion | | **12 / 15** |

### **Total: 84 / 100 — gate is ≥ 85 ⇒ BLOCKED**

**No P0 FAIL, so this is not a hard stop.** The run is held by one P1 FAIL (F1 / AC-5, an
unimplemented FR) and by AC-13's smoke half, which cannot be proven without deploying `645c5d8`.

## 6. Verdict

**BLOCKED — back to the Orchestrator.** Not to the CPO.

Three things close it:
1. Implement FR-6 «تحديد المطابقين» (or get a CPO waiver on the record downgrading AC-5 to the
   disclosure-only behaviour that shipped — which is defensible, since what shipped never lies).
2. Deploy `645c5d8` (or fold it into the deployed head) and run `npm run smoke` to close AC-13.
3. Decide on F2 — the «أُرسلت» headline on a zero-target campaign is the same invented-state defect
   the cycle was chartered to remove.

Before **any** re-run: the working tree must be committed or stashed. Evidence collected against a
dirty tree is not evidence about a commit, and `qa-crm.py`'s current `results.json` should be
regarded as describing an unnamed intermediate state.
