# Client A's standalone prototype → Massar parity

Source: `~/Downloads/مسار - نظام إدارة المبيعات (نسخة مستقلة) (1).html` (969 KB, walked screen by screen
on 2026-09-16; screenshots and per-screen text dumps in the session scratchpad).

The founder's instruction: **every single thing in the prototype must exist in Massar**, with the same or a
better experience — "where to find users, how to onboard a new customer, how to view users, opportunities,
and the home dashboard indicators". Massar's own rules still win where they conflict: RTL Arabic, the
`DESIGN.md` tokens and the `#2563EB` accent (the prototype's navy/green palette is NOT adopted), western
numerals, and no figure on screen the ledger cannot prove.

## The prototype's information architecture

Five groups, twelve doors, one persistent search field, and a role switch on the home screen
(«عرض تنفيذي» / «مدير منتج»).

| Group | Doors |
|---|---|
| نظرة عامة | الرئيسية |
| دورة البيع | العملاء · فرص البيع · لوحة المتابعة |
| التسويق | إنشاء حملة · متابعة الحملات · معرفة المنتج · شركاء المبيعات |
| التخطيط والأداء | المنتجات · المستهدفات · التقارير |
| المنشأة | الهيكل التنظيمي |

## Screen by screen

### 1. الرئيسية — «لوحة المدير التنفيذي»
Bands, in order: four KPI tiles (المستهدف الإجمالي · المحقق الإجمالي · نسبة الإنجاز · الفرص المفتوحة with its
value) → **صحة خط البيع** (four states, each a count AND a value: على المسار · متأخرة · بانتظار الدعم ·
مرفوضة, each with a one-line definition) → **ملخص أداء شركاء المبيعات** (donut + إجمالي المستهدف الأسبوعي ·
تم التواصل · العملاء المهتمون · غير مهتمين · لم يردوا, each with its share) → **القطاعات** (a card per sector:
achieved/target, a bar, product count, «تعمّق ←») → **المنتجات حسب الإنجاز** (bar per product with its
department) → **الإنجاز الربعي الإجمالي** (four quarters, achieved/target).

### 2. العملاء
Tabs «قائمة العملاء» / «مؤشرات استخدام العملاء». Filters: search, الكل / معتمدون / مقترحون, with a
«2 بانتظار الاعتماد» badge. Two entry points side by side: **«+ إضافة عميل جديد»** and **«استيراد مجموعة
عملاء من ملف»**. Table columns: العميل (with an importance pill under the name) · المدينة · القطاع ·
الموظف المسؤول · مصدر الإضافة · الحالة (inline اعتماد / رفض for proposed rows) · عدد الفرص · قيمة الفرص.

**Add-customer sheet**: «يُضاف العميل بحالة «مقترح» بانتظار اعتماد فريق المبيعات» — بيانات المنشأة (اسم *,
المدينة * as a select, القطاع as a select, درجة الأهمية, الموظف المسؤول) then جهات الاتصال (repeatable:
الاسم *, المنصب, الهاتف, البريد, one marked رئيسية).

### 3. شاشة العميل 360°
Header: name, approval pill, importance, sector, city, who added it. Then **مدير الحساب**, **مدراء المنتجات
المعنيون بالحساب** (person → product), **جهات الاتصال**, **المنتجات المستهدفة** (product → status:
فرصة قائمة / تم البيع), **فرص العميل** (each with expected close date, stage and value), **سجل الأنشطة**.

### 4. فرص البيع
One card per ACCOUNT, not per line: «4 منتجات · <owner>», state chips (قائمة · متوقّف · دعم), the split
«قائمة 2 · ربح 1 · خسارة 1», total value, then the product lines each with stage and value.

### 5. تفاصيل فرصة البيع
Account-level total, the product lines, a **selected product** with: a stall warning naming the stage, the days
in it and the limit; a five-step progress bar with نسبة الإنجاز; and **نتائج المراحل** — per stage: outcome,
date, السبب and الإجراء, with «لم تُسجَّل» for stages not reached.

### 6. لوحة المتابعة
Drag-and-drop kanban over the stages, filtered by كل المنتجات / كل الموظفين / **ردّة الفعل** (14 reactions).
Each card: account, product, value, date, the next action, and a reaction pill (يحتاج إجراء · مقبول · لم تُسجّل).

### 7. إنشاء حملة
Step 1 picks the product **by the assistant's knowledge score** (92% جاهز للبيع · 66% جاهز بتحفّظ ·
48% غير جاهز). Then the audience by city/sector/priority chips, a segment approval, and start now or schedule.

