#!/usr/bin/env python3
"""crm-record delivery evidence — pixel captures, design-plan geometry, tokens, a11y, console.

LOCAL by construction: the change is not deployed, so production cannot be screenshotted. The
engine under test is a local boot of commit 388832f against a real Postgres 16, with the WhatsApp
send path dead twice over (see harness/boot.sh). No message is sent, to any number, for any reason.
"""
import json, sys
from pathlib import Path

BASE = "http://127.0.0.1:8188"
TOK  = "qa-admin-token"
OUT  = Path("/Users/abdulaziz/Projects/Massar/.orbit/artifacts/crm-record/qa")
RICH, EMPTY, READ = "966500000850", "966500000861", "966500000862"
GATE_VP = [("375x812", 375, 812), ("768x1024", 768, 1024), ("1440x900", 1440, 900)]

results = {"captures": [], "design_checks": [], "tokens": [], "a11y": [], "console": []}


def open_record(page, phone, wait=4200):
    page.goto(f"{BASE}/dashboard?token={TOK}#customer/{phone}", wait_until="domcontentloaded")
    page.wait_for_timeout(wait)


def main():
    from playwright.sync_api import sync_playwright
    which = sys.argv[1] if len(sys.argv) > 1 else "actual"
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ---------- 1. gate captures at the three required viewports ----------
        for name, w, h in GATE_VP:
            ctx = browser.new_context(viewport={"width": w, "height": h}, locale="ar-SA",
                                      reduced_motion="reduce")
            page = ctx.new_page()
            errs = []
            THIRD = ("fonts.gstatic.com", "fonts.googleapis.com")
            def tp(m):
                try: loc = (m.location or {}).get("url", "") or ""
                except Exception: loc = ""
                return any(x in f"{m.text} {loc}" for x in THIRD)
            page.on("console", lambda m: None if (m.type != "error" or tp(m)) else errs.append("console: " + m.text[:160]))
            page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            open_record(page, RICH)
            shot = OUT / "visual" / which / f"customer@{name}.png"
            shot.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(shot), full_page=True)
            txt = page.inner_text("body")
            ov = page.evaluate("() => document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth")
            results["captures"].append({"route": "#customer/<phone>", "viewport": name,
                "file": str(shot), "chars": len(txt), "h_overflow_px": ov,
                "smoke_landmark_present": "ما تكتبه هنا لا يستطيع المساعد تغييره" in txt,
                "console_errors": errs[:]})
            results["console"] += errs
            ctx.close()

        # ---------- 2. design-plan §6 acceptance checks ----------
        # §6.1 @1440
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, locale="ar-SA", reduced_motion="reduce")
        page = ctx.new_page(); errs = []
        page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        open_record(page, RICH)
        m = page.evaluate("""() => {
          const crec = document.querySelector('.crec');
          const cs = getComputedStyle(crec);
          const panel = crec.children[0], main = crec.querySelector('.crecmain');
          const pr = panel.getBoundingClientRect(), mr = main.getBoundingClientRect();
          const marks = [...panel.querySelectorAll('.pm')].filter(e => e.offsetParent !== null);
          // the ROW marks only: the legend also uses .pm. Row marks are direct children of .frow.
          const rowMarks = [...panel.querySelectorAll('.frow > .pm')];
          const xs = rowMarks.map(e => Math.round(e.getBoundingClientRect().right * 100) / 100);
          return {
            dir: document.documentElement.dir || getComputedStyle(document.body).direction,
            gridCols: cs.gridTemplateColumns, gap: cs.columnGap,
            panelWidth: Math.round(pr.width * 100) / 100,
            panelRight: Math.round(pr.right), mainRight: Math.round(mr.right),
            panelIsRightmost: pr.right > mr.right,
            rowMarkCount: rowMarks.length, markRightEdges: xs,
            markSpreadPx: xs.length ? Math.round((Math.max(...xs) - Math.min(...xs)) * 100) / 100 : null,
            allMarkCount: marks.length,
            hOverflow: document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth,
            stageOrdinalPresent: /\\d+\\s*من\\s*[٦6]/.test(document.body.innerText),
            arabicOrdinalPresent: document.body.innerText.includes('من ٦'),
            salesRailPresent: typeof window.vSalesPath !== 'undefined',
            marks: [...panel.querySelectorAll('.frow > .pm')].map(e => e.className),
          };
        }""")
        results["design_checks"].append({"check": "§6.1 @1440x900", **m})

        # ---------- 3. token assertions vs DESIGN.md ----------
        tok = page.evaluate("""() => {
          const g = (sel, props) => { const e = document.querySelector(sel); if (!e) return {missing: sel};
            const cs = getComputedStyle(e); const o = {}; props.forEach(p => o[p] = cs[p]); return o; };
          const panel = document.querySelector('.crec').children[0];
          const firstRow = panel.querySelector('.frow');
          const lab = panel.querySelector('.flab'), val = panel.querySelector('.fval'),
                sig = panel.querySelector('.sig'), pen = panel.querySelector('.pen'),
                rd  = panel.querySelector('.rdrow'), lg = panel.querySelector('.plgnd');
          const cs = e => e ? getComputedStyle(e) : null;
          const box = e => { const c = cs(e); return c ? {w: c.width, h: c.height, bg: c.backgroundColor,
            border: c.borderTopWidth + ' ' + c.borderTopStyle + ' ' + c.borderTopColor,
            radius: c.borderTopLeftRadius, opacity: c.opacity, marginTop: c.marginTop} : null; };
          return {
            'pm-h': box(panel.querySelector('.pm-h')),
            'pm-a': box(panel.querySelector('.pm-a')),
            'pm-i': box(panel.querySelector('.pm-i')),
            'pm-m': box(panel.querySelector('.pm-m')),
            'rdrow': rd ? {bg: cs(rd).backgroundColor, margin: cs(rd).marginLeft + '/' + cs(rd).marginRight,
                           padding: cs(rd).paddingTop + ' ' + cs(rd).paddingLeft, radius: cs(rd).borderTopLeftRadius} : null,
            'flab': lab ? {size: cs(lab).fontSize, weight: cs(lab).fontWeight, color: cs(lab).color} : null,
            'fval(human)': val ? {size: cs(val).fontSize, weight: cs(val).fontWeight, color: cs(val).color} : null,
            'fval-a(reading)': (() => { const e = panel.querySelector('.fval-a'); return e ? {size: cs(e).fontSize, weight: cs(e).fontWeight, color: cs(e).color} : null; })(),
            'fval-m(missing)': (() => { const e = panel.querySelector('.fval-m'); return e ? {size: cs(e).fontSize, weight: cs(e).fontWeight, color: cs(e).color} : null; })(),
            'sig': sig ? {size: cs(sig).fontSize, weight: cs(sig).fontWeight, color: cs(sig).color} : null,
            'quote': (() => { const e = panel.querySelector('.quote'); return e ? {size: cs(e).fontSize, lh: cs(e).lineHeight, color: cs(e).color} : null; })(),
            'plgnd': lg ? {size: cs(lg).fontSize, weight: cs(lg).fontWeight, color: cs(lg).color} : null,
            'pen': pen ? {w: cs(pen).width, h: cs(pen).height, opacity: cs(pen).opacity, insetEnd: cs(pen).insetInlineEnd, top: cs(pen).top} : null,
            'frow': firstRow ? {padding: cs(firstRow).paddingTop + '/' + cs(firstRow).paddingBottom, border: cs(firstRow).borderBottomWidth + ' ' + cs(firstRow).borderBottomColor} : null,
            'add': (() => { const e = document.querySelector('.add'); return e ? {border: cs(e).borderTopWidth + ' ' + cs(e).borderTopStyle + ' ' + cs(e).borderTopColor, color: cs(e).color, bg: cs(e).backgroundColor} : null; })(),
            'confirm-pill': (() => { const e = panel.querySelector('.cbar .btn'); return e ? {size: cs(e).fontSize, weight: cs(e).fontWeight, padding: cs(e).paddingTop + ' ' + cs(e).paddingLeft, radius: cs(e).borderTopLeftRadius, minH: cs(e).minHeight, rectH: Math.round(e.getBoundingClientRect().height)} : null; })(),
            'crecmain': (() => { const e = document.querySelector('.crecmain'); return e ? {cols: cs(e).gridTemplateColumns, gap: cs(e).gap} : null; })(),
          };
        }""")
        results["tokens"].append({"viewport": "1440x900", "computed": tok})

        # a11y at 1440
        a11y = page.evaluate("""() => {
          const panel = document.querySelector('.crec').children[0];
          const pens = [...panel.querySelectorAll('.pen')];
          const btns = [...panel.querySelectorAll('button')];
          return {
            pencilCount: pens.length,
            pencilsWithAriaLabel: pens.filter(b => (b.getAttribute('aria-label') || '').trim().length > 0).length,
            buttonsWithoutAccessibleName: btns.filter(b => !((b.getAttribute('aria-label') || '') + b.textContent).trim()).length,
            focusVisibleRule: [...document.styleSheets].some(s => { try { return [...s.cssRules].some(r => (r.cssText || '').includes(':focus-visible') && (r.cssText||'').includes('#2E7D77')); } catch (e) { return false; } }),
            colourIsNotSoleCarrier: (() => {
              const words = ['سجّلها','أكّدها','قراءة المساعد','من ملف الاستيراد'];
              const rows = [...panel.querySelectorAll('.frow')];
              const marked = rows.filter(r => r.querySelector('.pm-h,.pm-a,.pm-i'));
              return marked.every(r => words.some(w => r.innerText.includes(w)));
            })(),
            legendWords: [...panel.querySelectorAll('.plgnd .i')].map(e => e.innerText.trim()),
          };
        }""")
        results["a11y"].append({"viewport": "1440x900", **a11y, "pageerrors": errs[:]})
        ctx.close()

        # §6.2 @900
        ctx = browser.new_context(viewport={"width": 900, "height": 1200}, locale="ar-SA", reduced_motion="reduce")
        page = ctx.new_page(); open_record(page, RICH)
        m9 = page.evaluate("""() => {
          const crec = document.querySelector('.crec');
          const cols = getComputedStyle(crec).gridTemplateColumns;
          const t = document.body.innerText;
          const order = [];
          const idx = s => t.indexOf(s);
          return {
            gridCols: cols, oneColumn: cols.split(' ').length === 1,
            i_identity: idx('د. سارة العتيبي'), i_status: idx('سجّل النتيجة الفعلية'),
            i_panel: idx('ملف العميل'), i_ai: idx('فهم المساعد'), i_timeline: idx('سجل التفاعل'),
            stageNameOccurrences: (t.match(/عرض الحل/g) || []).length,
            salesRailPresent: typeof window.vSalesPath !== 'undefined',
            ordinalPresent: /من\\s*[٦6]/.test(t),
            hOverflow: document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth,
          };
        }""")
        m9["order_ok"] = (m9["i_panel"] > m9["i_status"] > 0) and (m9["i_ai"] > m9["i_panel"]) and (m9["i_timeline"] > m9["i_ai"])
        results["design_checks"].append({"check": "§6.2 @900x1200", **m9})
        ctx.close()

        # §6.3 @390
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, locale="ar-SA",
                                  reduced_motion="reduce", has_touch=True, is_mobile=True)
        page = ctx.new_page(); open_record(page, RICH)
        m3 = page.evaluate("""() => {
          const panel = document.querySelector('.crec').children[0];
          const trunc = [...panel.querySelectorAll('.flab,.fval,.fval-a,.fval-m,.sig,.quote')]
            .filter(e => e.scrollWidth > e.clientWidth + 1)
            .map(e => e.className + ': ' + e.innerText.slice(0, 40));
          const hits = [...panel.querySelectorAll('.pen,.cbar .btn,.add')].map(e => {
            const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
            return {cls: e.className, w: Math.round(r.width), h: Math.round(r.height),
                    hitH: Math.round(r.height + parseFloat(cs.marginTop||0) + parseFloat(cs.marginBottom||0)),
                    opacity: cs.opacity};
          });
          // the identity phone number: LTR-isolated, '+' leftmost, no bracket flipping
          const phoneEl = [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && /^\\s*\\+?9665/.test(e.textContent||'') )[0];
          let phone = null;
          if (phoneEl) { const cs = getComputedStyle(phoneEl);
            phone = {text: phoneEl.textContent.trim(), direction: cs.direction, unicodeBidi: cs.unicodeBidi,
                     firstChar: phoneEl.textContent.trim()[0]}; }
          return {truncated: trunc, hits: hits, phone: phone,
                  hOverflow: document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth,
                  panelWidth: Math.round(panel.getBoundingClientRect().width)};
        }""")
        results["design_checks"].append({"check": "§6.3 @390x844", **m3})
        ctx.close()

        # ---------- 4. AC-13: an OLD contact whose props key is entirely absent ----------
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, locale="ar-SA", reduced_motion="reduce")
        page = ctx.new_page(); errs2 = []
        page.on("pageerror", lambda e: errs2.append("pageerror: " + str(e)))
        page.on("console", lambda m: errs2.append("console: " + m.text[:140]) if m.type == "error" and "fonts." not in m.text else None)
        open_record(page, EMPTY)
        m13 = page.evaluate("""() => {
          const panel = document.querySelector('.crec') ? document.querySelector('.crec').children[0] : null;
          if (!panel) return {rendered: false};
          const rows = [...panel.querySelectorAll('.frow')];
          const missing = rows.filter(r => r.querySelector('.pm-m'));
          return {rendered: true, rowCount: rows.length, missingMarkCount: missing.length,
            gapChip: (panel.querySelector('.chip')||{}).innerText,
            everyMissingRowIsTappable: missing.every(r => r.querySelector('.add') || r.querySelector('.pen')),
            missingCopy: missing.map(r => (r.querySelector('.fval-m')||{}).innerText),
            addLabels: [...panel.querySelectorAll('.add')].map(e => e.innerText.trim()),
            contextScoreGone: !document.body.innerText.includes('اكتمال السياق'),
            smokeLandmark: document.body.innerText.includes('ما تكتبه هنا لا يستطيع المساعد تغييره')};
        }""")
        results["design_checks"].append({"check": "AC-13 · old contact, props key absent (SQL NULL)",
                                         "phone": EMPTY, **m13, "console_errors": errs2[:]})
        page.screenshot(path=str(OUT / "visual" / "extra" / f"ac13-props-absent@1440x900-{which}.png"), full_page=True)
        results["console"] += errs2
        ctx.close()
        browser.close()

    (OUT / "harness" / f"qa-record-{which}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
