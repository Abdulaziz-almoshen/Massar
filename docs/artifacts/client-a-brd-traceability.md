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
| Campaigns | BR-CAM-004 | DEFERRED (DEC-10) | channel fixed to WhatsApp (DEC-06); start date/time and daily cap not built — see DEC-10 | S4 (decision) |
| Campaigns | BR-CAM-006 | DONE | confirm modal review summary (audience, product, objective, channel, timing, name, source, repeat, message) | S1 |
| Monitoring | BR-MON-004/006, BR-RPT-002 | DONE | «سلسلة التحويل» on the campaign's «الأداء» tab: sent → seen → replied → interested → qualified → opportunities → meetings → sent quotes → won, revenue; attribution rule `attributeLines` (campaign-results-domain), lines link to `#opps/<id>` | S4 |
| Monitoring | BR-MON-005 | DONE | knowledge score, median reply time, handoff rate (S4); self-rated confidence and reviewer-marked accuracy (S6) | S4/S6 |
| Customers | BR-CUS-001/005 | DONE | add sheet (name, city, sector, importance, owner, ≥1 contact); approval مقترح→معتمد/مرفوض; source + author + events (migration 012) | S2 |
| Customers | BR-CUS-002 | DONE | `entity_contacts` (name, role, phone, email, one primary), kept by id | S2 |
| Customers | BR-CUS-003 | DONE | «الحسابات» filters: product, sector, city, owner, status, importance, indicator; search reaches contacts | S2 |
| Customers | BR-CUS-004 | DONE | `#account/<id>`: data, contacts, owner, products with status, opportunities, campaigns, indicators, activity; opens without a conversation. Product-manager list not built | S2 |
| Knowledge | BR-KB-001/002/003 | DONE | eight weighted sections read from the document (`scoreKnowledge`), gaps listed, section editor → draft → approval | S6 |
| Knowledge | BR-KB-004/005 | DONE (runtime unobserved) | `record_answer_basis` + `handoffForAnswer` in code; approved knowledge narrowed to the locked product | S6 |
| Opportunities | BR-OPP-003/004/006/007 | DONE | `opp_activities` (meeting/call/presentation/email/note + next step), `opp_quotes` (draft→sent→accepted/rejected, apply to line), required lost reason on every path (locked-row rule), `partner` source (migration 013) | S3 |
| Reports | BR-RPT-003 | DONE | «الخسائر حسب السبب» counts board closes; reasons = ladder lost outcomes + price/competitor/cancel/fit/budget/other | S3 |
| Reports | BR-RPT-004 | PARTIAL | KPI table → campaign → attributed lines → opportunity drawer; the executive and stuck report cards are still not drillable | S4 |
| Partners | BR-PRT-001 | DONE | weekly target per partner × product (`partner_targets`), targets sheet with copy-previous-week | S5 |
| Partners | BR-PRT-002 | DONE | results مهتم/غير مهتم/لم يرد (`partner_results`), five tiles + achievement per product and partner (`summarizeWeek`) | S5 |
| Partners | BR-PRT-003 | DONE | «مهتم» → proposed account + partner opportunity (or the open one); result locked while the deal is open | S5 |
| Partners | BR-PRT-004 | DONE | per-partner follow-up with product and customer detail; «تواصل الشركاء» on the account record | S5 |
| Partners | partner login | DEFERRED | partners do not sign in; staff record for them until S7 roles | S7 |
| Org/RBAC | BR-014, NFR-001, NFR-007 | DONE | five roles (`rbac-domain`), one gate over all /admin routes, partner scope, «المستخدمون والصلاحيات» | S7 |
| Audit | NFR-002 | DONE | `audit_log` on every successful labelled /admin write, «سجل التدقيق»; agent/webhook actions stay in the stage ledger and events | S7 |
| AI labels | NFR-009 | DONE for suggestions | «توصية النظام» label, reason, dismiss/restore, modify tracked in `origin.modified` | S1 |
| KPIs §23 | adoption | DONE | Recommendation Adoption on the suggestions panel | S1 |
| KPIs §23 | read, reply, interest, qualification, opp conversion, win rate, campaign revenue, indicator yield, adoption, target achievement, handoff rate | DONE | `#reports` → «مؤشرات الأداء», `GET /admin/kpis`; rates are `funnelRates` with the BRD's own denominators and «—» over zero | S4 |
| KPIs §23 | answer confidence / accuracy | DONE | self-rated confidence (labelled as such) and reviewer-marked accuracy, last 30 days | S6 |

## Decisions the BRD leaves open (§28) and what was built meanwhile
- DEC-01 match key: phone → customer code (attrs «المعرف/رقم العميل») → folded exact name; ambiguous or partial → human review.
- DEC-02 rules vs AI scoring: rule-based only, every suggestion explainable. AI scoring is Release 3.
- DEC-03 re-targeting window: 30 days default, `SUPPRESSION_DAYS` env.
- DEC-04 minimum knowledge score: existing eligibility rule (approved or embedded knowledge) gates launch.
- DEC-06 channels: WhatsApp only.
- DEC-07 opportunity creation: existing `AUTO_OPP` flag behaviour unchanged.
- DEC-08 approval: new accounts (form, import, paste, WhatsApp) arrive «مقترح»; a «مرفوض» account is left out of campaign audiences and suggestions; «مقترح» is not blocked (to confirm with client A).
- DEC-09 account phone: required (the join key for conversations, campaigns, opportunities); Saudi mobile lengths enforced.
- DEC-10 campaign scheduling (BR-CAM-004): not built this release. A launch stays immediate and human-pressed. A scheduled start or a daily cap needs (1) approved Meta templates on the production WABA — the current sender is the Gupshup sandbox and a session message outside the 24h window fails; (2) a durable send queue with a pacer, which the engine does not have (a launch sends in-request); (3) a test send to verify it, which the standing no-send rule forbids. Revisit with the WABA migration.
- DEC-13 knowledge readiness: advisory at 60٪ of the weighted score; eligibility remains «approved knowledge or embedded» until client A sets a blocking threshold.
- DEC-14 campaign launch: administrator-only. §22 gives the product manager ✓ on «إنشاء/إطلاق حملة»; creating is granted, sending to real customers waits for the founder (CLAUDE.md §7).
- DEC-15 conversations: exec, product manager and sales may read transcripts (§22 is silent); product manager and sales may act on them (BR-AI-006). Partners may not (NFR-007).
- DEC-12 partner week: Sunday–Saturday in Riyadh time; achievement = contacts for targeted products ÷ target (may pass 100٪); a customer is counted once per partner and product, latest result wins unless an interest was already handed over.
- DEC-11 campaign attribution: a line belongs to the campaign its source names; otherwise a WhatsApp line belongs to the latest live campaign that targeted that phone for that product, launched before the line, within 30 days. Calls, visits, referrals and partners are never credited to a campaign. Rehearsals receive nothing. A sent quote counts; a draft does not.

## Slices
S1 indicators + suggestions + objective + repeat warning (this cycle) · S2 customer accounts (contacts,
importance, owner, source, filters, 360 opportunities) · S3 opportunities (meetings, quotes, lost reason,
partner source) · S4 campaign funnel, review summary, KPIs, scheduling decision · S5 partners · S6
knowledge sections + weighted score · S7 RBAC + audit log.
