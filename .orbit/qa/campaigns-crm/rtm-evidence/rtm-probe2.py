#!/usr/bin/env python3
import json, re
from pathlib import Path
BASE = "http://localhost:8098"
ENV = Path("/private/tmp/claude-501/-Users-abdulaziz-Projects-Massar/6ce77bb9-3bcb-4e49-9b8b-eb5155bc2f5a/scratchpad/wt645/.env")
OUT = Path("/private/tmp/claude-501/-Users-abdulaziz-Projects-Massar/6ce77bb9-3bcb-4e49-9b8b-eb5155bc2f5a/scratchpad/rtm-evidence")
tok = re.search(r"^ADMIN_TOKEN=(.+)$", ENV.read_text(encoding="utf-8"), re.M).group(1).strip()
FX = Path("/private/tmp/claude-501/-Users-abdulaziz-Projects-Massar/6ce77bb9-3bcb-4e49-9b8b-eb5155bc2f5a/scratchpad/rtm_probe.py").read_text(encoding="utf-8")
FIXTURE = FX.split('FIXTURE = r"""')[1].split('"""')[0]
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="ar-SA")
    pg = ctx.new_page()

    # --- FR-9 field coverage on detail ---
    pg.goto(f"{BASE}/dashboard?token={tok}#kmon/1", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    pg.evaluate(FIXTURE)
    pg.evaluate("() => { campaigns = window.__fx('default'); render(false); }")
    pg.wait_for_timeout(500)
    t = pg.inner_text("body")
    fields = {"الاسم/عنوان": "حملة العيادات" in t, "الخدمة": "الخدمة" in t,
              "تاريخ الإطلاق": bool(re.search(r"تاريخ", t)), "التصنيف": "التصنيف" in t,
              "عدد الجهات": ("حجم الجمهور" in t or "عدد الجهات" in t),
              "معرّف الحملة": ("معرّف" in t or "المعرّف" in t)}
    print("FR-9 side-panel fields present:", json.dumps(fields, ensure_ascii=False))
    print("spec-strip read-only notice:", "لا يقبل التعديل بعد الإطلاق" in t)
    tabs = pg.evaluate("""() => [].slice.call(document.querySelectorAll('[onclick*="crmSetDetailTab"]'))
        .map(function(e){ return (e.textContent||'').trim(); })""")
    print("FR-8 detail tabs:", json.dumps(tabs, ensure_ascii=False))

    # --- NFR-3: re-render of 400 campaigns ---
    pg.goto(f"{BASE}/dashboard?token={tok}#kmon", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    pg.evaluate(FIXTURE)
    pg.evaluate("() => { campaigns = window.__fx('many'); setCampTab('all'); render(false); }")
    pg.wait_for_timeout(400)
    for view in ["list", "group", "kanban"]:
        ms = pg.evaluate("""v => { crmSetView(v);
          var t = []; for (var i=0;i<7;i++){ var a=performance.now(); render(false); t.push(performance.now()-a); }
          t.sort(function(x,y){return x-y;}); return { median: Math.round(t[3]*10)/10, max: Math.round(t[6]*10)/10 }; }""", view)
        print(f"NFR-3 render 400 @{view}: median={ms['median']}ms max={ms['max']}ms (budget 200ms)")

    # --- detail render cost with many targets (contactRowsHtml N+1 at this commit) ---
    pg.evaluate("""() => { window.__fxBig = [{ id: 1, name: 'حملة كبيرة', product: 'التطعيمات', test: false,
        created_at: Date.now(), message: 'نص', targets: (function(){ var t=[]; for (var i=0;i<300;i++)
        t.push({ phone: '96650' + (100000+i), name: 'ج' + i }); return t; })() }]; }""")
    pg.evaluate("() => { campaigns = window.__fxBig; location.hash = 'kmon/1'; render(false); }")
    pg.wait_for_timeout(600)
    ms = pg.evaluate("""() => { var t=[]; for (var i=0;i<5;i++){ var a=performance.now(); render(false); t.push(performance.now()-a); }
        t.sort(function(x,y){return x-y;}); return { median: Math.round(t[2]*10)/10, max: Math.round(t[4]*10)/10,
        rows: document.querySelectorAll('.krow').length }; }""")
    print(f"detail with 300 targets: median={ms['median']}ms max={ms['max']}ms rows={ms['rows']}")
    pg.screenshot(path=str(OUT / "detail-300-targets.png"), full_page=False)
    b.close()
