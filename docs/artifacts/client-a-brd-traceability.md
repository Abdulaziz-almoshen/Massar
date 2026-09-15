# Client A — BRD v1.0 traceability (2026-09-15)

Source: `BRD_منصة_مسار_إدارة_التسويق_والمبيعات.docx` and the client's standalone prototype
(`مسار - نظام إدارة المبيعات (نسخة مستقلة).html`). The prototype differs from our `_مسار/مسار.dc.html`
in exactly one module: «مؤشرات استخدام العملاء» (a tab under العملاء plus the «مؤشر استخدام جديد»
form). Everything else in the prototype is attribute renames from a re-export.

Baseline measured against `massar-engine` HEAD 4e26c1f by reading code (not names): ~20 IDs DONE,
~30 PARTIAL, ~15 MISSING. Status below is AFTER the slice named in the last column.

| Area | ID | Status | Evidence / gap | Slice |
|---|---|---|---|---|
| Indicators | BR-IND-001..006, AC-001..003 | DONE | `usage_indicators` + members + audit (migration 011), `#indicators`, `#indicator/new|<id>|<id>/data`, drawer | S1 |
| Indicators | BR-IND-003, NFR-006 | DONE | `/admin/indicators/preview`: matched / review / unmatched, candidates, duplicates | S1 |
| Indicators | BR-IND-007/008, AC-004 | DONE | `suggestOpportunities` (5 rules, reasons, source indicators, count after exclusions) | S1 |
| Campaigns | BR-CAM-001 | DONE | objective required in wizard; `campaigns.objective` | S1 |
| Campaigns | BR-CAM-002 | PARTIAL | indicator added as audience filter; region/type/sector still only spreadsheet columns | S1 / S2 |
| Campaigns | BR-CAM-003, BR-MON-002/003, AC-005/006 | DONE | suggestions panel on `#kmon` and in `#aimkt`; «إنشاء حملة» prefills product+audience+objective | S1 |
| Campaigns | BR-CAM-007, BRULE-011 | DONE | `checkRepeatTargeting` warning in wizard (30-day window, `SUPPRESSION_DAYS`) | S1 |
| Campaigns | BR-CAM-004 | MISSING | no scheduling / daily cap; session sends need the 24h window → real scheduling needs approved templates (production WABA) | S4 (decision) |
| Campaigns | BR-CAM-006 | DONE | confirm modal review summary (audience, product, objective, channel, timing, name, source, repeat, message) | S1 |
| Monitoring | BR-MON-004/006, BR-RPT-002 | PARTIAL/MISSING | campaign stops at «interested»; no qualified/meetings/opps/won/revenue chain | S4 |
| Monitoring | BR-MON-005 | MISSING | no response-time / handoff-rate / confidence metrics | S4 |
| Customers | BR-CUS-001/005 | DONE | add sheet (name, city, sector, importance, owner, ≥1 contact); approval مقترح→معتمد/مرفوض; source + author + events (migration 012) | S2 |
| Customers | BR-CUS-002 | DONE | `entity_contacts` (name, role, phone, email, one primary), kept by id | S2 |
| Customers | BR-CUS-003 | DONE | «الحسابات» filters: product, sector, city, owner, status, importance, indicator; search reaches contacts | S2 |
| Customers | BR-CUS-004 | DONE | `#account/<id>`: data, contacts, owner, products with status, opportunities, campaigns, indicators, activity; opens without a conversation. Product-manager list not built | S2 |
| Knowledge | BR-KB-001/002/003 | PARTIAL | 4-cell readiness, no weighted per-section score, no guardrails/competitors sections | S6 |
| Knowledge | BR-KB-004/005 | PARTIAL | prompt-enforced only; no confidence signal | S6 |
| Opportunities | BR-OPP-003/004/006/007 | DONE | `opp_activities` (meeting/call/presentation/email/note + next step), `opp_quotes` (draft→sent→accepted/rejected, apply to line), required lost reason on every path (locked-row rule), `partner` source (migration 013) | S3 |
| Reports | BR-RPT-003 | DONE | «الخسائر حسب السبب» counts board closes; reasons = ladder lost outcomes + price/competitor/cancel/fit/budget/other | S3 |
| Reports | BR-RPT-004 | PARTIAL | report cards not drillable | S4 |
| Partners | BR-PRT-001..004 | MISSING | `#partners` is a placeholder | S5 |
| Org/RBAC | BR-014, NFR-001 | PARTIAL | one admin token + rep tokens; roles never authorize | S7 |
| Audit | NFR-002 | PARTIAL | indicator audit done (S1); launches/opp edits/KB changes have no audit table | S7 |
| AI labels | NFR-009 | DONE for suggestions | «توصية النظام» label, reason, dismiss/restore, modify tracked in `origin.modified` | S1 |
| KPIs §23 | adoption | DONE | Recommendation Adoption on the suggestions panel | S1 |
| KPIs §23 | qualification, opp conversion, win rate, campaign revenue, handoff rate, confidence | MISSING | | S4 |

## Decisions the BRD leaves open (§28) and what was built meanwhile
- DEC-01 match key: phone → customer code (attrs «المعرف/رقم العميل») → folded exact name; ambiguous or partial → human review.
- DEC-02 rules vs AI scoring: rule-based only, every suggestion explainable. AI scoring is Release 3.
- DEC-03 re-targeting window: 30 days default, `SUPPRESSION_DAYS` env.
- DEC-04 minimum knowledge score: existing eligibility rule (approved or embedded knowledge) gates launch.
- DEC-06 channels: WhatsApp only.
- DEC-07 opportunity creation: existing `AUTO_OPP` flag behaviour unchanged.
- DEC-08 approval: new accounts (form, import, paste, WhatsApp) arrive «مقترح»; a «مرفوض» account is left out of campaign audiences and suggestions; «مقترح» is not blocked (to confirm with client A).
- DEC-09 account phone: required (the join key for conversations, campaigns, opportunities); Saudi mobile lengths enforced.

## Slices
S1 indicators + suggestions + objective + repeat warning (this cycle) · S2 customer accounts (contacts,
importance, owner, source, filters, 360 opportunities) · S3 opportunities (meetings, quotes, lost reason,
partner source) · S4 campaign funnel, review summary, KPIs, scheduling decision · S5 partners · S6
knowledge sections + weighted score · S7 RBAC + audit log.
