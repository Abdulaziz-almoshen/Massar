# Massar WhatsApp Sales Agent — Expert Evaluation

**Date:** 2026-08-11 · **Evaluator:** AI-agent expert panel (read-only review)
**Scope:** `massar-engine/src/agent.ts` (persona, KB, tools, hard rules), `src/gupshup.ts` (channel capabilities), live production state (`/admin/state`) and two real transcripts: `966559402621` (مجمع عبدالعزيز الطبي — long demo thread, 30 turns) and `966500000777` (عيادة الاختبار للتجميل — hot-lead flow).
**Nothing was sent, toggled, or modified during this review.**

---

## Grade: 7 / 10

Strong conversational core — question discipline, button usage, and hot-lead recognition are genuinely
above the bar for B2B WhatsApp agents. The grade is held back by three verified hard-rule defects
(opt-out false positives, a turn-cap dead end, prompt-only bubble discipline), a "specialist will
contact you" promise with no machinery behind it, and the absence of the approved-template layer that
production WABA legally requires for any business-initiated message.

---

## 1. Conversation Quality

### 1.1 Opening strength — Good (with two gaps)

The current campaign opener shape (observed 14:55 in the demo thread):

> مرحبًا {الاسم} 👋 معك مساعد لِين الرقمي. نساعد المنشآت الصحية على تقليل زمن إصدار الإجازات المرضية بنسبة 70% بتوثيق رسمي وتكامل مع أنظمتكم. هل يناسبكم عرض تعريفي قصير هذا الأسبوع؟

What's right: leads with a quantified outcome (70%), identifies itself honestly as a digital assistant
(per prompt rule «لا تدّعِ أنك إنسان»), one CTA question, one emoji, name personalization.

Gaps:
- **No legitimacy line.** Cold B2B outreach in KSA converts and survives better with half a line of
  "why you": «بصفتكم مجمعًا طبيًا في الرياض…». Also reduces "من أنتم؟" replies and blocks.
- **No opt-out affordance in the cold opener.** A visible exit («ليس الآن» button or footer) measurably
  reduces *blocks* — and blocks damage WhatsApp quality rating far more than opt-outs do.

### 1.2 Question discipline — Excellent

Rule in prompt: «سؤال واحد كحد أقصى» + golden rule «كل رسالة تنتهي إمّا بسؤال ذكي أو بأزرار».
**Verified across both transcripts: every single agent message ends with exactly one question or a
button set.** No double-questions found. The qualification ladder in the demo thread is textbook —
one variable per turn: branches → current system (HIS) → time window (صباحًا) → stakeholders
(«هل هناك شخص آخر من فريق التقنية أو التشغيل تودون إشراكه؟»). That last one is a genuinely good
enterprise move most human SDRs forget.

### 1.3 Objection handling — Good on the one live sample; untested at depth

Only mild friction appears in the transcripts. When the customer pushed back —
«تقريبا خمس فروع ليه تسأل؟» — the agent recovered exactly right: justified the question, converted the
answer into a package recommendation («خمس فروع تدخل ضمن باقة المؤسسات… بـ95,000 ر.س»), and moved on.
The KB's canned objection pairs (price, "we have a system") are well-written but **no transcript yet
exercises a hard price/competitor objection** — flag for the first real-campaign spot-checks.

### 1.4 Pivot behavior — Good design, one live proof

The PIVOTS matrix (segment → next-best product, max 2 alternatives, then graceful handoff) is the
right architecture. Live evidence: «عندكم خدمات ثانية؟» → agent listed the portfolio and split intent
with 3 buttons. It never pushed an unrequested pivot in either thread. `offer_alternative` exists but
was never triggered — pivot success is currently **unmeasured** (see §5).

### 1.5 Closing moves — Good in-chat, broken after the chat

In-chat closing is strong: every interest signal is pushed to a concrete step («عرض تعريفي قصير هذا
الأسبوع»), time-boxed (صباحًا/بعد الظهر buttons), stakeholder-expanded. The hot-lead flow
(`966500000777`) was near-perfect: buying intent recognized on message one, `tag_interest(hot)` fired,
PM alert pushed (SYSTEM: «أُبلغ المدير: عميل جاد»), exact prices given, qualifying question asked, and
the final handoff carried a rich reason: «العميل يرغب بإتمام الاشتراك وطلب اتصالًا غدًا الساعة 10 صباحًا».

