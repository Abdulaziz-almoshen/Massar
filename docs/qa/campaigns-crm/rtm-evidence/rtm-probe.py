#!/usr/bin/env python3
"""Adversarial AC probe for campaigns-crm @645c5d8. Independent of scripts/qa-crm.py.

Every assertion reports the number of DOM nodes / matches it inspected, so a selector that
matches nothing can never be reported as a pass.
"""
import json, re, sys
from pathlib import Path

BASE = "http://localhost:8098"
OUT = Path("/private/tmp/claude-501/-Users-abdulaziz-Projects-Massar/6ce77bb9-3bcb-4e49-9b8b-eb5155bc2f5a/scratchpad/rtm-evidence")
ENV = Path("/private/tmp/claude-501/-Users-abdulaziz-Projects-Massar/6ce77bb9-3bcb-4e49-9b8b-eb5155bc2f5a/scratchpad/wt645/.env")

FIXTURE = r"""
window.__fx = function (kind) {
  var now = Date.now();
  var mk = function (id, name, product, test, nT, msg) {
    var t = [];
    for (var i = 0; i < nT; i++) t.push({ phone: "9665000" + (1000 + id * 20 + i), name: "جهة " + (i + 1) });
    return { id: id, name: name, product: product, test: test,
             created_at: now - id * 86400000, message: msg, targets: t };
  };
  if (kind === "empty") return [];
  if (kind === "one") return [mk(1, "حملة واحدة", "الإجازات المرضية", false, 3, "رسالة واحدة")];
  if (kind === "zero") return [mk(1, "حملة بلا جمهور", "الإجازات المرضية", false, 0, "نص بلا جمهور")];
  if (kind === "xss") return [mk(1, "حملة الحقن", "الإجازات المرضية", false, 2,
     "<img src=x onerror=\"window.__pwned=1\"> & <b>عريض</b> مرحبًا")];
  if (kind === "many") {
    /* 400 campaigns; exactly 137 carry product «التطعيمات» so a filter can match 137. */
    var a = [];
    for (var i = 1; i <= 400; i++)
      a.push(mk(i, "حملة رقم " + i, i <= 137 ? "التطعيمات" : "الإجازات المرضية", false, 4, "نص " + i));
    return a;
  }
  if (kind === "fifty") {
    /* 50 campaigns spanning all three BR-2 predicates, for the chip-vs-column identity test. */
    var a = [];
    for (var i = 1; i <= 50; i++) a.push(mk(i, "ح" + i, i % 2 ? "التطعيمات" : "الإجازات المرضية", i % 3 === 0, 4, "م" + i));
    return a;
  }
  return [mk(1, "حملة العيادات", "الإجازات المرضية", false, 6, "السلام عليكم"),
          mk(2, "بروفة داخلية", "التطعيمات", true, 2, "رسالة بروفة"),
          mk(3, "حملة بلا ردود", "التطعيمات", false, 5, "نص ثالث"),
          mk(4, "حملة رابعة", "التطعيمات", false, 5, "نص رابع"),
          mk(5, "حملة خامسة", "الإجازات المرضية", false, 5, "نص خامس"),
          mk(6, "حملة سادسة", "التطعيمات", false, 5, "نص سادس")];
};
"""

# In-page spy: records every fetch, optionally stubs the response so NOTHING reaches the server.
SPY = r"""
if (!window.__spy) {
  window.__spy = { calls: [], mode: "stub200" };
  window.__realFetch = window.fetch;
  window.fetch = function (u, o) {
    var url = typeof u === "string" ? u : (u && u.url) || String(u);
    window.__spy.calls.push({ url: url, method: (o && o.method) || "GET", body: (o && o.body) || null });
    if (window.__spy.mode === "stub500")
      return Promise.resolve({ ok: false, status: 500, json: function () { return Promise.resolve({}); },
                               text: function () { return Promise.resolve(""); } });
    return Promise.resolve({ ok: true, status: 200, json: function () { return Promise.resolve({ ok: true }); },
                             text: function () { return Promise.resolve("{}"); } });
  };
  window.__xhr = [];
  var _open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) { window.__xhr.push(m + " " + u); return _open.apply(this, arguments); };
  if (navigator.sendBeacon) {
    var _b = navigator.sendBeacon.bind(navigator);
    window.__beacon = [];
    navigator.sendBeacon = function (u, d) { window.__beacon.push(String(u)); return _b(u, d); };
  }
}
window.__spy.calls = [];
"""

