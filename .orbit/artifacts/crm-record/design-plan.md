# Design plan — the enrichable client record (`#customer/<phone>`)

Cycle `crm-record` · task #15 · `[designer]` · gate **B** (style approved).
Prototypes: `v1-dot-rail` · `v2-stripe-rows` · **`v3-signed-fields` ← chosen**
(`.orbit/design/previews/crm-record/`). Contract: `design/approved.json`, tokens: `DESIGN.md`.
Read: an operator's console for one Arabic sorter working 18,000 clinics. Dials: variance 3,
motion 2, density 8. System: none — bespoke Massar language; HubSpot's region contract borrowed as
IA only. Light mode only.

## 1 · Region map (RTL, desktop)

Full width, in order: back link → identity card → **status strip** (§2). Then the body:

```
.crec { display:grid; grid-template-columns:372px minmax(0,1fr); gap:18px; align-items:start; }
```

DOM order = enrichment panel, then `.main`. In RTL the 372px track lands on the **right** — the
start side, mirroring HubSpot's left rail. `.main` keeps the existing
`repeat(auto-fit,minmax(330px,1fr)); gap:16px` and holds فهم المساعد then سجل التفاعل.

**No third rail.** HubSpot's right rail holds Associations and Attachments; Massar has no deals,
companies or tickets, so it would hold nothing. Market §5 says this outright.

- **≤900px** (reuse the existing breakpoint, where `aside` already hides): `grid-template-columns:1fr`.
  Stack: identity → status → **ملف العميل** → فهم المساعد → سجل التفاعل. Properties beat the AI card
  deliberately.
- **≤600px**: page padding 14px, card padding 16px, status strip `.z` becomes `display:block`
  (three zones stack), pencils force `opacity:1`, confirm pills go full-width in a 2-col grid.

## 2 · The status strip

One tinted box, `border-inline-start:3px solid <outcome ink>` on the right. Three zones in a
`flex; gap:26px; flex-wrap:wrap`, ranked: **fact, fact, reading**.

1. **الفرز** — fact. `17px/700` in the outcome ink. Below it the quote: «لأنه قال: «…»». Unknown →
   «لم يُفرز بعد» in `#98A2B3`, strip falls to `#F9FAFB` with an `#EAECF0` border. No colour claim
   without an outcome.
2. **الاهتمام** — one solid chip per product from `c.tags` (fact). No tag but `ins.intent` exists →
   the dashed `c-read` chip with the «قراءة» prefix, already in the CSS. None → «لم يُسجَّل اهتمام بعد.»
   Never averaged.
3. **المرحلة** — reading, always. Hollow `.pm-a` mark + `12.5px/600 #475467`:
   «قراءة المساعد: عرض الحل», then the quote, or «بلا اقتباس يسندها بعد.» + «حدّث القراءة».
   **The «٣ من ٦» ordinal is deleted** — it is the banned rail in text form. No chip here: a chip
   would make the guess a peer of the two facts.

Under a hairline: «سجّل النتيجة الفعلية:» plus the four outcome buttons and «فتح المحادثة», moved
inside the strip so the fact-writing controls sit with the fact they write.

One-second rule: **filled/solid = fact, hollow-dashed and lighter = reading, dashed grey = missing.**
Texture, not hue, because hue is already spent on interest level.

## 3 · The enrichment panel — «ملف العميل»

Header: title + `c-warn` chip «ناقص ٢» (a count, via `fmtN()`, never a score). Sub:
«ما تكتبه هنا لا يستطيع المساعد تغييره.» Then a one-line legend of the four marks. All six fields in
**one panel** — market §5's gaps-in-one-panel rule, honored; no asterisks anywhere else.

Row: `[mark] · label / value / signature`, pencil pinned `inset-inline-end:0`, `opacity:0` until
hover/focus (always visible on touch). Edit is **per field**: pencil → `.inp` inline + «حفظ»/«إلغاء».
Enter saves, Esc cancels. Never Salesforce's whole-form mode.