**But the close depends on a promise the system cannot keep.** «تم إشعار المختص» was said 3 times in
4 minutes to the demo lead; «سيتواصل معكم المختص» appears in both threads; nothing schedules, reminds,
or follows up if the human never shows. The demo thread shows the cost (see §4.1).

### 1.6 Arabic register — Good MSA, one systematic flaw

The agent holds clean, warm MSA while customers write Gulf dialect («أبغى») — the correct register
asymmetry for B2B. Respectful plural (لديكم/يناسبكم) is consistent.

The flaw: **it addresses the organization name as a person, in vocative, repeatedly** —
«ممتاز يا مجمع عبدالعزيز الطبي»، «تم يا مجمع عبدالعزيز الطبي». `waName` is the org name; the prompt's
«استخدم اسمه الأول باعتدال» has no org/person distinction, so the model mail-merges the full facility
name 4× in one thread. Reads robotic in Arabic. Fix in prompt: if the name looks like a facility
(مجمع/مركز/عيادة/مستشفى/صيدلية…), greet the *person* («أهلًا بكم») and use the facility in third person.

### 1.7 Length and emoji discipline — Excellent

All conversational replies are 2–4 lines (rule: «سطران إلى أربعة»). Emoji: near-zero in conversation
turns, single emoji in openers, 🌿 on opt-out confirmation. This is exactly right; most AI sales
agents fail here.

### 1.8 Grounding — One embellishment found

The cross-sell reply named «سجل التطعيمات **الوطني**» — the KB says only «سجل موحّد». Small, but it is
precisely the claim-inflation class §3 of CLAUDE.md warns about (an unverifiable regulatory-sounding
adjective). Pricing was quoted verbatim-correct in all observed turns. Recommend adding a KB line:
"never add certification/regulatory adjectives not present in the KB."

---

## 2. Capability Usage (text vs buttons vs document)

### 2.1 Buttons — Best-in-class usage

Every choice point became ≤3 quick-reply buttons with customer-voice labels, all within limits
(code enforces ≤20 chars via `slice(0,20)`; WhatsApp allows 25):

| Moment | Buttons observed |
|---|---|
| After price quote | أبغى عرض تعريفي · لدينا فرع واحد · لدينا عدة فروع |
| Channel preference | اتصال هاتفي · واتساب |
| Scheduling | صباحًا · بعد الظهر |
| Demo vs info | نعم، هذا الأسبوع · أرسل التفاصيل أولًا |
| Cross-sell | فحص الموظفين · التقارير الطبية · سجل التطعيمات |

Two nits: (a) the 13:07 message attached صباحًا/بعد الظهر buttons to a statement with no question
text — the question was implied only by the buttons; (b) `slice(0,20)` truncates silently mid-word if
the model ever exceeds 20 — log a warning instead of silently cutting Arabic labels.

### 2.2 Document + caption — right moment, wrong enforcement

The intro-PDF moment is correct: sent on explicit request («أرسل لي الملف التعريفي») and available for
product openers, with a no-repeat rule («لا ترسل نفس الملف مرتين»). The single-bubble
document+caption shape (R32 reality check in `index.ts`: quick_reply+document renders as *separate*
messages on real devices; document-with-caption is the guaranteed single bubble) is the right final
form — the 21:13 test confirms it renders as one bubble.

**But single-bubble discipline is prompt-only.** At 13:16 live, the model ignored the tool result's
«أرجِع ردًا فارغًا» instruction and sent a follow-up text+buttons after the file — a double bubble to a
real thread. Enforce in code: after a successful `send_asset`, suppress (or hard-gate) any non-empty
`finalText` for that turn in `agent.ts`'s round loop.

### 2.3 Cold opener with PDF attached — test both ways

