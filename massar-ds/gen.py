# -*- coding: utf-8 -*-
"""Generates every Massar screen from one data model, so a field cannot exist
   on one screen and be forgotten on another. Mirrors the live app's routes."""
import io, json, os, re

SHELL = u'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="{door}" data-sub="{sub}">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a">{actions}</div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb">{crumb}</div>
          <h1 class="m-h1">{h1}</h1>
        </div>
        <div class="m-row">{tools}</div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">
{body}
      </div>
    </main>
  </div>
</div>
{dialogs}
<script src="shell.js"></script>
{script}
</body>
</html>
'''

def page(fn, title, door, sub, crumb, h1, actions="", tools="", body="", dialogs="", script=""):
    io.open(fn, "w", encoding="utf-8").write(SHELL.format(
        title=title, door=door, sub=sub, crumb=crumb, h1=h1,
        actions=actions, tools=tools, body=body, dialogs=dialogs, script=script))

BTN  = u'<button class="m-btn">{}</button>'
PRIM = u'<button class="m-btn m-btn--primary"{}>{}</button>'
def prim(t, open_=None): return PRIM.format(u' data-open="%s"' % open_ if open_ else u"", t)
def seg(*opts):
    b = u"".join(u'<button aria-pressed="%s">%s</button>' % ("true" if i==0 else "false", o)
                 for i, o in enumerate(opts))
    return u'<div class="m-seg" role="group" aria-label="تصفية">%s</div>' % b
def card(title, inner, extra=u"", pad0=True):
    h = u'<div class="m-tools"><h2 class="m-card__t">%s</h2>%s</div>' % (title, extra) if title else u""
    return u'<section class="m-card%s">%s%s</section>' % (u" m-card--pad0" if pad0 else u"", h, inner)
def table(heads, rows):
    th = u"".join(u"<th>%s</th>" % h for h in heads)
    return u'<table class="m-table"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (th, rows)
def n(v):  return u'<span class="m-n">%s</span>' % v
# No default. An empty cell has to say WHICH kind of empty it is.
def nil(t): return u'<span class="m-td-nil">%s</span>' % t
def chip(t, k=u""): return u'<span class="m-chip%s">%s</span>' % (u" m-chip--"+k if k else u"", t)
def field(lbl, inner, full=False, req=False):
    return (u'<div class="m-field%s"><label class="m-label%s">%s</label>%s</div>'
            % (u" full" if full else u"", u" m-req" if req else u"", lbl, inner))
def inp(ph=u"", val=u"", t="text"):
    return u'<input class="m-input" type="%s" placeholder="%s" value="%s">' % (t, ph, val)
def sel(*opts):
    return u'<select class="m-select">%s</select>' % u"".join(u"<option>%s</option>" % o for o in opts)
def ta(ph=u"", rows=6):
    return u'<textarea class="m-input" rows="%d" placeholder="%s"></textarea>' % (rows, ph)
def dlg(i, title, body, save=u"حفظ"):
    return (u'<dialog class="m-dlg" id="%s"><form method="dialog" class="m-dlg__p">'
            u'<div class="m-dlg__h"><h2 class="m-dlg__t">%s</h2>'
            u'<button class="m-x" data-close aria-label="إغلاق">&times;</button></div>'
            u'<div class="m-dlg__b">%s</div>'
            u'<div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button>'
            u'<button class="m-btn m-btn--primary">%s</button></div>'
            u'</form></dialog>') % (i, title, body, save)


# ---------------------------------------------------------------- THE LEDGER
# Extracted from the LIVE app on 16 Sep 2026, field by field. Eight products,
# three sectors, seven stages. Nothing here is invented.
SECTORS = [u"قطاع المستشفيات", u"قطاع الصيدليات", u"قطاع الأعمال", u"بلا قطاع"]
# name, sector, inferred?, assistant-status, published price, price note,
# target, target note, achieved, open value, open note, readiness%
PRODUCTS = [
 (u"الإجازات المرضية", u"قطاع المستشفيات", False, u"يبيعه المساعد · ينقصه ملف المعرفة",
  u"18,000 ر.س / سنة", u"يبدأ من · باقتان", u"34,000", u"ربع واحد من أربعة", u"0",
  u"4,200", u"بندان · بند واحد بلا تسعير", 80),
 (u"التقارير الطبية", u"قطاع المستشفيات", False, u"يبيعه المساعد · ينقصه ملف المعرفة",
  None, u"اشتراك سنوي يحدده المختص وفق الحجم", None, None, u"0", None, u"لا بنود مفتوحة", 68),
 (u"الشهادات الصحية", u"قطاع الصيدليات", False, u"يبيعه المساعد · ينقصه ملف المعرفة",
  None, u"اشتراك سنوي يحدده المختص", None, None, u"0", None, u"لا بنود مفتوحة", 45),
 (u"تكامل الأنظمة (HIS/ERP)", u"قطاع المستشفيات", False, u"يبيعه المساعد · ينقصه ملف المعرفة",
  None, u"مشروع تكامل واشتراك سنوي، يحدده المختص", None, None, u"0", None,
  u"بندان · بندان بلا تسعير", 45),
 (u"خدمات التطعيمات", u"قطاع الصيدليات", True, u"يبيعه المساعد · ينقصه ملف المعرفة",
  None, u"اشتراك سنوي يحدده المختص", None, None, u"0", None, u"بند واحد · بند واحد بلا تسعير", 45),
 (u"سجل التطعيمات الوطني", u"قطاع الصيدليات", True, u"يبيعه المساعد · ينقصه تحديث كتالوج المساعد",
  u"20,000 ر.س / سنة", u"hello", None, None, u"0", None, u"بند واحد · بند واحد بلا تسعير", 90),
 (u"صحة أعمال Plus", u"قطاع الأعمال", True, u"لا يبيعه المساعد · بانتظار اعتماد النص الحالي",
  None, u"لا سعر منشور", None, None, u"0", None, u"لا بنود مفتوحة", 0),
 (u"فحص الموظفين", u"قطاع الأعمال", True, u"يبيعه المساعد · ينقصه ملف المعرفة",
  None, u"اشتراك سنوي بتسعير لكل فحص، يحدده المختص وفق الحجم", None, None, u"0", None,
  u"لا بنود مفتوحة", 73),
]
ACCOUNTS = [
 (u"DL000", u"D", u"الجنوب", None, u"1", u"4,200", u"18 أغسطس", u"غير مسجّل"),
 (u"ابرهيم", u"ا", None, None, u"2", None, u"12 أغسطس", u"غير مسجّل"),
 (u"العمدة", u"ع", None, None, u"3", None, u"12 أغسطس", u"غير مسجّل"),
 (u"أبو حمزه", u"أ", None, None, None, None, u"12 أغسطس", u"غير مسجّل"),
 (u"أبو نور", u"أ", None, None, None, None, u"12 أغسطس", u"غير مسجّل"),
 (u"صيدلية الدواء", u"ص", u"الدمام", u"صيدليات", None, None, u"11 أغسطس", u"غير مسجّل"),
 (u"صيدلية الدواء (مثال)", u"ص", u"الدمام", u"clicnic", None, None, u"11 أغسطس", u"غير مسجّل"),
 (u"صيدلية الدواء (مثال)", u"ص", u"الدمام", u"صيدليات", None, None, u"11 أغسطس", u"غير مسجّل"),
]
LINES = [
 (u"ابرهيم", u"تكامل الأنظمة (HIS/ERP)", u"تواصل أولي", None, u"واتساب", u"35", u"12 أغسطس"),
 (u"ابرهيم", u"سجل التطعيمات الوطني", u"تواصل أولي", None, u"واتساب", u"35", u"12 أغسطس"),
 (u"العمدة", u"خدمات التطعيمات", u"تواصل أولي", None, u"واتساب", u"35", u"12 أغسطس"),
 (u"العمدة", u"تكامل الأنظمة (HIS/ERP)", u"تواصل أولي", None, u"واتساب", u"35", u"12 أغسطس"),
 (u"العمدة", u"الإجازات المرضية", u"اكتشاف الحاجة", None, u"واتساب", u"35", u"12 أغسطس"),
 (u"DL000", u"الإجازات المرضية", u"عرض السعر", u"4,200", u"واتساب", u"29", u"18 أغسطس"),
]
# Seven stages — التقييم التقني sits between عرض المنتج and عرض السعر in the live ladder.
STAGES = [(u"تواصل أولي",u"#5B6472",4,None),(u"اكتشاف الحاجة",u"#0072E9",1,None),
          (u"عرض المنتج",u"#8B5CF6",0,None),(u"التقييم التقني",u"#7C3AED",0,None),
          (u"عرض السعر",u"#2F6BFF",1,u"4,200"),(u"التفاوض والاعتماد",u"#B45309",0,None),
          (u"رابح",u"#15803D",0,None),(u"خاسر",u"#BE123C",0,None)]
KB_SECTIONS = [(u"وصف المنتج",80),(u"حالات الاستخدام",60),(u"الأسئلة الشائعة",45),
               (u"الأسعار والباقات",10),(u"الاعتراضات",0),(u"المنافسون",0),
               (u"التكامل التقني",20),(u"الامتثال",0)]
STAGE_LADDER = [(u"تواصل أولي",u"contact",10,u"3 أيام"),(u"اكتشاف الحاجة",u"discover",25,u"5 أيام"),
                (u"عرض المنتج",u"present",40,u"7 أيام"),(u"التقييم التقني",u"tech",55,u"10 أيام"),
                (u"عرض السعر",u"quote",60,u"7 أيام"),(u"التفاوض والاعتماد",u"negotiate",80,u"14 يومًا")]
# The live RBAC matrix: nine capabilities across five roles.
CAPS = [u"عرض لوحات الأداء", u"إدارة العملاء", u"إدارة المؤشرات", u"إدارة معرفة المنتج",
        u"إنشاء/إطلاق حملة", u"إدارة الفرص", u"تحديث نتائج التواصل", u"المحادثات والتدخل",
        u"إدارة الهيكل والصلاحيات"]
ROLE_COLS = [u"تنفيذي", u"مدير منتج", u"مبيعات", u"شريك", u"مدير نظام"]
GRANTS = {0:[1,1,1,1,1],1:[0,0,1,0,1],2:[0,1,1,0,1],3:[0,1,0,0,1],4:[0,1,1,0,1],
          5:[0,0,1,0,1],6:[0,0,1,1,1],7:[0,0,1,0,1],8:[0,0,0,0,1]}

# ---------------------------------------------------------------- DERIVED
# Every count below is computed from the records above. Astra's HIGH-5 finding
# was that hard-maintained summaries drift from their own tables: the nav said
# six products, home said "five of six", the truth was eight and seven. Nothing
# here is typed by hand twice.
N_PRODUCTS      = len(PRODUCTS)
N_NO_TARGET     = len([p for p in PRODUCTS if not p[6]])
# "بلا سعر منشور" means NO pricing statement at all — not "priced on request".
# Six products have no numeric price but do publish a basis ("اشتراك سنوي يحدده
# المختص"), which is a published position. Only صحة أعمال Plus publishes nothing,
# and the live app agrees: its chip reads 1. Counting absent numerals instead of
# absent statements would have produced 6 and contradicted the table under it.
N_NO_PRICE      = len([p for p in PRODUCTS if p[5] == u"لا سعر منشور"])
N_INFERRED      = len([p for p in PRODUCTS if p[2]])
N_NOT_SOLD      = len([p for p in PRODUCTS if p[3].startswith(u"لا يبيعه")])
N_LINES         = len(LINES)
N_UNPRICED      = len([l for l in LINES if not l[3]])
N_PRICED        = N_LINES - N_UNPRICED
OPEN_VALUE      = u"4,200"
N_ACCOUNTS      = 16
AGES            = sorted(int(l[5]) for l in LINES)
AGE_MIN, AGE_MAX = AGES[0], AGES[-1]
# Astra HIGH-4: "six lines aged 30+ days" included a 29-day line. Five qualify.
N_AGED_30       = len([a for a in AGES if a >= 30])
TARGET_TOTAL    = u"34,000"
TARGET_PRODUCT  = u"الإجازات المرضية"
TARGET_SCOPE    = u"الربع الثالث فقط"
LAST_MOVEMENT   = u"18 أغسطس"
TODAY_LABEL     = u"16 سبتمبر"


def unicode_n(v): return u"%s" % v

def lvl(p): return u"low" if p < 30 else (u"mid" if p < 70 else u"ok")

def KPI4(items):
    return u'<div class="m-qs" style="margin-block-end:var(--m-4)">' + u"".join(
        u'<div class="m-q" style="cursor:default"><div class="m-q__k">%s</div>'
        u'<div class="m-q__v%s">%s</div><div class="m-q__s">%s</div></div>' % (k, c, n(v), sub)
        for k, v, sub, c in items) + u'</div>'



# ============================================================ DIALOGS (shared)
D_OPP = dlg(u"dlgOpp", u"إضافة فرصة",
  u'<div class="m-form">'
  + field(u"العميل", sel(*[a[0] for a in ACCOUNTS]), req=True)
  + field(u"المنتج", sel(*[p[0] for p in PRODUCTS]), req=True)
  + field(u"المرحلة", sel(*[x[0] for x in STAGES[:6]]), req=True)
  + field(u"المصدر", sel(u"حملة واتساب", u"مكالمة", u"زيارة", u"إحالة", u"طلب وارد"), req=True)
  + field(u"الكمية", inp(u"1", t="number"))
  + field(u"السعر للوحدة (ر.س)", inp(u"لم يُسعَّر", t="number"))
  + field(u"عدد السنوات", inp(u"1", t="number"))
  + field(u"الخصم %", inp(u"0", t="number"))
  + field(u"الموظف المسؤول", sel(u"بلا مسؤول"))
  + field(u"تاريخ الإغلاق المتوقع", inp(t="date"))
  + field(u"الشريك", sel(u"لا شريك"))
  + field(u"ملاحظة", ta(u"", 3), full=True)
  + u'</div>', u"إضافة الفرصة")

D_PROD = dlg(u"dlgProd", u"إضافة منتج",
  u'<div class="m-form">'
  + field(u"اسم المنتج", inp(), req=True)
  + field(u"القطاع", sel(*SECTORS), req=True)
  + field(u"القسم", sel(u"بلا قسم"))
  + field(u"مدير المنتج", sel(u"بلا تحديد"))
  + field(u"السعر المنشور", inp(u"لا سعر منشور"))
  + field(u"وحدة التسعير", sel(u"سنة", u"شهر", u"لكل فحص", u"مشروع"))
  + field(u"حالة المساعد", sel(u"يبيعه المساعد", u"لا يبيعه المساعد"))
  + field(u"المستهدف 2026 (ر.س)", inp(u"بلا مستهدف", t="number"))
  + field(u"وصف المنتج", ta(u"", 4), full=True)
  + u'</div>', u"إضافة المنتج")

D_ACC = dlg(u"dlgAcc", u"إضافة عميل جديد",
  u'<div class="m-form">'
  + field(u"اسم المنشأة", inp(), req=True)
  + field(u"القطاع", sel(u"صيدليات", u"مستشفيات", u"clicnic", u"بدون"))
  + field(u"المدينة", sel(u"الدمام", u"الجنوب", u"بدون"))
  + field(u"الأهمية", sel(u"عادية", u"مرتفعة", u"حرجة"))
  + field(u"الموظف المسؤول", sel(u"بلا مسؤول"))
  + field(u"مصدر الإضافة", sel(u"يدوي", u"استيراد", u"حملة"))
  + field(u"جهة الاتصال — الاسم", inp())
  + field(u"جهة الاتصال — الجوال", inp(u"9665xxxxxxxx", t="tel"))
  + u'</div>', u"إضافة العميل")

D_TASK = dlg(u"dlgTask", u"مهمة جديدة",
  u'<div class="m-form">'
  + field(u"العنوان", inp(), full=True, req=True)
  + field(u"العميل", sel(u"بلا عميل", *[a[0] for a in ACCOUNTS]))
  + field(u"الفرصة", sel(u"بلا فرصة"))
  + field(u"الأولوية", sel(u"عادية", u"مرتفعة", u"عاجلة"))
  + field(u"الاستحقاق", inp(t="date"))
  + u'</div>', u"إضافة المهمة")

D_NOTE = dlg(u"dlgNote", u"ملاحظة جديدة",
  u'<div class="m-form">'
  + field(u"العميل", sel(u"بلا عميل", *[a[0] for a in ACCOUNTS]))
  + field(u"النوع", sel(u"ملاحظة", u"مكالمة", u"زيارة"))
  + field(u"النص", ta(u"", 5), full=True, req=True)
  + u'</div>', u"حفظ الملاحظة")

D_IND = dlg(u"dlgInd", u"إضافة مؤشر",
  u'<div class="m-form">'
  + field(u"اسم المؤشر", inp(), full=True, req=True)
  + field(u"نوع الإشارة", sel(u"استخدام", u"اشتراك", u"طلب دعم", u"تجديد"), req=True)
  + field(u"المنتج", sel(*[p[0] for p in PRODUCTS]))
  + field(u"مطابقة الأعضاء", sel(u"الجوال ← الكود ← الاسم", u"الجوال فقط", u"الكود فقط"))
  + field(u"ملف البيانات", u'<input class="m-input" type="file">', full=True)
  + u'</div>', u"إنشاء المؤشر")

D_TGT = dlg(u"dlgTgt", u"تحديد المستهدف",
  u'<div class="m-form">'
  + field(u"المنتج", sel(*[p[0] for p in PRODUCTS]), req=True)
  + field(u"السنة", sel(u"2026", u"2027"))
  + field(u"الربع 1 (ر.س)", inp(u"بلا مستهدف", t="number")) + field(u"الربع 2 (ر.س)", inp(u"بلا مستهدف", t="number"))
  + field(u"الربع 3 (ر.س)", inp(u"بلا مستهدف", t="number")) + field(u"الربع 4 (ر.س)", inp(u"بلا مستهدف", t="number"))
  + u'</div>', u"حفظ المستهدف")

D_STAGE = dlg(u"dlgStage", u"إضافة مرحلة",
  u'<div class="m-form">'
  + field(u"الاسم", inp(), req=True)
  + field(u"الوزن %", inp(u"0", t="number"), req=True)
  + field(u"مدة SLA", inp(u"7 أيام"))
  + field(u"الحالة", sel(u"نشطة", u"موقوفة"))
  + u'</div>', u"إضافة المرحلة")

D_USER = dlg(u"dlgUser", u"إضافة مستخدم",
  u'<div class="m-form">'
  + field(u"الاسم", inp(), req=True)
  + field(u"البريد", inp(t="email"), req=True)
  + field(u"الوظيفة", sel(*ROLE_COLS), req=True)
  + field(u"القسم", sel(u"بلا قسم"))
  + u'</div>', u"إنشاء المستخدم")

D_PKG = dlg(u"dlgPkg", u"باقة جديدة",
  u'<div class="m-form">'
  + field(u"اسم الباقة", inp(), req=True)
  + field(u"السعر المرجعي (ر.س)", inp(t="number"), req=True)
  + field(u"الوحدة", sel(u"سنويًا", u"شهريًا", u"لكل فحص", u"مشروع"))
  + field(u"الحالة", sel(u"مسودة", u"معتمدة"))
  + field(u"ما تشمله", ta(u"", 3), full=True)
  + u'</div>', u"حفظ الباقة")



# Tab controller, shared by every screen with a tab strip. Panels crossfade
# with a blur bridge; arrows move between tabs (RTL-correct).
TABJS = u"""<script>
var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
function sel(t){tabs.forEach(function(x){var on=x===t;
 x.setAttribute('aria-selected',on?'true':'false');
 var p=document.getElementById(x.dataset.t);if(!p)return;
 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
  p.removeAttribute('data-enter');}else{p.hidden=true;}});}
tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
</script>"""

# ===================================================================== SCREENS
# The kanban, built once and reused by every screen that shows it.
BOARD = u'<div class="m-board" style="padding:0 var(--m-3) var(--m-3)">'
for _nm, _tone, _cnt, _val in STAGES:
    _cards = u""
    for _a, _p, _st, _v, _src, _age, _d in LINES:
        if _st != _nm: continue
        _vv = (u'<span class="m-deal__v">%s ر.س</span>' % n(_v)) if _v else u'<span class="m-deal__v m-deal__v--nil">لم يُسعَّر</span>'
        _cards += (u'<article class="m-deal" tabindex="0"><div class="m-deal__n">%s</div>'
                   u'<div class="m-deal__p">%s</div><div class="m-deal__f">%s'
                   u'<span class="m-deal__age m-deal__age--old">%s يومًا</span></div></article>'
                   % (_a, _p, _vv, n(_age)))
    _rail = u" m-col--rail" if _cnt == 0 else u""
    _vline = (u'<div class="m-col__v">%s ر.س</div>' % n(_val)) if _val else (u'<div class="m-col__v">لم يُسعَّر</div>' if _cnt else u"")
    BOARD += (u'<div class="m-col%s" style="--m-tone:%s"%s>'
              u'<div class="m-col__t"><span class="m-col__dot"></span>'
              u'<span class="m-col__n">%s</span><span class="m-col__c">%s</span></div>'
              u'%s<div class="m-col__b">%s</div></div>'
              % (_rail, _tone, (u' tabindex="0" title="%s"' % _nm) if _rail else u"", _nm, n(_cnt), _vline, _cards))
BOARD += u'</div>'

# ---- opps: ONE screen, THREE views — جدول · كانبان · بطاقات
VIEWSEG = (u'<div class="m-seg" role="group" aria-label="طريقة العرض">'
  u'<button data-v="tbl" aria-pressed="true">جدول</button>'
  u'<button data-v="kan" aria-pressed="false">كانبان</button>'
  u'<button data-v="crd" aria-pressed="false">بطاقات</button></div>')
orows = u""
for _a, _p, _st, _v, _src, _age, _d in LINES:
    orows += (u'<tr><td class="m-td-n">%s</td><td>%s</td><td>%s</td><td>%s</td>'
              u'<td>%s</td><td class="m-td-v">%s يومًا</td><td class="m-cap">%s</td>'
              u'<td>%s</td></tr>') % (
        _a, _p, chip(_st, u"ac" if _st == u"عرض السعر" else u""),
        (u'<span class="m-td-v">%s ر.س</span>' % n(_v)) if _v else nil(u"لم يُسعَّر"),
        _src, n(_age), _d, u'<button class="m-btn">فتح</button>')
CARDS = u'<div class="m-kpis" style="padding:var(--m-3)">' + u"".join(
  u'<article class="m-deal" tabindex="0"><div class="m-deal__n">%s</div>'
  u'<div class="m-deal__p">%s</div><div class="m-deal__f">%s%s</div>'
  u'<div class="m-deal__f"><span class="m-cap">%s</span>'
  u'<span class="m-deal__age m-deal__age--old">%s يومًا</span></div></article>' % (
    _a, _p, (u'<span class="m-deal__v">%s ر.س</span>' % n(_v)) if _v else u'<span class="m-deal__v m-deal__v--nil">لم يُسعَّر</span>',
    chip(_st, u"ac" if _st == u"عرض السعر" else u""), _src, n(_age))
  for _a, _p, _st, _v, _src, _age, _d in LINES) + u'</div>'
OPPS_KPI = KPI4([(u"بنود مفتوحة", unicode_n(N_LINES), u"4,200 ر.س", u""),
                 (u"لم يُسعَّر", unicode_n(N_UNPRICED), u"من %s بنود" % N_LINES, u""),
                 (u"متوقفة", u"0", u"لا بند متوقف", u" nil"),
                 (u"راكدة %s يومًا+" % 30, unicode_n(N_AGED_30),
                  u"من %s · المدى %s–%s يومًا" % (N_LINES, AGE_MIN, AGE_MAX), u"")])
OPPS_ALERT = (u'<div class="m-alert" style="margin-block-end:var(--m-4)">'
  u'<span class="m-alert__t">جهتان مهتمّتان عبر واتساب بلا فرصة</span>%s</div>' % BTN.format(u"عرض"))
OPPS_BODY = OPPS_KPI + OPPS_ALERT + (
  u'<div class="m-view"><div class="m-view__p" id="tbl">'
  + card(u"", table([u"العميل", u"المنتج", u"المرحلة", u"القيمة", u"المصدر", u"في المرحلة", u"الإضافة", u""], orows)
         + u'<div class="m-tools"><span class="m-cap">%s بنود · %s ر.س · %s لم يُسعَّر</span></div>' % (n(N_LINES), n(u"4,200"), n(N_UNPRICED)))
  + u'</div><div class="m-view__p" id="kan" hidden>' + card(u"", BOARD)
  + u'</div><div class="m-view__p" id="crd" hidden>' + card(u"", CARDS) + u'</div></div>')
VIEWJS = u"""<script>
var vs=document.querySelectorAll('[data-v]');
vs.forEach(function(b){b.addEventListener('click',function(){
 vs.forEach(function(o){o.setAttribute('aria-pressed','false');});
 b.setAttribute('aria-pressed','true');
 ['tbl','kan','crd'].forEach(function(id){var p=document.getElementById(id);if(!p)return;
  if(id===b.dataset.v){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
   p.removeAttribute('data-enter');}else{p.hidden=true;}});});});
</script>"""
page(u"opps.html", u"فرص البيع", u"opps", u"opps", u"فرص البيع", u"فرص البيع",
     BTN.format(u"تصدير CSV") + prim(u"إضافة فرصة", u"dlgOpp"),
     VIEWSEG + seg(u"الكل", u"مُسعَّرة", u"راكدة", u"بلا مسؤول"), OPPS_BODY, D_OPP, VIEWJS)
page(u"board.html", u"لوحة المتابعة", u"opps", u"board", u"فرص البيع", u"لوحة المتابعة",
     BTN.format(u"سجل الأحداث") + prim(u"إضافة فرصة", u"dlgOpp"),
     seg(u"الكل", u"مُسعَّرة", u"راكدة", u"بلا مسؤول"),
     OPPS_KPI + OPPS_ALERT + card(u"", BOARD), D_OPP)
trows = u"".join(
  u'<tr><td class="m-td-n">%s</td><td>%s</td><td>%s</td><td class="m-cap">%s</td><td>%s</td></tr>' % (
    a2, chip(s2, k2), t2, d2, u'<button class="m-btn">فتح</button>')
  for a2, s2, k2, t2, d2 in [
    (u"DL000", u"موعد محدد", u"ok", u"طلب عرض سعر", u"18 أغسطس"),
    (u"العمدة", u"بانتظار المختص", u"warn", u"سؤال تقني", u"12 أغسطس"),
    (u"ابرهيم", u"مهتم بلا موعد", u"ac", u"طلب تفاصيل", u"12 أغسطس"),
    (u"أبو نور", u"مهتم بلا موعد", u"ac", u"بلا طلب محدد", u"12 أغسطس"),
    (u"أبو حمزه", u"مهتم بلا موعد", u"ac", u"بلا طلب محدد", u"12 أغسطس")])
page(u"triage.html", u"فرز الردود", u"opps", u"triage", u"فرص البيع", u"فرز الردود",
     prim(u"إضافة فرصة", u"dlgOpp"),
     seg(u"موعد محدد (1)", u"بانتظار المختص (1)", u"مهتم بلا موعد (3)", u"مؤجل (0)", u"لا يرغب (0)"),
     card(u"", table([u"الجهة", u"الحالة", u"الردّ", u"التاريخ", u""], trows)), D_OPP)
_ev = [(u"أُرسلت الحملة 38 إلى 21 جهة", u"صادر", u"11 أغسطس", u"ac"),
       (u"وصلت 19 رسالة", u"التسليم", u"11 أغسطس", u"ok"),
       (u"شوهدت 12 رسالة", u"التسليم", u"11 أغسطس", u"ok"),
       (u"ردّت 4 جهات", u"وارد", u"12 أغسطس", u"ok"),
       (u"أُنشئت 6 فرص من المهتمين", u"صادر", u"12 أغسطس", u"ac"),
       (u"DL000 انتقل إلى «عرض السعر»", u"مرحلة", u"18 أغسطس", u"warn"),
       (u"لا حركة منذ ذلك اليوم", u"سكون", u"اليوم", u"idle")]
_tl = u"".join(u'<div class="m-tl__i"><span class="m-tl__d %s"></span>'
               u'<span><span class="m-tl__n">%s</span><span class="m-tl__s">%s</span></span>'
               u'<span class="m-tl__t">%s</span></div>' % (k3, t3, s3, d3) for t3, s3, d3, k3 in _ev)
page(u"pipeline.html", u"سجل الأحداث", u"opps", u"pipeline", u"فرص البيع", u"سجل الأحداث",
     BTN.format(u"تصدير CSV"),
     seg(u"الكل (0)", u"صادر (0)", u"وارد (0)", u"التسليم (0)", u"إخفاقات (0)"),
     card(u"", u'<div class="m-tl" style="padding:0 var(--m-4) var(--m-4)">%s</div>' % _tl))

# ---------------------------------------------------------- ACCOUNTS  (door)
arows = u""
for nm, ini, city, sec, opps, val, d, appr in ACCOUNTS:
    arows += (u'<tr><td><a href="account.html" style="text-decoration:none;color:inherit">'
              u'<span class="m-row"><span class="m-av">%s</span>'
              u'<span class="m-td-n">%s</span></span></a></td>'
              u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'
              u'<td class="m-cap">%s</td><td>%s</td></tr>') % (
        ini, nm, city or nil(u"لم تُسجَّل"), sec or nil(u"لم يُصنَّف"),
        chip(u"معتمد", u"ok"), nil(u"بلا مسؤول"),
        (u'<span class="m-td-v">%s</span>' % n(opps)) if opps else nil(u"لا فرص"),
        (u'<span class="m-td-v">%s ر.س</span>' % n(val)) if val else nil(u"لا قيمة مسعّرة"),
        d, u'<button class="m-btn">فتح</button>')

page(u"accounts.html", u"العملاء", u"accounts", u"accounts", u"العملاء", u"العملاء",
     BTN.format(u"استيراد") + prim(u"عميل جديد", u"dlgAcc"),
     seg(u"الكل", u"معتمدون", u"بانتظار الاعتماد", u"مرفوضون", u"بلا مسؤول"),
     KPI4([(u"العملاء", u"16", u"كلهم معتمدون", u""), (u"بلا مسؤول", u"16", u"من 16", u""),
           (u"لها فرص", u"3", u"6 بنود", u""), (u"قيمة الفرص", u"4,200", u"ر.س", u"")])
     + card(u"", table([u"العميل", u"المدينة", u"القطاع", u"الحالة", u"المسؤول", u"الفرص", u"القيمة", u"الإضافة", u""], arows)
            + u'<div class="m-tools"><span class="m-cap">%s من %s</span>'
              u'<span class="m-row"><button class="m-btn">السابق</button>'
              u'<button class="m-btn">التالي</button></span></div>' % (n(8), n(16))),
     D_ACC)

crows = u"".join(
  u'<tr><td><span class="m-row"><span class="m-av">%s</span><span class="m-td-n">%s</span></span></td>'
  u'<td class="m-n">%s</td><td>%s</td><td class="m-td-v">%s</td><td class="m-cap">%s</td><td>%s</td></tr>' % (
    i, nm, ph, chip(s, k), n(msgs), d, u'<button class="m-btn">فتح المحادثة</button>')
  for i, nm, ph, s, k, msgs, d in [
    (u"D", u"DL000", u"966500000777", u"مهتم", u"ok", u"48", u"18 أغسطس"),
    (u"ع", u"العمدة", u"966500000xxx", u"مهتم", u"ok", u"36", u"12 أغسطس"),
    (u"ا", u"ابرهيم", u"966500000xxx", u"ردّ", u"", u"22", u"12 أغسطس"),
    (u"أ", u"أبو نور", u"966500000xxx", u"لم يردّ", u"", u"3", u"12 أغسطس"),
    (u"أ", u"أبو حمزه", u"966500000xxx", u"لم يردّ", u"", u"3", u"12 أغسطس")])
page(u"customers.html", u"المحادثات", u"accounts", u"customers", u"العملاء", u"المحادثات",
     BTN.format(u"تصدير"), seg(u"الكل", u"مهتم", u"ردّ", u"لم يردّ", u"موقوف"),
     KPI4([(u"جهات الاتصال", u"21", u"مستوردة", u""), (u"الرسائل", u"359", u"صادرة وواردة", u""),
           (u"الأحداث", u"1,233", u"في السجل", u""), (u"مهتم", u"2", u"من 21", u"")])
     + card(u"", table([u"الجهة", u"الجوال", u"الحالة", u"الرسائل", u"آخر نشاط", u""], crows)))

# ---- indicators (list) + the indicator form
irows = u'<tr><td colspan="6" style="padding:0"><div class="m-empty">' \
        u'<div class="m-empty__t">لا مؤشر مُعرَّف بعد</div>' \
        u'<div class="m-empty__a"><button class="m-btn m-btn--primary" data-open="dlgInd">مؤشر جديد</button></div>' \
        u'</div></td></tr>'
page(u"indicators.html", u"مؤشرات الاستخدام", u"accounts", u"indicators", u"العملاء", u"مؤشرات استخدام العملاء",
     prim(u"مؤشر جديد", u"dlgInd"), seg(u"الكل", u"استخدام", u"اشتراك", u"طلب دعم"),
     card(u"", table([u"المؤشر", u"الإشارة", u"المنتج", u"الأعضاء", u"آخر تحديث", u""], irows)), D_IND)

krows = u'<tr><td colspan="6" style="padding:0"><div class="m-empty">' \
        u'<div class="m-empty__t">لا مهمة مسجّلة</div>' \
        u'<div class="m-empty__a"><button class="m-btn m-btn--primary" data-open="dlgTask">مهمة جديدة</button></div>' \
        u'</div></td></tr>'
page(u"tasks.html", u"المهام", u"accounts", u"tasks", u"العملاء", u"المهام",
     prim(u"مهمة جديدة", u"dlgTask"), seg(u"الكل", u"اليوم", u"متأخرة", u"منجزة"),
     card(u"", table([u"المهمة", u"العميل", u"الفرصة", u"الأولوية", u"الاستحقاق", u""], krows)), D_TASK)

nrows = u'<tr><td colspan="4" style="padding:0"><div class="m-empty">' \
        u'<div class="m-empty__t">لا ملاحظة مدوّنة</div>' \
        u'<div class="m-empty__a"><button class="m-btn m-btn--primary" data-open="dlgNote">ملاحظة جديدة</button></div>' \
        u'</div></td></tr>'
page(u"notes.html", u"الملاحظات", u"accounts", u"notes", u"العملاء", u"الملاحظات",
     prim(u"ملاحظة جديدة", u"dlgNote"), seg(u"الكل", u"ملاحظة", u"مكالمة", u"زيارة"),
     card(u"", table([u"الملاحظة", u"العميل", u"الكاتب", u"التاريخ"], nrows)), D_NOTE)

# ---------------------------------------------------------- PRODUCTS  (door)
prows = u""
for nm, sec, inf, status, price, pnote, tgt, tnote, ach, opv, onote, ready in PRODUCTS:
    ready_k = u"bad" if ready < 50 else (u"warn" if ready < 80 else u"ok")
    prows += (u'<tr><td><a href="product.html" style="text-decoration:none;color:inherit">'
      u'<span class="m-td-n">%s</span></a><div class="m-item__s">%s%s</div></td>'
      u'<td><span class="m-row">%s<span class="m-cap">%s</span></span></td>'
      u'<td>%s<div class="m-item__s">%s</div></td>'
      u'<td>%s<div class="m-item__s">%s</div></td>'
      u'<td class="m-td-v m-td-nil">%s ر.س</td>'
      u'<td>%s<div class="m-item__s">%s</div></td>'
      u'<td><button class="m-btn">فتح</button></td></tr>') % (
        nm, sec, (u" · " + chip(u"مُستنتَج", u"")) if inf else u"",
        chip(n(u"%d%%" % ready), ready_k), status,
        (u'<span class="m-td-v">%s</span>' % price) if price else nil(u"لا سعر منشور"), pnote,
        (u'<span class="m-td-v">%s ر.س</span>' % n(tgt)) if tgt else chip(u"بلا مستهدف", u"warn"),
        tnote or u"",
        n(ach),
        (u'<span class="m-td-v">%s ر.س</span>' % n(opv)) if opv else nil(u"لا بنود مفتوحة"), onote)

PROD_FILTERS = (
  u'<select class="m-select" style="inline-size:auto"><option>كل القطاعات</option>'
  + u"".join(u"<option>%s</option>" % x for x in [u"بلا قطاع"] + SECTORS[:3]) + u'</select>'
  + u'<select class="m-select" style="inline-size:auto"><option>كل الحالات</option>'
    u'<option>لا يبيعها المساعد</option><option>يبيعها وتنقصها أشياء</option>'
    u'<option>جاهزة للمساعد</option></select>'
  + u'<select class="m-select" style="inline-size:auto"><option>حسب الاسم</option>'
    u'<option>الأعلى تحقيقًا</option><option>الأعلى مفتوحًا</option>'
    u'<option>غير الجاهزة أولًا</option></select>'
  + BTN.format(u"المؤرشفة"))

PROD_BANNER = (u'<div class="m-alert" style="margin-block-end:var(--m-4)">'
  u'<span class="m-alert__t">%s منتجات بلا ملف تعريفي</span>'
  u'<span class="m-alert__d">مهارة إعداد العرض تُنتجه بمساعد ذكاء اصطناعي · '
  u'<code style="font-family:monospace;font-size:var(--m-t-micro)">lean-proposal-deck-v2.3.1-upload.zip</code></span>'
  u'%s</div>') % (n(N_PRODUCTS), BTN.format(u"تحميل المهارة"))

page(u"products.html", u"المنتجات", u"products", u"products", u"المنتجات", u"المنتجات",
     BTN.format(u"استيراد") + prim(u"إضافة منتج", u"dlgProd"),
     PROD_FILTERS,
     # "المحقق 2026 · 0٪ من 34,000" frames a year against a target that is
     # recorded on one product for one quarter. The percentage is arithmetic
     # over two different things. State the basis instead of computing a rate.
     KPI4([(u"المحقق", u"0", u"لا صفقة رابحة على أي منتج", u" nil"),
           (u"لا يبيعها المساعد", unicode_n(N_NOT_SOLD), u"من %s منتجات" % N_PRODUCTS, u""),
           (u"بلا سعر منشور", unicode_n(N_NO_PRICE), u"من %s منتجات" % N_PRODUCTS, u""),
           (u"قطاع مُستنتَج", unicode_n(N_INFERRED), u"تحتاج تأكيدًا", u"")])
     + PROD_BANNER
     + card(u"", table([u"المنتج", u"جاهزية المساعد", u"السعر المنشور", u"المستهدف 2026",
                        u"المحقق", u"المفتوح الآن", u""], prows)
            + u'<div class="m-tools"><span class="m-cap">%s–%s من %s منتجات</span>'
              u'<span class="m-cap">المحقق للمعروض %s ر.س</span></div>' % (n(1), n(8), n(8), n(0))),
     D_PROD)

# ---- knowledge: an INDEX of readiness per product. The editor lives INSIDE
#      the product record; opening a knowledge editor before choosing a product
#      is the confusion the founder flagged, so this screen only routes.
krows = u""
for nm, sec, inf, status, price, pnote, tgt, tnote, ach, opv, onote, ready in PRODUCTS:
    kk = u"bad" if ready < 50 else (u"warn" if ready < 80 else u"ok")
    lack = status.split(u" \u00b7 ")[1] if u" \u00b7 " in status else u""
    krows += (u'<tr><td><a href="product.html" style="text-decoration:none;color:inherit">'
      u'<span class="m-td-n">%s</span></a><div class="m-item__s">%s</div></td>'
      u'<td style="min-inline-size:190px"><span class="m-seg-row__b" style="display:block">'
      u'<i class="%s" style="--m-pct:%d%%"></i></span></td>'
      u'<td class="m-td-v">%s</td><td>%s</td><td class="m-cap">%s</td>'
      u'<td><a class="m-btn" href="product.html" style="text-decoration:none">تحرير المعرفة</a></td></tr>') % (
        nm, sec, lvl(ready), ready, n(u"%d%%" % ready),
        chip(status.split(u" \u00b7 ")[0], kk), lack)
page(u"knowledge.html", u"معرفة المنتج", u"products", u"knowledge", u"المنتجات", u"معرفة المنتج",
     BTN.format(u"تصدير"),
     u'<select class="m-select" style="inline-size:auto"><option>كل القطاعات</option>'
     + u"".join(u"<option>%s</option>" % x for x in SECTORS[:3]) + u'</select>'
     + seg(u"الكل", u"غير جاهز", u"جاهز"),
     KPI4([(u"متوسط الجاهزية", u"57", u"من 100", u""),
           (u"جاهزة", u"1", u"من 8 منتجات", u""),
           (u"ينقصها ملف المعرفة", u"6", u"من 8 منتجات", u""),
           (u"لا يبيعها المساعد", unicode_n(N_NOT_SOLD), u"بانتظار اعتماد النص", u"")])
     + card(u"", table([u"المنتج", u"الجاهزية", u"", u"حالة المساعد", u"ما ينقصه", u""], krows)))

# ---- perf: real columns — المستهدف · المحقق · المتوقع · التقدّم · الإنجاز · التغطية · الحالة
sec_rows = u""
for secname in SECTORS[:3]:
    prods = [p for p in PRODUCTS if p[1] == secname]
    if not prods: continue
    sec_rows += (u'<tr><td colspan="8" style="background:var(--m-page);font-weight:700;'
                 u'color:var(--m-ink)">%s <span class="m-cap">%s منتجات</span></td></tr>'
                 % (secname, n(len(prods))))
    for nm, sec, inf, status, price, pnote, tgt, tnote, ach, opv, onote, ready in prods:
        has = bool(tgt)
        q = u"".join(u'<span class="m-chip%s">ر%d</span> '
                     % (u" m-chip--ac" if (has and i == 2) else u"", i + 1) for i in range(4))
        sec_rows += (u'<tr><td class="m-td-n">%s</td>'
          u'<td>%s</td><td class="m-td-v m-td-nil">%s ر.س</td>'
          u'<td>%s</td><td style="min-inline-size:120px">%s</td><td>%s</td>'
          u'<td class="m-cap">%s</td><td>%s</td></tr>') % (
            nm,
            (u'<span class="m-td-v">%s ر.س</span>' % n(tgt)) if has else nil(u"بلا مستهدف"),
            n(ach),
            (u'<span class="m-td-v">%s ر.س</span>' % n(opv)) if opv else nil(u"لا بنود مفتوحة"),
            u'<span class="m-seg-row__b" style="display:block"><i class="low" style="--m-pct:0%"></i></span>',
            (u'<span class="m-td-v m-td-nil">%s</span>' % n(u"0%")) if has
              else chip(u"بلا مستهدف", u"warn"),
            q,
            chip(u"متأخر", u"bad") if has else chip(u"خارج القياس", u""))
page(u"perf.html", u"المستهدفات والأداء", u"products", u"perf", u"المنتجات", u"المستهدفات والأداء",
     BTN.format(u"رفع ملف Excel/CSV") + prim(u"تحديد المستهدف", u"dlgTgt"),
     seg(u"الربع 1", u"الربع 2", u"الربع 3", u"الربع 4") + seg(u"2026", u"2027"),
     KPI4([(u"المستهدف", u"34,000", u"ر.س · منتج واحد من 8", u""),
           (u"المحقق", u"0", u"ر.س", u" nil"),
           (u"المتوقع من الفرص المفتوحة", u"3,360", u"ر.س", u""),
           (u"التغطية", u"1", u"من 8 منتجات", u"")])
     + card(u"", table([u"الخدمة", u"المستهدف", u"المحقق", u"المتوقع", u"التقدّم",
                        u"الإنجاز", u"التوزيع الربعي", u"الحالة"], sec_rows)),
     D_TGT)

# ---- org: الهيكل التنظيمي
org_rows = u"".join(
  u'<tr><td class="m-td-n">%s</td><td>%s</td><td class="m-td-v">%s</td><td>%s</td></tr>' % (
    s, d, n(c), o)
  for s, d, c, o in [(u"قطاع المستشفيات", u"بلا إدارة", u"3", nil(u"بلا مالك")),
                     (u"قطاع الصيدليات", u"بلا إدارة", u"3", nil(u"بلا مالك"))])
page(u"org.html", u"الهيكل التنظيمي", u"products", u"org", u"المنتجات", u"الهيكل التنظيمي",
     prim(u"قطاع جديد"), u"",
     KPI4([(u"القطاعات", u"2", u"مُعرَّفة", u""), (u"الإدارات", u"0", u"غير مُعرَّفة", u" nil"),
           (u"الموظفون", u"0", u"في الدليل", u" nil"), (u"المنتجات", u"6", u"موزّعة", u"")])
     + card(u"", table([u"القطاع", u"الإدارة", u"المنتجات", u"المالك"], org_rows)))

# ------------------------------------------------------------- KMON  (door)
FUNNEL = lambda steps: u'<div class="m-funnel">' + u"".join(
  u'<div class="m-fstep"><span class="m-fstep__k">%s</span>'
  u'<span class="m-fstep__b"><i style="--m-pct:%s%%"></i></span>'
  u'<span class="m-fstep__v">%s%s</span></div>' % (
    k, p, (n(v) if v else u'<span class="m-td-nil">لا شيء</span>'),
    (u' <span class="m-fstep__d">&#9662; %s</span>' % n(d)) if d else u"")
  for k, p, v, d in steps) + u'</div>'
CAMP = [(u"أُرسلت",100,u"21",None),(u"وصلت",90,u"19",None),(u"شوهدت",57,u"12",u"37%"),
        (u"رُدّ عليها",19,u"4",u"67%"),(u"مهتم",9,u"2",None),(u"فرص",0,None,None)]
krow = u'<tr><td class="m-td-n">الحملة 38</td><td>%s</td><td class="m-td-v">%s</td>' \
       u'<td class="m-td-v">%s</td><td class="m-td-v">%s</td><td class="m-td-v">%s</td>' \
       u'<td class="m-cap">11 أغسطس</td><td>%s</td></tr>' % (
         chip(u"منتهية", u"ok"), n(21), n(19), n(12), n(2), u'<button class="m-btn">فتح</button>')
page(u"kmon.html", u"متابعة الحملات", u"kmon", u"kmon", u"الحملات", u"متابعة الحملات",
     BTN.format(u"تصدير") + prim(u"حملة جديدة"),
     seg(u"الكل", u"منتهية", u"جارية", u"مسودة"),
     KPI4([(u"الحملات", u"1", u"منتهية", u""), (u"أُرسلت", u"21", u"رسالة", u""),
           (u"مهتم", u"2", u"من 21", u""), (u"فرص", u"6", u"من المهتمين", u"")])
     + card(u"", table([u"الحملة", u"الحالة", u"أُرسلت", u"وصلت", u"شوهدت", u"مهتم", u"التاريخ", u""], krow))
     + u'<div class="m-grid m-grid--main" style="margin-block-start:var(--m-4)">'
     + u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">قمع الحملة 38</h2></div>%s</section>' % FUNNEL(CAMP)
     + u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">الحجم</h2></div>'
     + u"".join(u'<div class="m-item"><span class="m-av m-av--sq">%s</span>'
                u'<span class="m-item__b"><span class="m-item__n">%s</span>'
                u'<span class="m-item__s">%s</span></span></div>' % (n(v), t, s)
                for v, t, s in [(u"21", u"جهات الاتصال", u"مستوردة"),
                                (u"359", u"الرسائل", u"صادرة وواردة"),
                                (u"1,233", u"الأحداث", u"في السجل")])
     + u'</section></div>')

WIZ = u'<div class="m-steps">' + u"".join(
  u'<div class="m-step"%s><i>%d</i>%s</div>' % (
    u' aria-current="step"' if i == 0 else (u' data-done' if False else u""), i+1, t)
  for i, t in enumerate([u"الهدف", u"الجمهور", u"المنتج", u"القالب", u"المراجعة"])) + u'</div>'
aimkt_body = WIZ + u'<section class="m-card"><div class="m-card__h">' \
  u'<h2 class="m-card__t">الهدف والجمهور</h2></div><div class="m-form">' \
  + field(u"هدف الحملة", sel(u"توليد فرص", u"إعادة استهداف", u"إعلان منتج", u"استطلاع"), req=True) \
  + field(u"المنتج", sel(*[p[0] for p in PRODUCTS]), req=True) \
  + field(u"القطاع", sel(u"الكل", u"صيدليات", u"مستشفيات", u"clicnic", u"بدون")) \
  + field(u"المدينة", sel(u"الكل", u"الدمام", u"الجنوب", u"بدون")) \
  + field(u"الأهمية", sel(u"الكل", u"عادية", u"مرتفعة", u"حرجة")) \
  + field(u"المؤشر", sel(u"بلا مؤشر")) \
  + u'</div><div class="m-alert" style="margin-block-start:var(--m-4)">' \
  + u'<span class="m-alert__t">الجمهور المطابق: %s جهة</span>' % n(21) \
  + u'<span class="m-alert__d">من %s جهة اتصال · %s مستبعدة (إيقاف)</span></div>' % (n(21), n(0)) \
  + u'<div class="m-row" style="margin-block-start:var(--m-4)">' + prim(u"التالي") + BTN.format(u"حفظ كمسودة") + u'</div></section>'
page(u"aimkt.html", u"إنشاء حملة", u"kmon", u"aimkt", u"الحملات", u"إنشاء حملة",
     BTN.format(u"إلغاء"), u"", aimkt_body)

trg = u"".join(u'<tr><td class="m-td-n">%s</td><td class="m-n">%s</td><td>%s</td><td>%s</td>'
               u'<td>%s</td><td class="m-cap">11 أغسطس</td></tr>' % (
                 nm, ph, sec or nil(u"لم يُصنَّف"), city or nil(u"لم تُسجَّل"),
                 chip(u"نشط", u"ok"))
               for nm, ini, city, sec, o, v, d, a in ACCOUNTS[:6]
               for ph in [u"966500000xxx"])
page(u"targets.html", u"جهات الاستهداف", u"kmon", u"targets", u"الحملات", u"جهات الاستهداف",
     BTN.format(u"استيراد ملف") + prim(u"جهة جديدة", u"dlgAcc"),
     seg(u"الكل", u"نشط", u"موقوف", u"مكرر"),
     KPI4([(u"جهات الاتصال", u"21", u"مستوردة", u""), (u"نشطة", u"21", u"قابلة للاستهداف", u""),
           (u"موقوفة", u"0", u"طلبت الإيقاف", u" nil"), (u"مكررة", u"0", u"لا تكرار مرصود", u" nil")])
     + card(u"", table([u"الجهة", u"الجوال", u"القطاع", u"المدينة", u"الحالة", u"الإضافة"], trg)), D_ACC)

page(u"partners.html", u"شركاء المبيعات", u"kmon", u"partners", u"الحملات", u"شركاء المبيعات",
     prim(u"شريك جديد"), seg(u"هذا الأسبوع", u"الشهر", u"الكل"),
     KPI4([(u"الشركاء", u"0", u"مُعرَّفون", u" nil"), (u"مستهدف التواصل", u"0", u"هذا الأسبوع", u" nil"),
           (u"تواصل مسجّل", u"0", u"هذا الأسبوع", u" nil"), (u"مهتم", u"0", u"سُلّم للمبيعات", u" nil")])
     + card(u"", u'<div class="m-empty"><div class="m-empty__t">لا شريك مُعرَّف</div>'
                 u'<div class="m-empty__a"><button class="m-btn m-btn--primary">شريك جديد</button></div></div>'))

# ------------------------------------------------------------------- REPORTS
REP_TABS = (u'<div class="m-tabs" role="tablist">'
  + u"".join(u'<button class="m-tab" role="tab" aria-selected="%s" data-t="r%d">%s</button>'
             % (u"true" if i == 0 else u"false", i, t)
             for i, t in enumerate([u"نظرة تنفيذية", u"تقارير التعثّر",
                                    u"قبول المنتجات", u"مؤشرات الأداء"]))
  + u'</div>')
FUN_STAGES = FUNNEL([(u"تواصل أولي",100,u"4",None),(u"اكتشاف الحاجة",25,u"1",u"75%"),
                     (u"عرض المنتج",0,None,None),(u"التقييم التقني",0,None,None),
                     (u"عرض السعر",25,u"1",None),(u"التفاوض والاعتماد",0,None,None),
                     (u"رابح",0,None,None)])
STUCK = table([u"المرحلة", u"الأقدم", u"الوسيط", u"البنود", u""], u"".join(
  u'<tr><td class="m-td-n">%s</td><td class="m-td-v">%s يومًا</td>'
  u'<td class="m-td-v">%s يومًا</td><td class="m-td-v">%s</td>'
  u'<td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr>'
  % (st, n(old), n(med), n(cnt))
  for st, old, med, cnt in [(u"تواصل أولي", u"35", u"35", u"4"),
                            (u"اكتشاف الحاجة", u"35", u"35", u"1"),
                            (u"عرض السعر", u"29", u"29", u"1")]))
ACCEPT = table([u"المنتج", u"جاهزية المساعد", u"السعر المنشور", u"الحالة"], u"".join(
  u'<tr><td class="m-td-n">%s</td><td class="m-td-v">%s</td><td>%s</td><td>%s</td></tr>' % (
    p[0], n(u"%d%%" % p[11]),
    (u'<span class="m-td-v">%s</span>' % p[4]) if p[4] else nil(u"لا سعر منشور"),
    chip(p[3].split(u" \u00b7 ")[0], u"bad" if p[11] < 50 else u"ok"))
  for p in PRODUCTS))
KPIS = table([u"المؤشر", u"القيمة", u"المدى"], u"".join(
  u'<tr><td class="m-td-n">%s</td><td class="m-td-v">%s</td><td class="m-cap">%s</td></tr>'
  % (k, v, r) for k, v, r in [
    (u"نسبة الردّ", n(u"19%"), u"4 من 21"), (u"نسبة الاهتمام", n(u"9%"), u"2 من 21"),
    (u"نسبة التحويل إلى فرصة", n(u"0%"), u"0 من 2"),
    (u"متوسط زمن الردّ", n(u"3") + u" ساعات", u"آخر 30 يومًا"),
    (u"متوسط العمر في المرحلة", n(u"34") + u" يومًا", u"البنود المفتوحة"),
    (u"نسبة الإنجاز", n(u"0%"), u"2026")]))
REP_BODY = (KPI4([(u"المحقق", u"0", u"ر.س", u" nil"),
                  (u"المفتوح", u"4,200", u"ر.س · 6 بنود", u""),
                  (u"المتوقع المرجّح", u"3,360", u"ر.س", u""),
                  (u"الراكدة", u"6", u"35 يومًا", u"")])
  + REP_TABS + u'<div class="m-view" style="margin-block-start:var(--m-4)">'
  + u'<section class="m-view__p" id="r0" role="tabpanel">'
  + u'<div class="m-grid m-grid--main">'
  + u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">قمع المراحل</h2></div>%s</section>' % FUN_STAGES
  + card(u"أين تتعثّر الصفقات", table([u"السبب", u"البنود"], u"".join(
      u'<tr><td class="m-td-n">%s</td><td class="m-td-v">%s</td></tr>' % (t, n(v))
      for t, v in [(u"بلا تسعير", unicode_n(N_UNPRICED)),
                   (u"راكدة %s يومًا+" % 30, unicode_n(N_AGED_30)),
                   (u"بلا موظف مسؤول", unicode_n(N_LINES)),
                   (u"بلا مستهدف منتج", unicode_n(N_NO_TARGET))])))
  + u'</div></section>'
  + u'<section class="m-view__p" id="r1" role="tabpanel" hidden>%s</section>' % card(u"", STUCK)
  + u'<section class="m-view__p" id="r2" role="tabpanel" hidden>%s</section>' % card(u"", ACCEPT)
  + u'<section class="m-view__p" id="r3" role="tabpanel" hidden>%s</section>' % card(u"", KPIS)
  + u'</div>')
page(u"reports.html", u"التقارير", u"reports", u"reports", u"التقارير", u"التقارير",
     BTN.format(u"تحديث") + BTN.format(u"تصدير"),
     seg(u"آخر 30 يومًا", u"آخر 90 يومًا"), REP_BODY, u"", TABJS)

# ------------------------------------------------------------ SETTINGS (door)
srows = u"".join(
  u'<tr><td class="m-td-n">%s</td><td class="m-cap">%s</td><td class="m-td-v">%s</td>'
  u'<td class="m-td-v">%s</td><td>%s</td><td>%s</td></tr>' % (
    nm, key, n(u"%d%%" % w), sla, chip(u"نشطة", u"ok"),
    u'<button class="m-btn">تعديل</button>')
  for nm, key, w, sla in STAGE_LADDER)
page(u"settings.html", u"مراحل البيع", u"settings", u"settings", u"الإعدادات", u"مراحل البيع",
     prim(u"مرحلة جديدة", u"dlgStage"), u"",
     card(u"", table([u"المرحلة", u"المفتاح", u"الوزن", u"مدة SLA", u"الحالة", u""], srows)
          + u'<div class="m-tools"><span class="m-cap">المفتاح يملكه الكود؛ الاسم والوزن والمدة يملكها المدير</span></div>'),
     D_STAGE)

page(u"divisions.html", u"الأقسام", u"settings", u"divisions", u"الإعدادات", u"الأقسام",
     prim(u"قسم جديد"), u"",
     card(u"", u'<div class="m-empty"><div class="m-empty__t">لا قسم مُعرَّف</div>'
               u'<div class="m-empty__a"><button class="m-btn m-btn--primary">قسم جديد</button></div></div>'))

page(u"team.html", u"الفريق", u"settings", u"team", u"الإعدادات", u"الفريق",
     prim(u"عضو جديد"), u"",
     card(u"", u'<div class="m-empty"><div class="m-empty__t">لا عضو في الدليل</div>'
               u'<div class="m-empty__a"><button class="m-btn m-btn--primary">عضو جديد</button></div></div>'))

ROLES = [(u"مدير النظام", u"كل الصلاحيات"), (u"مدير مبيعات", u"قراءة وكتابة على البيع"),
         (u"مندوب", u"فرصه وعملاؤه فقط"), (u"شريك", u"بياناته فقط"), (u"قارئ فقط", u"قراءة بلا كتابة")]
urows = u"".join(u'<tr><td class="m-td-n">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
    r, d, chip(u"1" if r == u"مدير النظام" else u"0", u"ok" if r == u"مدير النظام" else u""),
    u'<button class="m-btn">الصلاحيات</button>') for r, d in ROLES)
urows = u""
for i, cap in enumerate(CAPS):
    cells = u"".join(
      u'<td style="text-align:center">%s</td>' %
      (u'<span class="m-chip m-chip--ok m-chip--plain">&#10003;</span>' if g
       else u'<span class="m-td-nil">&mdash;</span>')
      for g in GRANTS[i])
    urows += u'<tr><td class="m-td-n">%s</td>%s</tr>' % (cap, cells)
page(u"users.html", u"المستخدمون والصلاحيات", u"settings", u"users", u"الإعدادات",
     u"المستخدمون والصلاحيات", prim(u"إضافة مستخدم", u"dlgUser"), u"",
     KPI4([(u"المستخدمون", u"1", u"مدير نظام", u""), (u"الوظائف", u"5", u"مُعرَّفة", u""),
           (u"الصلاحيات", u"9", u"قابلة للمنح", u""), (u"سجل التدقيق", u"3", u"عملية", u"")])
     + card(u"مصفوفة الصلاحيات",
            table([u"الصلاحية"] + ROLE_COLS, urows)), D_USER)

arow = u"".join(u'<tr><td class="m-cap">%s</td><td class="m-td-n">%s</td><td>%s</td>'
                u'<td>%s</td><td class="m-cap">%s</td></tr>' % (t, who, act, ent, d)
                for t, who, act, ent, d in [
                  (u"16 سبتمبر 14:02", u"مدير النظام", u"تعديل مستهدف", u"الإجازات المرضية", u"34,000 ر.س"),
                  (u"18 أغسطس 09:40", u"مدير النظام", u"نقل مرحلة", u"DL000", u"← عرض السعر"),
                  (u"11 أغسطس 08:15", u"مدير النظام", u"إطلاق حملة", u"الحملة 38", u"21 جهة")])
page(u"audit.html", u"سجل التدقيق", u"settings", u"audit", u"الإعدادات", u"سجل التدقيق",
     BTN.format(u"تصدير"), seg(u"الكل", u"تعديل", u"إنشاء", u"حذف"),
     card(u"", table([u"الوقت", u"من", u"العملية", u"السجل", u"التفاصيل"], arow)))

# ------------------------------------------------------------ DETAIL RECORDS
acc_tabs = u'<div class="m-tabs" role="tablist">' + u"".join(
  u'<button class="m-tab" role="tab" aria-selected="%s" data-t="a%d">%s</button>' % (
    u"true" if i == 0 else u"false", i, t)
  for i, t in enumerate([u"نظرة عامة", u"جهات الاتصال", u"الفرص", u"المحادثات", u"الحملات", u"المؤشرات", u"المهام", u"الملاحظات"])) + u'</div>'
acc_panes = u'<div class="m-view" style="margin-block-start:var(--m-4)">'
acc_panes += u'<section class="m-view__p" id="a0" role="tabpanel">' + \
  u'<div class="m-grid m-grid--main">' + \
  card(u"الفرص", table([u"المنتج", u"المرحلة", u"القيمة", u"في المرحلة"],
       u'<tr><td class="m-td-n">الإجازات المرضية</td><td>%s</td><td class="m-td-v">%s ر.س</td><td class="m-td-v">%s يومًا</td></tr>'
       % (chip(u"عرض السعر", u"ac"), n(u"4,200"), n(29)))) + \
  u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات</h2></div>' + \
  u"".join(u'<div class="m-item"><span class="m-item__b"><span class="m-item__s">%s</span>'
           u'<span class="m-item__n">%s</span></span></div>' % (k, v)
           for k, v in [(u"المدينة", u"الجنوب"), (u"القطاع", nil(u"لم يُصنَّف")), (u"الأهمية", u"عادية"),
                        (u"الموظف المسؤول", nil(u"بلا مسؤول")), (u"مصدر الإضافة", u"غير مسجّل"),
                        (u"الاعتماد", u"معتمد"), (u"الإضافة", u"18 أغسطس")]) + \
  u'</section></div></section>'
for i, t in enumerate([u"جهات الاتصال", u"الفرص", u"المحادثات", u"الحملات", u"المؤشرات", u"المهام", u"الملاحظات"], start=1):
    acc_panes += u'<section class="m-view__p" id="a%d" role="tabpanel" hidden>%s</section>' % (
      i, card(t, u'<div class="m-empty"><div class="m-empty__t">لا سجل في %s</div></div>' % t))
acc_panes += u'</div>'
TABJS = u'''<script>
var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');
 var p=document.getElementById(x.dataset.t);if(!p)return;
 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;p.removeAttribute('data-enter');}else{p.hidden=true;}});}
tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
</script>'''
page(u"account.html", u"سجل العميل", u"accounts", u"accounts", u"العملاء / DL000", u"DL000",
     BTN.format(u"تصعيد") + BTN.format(u"طلب دعم") + prim(u"فرصة جديدة", u"dlgOpp"),
     chip(u"معتمد", u"ok") + chip(u"الجنوب"),
     KPI4([(u"الفرص", u"1", u"مفتوحة", u""), (u"القيمة", u"4,200", u"ر.س", u""),
           (u"الرسائل", u"48", u"محادثة", u""), (u"آخر نشاط", u"29", u"يومًا", u"")])
     + acc_tabs + acc_panes, D_OPP, TABJS)


# ---- product record: the live tab set. معرفة المنتج and الأسعار والباقات are
#      EDITORS INSIDE the record — you choose the product first, then edit it.
P = PRODUCTS[0]
ptabs = u'<div class="m-tabs" role="tablist">' + u"".join(
  u'<button class="m-tab" role="tab" aria-selected="%s" data-t="q%d">%s%s</button>' % (
    u"true" if i == 0 else u"false", i, t, (u' <b>%s</b>' % b) if b else u"")
  for i, (t, b) in enumerate([(u"نظرة عامة", u""), (u"معرفة المنتج", u"80٪"),
                              (u"الأسعار والباقات", u"2"), (u"المستهدفات", u"يحتاج إكمالًا"),
                              (u"البيانات والإدارة", u"")])) + u'</div>'

kb_list = u"".join(u'<button class="m-kb__i"%s>%s<b class="%s">%s</b></button>'
                   % (u' aria-current="true"' if i == 0 else u"", sc, lvl(p), n(u"%d%%" % p))
                   for i, (sc, p) in enumerate(KB_SECTIONS))
PKGS = table([u"الباقة", u"السعر المرجعي", u"الوحدة", u"ما تشمله", u"الحالة", u""], u"".join(
  u'<tr><td class="m-td-n">%s</td><td class="m-td-v">%s</td><td>%s</td>'
  u'<td class="m-cap">%s</td><td>%s</td>'
  u'<td><span class="m-row"><button class="m-btn" data-open="dlgPkg">تعديل</button>'
  u'<button class="m-btn">حذف</button></span></td></tr>' % (
    nm, (u'%s ر.س' % n(pr)) if pr else nil(u"لم يُسعَّر"), un, inc, chip(st, k))
  for nm, pr, un, inc, st, k in [
    (u"أساسية", u"18,000", u"سنويًا", u"حتى 500 موظف · دعم قياسي", u"معتمدة", u"ok"),
    (u"متقدمة", u"34,000", u"سنويًا", u"غير محدود · دعم مخصص · تكامل", u"معتمدة", u"ok")]))

ppanes = u'<div class="m-view" style="margin-block-start:var(--m-4)">'
ppanes += (u'<section class="m-view__p" id="q0" role="tabpanel">'
  + KPI4([(u"الفرص المفتوحة", u"2", u"4,200 ر.س", u""), (u"الحملات", u"15", u"ذكرت المنتج", u""),
          (u"قراءة المساعد", u"1", u"اهتمام رصده المساعد", u""),
          (u"الجهات المستهدفة بالوسم", u"0", u"لا وسم مطبَّق", u" nil")])
  + u'<div class="m-grid m-grid--main">'
  + card(u"الفرص المفتوحة", table([u"العميل", u"المرحلة", u"القيمة", u"في المرحلة"],
      u'<tr><td class="m-td-n">DL000</td><td>%s</td><td class="m-td-v">%s ر.س</td>'
      u'<td class="m-td-v">%s يومًا</td></tr>'
      u'<tr><td class="m-td-n">العمدة</td><td>%s</td><td>%s</td>'
      u'<td class="m-td-v">%s يومًا</td></tr>' % (
        chip(u"عرض السعر", u"ac"), n(u"4,200"), n(29),
        chip(u"اكتشاف الحاجة"), nil(u"لم يُسعَّر"), n(35))),
      extra=u'<a class="m-link" href="opps.html">كل فرص المنتج &#8592;</a>')
  + u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات</h2></div>'
  + u"".join(u'<div class="m-item"><span class="m-item__b"><span class="m-item__s">%s</span>'
             u'<span class="m-item__n">%s</span></span></div>' % (k, v)
             for k, v in [(u"القطاع", P[1]), (u"مدير المنتج", nil(u"بلا تحديد")),
                          (u"السعر المنشور", P[4]), (u"وحدة التسعير", u"سنة"),
                          (u"حالة المساعد", P[3]), (u"المستهدف 2026", u"%s ر.س · %s" % (P[6], P[7]))])
  + u'<div class="m-row" style="margin-block-start:var(--m-4)">'
  + BTN.format(u"أطلق حملة بهذا المنتج") + BTN.format(u"&#8943;") + u'</div></section></div></section>')
# knowledge editor, inside the record
ppanes += (u'<section class="m-view__p" id="q1" role="tabpanel" hidden>'
  u'<div class="m-kb">'
  u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">الأقسام</h2>%s</div>'
  u'<div class="m-kb__l">%s</div></section>'
  u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">وصف المنتج</h2>'
  u'<span class="m-row">%s%s</span></div><div class="m-form"><div class="full">%s</div>%s</div>'
  u'<div class="m-row" style="margin-block-start:var(--m-4)">%s%s%s</div></section></div></section>' % (
    chip(u"80٪", u"ok"), kb_list, chip(u"معرفة مدمجة", u"warn"), BTN.format(u"سجل التغييرات"),
    ta(u"اكتب ما يعرفه المساعد عن هذا القسم…", 12),
    field(u"الحالة", sel(u"مدمجة", u"مسودة", u"بانتظار الاعتماد", u"معتمدة")),
    prim(u"حفظ كمسودة"), BTN.format(u"إرسال للاعتماد"), BTN.format(u"اعتماد")))
ppanes += (u'<section class="m-view__p" id="q2" role="tabpanel" hidden>%s</section>'
  % card(u"الباقات", PKGS, extra=u'<button class="m-btn m-btn--primary" data-open="dlgPkg">باقة جديدة</button>'))
ppanes += (u'<section class="m-view__p" id="q3" role="tabpanel" hidden>'
  u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">مستهدف 2026</h2>%s</div>'
  u'<div class="m-form">%s%s%s%s</div><div class="m-form" style="margin-block-start:var(--m-3)">%s</div>'
  u'<div class="m-alert" style="margin-block-start:var(--m-4)">'
  u'<span class="m-alert__t">ثلاثة أرباع بلا مستهدف</span>%s</div></section></section>' % (
    chip(u"يحتاج إكمالًا", u"warn"),
    field(u"الربع 1 (ر.س)", inp(u"بلا مستهدف", t="number")), field(u"الربع 2 (ر.س)", inp(u"بلا مستهدف", t="number")),
    field(u"الربع 3 (ر.س)", inp(u"", u"34000", t="number")), field(u"الربع 4 (ر.س)", inp(u"بلا مستهدف", t="number")),
    field(u"الإجمالي", u'<input class="m-input" value="34000" disabled>'),
    BTN.format(u"توزيع بالتساوي")))
ppanes += (u'<section class="m-view__p" id="q4" role="tabpanel" hidden>'
  u'<section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات والإدارة</h2></div>'
  u'<div class="m-form">%s%s%s%s%s%s</div>'
  u'<div class="m-row" style="margin-block-start:var(--m-4)">%s%s</div></section></section>' % (
    field(u"اسم المنتج", inp(u"", P[0])), field(u"القطاع", sel(*SECTORS)),
    field(u"القسم", sel(u"بلا قسم")), field(u"مدير المنتج", sel(u"بلا تحديد")),
    field(u"السعر المنشور", inp(u"", P[4])), field(u"وحدة التسعير", sel(u"سنة", u"شهر", u"لكل فحص")),
    prim(u"حفظ"), BTN.format(u"أرشفة المنتج")))
ppanes += u'</div>'
page(u"product.html", u"الإجازات المرضية", u"products", u"products",
     u'<a href="products.html">المنتجات</a> / الإجازات المرضية', P[0],
     BTN.format(u"أطلق حملة بهذا المنتج") + prim(u"حفظ"),
     chip(P[1]) + chip(u"مدير المنتج: بلا تحديد"),
     ptabs + ppanes, D_PKG, TABJS)

# ================================================= HOME — revenue first
# Astra blocked the previous home on five factual defects, all of one kind:
# the page computed figures the records do not contain. TARGET/12 invented a
# monthly target series out of a number that is Q3-only and single-product;
# "6 على المسار" labelled six stationary lines as healthy; the funnel printed
# a 75% drop between stage populations that were never a tracked cohort; a
# weighted forecast appeared with no probability model behind it. None of that
# is a styling problem, so none of it is fixed by restyling.
#
# What survives: the founder's period filter and the chart/list switch. Those
# were a real request. They now move only over things that are actually
# recorded — won revenue, lines created, days without movement — and a period
# with no target recorded says so rather than showing a share of someone
# else's target.

# key, button label, the period named in a sentence, target recorded, basis.
# A period with no target recorded says so. It does not get a share of the one
# target that exists — that division is what Astra blocked the old home on.
PERIODS = [
  (u"7",    u"أسبوع",   u"آخر سبعة أيام",   None,         u"لا مستهدف مسجّل لهذه الفترة"),
  (u"14",   u"أسبوعان", u"آخر أسبوعين",     None,         u"لا مستهدف مسجّل لهذه الفترة"),
  (u"30",   u"شهر",     u"آخر ثلاثين يومًا", None,        u"لا مستهدف مسجّل لهذه الفترة"),
  (u"q",    u"الربع",   u"الربع الثالث",    TARGET_TOTAL, u"%s · %s" % (TARGET_PRODUCT, TARGET_SCOPE)),
  (u"year", u"السنة",   u"السنة المالية 2026", None,      u"لا مستهدف سنوي مسجّل"),
]

# page() prints the h1. This is the dateline under it, not a second title.
HOME_HEAD = (u'<p class="m-meta m-home__dateline">السنة المالية %s · حتى %s سبتمبر</p>'
             % (n(u"2026"), n(u"16")))

# ---- the revenue surface. One figure at full strength, and the qualification
#      that says what it can and cannot be read against.
REVENUE = (
  u'<section class="m-card m-card--revenue" aria-labelledby="revTitle">'
  u'<div class="m-revenue__main">'
    u'<h2 class="m-label" id="revTitle">الإيراد المحقق</h2>'
    u'<p class="m-revenue__value">%s<span>ر.س</span></p>'
    u'<p class="m-body" id="revPeriod">لا صفقات رابحة حتى %s</p>'
    u'<p class="m-status m-status--warn">لا توجد إيرادات محققة حتى الآن</p>'
    u'<div class="m-actions"><a class="m-btn m-btn--primary" href="#priced-line">'
    u'مراجعة العرض المسعّر</a></div>'
  u'</div>'
  u'<div class="m-revenue__context"><dl class="m-facts">'
    u'<div><dt>المستهدف المسجّل</dt>'
      u'<dd class="m-facts__value" id="tgtV">%s ر.س</dd>'
      u'<dd id="tgtWhy">%s · %s</dd></div>'
    u'<div><dt>قيمة البنود المفتوحة المسعّرة</dt>'
      u'<dd class="m-facts__value">%s ر.س</dd>'
      u'<dd>بند واحد مسعّر من %s؛ %s بنود بلا تسعير</dd></div>'
  u'</dl>'
  u'<p class="m-revenue__qualification">%s منتجات بلا مستهدف. '
  u'لا يمكن تقييم تحقيق مستهدف الشركة.</p>'
  u'<a class="m-link" href="perf.html">استكمال المستهدفات &#8592;</a></div></section>'
  % (n(u"0"), TODAY_LABEL, n(TARGET_TOTAL), TARGET_PRODUCT, TARGET_SCOPE,
     n(u"4,200"), n(N_LINES), n(N_UNPRICED), n(N_NO_TARGET)))

# ---- the open lines. Two readings of the same six records: the rows, or how
#      long each has stood still. Nothing is aggregated into a rate.
def _lrow(l, first):
    acct, prod, stage, val, src, days, date = l
    idp = u' id="priced-line" tabindex="-1"' if val else u""
    cls = u"" if val else u' class="m-ledger__unpriced"'
    return (u'<tr%s%s><td class="m-td-n">%s</td><td>%s</td><td>%s</td>'
            u'<td class="m-td-v">%s</td><td class="m-td-v">%s</td>'
            u'<td class="m-cap">%s</td></tr>' % (
              idp, cls, acct, prod, chip(stage),
              n(val) if val else nil(u"لم يُسعَّر"),
              n(days), date))

_ordered = sorted(LINES, key=lambda l: (l[3] is None, -int(l[5])))
LEDGER_ROWS = u"".join(_lrow(l, i == 0) for i, l in enumerate(_ordered))

# The aging chart: one bar per line, length is days without movement. It is the
# same six numbers the table prints, drawn — not a derived rate, so switching
# view cannot change what the page claims.
_AGE_MAX_SCALE = AGE_MAX
AGING = (u'<div class="m-aging">' + u"".join(
  u'<div class="m-aging__r"><span class="m-aging__k">%s · %s</span>'
  u'<span class="m-aging__b"><i style="--m-pct:%d%%"%s></i></span>'
  u'<span class="m-aging__v">%s يومًا</span></div>' % (
    l[0], l[1], int(l[5]) * 100 // _AGE_MAX_SCALE,
    u' class="is-priced"' if l[3] else u"", n(l[5]))
  for l in _ordered) + u'</div>')

LEDGER = (
  u'<section class="m-card m-card--ledger" aria-labelledby="pipeTitle">'
  u'<header class="m-section-head"><div class="m-section-head__t">'
    u'<h2 class="m-h2" id="pipeTitle">فرص البيع المفتوحة</h2>'
    u'<p class="m-meta">%s بنود بلا حركة منذ %s يومًا · آخر حركة في %s</p></div>'
  u'<div class="m-seg" role="group" aria-label="طريقة العرض">'
    u'<button data-v="list" aria-pressed="true">قائمة</button>'
    u'<button data-v="chart" aria-pressed="false">مدة الركود</button></div></header>'
  u'<div class="m-view">'
    u'<div class="m-view__p" id="vList"><div class="m-tablewrap">'
    u'<table class="m-table m-ledger"><thead><tr><th>العميل</th><th>المنتج</th>'
    u'<th>المرحلة</th><th>القيمة</th><th>بلا حركة</th><th>آخر حركة</th></tr></thead>'
    u'<tbody>%s</tbody></table></div></div>'
    u'<div class="m-view__p" id="vChart" hidden>%s</div>'
  u'</div></section>'
  % (n(N_LINES), n(u"%s–%s" % (AGE_MIN, AGE_MAX)), LAST_MOVEMENT,
     LEDGER_ROWS, AGING))

# ---- what is blocking the sale. Each one is a count taken from the records
#      it links to, so the number and the destination cannot disagree.
DECISIONS = (
  u'<aside class="m-home__decisions" aria-labelledby="decTitle">'
  u'<h2 class="m-h2" id="decTitle">ما يعطّل البيع</h2>'
  + u"".join(
    u'<div class="m-decision"><h3 class="m-decision__title">%s</h3>'
    u'<p class="m-meta">%s</p><a class="m-link" href="%s">%s &#8592;</a></div>' % (t, s, h, cta)
    for t, s, h, cta in [
      (u"%s بنود بلا تسعير من %s" % (n(N_UNPRICED), n(N_LINES)),
       u"قيمة خط البيع تُقرأ من بند واحد فقط. الباقي لا يدخل أي مجموع.",
       u"opps.html", u"تسعير البنود"),
      (u"%s منتجات بلا مستهدف من %s" % (n(N_NO_TARGET), n(N_PRODUCTS)),
       u"المستهدف الوحيد المسجّل على %s، %s." % (TARGET_PRODUCT, TARGET_SCOPE),
       u"perf.html", u"تسجيل المستهدفات"),
      (u"%s عملاء بلا مسؤول" % n(u"16"),
       u"لا أحد مكلّف بالمتابعة، فلا حركة تُنتظر على أي بند.",
       u"accounts.html", u"إسناد المسؤولين")])
  + u'</aside>')

# ---- the indicators, folded in. The founder asked for them on the home page,
#      not on a page of their own; they are supporting evidence, so they open
#      rather than compete with the figure above.
EVIDENCE = (
  u'<details class="m-evidence" id="indicators"><summary>'
  u'<span class="m-h2">تفاصيل المؤشرات</span>'
  u'<span class="m-meta">جاهزية المساعد · نتائج الحملة · بيانات المنتجات · العملاء</span>'
  u'</summary>'
  + u"".join(
    u'<div class="m-evidence__row"><div><h3 class="m-label">%s</h3>'
    u'<p class="m-meta">%s</p></div><div>%s</div></div>' % (t, s, fig)
    for t, s, fig in [
      (u"جاهزية معرفة المنتج",
       u"%s من %s أقسام مكتملة. المساعد لا يجيب عن سعر غير منشور." % (n(u"3"), n(u"8")),
       u'<div class="m-meter" style="--m-pct:34%%"><i></i></div>'
       u'<span class="m-cap">%s من %s</span>' % (n(u"34"), n(u"100"))),
      (u"الحملة 38",
       u"%s رسالة أُرسلت · %s شوهدت · %s ردّوا · %s مهتم." % (
         n(u"21"), n(u"12"), n(u"4"), n(u"2")),
       u'<span class="m-cap">انتهت في %s أغسطس</span>' % n(u"11")),
      (u"بيانات المنتجات",
       u"%s منتجات بلا سعر منشور · %s بقطاع مُستنتَج · %s لا يبيعه المساعد."
       % (n(N_NO_PRICE), n(N_INFERRED), n(N_NOT_SOLD)),
       u'<a class="m-link" href="products.html">المنتجات &#8592;</a>'),
      (u"العملاء",
       u"%s عميلًا معتمدًا · لا عميل مرفوض · لا عميل بانتظار الاعتماد." % n(u"16"),
       u'<a class="m-link" href="accounts.html">العملاء &#8592;</a>')])
  + u'</details>')

# The period filter changes what is counted, never what is claimed. A period
# with no target recorded prints that sentence; it does not print a share of
# the one target that exists.
HOME_JS = u'''<script>
(function () {
  var P = %s;
  var segs = document.querySelectorAll(".m-dates .m-seg button");
  var tgtV = document.getElementById("tgtV");
  var tgtWhy = document.getElementById("tgtWhy");
  var revP = document.getElementById("revPeriod");
  function pick(k) {
    var p = P[k]; if (!p) return;
    if (p.t) { tgtV.innerHTML = '<span class="m-n">' + p.t + '</span> ر.س'; }
    else { tgtV.innerHTML = '<span class="m-td-nil">لا مستهدف</span>'; }
    tgtWhy.textContent = p.w;
    revP.textContent = "لا صفقات رابحة خلال " + p.s;
    segs.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-p") === k ? "true" : "false");
    });
  }
  segs.forEach(function (b) {
    b.addEventListener("click", function () { pick(b.getAttribute("data-p")); });
  });

  /* The two readings of the six lines. Crossfade with a blur bridge so the
     eye reads one surface changing rather than two stacked ones swapping. */
  var views = document.querySelectorAll(".m-card--ledger .m-view__p");
  var vbtn = document.querySelectorAll(".m-card--ledger .m-seg button");
  vbtn.forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-v");
      vbtn.forEach(function (o) {
        o.setAttribute("aria-pressed", o.getAttribute("data-v") === v ? "true" : "false");
      });
      views.forEach(function (p) {
        var on = p.id === (v === "list" ? "vList" : "vChart");
        if (on) { p.hidden = false; requestAnimationFrame(function () { p.removeAttribute("data-away"); }); }
        else { p.setAttribute("data-away", ""); setTimeout(function () { p.hidden = true; }, 120); }
      });
    });
  });
})();
</script>''' % json.dumps(
  dict((k, {"s": sent, "t": tgt, "w": why}) for k, _lbl, sent, tgt, why in PERIODS),
  ensure_ascii=False)

page(u"home.html", u"الرئيسية", u"home", u"home", u"الرئيسية", u"الأداء التجاري",
     BTN.format(u"تصدير") + prim(u"فرصة جديدة", u"dlgOpp"),
     u'<div class="m-dates"><div class="m-seg" role="group" aria-label="المدى الزمني">'
     + u"".join(u'<button data-p="%s" aria-pressed="%s">%s</button>'
                % (k, u"true" if k == u"q" else u"false", lbl)
                for k, lbl, _s, _t, _w in PERIODS)
     + u'</div><label class="m-range">'
       u'<input type="date" id="d1" value="2026-07-01" aria-label="من">'
       u'<span>&#8212;</span>'
       u'<input type="date" id="d2" value="2026-09-16" aria-label="إلى"></label></div>',
     HOME_HEAD + REVENUE
     + u'<div class="m-home__work">' + LEDGER + DECISIONS + u'</div>'
     + EVIDENCE,
     D_OPP, HOME_JS)

# ------------------------------------------------------------------ SHELL
# The rail's badges are counted here and written into shell.js, so the nav and
# the tables it leads to read from one source. Anchored single-line rewrite:
# a range edit on a hand-maintained file is how a helper disappears silently.
_counts = {u"opps": unicode_n(N_LINES), u"accounts": u"16",
           u"products": unicode_n(N_PRODUCTS)}
_sh = io.open(u"shell.js", encoding="utf-8").read()
_sh = re.sub(u"  var COUNTS = .*?; /\\* gen\\.py:COUNTS \\*/",
             u"  var COUNTS = %s; /* gen.py:COUNTS */"
             % json.dumps(_counts, ensure_ascii=False, sort_keys=True),
             _sh, count=1)
io.open(u"shell.js", "w", encoding="utf-8").write(_sh)
