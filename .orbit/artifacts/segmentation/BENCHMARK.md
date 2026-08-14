# التقسيم وإعادة الاستهداف — دراسة السوق قبل البناء
**11 منصة، بأدلة موثّقة.** طُلبت في R49: «ابحث عنه… أريده مبنيًا على السوق الحقيقي، لا على افتراض
متطلبات. قارن بتسع أدوات على الأقل تملك تقسيم إعادة الاستهداف، ثم ابنِ.»

الحالة التي وصفها المؤسس حرفيًا: **«فتح الرسالة عن هذا المنتج، ولم يردّ خمسة أيام ← نرسل له هذا القالب.»**

---

## ١. ما وجدناه: الحالة نفسها موجودة في السوق، وبالنافذة الزمنية نفسها
**Klaviyo** تشحن فئة جاهزة اسمها *High-intent WhatsApp shoppers*: «شاهد المنتج مرتين، بدأ الدفع،
**ولم يُكمل الطلب خلال آخر ٥ أيام**». نفس الشكل، ونفس الرقم الذي اختاره المؤسس.
→ الخمسة أيام ليست تخمينًا. ([Klaviyo WhatsApp segments](https://help.klaviyo.com/hc/en-us/articles/46806173017243))

## ٢. النواة التي لا تخلو منها أي أداة (٥/٥ في المجموعة الأولى)
| الأساس | المعنى | مثال حرفي من الأدوات |
|---|---|---|
| **حدث وقع / لم يقع** | الشرط الأول دائمًا | Klaviyo: «What someone has done (or not done)» |
| **نافذة زمنية نسبية** | `خلال آخر N يومًا` + `قبل` / `طوال الوقت` | Klaviyo · Braze · Customer.io · MoEngage |
| **التكرار** | `مرة على الأقل` / `صفر مرات` | Klaviyo: `At least once` · `Zero times` |
| **تجميع منطقي** | و/أو بمستوى تداخل واحد | Customer.io: «All» / «At least one» + Group |
| **عضوية حيّة** | الفئة تُحدِّث نفسها | الافتراضي في كل الأدوات |

**أنظف صياغة للحالة المطلوبة**، ونوصي بنسخها: Klaviyo `Zero times` + `In the last N days`.

## ٣. تسميات السوق للفئات (نستخدمها كما هي، لا نخترع أسماء)
| السوق | مسار | متاح في بياناتنا اليوم |
|---|---|---|
| Delivered-not-read (WATI: «Ignored») | **وصلت ولم تُقرأ** | ✅ `statusTimes.delivered` بلا `read` |
| Read-not-replied (WATI: «Read only (didn't reply)») | **قُرئت ولم يُردّ عليها** | ✅ `read` بلا `replied` |
| Replied | **ردّ** | ✅ |
| Failed / undelivered | **لم تُسلَّم** | ✅ `failed` |
| Lapsed / Winback (Attentive) | **ردّ ثم انقطع** | ✅ آخر رسالة واردة |
| Unengaged (HubSpot) | **غير متفاعل** | ✅ |
| — لا مقابل في السوق — | **مهتم بلا موعد** | ✅ وسم اهتمام بلا نتيجة بشرية |

آخر صف **فرصة تميّز لا فجوة**: لا أداة من الإحدى عشرة تربط قراءة نية الشراء بغياب اجتماع محجوز.

## ٤. النوافذ الافتراضية في المنتجات الحقيقية
| المنصة | النافذة |
|---|---|
| **Gupshup** (مزوّدنا) | **٧٢ ساعة** — سقفها أقل من طلب المؤسس |
| Attentive Winback | ٤٥ يومًا + انتظار ١٥ يومًا؛ تدرّج ٣٠/٦٠/٩٠ |
| HubSpot | ٩٠ يومًا |
| MoEngage · Insider · Klaviyo | بلا افتراضي — يحدده المسوّق |

**الحكم:** خمسة أيام **جريئة** بمقياس البريد والرسائل النصية (٣٠–٩٠ يومًا)، لكنها **متحفظة** بمقياس
المحادثات في واتساب. نعتمدها افتراضًا، قابلة للضبط بين ٣ و١٤ يومًا.

## ٥. الطبقة التي تفصلنا عن أدوات البريد (وهي الأهم)
- **نافذة الـ٢٤ ساعة**: خارجها لا يجوز إلا قالب معتمد. وبالتعريف، **كل** جمهور «لم يردّ منذ ٥ أيام»
  خارج النافذة ← إعادة الاستهداف **دائمًا** بقالب. ([Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages))
- **سقف Meta**: قالبان تسويقيان كحد أقصى للمستخدم الواحد كل ٢٤ ساعة **عبر كل الشركات**، والخطأ
  `131049` يعني أن الرسالة لم تصل. يجب أن نحسبه **نتيجة حقيقية لا نجاحًا**.
- **«فتح» مفهوم بريدي**: في واتساب لدينا *سُلِّمت · قُرئت · ردّ*، والقراءة قد يعطّلها العميل — فالتسمية
  الأمينة «قُرئت» لا «فُتحت».
- **فخ الأقدمية** (Customer.io توثّقه صراحة): جهة أُضيفت اليوم **لا يمكن** أن تحقق «لم يردّ منذ ٥ أيام».
  بلا حارس أقدمية، أول فئة يبنيها المؤسس ستعود فارغة. ([Customer.io](https://customer.io/docs/journeys/past-x-days-help/))

## ٦. الخطأ الذي نتجنّب نسخه
**WATI و AiSensy تفصلان النموذج إلى نصفين**: السلوك داخل تحليلات الحملة، والسمات داخل بانى الفئات،
**ولا يلتقيان**. لا يمكن التعبير عن «قرأ رسالة الخدمة س، ولم يردّ ٥ أيام، ولم نراسله خلال ٧ أيام» في
كائن واحد — تُعاد الاشتقاق يدويًا مع كل حملة، ولا شيء يمنع الإرسال المزدوج.

**قرارنا:** الفئة **كائن حيّ واحد فوق السجل**، ومعها **فحص تبريد/كتم إلزامي عند الإرسال**.

## ٧. الجدوى: كل الشروط محسوبة من بيانات نملكها الآن
تحقّقنا مباشرة من السجل الحيّ (قراءة فقط، بلا أي إرسال):

```
قُرئت ولم يُردّ عليها : 4 جهات   (أقدمها صامت منذ 1.2 يوم)
ردّ ثم انقطع        : 16 جهة
وصلت ولم تُقرأ       : 0
لم تُسلَّم           : 0
```

كل جهة تحمل أصلًا: `statusTimes` (sent · delivered · read · replied · failed) بطوابع زمنية،
ونص المحادثة بأدوارها، ووسوم الاهتمام بمستوياتها، والنتيجة البشرية، وسمات الملف المستورد
(المدينة · الحجم · القطاع)، وقراءة المساعد (نية · مرحلة · حكم الصفقة · سبب الخسارة).

**الناقص هو الباني، لا البيانات.**

---

## المصادر
Klaviyo ([الشروط](https://help.klaviyo.com/hc/en-us/articles/115005062847) · [التحديث](https://help.klaviyo.com/hc/en-us/articles/115005233488) · [واتساب](https://help.klaviyo.com/hc/en-us/articles/46806173017243)) ·
Braze ([المرشّحات](https://www.braze.com/docs/user_guide/audience/segments/segmentation_filters) · [إعادة الاستهداف](https://www.braze.com/docs/user_guide/messaging/campaigns/ideas_and_strategies/retargeting_campaigns)) ·
Customer.io ([الفئات](https://docs.customer.io/messaging/segmentation/segments/) · [فخ الأقدمية](https://customer.io/docs/journeys/past-x-days-help/)) ·
Iterable ([الاستعلام](https://support.iterable.com/hc/en-us/articles/29471665933972-Creating-a-Segmentation-Query)) ·
Mailchimp ([خيارات التقسيم](https://mailchimp.com/help/all-the-segmenting-options/) · [غير المتفاعلين](https://mailchimp.com/help/identify-inactive-subscribers/)) ·
WATI ([تحليلات الحملة](http://support.wati.io/en/articles/11463454-how-to-view-campaign-analytics) · [التنقيط](https://support.wati.io/en/articles/14734248-how-to-create-drip-campaigns-in-wati)) ·
AiSensy ([إعادة الاستهداف](https://aisensy.com/features/whatsapp-retargeting) · [تصفية الجمهور](https://wiki.aisensy.com/en/articles/11501871-filtering-audience-for-whatsapp-broadcasts)) ·
Gupshup ([Campaign Manager](https://www.gupshup.ai/en/converse/campaign-manager)) ·
MoEngage ([الحملات الحدثية](https://help.moengage.com/hc/en-us/articles/360058752652-Create-an-Event-Triggered-Campaign) · [سقف التكرار](https://help.moengage.com/hc/en-us/articles/15919660670356-Frequency-capping)) ·
Insider ([قناة واتساب](https://academy.insiderone.com/docs/architect-channel-use-whatsapp)) ·
HubSpot ([القوائم الحيّة](https://www.hublead.io/blog/hubspot-active-vs-static-list)) ·
Attentive ([Winback](https://help.attentivemobile.com/hc/en-us/articles/4406049270164-Create-a-winback-journey)) ·
Meta ([نافذة المراسلة](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages) · [فئات القوالب](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview))