Today's campaign launch leads with the document when an intro asset exists. That survives the WABA
migration (templates support DOCUMENT headers), but the stronger ladder for cold B2B is usually:
light text opener → PDF *on* the «أرسلوا التفاصيل» tap. The tap is an engagement event (feeds
interest tags + keeps the window fresh) and the document lands on a warmed reader. Recommend A/B:
`lean_intro_product_v1` vs `lean_intro_doc_v1` (both drafted in §3).

---

## 3. Template Strategy — the production gap, and a starter pack

**Current state:** `gupshup.ts` has `sendTemplate(destination, templateId, params)` and
`/admin/send-template` exists, but **zero templates are in use** — campaign launches go out as
*session* messages (document/quick-reply/text). That works only in the sandbox (recipients opted in
by messaging first). On the production WABA, any business-initiated message — campaign opener,
follow-up, retarget, re-engagement — **must be a Meta-approved template**; session messages are
allowed only inside the 24h customer-service window. This is the single biggest go-live blocker.

Engine note: `sendTemplate` currently sends only `{id, params}` — document-header templates on
Gupshup additionally need the media payload (`message: {"type":"document","document":{link,filename}}`).
Small adapter extension needed for `lean_intro_doc_v1`.

Operational rules to pair with the pack: new-number warm-up (Meta messaging tiers: 250 → 1K → 10K
unique users/24h — ramp sends gradually), per-contact frequency cap (≥72h between marketing
templates, ≤2 unanswered nudges per lead per month), and stop-on-quality-drop (pause campaigns if
quality rating leaves "High").

### Starter pack — 6 Arabic templates to Meta approval standards

Submission checklist applied to all: honest category (utility claims carry zero promo content);
sample values supplied for every variable; no line that is only a variable; body never begins or
ends with a variable; no ALL-CAPS/exclamation stacking/spam phrasing («مجانًا!!», «عرض لن يتكرر»);
marketing templates carry an opt-out footer; names snake_case; language `ar`; buttons ≤20 chars
(engine limit).

---

**T1 · `lean_intro_product_v1` — MARKETING · ar** (cold opener, text)

- **Body:**
  > مرحبًا {{1}}، معك مساعد لِين الرقمي من شركة لِين للصحة الرقمية.
  > بصفتكم منشأة صحية، نساعدكم على أتمتة {{2}} بتوثيق رسمي معتمد وتكامل مع أنظمتكم، ويقل زمن الإصدار حتى 70%.
  > هل يناسبكم عرض تعريفي قصير هذا الأسبوع؟
- **Footer:** للإيقاف أرسل «إيقاف»
- **Buttons (quick reply):** أرغب بعرض تعريفي · أرسلوا التفاصيل · ليس الآن
- **Samples:** {{1}} = مجمع النخيل الطبي · {{2}} = الإجازات المرضية
- Why it passes: introduces the business by name, states a legitimate B2B reason, single soft CTA,
  visible exit. The «ليس الآن» button converts silent annoyance into a taggable signal instead of a block.

**T2 · `lean_intro_doc_v1` — MARKETING · ar** (cold opener, intro-PDF header — A/B twin of T1)

- **Header:** DOCUMENT (sample: الإجازات-المرضية-تعريفي.pdf)
- **Body:**
  > مرحبًا {{1}}، معك مساعد لِين الرقمي من شركة لِين للصحة الرقمية.
  > أرفقنا لكم الملف التعريفي لخدمة {{2}} — إصدار إلكتروني موثّق، تكامل مع HIS وERP، وتفعيل خلال 5 أيام عمل.
  > هل نرتب لكم عرضًا تعريفيًا قصيرًا هذا الأسبوع؟
- **Footer:** للإيقاف أرسل «إيقاف»
- **Buttons:** أرغب بعرض تعريفي · لدينا استفسار · ليس الآن
- **Samples:** {{1}} = مجمع النخيل الطبي · {{2}} = الإجازات المرضية
- Preserves today's proven single-bubble doc+caption shape across the WABA migration.

**T3 · `lean_followup_48h_v1` — MARKETING · ar** (no-reply nudge, send once, ~48h after opener)

