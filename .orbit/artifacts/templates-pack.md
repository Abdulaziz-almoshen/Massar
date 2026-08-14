# مسار — حزمة قوالب واتساب الرسمية (Meta templates)
Extracted from the AI-agent evaluation (expert panel, 2026-08-11) for the production WABA
migration. NOT submitted anywhere — these are drafts for human review and Meta approval.
Engine note: sendTemplate() needs a small extension to carry DOCUMENT-header media for T2.

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

