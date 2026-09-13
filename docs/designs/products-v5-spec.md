# «المنتجات» V5 — one products section (spec, synthesized from UX · Fable · Astra)

## 0. Decisions where the voices diverged (reviewers: accept or reject each)
| # | Topic | UX | Fable | Astra | Decision |
|---|---|---|---|---|---|
| D1 | Record layout | tabs | two-column sections | one-column sections + jump links | Full page, **sections** in a fixed order; a 320px side column (readiness + related) at ledger ≥1100px, stacked under the header below that. Deep links via reserved last hash segment. |
| D2 | Knowledge approval | replace-only | replace-only | draft → review → approve/revoke with revisions | **Replace-only this release.** An upload by an authenticated admin is the approval act (as today), recorded as «اعتُمد بالرفع · <by> · <date>». Draft/approve workflow is deferred and named on screen. Reason: the founder asked for merge + add/edit + performance + skill; a revision model is a separate engine change (scope rule: enlarged scope needs an explicit yes). |
| D3 | Readiness | 4 cells incl. "agent recognises" | 4 cells incl. confirmed sector | state from approval + resolver only | **4 cells, 2 required + 2 recommended**: required ① معرفة معتمدة ② يميّزه المساعد (name in the assistant catalogue); recommended ③ ملف تعريفي ④ سعر منشور أو ملاحظة تسعير. Word: required missing → «لا يبيعه المساعد · ينقصه <first>»; only recommended missing → «يبيعه المساعد · ينقصه <first>»; all → «جاهز للمساعد». Sector confirmation is catalogue hygiene, not readiness (own metric). |
| D4 | Summary lead | achieved of target | achieved | open now | **«المحقق <year>»** with «من مستهدف …» or «بلا مستهدف سنوي»; open value is a supporting figure. (Open value already leads «فرص البيع»; this door is about product results.) |
| D5 | Delete | archive only | archive + delete when unreferenced | archive only | **Archive only** in the UI. `/admin/tags/delete` answers 409 when the name is referenced anywhere. |
| D6 | Create | drawer | drawer | full page | **Drawer** (same component as opps), atomic server create, then navigate to the record. |
| D7 | Win/loss readings | move to knowledge as chips | drop | drop from record | **Dropped** from this section. Only «اهتمام رصده المساعد» (distinct contacts, dashed `.c-read` chip) stays, as a related link. |
| D8 | Skill download | PDF row + toolbar overflow | action row while PDFs missing + PDF slot link | utility strip + PDF workflow | **Record: beside the intro-PDF slot. List: an action row inside the ledger while ≥1 product lacks a PDF (counted), otherwise a text link in the ledger footer.** Never a banner. |
| D9 | Bulk select on list | — | yes | no | **No** (eight products). |
| D10 | Rename | modal + cascade line | modal + counts + limit | + contacts JSON + aliases | Modal with computed counts; **extend the transaction to `contacts.tags[].product`**; aliases deferred — an old `#product/<old>` link shows «لا منتج بهذا الاسم» with a search of close names. |
| D11 | Agent resolver for new products | state limit | state limit | replace six-name restriction | **State the limit** («يميّزه المساعد» cell stays hatched with «يتطلب تحديث كتالوج المساعد»). Resolver rewrite is agent-code scope, deferred. |

## 1. Navigation and routes
- Door «المنتجات», tabs unchanged: «المنتجات · المستهدفات والأداء · الهيكل التنظيمي». `kb` removed from `SUBS.kmon` and `TITLES` (`check-nav-destinations` green).
- `#products` list · `#product/<name>` record · `#product/<name>/<section>` where the LAST segment ∈ {`performance`,`pricing`,`targets`,`knowledge`} scrolls to that section; the rest rejoins with «/» (names with «HIS/ERP» keep working). Create refuses a name whose last «/» segment is a reserved word.
- Redirects (history replace, no loop): `#kb` → `#products`; `#kb/<tag>` → `#product/<tag>/knowledge`; `#kb/<non-tag>` → `#products` with the «غير مطابق» row group expanded.
- List filters, sort, archived toggle and scroll survive opening a record and pressing Back.
- `smoke.py`: `#products` landmark «الكتالوج»; replace the `#kb` route with `#product/<a real tag>` landmark «جاهزية المساعد».