- **Body:**
  > مرحبًا {{1}}، تواصلنا معكم قبل يومين بخصوص خدمة {{2}} ولعل الانشغال حال دون الرد.
  > إن كان الموضوع يهمكم، يسعدنا ترتيب عرض تعريفي قصير في الوقت الأنسب لكم — وإن لم يكن مناسبًا الآن، يكفي اختيار «ليس الآن» ولن نكرر التذكير.
- **Footer:** للإيقاف أرسل «إيقاف»
- **Buttons:** أرغب بعرض تعريفي · ليس الآن
- **Samples:** {{1}} = مجمع النخيل الطبي · {{2}} = الإجازات المرضية
- The explicit "we won't nag" promise («لن نكرر التذكير») is a quality-rating protector — honor it in code.

**T4 · `lean_retarget_seen_v1` — MARKETING · ar** (read-but-silent retarget — new angle, not a repeat)

- **Body:**
  > مرحبًا {{1}}، سؤال واحد قصير: كم ساعة يقضي فريقكم أسبوعيًا في {{2}}؟
  > منشآت صحية مثلكم خفّضت هذا الوقت إلى دقائق بعد الأتمتة — بتوثيق رسمي ومن دون إدخال مزدوج.
  > إن أحببتم، نطلعكم على الطريقة في عرض قصير.
- **Footer:** للإيقاف أرسل «إيقاف»
- **Buttons:** أطلعوني على التفاصيل · ليس الآن
- **Samples:** {{1}} = مجمع النخيل الطبي · {{2}} = إصدار الإجازات المرضية وتوثيقها
- Targets `read`-without-`replied` contacts (tracker already records both). Pain-question angle
  instead of re-pitching — the retarget best practice Meta reviewers also favor.

**T5 · `lean_hot_confirm_v1` — UTILITY · ar** (hot-lead / handoff confirmation)

- **Body:**
  > مرحبًا {{1}}، نؤكد استلام طلبكم بخصوص {{2}}.
  > سيتواصل معكم مختصنا {{3}} كما اتفقنا. إن رغبتم بتغيير الموعد أو كان لديكم سؤال قبله، تفضلوا بالرد على هذه الرسالة.
- **Buttons:** تغيير الموعد · لدينا سؤال
- **Samples:** {{1}} = عيادة الاختبار للتجميل · {{2}} = عرض تعريفي لخدمة الإجازات المرضية · {{3}} = غدًا الساعة ١٠ صباحًا
- Category justification: confirms an action the customer explicitly requested (a callback/demo) —
  transaction-specific, zero promotional content, so it qualifies as UTILITY. Keep it promo-free or
  Meta reclassifies it as marketing. This is the template that turns «سيتواصل المختص» from a hope
  into a system: fire it on `request_human_handoff` / hot `tag_interest`, and it also reopens the
  window if the specialist slips past 24h.

**T6 · `lean_reengage_60d_v1` — MARKETING · ar** (long-silence re-engagement)

- **Body:**
  > مرحبًا {{1}}، مضت فترة منذ آخر حديث بيننا حول خدمات لِين للصحة الرقمية.
  > أضفنا منذ ذلك الحين تحسينات على {{2}}، ويسعدنا استئناف الحديث إن كان الوقت أنسب الآن — عرض قصير واحد يكفي لتقييم الجدوى لمنشأتكم.
- **Footer:** للإيقاف أرسل «إيقاف»
- **Buttons:** نعم، رتبوا عرضًا · أرسلوا الجديد · ليس الآن
- **Samples:** {{1}} = مجمع النخيل الطبي · {{2}} = خدمة الإجازات المرضية وتكامل الأنظمة
- «أرسلوا الجديد» gives a low-commitment middle option that restarts the 24h window for the agent.

---

## 4. Failure Modes Visible in the Transcripts

### 4.1 The 3.5-hour dead end after the CTA tap (severity: high — root cause fixed, risk class open)

