# Growth slice — lead alerts + retargeting + portal UX pass
2026-08-11 · R20: "not happy with UX/UI for creating a campaign and clients and dashboards;
no retargeting; if a potential client is serious what is the next action? agent should
message the product manager."

## Discovery (product-discovery)
Three real gaps, two functional: (1) the funnel dead-ends at جاد🔥 — the human who can
close never hears about it (the R16 no-dead-end law applies to the OWNER side too);
(2) retargeting was a pillar of the original MVP spec (track → filter → re-engage) and
is absent — campaigns are read-only trophies today; (3) the screens list data but don't
yet feel like the marketing product the prototype promises (his standing marketing-tool
bar, now a 3-signal Rule). Also discovered: the wizard's product step is the STATIC seed
list — hub-uploaded products (صحة أعمال Plus) can't be campaigned at all. Right bet:
close the loop (alert → human close; cohort → retarget) + make the four surfaces read
professional. Not in scope: saved-segment engine, multi-user roles, email channels.

## Business rules (business-analyst)
Lead alert: trigger = tag_interest level 'hot' OR request_human_handoff; recipient =
NOTIFY_NUMBER (fly secret; the PM's opted-in number); content = lead card (name/phone,
product, seriousness, last customer line, portal deep link); throttle = 1 alert per
contact per 6h (in-memory, ledger-noted); enforced in code (agent runtime), never via
prompt; event kind lead_alert recorded; tracker chip «أُبلغ المدير ✓». Silent no-op if
NOTIFY_NUMBER unset. Retarget: from campaign detail's ACTIVE filter (الكل/شوهدت/ردّوا/
مهتمون/فشل) → button carries cohort {phone,name}[] into the wizard; wizard shows a
locked cohort card (count + مسح); launch posts those targets (entities selection
bypassed); name defaults «إعادة استهداف — <filter> — <campaign>»; all launch guards
unchanged (cap 50, opt-out skip, confirm modal). Wizard products = seed ∪ hub registry
(hub-only products get knowledge chips, no fake scores). ACs: (1) hot tag live → PM
WhatsApp receives lead card ≤5s, event logged, chip visible; (2) throttle: second hot
signal within window sends nothing; (3) handoff also alerts; (4) retarget: filter ردّوا
→ button → wizard cohort card N correct → modal N correct (cancel — no send needed
beyond the alert proof); (5) hub product selectable in wizard step-1; (6) home shows
KPI row + hot-leads list + recent campaigns + quick actions from live data; (7) build,
node --check, 3-viewport captures ×4 screens, 0 console errors, gate PASS @commit.

## Prior art (market-researcher)
Intercom/HubSpot: lead-qualification alerts go to the OWNER's channel (Slack/email) with
contact card + one-click open — the WhatsApp equivalent here is a message to the PM's
own WhatsApp (he lives there) with a dashboard deep link. Mailchimp: retarget = segment
on campaign activity (opened/not-opened/clicked) → "create campaign from segment" — our
filter chips are exactly that activity segmentation; the button completes the known
pattern. Klaviyo home: KPI band → recent campaigns → action shortcuts; adopt that shape
for vHome. No new deps needed anywhere.

## Plan (planner)
1. config.ts: notifyNumber (NOTIFY_NUMBER). 2. agent.ts: notifyLead(contact, product,
level, reason, lastMsg) — throttled Map, sendText to notifyNumber, tracker.recordSystem
+ events lead_alert, called from tag_interest(hot) + request_human_handoff. 3. fly
secrets set NOTIFY_NUMBER (PM's opted-in number) + .env. 4. dashboard.ts: retargetCohort
global + kmon-detail button on active filter + wizard cohort card + launch body override;
wizard products from registry (seed sc + hub chip); vHome rebuild (KPI band incl. حملات
and تم التسليم, hot-leads list w/ openConvo links, recent campaigns mini-table, quick
actions); customers stats header (إجمالي/top-segment counts). 5. Prove per ACs (live
alert to PM number = sandbox self-test, pre-authorized); captures ×4 screens ×3
viewports; evidence + gate; reviewer packet on new commits; CPO round-7 binds the
combined audience+growth delivery; reporter.

## Design treatment (designer — massar-design-language)
Home: KPI band (existing .kpi idiom, add tone colors), then two-column: «عملاء جادون
الآن» card (rows: avatar, name, product·level chip, آخر رسالة truncated, عرض المحادثة ←)
+ «أحدث الحملات» card (name, sent/seen/replied minis, فتح ←); quick-actions row of two
tinted buttons (إنشاء حملة / استيراد مستهدفين). Wizard: keep step cards but connect
with a start-side rail; step-1 grid = registry cards (hub-only: teal معرفة ✓ chip
instead of score bar); sticky bottom launch bar (count · product · CTA) replacing the
inline centered button. Customers: stats strip above the dropzone (جهة · شرائح · آخر
استيراد). Retarget button: gold-tint (#C9A227 family) — it's an action on tracked
truth. Alert chip: c-teal «أُبلغ المدير».
