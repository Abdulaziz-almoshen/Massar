# Design Plan — رحلات الحملات داخل ملف العميل

Screen: `#customer/<phone>` → `vCustomer()`, `massar-engine/src/dashboard.ts` ~1878.
Style: approved Massar design language (gate B). 3 prototypes built, **v3-ledger-scope** selected.
Record: `design/approved.json`. Tokens: `DESIGN.md` § cycle `journey-scope`.

## 0. The journey is an addressable object, not a filter
Route `#customer/<phone>/c/<campaignId>`. The API already takes `?campaign=<id>` and already
windows `interactionRead`. Deep-linkable, back/forward-safe, one journey = one URL = one lifecycle
state. The ledger below is that object's index, not a filter widget over a lifetime feed.

## 1. Scope selector
Sticky banner under the back link, above the contact header, `z-index:30`. Deep-navy gradient
scoped, white card lifetime. Three lines: «الأرقام في هذه الصفحة تخصّ» / «حملة: تكامل HIS — يوليو» /
«النافذة: ٢٨ يوليو ٠٩:١٢ ← ٢٩ يوليو ٠٩:١٢ · ٢٤ ساعة، مثل نافذة الخدمة في واتساب».
`<select>` switches; «إلغاء النطاق» returns to lifetime, where it reads
«كامل السجل — لا نطاق حملة · كل ما جرى منذ أول رسالة في ٢ يوليو».
Default = newest journey whose window contains a real event, else lifetime. Arriving from a
campaign page pre-selects that campaign.

## 2. Journey row
`rail | name+window | أُرسلت | وصلت | شوهدت | ردّ | chip`.
**Belongs:** four real timestamps (`direction:ltr`), window bounds under the name, one lifecycle
chip — ردّ · شوهدت بلا ردّ · لم تُفتح · فشل الإرسال · بلا نافذة · غير منسوب.
**Must not appear:** tags, contextScore, deal verdict, intent, interest level, outcome buttons,
campaign-level rates.
**Two data-honesty rules the row must obey:**
- `statusTimes` holds only the LATEST timestamp per status, so at most one journey can own a
  delivered/read time. Any other journey shows «لم تُسجَّل — سجل الحالات يحفظ آخر قيمة فقط لكل حالة».
- `campaign_targets` stores no per-recipient send time. «أُرسلت» = the agent turn inside the window;
  with none, «لم يُسجَّل إرسال لهذا الرقم داخل النافذة» — never the launch time relabelled.

## 3. Overlap
Full-width note inside the row: «محسوب لحملتين. نافذة «الإجازات المرضية» كانت مفتوحة عند وصول هذا
الردّ، فنُسب للاثنتين معًا. لا تُرجَّح الأحدث تلقائيًا.» Both named, neither dimmed.

## 4. Empty / unreadable / unattributed
- Empty: «صفر داخل النافذة» + «لم يقع أي حدث بين ١٤ يوليو ١٠:٤٠ و١٥ يوليو ١٠:٤٠. الصفر هنا نتيجة
  الحملة، لا نقصًا في البيانات.»
- Unreadable: «بلا نافذة», four cells `٠`, + «تعذّرت قراءة وقت إطلاق هذه الحملة. بلا وقت إطلاق لا
  حدود لنافذتها، فلا يُنسب إليها أي حدث — القيم صفر حتى يُصحَّح وقت الإطلاق.»
- Unattributed: «خارج نافذة أي حملة» + «تفاعل وقع بعد إغلاق نوافذ كل الحملات. حقيقي ومحسوب للعميل،
  ولا يُضاف إلى نتيجة أي حملة.»
- None: «لم تستهدف أي حملة هذا الرقم بعد.»

## 5. Lifetime blocks
فهم المساعد · درجة السياق · وسوم الاهتمام: `3px #C9A227` start border, `#FEFBF0` fill, ribbon
«◷ مدى الحياة — خارج النطاق المختار», line: «محسوبة على كل تاريخ العميل منذ أول رسالة، ولا يمكن
قصرها على نافذة حملة. لا تُقرأ كنتيجة للحملة المختارة أعلاه.»
سجل التفاعل stays lifetime, tints in-window events `#2F5F94` and greys the rest to `#98A2B3`.

## 6. Tokens + RTL layout
See `DESIGN.md` § `journey-scope` for the full token table.
- **1440** — ledger grid `3px 1.5fr repeat(4,minmax(72px,.8fr)) auto`, gap 12, row `13px 20px`,
  column head row visible. Scope banner one line, select 210px, pinned to the start (right) edge.
- **768** — banner wraps to two rows (text block, then select full-width). Ledger switches to the
  stacked row: column head hidden, each fact a `label ⟷ value` line separated by
  `1px dashed #F2F4F7`. Card padding stays `18px 20px`.
- **375** — same stacked row, ledger side padding `20px → 14px`, select `width:100%`, journey name
  ellipsised at one line, window bounds wrap to two. Sticky banner capped at ~112px tall.
- A11y: focus ring `2px #2E7D77` offset 2 on select + every row; rows are `<button>` with
  `aria-current`; every state chip pairs a tinted dot with an Arabic word (colour never alone);
  motion limited to a 140ms hover tint, nothing on load.

## 7. QA baseline
Compare against `docs/design-previews/customer-journey-scope/v3-ledger-scope.html` + DESIGN.md
token assertions, on `#customer/<phone>` at **375×812 · 768×1024 · 1440×900**, in four states:
scoped+replied+overlapping · scoped+empty window · unreadable launch timestamp · lifetime.
