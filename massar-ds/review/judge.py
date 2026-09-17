#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renders each competition entry and measures the things that can be measured.

Taste is the last 40% of this judgement, not the first. Before anyone looks at a
screenshot, these checks settle the questions that have an answer: does the page
overflow at 400px, does it use physical directions in an RTL product, does it
honour reduced motion, does a figure appear that no record supports.

Usage:  ./.venv/bin/python judge.py            (from massar-engine, paths are absolute)
"""
import asyncio
import io
import json
import os
import re
import sys

ROOT = "/Users/abdulaziz/Projects/Massar/massar-ds/review/entries"
OUT = "/tmp/claude-501/judge"
PAGES = ["home.html", "ledger.html"]
WIDTHS = [(1440, 900), (400, 860)]

# Physical directions are a correctness failure in an RTL product, not a style
# preference: the layout silently mirrors wrong. Logical properties only.
PHYSICAL = re.compile(
    r"(?<![-\w])(margin|padding|border)-(left|right)\s*:"
    r"|(?<![-\w])(left|right)\s*:\s*(?!auto)[-0-9.]"
    r"|text-align\s*:\s*(left|right)\b"
    r"|(?<![-\w])border-(left|right)-(width|color|style)\s*:"
)

# Figures in the brief. Anything money-shaped or percent-shaped outside this set
# is a candidate fabrication and gets listed for a human to rule on.
ALLOWED_NUMBERS = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "12", "16", "19", "21", "24",
    "34", "38", "100", "4,200", "4200", "34,000", "34000", "2026",
}


def static_checks(path):
    src = io.open(path, encoding="utf-8").read()
    findings = []

    phys = [m.group(0).strip() for m in PHYSICAL.finditer(src)]
    if phys:
        findings.append(("physical-directions", len(phys), phys[:6]))

    if "prefers-reduced-motion" not in src:
        findings.append(("no-reduced-motion", 1, []))

    if "hover: hover" not in src and "hover:hover" not in src:
        if ":hover" in src:
            findings.append(("hover-not-gated", 1, []))

    # transition: all repaints everything; it is the cheap option, never the right one.
    alls = re.findall(r"transition\s*:\s*all\b", src)
    if alls:
        findings.append(("transition-all", len(alls), []))

    z = re.findall(r"scale\(\s*0\s*\)", src)
    if z:
        findings.append(("scale-zero-entry", len(z), []))

    slow = [d for d in re.findall(r"(\d{3,4})ms", src) if int(d) > 300]
    if slow:
        findings.append(("over-300ms", len(slow), sorted(set(slow))[:6]))

    # Every number that renders, minus the ones the records support.
    text = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", src)
    text = re.sub(r"<[^>]+>", " ", text)
    nums = re.findall(r"\d[\d,]*", text)
    unknown = sorted({n for n in nums if n not in ALLOWED_NUMBERS})
    if unknown:
        findings.append(("numbers-not-in-brief", len(unknown), unknown[:12]))

    return findings


async def render(entry, page, w, h, pw):
    b = await pw.chromium.launch()
    pg = await b.new_page(viewport={"width": w, "height": h})
    await pg.goto("file://" + os.path.join(ROOT, entry, page))
    await pg.wait_for_timeout(700)
    over = await pg.evaluate(
        "() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    shot = os.path.join(OUT, "%s-%s-%d.png" % (entry, page.replace(".html", ""), w))
    await pg.screenshot(path=shot, full_page=(w == 1440))
    await b.close()
    return {"overflows": over["sw"] > over["iw"] + 2, "scrollWidth": over["sw"],
            "innerWidth": over["iw"], "shot": shot}


async def main():
    from playwright.async_api import async_playwright
    os.makedirs(OUT, exist_ok=True)
    report = {}
    async with async_playwright() as pw:
        for entry in sorted(os.listdir(ROOT)):
            d = os.path.join(ROOT, entry)
            if not os.path.isdir(d):
                continue
            e = {"files": sorted(f for f in os.listdir(d) if not f.startswith("."))}
            for page in PAGES:
                p = os.path.join(d, page)
                if not os.path.exists(p):
                    e[page] = {"MISSING": True}
                    continue
                e[page] = {"static": static_checks(p), "renders": {}}
                for w, h in WIDTHS:
                    try:
                        e[page]["renders"][w] = await render(entry, page, w, h, pw)
                    except Exception as ex:                      # noqa: BLE001
                        e[page]["renders"][w] = {"ERROR": str(ex)[:200]}
            report[entry] = e
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