### 8. متابعة الحملات
حالة الحملات (نشطة · مجدولة · تحتاج تدخل · مكتملة · مسودة with shares) and **قراءة المساعد الذكي**:
إجمالي الفرص, أفضل حملة جارية, أعلى شريحة تفاعلًا, أعلى منتج اهتمامًا, حملة تحتاج متابعة.

### 9. معرفة المنتج
A readiness percentage with «3 من 10 أقسام مكتملة · 38 من 59 عنصر معرفة», a product picker, **ten** named
sections, «اختبار المساعد» and «أكمل التدريب».

### 10. شركاء المبيعات
Week navigation, product filter, the overall summary and a table per partner. (Massar already ships this.)

### 11. المنتجات — «لوحة مدير المنتج»
A product switcher, then annual target / achieved / نسبة الإنجاز / open opportunities, and quarterly
achievement against target.

### 12. المستهدفات
Annual target per product **and its quarterly split**, grouped by sector, with إجمالي المستهدف · إجمالي المحقق ·
المتبقّي · نسبة الإنجاز on top.

### 13. التقارير
**Product acceptance**: every product classified مقبولة — بيعت جيدًا / متعثّرة / غير مقبولة / لم تُبع بعد,
with مبيعة · خاسرة · مفتوحة · نسبة الإنجاز and **أبرز سبب عدم القبول**.

### 14. الهيكل التنظيمي
Four tiles (القطاعات · الإدارات · مدراء المنتجات · موظفو المبيعات) and three tabs (القطاعات · الإدارات ·
الموظفون), each row editable, sector rows carrying their head and email.

## Status — 2026-09-16

| Prototype screen | Massar today | State |
|---|---|---|
| الرئيسية (4 KPIs · صحة خط البيع · partners week · sectors · products · quarters) | `#home` — all six bands, and each health state OPENS its deals | **done** |
| العملاء (list, tabs, add, import) | `#accounts` is the door's landing route, named «العملاء» | **done** |
| شاشة العميل 360° | `#account/<id>` — owner, **product managers**, contacts, targeted products, opportunities with expected close, activities, campaigns, indicators, partner contact | **done** |
| فرص البيع (per-account cards) | `#opps` — line rows with the account's other lines in the drawer | **partial** (grouping by account not built) |
| تفاصيل فرصة البيع (نتائج المراحل · stall · progress) | the drawer's **«نتائج المراحل»** + «نسبة الإنجاز في الدورة» + the stall warning that was already there | **done** |
| لوحة المتابعة (drag kanban) | `#board`, its own tab; the event ledger renamed «سجل الأحداث» | **done** (the «ردّة الفعل» filter is not built) |
| إنشاء حملة (product by knowledge score) | step 1 now prints «N٪ معرفة» per product | **done** |
| متابعة الحملات (statuses + assistant reading) | `#kmon` reports live campaigns; مجدولة/مسودة do not exist because scheduling is deferred (DEC-10) | **partial, by decision** |
| معرفة المنتج | `#knowledge` — every product ranked least-ready first, missing sections named | **done** |
| شركاء المبيعات | `#partners` | **done** |
| المنتجات (product-manager dashboard) | `#products` list + `#product/<name>` record | **partial** (no product switcher on the record) |
| المستهدفات (year + quarterly split) | `#perf` opens on the year, per product, grouped by sector | **done** |
| التقارير (product acceptance) | `#reports` → «قبول المنتجات» | **done** |
| الهيكل التنظيمي | `#org` — sectors, departments, people | **done** |

Deliberately NOT copied: the prototype's navy-and-green palette (Massar keeps `#2563EB` and its type
tokens, per `DESIGN.md`), and any figure the ledger cannot prove — where the prototype shows a number
Massar has no data for, the screen says so instead of inventing one.
