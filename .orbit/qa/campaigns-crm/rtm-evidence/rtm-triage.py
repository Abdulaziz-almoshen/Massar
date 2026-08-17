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
    pg.goto(f"{BASE}/dashboard?token={tok}#kmon", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    pg.evaluate(FIXTURE)
    pg.evaluate("() => { campaigns = window.__fx('fifty'); render(false); }")
    pg.wait_for_timeout(400)
    print("== AC-3 triage: why only 34 rows? ==")
    print(json.dumps(pg.evaluate("""() => ({
      campTab: typeof campTab !== 'undefined' ? campTab : 'undef',
      campQ: typeof campQ !== 'undefined' ? campQ : 'undef',
      crmView: typeof crmView !== 'undefined' ? crmView : 'undef',
      total: campaigns.length,
      filtered: crmFiltered().length,
      rows: document.querySelectorAll('.krow').length,
      chips: document.querySelectorAll('.krow .chip').length,
      ls: Object.keys(localStorage).map(function(k){ return k + '=' + localStorage.getItem(k); })
    })""" ), ensure_ascii=False))
    # force campTab=all and re-measure
    pg.evaluate("() => { setCampTab('all'); }")
    pg.wait_for_timeout(400)
    m = pg.evaluate("""() => {
      var chips = {};
      document.querySelectorAll('.krow').forEach(function (r) {
        var nm = r.querySelector('div[style*="font-weight:700"]');
        var c = r.querySelector('.chip');
        if (nm && c) chips[nm.textContent.trim()] = c.textContent.trim(); });
      return { campTab: campTab, rows: document.querySelectorAll('.krow').length,
               nchips: Object.keys(chips).length, chips: chips }; }""")
    print("after setCampTab('all'): rows=%s chips=%s" % (m["rows"], m["nchips"]))
    pg.evaluate("() => { crmSetView('kanban'); crmSetGroup('perf'); render(false); }")
    pg.wait_for_timeout(500)
    cols = pg.evaluate("""() => {
      var out = {}, per = {};
      document.querySelectorAll('.kcol').forEach(function (col) {
        var k = col.getAttribute('data-col');
        per[k] = col.querySelectorAll('.kcard').length;
        col.querySelectorAll('.kcard .nm').forEach(function (n) { out[n.textContent.trim()] = k; }); });
      return { per: per, map: out, n: Object.keys(out).length }; }""")
    print("board per-column card counts:", json.dumps(cols["per"], ensure_ascii=False), "cards mapped:", cols["n"])
    mism = {k: (m["chips"][k], cols["map"][k]) for k in set(m["chips"]) & set(cols["map"])
            if m["chips"][k] != cols["map"][k]}
    print("AC-3 shared:", len(set(m["chips"]) & set(cols["map"])), "MISMATCHES:", json.dumps(mism, ensure_ascii=False))
    pg.screenshot(path=str(OUT / "ac3-board-50-all.png"), full_page=True)

    print("\n== AC-9 triage: what is the 1 input on detail? ==")
    pg.goto(f"{BASE}/dashboard?token={tok}#kmon/1", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    pg.evaluate(FIXTURE)
    pg.evaluate("() => { campaigns = window.__fx('default'); render(false); }")
    pg.wait_for_timeout(500)
    print(json.dumps(pg.evaluate("""() => {
      var v = document.querySelector('#view') || document.body;
      return {
        inputs: [].slice.call(v.querySelectorAll('input:not([type=checkbox])')).map(function(i){
          return { type: i.type, id: i.id, cls: i.className, ph: i.placeholder,
                   oninput: i.getAttribute('oninput'), onchange: i.getAttribute('onchange'),
                   inSpec: !!i.closest('.specstrip, .spec'), html: i.outerHTML.slice(0,180) }; }),
        mutators: [].slice.call(v.querySelectorAll('[onclick]')).map(function(e){
          return (e.getAttribute('onclick')||'').slice(0,90); })
          .filter(function(s){ return /setCampClass|fetch|POST|Class/i.test(s); }),
        allOnclickSample: [].slice.call(v.querySelectorAll('[onclick]')).length
      }; }""" ), ensure_ascii=False, indent=1))
    pg.screenshot(path=str(OUT / "ac9-detail-full.png"), full_page=True)
    print("\n== AC-9: is there a التصنيف control on detail at all? ==")
    print(json.dumps(pg.evaluate("""() => {
      var v = document.querySelector('#view') || document.body;
      return { hasClassWord: /التصنيف/.test(v.innerText),
               ctl: [].slice.call(v.querySelectorAll('button,[onclick]')).filter(function(e){
                 return /التصنيف|تجريبية|فعلية/.test(e.textContent||''); }).map(function(e){
                 return { t: (e.textContent||'').trim().slice(0,40), on: (e.getAttribute('onclick')||'').slice(0,80) }; }) }; }""" ), ensure_ascii=False, indent=1))
    b.close()