Demo thread, 09:36: the customer tapped **«أبغى عرض تعريفي»** — the highest-intent action possible —
then wrote «الو؟» (09:37), «الو» (11:38), «الو» (13:04). **Three unanswered pings over 3.5 hours from
the hottest possible lead.** Cause: the agent's turn had triggered a handoff, and the then-current
code muted the agent on handoff (`human=true`). The fix is already in `tracker.ts` («handoff no
longer flips `human`… A requested specialist without an active human must never dead-end the
customer») — correct fix. What remains open is the *class*: every «سيتواصل المختص» promise still has
no SLA timer, no reminder to the PM beyond the one throttled lead card, and no automated follow-up to
the customer (T5 above). Add a dead-air monitor: customer message unanswered > 5 minutes → alert.

### 4.2 The turn cap is a permanent canned-message loop (severity: high — live right now)

`MAX_AGENT_TURNS = 12`, but `agentTurns` is incremented by **every** `recordAgentReply` — including
campaign blasts and `/admin/send-test` messages. Contact `966559402621` already sits at **17/12**:
its next message will get the canned «شكرًا لتفاعلك — سيتولى أحد مختصينا…» — and because the cap
check has no once-guard and `safeSend` increments the counter further, **every subsequent message
from this hot lead gets the identical canned line, forever** (no reset mechanism exists). Fix:
count only genuine conversational turns, send the cap message once, reset on human resume / new
campaign / new day.

### 4.3 Opt-out false positives — verified by test (severity: high for production)

`isOptOut()` matches Arabic keywords as bare substrings anywhere in the message. Verified against the
live patterns:

| Customer message (benign) | Result |
|---|---|
| «كيف **أوقف** التزوير في الإجازات؟» | permanently opted out |
| «نبغى ن**توقف** عن الورق نهائيًا» | permanently opted out |
| «متى ت**توقف** الباقة؟» | permanently opted out |
| «ابغى ا**حظر** الموظف من التعديل» | permanently opted out |
| "can I **cancel** a sick leave in the system?" | permanently opted out |

The first one is brutal: the product's own pitch is «يقفل باب التزوير» — a customer *echoing the
value prop* gets silenced forever («تم إيقاف الرسائل نهائيًا»). Keep the sacred hard-rule
architecture, but tighten matching: anchor bare verbs to short standalone messages (e.g. message
≤ 3 words), keep «إيقاف»/«لا تراسلني»/STOP exact, and route ambiguous hits through one LLM
confirmation turn («هل ترغبون بإيقاف الرسائل نهائيًا؟» + button) before flipping the permanent flag.

### 4.4 Repetition and formula slips (severity: medium)

- «تم إشعار المختص» 3× within 4 minutes (13:04, 13:06, 13:07) — trust erosion through formula.
- Full org name in vocative 4× («يا مجمع عبدالعزيز الطبي») — see §1.6.
- 13:16: double bubble after `send_asset` despite the "return empty" tool instruction — see §2.2.

### 4.5 Interest-tag spam (severity: low, pollutes retargeting data)

`tag_interest` fired **5 identical hot tags** for the same product on `966559402621` (09:36, 13:04,
13:05, 13:06, 13:07 — roughly once per turn once the lead was hot). `addTag` has no dedupe. The 6h
`notifyLead` cooldown contained the WhatsApp noise (and its in-memory map resets on deploy — worst
case one duplicate card, acceptable), but the tag ledger that will drive retargeting audiences is
being inflated. Dedupe on (product, level) within a conversation.

### 4.6 Campaign personalization hazard (severity: note)

14:55 test into the demo thread opened «مرحبًا صيدلية الدواء (مثال) 👋» — a wrong-name send (test
data, but the launch path has no guard comparing the target list name against the existing contact's
`waName`). A mismatch check before send would prevent the single most embarrassing campaign bug.

### 4.7 Not yet observed (watch in first real campaign)

Hard price/competitor objections, multi-product confusion, voice notes/images inbound (non-text
`msgType` currently yields empty `text` — the agent replies to ""), rapid message bursts
(per-phone FIFO serializes correctly, but each burst message gets its own LLM turn against
stale context — consider a 5–10s coalesce window).

---

## 5. Measurement — KPI set per agent turn / conversation / campaign

Most of these are computable today from `transcript` timestamps, `statusTimes`, `tags`, and the
`events` table — no new instrumentation, just queries.