## 2. List `#products`
**Summary panel** (opps grammar: paper, 1px `--line`, `--r-lg`, `--s4`, no shadow, no filled-blue tiles).
- Start: «المحقق <arYear>» (12/500 muted); figure 28/600 (full SAR, `<bdi>`); sub-line «من مستهدف X ر.س · Y٪» or «بلا مستهدف سنوي» (never «٠٪» over no target). 8px bar: segment per product = won value, single blue ramp for ORDER, hatched remainder to the annual target; legend buttons filter the table (zero products muted, still operable). No bar when nothing is won and no target («لا مبيعات مربوحة بعد»).
- End: three work-owed metrics, hairline-separated, each a filter (tint + check when on): «لا يبيعها المساعد» (required readiness missing; warn glyph when >0) · «بلا سعر منشور» · «قطاع مُستنتَج».
- Summary follows search/sector/archived filters, not the metric shortcut it controls.

**Ledger panel «الكتالوج».**
- Toolbar 64px (opps rules: one row at ledger ≥1100px, filters wrap inside their own group, nothing clipped): search «ابحث باسم المنتج» · القطاع ▾ · الجاهزية ▾ · ترتيب ▾ (الاسم · المحقق · المفتوح · الجاهزية) · «مسح» when filtered · spacer · primary **«إضافة منتج»**. «عرض المؤرشفة» lives in the القطاع/الجاهزية filter group as a toggle.
- Skill action row (48px, `--accent-bar`, `--accent-deep`): shown only while ≥1 active product lacks an intro PDF: «٣ منتجات بلا ملف تعريفي — مهارة إعداد العرض تُنتجه بمساعد ذكاء اصطناعي» · «تحميل المهارة» (`<a download href="/assets/<pid>">`, filename in `<bdi>` 12 muted). Hidden when none lack a PDF → footer text link «مهارة إعداد العرض ↓». Missing `__skill__` asset → the row/link says «المهارة غير مرفوعة بعد» without a link.
- Unmatched action row (only when >0): «ملفات تحتاج ربطًا بمنتج · ٢» expands into flush rows: source name (dashed) · type (معرفة / ملف تعريفي) · filename · actions «ربط بمنتج ▾» and «إنشاء منتج بهذا الاسم». Excluded from every total.
- Table: header 40px `--surface` 12/600 muted; rows 56px, `--line-soft`, `--r-none`, hover `--accent-wash`. Columns start→end:

| col | width | content |
|---|---|---|
| المنتج | flex min 220 | name 14/600 (one line, title=full); line 2 12 muted «sector · owner»; assumed sector → dashed chip «مُستنتَج»; archived → outlined off pill «مؤرشف» |
| جاهزية المساعد | 180 | four 16×6 cells (required first; filled `--s-issued`, missing hatched `--surface-2`) + the D3 word |
| السعر المنشور | 190 | lowest active package «١٨٬٠٠٠ ر.س / سنة» 14/600 + line 2 «باقتان»; else pricing note (one line) or «لا سعر منشور» muted |
| المستهدف <year> | 120 end | full SAR or «بلا مستهدف» muted |
| المحقق | 130 end | full SAR; line 2 «Y٪ من المستهدف» or «—» |
| المفتوح | 120 end | open value (priced) + line 2 «٢ فرص · ١ بلا تسعير» |
| › | 36 | real `<button>` «فتح سجل <name>» |

- Footer: «١–٨ من ٨ منتجات» · «المحقق للمعروض X ر.س».
- States: 5 skeleton rows; empty «لم تُضف منتجات بعد» + «إضافة منتج»; filtered-empty «لا منتج يطابق التصفية» + «مسح التصفية»; failed «تعذّر تحميل المنتجات» + «أعد المحاولة» (stale rows stay under an inline warning; a failed load never renders an empty table). Every product read endpoint answers 503 when the database is unreachable (same rule as `/admin/opps`).
- Below 900px: stacked rows in the same panel (name + readiness word / price · achieved · open / ›); toolbar row 1 search + primary, row 2 a strip that scrolls inside itself.

## 3. Record `#product/<name>`
Back link «كل المنتجات ←» (restores list state). Width `--content-max`.

**Header panel**: name 22/600; line 2: sector **select** (autosave; choosing any value sets `sector_assumed=false`, the «مُستنتَج» chip goes) · owner **text with datalist** (autosave) · «آخر تحديث …». End: the single primary **«أطلق حملة بهذا المنتج»** → campaign wizard with the product preselected (sends nothing); disabled with the reason in words when required readiness is missing («يلزم ملف المعرفة أولًا»). Ghost «⋯»: «إعادة تسمية» · «أرشفة المنتج» / «استعادة». Archived → header pill «مؤرشف» + primary becomes «استعادة المنتج».