R = []
def rec(ac, name, ok, detail, inspected=None):
    R.append({"ac": ac, "check": name, "ok": bool(ok), "inspected": inspected, "detail": detail})
    print(("  PASS " if ok else "  FAIL ") + f"[{ac}] {name} :: inspected={inspected} :: {detail}")


def token():
    return re.search(r"^ADMIN_TOKEN=(.+)$", ENV.read_text(encoding="utf-8"), re.M).group(1).strip()


def load(page, tok, kind, route="#kmon", setup=""):
    page.goto(f"{BASE}/dashboard?token={tok}{route}", wait_until="domcontentloaded")
    page.wait_for_timeout(2200)
    page.evaluate(FIXTURE)
    page.evaluate(SPY)
    page.evaluate("k => { campaigns = window.__fx(k); render(false); }", kind)
    page.wait_for_timeout(300)
    if setup:
        page.evaluate(setup)
        page.wait_for_timeout(350)


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    tok = token()
    net = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="ar-SA")
        ctx.on("request", lambda r: net.append(f"{r.method} {r.url}"))
        page = ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))

        # ---------------- AC-7 · zero-target renders «—», never ٠٪ ----------------
        print("\n== AC-7 zero-denominator ==")
        load(page, tok, "zero", route="#kmon/1")
        body = page.inner_text("body")
        page.screenshot(path=str(OUT / "ac7-detail-zero.png"), full_page=True)
        zeropct = body.count("٠٪")
        dash = body.count("—")
        rec("AC-7", "detail of a 0-target campaign contains no «٠٪»", zeropct == 0,
            f"«٠٪» count={zeropct}; «—» count={dash}", len(body))
        rec("AC-7", "detail renders at least one «—» rate placeholder", dash > 0, f"«—» count={dash}", len(body))
        # non-vacuity: the page must really be the zero-target campaign
        rec("AC-7", "non-vacuity: page is the zero-target campaign", "حملة بلا جمهور" in body,
            "campaign name present in body", len(body))
        load(page, tok, "zero", route="#kmon")
        lbody = page.inner_text("body")
        page.screenshot(path=str(OUT / "ac7-list-zero.png"), full_page=True)
        rec("AC-7", "list row of a 0-target campaign contains no «٠٪»", lbody.count("٠٪") == 0,
            f"«٠٪» count={lbody.count('٠٪')}; «لا جهات استهداف»={'لا جهات استهداف' in lbody}", len(lbody))
        # count how many nodes actually rendered a rate cell (selector non-vacuity)
        nrows = page.eval_on_selector_all(".krow", "e => e.length")
        rec("AC-7", "non-vacuity: rate cells exist to be wrong", nrows == 1, f".krow count={nrows}", nrows)

        # ---------------- AC-5 · 400 campaigns / select-all ----------------
        print("\n== AC-5 400-campaign cap + select-all ==")
        load(page, tok, "many")
        rows = page.eval_on_selector_all(".krow", "e => e.length")
        body = page.inner_text("body")
        rec("AC-5", "LIST_CAP rows render out of 400", rows == 60, f".krow count={rows} (expect 60)", rows)
        rec("AC-5", "cap footer declares the true total ٤٠٠", "٤٠٠" in body,
            f"footer text present={'ضيّق بالبحث' in body}", len(body))
        # apply the filter that matches exactly 137
        page.evaluate("() => { campQ = 'التطعيمات'; render(false); }")
        page.wait_for_timeout(300)
        matched = page.evaluate("() => crmFiltered().length")
        rows2 = page.eval_on_selector_all(".krow", "e => e.length")
        body2 = page.inner_text("body")
        page.screenshot(path=str(OUT / "ac5-filter-137.png"), full_page=True)
        rec("AC-5", "filter matches exactly 137", matched == 137, f"crmFiltered().length={matched}", matched)
        rec("AC-5", "still only LIST_CAP rows render", rows2 == 60, f".krow count={rows2}", rows2)
        has_all = page.evaluate("() => typeof window.crmSelectAllMatching === 'function' || /تحديد المطابقين/.test(document.body.innerText)")
        rec("AC-5", "«تحديد المطابقين» control exists (FR-6)", has_all,
            "no crmSelectAllMatching fn and no «تحديد المطابقين» string in the DOM", None)
        # what the product DOES do on select-page
        page.evaluate("() => crmTogglePage()")
        page.wait_for_timeout(300)
        selbody = page.inner_text("body")
        nsel = page.evaluate("() => crmSelIds().length")
        page.screenshot(path=str(OUT / "ac5-selectpage-alert.png"), full_page=True)
        states_true_total = "١٣٧" in selbody
        rec("AC-5", "select-page selects only the rendered rows", nsel == 60, f"crmSelIds().length={nsel}", nsel)
        rec("AC-5", "the true match count ١٣٧ is stated to the operator", states_true_total,
            f"alert text contains ١٣٧={states_true_total}; body has «غير مشمول»={'غير مشمول' in selbody}", len(selbody))

        # ---------------- AC-4 · drag refusal / exactly one POST ----------------
        print("\n== AC-4 drag ==")
        # (a) التصنيف board — drag SHOULD write exactly one POST
        load(page, tok, "default", setup='crmSetView("kanban"); crmSetGroup("class");')
        page.evaluate(SPY)
        ncols = page.eval_on_selector_all(".kcol", "e => e.length")
        ndrag = page.eval_on_selector_all('.kcard[draggable="true"]', "e => e.length")
        ndrop = page.eval_on_selector_all(".kcol[ondrop]", "e => e.length")
        page.screenshot(path=str(OUT / "ac4-board-class.png"), full_page=True)
        rec("AC-4", "non-vacuity: التصنيف board rendered columns", ncols >= 2, f".kcol={ncols}", ncols)
        rec("AC-4", "cards are draggable on التصنيف", ndrag > 0, f'.kcard[draggable=true]={ndrag}', ndrag)
        rec("AC-4", "columns accept a drop on التصنيف", ndrop >= 2, f".kcol[ondrop]={ndrop}", ndrop)
        # simulate: campaign 1 (real) dropped into تجريبية
        page.evaluate("""() => { window.__spy.calls = [];
          crmDragStart({ dataTransfer: {} }, 1);
          crmDrop({ preventDefault: function(){} }, "تجريبية", null); }""")
        page.wait_for_timeout(400)
        calls = page.evaluate("() => window.__spy.calls")
        posts = [c for c in calls if "/admin/campaign/test" in c["url"]]
        rec("AC-4", "drag onto التصنيف issues exactly one POST /admin/campaign/test",
            len(calls) == 1 and len(posts) == 1 and posts[0]["method"] == "POST",
            f"spy calls={json.dumps(calls, ensure_ascii=False)}", len(calls))
        # (b) product board — must be read-only
        page.evaluate('crmSetGroup("product"); render(false);')
        page.wait_for_timeout(350)
        ncols_p = page.eval_on_selector_all(".kcol", "e => e.length")
        ndrag_p = page.eval_on_selector_all('.kcard[draggable="true"]', "e => e.length")
        ndrop_p = page.eval_on_selector_all(".kcol[ondrop]", "e => e.length")
        ncards_p = page.eval_on_selector_all(".kcard", "e => e.length")
        page.screenshot(path=str(OUT / "ac4-board-product.png"), full_page=True)
        rec("AC-4", "non-vacuity: product board rendered cards", ncards_p > 0 and ncols_p >= 2,
            f".kcol={ncols_p} .kcard={ncards_p}", ncards_p)
        rec("AC-4", "product board: zero draggable cards", ndrag_p == 0, f'draggable={ndrag_p}', ncards_p)
        rec("AC-4", "product board: zero drop targets", ndrop_p == 0, f"[ondrop]={ndrop_p}", ncols_p)
        page.evaluate("() => { window.__spy.calls = []; }")
        page.evaluate("""() => { var c = document.querySelector('.kcard');
          ['dragstart','dragover','drop'].forEach(function(t){
            var e = new Event(t, {bubbles:true, cancelable:true});
            try { Object.defineProperty(e,'dataTransfer',{value:{setData:function(){},effectAllowed:''}}); } catch(x){}
            c.dispatchEvent(e); }); }""")
        page.wait_for_timeout(400)
        calls_p = page.evaluate("() => window.__spy.calls")
        rec("AC-4", "product board: a real drag gesture issues ZERO requests", len(calls_p) == 0,
            f"spy calls={json.dumps(calls_p, ensure_ascii=False)}", 1)
        # (c) حالة الأداء board — has a column LITERALLY named «تجريبية»; must also be read-only
        page.evaluate('crmSetGroup("perf"); render(false);')
        page.wait_for_timeout(350)
        ndrag_f = page.eval_on_selector_all('.kcard[draggable="true"]', "e => e.length")
        ndrop_f = page.eval_on_selector_all(".kcol[ondrop]", "e => e.length")
        cols_f = page.eval_on_selector_all(".kcol", "e => e.map(x => x.getAttribute('data-col'))")
        page.screenshot(path=str(OUT / "ac4-board-perf.png"), full_page=True)
        rec("AC-4", "perf board is read-only despite a «تجريبية» column",
            ndrag_f == 0 and ndrop_f == 0,
            f"draggable={ndrag_f} ondrop={ndrop_f} cols={json.dumps(cols_f, ensure_ascii=False)}", len(cols_f))
        # adversarial: call the handler directly as if the guard were bypassed
        page.evaluate("() => { window.__spy.calls = []; }")
        page.evaluate("""() => { crmDragStart({dataTransfer:{}}, 3);
          crmDrop({preventDefault:function(){}}, "فيها ردود", null); }""")
        page.wait_for_timeout(300)
        calls_f = page.evaluate("() => window.__spy.calls")
        rec("AC-4", "DEPTH: crmDrop invoked with a non-التصنيف column name",
            len(calls_f) == 0,
            f"handler is not board-guarded internally; calls={json.dumps(calls_f, ensure_ascii=False)}", 1)

        # ---------------- AC-6 · bulk reclassify: N calls, zero outbound ----------------
        print("\n== AC-6 bulk ==")
        load(page, tok, "default", setup="""
          [1,3,4,5,6].forEach(function(i){ crmSel[i] = true; }); render(false);""")
        page.evaluate(SPY)
        nsel6 = page.evaluate("() => crmSelIds().length")
        page.screenshot(path=str(OUT / "ac6-selected-5.png"), full_page=True)
        net_before = len(net)
        page.evaluate("() => { window.__spy.calls = []; window.__spy.mode='stub200'; }")
        page.evaluate("async () => { await crmBulkClass(true); }")
        page.wait_for_timeout(600)
        calls6 = page.evaluate("() => window.__spy.calls")
        xhr6 = page.evaluate("() => window.__xhr || []")
        bec6 = page.evaluate("() => window.__beacon || []")
        body6 = page.inner_text("body")
        page.screenshot(path=str(OUT / "ac6-bulk-ok.png"), full_page=True)
        urls6 = sorted(set(c["url"] for c in calls6))
        rec("AC-6", "non-vacuity: 5 campaigns were selected", nsel6 == 5, f"crmSelIds().length={nsel6}", nsel6)
        rec("AC-6", "bulk reclassify of 5 fires exactly 5 calls", len(calls6) == 5,
            f"calls={len(calls6)} urls={json.dumps(urls6, ensure_ascii=False)}", len(calls6))
        rec("AC-6", "every call goes to /admin/campaign/test with POST",
            all(c["url"] == "/admin/campaign/test" and c["method"] == "POST" for c in calls6) and len(calls6) > 0,
            f"{json.dumps(calls6, ensure_ascii=False)[:400]}", len(calls6))
        rec("AC-6", "ZERO client requests to any other path (no send)",
            all(c["url"] == "/admin/campaign/test" for c in calls6) and not xhr6 and not bec6,
            f"other fetch={[c['url'] for c in calls6 if c['url'] != '/admin/campaign/test']} xhr={xhr6} beacon={bec6}",
            len(calls6))
        gup = [c for c in calls6 if re.search(r"gupshup|/send|message|outbound", c["url"], re.I)]
        rec("AC-6", "ZERO gupshup/send-shaped paths", len(gup) == 0, f"matches={gup}", len(calls6))
        rec("AC-6", "success line reports the count", "غُيّر تصنيف" in body6,
            f"alert present; ٥ in body={'٥' in body6}", len(body6))
        # forced 500 → partial-failure count
        load(page, tok, "default", setup="""
          [1,3,4,5,6].forEach(function(i){ crmSel[i] = true; }); render(false);""")
        page.evaluate(SPY)
        page.evaluate("() => { window.__spy.mode = 'stub500'; window.__spy.calls = []; }")
        page.evaluate("async () => { await crmBulkClass(true); }")
        page.wait_for_timeout(700)
        calls500 = page.evaluate("() => window.__spy.calls")
        body500 = page.inner_text("body")
        page.screenshot(path=str(OUT / "ac6-bulk-500.png"), full_page=True)
        rec("AC-6", "forced 500: still exactly 5 calls, no retry storm", len(calls500) == 5,
            f"calls={len(calls500)}", len(calls500))
        rec("AC-6", "forced 500: failed count surfaced to the operator",
            "تعذّر" in body500, f"body contains «تعذّر»={'تعذّر' in body500}; «٥»={'٥' in body500}", len(body500))

        # ---------------- AC-3 · chip == board column over 50 fixtures ----------------
        print("\n== AC-3 one function ==")
        load(page, tok, "fifty")
        chip_map = page.evaluate("""() => {
          var out = {};
          document.querySelectorAll('.krow').forEach(function (r) {
            var nm = r.querySelector('div[style*="font-weight:700"]');
            var chip = r.querySelector('.chip');
            if (nm && chip) out[nm.textContent.trim()] = chip.textContent.trim();
          });
          return out; }""")
        page.evaluate('crmSetView("kanban"); crmSetGroup("perf"); render(false);')
        page.wait_for_timeout(400)
        col_map = page.evaluate("""() => {
          var out = {};
          document.querySelectorAll('.kcol').forEach(function (col) {
            var k = col.getAttribute('data-col');
            col.querySelectorAll('.kcard .nm').forEach(function (n) { out[n.textContent.trim()] = k; });
          });
          return out; }""")
        page.screenshot(path=str(OUT / "ac3-board-perf-50.png"), full_page=True)
        shared = set(chip_map) & set(col_map)
        mism = {k: (chip_map[k], col_map[k]) for k in shared if chip_map[k] != col_map[k]}
        rec("AC-3", "non-vacuity: chips and cards both harvested", len(shared) >= 40,
            f"chips={len(chip_map)} cards={len(col_map)} shared={len(shared)}", len(shared))
        rec("AC-3", "chip label == board column for every shared campaign", len(mism) == 0,
            f"mismatches={json.dumps(mism, ensure_ascii=False)[:300]}", len(shared))
        labels = sorted(set(col_map.values()))
        rec("AC-3", "board labels are exactly the BR-2 three",
            set(labels) <= {"تجريبية", "فيها ردود", "بلا ردود بعد"},
            f"labels={json.dumps(labels, ensure_ascii=False)}", len(labels))
        allbody = page.inner_text("body")
        rec("AC-3", "«مكتملة» absent from every campaign surface", "مكتملة" not in allbody,
            f"occurrences on #kmon board={allbody.count('مكتملة')}", len(allbody))

        # ---------------- AC-1 · filter + sort ----------------
        print("\n== AC-1 filter + sort ==")
        load(page, tok, "many")
        page.evaluate("""() => { campQ = 'التطعيمات'; setCampSort({ value: 'replies' }); }""")
        page.wait_for_timeout(400)
        got = page.evaluate("""() => {
          var rows = [].slice.call(document.querySelectorAll('.krow'));
          return rows.map(function (r) {
            var cells = r.children;
            return { product: cells[2] ? cells[2].textContent.trim() : null }; }); }""")
        srv = page.evaluate("() => crmFiltered().map(function(x){ return { p: x.c.product, r: x.st.replied }; })")
        page.screenshot(path=str(OUT / "ac1-filter-sort.png"), full_page=True)
        offp = [g for g in got if g["product"] != "التطعيمات"]
        desc = all(srv[i]["r"] >= srv[i + 1]["r"] for i in range(len(srv) - 1))
        rec("AC-1", "non-vacuity: rows rendered under the filter", len(got) == 60, f"rows={len(got)}", len(got))
        rec("AC-1", "every rendered row matches the filtered product", len(offp) == 0,
            f"off-product rows={len(offp)}", len(got))
        rec("AC-1", "sort «الأكثر ردودًا» is non-increasing in replied", desc,
            f"n={len(srv)} first5={[x['r'] for x in srv[:5]]}", len(srv))
        rec("AC-1", "structured FR-2 condition builder present",
            page.evaluate("() => /فلترة/.test(document.body.innerText)"),
            "no «فلترة» condition-builder control in the bar; filtering is free-text search + class tab", None)

        # ---------------- AC-8 / AC-9 · detail message + read-only strip ----------------
        print("\n== AC-8/AC-9 detail ==")
        load(page, tok, "xss", route="#kmon/1")
        page.evaluate("() => { crmMsgOpen = true; render(false); }")
        page.wait_for_timeout(300)
        body8 = page.inner_text("body")
        pwned = page.evaluate("() => !!window.__pwned")
        imgs = page.eval_on_selector_all("#view img[src='x']", "e => e.length")
        page.screenshot(path=str(OUT / "ac8-message-escaped.png"), full_page=True)
        raw = '<img src=x onerror="window.__pwned=1"> & <b>عريض</b> مرحبًا'
        rec("AC-8", "camp.message rendered verbatim as text", raw in body8,
            f"verbatim match={raw in body8}", len(body8))
        rec("AC-8", "message is escaped, not executed", (not pwned) and imgs == 0,
            f"window.__pwned={pwned}; injected img nodes={imgs}", len(body8))
        load(page, tok, "default", route="#kmon/1")
        strip = page.evaluate("""() => {
          var v = document.querySelector('#view') || document.body;
          return { inputs: v.querySelectorAll('input:not([type=checkbox])').length,
                   textareas: v.querySelectorAll('textarea').length,
                   selects: v.querySelectorAll('select').length,
                   checkboxes: v.querySelectorAll('input[type=checkbox]').length,
                   saveish: [].slice.call(v.querySelectorAll('button')).filter(function(b){
                     return /حفظ|تعديل|احفظ/.test(b.textContent); }).length,
                   buttons: v.querySelectorAll('button').length,
                   classCtl: [].slice.call(v.querySelectorAll('button,[onclick]')).filter(function(b){
                     return /setCampClass/.test(b.getAttribute('onclick')||''); }).length }; }""")
        page.screenshot(path=str(OUT / "ac9-spec-strip.png"), full_page=True)
        rec("AC-9", "non-vacuity: detail view has controls to inspect", strip["buttons"] > 0,
            f"{json.dumps(strip)}", strip["buttons"])
        rec("AC-9", "no free-text input / textarea / save control in detail",
            strip["inputs"] == 0 and strip["textareas"] == 0 and strip["saveish"] == 0, f"{json.dumps(strip)}",
            strip["buttons"])
        rec("AC-9", "التصنيف is the only mutation control on detail", strip["classCtl"] >= 1,
            f"setCampClass controls={strip['classCtl']}", strip["buttons"])

        # ---------------- AC-2 · rendered columns ⊆ FR-5 closed set ----------------
        print("\n== AC-2 columns ==")
        load(page, tok, "default")
        heads = page.evaluate("""() => {
          var g = document.querySelector('.tblwrap div[style*="grid-template-columns"]');
          return g ? [].slice.call(g.children).map(function(c){ return c.textContent.trim(); }) : []; }""")
        allowed = {"", "الحملة", "الخدمة", "الحالة", "الجمهور", "مشاهدة", "ردود", "التقدّم",
                   "وصلت", "شوهدت", "ردّوا", "جهات مهتمة", "فشلت", "التصنيف", "التاريخ"}
        bad = [h for h in heads if h not in allowed]
        rec("AC-2", "non-vacuity: header row harvested", len([h for h in heads if h]) >= 6,
            f"headers={json.dumps(heads, ensure_ascii=False)}", len(heads))
        rec("AC-2", "every rendered column ∈ FR-5 closed set", len(bad) == 0,
            f"unexpected={json.dumps(bad, ensure_ascii=False)}", len(heads))

        # ---------------- AC-14 · empty / single ----------------
        print("\n== AC-14 edges ==")
        load(page, tok, "empty")
        e_body = page.inner_text("body")
        e_bar = page.eval_on_selector_all(".crmbar", "e => e.length")
        page.screenshot(path=str(OUT / "ac14-empty.png"), full_page=True)
        rec("AC-14", "empty: ViewControls bar hidden", e_bar == 0,
            f".crmbar count={e_bar}; empty landmark={'لا حملات بعد' in e_body}", e_bar)
        rec("AC-14", "non-vacuity: empty state actually rendered", "لا حملات بعد" in e_body,
            f"chars={len(e_body)}", len(e_body))
        load(page, tok, "one")
        o_body = page.inner_text("body")
        o_rows = page.eval_on_selector_all(".krow", "e => e.length")
        page.screenshot(path=str(OUT / "ac14-one.png"), full_page=True)
        rec("AC-14", "single: exactly one row, no cap footer", o_rows == 1 and "ضيّق بالبحث" not in o_body,
            f"rows={o_rows}; cap footer={'ضيّق بالبحث' in o_body}", o_rows)
        page.evaluate('crmSetView("kanban"); crmSetGroup("product"); render(false);')
        page.wait_for_timeout(350)
        o_cols = page.eval_on_selector_all(".kcol", "e => e.length")
        o_sparse = page.evaluate("() => /التجميع لا يضيف شيئًا هنا|لوحة/.test(document.body.innerText)")
        page.screenshot(path=str(OUT / "ac14-one-board.png"), full_page=True)
        rec("AC-14", "single: board shows one column, no invented empties", o_cols <= 1,
            f".kcol={o_cols}; degraded-to-list notice={o_sparse}", o_cols)

        rec("HEALTH", "zero pageerrors across the whole probe", len(errs) == 0, f"errors={errs[:3]}", len(errs))

        # ---------------- AC-12 · overflow at 3 viewports x 3 views ----------------
        print("\n== AC-12 overflow ==")
        ctx.close()
        for vp, w, h in [("375x812", 375, 812), ("768x1024", 768, 1024), ("1440x900", 1440, 900)]:
            c2 = b.new_context(viewport={"width": w, "height": h}, locale="ar-SA")
            pg = c2.new_page()
            for view, setup in [("list", ""), ("group", 'crmSetView("group");'),
                                ("kanban", 'crmSetView("kanban");')]:
                load(pg, tok, "many", setup=setup)
                m = pg.evaluate("""() => {
                  var s = document.scrollingElement;
                  var wide = [].slice.call(document.querySelectorAll('body *')).filter(function (e) {
                    var r = e.getBoundingClientRect();
                    return r.right > s.clientWidth + 2 && getComputedStyle(e).position !== 'fixed'; });
                  return { over: s.scrollWidth - s.clientWidth, cw: s.clientWidth,
                           bodyOver: document.body.scrollWidth - document.body.clientWidth,
                           nWide: wide.length,
                           wideTop: wide.slice(0,3).map(function(e){ return e.className || e.tagName; }),
                           scrollers: document.querySelectorAll('.ms-scroll').length }; }""")
                pg.screenshot(path=str(OUT / f"ac12-{view}@{vp}.png"), full_page=False)
                rec("AC-12", f"{view}@{vp}: page does not scroll horizontally", m["over"] <= 1,
                    f"scrollWidth-clientWidth={m['over']}px body={m['bodyOver']}px "
                    f"escaping-nodes={m['nWide']} {m['wideTop']} scrollers={m['scrollers']}", m["cw"])
            c2.close()
        b.close()

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "probe-results.json").write_text(json.dumps(R, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "network.log").write_text("\n".join(net), encoding="utf-8")
    bad = [r for r in R if not r["ok"]]
    print(f"\n[probe] {len(R)} assertions, {len(bad)} failed")
    for x in bad:
        print(f"  FAIL [{x['ac']}] {x['check']} :: {x['detail'][:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