**Per agent turn**
1. **Response latency** — customer msg → agent send, p50/p95; alert on > 5 min dead air inside an
   open session (would have caught §4.1 in real time).
2. **No-dead-end compliance** — % of agent messages ending in a question or buttons (the golden
   rule, currently 100% in samples — keep it measured, it's the first thing model drift breaks).
3. **Length compliance** — % of messages ≤ 4 lines; **question count** = exactly 1.
4. **Grounding audit** — price strings must match KB verbatim (regex); weekly sample of claims vs
   KB (catches «الوطني»-class embellishments).

**Per conversation**
5. **Reply depth** — customer messages per conversation; median turns to first tag and to outcome.
6. **Button CTR** — button taps ÷ button messages shown (inbound `msgType` button/interactive
   is already normalized in `gupshup.ts`). The single best proxy for message quality.
7. **Pivot success** — `offer_alternative` → subsequent `tag_interest` in the same conversation.
8. **Tag precision** — % of hot tags the PM confirms as real after contact (false-hot rate), plus
   duplicate-tag rate (currently 5:1 on the demo thread — see §4.5).
9. **Handoff precision** — % of handoffs whose `outcomeReason` contains product + concrete next step
   (both live samples pass — keep the bar); **handoff SLA** — handoff → first human touch, p50/p95.
10. **Asset engagement** — reply-within-24h rate after PDF send vs without (decides the §2.3 A/B).

**Per campaign / number health**
11. **Funnel** — sent → delivered → read → replied → tagged → handoff (counters already exist:
    `status:*`, `tag`, `outcome:*`; exclude `test=true` contacts).
12. **Opt-out rate** and **false-opt-out review count** (every opt-out gets a 10-second human glance
    while §4.3 is being fixed); **block/failure signals** — `status:failed` error codes trending up
    is the early warning before Meta drops the quality rating.
13. **Turn-cap hits** and **dead-air incidents** — both should be ~0 once §4.2 and T5 land.

---

## Top 5 Improvements (priority order)

1. **Fix the opt-out matcher** — verified false positives on benign sales questions («كيف أوقف
   التزوير؟» → permanent opt-out); anchor bare verbs to short standalone messages and confirm
   ambiguous hits with one button question before flipping the permanent flag.
2. **Fix the turn-cap dead end** — the cap counts campaign/test sends and then answers every
   message with the same canned line forever; contact 966559402621 is already at 17/12 and will
   hit the wall on its next message. Count conversational turns only, fire once, add a reset.
3. **Put machinery behind «سيتواصل المختص»** — SLA timer + `lean_hot_confirm_v1` utility template +
   dead-air alert; the demo thread showed a hot lead pinging «الو» for 3.5 hours after tapping the CTA.
4. **Ship the approved-template layer before the production WABA** — the 6-template pack above,
   per-contact frequency caps, number warm-up ramp; today's session-message campaign path cannot
   legally open conversations outside the sandbox.
5. **Polish the human layer** — org-name-aware greeting (stop «يا مجمع عبدالعزيز الطبي»), suppress
   post-`send_asset` extra bubbles in code rather than prompt, dedupe interest tags, and vary the
   «تم إشعار المختص» confirmation phrasing.

---

## Appendix — evidence pointers

- Agent core: `/Users/abdulaziz/Projects/Massar/massar-engine/src/agent.ts` (prompt lines 173–217,
  tools 221–301, opt-out 391–398, turn loop 400–463, lead alerts 303–332).
- Channel shapes: `/Users/abdulaziz/Projects/Massar/massar-engine/src/gupshup.ts` (text 74, quick-reply 82,
  single-bubble doc+caption 121, image 115, template API 127).
- Campaign send path + R32 single-bubble reality check: `/Users/abdulaziz/Projects/Massar/massar-engine/src/index.ts` (145–199).
- Turn/tag ledger: `/Users/abdulaziz/Projects/Massar/massar-engine/src/tracker.ts` (handoff/human note at 113–124).
- Transcripts reviewed from live `/admin/state` on 2026-08-11 (contacts 966559402621, 966500000777, both `test=true`).
