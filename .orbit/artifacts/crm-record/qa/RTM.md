# RTM — crm-record · enrichable client record
**Commit under test: `f54835c4262d4263bb3d1bbf25d2447aad9439f7`** (`f54835c`)
Delivery diff: `e60c069..f54835c` · previous QA baseline: `388832f` (this cycle, round 1)
Oracle: `.orbit/artifacts/crm-record/requirements.md` §5 + `design-plan.md` §6.
All artifact paths are relative to `.orbit/artifacts/crm-record/qa/`.

## Roll-up
**13 acceptance criteria + 3 design checks — 16 PASS, 0 CONCERNS, 0 FAIL. Score 95/100.**
Two P2 findings stay open (QA-4 documentation, QA-5 unreachable date control); neither blocks.

## Requirements traceability

| ID | Requirement | Criterion (EARS) | Method | Verdict | Evidence |
|----|-------------|------------------|--------|---------|----------|
| AC-1 | P0 · FR-1…6 the six-key contract | WHEN the record is read THE SYSTEM SHALL return `props` with only the six keys, and reject a seventh in a PATCH | API probe | **PASS** (finding QA-4 on the AC's wording) | `regression/dependency-impact.txt` ADDENDUM C |
| AC-2 | P0 · BR-1/BR-7 a fact outranks a reading | WHEN the agent re-infers over a human value THE SYSTEM SHALL refuse, keep value/source/by/ts, park `contested` once, log one `prop_rejected` | agent tool loop | **PASS** | `scenarios/SC-3-negative-agent-reinference-refused.txt` |
| AC-3 | P0 · BR-7b human-only / import-only keys | WHEN an agent-sourced write names `note` or `orgProfile` THE SYSTEM SHALL return `applied:false, not_agent_writable` and store nothing | API + guard | **PASS** | `regression/dependency-impact.txt` §3 |
| AC-4 | P0 · FR-7 confirm a reading | WHEN «أكّد» is tapped THE SYSTEM SHALL set `source:'human'` and keep the agent value/by/ts in `prior` | browser | **PASS** | `scenarios/SC-2-alternate-confirm-a-reading.txt` |
| AC-5 | P0 · the `upsertContact` trap | WHEN unrelated events and a re-hydrate follow a PATCH THE SYSTEM SHALL leave all six props identical | API + psql | **PASS** | `regression/dependency-impact.txt` §4 |
| AC-6 | P0 · BR-4 no enrichment path may send | WHEN a full PATCH runs THE SYSTEM SHALL make zero outbound WhatsApp calls | send spy + env | **PASS** | `regression/egress-assertion.txt` |
| AC-7 | P0 · BR-2 human interest correction | WHEN a human corrects الاهتمام THE SYSTEM SHALL rewrite `interest_tags`, keep unchanged products' `ts`, and render the chip as حقيقة | API + psql + browser | **PASS** | `regression/dependency-impact.txt` §5a · `scenarios/SC-3…txt` |
| AC-8 | P0 · NFR-3 the ledger is unreachable | WHEN the DB is down THE SYSTEM SHALL return `503 persisted:false`, keep the editor open with the retry line, and claim nothing | browser + docker | **PASS** | `scenarios/SC-6-failure-recovery-ledger-unreachable.txt` |
| AC-9 | P0 · RTL rendering | WHEN the panel renders THE SYSTEM SHALL be `dir=rtl`, run the phone LTR-isolated, pass `check:numerals`, and not scroll horizontally at 390 or 1440 | browser + CLI | **PASS** | `visual/design-conformance.txt` · `regression/cmd-check-numerals.txt` |
| AC-10 | BR-3 human disqualification | WHEN a human files `disqualifyReason` THE SYSTEM SHALL move `outcome`/`outcomeReason` and never set `opted_out` | API | **PASS** | `regression/dependency-impact.txt` §7 |
| AC-11 | NFR-1 bounds and erase | WHEN 121 chars are saved THE SYSTEM SHALL return `400 too_long`; WHEN an empty value is saved THE SYSTEM SHALL remove the key back to «ناقص» | API | **PASS** | `scenarios/SC-4-boundary-too-long-and-erase.txt` · `scenarios/SC-8…txt` |
| AC-12 | BR-5 one timeline line per write | WHEN a write is accepted THE SYSTEM SHALL append exactly one event naming key + writer | API + psql | **PASS** | `regression/dependency-impact.txt` §8 |
| AC-13 | Discovery §3 the missing-knowledge indicator | WHEN all six properties are absent THE SYSTEM SHALL show six visible «ناقص» holes, each tappable, and no `contextScore` | browser | **PASS** | `scenarios/AC-13-six-missing-holes.txt` · `visual/extra/ac13-six-missing@*.png` |
| D-6.1 | design-plan §6.1 · 1440 | two tracks · panel rightmost at 372±2 · gap 18 · six rail marks on one axis ±1px · no h-scroll | computed styles | **PASS** | `visual/design-conformance.txt` |
| D-6.2 | design-plan §6.2 · 900 | one column · ملف العميل → فهم المساعد → سجل التفاعل · stage name once · no rail | computed styles | **PASS** | `visual/design-conformance.txt` |
| D-6.3 | design-plan §6.3 · 390 | rows stack · phone LTR-isolated · pencil/أكّد/صحّح ≥40px · no truncation · no h-scroll | computed styles | **PASS** | `visual/design-conformance.txt` |

## Baseline comparison against the previous QA run (`388832f`)

| Finding | Severity | Then | Now |
|---|---|---|---|
| QA-1 · a latched-off pool refused every write until the process restarted | P1 | FAIL | **RESOLVED** — same PID, ledger restored, retry returns 200 and commits (`scenarios/SC-7…txt`) |
| QA-2 · the outcome button filed `no_need:` for «غير مناسب» | P2 | FAIL | **RESOLVED** — files `other:` (`scenarios/SC-8…txt` §6) |
| QA-3 · a bad date reported a length error | P2 | FAIL | **RESOLVED** — own `bad_date` code, own 400, own panel line (`scenarios/SC-8…txt` §§2-5) |
| QA-4 · AC-1 names a route that does not exist | P2 | open | **PERSISTENT** — documentation; the capability itself holds |
| QA-5 · no date control in the panel | P2 | not raised | **NEW** (pre-existing in code, first measured here) — `scenarios/PROBE-nextstep-date.txt` |

Trend: **IMPROVING** — 3 resolved, 1 persistent (doc-only), 1 new P2 that predates the cycle.

## Score
- P0 (AC-1…9, 9/9 PASS) — **40 / 40**
- P1 (QA-1, the delivery's headline fix, re-verified end to end) — **30 / 30**
- P2 (AC-10…13 PASS; two P2 findings open) — **12 / 15**
- Visual fidelity (30/30 conformance checks, 6/6 pixel pairs, AA contrast, zero console errors;
  −2 because the gate's baseline is a render-stability reference, not an approved-design render) — **13 / 15**
- **Total 95 / 100** (gate is ≥85)