| # | field | fact | reading | missing |
|---|---|---|---|---|
|1|**صاحب القرار**|«د. سارة العتيبي · مديرة العيادة» + «سجّلها عبدالعزيز · ١٢ أغسطس»|reading + quote + confirm bar|«لم يُسجَّل صاحب القرار بعد.» · «أضِف الاسم والصفة»|
|2|**المنشأة**|human overwrite allowed|`.pm-i` + «من ملف الاستيراد · ٣ أغسطس · يمكنك تصحيحه»|«غير مستورد في القوائم.» · «→ استورد القائمة»|
|3|**الاهتمام**|solid chips|dashed `c-read` chips + quote + confirm bar|«لم يُسجَّل اهتمام بعد.» · «سجّل الاهتمام»|
|4|**الخطوة التالية**|text + date|`.pm-h` «قال العميل: «بكرة الصبح»» *above* `.pm-a` «قراءتنا: الأحد ١٠ صباحًا · لم تُؤكَّد بعد»|«لا خطوة تالية محددة.» · «حدّد الخطوة»|
|5|**ملاحظة**|textarea, label suffix «· بخط الفريق فقط»|never|«لا ملاحظات. اكتب ما لا يظهر في المحادثة.»|
|6|**سبب الاستبعاد**|enum + free text|reading + confirm bar|«لم يُستبعد.» · «استبعد هذا العميل…»|

Field 4 carries two marks on purpose: the customer's sentence is a fact, our parse of it is not.

**«أكّد»** — one tap, teal pill, no dialog. PATCH, then the row flips to fact, the signature reads
«أكّدها عبدالعزيز · ١٢ أغسطس», and a 140ms `#ECFDF3` tint fades (skipped under reduced motion).
**«صحّح»** — ghost pill, opens the same editor prefilled with the reading, text selected, so
correcting costs one keystroke. Failure: editor stays open, «لم يُحفظ. أعد المحاولة.» in `#B42318`;
over-limit «النص أطول من المسموح (١٢٠ حرفًا).»; no `DATABASE_URL` → pencils disabled with
«التعديل معطّل: قاعدة البيانات غير متصلة.» A contested reading renders as a passive line:
«قراءة مختلفة من المساعد: «…»» + «اعتمدها» / «تجاهل». Field 6 is shown but **not counted** as a gap.

## 4 · The provenance language

Placement (RTL decision): an 8×8 box in a fixed column at the **right edge**, all six on one vertical
axis, so provenance is scannable before any label is read. Exact tokens in `DESIGN.md`:
`.pm-h` filled square `#1F7A73` · `.pm-a` hollow `1.5px dashed` circle `#B54708` · `.pm-i` filled
square `#2F5F94` at `.55` · `.pm-m` dashed outline square `#D0D5DD`. Reading rows take `#FFFDF7`.

Shape carries it, colour reinforces it, and **the mark never appears without its word** — so one
field lifted out of context still says «سجّلها عبدالعزيز» or «قراءة المساعد». We copy Attio's
placement and hover-reasoning, not its confidence grading: a confidence number is an invented number.
Support is shown **inline, not on hover** — quote at `11.5px #667085`, or, with none,
«بلا اقتباس يسندها بعد.» + «حدّث القراءة».

## 5 · Deleted

- `vSalesPath()` call (2104) — the 6-node rail, banned; paints five unreached stages and a ✓ nobody verified.
- `const missing` (1952) — dead code, and its source `contextScore` is a 0–100 invented score measuring platform activity, not knowledge gaps. **The panel replaces it** (AC-13). Stop reading `d.context`.
- «٣ من ٦» stage ordinal (2084).
- The 2×2 `mcards` grid (2118–2122): «القناة المفضّلة: واتساب» is constant on a WhatsApp-only platform; «نية الشراء» and «حكم الصفقة» each already render twice more on this page.
- `toneBadge(im…)` in the AI header (2108) and the `product_interest` badge row (2123) — third and fourth renderings of interest.
- Rename the AI box (2132) to «اقتراح المساعد للخطوة التالية»; two things named الخطوة التالية with different provenance is the confusion this cycle exists to kill.
- Show `ins.evidence` only when it differs from `c.outcomeEvidence`.

Preserved: `.card`/`.chip`/`c-*`/`.c-read`/`.rd`, `attrChips`, the timeline, the outcome buttons, the campaign-source sentence, `fmtN`/`fmtD`/`fmtT` (Arabic-Indic).

## 6 · Acceptance checks (screenshot-verifiable)

1. **1440** — exactly two columns; the panel is the **rightmost** block, `372px ±2`, gap `18px`; the six `.pm` marks share one x-axis within ±1px; no horizontal scroll.
2. **900** — one column, order identity → status → ملف العميل → فهم المساعد → سجل التفاعل; the stage name appears exactly **once** on the page and no stage rail exists anywhere.
3. **390** — every row stacks label/value/signature with no Arabic truncation; `+966…` renders LTR-isolated with `+` leftmost and no bracket flipping; pencil/أكّد/صحّح hit areas ≥40px; no horizontal scroll.