**Side column** (320, sticky, ≥1100 ledger; else directly under the header as a full-width block):
- «جاهزية المساعد»: four 44px rows, each cell + name + status + action that jumps to its section («رفع» / «عرض» / «أضف سعرًا»). ② shows «ضمن كتالوج المساعد» or «يتطلب تحديث كتالوج المساعد — لا يميّزه المساعد في المحادثات بعد» (no action). Footer word = D3.
- «المرتبط بهذا المنتج» (counted links): «الفرص المفتوحة ٢ · ٤٬٢٠٠ ر.س →» (`#opps` searched by product) · «الحملات ٣ →» (campaign list filtered; each campaign `#kmon/<id>`) · «اهتمام رصده المساعد ٢٣ →» (dashed chip; customers filtered by the reading → `#customer/<phone>`) · «الجهات المستهدفة ١٢ →» (targets filtered by tag).

**Main sections** (panels with a 48px header; order fixed; anchors = section keys):
1. **الأداء** `performance` — title suffix «من سجل الفرص». Figure «المحقق <year>» 28/600 + «من مستهدف …»; supporting «المفتوح الآن X ر.س · N فرص · M بلا تسعير», «مربوحة N · خاسرة N (<year>)». Quarter bar: 4 segments, achieved filled, target remainder hatched, «—» where no target. «أعلى الفرص المفتوحة» 3 flush rows (account · stage dot+word · value) → `#opps/<id>`; «كل فرص المنتج →». Source line: «القيمة الإجمالية للعقد — أساس المستهدف لم يُقَرّ بعد».
2. **الأسعار والباقات** `pricing` — flush table: الباقة · النطاق · المدة · السعر السنوي (end) · الحالة · actions. «+ باقة» adds an inline edit row (name*, scope, years 1–10 int, annual price ≥0 ≤2 decimals; explicit «حفظ الباقة» ghost / «إلغاء»); existing rows «تعديل» (same inline row, by id) and «تقاعد»; retired rows under «عرض المتقاعدة (N)» with «إعادة التفعيل». Note: «تعديل السعر لا يغيّر قيم الفرص المسجّلة». Field «ملاحظة التسعير» (autosave, ≤120) with helper «تُعرض حين لا توجد باقة منشورة».
3. **المستهدفات** `targets` — year switch (`arYear`, current and next). Four quarter rows: label · target field (`dir=ltr`, autosave; blank = no target, clears the row; «٠» is an explicit zero) · achieved · coverage bar (hatched, «—» with no target). Annual total «مجموع المستهدفات المدخلة» + «N أرباع بلا مستهدف».
4. **المعرفة والملفات** `knowledge` — two 64px rows:
   - «الملف التعريفي (PDF)» — «يُرسله المساعد للعميل»: filename `<bdi>`, size, date · «معاينة» · «استبدال»; empty: hatched cell + «رفع PDF» + text link «أنشئه بمهارة إعداد العرض ↓». Server: PDF only (magic bytes), ≤10 MB, product must be an active tag; a failed replace keeps the current file.
   - «ملف المعرفة» — «يقرأه المساعد ليجيب»: source filename, «اعتُمد بالرفع · <by> · <date>», «استبدال»; empty: «رفع ملف المعرفة». Upload always sends `product` before `file`; server rejects missing/unknown/archived product (400). Long-running state «جارٍ استخلاص المعرفة…»; failure keeps the current knowledge.
   - Accordion «النص المعتمد» — the markdown rendered read-only, with «يُحدَّث برفع ملف جديد — التحرير المباشر والمراجعة قبل الاعتماد في إصدار لاحق».
   - Accordion «المعرفة المدمجة» (only for the coded catalogue products) — pitch · الكفاءة · ملائم لـ · التسعير المعتمد, «مضمّنة في الشيفرة — للقراءة فقط».

**Footer**: «أُنشئ <date> · آخر تعديل <ago>».

## 4. Write model and endpoints
Autosave per field for sector, owner, pricing note, quarter targets (opps addendum v2 contract: pending «جارٍ الحفظ…» in the label row, 900ms «حُفظ ✓», failure keeps the value with «أعد المحاولة» / «تجاهل», ordered writes, invalid values blocked inline with `aria-invalid`). Explicit save for package rows, rename, create, archive, uploads.

New / changed endpoints (RFC 9457 errors, 401/403/404/409 documented; every write validates the product is an existing tag):
- **NEW `POST /admin/products`** `{name, sectorId?, owner?, pricingNote?, firstPackage?}` → 201 + `Location`; one transaction (tag + product_meta + package); 409 on existing name/reserved segment/`__` prefix.
- **NEW `PATCH /admin/products/:name`** `{sectorId|null, owner|null, pricingNote|null}` → 200 row; writes `product_meta` (upsert), sets `sector_assumed=false` when `sectorId` is sent. Registered in `check-ledger-writers`.
- **NEW `POST /admin/products/:name/archive`** `{archived:boolean}` → sets/clears `product_meta.archived_at`. Refuses (409) while any campaign for the product has queued/pending outbox sends; otherwise returns counts for the confirmation text. Archived products leave: the default list, the campaign wizard product list, the opps product select, and `agent.refreshKb()` (the assistant stops using that product's knowledge and PDF).
- **NEW `PATCH /admin/packages/:id`** `{name, listPrice, years, scope}` → identity-preserving edit; 409 on duplicate name within the product. Restore = existing retire endpoint with `{retire:false}`.
- **CHANGED `POST /admin/sales/targets`** — `amount:null` deletes the (product, year, quarter) row.
- **CHANGED `POST /admin/kb/upload`** — product required and must be an active tag (the model never names a product from any UI).
- **CHANGED `POST /admin/product-asset/upload`** — PDF magic bytes + ≤10 MB for products; the `__skill__` branch unchanged.
- **CHANGED `POST /admin/tags/rename`** — also rewrites `contacts.tags[].product`; returns affected counts; **NEW `GET /admin/products/:name/impact`** returns those counts for the modal before commit.
- **CHANGED `POST /admin/tags/delete`** — 409 when the name is referenced by any product table.
- **NEW `POST /admin/products/reconcile`** `{from, to, kind:"kb"|"asset"}` — moves an off-registry kb doc/asset onto an existing tag; 409 if the target already has one.
- **CHANGED `GET /admin/products`** — adds `archived`, `hasKb`, `kbSource`, `kbUpdatedAt`, `kbBy`, `hasAsset`, `assetFilename`, `inAgentCatalogue`, and a separate `unmatched[]`; 503 when the DB is unreachable. Reserved `__*` names excluded everywhere.
- Readiness, coverage, "first gap" word and price-summary rules live in a pure, unit-tested `src/product-domain.ts`.

Rename modal: new name field; computed line «سيُغيَّر الاسم في: ٣ فرص · حملتان · ملف المعرفة · الملف التعريفي · ١٢ جهة مستهدفة · ٢٣ قراءة للمساعد»; 409 inline «الاسم مستخدم لمنتج آخر»; success rewrites the route, toast.

Archive: hold-to-confirm (§3.13, keyboard two-step) with the counts text «٢ فرص مفتوحة تبقى كما هي · المساعد يتوقف عن استخدام معرفته»; restore is one click.

## 5. Connected (observable)
Opps drawer product name → record · wizard product chip → record · home exec band product → record · record primary → wizard prefilled · open value → `#opps` searched by the product · campaigns link → filtered campaigns → `#kmon/<id>` · interest link → customers filtered → `#customer/<phone>` · targeted entities → `#targets` filtered by tag · quarter targets are the same rows `#perf` edits · a product created here immediately appears in the opps product select and the wizard · every mutation updates the shared stores (catalogue, record, wizard registry, home band) without a reload.

## 6. Acceptance checklist (pass/fail)
1. Six rail doors; `kb` gone from الحملات; `#kb`, `#kb/<tag>`, `#kb/<non-tag>` and names with «/» resolve as §1 with no loop.
2. The list is built from `tags` only; unmatched kb docs/assets appear in the «غير مطابق» group with working «ربط بمنتج» and «إنشاء منتج بهذا الاسم»; `__*` never appears.
3. One leading 28px figure; no filled-blue tiles; three work-owed metrics filter; «بلا مستهدف» never shows «٠٪».
4. Flush 56px rows, dividers, hover wash; one blue primary per state; no black button.
5. Readiness = four cells (colour + hatch) + a word that distinguishes «لا يبيعه المساعد» from «يبيعه المساعد · ينقصه …».
6. Create drawer writes tag + meta + optional package atomically; collision inline; success opens the record; the new product appears in the opps select and the wizard without reload.
7. Sector, owner, pricing note and quarter targets autosave with pending/saved/failed states; failure keeps the value; clearing a target removes it.
8. Packages: add, edit by id, retire, restore; editing never changes recorded opportunity values.
9. Rename shows counts before commit, cascades including contact readings, collision changes nothing, route rewrites.
10. Archive is a hold, refused while sends are queued, removes the product from list default, wizard, opps select and the assistant's knowledge; restore brings everything back.
11. Knowledge and PDF uploads are scoped; server rejects unknown/archived products and non-PDF/oversized files; failed replace keeps the current file.
12. No agent-readings scoreboard anywhere in the section; performance is titled «من سجل الفرص» and reconciles to the opportunities ledger.
13. The skill download works from the record PDF slot and from the list (action row while PDFs are missing, footer link otherwise); missing skill is stated.
14. Every related link carries a count and lands on the correctly filtered destination.
15. Loading, empty, filtered-empty, failed (503) and unknown-product states are distinct and worded; stale data survives a failed refresh.
16. Focus management: drawer/modal trap and return focus; `<label for>` on every field; `:focus-visible` rings ≥3:1; keyboard hold two-step.
17. Arabic-Indic digits, counted nouns, `arYear`, `<bdi>` on Latin/filenames; no page overflow at 1440/1280/390; long names don't change row height.
18. `npm run check` green (nav, rename cascade, ledger writers, catalogue, productlock, crm literals/parse, numerals, design) with new unit tests for `product-domain.ts`; production smoke green with updated landmarks; home exec band unchanged.
19. NO WhatsApp send is possible from any new control; campaign launch only opens the wizard.
20. `#perf` target edits and the record's quarter targets show the same values.

## Addendum v2 — resolving spec review round 1 (Astra + Fable). Where this conflicts with §0–§6, THIS wins.

### A. Knowledge approval (Astra D2 REJECT, MUST-FIX 1; Fable §2.3) — minimal preview → approve
- Migration: `product_kb` gains `draft_md TEXT, draft_source TEXT, draft_by TEXT, draft_at BIGINT, approved_by TEXT, approved_at BIGINT`.
- `POST /admin/kb/upload` (product REQUIRED via multipart field before file OR `?product=`; must be an active tag) writes ONLY the draft columns; `md` (what the assistant reads) is untouched. No product row yet → a row with `md=''` and the draft.
- **NEW `POST /admin/products/:name/knowledge/approve` `{draftAt}`** — atomic: only if `draft_at` still equals the reviewed value (else 409 «تغيّرت المسودة منذ فتحها»): `md=draft_md, source_filename=draft_source, approved_by=adminName, approved_at=now`, clear draft columns, then `agent.refreshKb()`.
- **NEW `DELETE /admin/products/:name/knowledge/draft`** — discards the draft; approved knowledge untouched.
- UI (record §3.4 «ملف المعرفة»): approved state «اعتُمدت · <by> · <date>»; a pending draft shows a draft block: source filename · «رُفعت · <by> · <date>» · change summary «+N سطرًا · −M سطرًا» against the approved text · the draft rendered read-only · primary «اعتماد المعرفة» (demotes the header primary while visible) · ghost «تجاهل المسودة». Extraction in progress/failed states as before; failure keeps any existing draft and approved text.
- **Legacy rows** (`md` non-empty, `approved_at` NULL): remain in use by the assistant exactly as today (they were already live; removing them would change selling behaviour without a human act), labelled «مستخدمة قبل تسجيل الاعتماد — لم يُسجَّل من اعتمدها» with ghost «اعتماد النص الحالي» which records `approved_by/at` without changing content. No provenance is manufactured.
- Knowledge file types/limits (separate from PDF assets): `.pdf .docx .pptx .xlsx .md .txt`, ≤15 MB. Intro PDF: PDF magic bytes, ≤10 MB.
- Inline text editing and multi-revision history remain deferred and are named on screen.

### B. Runtime eligibility — one rule (Astra D3 REJECT, MUST-FIX 2; Fable §2.7, M5)
- Pure `isRuntimeEligible(p)` in `src/product-domain.ts`: `tagExists && !archived && (hasApprovedOrLegacyMd || isEmbeddedCatalogueProduct)`. `isEmbeddedCatalogueProduct` = name ∈ `SERVICE_CATALOGUE` (its pitch/FAQ live in `agent.ts PRODUCTS`).
- `agent.refreshKb()` loads hub md and assets through DB reads that JOIN `tags` and exclude `product_meta.archived_at IS NOT NULL`, exclude `__*`, and never read `draft_md`. The assistant exports `runtimeKnowledgeProducts()` (names currently in `hubKb`) and `/admin/products` reports `inAssistantKnowledge` from THAT list — enforced truth, not a re-derivation.
- Embedded six products cannot be archived or renamed (see D). So archive only affects products whose knowledge reaches the assistant solely through `hubKb`/assets — both filtered — which makes "the assistant stops using it" true for every archivable product.
- Readiness cells (order): ① معرفة المساعد (approved | legacy-in-use | embedded only | draft pending | none) ② ملف تعريفي ③ سعر منشور أو ملاحظة تسعير ④ يميّزه المساعد في المحادثة (catalogue lock). Word, derived from runtime eligibility first:
  - not eligible → «لا يبيعه المساعد · <reason>»: «بلا معرفة معتمدة» / «مسودة بانتظار الاعتماد» / «مؤرشف»;
  - eligible, gaps → «يبيعه المساعد · ينقصه <first of ② ③ ④ or "ملف المعرفة" for embedded-only>»;
  - eligible, no gaps → «جاهز للمساعد»;
  - products read failed → «تعذّر التحقق» (never a ready state).
- **Wizard and record agree**: `kbRegistry()`/`wizProducts()` are rewritten to read the catalogue (active tags) with status overlaid; step 1 shows non-eligible products hatched with the same reason and refuses «التالي» for them; the record primary «أطلق حملة بهذا المنتج» is disabled with the same reason. The server `POST /admin/campaign/launch` rejects a product that is archived or unknown (400) — a UI-only guard is not enough.
- Server-side archive enforcement on NEW selling writes: `POST /admin/opps` (new lines) and `POST /admin/campaign/launch` reject archived products (400 `archived_product`); PATCH of existing opp lines stays allowed.

### C. Archive without a queue (Fable §2.1, M1; Astra MUST-FIX 5)
- There is no outbox or campaign status (sends are synchronous inside launch). So archive is never "refused while queued". **NEW `GET /admin/products/:name/impact`** returns counts BEFORE confirmation: open opp lines, campaigns, targeted entities, interest readings, and `embedded` flag. The hold text uses them. `POST /admin/products/:name/archive {archived}` re-reads counts and returns them; restore is one click.
- Embedded catalogue products: «أرشفة» is not offered; ⋯ shows it disabled with «مضمَّن في كتالوج المساعد — الأرشفة تتطلب تحديث الكتالوج».

### D. Rename integrity (Astra D10 REJECT, MUST-FIX 3; Fable D10)
- Rename is **blocked for the embedded catalogue products** (UI disabled with the reason; server 409 `embedded_product`). Their names are coupled to `agent.ts PRODUCTS`, `SERVICE_CATALOGUE`, productlock patterns and boot seeds; a coordinated migration is a later slice.
- For other products: the existing transactional cascade (ten tables incl. `interest_tags`, `entities.product_tags`, deferred package FK) is kept; in the same request, after commit, the in-memory tracker contacts' `tags[].product` is rewritten and `agent.refreshKb()` runs. The modal's «قراءة للمساعد» count comes from `interest_tags`.
- **Boot seeding of tags from `product_kb` names is removed** (`index.ts` seed keeps `SERVICE_CATALOGUE` only), so neither a rename nor an unmatched upload can recreate a product at restart. Acceptance adds «rename → restart → old name absent everywhere».
- Aliases for old URLs stay deferred; an unknown `#product/<name>` shows «لا منتج بهذا الاسم» + a list of names containing the typed words.

### E. Identity and routing (Astra MUST-FIX 7)
- Pure `normalizeProductName()` in `product-domain.ts` (collapse whitespace, trim, ≤60, not starting `__`, no `#`, `?`, `%`, last `/`-segment not in {performance, pricing, targets, knowledge}) used by `POST /admin/products`, `POST /admin/tags`, and rename; 400 with the field and reason. Production names were checked: none violate it.
- Links are built as `#product/` + `encodeURIComponent(name)` [+ `/` + section]. Parser: split the raw hash on `/`; if the last raw segment is a reserved word it is the section; the remainder is joined with `/` and `decodeURIComponent`-ed. Legacy raw-slash links («HIS/ERP») still resolve.

### F. Reconciliation (Astra MUST-FIX 6)
- `POST /admin/products/reconcile {from, to, kind}`: `to` must be an active non-reserved tag; atomic move of the kb row (md, draft, provenance preserved) or asset row; 409 if `to` already has that kind; `agent.refreshKb()` after.
- «إنشاء منتج بهذا الاسم» = `POST /admin/products {name: from}`; if both a kb doc and an asset carry that name, both become matched by the same create; 409 when the name already exists (then the row offers «ربط بمنتج» only). Retry is idempotent.

### G. Performance contract (Astra MUST-FIX 4; Fable M2)
- «المفتوح الآن» = UNWEIGHTED sum over currently open lines of the product, all periods, priced lines only, value = price × qty × years × (1 − discount); plus open line count and unpriced line count. New SQL next to `salesPerformance`; the home band and #perf keep their weighted figure and label it «المرجَّح» — no screen in this section shows a weighted figure.
- «المحقق <year>» = sum of currently-won lines whose LATEST transition into won falls in the year (existing `track_stage_events` logic). Quarter achieved uses the same rule per quarter.
- «مربوحة N» / «خاسرة N» = counts of LINES whose latest transition into won/lost falls in the year.
- Coverage % = achieved ÷ target only when target > 0; otherwise «—». Annual target = sum of entered quarter targets; when 1–3 quarters are missing the figure reads «مجموع ٣ أرباع مدخلة · ربع بلا مستهدف».
- Money is integer SAR everywhere (`list_price`, `targets.amount` are BIGINT): price/target fields accept integers only.

### H. Exact related-link populations (Fable §2.5; Astra MUST-FIX 4)
Each link sets a global exact filter BEFORE the hash change (the `launchWithProduct` pattern) and the destination shows a removable chip «المنتج: <name> ×»:
- Opportunities: NEW `opProd` exact product filter in opps-crm (+ `opShort="open"` for the open link); chip in the toolbar.
- Campaigns: NEW `campProd` exact filter in the campaigns list (`campaigns.product === name`).
- Interested contacts: existing `cusTagF` (exact `contactTagged`).
- Targeted entities: existing `tgtProd`.
- Counts on the record are computed with the same predicates.

### I. Targets clear confirmation (Astra MUST-FIX 5)
Emptying a quarter field that has a saved target does not send; it shows inline «إزالة مستهدف الربع ٣؟ [إزالة] [تراجع]»; «تراجع» restores the saved value; «إزالة» sends `amount:null`. A never-set field left empty sends nothing.

### J. Delete guard (Astra MUST-FIX 5)
`POST /admin/tags/delete` → 409 when the name appears in any `PRODUCT_NAME_TABLES` table, `entities.product_tags`, or `interest_tags`; the targets tag panel shows the reason and points to archive.

### K. Responsive feasibility (Astra MUST-FIX 8) — container widths of the ledger panel
- ≥1100: all columns — المنتج flex(min 200) · الجاهزية 168 · السعر 168 · المستهدف 112 · المحقق 120 · المفتوح 120 · › 32, column-gap 16 (fits 1138).
- 900–1099: المستهدف column folds into المحقق line 2 («من ٣٤٬٠٠٠ · ١٢٪»); الجاهزية shows cells + short word; full word in the cell `title` and on the record.
- <900: stacked rows (name + readiness word / price · achieved · open / ›).
- Record <1100: side column becomes a full-width block under the header. Packages and quarter targets under 560px become labelled stacked groups (label above field), one per row; the inline package editor is a vertical form.

### L. Gates and literals (Fable M3, M4, M6, M7, M8)
- `dashboard.ts` anchored edits: delete `["kb", "معرفة الخدمة"], ` from `SUBS.kmon` (the line `["kb", "معرفة الخدمة"], ["partners", "شركاء المبيعات"]],` becomes `["partners", "شركاء المبيعات"]],`) and delete the `TITLES` line `kb: ["معرفة الخدمة لمساعد المبيعات", "المعرفة المعتمدة التي يستند إليها مساعد المبيعات في واتساب"],`.
- `smoke.py`: delete `("#kb", "منها بمعرفة معتمدة"),`; add `("#product/الإجازات المرضية", "جاهزية المساعد"),`.
- `check-ledger-writers.mjs` `MUST_HAVE_WRITERS` gains `product_kb` and `product_assets`.
- Every products read (`/admin/products`, `/admin/products/:name/impact`, `/admin/kb`, `/admin/product-assets`) calls `db.canRead()` first and answers 503 `db_unavailable` when unreachable; the UI shows the failed state.
- `#kb/<non-tag>` redirect sets global `pcUnmatchedOpen = true` before `history.replaceState` to `#products`.
- `listAssets()` adds `octet_length(bytes) AS size` and `updated_at`.

### Acceptance additions
21. Upload creates a draft that the assistant does not read; «اعتماد المعرفة» publishes exactly the reviewed draft (stale draftAt → 409); legacy text stays in use and is labelled honestly.
22. Readiness word follows runtime eligibility; wizard, record primary and `POST /admin/campaign/launch` agree; archived product rejected server-side for new opps and launches.
23. Embedded catalogue products cannot be renamed or archived (UI reason + server 409).
24. Rename → restart → the old name appears in no list, selector or assistant prompt.
25. Every related link lands on the exact population with a removable product chip; record counts equal destination counts.
26. Clearing a saved target needs inline confirmation; «تراجع» restores it.

## Addendum v3 — resolving spec review round 2. Where this conflicts with earlier text, THIS wins.

### A′. No unapproved text reaches the assistant (Astra D2/MF1; Fable #2)
- **Legacy rows are NOT exempt.** A `product_kb` row is used by the assistant only when `approved_at IS NOT NULL AND md <> ''`. On deploy, legacy rows (`approved_at IS NULL`) stop reaching the assistant until a human approves them. The record shows «بانتظار اعتماد النص الحالي — المساعد لا يستخدمه» with primary «اعتماد النص الحالي».
- «اعتماد النص الحالي» sends `{contentHash}` = SHA-256 of the exact `md` the reviewer was shown (the page renders it before the button is enabled); the server recomputes and approves only on equality (else 409 «تغيّر النص منذ فتحه»).
- «اعتماد المعرفة» for a draft likewise sends `{draftHash}` = SHA-256 of the shown `draft_md` (replaces `draftAt` from §A).
- **Embedded catalogue content** (`agent.ts PRODUCTS` for the six `SERVICE_CATALOGUE` names) is the approved baseline by code review: it ships only through a reviewed commit and a deploy. The record labels it «معرفة مدمجة معتمدة بمراجعة الشيفرة — للقراءة فقط».
- The founder is told in the release note which products lose assistant knowledge until he approves (production today: every non-embedded product with a hub document).

### B′. One eligibility rule, enforced at every runtime path (Astra D3/MF2; Fable #3)
`isRuntimeEligible(p) = tagExists && !archived && (hasApprovedMd || isEmbeddedCatalogueProduct)`, pure, unit-tested, and used by:
1. **Prompt knowledge** — `agent.refreshKb()` loads hub md only for rows with `approved_at IS NOT NULL AND md <> ''` whose product is an active (non-archived) tag.
2. **Composition** — `composeOpener()` reads the same filtered `hubKb`; for a non-eligible product it throws `not_eligible` and `POST /admin/compose` answers 400.
3. **Asset selection** — `refreshKb()` loads assets only for runtime-eligible products; `send_asset` resolves by exact canonical name (no substring match).
4. **Campaign launch** — when a `product` is supplied, `POST /admin/campaign/launch` answers 400 `product_not_eligible` unless eligible (unknown, archived, or no approved/embedded knowledge); a launch without a product is unchanged.
5. **New opportunities** — `POST /admin/opps` rejects archived products for new lines (not eligibility: a rep may record a deal for a product the assistant cannot sell).
6. **Refresh points** — `refreshKb()` runs after: approve, discard (no-op for runtime but keeps state consistent), archive/restore, rename, reconcile, and `POST /admin/products` (a create that matches existing files).
The UI's readiness word, the wizard's step-1 gate and the record primary read `inAssistantKnowledge`/`eligible` from `/admin/products`, which the server computes from the agent's live `hubKb` plus the embedded list.

### G′. Counts (Astra MF4)
«مربوحة N» / «خاسرة N» = lines whose CURRENT stage is won/lost AND whose latest transition into that stage falls in the selected year. Quarter achieved uses the won predicate per quarter.

### H′. Links reproduce their populations (Astra MF4; Fable #1)
Each link handler resets the destination's filters, then sets the exact product filter, then changes the hash:
- Opportunities: `opQ=""; opStg="all"; opSrc="all"; opOwn="all"; opShort=""; opMode="list"; opProd=<name>`; the open link also sets `opShort="open"`. Opps has no period filter, so «المفتوح الآن» is all periods by construction.
- Campaigns: `campQ=""; campTab="all"; campProd=<name>` (campaigns whose `product === name`, real and test both shown because the count includes both; the chip says «كل الحملات · المنتج: <name>»).
- Interested contacts: NEW `cusProdF=<name>` — contacts with any `tags[].product === name` (assistant readings), distinct by phone; resets `cusQ`, `cusTagF` and other customer filters. (`contactTagged`/`cusTagF` filter operator targeting labels and are NOT used here.)
- Targeted entities: resets target filters, sets `tgtProd=<name>`.
- Every destination shows a removable chip «المنتج: <name> ×»; removing it clears only `…Prod`.
- The record's counts use exactly these predicates.

### A″. Discard draft is confirmed (Astra MF5)
«تجاهل المسودة» is hold-to-confirm (§3.13; keyboard arm/commit; reduced-motion two-step). Cancelling or releasing early keeps the draft. The DELETE is sent only on commit.

### Acceptance additions
27. A legacy knowledge row is not in the assistant prompt until «اعتماد النص الحالي» succeeds with the matching hash; a stale hash returns 409 and changes nothing.
28. `composeOpener`, `send_asset` and `/admin/campaign/launch` (with product) all refuse a non-eligible product; the same product shows «لا يبيعه المساعد · <reason>» on the list, the record and the wizard.
29. Each related link lands on a population whose count equals the record's count even when the destination previously had other filters applied.
30. Discarding a draft requires a completed hold; releasing early keeps it.
