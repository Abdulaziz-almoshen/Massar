Reading additional input from stdin...
OpenAI Codex v0.154.0
--------
workdir: /Users/abdulaziz/Projects/Massar
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 01a0ad6a-ea27-7412-9bf1-df8985a80ea1
--------
user
Read massar-ds/BRIEF.md first — it is your full brief. Then read massar-ds/massar.css, massar-ds/shell.js, massar-ds/home.html, massar-ds/products.html, massar-ds/product.html and massar-ds/reports.html. Deliver the redesign the brief asks for: (1) brutal specific diagnosis naming selectors and values, (2) a fixed information architecture for HOME, (3) exact pasteable CSS — tokens, type scale with line-heights and tracking, spacing rhythm, card treatment, grid, (4) the near-empty state designed as the PRIMARY state, (5) an explicit delete list. Be opinionated and own the direction. Do not hedge.
codex
I’ll read the brief first, then the CSS, shell, and four pages, and give you a concrete redesign with exact selectors and pasteable CSS.
exec
/bin/zsh -lc 'cat massar-ds/BRIEF.md' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
# ASTRA BRIEF — Massar design, and why it is not good enough yet

You are gpt-6-astra. This is a HARD problem and we need your strength on it.
A founder has rejected this product's home page and dashboard EIGHT times in a
row over two days. Every rejection was some version of "this is not a good
design system and UX at all", "it looks old", "AI slop". We need a design that
looks like a HUMAN designer made it — clean, confident, restrained, and
obviously better than what is here now. Do not stop until it is done.

## The product
Massar (مسار) is Lean's Arabic-first, RTL sales-management platform for Saudi
healthcare. The primary user is THE FOUNDER. His five-second question is
«are we going to hit the number?». He is money-first, statistics-driven and
detail-oriented. His North Star is revenue booked.

## Hard constraints (non-negotiable)
- Arabic, RTL, Cairo font. Logical CSS properties only, never left/right.
- WESTERN numerals (0123456789), tabular figures.
- Arabic counted-noun grammar (مفرد/مثنى/جمع القلة/تمييز), never "n + noun".
- Time runs RIGHT to LEFT in charts: January at the right edge.
- Colour is never the only channel; every tone also carries a dot/label.
- Motion: one easing curve, UI motion under 300ms, exit faster than enter,
  scale(.97) press feedback, never enter from scale(0), every hover behind
  @media (hover:hover) and (pointer:fine), prefers-reduced-motion honoured.
- The founder supplied a reference image: a light fintech dashboard — near
  white ground, big tight display type, one huge figure with a delta pill,
  rounded soft cards, pill controls, a chart of gradient bars capped with dots
  over a dotted grid.

## THE REAL DATA (do not invent, do not drop, do not add)
Fiscal year 2026, today is 16 Sep 2026.
- Target 34,000 SAR — and it is set on ONE product, in Q3 ONLY. 7 of 8
  products have no target at all. So the headline % is structurally misleading.
- Achieved 0 SAR. Zero won deals all year.
- Open pipeline 4,200 SAR across 6 opportunity lines; only 1 line is priced.
- Every open line has been stuck 29-35 days. Last movement 18 Aug.
- 16 accounts, all approved, 0 with an owner, 0 with a contact, 7 have a sector,
  7 have a city.
- 21 contacts, 359 messages, 1,233 events. Campaign 38: sent 21, delivered 19,
  seen 12, replied 4, interested 2, opportunities 0.
- 3 sectors: قطاع المستشفيات, قطاع الصيدليات, قطاع الأعمال (+ بلا قطاع).
- 8 products: الإجازات المرضية (18,000 ر.س/سنة, target 34,000, open 4,200,
  readiness 80%), التقارير الطبية (68%), الشهادات الصحية (45%),
  تكامل الأنظمة HIS/ERP (45%), خدمات التطعيمات (45%), سجل التطعيمات الوطني
  (20,000 ر.س/سنة, 90%), صحة أعمال Plus (0%, not sold by the assistant),
  فحص الموظفين (73%). Four have an INFERRED sector needing confirmation.
- 7 stages: تواصل أولي(4) · اكتشاف الحاجة(1) · عرض المنتج(0) · التقييم التقني(0)
  · عرض السعر(1, 4,200) · التفاوض والاعتماد(0) · رابح(0) / خاسر(0).
- Knowledge has 8 weighted sections; الاعتراضات and المنافسون and الامتثال are 0%.

**The near-empty state IS the product's real state and will be for months.
A design that only looks right once the database is full is the wrong design.**

## What exists in this folder
- massar.css — the design system (one card, one row, one chip, one button,
  variants as modifiers). Table/input/select/checkbox/badge/tooltip geometry
  was PORTED FROM MEASURED VALUES off coss.com/ui and beui.dev.
- shell.js — animated side menu (256px <-> 68px, measured off beui.dev:
  label enters 200ms after an 80ms delay, exits 120ms) + sub-tab strip + dialogs.
- 26 screens mirroring the live app's routes exactly:
  home · opps/board/triage/pipeline · accounts/customers/indicators/tasks/notes
  · products/knowledge/perf/org · kmon/aimkt/targets/partners · reports
  · settings/divisions/team/users/audit · product · account
- gen.py generates all screens from one data model.

## YOUR TASK
Read massar.css, shell.js, home.html, products.html, product.html, opps.html,
reports.html. Then deliver a CONCRETE, OPINIONATED redesign that is clearly
better. Specifically:

1. **Diagnose what still makes this read as AI-generated rather than
   human-designed.** Be brutal and specific — name selectors, values, spacing,
   type sizes, the rhythm, the copy. "Looks generic" is not useful; "the card
   padding is uniform 24px everywhere, so nothing has weight" is.

2. **Fix the information architecture of HOME.** It currently stacks: money
   card -> quarters -> indicators (arcs/matrices/heat) -> funnel -> decisions
   -> board. That is six sections of equal weight. What should actually lead,
   what should be secondary, what should be removed entirely? The founder said
   "the indicators and the home page must be combined, they are not separate".

3. **Give exact CSS.** Token values, type scale with line-heights and tracking,
   the spacing rhythm, the card treatment, the grid. Write real CSS I can paste.

4. **Design the empty/near-empty state as the PRIMARY state**, not a fallback.

5. **Say what to delete.** The single most common failure here has been adding.

Anti-slop rules: no purple gradient palette, no 3-column feature grid, no
centred everything, no decorative blobs, no nested cards, no kicker above every
heading, no icon tile above every heading, no dark-mode glow.

Be specific. Be opinionated. Own the direction. Do not hedge.

exec
/bin/zsh -lc 'cat /Users/abdulaziz/Projects/Massar/.agents/skills/better-ui/SKILL.md' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
---
name: better-ui
description: Polishes and improves the UI in your project. Covers concentric border radius, optical alignment, surface depth, contextual icons, hit areas and more.
---

# UI polish

Polish comes from a pile of small details that compound. This skill is the reference for which are worth having and what values they take.

When reviewing, slow the interface down. What feels off at 10% speed is what is subtly wrong at full speed.

Keep the project's component library, tokens and density, and match its motion language except where a rule below prescribes an exact interaction.

Every duration, curve, scale and blur below is a specific value, not a range to approximate. `cubic-bezier(0.2, 0, 0, 1)` is not `cubic-bezier(0.4, 0, 0.2, 1)`, and `0.96` is not `0.95`. Use what is written.

Text wrapping, font rendering, tabular numbers and text spacing belong to `better-typography`. Hit areas, focus, keyboard support, ARIA and reduced motion belong to `better-accessibility`. Grouping, section spacing, breakpoints and spatial RTL belong to `better-layout`.

## Concentric border radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes an interface feel off. Radius, shadow and outline recipes are in [surfaces.md](surfaces.md).

## Optical over geometric alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles and asymmetric icons all need a manual nudge.

## Shadows for elevation, borders for structure

Where a border exists only to create depth, prefer layered transparent `box-shadow` values. Keep borders that communicate structure or state: dividers, separators and selected or focus states.

## Interruptible animations

Use CSS transitions for interactive state changes, because they can be interrupted mid-animation. Reserve keyframes for staged sequences that run once.

## Split and stagger enter animations

For an infrequent staged entrance where sequence communicates hierarchy, break the content into semantic chunks and stagger them by ~100ms. Animating one container gets you less for the same cost. Leave high-frequency interactions unstaggered. See [enter-exit.md](enter-exit.md).

## Subtle exit animations

Use a small fixed `translateY` rather than full height. Exits should be softer than enters. Use `ease-out` for both directions.

## Contextual icon animations

Animate icons with `opacity`, `scale` and `blur` rather than toggling visibility. Use exactly these values: scale `0.25` to `1`, opacity `0` to `1`, blur `4px` to `0px`.

With a motion library (`motion` or `framer-motion` in `package.json`), match that package's import path, or nearby imports where both exist. Use `transition: { type: "spring", duration: 0.3, bounce: 0 }`. Bounce is always `0`.

Without one, keep both icons in the DOM with one absolutely positioned, and cross-fade with `cubic-bezier(0.2, 0, 0, 1)`. That gives you enter and exit with no dependency. Both recipes are in [icon-transitions.md](icon-transitions.md).

## Image outlines

Give images a `1px` outline at low opacity for consistent depth. Pure black in light mode (`oklch(0 0 0 / 0.1)`), pure white in dark (`oklch(1 0 0 / 0.1)`). Never a near-black like slate or zinc and never a tinted neutral. A tinted outline picks up the surface underneath and reads as dirt on the image edge.

## Scale on press

A `scale(0.96)` on click gives a button tactile feedback. Always `0.96`; anything below `0.95` feels exaggerated. Add a `static` prop to switch it off where motion would distract. See [recipes for CSS, Tailwind and Motion](animations.md#scale-on-press).

## Skip animation on page load

Use `initial={false}` on `AnimatePresence` to keep enter animations off the first render. Check that it leaves intentional page entrances intact.

## Suppress transitions on theme switch

A theme flip changes color, background, border and shadow on nearly every element at once. Every transition on those properties fires together and the switch smears instead of snapping. Inject `*,*::before,*::after{transition:none !important}`, force a reflow, then remove it on the next frame. See the [recipe](animations.md#suppress-transitions-on-theme-switch).

## Transition only what changes

Always name the exact properties: `transition-property: scale, opacity`. Tailwind's `transition-transform` covers `transform, translate, scale, rotate`.

## Use `will-change` sparingly

Only for `transform`, `opacity` and `filter`, which the GPU can composite. Never `will-change: all`. Add it when you see first-frame stutter, not before. See [performance.md](performance.md).

## Match icon stroke to text weight

An icon next to text carries the text's optical weight: `1.5px` stroke beside regular (400) text, `2px` beside semibold (600). One stroke weight per icon set and one icon library per surface. Sizing and RTL flipping are in [icons.md](icons.md).

## One SVG, recolored per state

Icons use `currentColor` and take hover, selected and disabled states from CSS color and opacity, never from separate assets. Outline is the default variant; fill marks the active state.

## Motion restraint

Give high-frequency interactions instant feedback, or a transition of `150ms` or less on opacity and color. A custom animation there charges its attention cost on every trigger.

Every animated state change also needs a static cue: color, an icon, or a label. Motion is never the only feedback channel.

## Before you finish

| Mistake | Fix |
| --- | --- |
| Icons look off-center | Nudge optically with padding, or fix the SVG |
| Jarring staged entrance or exit | Stagger infrequent entrances; keep exits subtle |
| Theme toggle crossfades the whole page | Disable transitions for the swap, force a reflow, restore on the next frame |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change: transform` (sparingly) |
| Hairline icon beside bold text | Match the stroke width to the text weight |

## Reporting

**Severity.** `HIGH` breaks an interaction, makes motion unusable, or leaves a state change visible only while the animation runs. `MEDIUM` is a visible inconsistency in surfaces, icons, or motion. `LOW` is isolated polish.

**Verification.** Without a browser: every state the component defines, meaning hover, focus, active, loading and empty, plus motion durations and easings read from the code. With one: walk each state, and replay motion at 10% speed in the browser's Animations panel. Report every check you could not run as `Not verified`.

**Format.** Group findings under the principle each violates, ordered by severity, one row per root cause listing every location it appears in:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`Location` is `path/to/file:line`. `Why` names the principle and the user impact.

End with `Block` when any `HIGH` remains, `Approve` otherwise, leaving the rest in the table as work to do. Never `Approve` coverage you did not inspect. With nothing to report, state "No actionable UI-polish findings" and report verification.

exec
/bin/zsh -lc "rg --files -g AGENTS.md -g 'massar-ds/**' -g '"'!node_modules'"' -g '"'!**/.git/**'"'" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
massar-ds/massar.css
massar-ds/reports.html
massar-ds/audit.html
massar-ds/shot-accounts.png
massar-ds/settings.html
massar-ds/triage.html
massar-ds/BRIEF.md
massar-ds/shot-indicators.png
massar-ds/shot-products.png
massar-ds/board.html
massar-ds/targets.html
massar-ds/indicators.png
massar-ds/customers.html
massar-ds/opps.html
massar-ds/partners.html
massar-ds/_tbl.png
massar-ds/users.html
massar-ds/indicators.html
massar-ds/_dialog.png
massar-ds/account.html
massar-ds/divisions.html
massar-ds/home-viewport.png
massar-ds/notes.html
massar-ds/perf.html
massar-ds/home.png
massar-ds/shot-opps.png
massar-ds/home_js.txt
massar-ds/ASTRA.md
massar-ds/products.html
massar-ds/gen.py
massar-ds/shot-campaigns.png
massar-ds/tasks.html
massar-ds/knowledge.html
massar-ds/product.html
massar-ds/kmon.html
massar-ds/shot-home.png
massar-ds/accounts.html
massar-ds/home.html
massar-ds/org.html
massar-ds/aimkt.html
massar-ds/shot-targets.png
massar-ds/team.html
massar-ds/shot-product.png
massar-ds/pipeline.html
massar-ds/_home.png
massar-ds/shell.js
massar-ds/research/shot-23424811.png
massar-ds/research/shot-20481876.png
massar-ds/research/shot-27598200.png
massar-ds/research/shot-27060942.png
massar-ds/research/shot-24170257.png
massar-ds/research/shot-26297032.png
massar-ds/research/shot-27262153.png
massar-ds/research/table/beui-table-light.png
massar-ds/research/table/coss-table-default.png
massar-ds/research/table/beui-table-dark.png
massar-ds/research/table/coss-table-datatable.png
massar-ds/research/shot-24482405.png
massar-ds/research/stripe-home.png
massar-ds/research/shot-26981666.png
massar-ds/research/stripe-dashboard-login.png
massar-ds/research/sidebar/21st-hover-rail-collapsed.png
massar-ds/research/sidebar/beui-sidebar-collapsed.png
massar-ds/research/sidebar/21st-uniquesonu-dashboard.png
massar-ds/research/sidebar/21st-hover-rail-hovered.png
massar-ds/research/sidebar/21st-shadcn-sidebar.png
massar-ds/research/shot-26766456.png

exec
/bin/zsh -lc 'nl -ba massar-ds/shell.js' in /Users/abdulaziz/Projects/Massar
exec
/bin/zsh -lc 'nl -ba massar-ds/massar.css' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
     1	/* Massar shell — the side menu and the sub-tab strip, injected once so every
     2	   screen shares them. The structure mirrors the live app exactly: seven doors,
     3	   each with its own ordered sub-destinations, the first of which is the door's
     4	   own landing route. A door with one entry renders no tab strip at all.
     5	   A screen sets `data-nav` (door) and `data-sub` (route) on <body>. */
     6	(function () {
     7	  var DOORS = [
     8	    { id: "home",     l: "الرئيسية",  d: "M3 10.5 12 3l9 7.5M5.5 9.5V20h13V9.5" },
     9	    { id: "opps",     l: "فرص البيع", d: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z", n: "6" },
    10	    { id: "accounts", l: "العملاء",   d: "M16 20v-2a4 4 0 0 0-8 0v2M12 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7", n: "16" },
    11	    { id: "products", l: "المنتجات",  d: "M21 8 12 3 3 8l9 5 9-5ZM3 8v8l9 5 9-5V8", n: "6" },
    12	    { id: "kmon",     l: "الحملات",   d: "M4 11v3l14 5V6L4 11ZM4 11H3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1" },
    13	    { id: "reports",  l: "التقارير",  d: "M4 20V10M10 20V4M16 20v-7M22 20H2" },
    14	    { id: "settings", l: "الإعدادات", d: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1 2 2 0 1 1-4 0 1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 4.6 15a2 2 0 1 1 0-4 1.6 1.6 0 0 0 1.1-2.7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 11 4.6a2 2 0 1 1 4 0 1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7 2 2 0 1 1 0 4Z" }
    15	  ];
    16	  var SUBS = {
    17	    opps:     [["opps","الفرص"],["board","لوحة المتابعة"],["triage","فرز الردود"],["pipeline","سجل الأحداث"]],
    18	    accounts: [["accounts","العملاء"],["customers","المحادثات"],["indicators","مؤشرات الاستخدام"],["tasks","المهام"],["notes","الملاحظات"]],
    19	    products: [["products","المنتجات"],["knowledge","معرفة المنتج"],["perf","المستهدفات والأداء"],["org","الهيكل التنظيمي"]],
    20	    kmon:     [["kmon","متابعة الحملات"],["aimkt","إنشاء حملة"],["targets","جهات الاستهداف"],["partners","شركاء المبيعات"]],
    21	    settings: [["settings","مراحل البيع"],["divisions","الأقسام"],["team","الفريق"],["users","المستخدمون والصلاحيات"],["audit","سجل التدقيق"]]
    22	  };
    23	
    24	  var door = document.body.getAttribute("data-nav") || "home";
    25	  var sub  = document.body.getAttribute("data-sub") || door;
    26	
    27	  var items = DOORS.map(function (i) {
    28	    return '<a class="m-nav" href="' + i.id + '.html" data-t="' + i.l + '" title="' + i.l + '"' +
    29	      (i.id === door ? ' aria-current="page"' : "") + '>' +
    30	      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + i.d + '"/></svg>' +
    31	      "<span>" + i.l + "</span>" + (i.n ? "<b>" + i.n + "</b>" : "") + "</a>";
    32	  }).join("");
    33	
    34	  var side = document.createElement("nav");
    35	  side.className = "m-side";
    36	  side.setAttribute("aria-label", "التنقل");
    37	  side.innerHTML =
    38	    '<div class="m-side__b"><span class="m-side__logo">م</span>' +
    39	      '<span class="m-side__w"><span class="m-side__n">مسار</span>' +
    40	      '<span class="m-side__r">مدير النظام</span></span></div>' +
    41	    '<div class="m-side__nav">' + items + "</div>" +
    42	    '<div class="m-side__f"><button class="m-side__t" type="button" aria-expanded="true">' +
    43	      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 7 5 5-5 5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
    44	      "<span>طيّ القائمة</span></button></div>";
    45	  document.querySelector(".m-shell").prepend(side);
    46	
    47	  // The sub-tab strip renders under the page title, so a door's destinations
    48	  // are reachable in one click from anywhere inside that door.
    49	  var host = document.querySelector("[data-subs]");
    50	  if (host && SUBS[door]) {
    51	    host.innerHTML = '<div class="m-tabs" role="tablist">' + SUBS[door].map(function (s) {
    52	      return '<a class="m-tab" role="tab" href="' + s[0] + '.html"' +
    53	        (s[0] === sub ? ' aria-selected="true"' : ' aria-selected="false"') + ">" + s[1] + "</a>";
    54	    }).join("") + "</div>";
    55	  }
    56	
    57	  var KEY = "massar.side.collapsed";
    58	  function read() { try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; } }
    59	  function write(v) { try { localStorage.setItem(KEY, v ? "1" : "0"); } catch (e) {} }
    60	
    61	  var btn = side.querySelector(".m-side__t");
    62	  function apply(c, animate) {
    63	    // The first paint must not animate, or the rail slides in on every load.
    64	    if (!animate) side.style.transition = "none";
    65	    if (c) side.setAttribute("data-collapsed", ""); else side.removeAttribute("data-collapsed");
    66	    btn.setAttribute("aria-expanded", c ? "false" : "true");
    67	    if (!animate) { void side.offsetWidth; side.style.transition = ""; }
    68	  }
    69	  apply(read(), false);
    70	  function toggle() { var n = !side.hasAttribute("data-collapsed"); apply(n, true); write(n); }
    71	  btn.addEventListener("click", toggle);
    72	  document.addEventListener("keydown", function (e) {
    73	    if ((e.metaKey || e.ctrlKey) && (e.key === "b" || e.key === "B")) { e.preventDefault(); toggle(); }
    74	  });
    75	
    76	  /* ---- Dialogs. Any [data-open="id"] opens the <dialog id>. Escape and the
    77	     backdrop close it. The panel enters from scale(.97), never scale(0) —
    78	     nothing in the real world appears from nothing. ---- */
    79	  document.addEventListener("click", function (e) {
    80	    var t = e.target.closest("[data-open]");
    81	    if (t) { var dlg = document.getElementById(t.getAttribute("data-open"));
    82	             if (dlg) { dlg.showModal(); } return; }
    83	    var c = e.target.closest("[data-close]");
    84	    if (c) { c.closest("dialog").close(); return; }
    85	  });
    86	  document.addEventListener("click", function (e) {
    87	    if (e.target.tagName === "DIALOG") e.target.close();   // backdrop
    88	  });
    89	})();

 succeeded in 0ms:
     1	/* ============================================================================
     2	   MASSAR — the design system
     3	   ----------------------------------------------------------------------------
     4	   BRIEF (founder, Sep 16 2026):
     5	     · Primary user is the FOUNDER. The screen answers one question in five
     6	       seconds: «are we going to hit the number?»
     7	     · Home leads with that answer, then the pipeline as the thing you work.
     8	     · Visual register: set by the founder's own reference image — a modern
     9	       light fintech dashboard.
    10	
    11	   THE REFERENCE, READ CONCRETELY (not from memory — from the image supplied):
    12	     · near-white ground, pure white cards, LARGE radii (14-20px)
    13	     · soft diffuse shadows, no hard borders
    14	     · a very large, tight-tracked display headline that greets the reader
    15	     · one enormous figure, with a tinted DELTA PILL beside it
    16	     · the signature chart: vertical gradient bars fading to nothing, a round
    17	       dot capping each bar, over a DOTTED GRID, with a dashed trend line
    18	     · pill-shaped controls with hairlines; a search pill carrying a kbd badge
    19	     · segmented dotted progress tracks with a round knob
    20	     · blue primary, violet secondary, green for a positive delta
    21	
    22	   THE RULE: a screen composes these primitives. It never defines its own
    23	   surface, card, row, figure, chip or button. A missing capability becomes a
    24	   new variant HERE, decided once, not a private class THERE.
    25	   ========================================================================== */
    26	
    27	:root{
    28	  /* --- ground --- */
    29	  --m-page:#F7F8FA;
    30	  --m-paper:#FFFFFF;
    31	  --m-sunk:#F1F3F7;      /* a track, a well                                 */
    32	  --m-line:#EAECF0;      /* the quiet divider                               */
    33	  --m-line-2:#DFE3EA;    /* a divider that must be seen                     */
    34	  --m-dot:#E4E8F0;       /* the chart's dotted grid                         */
    35	
    36	  /* --- ink. Near-black display ink; the reference uses real black for the
    37	         headline and the figure, and grey for everything supporting. --- */
    38	  --m-ink:#0B0D12;       /* display headline, the leading figure            */
    39	  --m-ink-2:#3A404B;     /* body                                            */
    40	  --m-mut:#6B7280;       /* labels, captions, axis                          */
    41	  --m-faint:#9AA1AC;     /* a value that is absent                          */
    42	
    43	  /* --- accent --- */
    44	  --m-ac:#2F6BFF;
    45	  --m-ac-deep:#1D4FD8;
    46	  --m-ac-dim:#EDF3FF;
    47	  --m-ac-line:#CFE0FF;
    48	  --m-vi:#8B5CF6;        /* the chart's second series                       */
    49	  --m-vi-dim:#F3EEFE;
    50	
    51	  /* --- status --- */
    52	  --m-ok:#15803D;    --m-ok-dim:#E7F8EE;   --m-ok-line:#B7E9C9;
    53	  --m-warn:#B45309;  --m-warn-dim:#FEF4E4; --m-warn-line:#F6D9A8;
    54	  --m-bad:#BE123C;   --m-bad-dim:#FDEDF1;  --m-bad-line:#F7CAD6;
    55	  --m-idle:#5B6472;  --m-idle-dim:#F1F3F7; --m-idle-line:#DFE3EA;
    56	
    57	  /* --- type. The reference's defining move is the SIZE JUMP: a display
    58	         headline and a huge figure, with everything else small and calm.
    59	         Tracking goes negative as size grows. --- */
    60	  --m-t-micro:11px; --m-t-cap:12.5px; --m-t-body:14px; --m-t-sub:16px;
    61	  --m-t-h:19px;     --m-t-fig:26px;   --m-t-display:34px; --m-t-hero:58px;
    62	
    63	  /* --- space --- */
    64	  --m-1:4px; --m-2:8px; --m-3:12px; --m-4:16px; --m-5:24px; --m-6:32px; --m-7:44px;
    65	
    66	  /* --- radius. BIG. This is most of the reference's character. --- */
    67	  --m-r-chip:999px; --m-r-ctl:10px; --m-r-card:16px; --m-r-band:20px;
    68	
    69	  /* --- material. Soft and diffuse; never a hard border. --- */
    70	  --m-hair:0 0 0 1px var(--m-line);
    71	  --m-low:0 1px 2px rgba(16,24,40,.04),0 0 0 1px var(--m-line);
    72	  --m-soft:0 1px 3px rgba(16,24,40,.04),0 8px 24px -8px rgba(16,24,40,.10),0 0 0 1px var(--m-line);
    73	  --m-lift:0 2px 6px rgba(16,24,40,.06),0 16px 36px -12px rgba(16,24,40,.16),0 0 0 1px var(--m-line-2);
    74	  --m-focus:0 0 0 3px var(--m-ac-line);
    75	
    76	  /* --- motion. One curve; duration carries the meaning. --- */
    77	  --m-ease:cubic-bezier(.16,1,.3,1);
    78	  --m-move:cubic-bezier(.77,0,.175,1);
    79	  --m-press:110ms; --m-swap:170ms; --m-in:280ms; --m-out:150ms;
    80	}
    81	
    82	*,*::before,*::after{box-sizing:border-box}
    83	html,body{margin:0}
    84	body{
    85	  font-family:Cairo,"Noto Naskh Arabic",system-ui,sans-serif;
    86	  background:var(--m-page); color:var(--m-ink-2); direction:rtl;
    87	  font-size:var(--m-t-body); line-height:1.55; -webkit-font-smoothing:antialiased;
    88	}
    89	@media (prefers-reduced-motion:reduce){
    90	  *,*::before,*::after{animation-duration:1ms!important;transition-duration:1ms!important}
    91	}
    92	
    93	/* ---------------------------------------------------------- NUMBER — `m-n`
    94	   Every numeral goes through this: western digits, tabular so columns stack
    95	   and a changing figure never jumps sideways, direction isolated so
    96	   surrounding Arabic cannot reorder it. */
    97	.m-n{font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1;
    98	     direction:ltr;unicode-bidi:isolate;display:inline-block}
    99	
   100	/* ============================================================================
   101	   SHELL — the animated side menu
   102	   ----------------------------------------------------------------------------
   103	   Collapses 248px -> 68px. Only `inline-size` and the label's opacity animate;
   104	   nothing reflows the page content because the main column is a flex sibling.
   105	   The label CLIPS rather than wraps (white-space:nowrap + overflow) so a long
   106	   Arabic name never reflows mid-animation.
   107	   Motion per emil-design-eng: one curve, 260ms, exit faster, press feedback,
   108	   hover behind a fine-pointer query, reduced-motion honoured globally.
   109	   ========================================================================== */
   110	.m-shell{display:flex;min-block-size:100vh}
   111	.m-side{inline-size:256px;flex:0 0 auto;background:var(--m-paper);
   112	        border-inline-start:1px solid var(--m-line);
   113	        display:flex;flex-direction:column;position:sticky;inset-block-start:0;
   114	        block-size:100vh;overflow:hidden;
   115	        transition:inline-size var(--m-in) var(--m-ease)}
   116	.m-side[data-collapsed]{inline-size:68px}
   117	
   118	.m-side__b{display:flex;align-items:center;gap:var(--m-2);padding:var(--m-4) var(--m-3) var(--m-2);
   119	           white-space:nowrap}
   120	.m-side__logo{inline-size:28px;block-size:28px;border-radius:9px;flex:0 0 auto;
   121	              display:grid;place-items:center;font-weight:800;font-size:var(--m-t-body);
   122	              color:#fff;background:linear-gradient(140deg,var(--m-ac),var(--m-vi))}
   123	.m-side__w{min-inline-size:0;overflow:hidden;
   124	           transition:opacity 200ms var(--m-ease) 80ms}
   125	.m-side__n{font-size:var(--m-t-sub);font-weight:700;color:var(--m-ink);line-height:1.2}
   126	.m-side__r{font-size:var(--m-t-micro);color:var(--m-faint)}
   127	.m-side[data-collapsed] .m-side__w{opacity:0;transition:opacity 120ms var(--m-ease)}
   128	
   129	.m-side__grp{font-size:var(--m-t-micro);font-weight:700;color:var(--m-faint);
   130	             letter-spacing:.6px;padding:var(--m-4) var(--m-4) var(--m-1);white-space:nowrap;
   131	             transition:opacity var(--m-out) var(--m-ease)}
   132	.m-side[data-collapsed] .m-side__grp{opacity:0}
   133	
   134	.m-side__nav{flex:1 1 auto;min-block-size:0;overflow-y:auto;overflow-x:hidden;
   135	             padding:0 var(--m-2)}
   136	.m-nav{display:flex;align-items:center;gap:10px;padding:8px var(--m-3);min-block-size:36px;
   137	       border-radius:12px;color:var(--m-ink-2);text-decoration:none;
   138	       font-size:var(--m-t-body);white-space:nowrap;position:relative;
   139	       transition:background var(--m-out) var(--m-ease),color var(--m-out) var(--m-ease),
   140	                  transform var(--m-press) var(--m-ease)}
   141	.m-nav svg{inline-size:20px;block-size:20px;flex:0 0 auto;stroke:currentColor;
   142	           stroke-width:1.7;fill:none;stroke-linecap:round;stroke-linejoin:round}
   143	.m-nav span{flex:1 1 auto;min-inline-size:0;overflow:hidden;
   144	            transition:opacity 200ms var(--m-ease) 80ms,transform 200ms var(--m-ease) 80ms}
   145	.m-side[data-collapsed] .m-nav span{opacity:0;transform:translateX(4px);
   146	            transition:opacity 120ms var(--m-ease),transform 120ms var(--m-ease)}
   147	.m-nav b{font-size:var(--m-t-micro);font-weight:700;background:var(--m-sunk);
   148	         color:var(--m-mut);border-radius:var(--m-r-chip);padding:1px 7px;
   149	         font-variant-numeric:tabular-nums;
   150	         transition:opacity var(--m-out) var(--m-ease)}
   151	.m-side[data-collapsed] .m-nav b{opacity:0}
   152	@media (hover:hover) and (pointer:fine){
   153	  .m-nav:hover{background:var(--m-page);color:var(--m-ink)} }
   154	.m-nav:active{transform:scale(.98)}
   155	.m-nav[aria-current]{background:var(--m-ac-dim);color:var(--m-ac-deep);font-weight:600}
   156	.m-nav[aria-current] b{background:var(--m-paper);color:var(--m-ac-deep)}
   157	.m-nav:focus-visible{outline:none;box-shadow:var(--m-focus)}
   158	/* On a collapsed rail the label becomes a flyout, so the rail stays usable. */
   159	.m-nav::after{content:attr(data-t);position:absolute;inset-inline-end:calc(100% + 10px);
   160	  inset-block-start:50%;transform:translateY(-50%) scale(.96);transform-origin:center right;
   161	  background:var(--m-ink);color:#fff;font-size:var(--m-t-cap);font-weight:600;
   162	  padding:5px 10px;border-radius:var(--m-r-ctl);white-space:nowrap;pointer-events:none;
   163	  opacity:0;z-index:20;transition:opacity var(--m-out) var(--m-ease),
   164	                                  transform var(--m-out) var(--m-ease)}
   165	@media (hover:hover) and (pointer:fine){
   166	  .m-side[data-collapsed] .m-nav:hover::after{opacity:1;transform:translateY(-50%) scale(1)} }
   167	
   168	.m-side__f{padding:var(--m-2) var(--m-2) var(--m-3);border-block-start:1px solid var(--m-line)}
   169	.m-side__t{display:flex;align-items:center;gap:var(--m-3);inline-size:100%;
   170	           padding:9px var(--m-3);border:0;background:transparent;cursor:pointer;
   171	           border-radius:var(--m-r-ctl);color:var(--m-mut);font:inherit;
   172	           font-size:var(--m-t-cap);white-space:nowrap;
   173	           transition:background var(--m-out) var(--m-ease),transform var(--m-press) var(--m-ease)}
   174	@media (hover:hover) and (pointer:fine){ .m-side__t:hover{background:var(--m-page)} }
   175	.m-side__t:active{transform:scale(.98)}
   176	.m-side__t svg{inline-size:18px;block-size:18px;flex:0 0 auto;stroke:currentColor;
   177	               stroke-width:1.7;fill:none;transition:transform var(--m-in) var(--m-ease)}
   178	.m-side[data-collapsed] .m-side__t svg{transform:rotate(180deg)}
   179	.m-side[data-collapsed] .m-side__t span{opacity:0}
   180	
   181	.m-main{flex:1 1 auto;min-inline-size:0}
   182	.m-bar{background:var(--m-paper);border-block-end:1px solid var(--m-line);
   183	       padding:var(--m-3) var(--m-6);display:flex;align-items:center;
   184	       justify-content:space-between;gap:var(--m-4);flex-wrap:wrap;
   185	       position:sticky;inset-block-start:0;z-index:10}
   186	.m-page{padding:var(--m-5) var(--m-6) var(--m-7);max-inline-size:1440px}
   187	@media (max-width:900px){
   188	  .m-side{position:fixed;inset-inline-end:0;z-index:40;transform:translateX(100%);
   189	          transition:transform var(--m-in) var(--m-ease)}
   190	  .m-side[data-open]{transform:none}
   191	  .m-bar,.m-page{padding-inline:var(--m-4)}
   192	}
   193	
   194	/* BREADCRUMB + PAGE TITLE — one line each, no explanatory subtitle. */
   195	.m-crumb{font-size:var(--m-t-cap);color:var(--m-faint)}
   196	.m-h1{margin:0;font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
   197	      letter-spacing:-1px;line-height:1.2}
   198	.m-head{display:flex;align-items:center;justify-content:space-between;
   199	        gap:var(--m-4);flex-wrap:wrap;margin-block-end:var(--m-5)}
   200	.m-head__a{display:flex;gap:var(--m-2);align-items:center;flex-wrap:wrap}
   201	
   202	/* SEARCH */
   203	.m-search{display:flex;align-items:center;gap:var(--m-2);background:var(--m-page);
   204	          border-radius:var(--m-r-chip);padding:8px var(--m-4);box-shadow:var(--m-hair);
   205	          color:var(--m-faint);font-size:var(--m-t-body);min-inline-size:230px}
   206	.m-search svg{inline-size:16px;block-size:16px;stroke:currentColor;stroke-width:1.8;fill:none}
   207	.m-kbd{margin-inline-start:auto;display:flex;gap:3px}
   208	.m-kbd span{font-size:var(--m-t-micro);font-weight:600;color:var(--m-mut);
   209	            background:var(--m-paper);border-radius:5px;padding:2px 6px;box-shadow:var(--m-hair)}
   210	
   211	/* TABS — the record navigator. The indicator GLIDES and is deliberately
   212	   over-damped (no overshoot): in a scrollable rail an overshoot produces a
   213	   transient scrollbar and a layout shift. Measured on beui.dev. */
   214	.m-tabs{display:flex;gap:var(--m-1);border-block-end:1px solid var(--m-line);
   215	        overflow-x:auto;position:relative}
   216	.m-tab{display:inline-flex;align-items:center;gap:7px;padding:11px var(--m-3);
   217	       color:var(--m-mut);text-decoration:none;font-size:var(--m-t-body);font-weight:500;
   218	       border:0;background:transparent;cursor:pointer;font-family:inherit;
   219	       white-space:nowrap;border-block-end:2px solid transparent;margin-block-end:-1px;
   220	       transition:color var(--m-out) var(--m-ease)}
   221	@media (hover:hover) and (pointer:fine){ .m-tab:hover{color:var(--m-ink)} }
   222	.m-tab[aria-selected="true"]{color:var(--m-ink);font-weight:600;
   223	       border-block-end-color:var(--m-ac)}
   224	.m-tab b{font-size:var(--m-t-micro);font-weight:700;background:var(--m-sunk);
   225	         color:var(--m-mut);border-radius:var(--m-r-chip);padding:1px 6px;
   226	         font-variant-numeric:tabular-nums}
   227	.m-tab:focus-visible{outline:none;box-shadow:var(--m-focus);border-radius:var(--m-r-sm,6px)}
   228	
   229	/* SEGMENTED CONTROL */
   230	.m-seg{display:inline-flex;background:var(--m-sunk);border-radius:var(--m-r-chip);padding:3px}
   231	.m-seg button{font:inherit;font-size:var(--m-t-cap);font-weight:600;border:0;cursor:pointer;
   232	       background:transparent;color:var(--m-mut);padding:5px 13px;border-radius:var(--m-r-chip);
   233	       transition:background var(--m-out) var(--m-ease),color var(--m-out) var(--m-ease),
   234	                  transform var(--m-press) var(--m-ease)}
   235	.m-seg button:active{transform:scale(.97)}
   236	.m-seg button[aria-pressed="true"]{background:var(--m-paper);color:var(--m-ink);
   237	       box-shadow:var(--m-low)}
   238	
   239	/* ============================================================================
   240	   FORM CONTROLS — ported from coss.com/ui, measured
   241	   input/select trigger 32px · padding 0 11px · radius 10px · resting shadow
   242	   `0 1px 2px rgba(0,0,0,.05)` plus an inset top hairline · focus replaces the
   243	   resting shadow with a 3px ring and darkens the border · 150ms
   244	   cubic-bezier(.4,0,.2,1). Massar swaps the neutral ring for the accent.
   245	   ========================================================================== */
   246	.m-field{display:flex;flex-direction:column;gap:6px}
   247	.m-label{font-size:var(--m-t-cap);font-weight:500;color:var(--m-ink-2)}
   248	.m-req::after{content:"*";color:var(--m-bad);margin-inline-start:3px}
   249	.m-input,.m-select{font:inherit;font-size:var(--m-t-body);color:var(--m-ink);
   250	  background:var(--m-paper);border:0;border-radius:10px;
   251	  padding:0 11px;block-size:36px;inline-size:100%;
   252	  box-shadow:0 0 0 1px var(--m-line-2),0 1px 2px rgba(0,0,0,.05),
   253	             inset 0 1px rgba(0,0,0,.04);
   254	  transition:box-shadow 150ms cubic-bezier(.4,0,.2,1)}
   255	.m-input::placeholder{color:var(--m-faint);opacity:.72}
   256	.m-input:focus,.m-select:focus{outline:none;
   257	  box-shadow:0 0 0 1px var(--m-ac),0 0 0 3px var(--m-ac-line)}
   258	.m-input[aria-invalid="true"]{box-shadow:0 0 0 1px var(--m-bad),0 0 0 3px var(--m-bad-dim)}
   259	textarea.m-input{resize:vertical;line-height:1.7;block-size:auto;padding:9px 11px}
   260	/* The select's own chevron, 16px at 80% — measured. */
   261	.m-select{appearance:none;padding-inline-end:32px;
   262	  background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' opacity='.8'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
   263	  background-repeat:no-repeat;background-size:16px;
   264	  background-position:left 10px center}
   265	.m-hint{font-size:var(--m-t-micro);color:var(--m-faint)}
   266	.m-err{font-size:var(--m-t-micro);color:var(--m-bad);font-weight:600}
   267	.m-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--m-4)}
   268	.m-form .full{grid-column:1 / -1}
   269	@media (max-width:640px){ .m-form{grid-template-columns:1fr} }
   270	
   271	/* BADGE — 18px tall, padding 0 3px, radius 6, 12/16 at 500. A tinted variant
   272	   is the accent at 8% alpha carrying the full-strength accent as its text. */
   273	.m-chip{display:inline-flex;align-items:center;gap:4px;min-block-size:18px;
   274	        padding:1px 7px;border-radius:6px;font-size:var(--m-t-cap);line-height:16px;
   275	        font-weight:500;white-space:nowrap;
   276	        background:color-mix(in srgb,var(--m-idle) 8%,transparent);color:var(--m-idle)}
   277	.m-chip--ok{background:color-mix(in srgb,var(--m-ok) 8%,transparent);color:var(--m-ok)}
   278	.m-chip--warn{background:color-mix(in srgb,var(--m-warn) 8%,transparent);color:var(--m-warn)}
   279	.m-chip--bad{background:color-mix(in srgb,var(--m-bad) 8%,transparent);color:var(--m-bad)}
   280	.m-chip--ac{background:color-mix(in srgb,var(--m-ac) 8%,transparent);color:var(--m-ac-deep)}
   281	/* Colour is never the only channel — a tone chip carries a dot too. */
   282	.m-chip::before{content:"";inline-size:5px;block-size:5px;border-radius:50%;
   283	                background:currentColor;flex:0 0 auto}
   284	.m-chip--plain::before{display:none}
   285	
   286	/* TOOLTIP — 4px 8px, radius 8, 12/16; enters from scale(.98), 150ms. */
   287	.m-tip2{position:absolute;padding:4px 8px;border-radius:8px;font-size:var(--m-t-cap);
   288	        line-height:16px;background:var(--m-paper);color:var(--m-ink);
   289	        box-shadow:0 0 0 1px var(--m-line),0 4px 6px -1px rgba(0,0,0,.05),
   290	                   0 2px 4px -2px rgba(0,0,0,.05),inset 0 1px rgba(0,0,0,.04);
   291	        opacity:0;transform:scale(.98);pointer-events:none;
   292	        transition:opacity 150ms cubic-bezier(.4,0,.2,1),
   293	                   transform 150ms cubic-bezier(.4,0,.2,1)}
   294	.m-tip2[data-open]{opacity:1;transform:none}
   295	
   296	/* ============================================================================
   297	   TABLE — ported from measured values, not invented
   298	   ----------------------------------------------------------------------------
   299	   Geometry and motion taken from coss.com/ui/docs/components/table (the light
   300	   fintech register) and beui.dev/components/motion/table (the sortable header
   301	   and the sticky treatment). Colour is mapped onto Massar's palette; every
   302	   physical direction is rewritten as a logical property for RTL.
   303	
   304	   coss:  row 39px · th 40px · th padding 0 10px · 14px/500 · header has NO fill
   305	          td padding 10px · row rule 1px rgba(0,0,0,.08) · hover #FAFAFA
   306	          selected #F5F5F5 · checkbox col 26px · tfoot 43px, padding 14px 10px
   307	   beui:  sticky header · container radius 16px + overflow hidden
   308	          sortable th is a FULL-HEIGHT button; chevron 14px rotates 0->180deg,
   309	          opacity .35 -> 1, 180ms cubic-bezier(.16,1,.3,1)
   310	   Both ship WITHOUT tabular figures; Massar adds them, because a ledger column
   311	   that shifts as its digits change is unreadable.
   312	   ========================================================================== */
   313	.m-tablewrap{position:relative;inline-size:100%;overflow-x:auto;
   314	             border-radius:var(--m-r-card)}
   315	.m-table{inline-size:100%;border-collapse:collapse}
   316	.m-table th{block-size:40px;padding:0 10px;font-size:var(--m-t-body);font-weight:500;
   317	            line-height:14px;color:var(--m-mut);text-align:start;white-space:nowrap;
   318	            background:transparent;border-block-end:1px solid var(--m-line)}
   319	.m-table td{padding:10px;font-size:var(--m-t-body);font-weight:500;line-height:1.45;
   320	            color:var(--m-ink-2);vertical-align:middle;
   321	            border-block-start:1px solid var(--m-line)}
   322	.m-table tbody tr{transition:background-color 150ms cubic-bezier(.4,0,.2,1)}
   323	@media (hover:hover) and (pointer:fine){
   324	  .m-table tbody tr:hover{background:var(--m-page)} }
   325	.m-table tbody tr[aria-selected="true"]{background:var(--m-sunk)}
   326	/* Sticky header, from beui. A ledger is scrolled, so the column names stay. */
   327	.m-table--sticky thead th{position:sticky;inset-block-start:0;z-index:2;
   328	            background:var(--m-paper)}
   329	/* The sortable header is a full-height button, so the whole cell is the target. */
   330	.m-th-sort{display:flex;align-items:center;gap:4px;inline-size:100%;block-size:100%;
   331	           font:inherit;color:inherit;background:none;border:0;cursor:pointer;
   332	           padding:0;text-align:start}
   333	.m-th-sort svg{inline-size:14px;block-size:14px;flex:0 0 auto;opacity:.35;
   334	           stroke:currentColor;stroke-width:2;fill:none;
   335	           transition:transform 180ms cubic-bezier(.16,1,.3,1),
   336	                      opacity 180ms cubic-bezier(.16,1,.3,1)}
   337	.m-table th[aria-sort] .m-th-sort svg{opacity:1}
   338	.m-table th[aria-sort="descending"] .m-th-sort svg{transform:rotate(180deg)}
   339	/* Checkbox column: 26px, exactly as measured. */
   340	.m-table th.m-sel{inline-size:26px;padding:0 0 0 10px}
   341	.m-table td.m-sel{padding:10px 0 10px 9px}
   342	/* A totals row, not pagination — coss ships no pagination bar. */
   343	.m-table tfoot td{block-size:43px;padding:14px 10px;font-weight:600;color:var(--m-ink);
   344	            background:var(--m-page);border-block-start:1px solid var(--m-line-2)}
   345	.m-td-n{font-weight:600;color:var(--m-ink)}
   346	/* Numeric columns align to the OUTSIDE edge and carry tabular figures. */
   347	.m-td-v{text-align:end;font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1;
   348	        font-weight:600;color:var(--m-ink);white-space:nowrap}
   349	.m-table th.num{text-align:end}
   350	.m-td-nil{color:var(--m-faint);font-weight:400}
   351	.m-table__empty td{padding:0}
   352	.m-tools{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3);
   353	         padding:var(--m-3);flex-wrap:wrap}
   354	
   355	/* CHECKBOX — 16x16, radius 4, only the shadow transitions (measured: the check
   356	   mark itself is not animated on coss). */
   357	.m-cb{inline-size:16px;block-size:16px;border-radius:4px;appearance:none;cursor:pointer;
   358	      background:var(--m-paper);box-shadow:0 0 0 1px var(--m-line-2),0 1px 2px rgba(0,0,0,.05);
   359	      display:grid;place-items:center;transition:box-shadow 150ms cubic-bezier(.4,0,.2,1)}
   360	.m-cb:checked{background:var(--m-ac);box-shadow:0 0 0 1px var(--m-ac)}
   361	.m-cb:checked::after{content:"";inline-size:9px;block-size:5px;border:2px solid #fff;
   362	      border-block-start:0;border-inline-end:0;transform:rotate(-45deg) translate(1px,-1px)}
   363	.m-cb:focus-visible{outline:none;box-shadow:0 0 0 1px var(--m-ac),var(--m-focus)}
   364	
   365	/* AVATAR */
   366	.m-av{inline-size:30px;block-size:30px;border-radius:50%;flex:0 0 auto;display:grid;
   367	      place-items:center;font-size:var(--m-t-cap);font-weight:700;
   368	      background:var(--m-ac-dim);color:var(--m-ac-deep)}
   369	.m-av--sq{border-radius:9px;background:var(--m-sunk);color:var(--m-ink-2)}
   370	
   371	/* --------------------------------------------------------------- GREETING
   372	   The reference's opening move: a breadcrumb, then a large tight display
   373	   headline that speaks to the reader, then one calm subtitle. */
   374	.m-crumb{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-end:var(--m-3)}
   375	.m-greet{display:flex;align-items:flex-end;justify-content:space-between;
   376	         gap:var(--m-5);flex-wrap:wrap;margin-block-end:var(--m-5)}
   377	.m-greet__t{margin:0;font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
   378	            letter-spacing:-1px;line-height:1.2}
   379	.m-greet__s{font-size:var(--m-t-sub);color:var(--m-mut);margin-block-start:var(--m-2)}
   380	.m-greet__a{display:flex;gap:var(--m-2);align-items:center;flex-wrap:wrap}
   381	
   382	/* SEARCH PILL with a kbd badge, straight from the reference. */
   383	.m-search{display:flex;align-items:center;gap:var(--m-2);background:var(--m-paper);
   384	          border-radius:var(--m-r-chip);padding:9px var(--m-4);box-shadow:var(--m-low);
   385	          color:var(--m-faint);font-size:var(--m-t-body);min-inline-size:240px}
   386	.m-kbd{margin-inline-start:auto;display:flex;gap:3px}
   387	.m-kbd span{font-size:var(--m-t-micro);font-weight:600;color:var(--m-mut);
   388	            background:var(--m-page);border-radius:5px;padding:2px 6px;box-shadow:var(--m-hair)}
   389	
   390	/* ------------------------------------------------------------------ CARD */
   391	.m-card{background:var(--m-paper);border-radius:var(--m-r-card);box-shadow:var(--m-soft);
   392	        padding:var(--m-5)}
   393	.m-card--band{border-radius:var(--m-r-band);padding:var(--m-6)}
   394	.m-card--pad0{padding:0}
   395	.m-card__h{display:flex;align-items:flex-start;justify-content:space-between;
   396	           gap:var(--m-3);margin-block-end:var(--m-4)}
   397	.m-card__t{margin:0;font-size:var(--m-t-h);font-weight:700;color:var(--m-ink);
   398	           letter-spacing:-.3px}
   399	.m-card__k{font-size:var(--m-t-body);color:var(--m-mut);font-weight:500}
   400	
   401	/* THE LEADING FIGURE + DELTA PILL. The reference's centrepiece. */
   402	.m-lead{display:flex;align-items:center;gap:var(--m-4);flex-wrap:wrap}
   403	.m-lead__v{font-size:var(--m-t-hero);font-weight:800;color:var(--m-ink);
   404	           letter-spacing:-2.5px;line-height:1.05;font-variant-numeric:tabular-nums}
   405	.m-lead__v small{font-size:var(--m-t-h);font-weight:600;color:var(--m-mut);
   406	                 letter-spacing:0;margin-inline-start:var(--m-2)}
   407	.m-delta{display:inline-flex;align-items:center;gap:6px;font-size:var(--m-t-body);
   408	         font-weight:600;padding:6px 13px;border-radius:var(--m-r-chip);
   409	         background:var(--m-ok-dim);color:var(--m-ok)}
   410	.m-delta--bad{background:var(--m-bad-dim);color:var(--m-bad)}
   411	.m-delta--warn{background:var(--m-warn-dim);color:var(--m-warn)}
   412	.m-delta--flat{background:var(--m-idle-dim);color:var(--m-idle)}
   413	
   414	/* ------------------------------------------------------------------- STAT */
   415	.m-stat__k{font-size:var(--m-t-cap);color:var(--m-mut);font-weight:500}
   416	.m-stat__v{font-size:var(--m-t-fig);font-weight:800;color:var(--m-ink);line-height:1.2;
   417	           margin-block-start:var(--m-1);letter-spacing:-.8px;
   418	           font-variant-numeric:tabular-nums}
   419	.m-stat__v small{font-size:var(--m-t-cap);font-weight:600;color:var(--m-mut);
   420	                 letter-spacing:0;margin-inline-start:4px}
   421	.m-stat__s{font-size:var(--m-t-micro);color:var(--m-faint);margin-block-start:3px}
   422	.m-stat--ac .m-stat__v{color:var(--m-ac)}
   423	.m-stat--mut .m-stat__v{color:var(--m-faint)}
   424	.m-stats{display:flex;gap:var(--m-6);flex-wrap:wrap}
   425	
   426	/* ------------------------------------------------------------------ CHART
   427	   The reference's signature: gradient bars fading to nothing, a round dot
   428	   capping each, over a dotted grid, with a dashed trend line.
   429	   TIME RUNS RIGHT TO LEFT in RTL — January at the right edge. */
   430	.m-chart{display:block;inline-size:100%;block-size:auto;overflow:visible}
   431	.m-chart__ax{font-size:var(--m-t-cap);fill:var(--m-mut);font-family:inherit}
   432	.m-chart__bar{fill:url(#mBar)}
   433	.m-chart__cap{fill:var(--m-ac)}
   434	.m-chart__cap--vi{fill:var(--m-vi)}
   435	.m-chart__trend{stroke:var(--m-ac-line);stroke-width:2;stroke-dasharray:5 5;fill:none}
   436	.m-chart__zero{stroke:var(--m-line-2);stroke-width:1}
   437	.m-chart__now{stroke:var(--m-line-2);stroke-width:1;stroke-dasharray:3 4}
   438	/* The bars draw upward on first paint only. */
   439	.m-chart__grow{transform-box:fill-box;transform-origin:bottom;
   440	               animation:m-grow 700ms var(--m-ease) both}
   441	@keyframes m-grow{from{transform:scaleY(.02);opacity:0}to{transform:scaleY(1);opacity:1}}
   442	@media (prefers-reduced-motion:reduce){ .m-chart__grow{animation:none} }
   443	
   444	/* TOOLTIP, as drawn in the reference: a white rounded card with two columns. */
   445	.m-tip{position:absolute;background:var(--m-paper);border-radius:var(--m-r-ctl);
   446	       box-shadow:var(--m-lift);padding:var(--m-3) var(--m-4);pointer-events:none}
   447	.m-tip__d{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-end:var(--m-2)}
   448	.m-tip__g{display:flex;gap:var(--m-5)}
   449	.m-tip__k{font-size:var(--m-t-cap);color:var(--m-mut)}
   450	.m-tip__v{font-size:var(--m-t-sub);font-weight:700;color:var(--m-ink);
   451	          font-variant-numeric:tabular-nums}
   452	.m-tip__v--bad{color:var(--m-bad)}
   453	
   454	/* ------------------------------------------------------- SEGMENTED TRACK
   455	   The reference's goal bar: a row of dots that fill, with a round knob at
   456	   the head. Reads as progress without pretending to a precision it lacks. */
   457	.m-seg-bar{display:flex;align-items:center;gap:3px;margin-block:var(--m-3) var(--m-2)}
   458	.m-seg-bar i{block-size:8px;flex:1 1 auto;border-radius:99px;background:var(--m-sunk)}
   459	.m-seg-bar i.on{background:var(--m-ac)}
   460	.m-seg-bar b{inline-size:16px;block-size:16px;border-radius:50%;background:var(--m-paper);
   461	             box-shadow:0 0 0 3px var(--m-ac),0 1px 3px rgba(16,24,40,.2);flex:0 0 auto}
   462	
   463	/* -------------------------------------------------------------- THE BOARD
   464	   Kept from the settled paradigm: home is where the pipeline is worked.
   465	   Empty stages collapse to a rail so the real content starts immediately. */
   466	.m-board{display:flex;gap:var(--m-3);align-items:flex-start;overflow-x:auto;
   467	         padding-block-end:var(--m-2)}
   468	.m-col{inline-size:252px;flex:0 0 auto;display:flex;flex-direction:column;
   469	       background:var(--m-page);border-radius:var(--m-r-ctl);padding:var(--m-3)}
   470	.m-col__t{display:flex;align-items:center;gap:var(--m-2);margin-block-end:var(--m-1)}
   471	.m-col__dot{inline-size:8px;block-size:8px;border-radius:50%;flex:0 0 auto;
   472	            background:var(--m-tone,var(--m-idle))}
   473	.m-col__n{font-size:var(--m-t-body);font-weight:600;color:var(--m-ink);flex:1 1 auto}
   474	.m-col__c{font-size:var(--m-t-micro);font-weight:700;color:var(--m-mut);
   475	          background:var(--m-paper);border-radius:var(--m-r-chip);padding:1px 7px;
   476	          box-shadow:var(--m-hair);font-variant-numeric:tabular-nums}
   477	.m-col__v{font-size:var(--m-t-cap);color:var(--m-mut);padding-inline-start:16px;
   478	          margin-block-end:var(--m-2);font-variant-numeric:tabular-nums}
   479	.m-col__b{display:flex;flex-direction:column;gap:var(--m-2)}
   480	.m-col--rail{inline-size:44px;cursor:pointer;align-self:stretch}
   481	.m-col--rail .m-col__b,.m-col--rail .m-col__v{display:none}
   482	.m-col--rail .m-col__t{flex-direction:column;gap:var(--m-3);margin:0}
   483	.m-col--rail .m-col__n{writing-mode:vertical-rl;transform:rotate(180deg);
   484	            white-space:nowrap;flex:0 0 auto;font-size:var(--m-t-cap);color:var(--m-mut)}
   485	@media (hover:hover) and (pointer:fine){ .m-col--rail:hover{background:var(--m-sunk)} }
   486	
   487	.m-deal{background:var(--m-paper);border-radius:var(--m-r-ctl);padding:var(--m-3);
   488	        box-shadow:var(--m-low);cursor:grab;
   489	        transition:box-shadow var(--m-out) var(--m-ease),transform var(--m-press) var(--m-ease)}
   490	@media (hover:hover) and (pointer:fine){ .m-deal:hover{box-shadow:var(--m-lift)} }
   491	.m-deal:active{cursor:grabbing;transform:scale(.985)}
   492	.m-deal:focus-visible{outline:none;box-shadow:var(--m-focus),var(--m-low)}
   493	.m-deal__n{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
   494	           display:flex;align-items:center;justify-content:space-between;gap:var(--m-2)}
   495	.m-deal__p{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:2px}
   496	.m-deal__f{display:flex;align-items:center;justify-content:space-between;
   497	           gap:var(--m-2);margin-block-start:var(--m-2)}
   498	.m-deal__v{font-size:var(--m-t-sub);font-weight:700;color:var(--m-ink);
   499	           font-variant-numeric:tabular-nums}
   500	.m-deal__v--nil{font-size:var(--m-t-cap);font-weight:600;color:var(--m-warn)}
   501	.m-deal__age{font-size:var(--m-t-micro);color:var(--m-faint);font-variant-numeric:tabular-nums}
   502	.m-deal__age--old{color:var(--m-warn);font-weight:600}
   503	.m-empty-col{padding:var(--m-4) var(--m-3);text-align:center;border-radius:var(--m-r-ctl);
   504	             border:1px dashed var(--m-line-2);color:var(--m-faint);
   505	             font-size:var(--m-t-cap);line-height:1.7}
   506	
   507	/* -------------------------------------------------------------- LIST ROW
   508	   The reference's «Recent Transactions»: a round brand mark, a two-line
   509	   label, and a value on the outside edge. */
   510	.m-item{display:flex;align-items:center;gap:var(--m-3);padding:var(--m-3) 0;
   511	        border-block-start:1px solid var(--m-line)}
   512	.m-item:first-child{border-block-start:0}
   513	.m-item__m{inline-size:38px;block-size:38px;border-radius:50%;flex:0 0 auto;
   514	           display:grid;place-items:center;font-size:var(--m-t-body);font-weight:700;
   515	           background:var(--m-page);color:var(--m-ink-2);box-shadow:var(--m-hair)}
   516	.m-item__b{flex:1 1 auto;min-inline-size:0}
   517	.m-item__n{font-size:var(--m-t-body);font-weight:600;color:var(--m-ink)}
   518	.m-item__s{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-start:1px}
   519	.m-item__v{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
   520	           font-variant-numeric:tabular-nums;white-space:nowrap}
   521	
   522	/* ------------------------------------------------------------- INSIGHTS
   523	   The reference's AI panel: a dithered blue field with a white card floating
   524	   on it. The dither is a repeating radial-gradient, not an image. */
   525	.m-insight{border-radius:var(--m-r-band);padding:var(--m-5);color:#fff;
   526	  background:
   527	    radial-gradient(circle at 1px 1px,rgba(255,255,255,.32) 1px,transparent 0) 0 0/8px 8px,
   528	    linear-gradient(150deg,#1D4FD8,#2F6BFF 45%,#8B5CF6);
   529	  display:flex;flex-direction:column;gap:var(--m-3)}
   530	.m-insight__k{font-size:var(--m-t-cap);opacity:.85;font-weight:600}
   531	.m-insight__t{font-size:var(--m-t-h);font-weight:700;letter-spacing:-.3px;line-height:1.35}
   532	.m-insight__c{background:var(--m-paper);border-radius:var(--m-r-ctl);padding:var(--m-3) var(--m-4);
   533	              color:var(--m-ink-2);font-size:var(--m-t-cap);line-height:1.75}
   534	.m-insight__c b{color:var(--m-ink)}
   535	.m-dots{display:flex;gap:5px}
   536	.m-dots i{inline-size:16px;block-size:4px;border-radius:99px;background:rgba(255,255,255,.35)}
   537	.m-dots i.on{background:#fff;inline-size:22px}
   538	
   539	/* ------------------------------------------------------------------- CHIP */
   540	.m-chip{display:inline-flex;align-items:center;gap:6px;font-size:var(--m-t-micro);
   541	        font-weight:600;padding:3px 9px;border-radius:var(--m-r-chip);
   542	        background:var(--m-idle-dim);color:var(--m-idle);white-space:nowrap}
   543	.m-chip--ok{background:var(--m-ok-dim);color:var(--m-ok)}
   544	.m-chip--warn{background:var(--m-warn-dim);color:var(--m-warn)}
   545	.m-chip--bad{background:var(--m-bad-dim);color:var(--m-bad)}
   546	.m-chip--ac{background:var(--m-ac-dim);color:var(--m-ac-deep)}
   547	/* Colour is never the only channel — a tone chip carries a dot too. */
   548	.m-chip::before{content:"";inline-size:5px;block-size:5px;border-radius:50%;background:currentColor}
   549	.m-chip--plain::before{display:none}
   550	
   551	/* ----------------------------------------------------------------- BUTTON */
   552	.m-btn{display:inline-flex;align-items:center;gap:7px;font:inherit;
   553	       font-size:var(--m-t-body);font-weight:600;padding:9px 16px;
   554	       border-radius:var(--m-r-chip);border:0;cursor:pointer;
   555	       background:var(--m-paper);color:var(--m-ink);box-shadow:var(--m-low);
   556	       transition:transform var(--m-press) var(--m-ease),background var(--m-out) var(--m-ease)}
   557	.m-btn:active{transform:scale(.97)}
   558	@media (hover:hover) and (pointer:fine){ .m-btn:hover{background:var(--m-page)} }
   559	.m-btn--primary{background:var(--m-ac);color:#fff;box-shadow:0 1px 2px rgba(47,107,255,.35)}
   560	@media (hover:hover) and (pointer:fine){ .m-btn--primary:hover{background:var(--m-ac-deep)} }
   561	.m-btn--primary:active{background:var(--m-ac-deep)}
   562	.m-btn--icon{padding:9px;inline-size:36px;block-size:36px;justify-content:center}
   563	.m-btn--quiet{background:transparent;box-shadow:none;color:var(--m-ac-deep);padding-inline:6px}
   564	.m-btn[disabled]{color:var(--m-faint);cursor:not-allowed;background:var(--m-sunk);box-shadow:none}
   565	.m-btn:focus-visible{outline:none;box-shadow:var(--m-focus),var(--m-low)}
   566	.m-link{font-size:var(--m-t-cap);font-weight:600;color:var(--m-ac-deep);text-decoration:none}
   567	@media (hover:hover) and (pointer:fine){ .m-link:hover{text-decoration:underline} }
   568	
   569	/* ------------------------------------------------------------------ ALERT */
   570	.m-alert{display:flex;align-items:center;gap:var(--m-3);flex-wrap:wrap;
   571	         background:var(--m-warn-dim);border-radius:var(--m-r-card);
   572	         padding:var(--m-3) var(--m-4);box-shadow:0 0 0 1px var(--m-warn-line)}
   573	.m-alert__t{font-size:var(--m-t-body);font-weight:700;color:var(--m-warn)}
   574	.m-alert__d{font-size:var(--m-t-cap);color:var(--m-ink-2);flex:1 1 240px}
   575	
   576	/* ------------------------------------------------------------------ EMPTY */
   577	.m-empty{padding:var(--m-6) var(--m-5);text-align:center}
   578	.m-empty__t{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink)}
   579	.m-empty__d{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:var(--m-2);
   580	            max-inline-size:52ch;margin-inline:auto;line-height:1.75}
   581	.m-empty__a{margin-block-start:var(--m-4)}
   582	.m-nil{color:var(--m-faint);font-size:var(--m-t-cap)}
   583	
   584	/* --------------------------------------------------------------- LAYOUT */
   585	.m-grid{display:grid;gap:var(--m-4)}
   586	.m-grid--main{grid-template-columns:minmax(0,1fr) 340px}
   587	.m-grid--3{grid-template-columns:repeat(3,minmax(0,1fr))}
   588	@media (max-width:1180px){ .m-grid--main{grid-template-columns:1fr} }
   589	@media (max-width:980px){ .m-grid--3{grid-template-columns:1fr} }
   590	.m-between{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3)}
   591	.m-row{display:flex;align-items:center;gap:var(--m-2)}
   592	.m-cap{font-size:var(--m-t-cap);color:var(--m-mut)}
   593	.m-rel{position:relative}
   594	
   595	/* ============================================================================
   596	   INDICATORS — a different chart vocabulary
   597	   ----------------------------------------------------------------------------
   598	   Bars and lines answer «how much, over time». Massar's indicators mostly
   599	   answer other questions — «how ready», «how many of what kind», «where does
   600	   it leak», «is anything happening» — and drawing all four as bars is what
   601	   made every earlier dashboard read the same. Each shape below is chosen for
   602	   the QUESTION it answers:
   603	     arc      → a bounded score (0-100). The gap in the ring IS the shortfall.
   604	     matrix   → a count of things you could point at. One dot is one record.
   605	     funnel   → where a population leaks between stages.
   606	     heat     → whether anything happened, per day, over a window.
   607	     meter    → one record's standing on a scale, with its own evidence.
   608	   ========================================================================== */
   609	
   610	/* ARC GAUGE — a bounded score. Drawn with stroke-dasharray on a semicircle,
   611	   so the empty part of the ring is visibly the part not earned. */
   612	.m-arc{position:relative;inline-size:100%;max-inline-size:200px;margin-inline:auto}
   613	.m-arc svg{display:block;inline-size:100%;block-size:auto;overflow:visible}
   614	.m-arc__track{fill:none;stroke:var(--m-sunk);stroke-width:14;stroke-linecap:round}
   615	.m-arc__fill{fill:none;stroke:var(--m-ac);stroke-width:14;stroke-linecap:round;
   616	             stroke-dasharray:var(--m-dash,0) 999;
   617	             animation:m-arc 900ms var(--m-ease) both}
   618	.m-arc__fill--warn{stroke:var(--m-warn)}
   619	.m-arc__fill--bad{stroke:var(--m-bad)}
   620	.m-arc__fill--ok{stroke:var(--m-ok)}
   621	@keyframes m-arc{from{stroke-dasharray:0 999}}
   622	@media (prefers-reduced-motion:reduce){ .m-arc__fill{animation:none} }
   623	.m-arc__c{position:absolute;inset-inline:0;inset-block-end:6%;text-align:center}
   624	.m-arc__v{font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
   625	          letter-spacing:-1.5px;line-height:1;font-variant-numeric:tabular-nums}
   626	.m-arc__k{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:var(--m-1)}
   627	
   628	/* DOT MATRIX — one dot is one record, so a count you can point at rather
   629	   than a bar whose height you have to decode. */
   630	.m-matrix{display:flex;flex-wrap:wrap;gap:5px;margin-block:var(--m-3)}
   631	.m-matrix i{inline-size:12px;block-size:12px;border-radius:4px;background:var(--m-sunk)}
   632	.m-matrix i.is-ok{background:var(--m-ok-line)}
   633	.m-matrix i.is-ac{background:var(--m-ac)}
   634	.m-matrix i.is-warn{background:var(--m-warn-line)}
   635	.m-matrix i.is-bad{background:var(--m-bad-line)}
   636	.m-matrix i.is-idle{background:var(--m-line-2)}
   637	.m-key{display:flex;gap:var(--m-4);flex-wrap:wrap;font-size:var(--m-t-cap);color:var(--m-mut)}
   638	.m-key span{display:inline-flex;align-items:center;gap:6px}
   639	.m-key i{inline-size:10px;block-size:10px;border-radius:3px}
   640	
   641	/* FUNNEL — stepped bars that narrow, so a leak is visible as a step change
   642	   rather than as two numbers you have to subtract. */
   643	.m-funnel{display:flex;flex-direction:column;gap:var(--m-2)}
   644	.m-fstep{display:grid;grid-template-columns:104px 1fr auto;align-items:center;gap:var(--m-3)}
   645	.m-fstep__k{font-size:var(--m-t-cap);color:var(--m-mut)}
   646	.m-fstep__b{block-size:30px;border-radius:var(--m-r-ctl);background:var(--m-sunk);
   647	            position:relative;overflow:hidden}
   648	.m-fstep__b i{position:absolute;inset-block:0;inset-inline-start:0;inline-size:var(--m-pct,0%);
   649	              background:linear-gradient(90deg,var(--m-ac),var(--m-vi));border-radius:var(--m-r-ctl);
   650	              animation:m-fgrow 700ms var(--m-ease) both}
   651	@keyframes m-fgrow{from{inline-size:0}}
   652	@media (prefers-reduced-motion:reduce){ .m-fstep__b i{animation:none} }
   653	.m-fstep__v{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
   654	            font-variant-numeric:tabular-nums;min-inline-size:56px;text-align:start}
   655	.m-fstep__d{font-size:var(--m-t-micro);color:var(--m-bad);font-weight:600}
   656	
   657	/* HEAT STRIP — did anything happen, per day. Absence is the signal here, so
   658	   an empty cell must be legible as «nothing», not as «no data». */
   659	.m-heat{display:flex;gap:4px;margin-block:var(--m-3)}
   660	.m-heat i{flex:1 1 auto;block-size:34px;border-radius:5px;background:var(--m-sunk)}
   661	.m-heat i.l1{background:var(--m-ac-line)}
   662	.m-heat i.l2{background:#9CC0FF}
   663	.m-heat i.l3{background:var(--m-ac)}
   664	.m-heat__ax{display:flex;justify-content:space-between;font-size:var(--m-t-micro);
   665	            color:var(--m-faint)}
   666	
   667	/* METER — one record on a 0-100 scale, with the threshold marked. */
   668	.m-meter{block-size:10px;border-radius:99px;background:var(--m-sunk);position:relative;
   669	         margin-block:var(--m-3) var(--m-2)}
   670	.m-meter i{position:absolute;inset-block:0;inset-inline-start:0;inline-size:var(--m-pct,0%);
   671	           border-radius:99px;background:linear-gradient(90deg,var(--m-ac),var(--m-vi))}
   672	.m-meter b{position:absolute;inset-block:-4px;inset-inline-start:var(--m-mark,50%);
   673	           inline-size:2px;background:var(--m-ink);opacity:.35}
   674	
   675	/* RING SEGMENTS — a weighted score built of named sections, each drawn as its
   676	   own arc segment so a low section is findable, not averaged away. */
   677	.m-segs{display:flex;flex-direction:column;gap:var(--m-2)}
   678	.m-seg-row{display:grid;grid-template-columns:1fr 92px 44px;align-items:center;gap:var(--m-3);
   679	           font-size:var(--m-t-cap)}
   680	.m-seg-row__t{color:var(--m-ink-2)}
   681	.m-seg-row__b{block-size:6px;border-radius:99px;background:var(--m-sunk);overflow:hidden}
   682	.m-seg-row__b i{display:block;block-size:100%;inline-size:var(--m-pct,0%);border-radius:99px;
   683	                background:var(--m-ac)}
   684	.m-seg-row__b i.low{background:var(--m-bad)}
   685	.m-seg-row__b i.mid{background:var(--m-warn)}
   686	.m-seg-row__v{font-weight:700;color:var(--m-ink);font-variant-numeric:tabular-nums;text-align:start}
   687	
   688	/* ============================================================================
   689	   THE MONEY CARD — a filtered figure that can switch how it is drawn
   690	   ----------------------------------------------------------------------------
   691	   The reader is money-first and detail-oriented, so the card leads with the
   692	   booked figure, states it against the same period's requirement, and lets the
   693	   same data be read as a CHART or as a LIST without reloading. The swap is a
   694	   crossfade with a small vertical offset and a blur — blur bridges the two
   695	   states so the eye reads one object changing rather than two objects
   696	   swapping (emil-design-eng: "use blur to mask imperfect transitions").
   697	   ========================================================================== */
   698	.m-view{position:relative}
   699	.m-view__p{transition:opacity var(--m-swap) var(--m-ease),
   700	                      transform var(--m-swap) var(--m-ease),
   701	                      filter var(--m-swap) var(--m-ease)}
   702	.m-view__p[hidden]{display:none!important}
   703	.m-view__p[data-enter]{opacity:0;transform:translateY(6px);filter:blur(3px)}
   704	@media (prefers-reduced-motion:reduce){
   705	  .m-view__p[data-enter]{transform:none;filter:none} }
   706	
   707	/* DATE FILTER — presets plus a custom range. */
   708	.m-dates{display:flex;align-items:center;gap:var(--m-2);flex-wrap:wrap}
   709	.m-range{display:flex;align-items:center;gap:var(--m-2);background:var(--m-paper);
   710	         border-radius:var(--m-r-chip);padding:5px 6px 5px var(--m-3);box-shadow:var(--m-hair)}
   711	.m-range input{font:inherit;font-size:var(--m-t-cap);color:var(--m-ink);border:0;
   712	               background:transparent;padding:3px;inline-size:126px;
   713	               font-variant-numeric:tabular-nums}
   714	.m-range input:focus{outline:none;box-shadow:var(--m-focus);border-radius:6px}
   715	.m-range span{color:var(--m-faint);font-size:var(--m-t-cap)}
   716	
   717	/* QUARTER STRIP — four cells, the current one marked. */
   718	.m-qs{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--m-line);
   719	      border-radius:var(--m-r-card);overflow:hidden;box-shadow:var(--m-hair)}
   720	.m-q{background:var(--m-paper);padding:var(--m-3) var(--m-4);cursor:pointer;
   721	     transition:background var(--m-out) var(--m-ease)}
   722	@media (hover:hover) and (pointer:fine){ .m-q:hover{background:var(--m-page)} }
   723	.m-q__k{font-size:var(--m-t-cap);color:var(--m-mut);display:flex;align-items:center;gap:6px}
   724	.m-q__k i{inline-size:6px;block-size:6px;border-radius:50%;background:var(--m-ac)}
   725	.m-q__v{font-size:var(--m-t-fig);font-weight:800;color:var(--m-ink);letter-spacing:-.8px;
   726	        margin-block-start:2px;font-variant-numeric:tabular-nums}
   727	.m-q__v.nil{color:var(--m-faint)}
   728	.m-q__s{font-size:var(--m-t-micro);color:var(--m-faint);margin-block-start:2px}
   729	.m-q__b{block-size:4px;border-radius:99px;background:var(--m-sunk);margin-block-start:var(--m-2);
   730	        overflow:hidden}
   731	.m-q__b i{display:block;block-size:100%;inline-size:var(--m-pct,0%);border-radius:99px;
   732	          background:var(--m-ac);transition:inline-size var(--m-in) var(--m-move)}
   733	.m-q[aria-current]{background:var(--m-ac-dim)}
   734	.m-q[aria-current] .m-q__k{color:var(--m-ac-deep);font-weight:600}
   735	
   736	/* The list rendering of the same series the chart draws. */
   737	.m-mini{inline-size:100%;border-collapse:collapse}
   738	.m-mini th{font-size:var(--m-t-micro);font-weight:600;color:var(--m-mut);text-align:start;
   739	           padding:var(--m-2) var(--m-3);border-block-end:1px solid var(--m-line)}
   740	.m-mini td{padding:9px var(--m-3);border-block-start:1px solid var(--m-line);
   741	           font-size:var(--m-t-body);font-variant-numeric:tabular-nums}
   742	.m-mini td:first-child{color:var(--m-ink);font-weight:600;font-variant-numeric:normal}
   743	.m-mini tr[data-now]{background:var(--m-ac-dim)}
   744	.m-mini .gap{color:var(--m-bad);font-weight:600}
   745	
   746	/* A list item that is a link must not look like body copy with an underline. */
   747	a.m-item{text-decoration:none;color:inherit;
   748	         transition:background var(--m-out) var(--m-ease)}
   749	@media (hover:hover) and (pointer:fine){ a.m-item:hover{background:var(--m-page)} }
   750	a.m-item:focus-visible{outline:none;box-shadow:var(--m-focus);border-radius:var(--m-r-ctl)}
   751	.m-item__b{display:block}
   752	.m-item__n,.m-item__s{display:block}
   753	/* Columns size to their content; a short stack must not leave a tall well. */
   754	.m-board{align-items:flex-start}
   755	.m-col{align-self:flex-start}
   756	.m-col--rail{align-self:stretch;min-block-size:150px}
   757	
   758	/* The brand name and the role are two lines, not one run-on string. */
   759	.m-side__n,.m-side__r{display:block}
   760	.m-crumb a{color:inherit;text-decoration:none}
   761	@media (hover:hover) and (pointer:fine){ .m-crumb a:hover{color:var(--m-ac-deep)} }
   762	
   763	/* ============================================================================
   764	   DIALOG — the add/edit surface
   765	   Enters from scale(.97) with a small lift, never from scale(0): nothing in
   766	   the real world appears from nothing. Exit is faster than enter.
   767	   ========================================================================== */
   768	dialog.m-dlg{border:0;padding:0;background:transparent;max-inline-size:min(680px,92vw);
   769	             inline-size:100%}
   770	dialog.m-dlg::backdrop{background:rgba(11,13,18,.44);backdrop-filter:blur(2px);
   771	                       animation:m-fade 200ms var(--m-ease)}
   772	@keyframes m-fade{from{opacity:0}}
   773	.m-dlg__p{background:var(--m-paper);border-radius:var(--m-r-band);box-shadow:var(--m-lift);
   774	          animation:m-pop 220ms var(--m-ease)}
   775	@keyframes m-pop{from{opacity:0;transform:scale(.97) translateY(8px)}}
   776	@media (prefers-reduced-motion:reduce){
   777	  .m-dlg__p,dialog.m-dlg::backdrop{animation:none} }
   778	.m-dlg__h{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3);
   779	          padding:var(--m-4) var(--m-5);border-block-end:1px solid var(--m-line)}
   780	.m-dlg__t{margin:0;font-size:var(--m-t-h);font-weight:700;color:var(--m-ink)}
   781	.m-dlg__b{padding:var(--m-5);max-block-size:66vh;overflow-y:auto}
   782	.m-dlg__f{display:flex;justify-content:flex-end;gap:var(--m-2);
   783	          padding:var(--m-3) var(--m-5);border-block-start:1px solid var(--m-line)}
   784	.m-x{inline-size:32px;block-size:32px;border-radius:50%;border:0;cursor:pointer;
   785	     background:transparent;color:var(--m-mut);font-size:18px;line-height:1;
   786	     transition:background var(--m-out) var(--m-ease)}
   787	@media (hover:hover) and (pointer:fine){ .m-x:hover{background:var(--m-page)} }
   788	
   789	/* FORM GRID */
   790	.m-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--m-4)}
   791	.m-form .full{grid-column:1 / -1}
   792	@media (max-width:640px){ .m-form{grid-template-columns:1fr} }
   793	textarea.m-input{resize:vertical;line-height:1.7}
   794	.m-req::after{content:"*";color:var(--m-bad);margin-inline-start:3px}
   795	
   796	/* KNOWLEDGE / long-text editor */
   797	.m-kb{display:grid;grid-template-columns:260px minmax(0,1fr);gap:var(--m-4)}
   798	@media (max-width:900px){ .m-kb{grid-template-columns:1fr} }
   799	.m-kb__l{display:flex;flex-direction:column;gap:2px}
   800	.m-kb__i{display:flex;align-items:center;justify-content:space-between;gap:var(--m-2);
   801	         padding:9px var(--m-3);border-radius:var(--m-r-ctl);border:0;background:transparent;
   802	         cursor:pointer;font:inherit;font-size:var(--m-t-body);color:var(--m-ink-2);
   803	         text-align:start;transition:background var(--m-out) var(--m-ease)}
   804	@media (hover:hover) and (pointer:fine){ .m-kb__i:hover{background:var(--m-page)} }
   805	.m-kb__i[aria-current]{background:var(--m-ac-dim);color:var(--m-ac-deep);font-weight:600}
   806	.m-kb__i b{font-size:var(--m-t-micro);font-weight:700;font-variant-numeric:tabular-nums}
   807	.m-kb__i b.low{color:var(--m-bad)} .m-kb__i b.mid{color:var(--m-warn)} .m-kb__i b.ok{color:var(--m-ok)}
   808	
   809	/* STEPPER — the campaign wizard */
   810	.m-steps{display:flex;gap:var(--m-2);margin-block-end:var(--m-5);flex-wrap:wrap}
   811	.m-step{display:flex;align-items:center;gap:var(--m-2);font-size:var(--m-t-cap);
   812	        color:var(--m-faint)}
   813	.m-step i{inline-size:22px;block-size:22px;border-radius:50%;display:grid;place-items:center;
   814	          font-size:var(--m-t-micro);font-weight:700;background:var(--m-sunk);color:var(--m-mut);
   815	          font-variant-numeric:tabular-nums}
   816	.m-step[aria-current]{color:var(--m-ink);font-weight:600}
   817	.m-step[aria-current] i{background:var(--m-ac);color:#fff}
   818	.m-step[data-done] i{background:var(--m-ok-dim);color:var(--m-ok)}
   819	.m-step::after{content:"";inline-size:22px;block-size:1px;background:var(--m-line-2)}
   820	.m-step:last-child::after{display:none}
   821	
   822	/* TIMELINE — the event ledger */
   823	.m-tl{display:flex;flex-direction:column}
   824	.m-tl__i{display:grid;grid-template-columns:22px minmax(0,1fr) auto;gap:var(--m-3);
   825	         padding:var(--m-3) 0;position:relative}
   826	.m-tl__d{inline-size:9px;block-size:9px;border-radius:50%;background:var(--m-ac);
   827	         margin-block-start:6px;margin-inline-start:6px;position:relative;z-index:1}
   828	.m-tl__d.ok{background:var(--m-ok)} .m-tl__d.warn{background:var(--m-warn)}
   829	.m-tl__d.idle{background:var(--m-line-2)}
   830	.m-tl__i:not(:last-child)::before{content:"";position:absolute;inset-block:22px -6px;
   831	         inset-inline-start:10px;inline-size:1px;background:var(--m-line)}
   832	.m-tl__n{font-size:var(--m-t-body);color:var(--m-ink)}
   833	.m-tl__s{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-start:2px}
   834	.m-tl__t{font-size:var(--m-t-micro);color:var(--m-faint);white-space:nowrap;
   835	         font-variant-numeric:tabular-nums}
   836	
   837	/* TOGGLE */
   838	.m-sw{inline-size:38px;block-size:22px;border-radius:99px;background:var(--m-line-2);
   839	      border:0;cursor:pointer;padding:0;position:relative;flex:0 0 auto;
   840	      transition:background var(--m-out) var(--m-ease)}
   841	.m-sw::after{content:"";position:absolute;inset-block-start:3px;inset-inline-start:3px;
   842	      inline-size:16px;block-size:16px;border-radius:50%;background:#fff;
   843	      box-shadow:0 1px 2px rgba(16,24,40,.2);
   844	      transition:transform var(--m-swap) var(--m-ease)}
   845	.m-sw[aria-checked="true"]{background:var(--m-ac)}
   846	.m-sw[aria-checked="true"]::after{transform:translateX(-16px)}
   847	
   848	/* KPI GRID for the merged home */
   849	.m-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--m-3)}
   850	@media (max-width:1100px){ .m-kpis{grid-template-columns:repeat(2,minmax(0,1fr))} }
   851	@media (max-width:560px){ .m-kpis{grid-template-columns:1fr} }

exec
/bin/zsh -lc 'nl -ba massar-ds/home.html' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
     1	<!doctype html>
     2	<html lang="ar" dir="rtl">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
     6	<title>مسار — الرئيسية</title>
     7	<link rel="preconnect" href="https://fonts.googleapis.com">
     8	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     9	<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    10	<link rel="stylesheet" href="massar.css">
    11	</head>
    12	<body data-nav="home" data-sub="home">
    13	<div class="m-shell">
    14	  <div class="m-main">
    15	    <div class="m-bar">
    16	      <div class="m-search">
    17	        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    18	        بحث
    19	        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
    20	      </div>
    21	      <div class="m-head__a"><button class="m-btn">تصدير</button><button class="m-btn m-btn--primary" data-open="dlgOpp">فرصة جديدة</button></div>
    22	    </div>
    23	    <main class="m-page">
    24	      <div class="m-head">
    25	        <div>
    26	          <div class="m-crumb">الرئيسية</div>
    27	          <h1 class="m-h1">الأداء التجاري</h1>
    28	        </div>
    29	        <div class="m-row"><div class="m-dates"><div class="m-seg" role="group" aria-label="المدى الزمني"><button data-p="7" aria-pressed="false">أسبوع</button><button data-p="14" aria-pressed="false">أسبوعان</button><button data-p="30" aria-pressed="false">شهر</button><button data-p="q" aria-pressed="false">الربع</button><button data-p="year" aria-pressed="true">السنة</button></div><label class="m-range"><input type="date" id="d1" value="2026-01-01" aria-label="من"><span>—</span><input type="date" id="d2" value="2026-09-16" aria-label="إلى"></label></div></div>
    30	      </div>
    31	      <div data-subs></div>
    32	      <div style="margin-block-start:var(--m-4)">
    33	
    34	<!-- THE MONEY CARD — filtered, and switchable between chart and list -->
    35	<section class="m-card m-card--band">
    36	  <div class="m-between" style="align-items:flex-start;flex-wrap:wrap;gap:var(--m-4)">
    37	    <div>
    38	      <div class="m-card__k" id="periodLabel">المحقق · السنة المالية 2026</div>
    39	      <div class="m-lead" style="margin-block-start:var(--m-2)">
    40	        <div class="m-lead__v"><span class="m-n" id="bookedV">0</span><small>ر.س</small></div>
    41	        <span class="m-delta m-delta--bad" id="deltaPill">&#9662; <span class="m-n">34,000</span> ر.س دون المطلوب</span>
    42	      </div>
    43	    </div>
    44	    <div class="m-row" style="align-items:flex-start;gap:var(--m-5);flex-wrap:wrap">
    45	      <div class="m-stat"><div class="m-stat__k">المطلوب</div>
    46	        <div class="m-stat__v"><span class="m-n" id="targetV">34,000</span></div></div>
    47	      <div class="m-stat m-stat--ac"><div class="m-stat__k">خط البيع</div>
    48	        <div class="m-stat__v"><span class="m-n" id="openV">4,200</span></div></div>
    49	      <div class="m-stat m-stat--mut"><div class="m-stat__k">صفقات رابحة</div>
    50	        <div class="m-stat__v"><span class="m-n">0</span></div></div>
    51	      <div class="m-seg" role="group" aria-label="طريقة العرض">
    52	        <button data-v="chart" aria-pressed="true">رسم</button>
    53	        <button data-v="list" aria-pressed="false">قائمة</button>
    54	      </div>
    55	    </div>
    56	  </div>
    57	  <div class="m-view" style="margin-block-start:var(--m-4)">
    58	    <div class="m-view__p" id="vChart">
    59	      <svg class="m-chart" viewBox="0 0 900 280" role="img" aria-label="المطلوب شهريًا مقابل المحقق">
    60	        <defs>
    61	          <linearGradient id="mBar" x1="0" y1="0" x2="0" y2="1">
    62	            <stop offset="0%" stop-color="#2F6BFF" stop-opacity=".28"/>
    63	            <stop offset="100%" stop-color="#2F6BFF" stop-opacity="0"/></linearGradient>
    64	          <pattern id="mDots" width="14" height="14" patternUnits="userSpaceOnUse">
    65	            <circle cx="1.5" cy="1.5" r="1.5" fill="#E4E8F0"/></pattern>
    66	        </defs>
    67	        <rect x="56" y="18" width="816" height="200" fill="url(#mDots)"/>
    68	        <g id="bars"></g><line x1="56" y1="218" x2="872" y2="218" stroke="#DFE3EA"/><g id="axis"></g>
    69	      </svg>
    70	    </div>
    71	    <div class="m-view__p" id="vList" hidden>
    72	      <table class="m-mini"><thead><tr><th>الشهر</th><th>المطلوب</th><th>المحقق</th>
    73	      <th>الفجوة</th><th>فرص أُنشئت</th></tr></thead><tbody id="listBody"></tbody></table>
    74	    </div>
    75	  </div>
    76	</section>
    77	
    78	<div class="m-qs" style="margin-block-start:var(--m-4)" id="quarters"></div>
    79	<div class="m-grid m-grid--3" style="margin-block-start:var(--m-4)"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">جاهزية المساعد</h2><span class="m-chip m-chip--bad">غير جاهز</span></div><div class="m-arc"><svg viewBox="0 0 200 116" role="img" aria-label="جاهزية المساعد 34"><path class="m-arc__track" d="M18,104 A82,82 0 0 1 182,104"/><path class="m-arc__fill m-arc__fill--warn" style="--m-dash:88" d="M18,104 A82,82 0 0 1 182,104"/></svg><div class="m-arc__c"><div class="m-arc__v"><span class="m-n">34</span></div><div class="m-arc__k">من <span class="m-n">100</span></div></div></div><div class="m-segs"><div class="m-seg-row"><span class="m-seg-row__t">وصف المنتج</span><span class="m-seg-row__b"><i class="ok" style="--m-pct:80%"></i></span><span class="m-seg-row__v"><span class="m-n">80%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">حالات الاستخدام</span><span class="m-seg-row__b"><i class="mid" style="--m-pct:60%"></i></span><span class="m-seg-row__v"><span class="m-n">60%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">الأسئلة الشائعة</span><span class="m-seg-row__b"><i class="mid" style="--m-pct:45%"></i></span><span class="m-seg-row__v"><span class="m-n">45%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">الأسعار والباقات</span><span class="m-seg-row__b"><i class="low" style="--m-pct:10%"></i></span><span class="m-seg-row__v"><span class="m-n">10%</span></span></div></div><div class="m-empty__a"><a class="m-link" href="knowledge.html">كل الأقسام &#8592;</a></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">صحة خط البيع</h2></div><div class="m-matrix" aria-hidden="true"><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i></div><div class="m-key"><span><i style="background:var(--m-ac)"></i>على المسار <span class="m-n">6</span></span><span><i style="background:var(--m-warn-line)"></i>متأخرة <span class="m-n">0</span></span><span><i style="background:var(--m-line-2)"></i>بانتظار الدعم <span class="m-n">0</span></span><span><i style="background:var(--m-bad-line)"></i>مرفوضة <span class="m-n">0</span></span></div><div class="m-card__h" style="margin-block:var(--m-5) var(--m-3)"><h2 class="m-card__t">العملاء</h2></div><div class="m-matrix" aria-hidden="true"><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i></div><div class="m-key"><span><i style="background:var(--m-ok-line)"></i>معتمد <span class="m-n">16</span></span><span><i style="background:var(--m-line-2)"></i>بانتظار <span class="m-n">0</span></span><span><i style="background:var(--m-bad-line)"></i>مرفوض <span class="m-n">0</span></span></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">النشاط · <span class="m-n">21</span> يومًا</h2><span class="m-chip m-chip--bad">صامت</span></div><div class="m-heat" aria-hidden="true"><i class="l3"></i><i class="l2"></i><i class="l1"></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="m-heat__ax"><span>اليوم</span><span>قبل <span class="m-n">21</span> يومًا</span></div><div class="m-card__h" style="margin-block:var(--m-5) var(--m-3)"><h2 class="m-card__t">قمع الحملة 38</h2></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">أُرسلت</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">21</span></span></div><div class="m-fstep"><span class="m-fstep__k">وصلت</span><span class="m-fstep__b"><i style="--m-pct:90%"></i></span><span class="m-fstep__v"><span class="m-n">19</span></span></div><div class="m-fstep"><span class="m-fstep__k">شوهدت</span><span class="m-fstep__b"><i style="--m-pct:57%"></i></span><span class="m-fstep__v"><span class="m-n">12</span> <span class="m-fstep__d">&#9662; <span class="m-n">37%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">رُدّ عليها</span><span class="m-fstep__b"><i style="--m-pct:19%"></i></span><span class="m-fstep__v"><span class="m-n">4</span> <span class="m-fstep__d">&#9662; <span class="m-n">67%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">مهتم</span><span class="m-fstep__b"><i style="--m-pct:9%"></i></span><span class="m-fstep__v"><span class="m-n">2</span></span></div></div></section></div><div class="m-grid m-grid--main" style="margin-block-start:var(--m-4)"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">أين يتسرّب خط البيع</h2><a class="m-link" href="reports.html">التقارير &#8592;</a></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">تواصل أولي</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">4</span></span></div><div class="m-fstep"><span class="m-fstep__k">اكتشاف الحاجة</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span> <span class="m-fstep__d">&#9662; <span class="m-n">75%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض المنتج</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض السعر</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span></span></div><div class="m-fstep"><span class="m-fstep__k">التفاوض</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">رابح</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div></div></section><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">يحتاج قرارك</h2><span class="m-cap"><span class="m-n">4</span></span></div><a class="m-item" href="perf.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">5</span></span><span class="m-item__b"><span class="m-item__n">منتجات بلا مستهدف</span><span class="m-item__s">من <span class="m-n">6</span></span></span><span class="m-chip m-chip--warn">يشوّه النسبة</span></a><a class="m-item" href="opps.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">5</span></span><span class="m-item__b"><span class="m-item__n">بنود بلا تسعير</span><span class="m-item__s">من <span class="m-n">6</span></span></span><span class="m-chip m-chip--warn">يشوّه القيمة</span></a><a class="m-item" href="accounts.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">16</span></span><span class="m-item__b"><span class="m-item__n">عملاء بلا مسؤول</span><span class="m-item__s">من <span class="m-n">16</span></span></span><span class="m-chip">بلا متابعة</span></a><a class="m-item" href="board.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">6</span></span><span class="m-item__b"><span class="m-item__n">بنود راكدة</span><span class="m-item__s"><span class="m-n">35</span> يومًا بلا حركة</span></span><span class="m-chip m-chip--bad">متوقفة</span></a></section></div><section class="m-card m-card--pad0" style="margin-block-start:var(--m-4)"><div class="m-tools"><h2 class="m-card__t">خط البيع</h2><span class="m-row"><span class="m-cap"><span class="m-n">6</span> بنود · <span class="m-n">4,200</span> ر.س</span><a class="m-link" href="board.html">اللوحة &#8592;</a></span></div><div class="m-board" style="padding:0 var(--m-3) var(--m-3)"><div class="m-col" style="--m-tone:#5B6472"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">تواصل أولي</span><span class="m-col__c"><span class="m-n">4</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col" style="--m-tone:#0072E9"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">اكتشاف الحاجة</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#8B5CF6" tabindex="0" title="عرض المنتج"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض المنتج</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#7C3AED" tabindex="0" title="التقييم التقني"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التقييم التقني</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col" style="--m-tone:#2F6BFF"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض السعر</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v"><span class="m-n">4,200</span> ر.س</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#B45309" tabindex="0" title="التفاوض والاعتماد"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التفاوض والاعتماد</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#15803D" tabindex="0" title="رابح"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">رابح</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#BE123C" tabindex="0" title="خاسر"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">خاسر</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div></div></section>
    80	      </div>
    81	    </main>
    82	  </div>
    83	</div>
    84	<dialog class="m-dlg" id="dlgOpp"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة فرصة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">العميل</label><select class="m-select"><option>DL000</option><option>ابرهيم</option><option>العمدة</option><option>أبو حمزه</option><option>أبو نور</option><option>صيدلية الدواء</option><option>صيدلية الدواء (مثال)</option><option>صيدلية الدواء (مثال)</option></select></div><div class="m-field"><label class="m-label m-req">المنتج</label><select class="m-select"><option>الإجازات المرضية</option><option>التقارير الطبية</option><option>الشهادات الصحية</option><option>تكامل الأنظمة (HIS/ERP)</option><option>خدمات التطعيمات</option><option>سجل التطعيمات الوطني</option><option>صحة أعمال Plus</option><option>فحص الموظفين</option></select></div><div class="m-field"><label class="m-label m-req">المرحلة</label><select class="m-select"><option>تواصل أولي</option><option>اكتشاف الحاجة</option><option>عرض المنتج</option><option>التقييم التقني</option><option>عرض السعر</option><option>التفاوض والاعتماد</option></select></div><div class="m-field"><label class="m-label m-req">المصدر</label><select class="m-select"><option>حملة واتساب</option><option>مكالمة</option><option>زيارة</option><option>إحالة</option><option>طلب وارد</option></select></div><div class="m-field"><label class="m-label">الكمية</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">السعر للوحدة (ر.س)</label><input class="m-input" type="number" placeholder="لم تُسعَّر" value=""></div><div class="m-field"><label class="m-label">عدد السنوات</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">الخصم %</label><input class="m-input" type="number" placeholder="0" value=""></div><div class="m-field"><label class="m-label">الموظف المسؤول</label><select class="m-select"><option>بلا مسؤول</option></select></div><div class="m-field"><label class="m-label">تاريخ الإغلاق المتوقع</label><input class="m-input" type="date" placeholder="" value=""></div><div class="m-field"><label class="m-label">الشريك</label><select class="m-select"><option>لا شريك</option></select></div><div class="m-field full"><label class="m-label">ملاحظة</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة الفرصة</button></div></form></dialog>
    85	<script src="shell.js"></script>
    86	<script>
    87	/* ---------------------------------------------------------------------------
    88	   The ledger, as the screen knows it. Every figure below is a real value from
    89	   the live system; nothing is invented and nothing is dropped.
    90	   `won` is booked revenue, `made` is opportunity value created in the month,
    91	   `lines` is how many opportunity lines were opened.
    92	   --------------------------------------------------------------------------- */
    93	var YEAR = 2026, TARGET = 34000, MONTHLY = TARGET / 12;
    94	var M = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"];
    95	var LEDGER = [
    96	  {m:0,won:0,made:0,lines:0},{m:1,won:0,made:0,lines:0},{m:2,won:0,made:0,lines:0},
    97	  {m:3,won:0,made:0,lines:0},{m:4,won:0,made:0,lines:0},{m:5,won:0,made:0,lines:0},
    98	  {m:6,won:0,made:0,lines:0},{m:7,won:0,made:4200,lines:6},{m:8,won:0,made:0,lines:0},
    99	  {m:9,won:0,made:0,lines:0},{m:10,won:0,made:0,lines:0},{m:11,won:0,made:0,lines:0}
   100	];
   101	var TODAY = new Date(YEAR, 8, 16);           // 16 Sep 2026
   102	var fmt = function (n) { return n.toLocaleString("en-US"); };
   103	var $ = function (id) { return document.getElementById(id) || { style:{}, set textContent(v){}, set innerHTML(v){}, setAttribute:function(){}, insertAdjacentHTML:function(){}, className:"" }; };
   104	
   105	function rangeFor(preset) {
   106	  var end = new Date(TODAY), start;
   107	  if (preset === "year") start = new Date(YEAR, 0, 1);
   108	  else if (preset === "q") start = new Date(YEAR, Math.floor(TODAY.getMonth() / 3) * 3, 1);
   109	  else { start = new Date(TODAY); start.setDate(start.getDate() - (parseInt(preset, 10) - 1)); }
   110	  return [start, end];
   111	}
   112	
   113	function sum(start, end) {
   114	  // A month counts when any part of it falls inside the range. The target for
   115	  // a partial month is pro-rated by days, so «المطلوب» never overstates a
   116	  // one-week window — the reader is comparing money to money.
   117	  var won = 0, made = 0, lines = 0, req = 0;
   118	  for (var i = 0; i < 12; i++) {
   119	    var ms = new Date(YEAR, i, 1), me = new Date(YEAR, i + 1, 0);
   120	    var a = ms > start ? ms : start, b = me < end ? me : end;
   121	    if (a > b) continue;
   122	    var days = (b - a) / 86400000 + 1, full = me.getDate();
   123	    req += MONTHLY * (days / full);
   124	    won += LEDGER[i].won; made += LEDGER[i].made; lines += LEDGER[i].lines;
   125	  }
   126	  return { won: won, made: made, lines: lines, req: Math.round(req) };
   127	}
   128	
   129	function label(start, end, preset) {
   130	  if (preset === "year") return "المحقق · السنة المالية " + YEAR;
   131	  if (preset === "q") return "المحقق · الربع " + (Math.floor(TODAY.getMonth() / 3) + 1) + " · " + YEAR;
   132	  return "المحقق · " + start.getDate() + " " + M[start.getMonth()] +
   133	         " — " + end.getDate() + " " + M[end.getMonth()];
   134	}
   135	
   136	function paint(preset, start, end) {
   137	  var s = sum(start, end);
   138	  $("periodLabel").textContent = label(start, end, preset);
   139	  $("bookedV").textContent = fmt(s.won);
   140	  $("targetV").textContent = fmt(s.req);
   141	  $("openV").textContent   = fmt(s.made);
   142	  $("wonV").textContent    = "0";
   143	
   144	  var gap = s.req - s.won;
   145	  var pill = $("deltaPill");
   146	  pill.className = "m-delta " + (gap > 0 ? "m-delta--bad" : "m-delta--ok");
   147	  pill.innerHTML = gap > 0
   148	    ? '▾ <span class="m-n">' + fmt(gap) + '</span> ر.س دون المطلوب'
   149	    : '▴ مطابق للمطلوب';
   150	
   151	  // bars: required per month; the cap dot marks what was booked
   152	  var bars = $("bars"), axis = $("axis");
   153	  bars.innerHTML = ""; axis.innerHTML = "";
   154	  var max = Math.max(MONTHLY * 1.25, 1), x0 = 872, step = 68;
   155	  for (var i = 0; i < 12; i++) {
   156	    var x = x0 - i * step - 26;                       // RTL: يناير at the right
   157	    var inR = new Date(YEAR, i, 15) >= start && new Date(YEAR, i, 15) <= end;
   158	    var hReq = Math.round(200 * (MONTHLY / max));
   159	    bars.insertAdjacentHTML("beforeend",
   160	      '<rect class="m-chart__bar" x="' + x + '" y="' + (218 - hReq) + '" width="26" height="' +
   161	      hReq + '" rx="13" opacity="' + (inR ? 1 : .3) + '"/>' +
   162	      '<circle r="5" cx="' + (x + 13) + '" cy="218" fill="' + (inR ? "#BE123C" : "#DFE3EA") + '"/>');
   163	    if (i % 2 === 0) axis.insertAdjacentHTML("beforeend",
   164	      '<text class="m-chart__ax" x="' + (x + 13) + '" y="242" text-anchor="middle">' + M[i] + "</text>");
   165	  }
   166	
   167	  // list: the same series, read as a table
   168	  var rows = "";
   169	  for (var j = 0; j < 12; j++) {
   170	    var inR2 = new Date(YEAR, j, 15) >= start && new Date(YEAR, j, 15) <= end;
   171	    if (!inR2) continue;
   172	    rows += '<tr' + (j === TODAY.getMonth() ? ' data-now' : '') + '><td>' + M[j] + "</td>" +
   173	      '<td class="m-n">' + fmt(Math.round(MONTHLY)) + "</td>" +
   174	      '<td class="m-n">' + fmt(LEDGER[j].won) + "</td>" +
   175	      '<td class="m-n gap">' + fmt(Math.round(MONTHLY) - LEDGER[j].won) + "</td>" +
   176	      '<td class="m-n">' + (LEDGER[j].lines || "—") + "</td></tr>";
   177	  }
   178	  $("listBody").innerHTML = rows;
   179	}
   180	
   181	function paintQuarters() {
   182	  var q = $("quarters"), cur = Math.floor(TODAY.getMonth() / 3), out = "";
   183	  for (var i = 0; i < 4; i++) {
   184	    var won = 0, req = 0;
   185	    for (var m = i * 3; m < i * 3 + 3; m++) { won += LEDGER[m].won; req += MONTHLY; }
   186	    var pct = req ? Math.round((won / req) * 100) : 0;
   187	    out += '<button class="m-q" type="button"' + (i === cur ? ' aria-current="true"' : '') + '>' +
   188	      '<span class="m-q__k">' + (i === cur ? "<i></i>" : "") + "الربع " + (i + 1) + "</span>" +
   189	      '<div class="m-q__v' + (won ? "" : " nil") + '"><span class="m-n">' + fmt(won) + "</span></div>" +
   190	      '<div class="m-q__s">من <span class="m-n">' + fmt(Math.round(req)) +
   191	        '</span> ر.س · <span class="m-n">' + pct + '%</span></div>' +
   192	      '<div class="m-q__b"><i style="--m-pct:' + pct + '%"></i></div></button>';
   193	  }
   194	  q.innerHTML = out;
   195	}
   196	
   197	/* presets */
   198	var presets = document.querySelectorAll('[data-p]');
   199	presets.forEach(function (b) {
   200	  b.addEventListener("click", function () {
   201	    presets.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
   202	    b.setAttribute("aria-pressed", "true");
   203	    var r = rangeFor(b.dataset.p);
   204	    $("d1").value = r[0].toISOString().slice(0, 10);
   205	    $("d2").value = r[1].toISOString().slice(0, 10);
   206	    paint(b.dataset.p, r[0], r[1]);
   207	  });
   208	});
   209	["d1", "d2"].forEach(function (id) {
   210	  $(id).addEventListener("change", function () {
   211	    presets.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
   212	    paint("custom", new Date($("d1").value), new Date($("d2").value));
   213	  });
   214	});
   215	
   216	/* chart <-> list, crossfaded. Blur bridges the two states so the eye reads one
   217	   object changing rather than two objects swapping. */
   218	var views = document.querySelectorAll('[data-v]');
   219	views.forEach(function (b) {
   220	  b.addEventListener("click", function () {
   221	    views.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
   222	    b.setAttribute("aria-pressed", "true");
   223	    var show = b.dataset.v === "chart" ? $("vChart") : $("vList");
   224	    var hide = b.dataset.v === "chart" ? $("vList") : $("vChart");
   225	    hide.hidden = true;
   226	    show.hidden = false;
   227	    show.setAttribute("data-enter", "");
   228	    void show.offsetWidth;                 // force the start state to land
   229	    show.removeAttribute("data-enter");
   230	  });
   231	});
   232	
   233	paintQuarters();
   234	paint("year", new Date(YEAR, 0, 1), TODAY);
   235	</script>
   236	</body>
   237	</html>

exec
/bin/zsh -lc 'nl -ba massar-ds/products.html
nl -ba massar-ds/product.html
nl -ba massar-ds/opps.html
nl -ba massar-ds/reports.html' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
     1	<!doctype html>
     2	<html lang="ar" dir="rtl">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
     6	<title>مسار — المنتجات</title>
     7	<link rel="preconnect" href="https://fonts.googleapis.com">
     8	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     9	<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    10	<link rel="stylesheet" href="massar.css">
    11	</head>
    12	<body data-nav="products" data-sub="products">
    13	<div class="m-shell">
    14	  <div class="m-main">
    15	    <div class="m-bar">
    16	      <div class="m-search">
    17	        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    18	        بحث
    19	        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
    20	      </div>
    21	      <div class="m-head__a"><button class="m-btn">استيراد</button><button class="m-btn m-btn--primary" data-open="dlgProd">إضافة منتج</button></div>
    22	    </div>
    23	    <main class="m-page">
    24	      <div class="m-head">
    25	        <div>
    26	          <div class="m-crumb">المنتجات</div>
    27	          <h1 class="m-h1">المنتجات</h1>
    28	        </div>
    29	        <div class="m-row"><select class="m-select" style="inline-size:auto"><option>كل القطاعات</option><option>بلا قطاع</option><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option></select><select class="m-select" style="inline-size:auto"><option>كل الحالات</option><option>لا يبيعها المساعد</option><option>يبيعها وتنقصها أشياء</option><option>جاهزة للمساعد</option></select><select class="m-select" style="inline-size:auto"><option>حسب الاسم</option><option>الأعلى تحقيقًا</option><option>الأعلى مفتوحًا</option><option>غير الجاهزة أولًا</option></select><button class="m-btn">المؤرشفة</button></div>
    30	      </div>
    31	      <div data-subs></div>
    32	      <div style="margin-block-start:var(--m-4)">
    33	<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">المحقق 2026</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">من مستهدف 34,000 ر.س · 0٪</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">لا يبيعها المساعد</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">من 8 منتجات</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">بلا سعر منشور</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">من 8 منتجات</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">قطاع مُستنتَج</div><div class="m-q__v"><span class="m-n">4</span></div><div class="m-q__s">تحتاج تأكيدًا</div></div></div><div class="m-alert" style="margin-block-end:var(--m-4)"><span class="m-alert__t"><span class="m-n">6</span> منتجات بلا ملف تعريفي</span><span class="m-alert__d">مهارة إعداد العرض تُنتجه بمساعد ذكاء اصطناعي · <code style="font-family:monospace;font-size:var(--m-t-micro)">lean-proposal-deck-v2.3.1-upload.zip</code></span><button class="m-btn">تحميل المهارة</button></div><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المنتج</th><th>جاهزية المساعد</th><th>السعر المنشور</th><th>المستهدف 2026</th><th>المحقق</th><th>المفتوح الآن</th><th></th></tr></thead><tbody><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">الإجازات المرضية</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--ok"><span class="m-n">80%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-v">18,000 ر.س / سنة</span><div class="m-item__s">يبدأ من · باقتان</div></td><td><span class="m-td-v"><span class="m-n">34,000</span> ر.س</span><div class="m-item__s">ربع واحد من أربعة</div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-v"><span class="m-n">4,200</span> ر.س</span><div class="m-item__s">بندان · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">التقارير الطبية</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--warn"><span class="m-n">68%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص وفق الحجم</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">الشهادات الصحية</span></a><div class="m-item__s">قطاع الصيدليات</div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">تكامل الأنظمة (HIS/ERP)</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">مشروع تكامل واشتراك سنوي، يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بندان · بندان بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">خدمات التطعيمات</span></a><div class="m-item__s">قطاع الصيدليات · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بند واحد · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">سجل التطعيمات الوطني</span></a><div class="m-item__s">قطاع الصيدليات · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--ok"><span class="m-n">90%</span></span><span class="m-cap">يبيعه المساعد · ينقصه تحديث كتالوج المساعد</span></span></td><td><span class="m-td-v">20,000 ر.س / سنة</span><div class="m-item__s">hello</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بند واحد · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">صحة أعمال Plus</span></a><div class="m-item__s">قطاع الأعمال · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">0%</span></span><span class="m-cap">لا يبيعه المساعد · بانتظار اعتماد النص الحالي</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">لا سعر منشور</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">فحص الموظفين</span></a><div class="m-item__s">قطاع الأعمال · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--warn"><span class="m-n">73%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي بتسعير لكل فحص، يحدده المختص وفق الحجم</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr></tbody></table><div class="m-tools"><span class="m-cap"><span class="m-n">1</span>–<span class="m-n">8</span> من <span class="m-n">8</span> منتجات</span><span class="m-cap">المحقق للمعروض <span class="m-n">0</span> ر.س</span></div></section>
    34	      </div>
    35	    </main>
    36	  </div>
    37	</div>
    38	<dialog class="m-dlg" id="dlgProd"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة منتج</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">اسم المنتج</label><input class="m-input" type="text" placeholder="" value=""></div><div class="m-field"><label class="m-label m-req">القطاع</label><select class="m-select"><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option><option>بلا قطاع</option></select></div><div class="m-field"><label class="m-label">القسم</label><select class="m-select"><option>بلا قسم</option></select></div><div class="m-field"><label class="m-label">مدير المنتج</label><select class="m-select"><option>بلا تحديد</option></select></div><div class="m-field"><label class="m-label">السعر المنشور</label><input class="m-input" type="text" placeholder="لا سعر منشور" value=""></div><div class="m-field"><label class="m-label">وحدة التسعير</label><select class="m-select"><option>سنة</option><option>شهر</option><option>لكل فحص</option><option>مشروع</option></select></div><div class="m-field"><label class="m-label">حالة المساعد</label><select class="m-select"><option>يبيعه المساعد</option><option>لا يبيعه المساعد</option></select></div><div class="m-field"><label class="m-label">المستهدف 2026 (ر.س)</label><input class="m-input" type="number" placeholder="بلا مستهدف" value=""></div><div class="m-field full"><label class="m-label">وصف المنتج</label><textarea class="m-input" rows="4" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة المنتج</button></div></form></dialog>
    39	<script src="shell.js"></script>
    40	
    41	</body>
    42	</html>
     1	<!doctype html>
     2	<html lang="ar" dir="rtl">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
     6	<title>مسار — الإجازات المرضية</title>
     7	<link rel="preconnect" href="https://fonts.googleapis.com">
     8	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     9	<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    10	<link rel="stylesheet" href="massar.css">
    11	</head>
    12	<body data-nav="products" data-sub="products">
    13	<div class="m-shell">
    14	  <div class="m-main">
    15	    <div class="m-bar">
    16	      <div class="m-search">
    17	        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    18	        بحث
    19	        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
    20	      </div>
    21	      <div class="m-head__a"><button class="m-btn">أطلق حملة بهذا المنتج</button><button class="m-btn m-btn--primary">حفظ</button></div>
    22	    </div>
    23	    <main class="m-page">
    24	      <div class="m-head">
    25	        <div>
    26	          <div class="m-crumb"><a href="products.html">المنتجات</a> / الإجازات المرضية</div>
    27	          <h1 class="m-h1">الإجازات المرضية</h1>
    28	        </div>
    29	        <div class="m-row"><span class="m-chip">قطاع المستشفيات</span><span class="m-chip">مدير المنتج: بلا تحديد</span></div>
    30	      </div>
    31	      <div data-subs></div>
    32	      <div style="margin-block-start:var(--m-4)">
    33	<div class="m-tabs" role="tablist"><button class="m-tab" role="tab" aria-selected="true" data-t="q0">نظرة عامة</button><button class="m-tab" role="tab" aria-selected="false" data-t="q1">معرفة المنتج <b>80٪</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q2">الأسعار والباقات <b>2</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q3">المستهدفات <b>يحتاج إكمالًا</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q4">البيانات والإدارة</button></div><div class="m-view" style="margin-block-start:var(--m-4)"><section class="m-view__p" id="q0" role="tabpanel"><div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">الفرص المفتوحة</div><div class="m-q__v"><span class="m-n">2</span></div><div class="m-q__s">4,200 ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الحملات</div><div class="m-q__v"><span class="m-n">15</span></div><div class="m-q__s">ذكرت المنتج</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">قراءة المساعد</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">اهتمام رصده المساعد</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الجهات المستهدفة بالوسم</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">—</div></div></div><div class="m-grid m-grid--main"><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">الفرص المفتوحة</h2><a class="m-link" href="opps.html">كل فرص المنتج &#8592;</a></div><table class="m-table"><thead><tr><th>العميل</th><th>المرحلة</th><th>القيمة</th><th>في المرحلة</th></tr></thead><tbody><tr><td class="m-td-n">DL000</td><td><span class="m-chip m-chip--ac">عرض السعر</span></td><td class="m-td-v"><span class="m-n">4,200</span> ر.س</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td></tr><tr><td class="m-td-n">العمدة</td><td><span class="m-chip">اكتشاف الحاجة</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td class="m-td-v"><span class="m-n">35</span> يومًا</td></tr></tbody></table></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات</h2></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">القطاع</span><span class="m-item__n">قطاع المستشفيات</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">مدير المنتج</span><span class="m-item__n"><span class="m-td-nil">بلا تحديد</span></span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">السعر المنشور</span><span class="m-item__n">18,000 ر.س / سنة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">وحدة التسعير</span><span class="m-item__n">سنة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">حالة المساعد</span><span class="m-item__n">يبيعه المساعد · ينقصه ملف المعرفة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">المستهدف 2026</span><span class="m-item__n">34,000 ر.س · ربع واحد من أربعة</span></span></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn">أطلق حملة بهذا المنتج</button><button class="m-btn">&#8943;</button></div></section></div></section><section class="m-view__p" id="q1" role="tabpanel" hidden><div class="m-kb"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">الأقسام</h2><span class="m-chip m-chip--ok">80٪</span></div><div class="m-kb__l"><button class="m-kb__i" aria-current="true">وصف المنتج<b class="ok"><span class="m-n">80%</span></b></button><button class="m-kb__i">حالات الاستخدام<b class="mid"><span class="m-n">60%</span></b></button><button class="m-kb__i">الأسئلة الشائعة<b class="mid"><span class="m-n">45%</span></b></button><button class="m-kb__i">الأسعار والباقات<b class="low"><span class="m-n">10%</span></b></button><button class="m-kb__i">الاعتراضات<b class="low"><span class="m-n">0%</span></b></button><button class="m-kb__i">المنافسون<b class="low"><span class="m-n">0%</span></b></button><button class="m-kb__i">التكامل التقني<b class="low"><span class="m-n">20%</span></b></button><button class="m-kb__i">الامتثال<b class="low"><span class="m-n">0%</span></b></button></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">وصف المنتج</h2><span class="m-row"><span class="m-chip m-chip--warn">معرفة مدمجة</span><button class="m-btn">سجل التغييرات</button></span></div><div class="m-form"><div class="full"><textarea class="m-input" rows="12" placeholder="اكتب ما يعرفه المساعد عن هذا القسم…"></textarea></div><div class="m-field"><label class="m-label">الحالة</label><select class="m-select"><option>مدمجة</option><option>مسودة</option><option>بانتظار الاعتماد</option><option>معتمدة</option></select></div></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn m-btn--primary">حفظ كمسودة</button><button class="m-btn">إرسال للاعتماد</button><button class="m-btn">اعتماد</button></div></section></div></section><section class="m-view__p" id="q2" role="tabpanel" hidden><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">الباقات</h2><button class="m-btn m-btn--primary" data-open="dlgPkg">باقة جديدة</button></div><table class="m-table"><thead><tr><th>الباقة</th><th>السعر المرجعي</th><th>الوحدة</th><th>ما تشمله</th><th>الحالة</th><th></th></tr></thead><tbody><tr><td class="m-td-n">أساسية</td><td class="m-td-v"><span class="m-n">18,000</span> ر.س</td><td>سنويًا</td><td class="m-cap">حتى 500 موظف · دعم قياسي</td><td><span class="m-chip m-chip--ok">معتمدة</span></td><td><span class="m-row"><button class="m-btn" data-open="dlgPkg">تعديل</button><button class="m-btn">حذف</button></span></td></tr><tr><td class="m-td-n">متقدمة</td><td class="m-td-v"><span class="m-n">34,000</span> ر.س</td><td>سنويًا</td><td class="m-cap">غير محدود · دعم مخصص · تكامل</td><td><span class="m-chip m-chip--ok">معتمدة</span></td><td><span class="m-row"><button class="m-btn" data-open="dlgPkg">تعديل</button><button class="m-btn">حذف</button></span></td></tr></tbody></table></section></section><section class="m-view__p" id="q3" role="tabpanel" hidden><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">مستهدف 2026</h2><span class="m-chip m-chip--warn">يحتاج إكمالًا</span></div><div class="m-form"><div class="m-field"><label class="m-label">الربع 1 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div><div class="m-field"><label class="m-label">الربع 2 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div><div class="m-field"><label class="m-label">الربع 3 (ر.س)</label><input class="m-input" type="number" placeholder="" value="34000"></div><div class="m-field"><label class="m-label">الربع 4 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div></div><div class="m-form" style="margin-block-start:var(--m-3)"><div class="m-field"><label class="m-label">الإجمالي</label><input class="m-input" value="34000" disabled></div></div><div class="m-alert" style="margin-block-start:var(--m-4)"><span class="m-alert__t">ثلاثة أرباع بلا مستهدف</span><button class="m-btn">توزيع بالتساوي</button></div></section></section><section class="m-view__p" id="q4" role="tabpanel" hidden><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات والإدارة</h2></div><div class="m-form"><div class="m-field"><label class="m-label">اسم المنتج</label><input class="m-input" type="text" placeholder="" value="الإجازات المرضية"></div><div class="m-field"><label class="m-label">القطاع</label><select class="m-select"><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option><option>بلا قطاع</option></select></div><div class="m-field"><label class="m-label">القسم</label><select class="m-select"><option>بلا قسم</option></select></div><div class="m-field"><label class="m-label">مدير المنتج</label><select class="m-select"><option>بلا تحديد</option></select></div><div class="m-field"><label class="m-label">السعر المنشور</label><input class="m-input" type="text" placeholder="" value="18,000 ر.س / سنة"></div><div class="m-field"><label class="m-label">وحدة التسعير</label><select class="m-select"><option>سنة</option><option>شهر</option><option>لكل فحص</option></select></div></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn m-btn--primary">حفظ</button><button class="m-btn">أرشفة المنتج</button></div></section></section></div>
    34	      </div>
    35	    </main>
    36	  </div>
    37	</div>
    38	<dialog class="m-dlg" id="dlgPkg"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">باقة جديدة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">اسم الباقة</label><input class="m-input" type="text" placeholder="" value=""></div><div class="m-field"><label class="m-label m-req">السعر المرجعي (ر.س)</label><input class="m-input" type="number" placeholder="" value=""></div><div class="m-field"><label class="m-label">الوحدة</label><select class="m-select"><option>سنويًا</option><option>شهريًا</option><option>لكل فحص</option><option>مشروع</option></select></div><div class="m-field"><label class="m-label">الحالة</label><select class="m-select"><option>مسودة</option><option>معتمدة</option></select></div><div class="m-field full"><label class="m-label">ما تشمله</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">حفظ الباقة</button></div></form></dialog>
    39	<script src="shell.js"></script>
    40	<script>
    41	var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
    42	function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');
    43	 var p=document.getElementById(x.dataset.t);if(!p)return;
    44	 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;p.removeAttribute('data-enter');}else{p.hidden=true;}});}
    45	tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
    46	 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
    47	 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
    48	</script>
    49	</body>
    50	</html>
     1	<!doctype html>
     2	<html lang="ar" dir="rtl">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
     6	<title>مسار — فرص البيع</title>
     7	<link rel="preconnect" href="https://fonts.googleapis.com">
     8	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     9	<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    10	<link rel="stylesheet" href="massar.css">
    11	</head>
    12	<body data-nav="opps" data-sub="opps">
    13	<div class="m-shell">
    14	  <div class="m-main">
    15	    <div class="m-bar">
    16	      <div class="m-search">
    17	        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    18	        بحث
    19	        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
    20	      </div>
    21	      <div class="m-head__a"><button class="m-btn">تصدير CSV</button><button class="m-btn m-btn--primary" data-open="dlgOpp">إضافة فرصة</button></div>
    22	    </div>
    23	    <main class="m-page">
    24	      <div class="m-head">
    25	        <div>
    26	          <div class="m-crumb">فرص البيع</div>
    27	          <h1 class="m-h1">فرص البيع</h1>
    28	        </div>
    29	        <div class="m-row"><div class="m-seg" role="group" aria-label="طريقة العرض"><button data-v="tbl" aria-pressed="true">جدول</button><button data-v="kan" aria-pressed="false">كانبان</button><button data-v="crd" aria-pressed="false">بطاقات</button></div><div class="m-seg" role="group" aria-label="تصفية"><button aria-pressed="true">الكل</button><button aria-pressed="false">مُسعَّرة</button><button aria-pressed="false">راكدة</button><button aria-pressed="false">بلا مسؤول</button></div></div>
    30	      </div>
    31	      <div data-subs></div>
    32	      <div style="margin-block-start:var(--m-4)">
    33	<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">بنود مفتوحة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">4,200 ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">لم تُسعَّر</div><div class="m-q__v"><span class="m-n">5</span></div><div class="m-q__s">من 6 بنود</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">متوقفة</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">—</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">راكدة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">35 يومًا</div></div></div><div class="m-alert" style="margin-block-end:var(--m-4)"><span class="m-alert__t">جهتان مهتمّتان عبر واتساب بلا فرصة</span><button class="m-btn">عرض</button></div><div class="m-view"><div class="m-view__p" id="tbl"><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>العميل</th><th>المنتج</th><th>المرحلة</th><th>القيمة</th><th>المصدر</th><th>في المرحلة</th><th>الإضافة</th><th></th></tr></thead><tbody><tr><td class="m-td-n">ابرهيم</td><td>تكامل الأنظمة (HIS/ERP)</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">ابرهيم</td><td>سجل التطعيمات الوطني</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>خدمات التطعيمات</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>تكامل الأنظمة (HIS/ERP)</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>الإجازات المرضية</td><td><span class="m-chip">اكتشاف الحاجة</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">DL000</td><td>الإجازات المرضية</td><td><span class="m-chip m-chip--ac">عرض السعر</span></td><td><span class="m-td-v"><span class="m-n">4,200</span> ر.س</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-cap">18 أغسطس</td><td><button class="m-btn">فتح</button></td></tr></tbody></table><div class="m-tools"><span class="m-cap"><span class="m-n">6</span> بنود · <span class="m-n">4,200</span> ر.س · <span class="m-n">5</span> لم تُسعَّر</span></div></section></div><div class="m-view__p" id="kan" hidden><section class="m-card m-card--pad0"><div class="m-board" style="padding:0 var(--m-3) var(--m-3)"><div class="m-col" style="--m-tone:#5B6472"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">تواصل أولي</span><span class="m-col__c"><span class="m-n">4</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col" style="--m-tone:#0072E9"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">اكتشاف الحاجة</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#8B5CF6" tabindex="0" title="عرض المنتج"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض المنتج</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#7C3AED" tabindex="0" title="التقييم التقني"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التقييم التقني</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col" style="--m-tone:#2F6BFF"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض السعر</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v"><span class="m-n">4,200</span> ر.س</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#B45309" tabindex="0" title="التفاوض والاعتماد"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التفاوض والاعتماد</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#15803D" tabindex="0" title="رابح"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">رابح</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#BE123C" tabindex="0" title="خاسر"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">خاسر</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div></div></section></div><div class="m-view__p" id="crd" hidden><section class="m-card m-card--pad0"><div class="m-kpis" style="padding:var(--m-3)"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">اكتشاف الحاجة</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-chip m-chip--ac">عرض السعر</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></section></div></div>
    34	      </div>
    35	    </main>
    36	  </div>
    37	</div>
    38	<dialog class="m-dlg" id="dlgOpp"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة فرصة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">العميل</label><select class="m-select"><option>DL000</option><option>ابرهيم</option><option>العمدة</option><option>أبو حمزه</option><option>أبو نور</option><option>صيدلية الدواء</option><option>صيدلية الدواء (مثال)</option><option>صيدلية الدواء (مثال)</option></select></div><div class="m-field"><label class="m-label m-req">المنتج</label><select class="m-select"><option>الإجازات المرضية</option><option>التقارير الطبية</option><option>الشهادات الصحية</option><option>تكامل الأنظمة (HIS/ERP)</option><option>خدمات التطعيمات</option><option>سجل التطعيمات الوطني</option><option>صحة أعمال Plus</option><option>فحص الموظفين</option></select></div><div class="m-field"><label class="m-label m-req">المرحلة</label><select class="m-select"><option>تواصل أولي</option><option>اكتشاف الحاجة</option><option>عرض المنتج</option><option>التقييم التقني</option><option>عرض السعر</option><option>التفاوض والاعتماد</option></select></div><div class="m-field"><label class="m-label m-req">المصدر</label><select class="m-select"><option>حملة واتساب</option><option>مكالمة</option><option>زيارة</option><option>إحالة</option><option>طلب وارد</option></select></div><div class="m-field"><label class="m-label">الكمية</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">السعر للوحدة (ر.س)</label><input class="m-input" type="number" placeholder="لم تُسعَّر" value=""></div><div class="m-field"><label class="m-label">عدد السنوات</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">الخصم %</label><input class="m-input" type="number" placeholder="0" value=""></div><div class="m-field"><label class="m-label">الموظف المسؤول</label><select class="m-select"><option>بلا مسؤول</option></select></div><div class="m-field"><label class="m-label">تاريخ الإغلاق المتوقع</label><input class="m-input" type="date" placeholder="" value=""></div><div class="m-field"><label class="m-label">الشريك</label><select class="m-select"><option>لا شريك</option></select></div><div class="m-field full"><label class="m-label">ملاحظة</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة الفرصة</button></div></form></dialog>
    39	<script src="shell.js"></script>
    40	<script>
    41	var vs=document.querySelectorAll('[data-v]');
    42	vs.forEach(function(b){b.addEventListener('click',function(){
    43	 vs.forEach(function(o){o.setAttribute('aria-pressed','false');});
    44	 b.setAttribute('aria-pressed','true');
    45	 ['tbl','kan','crd'].forEach(function(id){var p=document.getElementById(id);if(!p)return;
    46	  if(id===b.dataset.v){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
    47	   p.removeAttribute('data-enter');}else{p.hidden=true;}});});});
    48	</script>
    49	</body>
    50	</html>
     1	<!doctype html>
     2	<html lang="ar" dir="rtl">
     3	<head>
     4	<meta charset="utf-8">
     5	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
     6	<title>مسار — التقارير</title>
     7	<link rel="preconnect" href="https://fonts.googleapis.com">
     8	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     9	<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    10	<link rel="stylesheet" href="massar.css">
    11	</head>
    12	<body data-nav="reports" data-sub="reports">
    13	<div class="m-shell">
    14	  <div class="m-main">
    15	    <div class="m-bar">
    16	      <div class="m-search">
    17	        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    18	        بحث
    19	        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
    20	      </div>
    21	      <div class="m-head__a"><button class="m-btn">تحديث</button><button class="m-btn">تصدير</button></div>
    22	    </div>
    23	    <main class="m-page">
    24	      <div class="m-head">
    25	        <div>
    26	          <div class="m-crumb">التقارير</div>
    27	          <h1 class="m-h1">التقارير</h1>
    28	        </div>
    29	        <div class="m-row"><div class="m-seg" role="group" aria-label="تصفية"><button aria-pressed="true">آخر 30 يومًا</button><button aria-pressed="false">آخر 90 يومًا</button></div></div>
    30	      </div>
    31	      <div data-subs></div>
    32	      <div style="margin-block-start:var(--m-4)">
    33	<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">المحقق</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">المفتوح</div><div class="m-q__v"><span class="m-n">4,200</span></div><div class="m-q__s">ر.س · 6 بنود</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">المتوقع المرجّح</div><div class="m-q__v"><span class="m-n">3,360</span></div><div class="m-q__s">ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الراكدة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">35 يومًا</div></div></div><div class="m-tabs" role="tablist"><button class="m-tab" role="tab" aria-selected="true" data-t="r0">نظرة تنفيذية</button><button class="m-tab" role="tab" aria-selected="false" data-t="r1">تقارير التعثّر</button><button class="m-tab" role="tab" aria-selected="false" data-t="r2">قبول المنتجات</button><button class="m-tab" role="tab" aria-selected="false" data-t="r3">مؤشرات الأداء</button></div><div class="m-view" style="margin-block-start:var(--m-4)"><section class="m-view__p" id="r0" role="tabpanel"><div class="m-grid m-grid--main"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">قمع المراحل</h2></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">تواصل أولي</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">4</span></span></div><div class="m-fstep"><span class="m-fstep__k">اكتشاف الحاجة</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span> <span class="m-fstep__d">&#9662; <span class="m-n">75%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض المنتج</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">التقييم التقني</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض السعر</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span></span></div><div class="m-fstep"><span class="m-fstep__k">التفاوض والاعتماد</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">رابح</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div></div></section><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">أين تتعثّر الصفقات</h2></div><table class="m-table"><thead><tr><th>السبب</th><th>البنود</th></tr></thead><tbody><tr><td class="m-td-n">بلا تسعير</td><td class="m-td-v"><span class="m-n">5</span></td></tr><tr><td class="m-td-n">راكدة 30 يومًا+</td><td class="m-td-v"><span class="m-n">6</span></td></tr><tr><td class="m-td-n">بلا موظف مسؤول</td><td class="m-td-v"><span class="m-n">6</span></td></tr><tr><td class="m-td-n">بلا مستهدف منتج</td><td class="m-td-v"><span class="m-n">7</span></td></tr></tbody></table></section></div></section><section class="m-view__p" id="r1" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المرحلة</th><th>الأقدم</th><th>الوسيط</th><th>البنود</th><th></th></tr></thead><tbody><tr><td class="m-td-n">تواصل أولي</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">4</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr><tr><td class="m-td-n">اكتشاف الحاجة</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">1</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr><tr><td class="m-td-n">عرض السعر</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-td-v"><span class="m-n">1</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr></tbody></table></section></section><section class="m-view__p" id="r2" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المنتج</th><th>جاهزية المساعد</th><th>السعر المنشور</th><th>الحالة</th></tr></thead><tbody><tr><td class="m-td-n">الإجازات المرضية</td><td class="m-td-v"><span class="m-n">80%</span></td><td><span class="m-td-v">18,000 ر.س / سنة</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">التقارير الطبية</td><td class="m-td-v"><span class="m-n">68%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">الشهادات الصحية</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">تكامل الأنظمة (HIS/ERP)</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">خدمات التطعيمات</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">سجل التطعيمات الوطني</td><td class="m-td-v"><span class="m-n">90%</span></td><td><span class="m-td-v">20,000 ر.س / سنة</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">صحة أعمال Plus</td><td class="m-td-v"><span class="m-n">0%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">لا يبيعه المساعد</span></td></tr><tr><td class="m-td-n">فحص الموظفين</td><td class="m-td-v"><span class="m-n">73%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr></tbody></table></section></section><section class="m-view__p" id="r3" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المؤشر</th><th>القيمة</th><th>المدى</th></tr></thead><tbody><tr><td class="m-td-n">نسبة الردّ</td><td class="m-td-v"><span class="m-n">19%</span></td><td class="m-cap">4 من 21</td></tr><tr><td class="m-td-n">نسبة الاهتمام</td><td class="m-td-v"><span class="m-n">9%</span></td><td class="m-cap">2 من 21</td></tr><tr><td class="m-td-n">نسبة التحويل إلى فرصة</td><td class="m-td-v"><span class="m-n">0%</span></td><td class="m-cap">0 من 2</td></tr><tr><td class="m-td-n">متوسط زمن الردّ</td><td class="m-td-v"><span class="m-n">3</span> ساعات</td><td class="m-cap">آخر 30 يومًا</td></tr><tr><td class="m-td-n">متوسط العمر في المرحلة</td><td class="m-td-v"><span class="m-n">34</span> يومًا</td><td class="m-cap">البنود المفتوحة</td></tr><tr><td class="m-td-n">نسبة الإنجاز</td><td class="m-td-v"><span class="m-n">0%</span></td><td class="m-cap">2026</td></tr></tbody></table></section></section></div>
    34	      </div>
    35	    </main>
    36	  </div>
    37	</div>
    38	
    39	<script src="shell.js"></script>
    40	<script>
    41	var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
    42	function sel(t){tabs.forEach(function(x){var on=x===t;
    43	 x.setAttribute('aria-selected',on?'true':'false');
    44	 var p=document.getElementById(x.dataset.t);if(!p)return;
    45	 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
    46	  p.removeAttribute('data-enter');}else{p.hidden=true;}});}
    47	tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
    48	 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
    49	 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
    50	</script>
    51	</body>
    52	</html>

codex
I’m using the better-ui skill to check the component details, with the brief’s constraints taking precedence. The main failure is already visible: the interface gives incomplete targets and unpriced pipeline the visual authority of a reliable forecast. The redesign needs to make those limits part of the headline.
exec
/bin/zsh -lc "sed -n '285,510p' massar-ds/massar.css" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:

/* TOOLTIP — 4px 8px, radius 8, 12/16; enters from scale(.98), 150ms. */
.m-tip2{position:absolute;padding:4px 8px;border-radius:8px;font-size:var(--m-t-cap);
        line-height:16px;background:var(--m-paper);color:var(--m-ink);
        box-shadow:0 0 0 1px var(--m-line),0 4px 6px -1px rgba(0,0,0,.05),
                   0 2px 4px -2px rgba(0,0,0,.05),inset 0 1px rgba(0,0,0,.04);
        opacity:0;transform:scale(.98);pointer-events:none;
        transition:opacity 150ms cubic-bezier(.4,0,.2,1),
                   transform 150ms cubic-bezier(.4,0,.2,1)}
.m-tip2[data-open]{opacity:1;transform:none}

/* ============================================================================
   TABLE — ported from measured values, not invented
   ----------------------------------------------------------------------------
   Geometry and motion taken from coss.com/ui/docs/components/table (the light
   fintech register) and beui.dev/components/motion/table (the sortable header
   and the sticky treatment). Colour is mapped onto Massar's palette; every
   physical direction is rewritten as a logical property for RTL.

   coss:  row 39px · th 40px · th padding 0 10px · 14px/500 · header has NO fill
          td padding 10px · row rule 1px rgba(0,0,0,.08) · hover #FAFAFA
          selected #F5F5F5 · checkbox col 26px · tfoot 43px, padding 14px 10px
   beui:  sticky header · container radius 16px + overflow hidden
          sortable th is a FULL-HEIGHT button; chevron 14px rotates 0->180deg,
          opacity .35 -> 1, 180ms cubic-bezier(.16,1,.3,1)
   Both ship WITHOUT tabular figures; Massar adds them, because a ledger column
   that shifts as its digits change is unreadable.
   ========================================================================== */
.m-tablewrap{position:relative;inline-size:100%;overflow-x:auto;
             border-radius:var(--m-r-card)}
.m-table{inline-size:100%;border-collapse:collapse}
.m-table th{block-size:40px;padding:0 10px;font-size:var(--m-t-body);font-weight:500;
            line-height:14px;color:var(--m-mut);text-align:start;white-space:nowrap;
            background:transparent;border-block-end:1px solid var(--m-line)}
.m-table td{padding:10px;font-size:var(--m-t-body);font-weight:500;line-height:1.45;
            color:var(--m-ink-2);vertical-align:middle;
            border-block-start:1px solid var(--m-line)}
.m-table tbody tr{transition:background-color 150ms cubic-bezier(.4,0,.2,1)}
@media (hover:hover) and (pointer:fine){
  .m-table tbody tr:hover{background:var(--m-page)} }
.m-table tbody tr[aria-selected="true"]{background:var(--m-sunk)}
/* Sticky header, from beui. A ledger is scrolled, so the column names stay. */
.m-table--sticky thead th{position:sticky;inset-block-start:0;z-index:2;
            background:var(--m-paper)}
/* The sortable header is a full-height button, so the whole cell is the target. */
.m-th-sort{display:flex;align-items:center;gap:4px;inline-size:100%;block-size:100%;
           font:inherit;color:inherit;background:none;border:0;cursor:pointer;
           padding:0;text-align:start}
.m-th-sort svg{inline-size:14px;block-size:14px;flex:0 0 auto;opacity:.35;
           stroke:currentColor;stroke-width:2;fill:none;
           transition:transform 180ms cubic-bezier(.16,1,.3,1),
                      opacity 180ms cubic-bezier(.16,1,.3,1)}
.m-table th[aria-sort] .m-th-sort svg{opacity:1}
.m-table th[aria-sort="descending"] .m-th-sort svg{transform:rotate(180deg)}
/* Checkbox column: 26px, exactly as measured. */
.m-table th.m-sel{inline-size:26px;padding:0 0 0 10px}
.m-table td.m-sel{padding:10px 0 10px 9px}
/* A totals row, not pagination — coss ships no pagination bar. */
.m-table tfoot td{block-size:43px;padding:14px 10px;font-weight:600;color:var(--m-ink);
            background:var(--m-page);border-block-start:1px solid var(--m-line-2)}
.m-td-n{font-weight:600;color:var(--m-ink)}
/* Numeric columns align to the OUTSIDE edge and carry tabular figures. */
.m-td-v{text-align:end;font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1;
        font-weight:600;color:var(--m-ink);white-space:nowrap}
.m-table th.num{text-align:end}
.m-td-nil{color:var(--m-faint);font-weight:400}
.m-table__empty td{padding:0}
.m-tools{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3);
         padding:var(--m-3);flex-wrap:wrap}

/* CHECKBOX — 16x16, radius 4, only the shadow transitions (measured: the check
   mark itself is not animated on coss). */
.m-cb{inline-size:16px;block-size:16px;border-radius:4px;appearance:none;cursor:pointer;
      background:var(--m-paper);box-shadow:0 0 0 1px var(--m-line-2),0 1px 2px rgba(0,0,0,.05);
      display:grid;place-items:center;transition:box-shadow 150ms cubic-bezier(.4,0,.2,1)}
.m-cb:checked{background:var(--m-ac);box-shadow:0 0 0 1px var(--m-ac)}
.m-cb:checked::after{content:"";inline-size:9px;block-size:5px;border:2px solid #fff;
      border-block-start:0;border-inline-end:0;transform:rotate(-45deg) translate(1px,-1px)}
.m-cb:focus-visible{outline:none;box-shadow:0 0 0 1px var(--m-ac),var(--m-focus)}

/* AVATAR */
.m-av{inline-size:30px;block-size:30px;border-radius:50%;flex:0 0 auto;display:grid;
      place-items:center;font-size:var(--m-t-cap);font-weight:700;
      background:var(--m-ac-dim);color:var(--m-ac-deep)}
.m-av--sq{border-radius:9px;background:var(--m-sunk);color:var(--m-ink-2)}

/* --------------------------------------------------------------- GREETING
   The reference's opening move: a breadcrumb, then a large tight display
   headline that speaks to the reader, then one calm subtitle. */
.m-crumb{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-end:var(--m-3)}
.m-greet{display:flex;align-items:flex-end;justify-content:space-between;
         gap:var(--m-5);flex-wrap:wrap;margin-block-end:var(--m-5)}
.m-greet__t{margin:0;font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
            letter-spacing:-1px;line-height:1.2}
.m-greet__s{font-size:var(--m-t-sub);color:var(--m-mut);margin-block-start:var(--m-2)}
.m-greet__a{display:flex;gap:var(--m-2);align-items:center;flex-wrap:wrap}

/* SEARCH PILL with a kbd badge, straight from the reference. */
.m-search{display:flex;align-items:center;gap:var(--m-2);background:var(--m-paper);
          border-radius:var(--m-r-chip);padding:9px var(--m-4);box-shadow:var(--m-low);
          color:var(--m-faint);font-size:var(--m-t-body);min-inline-size:240px}
.m-kbd{margin-inline-start:auto;display:flex;gap:3px}
.m-kbd span{font-size:var(--m-t-micro);font-weight:600;color:var(--m-mut);
            background:var(--m-page);border-radius:5px;padding:2px 6px;box-shadow:var(--m-hair)}

/* ------------------------------------------------------------------ CARD */
.m-card{background:var(--m-paper);border-radius:var(--m-r-card);box-shadow:var(--m-soft);
        padding:var(--m-5)}
.m-card--band{border-radius:var(--m-r-band);padding:var(--m-6)}
.m-card--pad0{padding:0}
.m-card__h{display:flex;align-items:flex-start;justify-content:space-between;
           gap:var(--m-3);margin-block-end:var(--m-4)}
.m-card__t{margin:0;font-size:var(--m-t-h);font-weight:700;color:var(--m-ink);
           letter-spacing:-.3px}
.m-card__k{font-size:var(--m-t-body);color:var(--m-mut);font-weight:500}

/* THE LEADING FIGURE + DELTA PILL. The reference's centrepiece. */
.m-lead{display:flex;align-items:center;gap:var(--m-4);flex-wrap:wrap}
.m-lead__v{font-size:var(--m-t-hero);font-weight:800;color:var(--m-ink);
           letter-spacing:-2.5px;line-height:1.05;font-variant-numeric:tabular-nums}
.m-lead__v small{font-size:var(--m-t-h);font-weight:600;color:var(--m-mut);
                 letter-spacing:0;margin-inline-start:var(--m-2)}
.m-delta{display:inline-flex;align-items:center;gap:6px;font-size:var(--m-t-body);
         font-weight:600;padding:6px 13px;border-radius:var(--m-r-chip);
         background:var(--m-ok-dim);color:var(--m-ok)}
.m-delta--bad{background:var(--m-bad-dim);color:var(--m-bad)}
.m-delta--warn{background:var(--m-warn-dim);color:var(--m-warn)}
.m-delta--flat{background:var(--m-idle-dim);color:var(--m-idle)}

/* ------------------------------------------------------------------- STAT */
.m-stat__k{font-size:var(--m-t-cap);color:var(--m-mut);font-weight:500}
.m-stat__v{font-size:var(--m-t-fig);font-weight:800;color:var(--m-ink);line-height:1.2;
           margin-block-start:var(--m-1);letter-spacing:-.8px;
           font-variant-numeric:tabular-nums}
.m-stat__v small{font-size:var(--m-t-cap);font-weight:600;color:var(--m-mut);
                 letter-spacing:0;margin-inline-start:4px}
.m-stat__s{font-size:var(--m-t-micro);color:var(--m-faint);margin-block-start:3px}
.m-stat--ac .m-stat__v{color:var(--m-ac)}
.m-stat--mut .m-stat__v{color:var(--m-faint)}
.m-stats{display:flex;gap:var(--m-6);flex-wrap:wrap}

/* ------------------------------------------------------------------ CHART
   The reference's signature: gradient bars fading to nothing, a round dot
   capping each, over a dotted grid, with a dashed trend line.
   TIME RUNS RIGHT TO LEFT in RTL — January at the right edge. */
.m-chart{display:block;inline-size:100%;block-size:auto;overflow:visible}
.m-chart__ax{font-size:var(--m-t-cap);fill:var(--m-mut);font-family:inherit}
.m-chart__bar{fill:url(#mBar)}
.m-chart__cap{fill:var(--m-ac)}
.m-chart__cap--vi{fill:var(--m-vi)}
.m-chart__trend{stroke:var(--m-ac-line);stroke-width:2;stroke-dasharray:5 5;fill:none}
.m-chart__zero{stroke:var(--m-line-2);stroke-width:1}
.m-chart__now{stroke:var(--m-line-2);stroke-width:1;stroke-dasharray:3 4}
/* The bars draw upward on first paint only. */
.m-chart__grow{transform-box:fill-box;transform-origin:bottom;
               animation:m-grow 700ms var(--m-ease) both}
@keyframes m-grow{from{transform:scaleY(.02);opacity:0}to{transform:scaleY(1);opacity:1}}
@media (prefers-reduced-motion:reduce){ .m-chart__grow{animation:none} }

/* TOOLTIP, as drawn in the reference: a white rounded card with two columns. */
.m-tip{position:absolute;background:var(--m-paper);border-radius:var(--m-r-ctl);
       box-shadow:var(--m-lift);padding:var(--m-3) var(--m-4);pointer-events:none}
.m-tip__d{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-end:var(--m-2)}
.m-tip__g{display:flex;gap:var(--m-5)}
.m-tip__k{font-size:var(--m-t-cap);color:var(--m-mut)}
.m-tip__v{font-size:var(--m-t-sub);font-weight:700;color:var(--m-ink);
          font-variant-numeric:tabular-nums}
.m-tip__v--bad{color:var(--m-bad)}

/* ------------------------------------------------------- SEGMENTED TRACK
   The reference's goal bar: a row of dots that fill, with a round knob at
   the head. Reads as progress without pretending to a precision it lacks. */
.m-seg-bar{display:flex;align-items:center;gap:3px;margin-block:var(--m-3) var(--m-2)}
.m-seg-bar i{block-size:8px;flex:1 1 auto;border-radius:99px;background:var(--m-sunk)}
.m-seg-bar i.on{background:var(--m-ac)}
.m-seg-bar b{inline-size:16px;block-size:16px;border-radius:50%;background:var(--m-paper);
             box-shadow:0 0 0 3px var(--m-ac),0 1px 3px rgba(16,24,40,.2);flex:0 0 auto}

/* -------------------------------------------------------------- THE BOARD
   Kept from the settled paradigm: home is where the pipeline is worked.
   Empty stages collapse to a rail so the real content starts immediately. */
.m-board{display:flex;gap:var(--m-3);align-items:flex-start;overflow-x:auto;
         padding-block-end:var(--m-2)}
.m-col{inline-size:252px;flex:0 0 auto;display:flex;flex-direction:column;
       background:var(--m-page);border-radius:var(--m-r-ctl);padding:var(--m-3)}
.m-col__t{display:flex;align-items:center;gap:var(--m-2);margin-block-end:var(--m-1)}
.m-col__dot{inline-size:8px;block-size:8px;border-radius:50%;flex:0 0 auto;
            background:var(--m-tone,var(--m-idle))}
.m-col__n{font-size:var(--m-t-body);font-weight:600;color:var(--m-ink);flex:1 1 auto}
.m-col__c{font-size:var(--m-t-micro);font-weight:700;color:var(--m-mut);
          background:var(--m-paper);border-radius:var(--m-r-chip);padding:1px 7px;
          box-shadow:var(--m-hair);font-variant-numeric:tabular-nums}
.m-col__v{font-size:var(--m-t-cap);color:var(--m-mut);padding-inline-start:16px;
          margin-block-end:var(--m-2);font-variant-numeric:tabular-nums}
.m-col__b{display:flex;flex-direction:column;gap:var(--m-2)}
.m-col--rail{inline-size:44px;cursor:pointer;align-self:stretch}
.m-col--rail .m-col__b,.m-col--rail .m-col__v{display:none}
.m-col--rail .m-col__t{flex-direction:column;gap:var(--m-3);margin:0}
.m-col--rail .m-col__n{writing-mode:vertical-rl;transform:rotate(180deg);
            white-space:nowrap;flex:0 0 auto;font-size:var(--m-t-cap);color:var(--m-mut)}
@media (hover:hover) and (pointer:fine){ .m-col--rail:hover{background:var(--m-sunk)} }

.m-deal{background:var(--m-paper);border-radius:var(--m-r-ctl);padding:var(--m-3);
        box-shadow:var(--m-low);cursor:grab;
        transition:box-shadow var(--m-out) var(--m-ease),transform var(--m-press) var(--m-ease)}
@media (hover:hover) and (pointer:fine){ .m-deal:hover{box-shadow:var(--m-lift)} }
.m-deal:active{cursor:grabbing;transform:scale(.985)}
.m-deal:focus-visible{outline:none;box-shadow:var(--m-focus),var(--m-low)}
.m-deal__n{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
           display:flex;align-items:center;justify-content:space-between;gap:var(--m-2)}
.m-deal__p{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:2px}
.m-deal__f{display:flex;align-items:center;justify-content:space-between;
           gap:var(--m-2);margin-block-start:var(--m-2)}
.m-deal__v{font-size:var(--m-t-sub);font-weight:700;color:var(--m-ink);
           font-variant-numeric:tabular-nums}
.m-deal__v--nil{font-size:var(--m-t-cap);font-weight:600;color:var(--m-warn)}
.m-deal__age{font-size:var(--m-t-micro);color:var(--m-faint);font-variant-numeric:tabular-nums}
.m-deal__age--old{color:var(--m-warn);font-weight:600}
.m-empty-col{padding:var(--m-4) var(--m-3);text-align:center;border-radius:var(--m-r-ctl);
             border:1px dashed var(--m-line-2);color:var(--m-faint);
             font-size:var(--m-t-cap);line-height:1.7}

/* -------------------------------------------------------------- LIST ROW
   The reference's «Recent Transactions»: a round brand mark, a two-line
   label, and a value on the outside edge. */
.m-item{display:flex;align-items:center;gap:var(--m-3);padding:var(--m-3) 0;

exec
/bin/zsh -lc "sed -n '510,850p' massar-ds/massar.css" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
.m-item{display:flex;align-items:center;gap:var(--m-3);padding:var(--m-3) 0;
        border-block-start:1px solid var(--m-line)}
.m-item:first-child{border-block-start:0}
.m-item__m{inline-size:38px;block-size:38px;border-radius:50%;flex:0 0 auto;
           display:grid;place-items:center;font-size:var(--m-t-body);font-weight:700;
           background:var(--m-page);color:var(--m-ink-2);box-shadow:var(--m-hair)}
.m-item__b{flex:1 1 auto;min-inline-size:0}
.m-item__n{font-size:var(--m-t-body);font-weight:600;color:var(--m-ink)}
.m-item__s{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-start:1px}
.m-item__v{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
           font-variant-numeric:tabular-nums;white-space:nowrap}

/* ------------------------------------------------------------- INSIGHTS
   The reference's AI panel: a dithered blue field with a white card floating
   on it. The dither is a repeating radial-gradient, not an image. */
.m-insight{border-radius:var(--m-r-band);padding:var(--m-5);color:#fff;
  background:
    radial-gradient(circle at 1px 1px,rgba(255,255,255,.32) 1px,transparent 0) 0 0/8px 8px,
    linear-gradient(150deg,#1D4FD8,#2F6BFF 45%,#8B5CF6);
  display:flex;flex-direction:column;gap:var(--m-3)}
.m-insight__k{font-size:var(--m-t-cap);opacity:.85;font-weight:600}
.m-insight__t{font-size:var(--m-t-h);font-weight:700;letter-spacing:-.3px;line-height:1.35}
.m-insight__c{background:var(--m-paper);border-radius:var(--m-r-ctl);padding:var(--m-3) var(--m-4);
              color:var(--m-ink-2);font-size:var(--m-t-cap);line-height:1.75}
.m-insight__c b{color:var(--m-ink)}
.m-dots{display:flex;gap:5px}
.m-dots i{inline-size:16px;block-size:4px;border-radius:99px;background:rgba(255,255,255,.35)}
.m-dots i.on{background:#fff;inline-size:22px}

/* ------------------------------------------------------------------- CHIP */
.m-chip{display:inline-flex;align-items:center;gap:6px;font-size:var(--m-t-micro);
        font-weight:600;padding:3px 9px;border-radius:var(--m-r-chip);
        background:var(--m-idle-dim);color:var(--m-idle);white-space:nowrap}
.m-chip--ok{background:var(--m-ok-dim);color:var(--m-ok)}
.m-chip--warn{background:var(--m-warn-dim);color:var(--m-warn)}
.m-chip--bad{background:var(--m-bad-dim);color:var(--m-bad)}
.m-chip--ac{background:var(--m-ac-dim);color:var(--m-ac-deep)}
/* Colour is never the only channel — a tone chip carries a dot too. */
.m-chip::before{content:"";inline-size:5px;block-size:5px;border-radius:50%;background:currentColor}
.m-chip--plain::before{display:none}

/* ----------------------------------------------------------------- BUTTON */
.m-btn{display:inline-flex;align-items:center;gap:7px;font:inherit;
       font-size:var(--m-t-body);font-weight:600;padding:9px 16px;
       border-radius:var(--m-r-chip);border:0;cursor:pointer;
       background:var(--m-paper);color:var(--m-ink);box-shadow:var(--m-low);
       transition:transform var(--m-press) var(--m-ease),background var(--m-out) var(--m-ease)}
.m-btn:active{transform:scale(.97)}
@media (hover:hover) and (pointer:fine){ .m-btn:hover{background:var(--m-page)} }
.m-btn--primary{background:var(--m-ac);color:#fff;box-shadow:0 1px 2px rgba(47,107,255,.35)}
@media (hover:hover) and (pointer:fine){ .m-btn--primary:hover{background:var(--m-ac-deep)} }
.m-btn--primary:active{background:var(--m-ac-deep)}
.m-btn--icon{padding:9px;inline-size:36px;block-size:36px;justify-content:center}
.m-btn--quiet{background:transparent;box-shadow:none;color:var(--m-ac-deep);padding-inline:6px}
.m-btn[disabled]{color:var(--m-faint);cursor:not-allowed;background:var(--m-sunk);box-shadow:none}
.m-btn:focus-visible{outline:none;box-shadow:var(--m-focus),var(--m-low)}
.m-link{font-size:var(--m-t-cap);font-weight:600;color:var(--m-ac-deep);text-decoration:none}
@media (hover:hover) and (pointer:fine){ .m-link:hover{text-decoration:underline} }

/* ------------------------------------------------------------------ ALERT */
.m-alert{display:flex;align-items:center;gap:var(--m-3);flex-wrap:wrap;
         background:var(--m-warn-dim);border-radius:var(--m-r-card);
         padding:var(--m-3) var(--m-4);box-shadow:0 0 0 1px var(--m-warn-line)}
.m-alert__t{font-size:var(--m-t-body);font-weight:700;color:var(--m-warn)}
.m-alert__d{font-size:var(--m-t-cap);color:var(--m-ink-2);flex:1 1 240px}

/* ------------------------------------------------------------------ EMPTY */
.m-empty{padding:var(--m-6) var(--m-5);text-align:center}
.m-empty__t{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink)}
.m-empty__d{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:var(--m-2);
            max-inline-size:52ch;margin-inline:auto;line-height:1.75}
.m-empty__a{margin-block-start:var(--m-4)}
.m-nil{color:var(--m-faint);font-size:var(--m-t-cap)}

/* --------------------------------------------------------------- LAYOUT */
.m-grid{display:grid;gap:var(--m-4)}
.m-grid--main{grid-template-columns:minmax(0,1fr) 340px}
.m-grid--3{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:1180px){ .m-grid--main{grid-template-columns:1fr} }
@media (max-width:980px){ .m-grid--3{grid-template-columns:1fr} }
.m-between{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3)}
.m-row{display:flex;align-items:center;gap:var(--m-2)}
.m-cap{font-size:var(--m-t-cap);color:var(--m-mut)}
.m-rel{position:relative}

/* ============================================================================
   INDICATORS — a different chart vocabulary
   ----------------------------------------------------------------------------
   Bars and lines answer «how much, over time». Massar's indicators mostly
   answer other questions — «how ready», «how many of what kind», «where does
   it leak», «is anything happening» — and drawing all four as bars is what
   made every earlier dashboard read the same. Each shape below is chosen for
   the QUESTION it answers:
     arc      → a bounded score (0-100). The gap in the ring IS the shortfall.
     matrix   → a count of things you could point at. One dot is one record.
     funnel   → where a population leaks between stages.
     heat     → whether anything happened, per day, over a window.
     meter    → one record's standing on a scale, with its own evidence.
   ========================================================================== */

/* ARC GAUGE — a bounded score. Drawn with stroke-dasharray on a semicircle,
   so the empty part of the ring is visibly the part not earned. */
.m-arc{position:relative;inline-size:100%;max-inline-size:200px;margin-inline:auto}
.m-arc svg{display:block;inline-size:100%;block-size:auto;overflow:visible}
.m-arc__track{fill:none;stroke:var(--m-sunk);stroke-width:14;stroke-linecap:round}
.m-arc__fill{fill:none;stroke:var(--m-ac);stroke-width:14;stroke-linecap:round;
             stroke-dasharray:var(--m-dash,0) 999;
             animation:m-arc 900ms var(--m-ease) both}
.m-arc__fill--warn{stroke:var(--m-warn)}
.m-arc__fill--bad{stroke:var(--m-bad)}
.m-arc__fill--ok{stroke:var(--m-ok)}
@keyframes m-arc{from{stroke-dasharray:0 999}}
@media (prefers-reduced-motion:reduce){ .m-arc__fill{animation:none} }
.m-arc__c{position:absolute;inset-inline:0;inset-block-end:6%;text-align:center}
.m-arc__v{font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
          letter-spacing:-1.5px;line-height:1;font-variant-numeric:tabular-nums}
.m-arc__k{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:var(--m-1)}

/* DOT MATRIX — one dot is one record, so a count you can point at rather
   than a bar whose height you have to decode. */
.m-matrix{display:flex;flex-wrap:wrap;gap:5px;margin-block:var(--m-3)}
.m-matrix i{inline-size:12px;block-size:12px;border-radius:4px;background:var(--m-sunk)}
.m-matrix i.is-ok{background:var(--m-ok-line)}
.m-matrix i.is-ac{background:var(--m-ac)}
.m-matrix i.is-warn{background:var(--m-warn-line)}
.m-matrix i.is-bad{background:var(--m-bad-line)}
.m-matrix i.is-idle{background:var(--m-line-2)}
.m-key{display:flex;gap:var(--m-4);flex-wrap:wrap;font-size:var(--m-t-cap);color:var(--m-mut)}
.m-key span{display:inline-flex;align-items:center;gap:6px}
.m-key i{inline-size:10px;block-size:10px;border-radius:3px}

/* FUNNEL — stepped bars that narrow, so a leak is visible as a step change
   rather than as two numbers you have to subtract. */
.m-funnel{display:flex;flex-direction:column;gap:var(--m-2)}
.m-fstep{display:grid;grid-template-columns:104px 1fr auto;align-items:center;gap:var(--m-3)}
.m-fstep__k{font-size:var(--m-t-cap);color:var(--m-mut)}
.m-fstep__b{block-size:30px;border-radius:var(--m-r-ctl);background:var(--m-sunk);
            position:relative;overflow:hidden}
.m-fstep__b i{position:absolute;inset-block:0;inset-inline-start:0;inline-size:var(--m-pct,0%);
              background:linear-gradient(90deg,var(--m-ac),var(--m-vi));border-radius:var(--m-r-ctl);
              animation:m-fgrow 700ms var(--m-ease) both}
@keyframes m-fgrow{from{inline-size:0}}
@media (prefers-reduced-motion:reduce){ .m-fstep__b i{animation:none} }
.m-fstep__v{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink);
            font-variant-numeric:tabular-nums;min-inline-size:56px;text-align:start}
.m-fstep__d{font-size:var(--m-t-micro);color:var(--m-bad);font-weight:600}

/* HEAT STRIP — did anything happen, per day. Absence is the signal here, so
   an empty cell must be legible as «nothing», not as «no data». */
.m-heat{display:flex;gap:4px;margin-block:var(--m-3)}
.m-heat i{flex:1 1 auto;block-size:34px;border-radius:5px;background:var(--m-sunk)}
.m-heat i.l1{background:var(--m-ac-line)}
.m-heat i.l2{background:#9CC0FF}
.m-heat i.l3{background:var(--m-ac)}
.m-heat__ax{display:flex;justify-content:space-between;font-size:var(--m-t-micro);
            color:var(--m-faint)}

/* METER — one record on a 0-100 scale, with the threshold marked. */
.m-meter{block-size:10px;border-radius:99px;background:var(--m-sunk);position:relative;
         margin-block:var(--m-3) var(--m-2)}
.m-meter i{position:absolute;inset-block:0;inset-inline-start:0;inline-size:var(--m-pct,0%);
           border-radius:99px;background:linear-gradient(90deg,var(--m-ac),var(--m-vi))}
.m-meter b{position:absolute;inset-block:-4px;inset-inline-start:var(--m-mark,50%);
           inline-size:2px;background:var(--m-ink);opacity:.35}

/* RING SEGMENTS — a weighted score built of named sections, each drawn as its
   own arc segment so a low section is findable, not averaged away. */
.m-segs{display:flex;flex-direction:column;gap:var(--m-2)}
.m-seg-row{display:grid;grid-template-columns:1fr 92px 44px;align-items:center;gap:var(--m-3);
           font-size:var(--m-t-cap)}
.m-seg-row__t{color:var(--m-ink-2)}
.m-seg-row__b{block-size:6px;border-radius:99px;background:var(--m-sunk);overflow:hidden}
.m-seg-row__b i{display:block;block-size:100%;inline-size:var(--m-pct,0%);border-radius:99px;
                background:var(--m-ac)}
.m-seg-row__b i.low{background:var(--m-bad)}
.m-seg-row__b i.mid{background:var(--m-warn)}
.m-seg-row__v{font-weight:700;color:var(--m-ink);font-variant-numeric:tabular-nums;text-align:start}

/* ============================================================================
   THE MONEY CARD — a filtered figure that can switch how it is drawn
   ----------------------------------------------------------------------------
   The reader is money-first and detail-oriented, so the card leads with the
   booked figure, states it against the same period's requirement, and lets the
   same data be read as a CHART or as a LIST without reloading. The swap is a
   crossfade with a small vertical offset and a blur — blur bridges the two
   states so the eye reads one object changing rather than two objects
   swapping (emil-design-eng: "use blur to mask imperfect transitions").
   ========================================================================== */
.m-view{position:relative}
.m-view__p{transition:opacity var(--m-swap) var(--m-ease),
                      transform var(--m-swap) var(--m-ease),
                      filter var(--m-swap) var(--m-ease)}
.m-view__p[hidden]{display:none!important}
.m-view__p[data-enter]{opacity:0;transform:translateY(6px);filter:blur(3px)}
@media (prefers-reduced-motion:reduce){
  .m-view__p[data-enter]{transform:none;filter:none} }

/* DATE FILTER — presets plus a custom range. */
.m-dates{display:flex;align-items:center;gap:var(--m-2);flex-wrap:wrap}
.m-range{display:flex;align-items:center;gap:var(--m-2);background:var(--m-paper);
         border-radius:var(--m-r-chip);padding:5px 6px 5px var(--m-3);box-shadow:var(--m-hair)}
.m-range input{font:inherit;font-size:var(--m-t-cap);color:var(--m-ink);border:0;
               background:transparent;padding:3px;inline-size:126px;
               font-variant-numeric:tabular-nums}
.m-range input:focus{outline:none;box-shadow:var(--m-focus);border-radius:6px}
.m-range span{color:var(--m-faint);font-size:var(--m-t-cap)}

/* QUARTER STRIP — four cells, the current one marked. */
.m-qs{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--m-line);
      border-radius:var(--m-r-card);overflow:hidden;box-shadow:var(--m-hair)}
.m-q{background:var(--m-paper);padding:var(--m-3) var(--m-4);cursor:pointer;
     transition:background var(--m-out) var(--m-ease)}
@media (hover:hover) and (pointer:fine){ .m-q:hover{background:var(--m-page)} }
.m-q__k{font-size:var(--m-t-cap);color:var(--m-mut);display:flex;align-items:center;gap:6px}
.m-q__k i{inline-size:6px;block-size:6px;border-radius:50%;background:var(--m-ac)}
.m-q__v{font-size:var(--m-t-fig);font-weight:800;color:var(--m-ink);letter-spacing:-.8px;
        margin-block-start:2px;font-variant-numeric:tabular-nums}
.m-q__v.nil{color:var(--m-faint)}
.m-q__s{font-size:var(--m-t-micro);color:var(--m-faint);margin-block-start:2px}
.m-q__b{block-size:4px;border-radius:99px;background:var(--m-sunk);margin-block-start:var(--m-2);
        overflow:hidden}
.m-q__b i{display:block;block-size:100%;inline-size:var(--m-pct,0%);border-radius:99px;
          background:var(--m-ac);transition:inline-size var(--m-in) var(--m-move)}
.m-q[aria-current]{background:var(--m-ac-dim)}
.m-q[aria-current] .m-q__k{color:var(--m-ac-deep);font-weight:600}

/* The list rendering of the same series the chart draws. */
.m-mini{inline-size:100%;border-collapse:collapse}
.m-mini th{font-size:var(--m-t-micro);font-weight:600;color:var(--m-mut);text-align:start;
           padding:var(--m-2) var(--m-3);border-block-end:1px solid var(--m-line)}
.m-mini td{padding:9px var(--m-3);border-block-start:1px solid var(--m-line);
           font-size:var(--m-t-body);font-variant-numeric:tabular-nums}
.m-mini td:first-child{color:var(--m-ink);font-weight:600;font-variant-numeric:normal}
.m-mini tr[data-now]{background:var(--m-ac-dim)}
.m-mini .gap{color:var(--m-bad);font-weight:600}

/* A list item that is a link must not look like body copy with an underline. */
a.m-item{text-decoration:none;color:inherit;
         transition:background var(--m-out) var(--m-ease)}
@media (hover:hover) and (pointer:fine){ a.m-item:hover{background:var(--m-page)} }
a.m-item:focus-visible{outline:none;box-shadow:var(--m-focus);border-radius:var(--m-r-ctl)}
.m-item__b{display:block}
.m-item__n,.m-item__s{display:block}
/* Columns size to their content; a short stack must not leave a tall well. */
.m-board{align-items:flex-start}
.m-col{align-self:flex-start}
.m-col--rail{align-self:stretch;min-block-size:150px}

/* The brand name and the role are two lines, not one run-on string. */
.m-side__n,.m-side__r{display:block}
.m-crumb a{color:inherit;text-decoration:none}
@media (hover:hover) and (pointer:fine){ .m-crumb a:hover{color:var(--m-ac-deep)} }

/* ============================================================================
   DIALOG — the add/edit surface
   Enters from scale(.97) with a small lift, never from scale(0): nothing in
   the real world appears from nothing. Exit is faster than enter.
   ========================================================================== */
dialog.m-dlg{border:0;padding:0;background:transparent;max-inline-size:min(680px,92vw);
             inline-size:100%}
dialog.m-dlg::backdrop{background:rgba(11,13,18,.44);backdrop-filter:blur(2px);
                       animation:m-fade 200ms var(--m-ease)}
@keyframes m-fade{from{opacity:0}}
.m-dlg__p{background:var(--m-paper);border-radius:var(--m-r-band);box-shadow:var(--m-lift);
          animation:m-pop 220ms var(--m-ease)}
@keyframes m-pop{from{opacity:0;transform:scale(.97) translateY(8px)}}
@media (prefers-reduced-motion:reduce){
  .m-dlg__p,dialog.m-dlg::backdrop{animation:none} }
.m-dlg__h{display:flex;align-items:center;justify-content:space-between;gap:var(--m-3);
          padding:var(--m-4) var(--m-5);border-block-end:1px solid var(--m-line)}
.m-dlg__t{margin:0;font-size:var(--m-t-h);font-weight:700;color:var(--m-ink)}
.m-dlg__b{padding:var(--m-5);max-block-size:66vh;overflow-y:auto}
.m-dlg__f{display:flex;justify-content:flex-end;gap:var(--m-2);
          padding:var(--m-3) var(--m-5);border-block-start:1px solid var(--m-line)}
.m-x{inline-size:32px;block-size:32px;border-radius:50%;border:0;cursor:pointer;
     background:transparent;color:var(--m-mut);font-size:18px;line-height:1;
     transition:background var(--m-out) var(--m-ease)}
@media (hover:hover) and (pointer:fine){ .m-x:hover{background:var(--m-page)} }

/* FORM GRID */
.m-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--m-4)}
.m-form .full{grid-column:1 / -1}
@media (max-width:640px){ .m-form{grid-template-columns:1fr} }
textarea.m-input{resize:vertical;line-height:1.7}
.m-req::after{content:"*";color:var(--m-bad);margin-inline-start:3px}

/* KNOWLEDGE / long-text editor */
.m-kb{display:grid;grid-template-columns:260px minmax(0,1fr);gap:var(--m-4)}
@media (max-width:900px){ .m-kb{grid-template-columns:1fr} }
.m-kb__l{display:flex;flex-direction:column;gap:2px}
.m-kb__i{display:flex;align-items:center;justify-content:space-between;gap:var(--m-2);
         padding:9px var(--m-3);border-radius:var(--m-r-ctl);border:0;background:transparent;
         cursor:pointer;font:inherit;font-size:var(--m-t-body);color:var(--m-ink-2);
         text-align:start;transition:background var(--m-out) var(--m-ease)}
@media (hover:hover) and (pointer:fine){ .m-kb__i:hover{background:var(--m-page)} }
.m-kb__i[aria-current]{background:var(--m-ac-dim);color:var(--m-ac-deep);font-weight:600}
.m-kb__i b{font-size:var(--m-t-micro);font-weight:700;font-variant-numeric:tabular-nums}
.m-kb__i b.low{color:var(--m-bad)} .m-kb__i b.mid{color:var(--m-warn)} .m-kb__i b.ok{color:var(--m-ok)}

/* STEPPER — the campaign wizard */
.m-steps{display:flex;gap:var(--m-2);margin-block-end:var(--m-5);flex-wrap:wrap}
.m-step{display:flex;align-items:center;gap:var(--m-2);font-size:var(--m-t-cap);
        color:var(--m-faint)}
.m-step i{inline-size:22px;block-size:22px;border-radius:50%;display:grid;place-items:center;
          font-size:var(--m-t-micro);font-weight:700;background:var(--m-sunk);color:var(--m-mut);
          font-variant-numeric:tabular-nums}
.m-step[aria-current]{color:var(--m-ink);font-weight:600}
.m-step[aria-current] i{background:var(--m-ac);color:#fff}
.m-step[data-done] i{background:var(--m-ok-dim);color:var(--m-ok)}
.m-step::after{content:"";inline-size:22px;block-size:1px;background:var(--m-line-2)}
.m-step:last-child::after{display:none}

/* TIMELINE — the event ledger */
.m-tl{display:flex;flex-direction:column}
.m-tl__i{display:grid;grid-template-columns:22px minmax(0,1fr) auto;gap:var(--m-3);
         padding:var(--m-3) 0;position:relative}
.m-tl__d{inline-size:9px;block-size:9px;border-radius:50%;background:var(--m-ac);
         margin-block-start:6px;margin-inline-start:6px;position:relative;z-index:1}
.m-tl__d.ok{background:var(--m-ok)} .m-tl__d.warn{background:var(--m-warn)}
.m-tl__d.idle{background:var(--m-line-2)}
.m-tl__i:not(:last-child)::before{content:"";position:absolute;inset-block:22px -6px;
         inset-inline-start:10px;inline-size:1px;background:var(--m-line)}
.m-tl__n{font-size:var(--m-t-body);color:var(--m-ink)}
.m-tl__s{font-size:var(--m-t-cap);color:var(--m-faint);margin-block-start:2px}
.m-tl__t{font-size:var(--m-t-micro);color:var(--m-faint);white-space:nowrap;
         font-variant-numeric:tabular-nums}

/* TOGGLE */
.m-sw{inline-size:38px;block-size:22px;border-radius:99px;background:var(--m-line-2);
      border:0;cursor:pointer;padding:0;position:relative;flex:0 0 auto;
      transition:background var(--m-out) var(--m-ease)}
.m-sw::after{content:"";position:absolute;inset-block-start:3px;inset-inline-start:3px;
      inline-size:16px;block-size:16px;border-radius:50%;background:#fff;
      box-shadow:0 1px 2px rgba(16,24,40,.2);
      transition:transform var(--m-swap) var(--m-ease)}
.m-sw[aria-checked="true"]{background:var(--m-ac)}
.m-sw[aria-checked="true"]::after{transform:translateX(-16px)}

/* KPI GRID for the merged home */
.m-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--m-3)}
@media (max-width:1100px){ .m-kpis{grid-template-columns:repeat(2,minmax(0,1fr))} }

exec
/bin/zsh -lc 'cat massar-ds/shell.js' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
/* Massar shell — the side menu and the sub-tab strip, injected once so every
   screen shares them. The structure mirrors the live app exactly: seven doors,
   each with its own ordered sub-destinations, the first of which is the door's
   own landing route. A door with one entry renders no tab strip at all.
   A screen sets `data-nav` (door) and `data-sub` (route) on <body>. */
(function () {
  var DOORS = [
    { id: "home",     l: "الرئيسية",  d: "M3 10.5 12 3l9 7.5M5.5 9.5V20h13V9.5" },
    { id: "opps",     l: "فرص البيع", d: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z", n: "6" },
    { id: "accounts", l: "العملاء",   d: "M16 20v-2a4 4 0 0 0-8 0v2M12 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7", n: "16" },
    { id: "products", l: "المنتجات",  d: "M21 8 12 3 3 8l9 5 9-5ZM3 8v8l9 5 9-5V8", n: "6" },
    { id: "kmon",     l: "الحملات",   d: "M4 11v3l14 5V6L4 11ZM4 11H3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1" },
    { id: "reports",  l: "التقارير",  d: "M4 20V10M10 20V4M16 20v-7M22 20H2" },
    { id: "settings", l: "الإعدادات", d: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1 2 2 0 1 1-4 0 1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 4.6 15a2 2 0 1 1 0-4 1.6 1.6 0 0 0 1.1-2.7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 11 4.6a2 2 0 1 1 4 0 1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7 2 2 0 1 1 0 4Z" }
  ];
  var SUBS = {
    opps:     [["opps","الفرص"],["board","لوحة المتابعة"],["triage","فرز الردود"],["pipeline","سجل الأحداث"]],
    accounts: [["accounts","العملاء"],["customers","المحادثات"],["indicators","مؤشرات الاستخدام"],["tasks","المهام"],["notes","الملاحظات"]],
    products: [["products","المنتجات"],["knowledge","معرفة المنتج"],["perf","المستهدفات والأداء"],["org","الهيكل التنظيمي"]],
    kmon:     [["kmon","متابعة الحملات"],["aimkt","إنشاء حملة"],["targets","جهات الاستهداف"],["partners","شركاء المبيعات"]],
    settings: [["settings","مراحل البيع"],["divisions","الأقسام"],["team","الفريق"],["users","المستخدمون والصلاحيات"],["audit","سجل التدقيق"]]
  };

  var door = document.body.getAttribute("data-nav") || "home";
  var sub  = document.body.getAttribute("data-sub") || door;

  var items = DOORS.map(function (i) {
    return '<a class="m-nav" href="' + i.id + '.html" data-t="' + i.l + '" title="' + i.l + '"' +
      (i.id === door ? ' aria-current="page"' : "") + '>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + i.d + '"/></svg>' +
      "<span>" + i.l + "</span>" + (i.n ? "<b>" + i.n + "</b>" : "") + "</a>";
  }).join("");

  var side = document.createElement("nav");
  side.className = "m-side";
  side.setAttribute("aria-label", "التنقل");
  side.innerHTML =
    '<div class="m-side__b"><span class="m-side__logo">م</span>' +
      '<span class="m-side__w"><span class="m-side__n">مسار</span>' +
      '<span class="m-side__r">مدير النظام</span></span></div>' +
    '<div class="m-side__nav">' + items + "</div>" +
    '<div class="m-side__f"><button class="m-side__t" type="button" aria-expanded="true">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 7 5 5-5 5" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
      "<span>طيّ القائمة</span></button></div>";
  document.querySelector(".m-shell").prepend(side);

  // The sub-tab strip renders under the page title, so a door's destinations
  // are reachable in one click from anywhere inside that door.
  var host = document.querySelector("[data-subs]");
  if (host && SUBS[door]) {
    host.innerHTML = '<div class="m-tabs" role="tablist">' + SUBS[door].map(function (s) {
      return '<a class="m-tab" role="tab" href="' + s[0] + '.html"' +
        (s[0] === sub ? ' aria-selected="true"' : ' aria-selected="false"') + ">" + s[1] + "</a>";
    }).join("") + "</div>";
  }

  var KEY = "massar.side.collapsed";
  function read() { try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; } }
  function write(v) { try { localStorage.setItem(KEY, v ? "1" : "0"); } catch (e) {} }

  var btn = side.querySelector(".m-side__t");
  function apply(c, animate) {
    // The first paint must not animate, or the rail slides in on every load.
    if (!animate) side.style.transition = "none";
    if (c) side.setAttribute("data-collapsed", ""); else side.removeAttribute("data-collapsed");
    btn.setAttribute("aria-expanded", c ? "false" : "true");
    if (!animate) { void side.offsetWidth; side.style.transition = ""; }
  }
  apply(read(), false);
  function toggle() { var n = !side.hasAttribute("data-collapsed"); apply(n, true); write(n); }
  btn.addEventListener("click", toggle);
  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "b" || e.key === "B")) { e.preventDefault(); toggle(); }
  });

  /* ---- Dialogs. Any [data-open="id"] opens the <dialog id>. Escape and the
     backdrop close it. The panel enters from scale(.97), never scale(0) —
     nothing in the real world appears from nothing. ---- */
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-open]");
    if (t) { var dlg = document.getElementById(t.getAttribute("data-open"));
             if (dlg) { dlg.showModal(); } return; }
    var c = e.target.closest("[data-close]");
    if (c) { c.closest("dialog").close(); return; }
  });
  document.addEventListener("click", function (e) {
    if (e.target.tagName === "DIALOG") e.target.close();   // backdrop
  });
})();

exec
/bin/zsh -lc "wc -lc massar-ds/home.html massar-ds/products.html massar-ds/product.html massar-ds/opps.html massar-ds/reports.html
sed -n '1,120p' massar-ds/home.html" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
     237   27881 massar-ds/home.html
      42   13152 massar-ds/products.html
      50   13232 massar-ds/product.html
      50   16588 massar-ds/opps.html
      52   10651 massar-ds/reports.html
     431   81504 total
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — الرئيسية</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="home" data-sub="home">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a"><button class="m-btn">تصدير</button><button class="m-btn m-btn--primary" data-open="dlgOpp">فرصة جديدة</button></div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb">الرئيسية</div>
          <h1 class="m-h1">الأداء التجاري</h1>
        </div>
        <div class="m-row"><div class="m-dates"><div class="m-seg" role="group" aria-label="المدى الزمني"><button data-p="7" aria-pressed="false">أسبوع</button><button data-p="14" aria-pressed="false">أسبوعان</button><button data-p="30" aria-pressed="false">شهر</button><button data-p="q" aria-pressed="false">الربع</button><button data-p="year" aria-pressed="true">السنة</button></div><label class="m-range"><input type="date" id="d1" value="2026-01-01" aria-label="من"><span>—</span><input type="date" id="d2" value="2026-09-16" aria-label="إلى"></label></div></div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">

<!-- THE MONEY CARD — filtered, and switchable between chart and list -->
<section class="m-card m-card--band">
  <div class="m-between" style="align-items:flex-start;flex-wrap:wrap;gap:var(--m-4)">
    <div>
      <div class="m-card__k" id="periodLabel">المحقق · السنة المالية 2026</div>
      <div class="m-lead" style="margin-block-start:var(--m-2)">
        <div class="m-lead__v"><span class="m-n" id="bookedV">0</span><small>ر.س</small></div>
        <span class="m-delta m-delta--bad" id="deltaPill">&#9662; <span class="m-n">34,000</span> ر.س دون المطلوب</span>
      </div>
    </div>
    <div class="m-row" style="align-items:flex-start;gap:var(--m-5);flex-wrap:wrap">
      <div class="m-stat"><div class="m-stat__k">المطلوب</div>
        <div class="m-stat__v"><span class="m-n" id="targetV">34,000</span></div></div>
      <div class="m-stat m-stat--ac"><div class="m-stat__k">خط البيع</div>
        <div class="m-stat__v"><span class="m-n" id="openV">4,200</span></div></div>
      <div class="m-stat m-stat--mut"><div class="m-stat__k">صفقات رابحة</div>
        <div class="m-stat__v"><span class="m-n">0</span></div></div>
      <div class="m-seg" role="group" aria-label="طريقة العرض">
        <button data-v="chart" aria-pressed="true">رسم</button>
        <button data-v="list" aria-pressed="false">قائمة</button>
      </div>
    </div>
  </div>
  <div class="m-view" style="margin-block-start:var(--m-4)">
    <div class="m-view__p" id="vChart">
      <svg class="m-chart" viewBox="0 0 900 280" role="img" aria-label="المطلوب شهريًا مقابل المحقق">
        <defs>
          <linearGradient id="mBar" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#2F6BFF" stop-opacity=".28"/>
            <stop offset="100%" stop-color="#2F6BFF" stop-opacity="0"/></linearGradient>
          <pattern id="mDots" width="14" height="14" patternUnits="userSpaceOnUse">
            <circle cx="1.5" cy="1.5" r="1.5" fill="#E4E8F0"/></pattern>
        </defs>
        <rect x="56" y="18" width="816" height="200" fill="url(#mDots)"/>
        <g id="bars"></g><line x1="56" y1="218" x2="872" y2="218" stroke="#DFE3EA"/><g id="axis"></g>
      </svg>
    </div>
    <div class="m-view__p" id="vList" hidden>
      <table class="m-mini"><thead><tr><th>الشهر</th><th>المطلوب</th><th>المحقق</th>
      <th>الفجوة</th><th>فرص أُنشئت</th></tr></thead><tbody id="listBody"></tbody></table>
    </div>
  </div>
</section>

<div class="m-qs" style="margin-block-start:var(--m-4)" id="quarters"></div>
<div class="m-grid m-grid--3" style="margin-block-start:var(--m-4)"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">جاهزية المساعد</h2><span class="m-chip m-chip--bad">غير جاهز</span></div><div class="m-arc"><svg viewBox="0 0 200 116" role="img" aria-label="جاهزية المساعد 34"><path class="m-arc__track" d="M18,104 A82,82 0 0 1 182,104"/><path class="m-arc__fill m-arc__fill--warn" style="--m-dash:88" d="M18,104 A82,82 0 0 1 182,104"/></svg><div class="m-arc__c"><div class="m-arc__v"><span class="m-n">34</span></div><div class="m-arc__k">من <span class="m-n">100</span></div></div></div><div class="m-segs"><div class="m-seg-row"><span class="m-seg-row__t">وصف المنتج</span><span class="m-seg-row__b"><i class="ok" style="--m-pct:80%"></i></span><span class="m-seg-row__v"><span class="m-n">80%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">حالات الاستخدام</span><span class="m-seg-row__b"><i class="mid" style="--m-pct:60%"></i></span><span class="m-seg-row__v"><span class="m-n">60%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">الأسئلة الشائعة</span><span class="m-seg-row__b"><i class="mid" style="--m-pct:45%"></i></span><span class="m-seg-row__v"><span class="m-n">45%</span></span></div><div class="m-seg-row"><span class="m-seg-row__t">الأسعار والباقات</span><span class="m-seg-row__b"><i class="low" style="--m-pct:10%"></i></span><span class="m-seg-row__v"><span class="m-n">10%</span></span></div></div><div class="m-empty__a"><a class="m-link" href="knowledge.html">كل الأقسام &#8592;</a></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">صحة خط البيع</h2></div><div class="m-matrix" aria-hidden="true"><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i><i class="is-ac"></i></div><div class="m-key"><span><i style="background:var(--m-ac)"></i>على المسار <span class="m-n">6</span></span><span><i style="background:var(--m-warn-line)"></i>متأخرة <span class="m-n">0</span></span><span><i style="background:var(--m-line-2)"></i>بانتظار الدعم <span class="m-n">0</span></span><span><i style="background:var(--m-bad-line)"></i>مرفوضة <span class="m-n">0</span></span></div><div class="m-card__h" style="margin-block:var(--m-5) var(--m-3)"><h2 class="m-card__t">العملاء</h2></div><div class="m-matrix" aria-hidden="true"><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i><i class="is-ok"></i></div><div class="m-key"><span><i style="background:var(--m-ok-line)"></i>معتمد <span class="m-n">16</span></span><span><i style="background:var(--m-line-2)"></i>بانتظار <span class="m-n">0</span></span><span><i style="background:var(--m-bad-line)"></i>مرفوض <span class="m-n">0</span></span></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">النشاط · <span class="m-n">21</span> يومًا</h2><span class="m-chip m-chip--bad">صامت</span></div><div class="m-heat" aria-hidden="true"><i class="l3"></i><i class="l2"></i><i class="l1"></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="m-heat__ax"><span>اليوم</span><span>قبل <span class="m-n">21</span> يومًا</span></div><div class="m-card__h" style="margin-block:var(--m-5) var(--m-3)"><h2 class="m-card__t">قمع الحملة 38</h2></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">أُرسلت</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">21</span></span></div><div class="m-fstep"><span class="m-fstep__k">وصلت</span><span class="m-fstep__b"><i style="--m-pct:90%"></i></span><span class="m-fstep__v"><span class="m-n">19</span></span></div><div class="m-fstep"><span class="m-fstep__k">شوهدت</span><span class="m-fstep__b"><i style="--m-pct:57%"></i></span><span class="m-fstep__v"><span class="m-n">12</span> <span class="m-fstep__d">&#9662; <span class="m-n">37%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">رُدّ عليها</span><span class="m-fstep__b"><i style="--m-pct:19%"></i></span><span class="m-fstep__v"><span class="m-n">4</span> <span class="m-fstep__d">&#9662; <span class="m-n">67%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">مهتم</span><span class="m-fstep__b"><i style="--m-pct:9%"></i></span><span class="m-fstep__v"><span class="m-n">2</span></span></div></div></section></div><div class="m-grid m-grid--main" style="margin-block-start:var(--m-4)"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">أين يتسرّب خط البيع</h2><a class="m-link" href="reports.html">التقارير &#8592;</a></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">تواصل أولي</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">4</span></span></div><div class="m-fstep"><span class="m-fstep__k">اكتشاف الحاجة</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span> <span class="m-fstep__d">&#9662; <span class="m-n">75%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض المنتج</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض السعر</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span></span></div><div class="m-fstep"><span class="m-fstep__k">التفاوض</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">رابح</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div></div></section><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">يحتاج قرارك</h2><span class="m-cap"><span class="m-n">4</span></span></div><a class="m-item" href="perf.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">5</span></span><span class="m-item__b"><span class="m-item__n">منتجات بلا مستهدف</span><span class="m-item__s">من <span class="m-n">6</span></span></span><span class="m-chip m-chip--warn">يشوّه النسبة</span></a><a class="m-item" href="opps.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">5</span></span><span class="m-item__b"><span class="m-item__n">بنود بلا تسعير</span><span class="m-item__s">من <span class="m-n">6</span></span></span><span class="m-chip m-chip--warn">يشوّه القيمة</span></a><a class="m-item" href="accounts.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">16</span></span><span class="m-item__b"><span class="m-item__n">عملاء بلا مسؤول</span><span class="m-item__s">من <span class="m-n">16</span></span></span><span class="m-chip">بلا متابعة</span></a><a class="m-item" href="board.html" style="padding-inline:var(--m-4)"><span class="m-av m-av--sq"><span class="m-n">6</span></span><span class="m-item__b"><span class="m-item__n">بنود راكدة</span><span class="m-item__s"><span class="m-n">35</span> يومًا بلا حركة</span></span><span class="m-chip m-chip--bad">متوقفة</span></a></section></div><section class="m-card m-card--pad0" style="margin-block-start:var(--m-4)"><div class="m-tools"><h2 class="m-card__t">خط البيع</h2><span class="m-row"><span class="m-cap"><span class="m-n">6</span> بنود · <span class="m-n">4,200</span> ر.س</span><a class="m-link" href="board.html">اللوحة &#8592;</a></span></div><div class="m-board" style="padding:0 var(--m-3) var(--m-3)"><div class="m-col" style="--m-tone:#5B6472"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">تواصل أولي</span><span class="m-col__c"><span class="m-n">4</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col" style="--m-tone:#0072E9"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">اكتشاف الحاجة</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#8B5CF6" tabindex="0" title="عرض المنتج"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض المنتج</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#7C3AED" tabindex="0" title="التقييم التقني"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التقييم التقني</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col" style="--m-tone:#2F6BFF"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض السعر</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v"><span class="m-n">4,200</span> ر.س</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#B45309" tabindex="0" title="التفاوض والاعتماد"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التفاوض والاعتماد</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#15803D" tabindex="0" title="رابح"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">رابح</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#BE123C" tabindex="0" title="خاسر"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">خاسر</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div></div></section>
      </div>
    </main>
  </div>
</div>
<dialog class="m-dlg" id="dlgOpp"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة فرصة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">العميل</label><select class="m-select"><option>DL000</option><option>ابرهيم</option><option>العمدة</option><option>أبو حمزه</option><option>أبو نور</option><option>صيدلية الدواء</option><option>صيدلية الدواء (مثال)</option><option>صيدلية الدواء (مثال)</option></select></div><div class="m-field"><label class="m-label m-req">المنتج</label><select class="m-select"><option>الإجازات المرضية</option><option>التقارير الطبية</option><option>الشهادات الصحية</option><option>تكامل الأنظمة (HIS/ERP)</option><option>خدمات التطعيمات</option><option>سجل التطعيمات الوطني</option><option>صحة أعمال Plus</option><option>فحص الموظفين</option></select></div><div class="m-field"><label class="m-label m-req">المرحلة</label><select class="m-select"><option>تواصل أولي</option><option>اكتشاف الحاجة</option><option>عرض المنتج</option><option>التقييم التقني</option><option>عرض السعر</option><option>التفاوض والاعتماد</option></select></div><div class="m-field"><label class="m-label m-req">المصدر</label><select class="m-select"><option>حملة واتساب</option><option>مكالمة</option><option>زيارة</option><option>إحالة</option><option>طلب وارد</option></select></div><div class="m-field"><label class="m-label">الكمية</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">السعر للوحدة (ر.س)</label><input class="m-input" type="number" placeholder="لم تُسعَّر" value=""></div><div class="m-field"><label class="m-label">عدد السنوات</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">الخصم %</label><input class="m-input" type="number" placeholder="0" value=""></div><div class="m-field"><label class="m-label">الموظف المسؤول</label><select class="m-select"><option>بلا مسؤول</option></select></div><div class="m-field"><label class="m-label">تاريخ الإغلاق المتوقع</label><input class="m-input" type="date" placeholder="" value=""></div><div class="m-field"><label class="m-label">الشريك</label><select class="m-select"><option>لا شريك</option></select></div><div class="m-field full"><label class="m-label">ملاحظة</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة الفرصة</button></div></form></dialog>
<script src="shell.js"></script>
<script>
/* ---------------------------------------------------------------------------
   The ledger, as the screen knows it. Every figure below is a real value from
   the live system; nothing is invented and nothing is dropped.
   `won` is booked revenue, `made` is opportunity value created in the month,
   `lines` is how many opportunity lines were opened.
   --------------------------------------------------------------------------- */
var YEAR = 2026, TARGET = 34000, MONTHLY = TARGET / 12;
var M = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"];
var LEDGER = [
  {m:0,won:0,made:0,lines:0},{m:1,won:0,made:0,lines:0},{m:2,won:0,made:0,lines:0},
  {m:3,won:0,made:0,lines:0},{m:4,won:0,made:0,lines:0},{m:5,won:0,made:0,lines:0},
  {m:6,won:0,made:0,lines:0},{m:7,won:0,made:4200,lines:6},{m:8,won:0,made:0,lines:0},
  {m:9,won:0,made:0,lines:0},{m:10,won:0,made:0,lines:0},{m:11,won:0,made:0,lines:0}
];
var TODAY = new Date(YEAR, 8, 16);           // 16 Sep 2026
var fmt = function (n) { return n.toLocaleString("en-US"); };
var $ = function (id) { return document.getElementById(id) || { style:{}, set textContent(v){}, set innerHTML(v){}, setAttribute:function(){}, insertAdjacentHTML:function(){}, className:"" }; };

function rangeFor(preset) {
  var end = new Date(TODAY), start;
  if (preset === "year") start = new Date(YEAR, 0, 1);
  else if (preset === "q") start = new Date(YEAR, Math.floor(TODAY.getMonth() / 3) * 3, 1);
  else { start = new Date(TODAY); start.setDate(start.getDate() - (parseInt(preset, 10) - 1)); }
  return [start, end];
}

function sum(start, end) {
  // A month counts when any part of it falls inside the range. The target for
  // a partial month is pro-rated by days, so «المطلوب» never overstates a
  // one-week window — the reader is comparing money to money.
  var won = 0, made = 0, lines = 0, req = 0;
  for (var i = 0; i < 12; i++) {
    var ms = new Date(YEAR, i, 1), me = new Date(YEAR, i + 1, 0);
    var a = ms > start ? ms : start, b = me < end ? me : end;

exec
/bin/zsh -lc "sed -n '120,260p' massar-ds/home.html
cat massar-ds/products.html" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
    var a = ms > start ? ms : start, b = me < end ? me : end;
    if (a > b) continue;
    var days = (b - a) / 86400000 + 1, full = me.getDate();
    req += MONTHLY * (days / full);
    won += LEDGER[i].won; made += LEDGER[i].made; lines += LEDGER[i].lines;
  }
  return { won: won, made: made, lines: lines, req: Math.round(req) };
}

function label(start, end, preset) {
  if (preset === "year") return "المحقق · السنة المالية " + YEAR;
  if (preset === "q") return "المحقق · الربع " + (Math.floor(TODAY.getMonth() / 3) + 1) + " · " + YEAR;
  return "المحقق · " + start.getDate() + " " + M[start.getMonth()] +
         " — " + end.getDate() + " " + M[end.getMonth()];
}

function paint(preset, start, end) {
  var s = sum(start, end);
  $("periodLabel").textContent = label(start, end, preset);
  $("bookedV").textContent = fmt(s.won);
  $("targetV").textContent = fmt(s.req);
  $("openV").textContent   = fmt(s.made);
  $("wonV").textContent    = "0";

  var gap = s.req - s.won;
  var pill = $("deltaPill");
  pill.className = "m-delta " + (gap > 0 ? "m-delta--bad" : "m-delta--ok");
  pill.innerHTML = gap > 0
    ? '▾ <span class="m-n">' + fmt(gap) + '</span> ر.س دون المطلوب'
    : '▴ مطابق للمطلوب';

  // bars: required per month; the cap dot marks what was booked
  var bars = $("bars"), axis = $("axis");
  bars.innerHTML = ""; axis.innerHTML = "";
  var max = Math.max(MONTHLY * 1.25, 1), x0 = 872, step = 68;
  for (var i = 0; i < 12; i++) {
    var x = x0 - i * step - 26;                       // RTL: يناير at the right
    var inR = new Date(YEAR, i, 15) >= start && new Date(YEAR, i, 15) <= end;
    var hReq = Math.round(200 * (MONTHLY / max));
    bars.insertAdjacentHTML("beforeend",
      '<rect class="m-chart__bar" x="' + x + '" y="' + (218 - hReq) + '" width="26" height="' +
      hReq + '" rx="13" opacity="' + (inR ? 1 : .3) + '"/>' +
      '<circle r="5" cx="' + (x + 13) + '" cy="218" fill="' + (inR ? "#BE123C" : "#DFE3EA") + '"/>');
    if (i % 2 === 0) axis.insertAdjacentHTML("beforeend",
      '<text class="m-chart__ax" x="' + (x + 13) + '" y="242" text-anchor="middle">' + M[i] + "</text>");
  }

  // list: the same series, read as a table
  var rows = "";
  for (var j = 0; j < 12; j++) {
    var inR2 = new Date(YEAR, j, 15) >= start && new Date(YEAR, j, 15) <= end;
    if (!inR2) continue;
    rows += '<tr' + (j === TODAY.getMonth() ? ' data-now' : '') + '><td>' + M[j] + "</td>" +
      '<td class="m-n">' + fmt(Math.round(MONTHLY)) + "</td>" +
      '<td class="m-n">' + fmt(LEDGER[j].won) + "</td>" +
      '<td class="m-n gap">' + fmt(Math.round(MONTHLY) - LEDGER[j].won) + "</td>" +
      '<td class="m-n">' + (LEDGER[j].lines || "—") + "</td></tr>";
  }
  $("listBody").innerHTML = rows;
}

function paintQuarters() {
  var q = $("quarters"), cur = Math.floor(TODAY.getMonth() / 3), out = "";
  for (var i = 0; i < 4; i++) {
    var won = 0, req = 0;
    for (var m = i * 3; m < i * 3 + 3; m++) { won += LEDGER[m].won; req += MONTHLY; }
    var pct = req ? Math.round((won / req) * 100) : 0;
    out += '<button class="m-q" type="button"' + (i === cur ? ' aria-current="true"' : '') + '>' +
      '<span class="m-q__k">' + (i === cur ? "<i></i>" : "") + "الربع " + (i + 1) + "</span>" +
      '<div class="m-q__v' + (won ? "" : " nil") + '"><span class="m-n">' + fmt(won) + "</span></div>" +
      '<div class="m-q__s">من <span class="m-n">' + fmt(Math.round(req)) +
        '</span> ر.س · <span class="m-n">' + pct + '%</span></div>' +
      '<div class="m-q__b"><i style="--m-pct:' + pct + '%"></i></div></button>';
  }
  q.innerHTML = out;
}

/* presets */
var presets = document.querySelectorAll('[data-p]');
presets.forEach(function (b) {
  b.addEventListener("click", function () {
    presets.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
    b.setAttribute("aria-pressed", "true");
    var r = rangeFor(b.dataset.p);
    $("d1").value = r[0].toISOString().slice(0, 10);
    $("d2").value = r[1].toISOString().slice(0, 10);
    paint(b.dataset.p, r[0], r[1]);
  });
});
["d1", "d2"].forEach(function (id) {
  $(id).addEventListener("change", function () {
    presets.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
    paint("custom", new Date($("d1").value), new Date($("d2").value));
  });
});

/* chart <-> list, crossfaded. Blur bridges the two states so the eye reads one
   object changing rather than two objects swapping. */
var views = document.querySelectorAll('[data-v]');
views.forEach(function (b) {
  b.addEventListener("click", function () {
    views.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
    b.setAttribute("aria-pressed", "true");
    var show = b.dataset.v === "chart" ? $("vChart") : $("vList");
    var hide = b.dataset.v === "chart" ? $("vList") : $("vChart");
    hide.hidden = true;
    show.hidden = false;
    show.setAttribute("data-enter", "");
    void show.offsetWidth;                 // force the start state to land
    show.removeAttribute("data-enter");
  });
});

paintQuarters();
paint("year", new Date(YEAR, 0, 1), TODAY);
</script>
</body>
</html>
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — المنتجات</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="products" data-sub="products">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a"><button class="m-btn">استيراد</button><button class="m-btn m-btn--primary" data-open="dlgProd">إضافة منتج</button></div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb">المنتجات</div>
          <h1 class="m-h1">المنتجات</h1>
        </div>
        <div class="m-row"><select class="m-select" style="inline-size:auto"><option>كل القطاعات</option><option>بلا قطاع</option><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option></select><select class="m-select" style="inline-size:auto"><option>كل الحالات</option><option>لا يبيعها المساعد</option><option>يبيعها وتنقصها أشياء</option><option>جاهزة للمساعد</option></select><select class="m-select" style="inline-size:auto"><option>حسب الاسم</option><option>الأعلى تحقيقًا</option><option>الأعلى مفتوحًا</option><option>غير الجاهزة أولًا</option></select><button class="m-btn">المؤرشفة</button></div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">
<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">المحقق 2026</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">من مستهدف 34,000 ر.س · 0٪</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">لا يبيعها المساعد</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">من 8 منتجات</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">بلا سعر منشور</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">من 8 منتجات</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">قطاع مُستنتَج</div><div class="m-q__v"><span class="m-n">4</span></div><div class="m-q__s">تحتاج تأكيدًا</div></div></div><div class="m-alert" style="margin-block-end:var(--m-4)"><span class="m-alert__t"><span class="m-n">6</span> منتجات بلا ملف تعريفي</span><span class="m-alert__d">مهارة إعداد العرض تُنتجه بمساعد ذكاء اصطناعي · <code style="font-family:monospace;font-size:var(--m-t-micro)">lean-proposal-deck-v2.3.1-upload.zip</code></span><button class="m-btn">تحميل المهارة</button></div><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المنتج</th><th>جاهزية المساعد</th><th>السعر المنشور</th><th>المستهدف 2026</th><th>المحقق</th><th>المفتوح الآن</th><th></th></tr></thead><tbody><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">الإجازات المرضية</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--ok"><span class="m-n">80%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-v">18,000 ر.س / سنة</span><div class="m-item__s">يبدأ من · باقتان</div></td><td><span class="m-td-v"><span class="m-n">34,000</span> ر.س</span><div class="m-item__s">ربع واحد من أربعة</div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-v"><span class="m-n">4,200</span> ر.س</span><div class="m-item__s">بندان · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">التقارير الطبية</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--warn"><span class="m-n">68%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص وفق الحجم</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">الشهادات الصحية</span></a><div class="m-item__s">قطاع الصيدليات</div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">تكامل الأنظمة (HIS/ERP)</span></a><div class="m-item__s">قطاع المستشفيات</div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">مشروع تكامل واشتراك سنوي، يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بندان · بندان بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">خدمات التطعيمات</span></a><div class="m-item__s">قطاع الصيدليات · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">45%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي يحدده المختص</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بند واحد · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">سجل التطعيمات الوطني</span></a><div class="m-item__s">قطاع الصيدليات · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--ok"><span class="m-n">90%</span></span><span class="m-cap">يبيعه المساعد · ينقصه تحديث كتالوج المساعد</span></span></td><td><span class="m-td-v">20,000 ر.س / سنة</span><div class="m-item__s">hello</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">بند واحد · بند واحد بلا تسعير</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">صحة أعمال Plus</span></a><div class="m-item__s">قطاع الأعمال · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--bad"><span class="m-n">0%</span></span><span class="m-cap">لا يبيعه المساعد · بانتظار اعتماد النص الحالي</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">لا سعر منشور</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr><tr><td><a href="product.html" style="text-decoration:none;color:inherit"><span class="m-td-n">فحص الموظفين</span></a><div class="m-item__s">قطاع الأعمال · <span class="m-chip">مُستنتَج</span></div></td><td><span class="m-row"><span class="m-chip m-chip--warn"><span class="m-n">73%</span></span><span class="m-cap">يبيعه المساعد · ينقصه ملف المعرفة</span></span></td><td><span class="m-td-nil">لا سعر منشور</span><div class="m-item__s">اشتراك سنوي بتسعير لكل فحص، يحدده المختص وفق الحجم</div></td><td><span class="m-chip m-chip--warn">بلا مستهدف</span><div class="m-item__s"></div></td><td class="m-td-v m-td-nil"><span class="m-n">0</span> ر.س</td><td><span class="m-td-nil">—</span><div class="m-item__s">لا بنود مفتوحة</div></td><td><button class="m-btn">فتح</button></td></tr></tbody></table><div class="m-tools"><span class="m-cap"><span class="m-n">1</span>–<span class="m-n">8</span> من <span class="m-n">8</span> منتجات</span><span class="m-cap">المحقق للمعروض <span class="m-n">0</span> ر.س</span></div></section>
      </div>
    </main>
  </div>
</div>
<dialog class="m-dlg" id="dlgProd"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة منتج</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">اسم المنتج</label><input class="m-input" type="text" placeholder="" value=""></div><div class="m-field"><label class="m-label m-req">القطاع</label><select class="m-select"><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option><option>بلا قطاع</option></select></div><div class="m-field"><label class="m-label">القسم</label><select class="m-select"><option>بلا قسم</option></select></div><div class="m-field"><label class="m-label">مدير المنتج</label><select class="m-select"><option>بلا تحديد</option></select></div><div class="m-field"><label class="m-label">السعر المنشور</label><input class="m-input" type="text" placeholder="لا سعر منشور" value=""></div><div class="m-field"><label class="m-label">وحدة التسعير</label><select class="m-select"><option>سنة</option><option>شهر</option><option>لكل فحص</option><option>مشروع</option></select></div><div class="m-field"><label class="m-label">حالة المساعد</label><select class="m-select"><option>يبيعه المساعد</option><option>لا يبيعه المساعد</option></select></div><div class="m-field"><label class="m-label">المستهدف 2026 (ر.س)</label><input class="m-input" type="number" placeholder="بلا مستهدف" value=""></div><div class="m-field full"><label class="m-label">وصف المنتج</label><textarea class="m-input" rows="4" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة المنتج</button></div></form></dialog>
<script src="shell.js"></script>

</body>
</html>

exec
/bin/zsh -lc 'cat massar-ds/product.html' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — الإجازات المرضية</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="products" data-sub="products">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a"><button class="m-btn">أطلق حملة بهذا المنتج</button><button class="m-btn m-btn--primary">حفظ</button></div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb"><a href="products.html">المنتجات</a> / الإجازات المرضية</div>
          <h1 class="m-h1">الإجازات المرضية</h1>
        </div>
        <div class="m-row"><span class="m-chip">قطاع المستشفيات</span><span class="m-chip">مدير المنتج: بلا تحديد</span></div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">
<div class="m-tabs" role="tablist"><button class="m-tab" role="tab" aria-selected="true" data-t="q0">نظرة عامة</button><button class="m-tab" role="tab" aria-selected="false" data-t="q1">معرفة المنتج <b>80٪</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q2">الأسعار والباقات <b>2</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q3">المستهدفات <b>يحتاج إكمالًا</b></button><button class="m-tab" role="tab" aria-selected="false" data-t="q4">البيانات والإدارة</button></div><div class="m-view" style="margin-block-start:var(--m-4)"><section class="m-view__p" id="q0" role="tabpanel"><div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">الفرص المفتوحة</div><div class="m-q__v"><span class="m-n">2</span></div><div class="m-q__s">4,200 ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الحملات</div><div class="m-q__v"><span class="m-n">15</span></div><div class="m-q__s">ذكرت المنتج</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">قراءة المساعد</div><div class="m-q__v"><span class="m-n">1</span></div><div class="m-q__s">اهتمام رصده المساعد</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الجهات المستهدفة بالوسم</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">—</div></div></div><div class="m-grid m-grid--main"><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">الفرص المفتوحة</h2><a class="m-link" href="opps.html">كل فرص المنتج &#8592;</a></div><table class="m-table"><thead><tr><th>العميل</th><th>المرحلة</th><th>القيمة</th><th>في المرحلة</th></tr></thead><tbody><tr><td class="m-td-n">DL000</td><td><span class="m-chip m-chip--ac">عرض السعر</span></td><td class="m-td-v"><span class="m-n">4,200</span> ر.س</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td></tr><tr><td class="m-td-n">العمدة</td><td><span class="m-chip">اكتشاف الحاجة</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td class="m-td-v"><span class="m-n">35</span> يومًا</td></tr></tbody></table></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات</h2></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">القطاع</span><span class="m-item__n">قطاع المستشفيات</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">مدير المنتج</span><span class="m-item__n"><span class="m-td-nil">بلا تحديد</span></span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">السعر المنشور</span><span class="m-item__n">18,000 ر.س / سنة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">وحدة التسعير</span><span class="m-item__n">سنة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">حالة المساعد</span><span class="m-item__n">يبيعه المساعد · ينقصه ملف المعرفة</span></span></div><div class="m-item"><span class="m-item__b"><span class="m-item__s">المستهدف 2026</span><span class="m-item__n">34,000 ر.س · ربع واحد من أربعة</span></span></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn">أطلق حملة بهذا المنتج</button><button class="m-btn">&#8943;</button></div></section></div></section><section class="m-view__p" id="q1" role="tabpanel" hidden><div class="m-kb"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">الأقسام</h2><span class="m-chip m-chip--ok">80٪</span></div><div class="m-kb__l"><button class="m-kb__i" aria-current="true">وصف المنتج<b class="ok"><span class="m-n">80%</span></b></button><button class="m-kb__i">حالات الاستخدام<b class="mid"><span class="m-n">60%</span></b></button><button class="m-kb__i">الأسئلة الشائعة<b class="mid"><span class="m-n">45%</span></b></button><button class="m-kb__i">الأسعار والباقات<b class="low"><span class="m-n">10%</span></b></button><button class="m-kb__i">الاعتراضات<b class="low"><span class="m-n">0%</span></b></button><button class="m-kb__i">المنافسون<b class="low"><span class="m-n">0%</span></b></button><button class="m-kb__i">التكامل التقني<b class="low"><span class="m-n">20%</span></b></button><button class="m-kb__i">الامتثال<b class="low"><span class="m-n">0%</span></b></button></div></section><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">وصف المنتج</h2><span class="m-row"><span class="m-chip m-chip--warn">معرفة مدمجة</span><button class="m-btn">سجل التغييرات</button></span></div><div class="m-form"><div class="full"><textarea class="m-input" rows="12" placeholder="اكتب ما يعرفه المساعد عن هذا القسم…"></textarea></div><div class="m-field"><label class="m-label">الحالة</label><select class="m-select"><option>مدمجة</option><option>مسودة</option><option>بانتظار الاعتماد</option><option>معتمدة</option></select></div></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn m-btn--primary">حفظ كمسودة</button><button class="m-btn">إرسال للاعتماد</button><button class="m-btn">اعتماد</button></div></section></div></section><section class="m-view__p" id="q2" role="tabpanel" hidden><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">الباقات</h2><button class="m-btn m-btn--primary" data-open="dlgPkg">باقة جديدة</button></div><table class="m-table"><thead><tr><th>الباقة</th><th>السعر المرجعي</th><th>الوحدة</th><th>ما تشمله</th><th>الحالة</th><th></th></tr></thead><tbody><tr><td class="m-td-n">أساسية</td><td class="m-td-v"><span class="m-n">18,000</span> ر.س</td><td>سنويًا</td><td class="m-cap">حتى 500 موظف · دعم قياسي</td><td><span class="m-chip m-chip--ok">معتمدة</span></td><td><span class="m-row"><button class="m-btn" data-open="dlgPkg">تعديل</button><button class="m-btn">حذف</button></span></td></tr><tr><td class="m-td-n">متقدمة</td><td class="m-td-v"><span class="m-n">34,000</span> ر.س</td><td>سنويًا</td><td class="m-cap">غير محدود · دعم مخصص · تكامل</td><td><span class="m-chip m-chip--ok">معتمدة</span></td><td><span class="m-row"><button class="m-btn" data-open="dlgPkg">تعديل</button><button class="m-btn">حذف</button></span></td></tr></tbody></table></section></section><section class="m-view__p" id="q3" role="tabpanel" hidden><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">مستهدف 2026</h2><span class="m-chip m-chip--warn">يحتاج إكمالًا</span></div><div class="m-form"><div class="m-field"><label class="m-label">الربع 1 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div><div class="m-field"><label class="m-label">الربع 2 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div><div class="m-field"><label class="m-label">الربع 3 (ر.س)</label><input class="m-input" type="number" placeholder="" value="34000"></div><div class="m-field"><label class="m-label">الربع 4 (ر.س)</label><input class="m-input" type="number" placeholder="—" value=""></div></div><div class="m-form" style="margin-block-start:var(--m-3)"><div class="m-field"><label class="m-label">الإجمالي</label><input class="m-input" value="34000" disabled></div></div><div class="m-alert" style="margin-block-start:var(--m-4)"><span class="m-alert__t">ثلاثة أرباع بلا مستهدف</span><button class="m-btn">توزيع بالتساوي</button></div></section></section><section class="m-view__p" id="q4" role="tabpanel" hidden><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">البيانات والإدارة</h2></div><div class="m-form"><div class="m-field"><label class="m-label">اسم المنتج</label><input class="m-input" type="text" placeholder="" value="الإجازات المرضية"></div><div class="m-field"><label class="m-label">القطاع</label><select class="m-select"><option>قطاع المستشفيات</option><option>قطاع الصيدليات</option><option>قطاع الأعمال</option><option>بلا قطاع</option></select></div><div class="m-field"><label class="m-label">القسم</label><select class="m-select"><option>بلا قسم</option></select></div><div class="m-field"><label class="m-label">مدير المنتج</label><select class="m-select"><option>بلا تحديد</option></select></div><div class="m-field"><label class="m-label">السعر المنشور</label><input class="m-input" type="text" placeholder="" value="18,000 ر.س / سنة"></div><div class="m-field"><label class="m-label">وحدة التسعير</label><select class="m-select"><option>سنة</option><option>شهر</option><option>لكل فحص</option></select></div></div><div class="m-row" style="margin-block-start:var(--m-4)"><button class="m-btn m-btn--primary">حفظ</button><button class="m-btn">أرشفة المنتج</button></div></section></section></div>
      </div>
    </main>
  </div>
</div>
<dialog class="m-dlg" id="dlgPkg"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">باقة جديدة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">اسم الباقة</label><input class="m-input" type="text" placeholder="" value=""></div><div class="m-field"><label class="m-label m-req">السعر المرجعي (ر.س)</label><input class="m-input" type="number" placeholder="" value=""></div><div class="m-field"><label class="m-label">الوحدة</label><select class="m-select"><option>سنويًا</option><option>شهريًا</option><option>لكل فحص</option><option>مشروع</option></select></div><div class="m-field"><label class="m-label">الحالة</label><select class="m-select"><option>مسودة</option><option>معتمدة</option></select></div><div class="m-field full"><label class="m-label">ما تشمله</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">حفظ الباقة</button></div></form></dialog>
<script src="shell.js"></script>
<script>
var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');
 var p=document.getElementById(x.dataset.t);if(!p)return;
 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;p.removeAttribute('data-enter');}else{p.hidden=true;}});}
tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
</script>
</body>
</html>

exec
/bin/zsh -lc 'cat massar-ds/opps.html' in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — فرص البيع</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="opps" data-sub="opps">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a"><button class="m-btn">تصدير CSV</button><button class="m-btn m-btn--primary" data-open="dlgOpp">إضافة فرصة</button></div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb">فرص البيع</div>
          <h1 class="m-h1">فرص البيع</h1>
        </div>
        <div class="m-row"><div class="m-seg" role="group" aria-label="طريقة العرض"><button data-v="tbl" aria-pressed="true">جدول</button><button data-v="kan" aria-pressed="false">كانبان</button><button data-v="crd" aria-pressed="false">بطاقات</button></div><div class="m-seg" role="group" aria-label="تصفية"><button aria-pressed="true">الكل</button><button aria-pressed="false">مُسعَّرة</button><button aria-pressed="false">راكدة</button><button aria-pressed="false">بلا مسؤول</button></div></div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">
<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">بنود مفتوحة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">4,200 ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">لم تُسعَّر</div><div class="m-q__v"><span class="m-n">5</span></div><div class="m-q__s">من 6 بنود</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">متوقفة</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">—</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">راكدة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">35 يومًا</div></div></div><div class="m-alert" style="margin-block-end:var(--m-4)"><span class="m-alert__t">جهتان مهتمّتان عبر واتساب بلا فرصة</span><button class="m-btn">عرض</button></div><div class="m-view"><div class="m-view__p" id="tbl"><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>العميل</th><th>المنتج</th><th>المرحلة</th><th>القيمة</th><th>المصدر</th><th>في المرحلة</th><th>الإضافة</th><th></th></tr></thead><tbody><tr><td class="m-td-n">ابرهيم</td><td>تكامل الأنظمة (HIS/ERP)</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">ابرهيم</td><td>سجل التطعيمات الوطني</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>خدمات التطعيمات</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>تكامل الأنظمة (HIS/ERP)</td><td><span class="m-chip">تواصل أولي</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">العمدة</td><td>الإجازات المرضية</td><td><span class="m-chip">اكتشاف الحاجة</span></td><td><span class="m-td-nil">لم تُسعَّر</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-cap">12 أغسطس</td><td><button class="m-btn">فتح</button></td></tr><tr><td class="m-td-n">DL000</td><td>الإجازات المرضية</td><td><span class="m-chip m-chip--ac">عرض السعر</span></td><td><span class="m-td-v"><span class="m-n">4,200</span> ر.س</span></td><td>واتساب</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-cap">18 أغسطس</td><td><button class="m-btn">فتح</button></td></tr></tbody></table><div class="m-tools"><span class="m-cap"><span class="m-n">6</span> بنود · <span class="m-n">4,200</span> ر.س · <span class="m-n">5</span> لم تُسعَّر</span></div></section></div><div class="m-view__p" id="kan" hidden><section class="m-card m-card--pad0"><div class="m-board" style="padding:0 var(--m-3) var(--m-3)"><div class="m-col" style="--m-tone:#5B6472"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">تواصل أولي</span><span class="m-col__c"><span class="m-n">4</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col" style="--m-tone:#0072E9"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">اكتشاف الحاجة</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v">لم تُسعَّر</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#8B5CF6" tabindex="0" title="عرض المنتج"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض المنتج</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#7C3AED" tabindex="0" title="التقييم التقني"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التقييم التقني</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col" style="--m-tone:#2F6BFF"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">عرض السعر</span><span class="m-col__c"><span class="m-n">1</span></span></div><div class="m-col__v"><span class="m-n">4,200</span> ر.س</div><div class="m-col__b"><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></div><div class="m-col m-col--rail" style="--m-tone:#B45309" tabindex="0" title="التفاوض والاعتماد"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">التفاوض والاعتماد</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#15803D" tabindex="0" title="رابح"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">رابح</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div><div class="m-col m-col--rail" style="--m-tone:#BE123C" tabindex="0" title="خاسر"><div class="m-col__t"><span class="m-col__dot"></span><span class="m-col__n">خاسر</span><span class="m-col__c"><span class="m-n">0</span></span></div><div class="m-col__b"></div></div></div></section></div><div class="m-view__p" id="crd" hidden><section class="m-card m-card--pad0"><div class="m-kpis" style="padding:var(--m-3)"><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">ابرهيم</div><div class="m-deal__p">سجل التطعيمات الوطني</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">خدمات التطعيمات</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">تكامل الأنظمة (HIS/ERP)</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">تواصل أولي</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">العمدة</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v m-deal__v--nil">لم تُسعَّر</span><span class="m-chip">اكتشاف الحاجة</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">35</span> يومًا</span></div></article><article class="m-deal" tabindex="0"><div class="m-deal__n">DL000</div><div class="m-deal__p">الإجازات المرضية</div><div class="m-deal__f"><span class="m-deal__v"><span class="m-n">4,200</span> ر.س</span><span class="m-chip m-chip--ac">عرض السعر</span></div><div class="m-deal__f"><span class="m-cap">واتساب</span><span class="m-deal__age m-deal__age--old"><span class="m-n">29</span> يومًا</span></div></article></div></section></div></div>
      </div>
    </main>
  </div>
</div>
<dialog class="m-dlg" id="dlgOpp"><form method="dialog" class="m-dlg__p"><div class="m-dlg__h"><h2 class="m-dlg__t">إضافة فرصة</h2><button class="m-x" data-close aria-label="إغلاق">&times;</button></div><div class="m-dlg__b"><div class="m-form"><div class="m-field"><label class="m-label m-req">العميل</label><select class="m-select"><option>DL000</option><option>ابرهيم</option><option>العمدة</option><option>أبو حمزه</option><option>أبو نور</option><option>صيدلية الدواء</option><option>صيدلية الدواء (مثال)</option><option>صيدلية الدواء (مثال)</option></select></div><div class="m-field"><label class="m-label m-req">المنتج</label><select class="m-select"><option>الإجازات المرضية</option><option>التقارير الطبية</option><option>الشهادات الصحية</option><option>تكامل الأنظمة (HIS/ERP)</option><option>خدمات التطعيمات</option><option>سجل التطعيمات الوطني</option><option>صحة أعمال Plus</option><option>فحص الموظفين</option></select></div><div class="m-field"><label class="m-label m-req">المرحلة</label><select class="m-select"><option>تواصل أولي</option><option>اكتشاف الحاجة</option><option>عرض المنتج</option><option>التقييم التقني</option><option>عرض السعر</option><option>التفاوض والاعتماد</option></select></div><div class="m-field"><label class="m-label m-req">المصدر</label><select class="m-select"><option>حملة واتساب</option><option>مكالمة</option><option>زيارة</option><option>إحالة</option><option>طلب وارد</option></select></div><div class="m-field"><label class="m-label">الكمية</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">السعر للوحدة (ر.س)</label><input class="m-input" type="number" placeholder="لم تُسعَّر" value=""></div><div class="m-field"><label class="m-label">عدد السنوات</label><input class="m-input" type="number" placeholder="1" value=""></div><div class="m-field"><label class="m-label">الخصم %</label><input class="m-input" type="number" placeholder="0" value=""></div><div class="m-field"><label class="m-label">الموظف المسؤول</label><select class="m-select"><option>بلا مسؤول</option></select></div><div class="m-field"><label class="m-label">تاريخ الإغلاق المتوقع</label><input class="m-input" type="date" placeholder="" value=""></div><div class="m-field"><label class="m-label">الشريك</label><select class="m-select"><option>لا شريك</option></select></div><div class="m-field full"><label class="m-label">ملاحظة</label><textarea class="m-input" rows="3" placeholder=""></textarea></div></div></div><div class="m-dlg__f"><button class="m-btn" data-close>إلغاء</button><button class="m-btn m-btn--primary">إضافة الفرصة</button></div></form></dialog>
<script src="shell.js"></script>
<script>
var vs=document.querySelectorAll('[data-v]');
vs.forEach(function(b){b.addEventListener('click',function(){
 vs.forEach(function(o){o.setAttribute('aria-pressed','false');});
 b.setAttribute('aria-pressed','true');
 ['tbl','kan','crd'].forEach(function(id){var p=document.getElementById(id);if(!p)return;
  if(id===b.dataset.v){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
   p.removeAttribute('data-enter');}else{p.hidden=true;}});});});
</script>
</body>
</html>

exec
/bin/zsh -lc "cat massar-ds/reports.html
rg -n '"'^'"\\.(m-card|m-h1|m-lead__v|m-chip|m-empty|m-grid--3|m-arc__fill|m-chart__grow|m-fstep__b|m-col--rail|m-table th|m-view__p|m-side__logo)' massar-ds/massar.css" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>مسار — التقارير</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="massar.css">
</head>
<body data-nav="reports" data-sub="reports">
<div class="m-shell">
  <div class="m-main">
    <div class="m-bar">
      <div class="m-search">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        بحث
        <span class="m-kbd"><span>&#8984;</span><span>K</span></span>
      </div>
      <div class="m-head__a"><button class="m-btn">تحديث</button><button class="m-btn">تصدير</button></div>
    </div>
    <main class="m-page">
      <div class="m-head">
        <div>
          <div class="m-crumb">التقارير</div>
          <h1 class="m-h1">التقارير</h1>
        </div>
        <div class="m-row"><div class="m-seg" role="group" aria-label="تصفية"><button aria-pressed="true">آخر 30 يومًا</button><button aria-pressed="false">آخر 90 يومًا</button></div></div>
      </div>
      <div data-subs></div>
      <div style="margin-block-start:var(--m-4)">
<div class="m-qs" style="margin-block-end:var(--m-4)"><div class="m-q" style="cursor:default"><div class="m-q__k">المحقق</div><div class="m-q__v nil"><span class="m-n">0</span></div><div class="m-q__s">ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">المفتوح</div><div class="m-q__v"><span class="m-n">4,200</span></div><div class="m-q__s">ر.س · 6 بنود</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">المتوقع المرجّح</div><div class="m-q__v"><span class="m-n">3,360</span></div><div class="m-q__s">ر.س</div></div><div class="m-q" style="cursor:default"><div class="m-q__k">الراكدة</div><div class="m-q__v"><span class="m-n">6</span></div><div class="m-q__s">35 يومًا</div></div></div><div class="m-tabs" role="tablist"><button class="m-tab" role="tab" aria-selected="true" data-t="r0">نظرة تنفيذية</button><button class="m-tab" role="tab" aria-selected="false" data-t="r1">تقارير التعثّر</button><button class="m-tab" role="tab" aria-selected="false" data-t="r2">قبول المنتجات</button><button class="m-tab" role="tab" aria-selected="false" data-t="r3">مؤشرات الأداء</button></div><div class="m-view" style="margin-block-start:var(--m-4)"><section class="m-view__p" id="r0" role="tabpanel"><div class="m-grid m-grid--main"><section class="m-card"><div class="m-card__h"><h2 class="m-card__t">قمع المراحل</h2></div><div class="m-funnel"><div class="m-fstep"><span class="m-fstep__k">تواصل أولي</span><span class="m-fstep__b"><i style="--m-pct:100%"></i></span><span class="m-fstep__v"><span class="m-n">4</span></span></div><div class="m-fstep"><span class="m-fstep__k">اكتشاف الحاجة</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span> <span class="m-fstep__d">&#9662; <span class="m-n">75%</span></span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض المنتج</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">التقييم التقني</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">عرض السعر</span><span class="m-fstep__b"><i style="--m-pct:25%"></i></span><span class="m-fstep__v"><span class="m-n">1</span></span></div><div class="m-fstep"><span class="m-fstep__k">التفاوض والاعتماد</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div><div class="m-fstep"><span class="m-fstep__k">رابح</span><span class="m-fstep__b"><i style="--m-pct:0%"></i></span><span class="m-fstep__v"><span class="m-td-nil">لا شيء</span></span></div></div></section><section class="m-card m-card--pad0"><div class="m-tools"><h2 class="m-card__t">أين تتعثّر الصفقات</h2></div><table class="m-table"><thead><tr><th>السبب</th><th>البنود</th></tr></thead><tbody><tr><td class="m-td-n">بلا تسعير</td><td class="m-td-v"><span class="m-n">5</span></td></tr><tr><td class="m-td-n">راكدة 30 يومًا+</td><td class="m-td-v"><span class="m-n">6</span></td></tr><tr><td class="m-td-n">بلا موظف مسؤول</td><td class="m-td-v"><span class="m-n">6</span></td></tr><tr><td class="m-td-n">بلا مستهدف منتج</td><td class="m-td-v"><span class="m-n">7</span></td></tr></tbody></table></section></div></section><section class="m-view__p" id="r1" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المرحلة</th><th>الأقدم</th><th>الوسيط</th><th>البنود</th><th></th></tr></thead><tbody><tr><td class="m-td-n">تواصل أولي</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">4</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr><tr><td class="m-td-n">اكتشاف الحاجة</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">35</span> يومًا</td><td class="m-td-v"><span class="m-n">1</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr><tr><td class="m-td-n">عرض السعر</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-td-v"><span class="m-n">29</span> يومًا</td><td class="m-td-v"><span class="m-n">1</span></td><td><a class="m-btn" href="opps.html" style="text-decoration:none">افتح البنود</a></td></tr></tbody></table></section></section><section class="m-view__p" id="r2" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المنتج</th><th>جاهزية المساعد</th><th>السعر المنشور</th><th>الحالة</th></tr></thead><tbody><tr><td class="m-td-n">الإجازات المرضية</td><td class="m-td-v"><span class="m-n">80%</span></td><td><span class="m-td-v">18,000 ر.س / سنة</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">التقارير الطبية</td><td class="m-td-v"><span class="m-n">68%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">الشهادات الصحية</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">تكامل الأنظمة (HIS/ERP)</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">خدمات التطعيمات</td><td class="m-td-v"><span class="m-n">45%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">سجل التطعيمات الوطني</td><td class="m-td-v"><span class="m-n">90%</span></td><td><span class="m-td-v">20,000 ر.س / سنة</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr><tr><td class="m-td-n">صحة أعمال Plus</td><td class="m-td-v"><span class="m-n">0%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--bad">لا يبيعه المساعد</span></td></tr><tr><td class="m-td-n">فحص الموظفين</td><td class="m-td-v"><span class="m-n">73%</span></td><td><span class="m-td-nil">لا سعر منشور</span></td><td><span class="m-chip m-chip--ok">يبيعه المساعد</span></td></tr></tbody></table></section></section><section class="m-view__p" id="r3" role="tabpanel" hidden><section class="m-card m-card--pad0"><table class="m-table"><thead><tr><th>المؤشر</th><th>القيمة</th><th>المدى</th></tr></thead><tbody><tr><td class="m-td-n">نسبة الردّ</td><td class="m-td-v"><span class="m-n">19%</span></td><td class="m-cap">4 من 21</td></tr><tr><td class="m-td-n">نسبة الاهتمام</td><td class="m-td-v"><span class="m-n">9%</span></td><td class="m-cap">2 من 21</td></tr><tr><td class="m-td-n">نسبة التحويل إلى فرصة</td><td class="m-td-v"><span class="m-n">0%</span></td><td class="m-cap">0 من 2</td></tr><tr><td class="m-td-n">متوسط زمن الردّ</td><td class="m-td-v"><span class="m-n">3</span> ساعات</td><td class="m-cap">آخر 30 يومًا</td></tr><tr><td class="m-td-n">متوسط العمر في المرحلة</td><td class="m-td-v"><span class="m-n">34</span> يومًا</td><td class="m-cap">البنود المفتوحة</td></tr><tr><td class="m-td-n">نسبة الإنجاز</td><td class="m-td-v"><span class="m-n">0%</span></td><td class="m-cap">2026</td></tr></tbody></table></section></section></div>
      </div>
    </main>
  </div>
</div>

<script src="shell.js"></script>
<script>
var tabs=Array.prototype.slice.call(document.querySelectorAll('.m-tab[data-t]'));
function sel(t){tabs.forEach(function(x){var on=x===t;
 x.setAttribute('aria-selected',on?'true':'false');
 var p=document.getElementById(x.dataset.t);if(!p)return;
 if(on){p.hidden=false;p.setAttribute('data-enter','');void p.offsetWidth;
  p.removeAttribute('data-enter');}else{p.hidden=true;}});}
tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});
 t.addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0;
 if(!d)return;e.preventDefault();var x=tabs[(i+d+tabs.length)%tabs.length];x.focus();sel(x);});});
</script>
</body>
</html>
120:.m-side__logo{inline-size:28px;block-size:28px;border-radius:9px;flex:0 0 auto;
196:.m-h1{margin:0;font-size:var(--m-t-display);font-weight:800;color:var(--m-ink);
273:.m-chip{display:inline-flex;align-items:center;gap:4px;min-block-size:18px;
277:.m-chip--ok{background:color-mix(in srgb,var(--m-ok) 8%,transparent);color:var(--m-ok)}
278:.m-chip--warn{background:color-mix(in srgb,var(--m-warn) 8%,transparent);color:var(--m-warn)}
279:.m-chip--bad{background:color-mix(in srgb,var(--m-bad) 8%,transparent);color:var(--m-bad)}
280:.m-chip--ac{background:color-mix(in srgb,var(--m-ac) 8%,transparent);color:var(--m-ac-deep)}
282:.m-chip::before{content:"";inline-size:5px;block-size:5px;border-radius:50%;
284:.m-chip--plain::before{display:none}
316:.m-table th{block-size:40px;padding:0 10px;font-size:var(--m-t-body);font-weight:500;
337:.m-table th[aria-sort] .m-th-sort svg{opacity:1}
338:.m-table th[aria-sort="descending"] .m-th-sort svg{transform:rotate(180deg)}
340:.m-table th.m-sel{inline-size:26px;padding:0 0 0 10px}
349:.m-table th.num{text-align:end}
391:.m-card{background:var(--m-paper);border-radius:var(--m-r-card);box-shadow:var(--m-soft);
393:.m-card--band{border-radius:var(--m-r-band);padding:var(--m-6)}
394:.m-card--pad0{padding:0}
395:.m-card__h{display:flex;align-items:flex-start;justify-content:space-between;
397:.m-card__t{margin:0;font-size:var(--m-t-h);font-weight:700;color:var(--m-ink);
399:.m-card__k{font-size:var(--m-t-body);color:var(--m-mut);font-weight:500}
403:.m-lead__v{font-size:var(--m-t-hero);font-weight:800;color:var(--m-ink);
405:.m-lead__v small{font-size:var(--m-t-h);font-weight:600;color:var(--m-mut);
439:.m-chart__grow{transform-box:fill-box;transform-origin:bottom;
480:.m-col--rail{inline-size:44px;cursor:pointer;align-self:stretch}
481:.m-col--rail .m-col__b,.m-col--rail .m-col__v{display:none}
482:.m-col--rail .m-col__t{flex-direction:column;gap:var(--m-3);margin:0}
483:.m-col--rail .m-col__n{writing-mode:vertical-rl;transform:rotate(180deg);
503:.m-empty-col{padding:var(--m-4) var(--m-3);text-align:center;border-radius:var(--m-r-ctl);
540:.m-chip{display:inline-flex;align-items:center;gap:6px;font-size:var(--m-t-micro);
543:.m-chip--ok{background:var(--m-ok-dim);color:var(--m-ok)}
544:.m-chip--warn{background:var(--m-warn-dim);color:var(--m-warn)}
545:.m-chip--bad{background:var(--m-bad-dim);color:var(--m-bad)}
546:.m-chip--ac{background:var(--m-ac-dim);color:var(--m-ac-deep)}
548:.m-chip::before{content:"";inline-size:5px;block-size:5px;border-radius:50%;background:currentColor}
549:.m-chip--plain::before{display:none}
577:.m-empty{padding:var(--m-6) var(--m-5);text-align:center}
578:.m-empty__t{font-size:var(--m-t-body);font-weight:700;color:var(--m-ink)}
579:.m-empty__d{font-size:var(--m-t-cap);color:var(--m-mut);margin-block-start:var(--m-2);
581:.m-empty__a{margin-block-start:var(--m-4)}
587:.m-grid--3{grid-template-columns:repeat(3,minmax(0,1fr))}
615:.m-arc__fill{fill:none;stroke:var(--m-ac);stroke-width:14;stroke-linecap:round;
618:.m-arc__fill--warn{stroke:var(--m-warn)}
619:.m-arc__fill--bad{stroke:var(--m-bad)}
620:.m-arc__fill--ok{stroke:var(--m-ok)}
646:.m-fstep__b{block-size:30px;border-radius:var(--m-r-ctl);background:var(--m-sunk);
648:.m-fstep__b i{position:absolute;inset-block:0;inset-inline-start:0;inline-size:var(--m-pct,0%);
699:.m-view__p{transition:opacity var(--m-swap) var(--m-ease),
702:.m-view__p[hidden]{display:none!important}
703:.m-view__p[data-enter]{opacity:0;transform:translateY(6px);filter:blur(3px)}
756:.m-col--rail{align-self:stretch;min-block-size:150px}

codex
The source confirms several concrete errors: Home spreads the Q3-only target across all twelve months, labels all six stale lines “on track,” and says five of six products lack targets when the real count is seven of eight. Reports also invents a weighted forecast and treats stage counts as conversion losses.

I’m taking Home down to three parts: booked revenue with the target limitation beside it, the six opportunity lines, and a compact action list. The indicators will live beside the decisions they support.
exec
/bin/zsh -lc "python3 -c 'colors=[\"#17201F\",\"#46504D\",\"#646D69\",\"#245BD6\",\"#8A4B08\",\"#B42318\"]
def lum(h):
 v=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
 return sum(x*w for x,w in zip(v,[.2126,.7152,.0722]))
for c in colors: print(c,round(1.05/(lum(c)+.05),2))
print(\"Current prorated target:\",round(34000/12*(8+16/30)))'" in /Users/abdulaziz/Projects/Massar
 succeeded in 0ms:
#17201F 16.63
#46504D 8.35
#646D69 5.34
#245BD6 5.93
#8A4B08 6.79
#B42318 6.57
Current prorated target: 24178

codex
**Massar should feel like a founder’s revenue ledger: one unmistakable number, an honest statement of what it means, and the work that can change it.**

The current page spends its attention budget drawing the database. It needs to spend that budget interpreting it.

**1. The diagnosis**

The most serious problems are factual. Visual polish currently makes them more convincing.

| Severity | Location | Before | Required change |
|---|---|---|---|
| HIGH | [home.html:97](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:97), `MONTHLY`, `sum()`, `paintQuarters()` | `TARGET / 12` distributes a **Q3-only, single-product target** across the year. Initial rendering changes the displayed requirement to **24,178**, and quarters receive **8,500** each. | Delete this allocation. Show **34,000 ر.س · الإجازات المرضية · الربع الثالث**. Other periods have **no target recorded**, not zero targets. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-matrix`, `.m-key` | All six lines are labelled **على المسار**, while all have been stationary for 29–35 days. | Replace the entire widget with **ستة بنود بلا حركة منذ 29–35 يومًا** beside the opportunity list. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-funnel` | Four records in one stage and one in another become a **75% loss**. These are current stage populations, not a tracked conversion cohort. | Delete the leakage claim and percentage. Preserve stage counts as counts. |
| HIGH | [reports.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/reports.html:33) | **3,360** “weighted expected” revenue has no supported probability model in the brief. “Six lines aged 30+ days” includes the 29-day line. | Remove the forecast. Show the actual **29–35-day range**; only five meet a 30-day threshold. |
| HIGH | [shell.js:11](/Users/abdulaziz/Projects/Massar/massar-ds/shell.js:11), Home decisions, Products summary | Navigation says six products; Home says five of six lack targets; reality is eight products, seven without targets. Products says one lacks published pricing, while six rows say otherwise. | Compute summaries from the same records as their tables. No separately maintained counts. |

The visual system then compounds those errors:

| Severity | Location | Before | After and why |
|---|---|---|---|
| MEDIUM | [massar.css:391](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:391), `.m-card`, `.m-grid--3` | Every secondary story gets a white surface, **24px padding**, **16px radius**, the same shadow and a **19px heading**. Equal treatment makes everything equally urgent. | Two substantial surfaces on Home: revenue and opportunities. Decisions and supporting evidence use plain rows. |
| MEDIUM | [massar.css:60](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:60), type tokens | Eight sizes, including **11px** and **12.5px**, push material qualifications into miniature grey text. | Five principal levels: **72, 28, 20, 15, 13px**. Target coverage must be readable body text. |
| MEDIUM | `.m-h1`, `.m-card__t`, `.m-lead__v` | Arabic titles inherit **−1px / −.3px tracking**; the monetary figure and currency share display treatment. | Arabic tracking **0**. Tighten Western display numerals only. Give Cairo room vertically. |
| MEDIUM | [massar.css:273](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:273) and [massar.css:540](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:540), `.m-chip` | The same component is defined twice: first **12.5px, 6px radius, 1px 7px padding**, later **11px, pill radius, 3px 9px**. | One definition: **13/22px**, pill, used only for actual statuses. The cascade should not make design decisions. |
| MEDIUM | `.m-chart`, `.m-arc`, `.m-heat`, `.m-fstep` | A **900×280** chart, **200px** gauge, **34px** heat cells and **30px** funnel bars illustrate mostly zeros and unsupported subdivisions. | Remove them from Home. Their area exceeds their information. |
| MEDIUM | `.m-col`, `.m-col--rail`, `.m-deal` | **252px columns**, **44px rotated empty rails**, cards inside columns inside a card. Six records require horizontal exploration. | One six-row table. Empty stages remain accessible in the pipeline workspace. |
| MEDIUM | `.m-side__logo`, `.m-insight`, `.m-fstep__b i`, `.m-meter i` | Blue–violet gradients assign decorative excitement to unrelated things. | One blue accent. Status colours carry meaning and readable labels. |
| MEDIUM | `.m-empty`, `.m-q__v.nil`, `.m-stat--mut` | Empty content is centred; zeros become faint. | Align to inline-start. **Booked zero stays black.** Absence is the principal finding. |
| MEDIUM | [products.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/products.html:33) | An implementation ZIP filename interrupts product management; another row literally says **hello**. | Remove both. Product copy describes the business record and its next action. |
| MEDIUM | [product.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/product.html:33) | Global product navigation sits above five record tabs; summary tiles give campaign mentions equal weight to open revenue. | Record page gets a breadcrumb and one record-level tab strip. Overview leads with this product’s revenue, scoped target and two opportunity lines. |
| MEDIUM | Motion rules and `shell.js` | **700ms** chart growth, **900ms** gauges, multiple easing curves, press scales **.98/.985**, and a dialog that closes immediately despite comments promising an exit. | Static charts; one curve; **180ms enter / 120ms exit / 100ms press**, **.97** press scale. Implement the dialog exit before calling `close()`. |

There is also interaction theatre: `.m-search` is a `div` advertising `⌘K`; several “فتح” buttons have no handler; `cursor:grab` suggests dragging that the supplied scripts do not implement. These controls should either work or disappear.

**2. The fixed Home**

Use the brief’s snapshot date: **16 September 2026**.

The page has three parts, in this reading order.

**A. Revenue and its limits**

A compact page header:

> **الأداء التجاري**  
> السنة المالية 2026 · حتى 16 سبتمبر

No breadcrumb saying “الرئيسية” directly above it. No five-way date switch. Historical ranges belong in Reports.

One full-width revenue surface, internally divided into a dominant right column and a quieter left column:

| Right: dominant | Left: supporting |
|---|---|
| الإيراد المحقق | المستهدف المسجّل |
| **0 ر.س** | **34,000 ر.س** |
| لا صفقات رابحة حتى 16 سبتمبر | الإجازات المرضية · الربع الثالث فقط |
| **● لا توجد إيرادات محققة حتى الآن** | **سبعة منتجات بلا مستهدف. لا يمكن تقييم تحقيق مستهدف الشركة.** |
| Primary action: **مراجعة العرض المسعّر** | Secondary link: **استكمال المستهدفات** |
|  | قيمة البنود المفتوحة المسعّرة: **4,200 ر.س** |
|  | بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير |

That is the five-second answer. No invented probability, no company attainment percentage, no red downward arrow pretending a target gap is a period-over-period delta.

The reference’s large number and pill remain. The pill communicates a supported status.

**B. The work that changes the number**

Below the hero, use an asymmetric two-column layout.

The larger **right-hand column** contains the six opportunity lines. Put the priced quotation first because it is the only known money currently available to pursue.

Heading:

> **فرص البيع المفتوحة**  
> ستة بنود بلا حركة منذ 29–35 يومًا · آخر حركة في 18 أغسطس

Columns, in RTL order:

| العميل / المنتج | المرحلة | القيمة | بلا حركة |
|---|---|---:|---:|
| DL000 / الإجازات المرضية | عرض السعر | 4,200 ر.س | 29 يومًا |
| العمدة / الإجازات المرضية | اكتشاف الحاجة | لم يُسعّر | 35 يومًا |
| ابرهيم / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |
| ابرهيم / سجل التطعيمات الوطني | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / خدمات التطعيمات | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |

Use one explicit record link per row. No repeated pill-shaped “فتح” buttons.

The smaller **left-hand column** is an unboxed action list titled **ما يعطّل البيع**:

1. **خمسة بنود بلا تسعير** — action: **استكمال التسعير**.
2. **16 حسابًا بلا مسؤول وبلا جهة اتصال مرتبطة** — action: **تعيين المسؤولين وربط جهات الاتصال**.
3. **جهتان مهتمتان دون فرصة من الحملة 38** — action: **مراجعة المهتمين**.

Each action opens the relevant filtered records. Do not send the founder to an unfiltered landing page.

Target incompleteness is already beside the target. Staleness is already beside the pipeline. Do not repeat either as another warning card.

**C. Supporting evidence**

One unboxed disclosure titled **تفاصيل المؤشرات**. Closed initially. Its summary reads:

> اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات

Inside, use four plain rows, not four cards:

- **Accounts:** 16 approved accounts; none has an owner or linked contact; seven have a sector and seven have a city. The 21 contacts are a separate entity count, not evidence of account linkage.
- **Campaign 38:** sent 21 → delivered 19 → seen 12 → replied 4 → interested 2 → opportunities 0. Render the sequence from right to left with labels and counts.
- **Activity totals:** 21 contacts, 359 messages, 1,233 events. Label these as recorded totals; do not imply they are today’s activity or revenue.
- **Knowledge:** eight weighted sections; objections, competitors and compliance are each 0%. Link to the named sections. Do not manufacture an overall readiness score from undocumented weights.

**This is the Home/indicators merger:** relevant indicators explain the revenue and actions; the rest remain available in one subordinate disclosure. Remove “مؤشرات الاستخدام” as a separate navigation destination and redirect its existing route to this disclosure.

Keep all eight products and their supplied readiness values in Products. Retain both published annual prices, the four inferred-sector labels, all three sectors plus “بلا قطاع”, and the explicit “لا يبيعه المساعد” status for صحة أعمال Plus. These facts do not need eight widgets on Home.

**3. Pasteable CSS**

Paste this **after the existing stylesheet** while replacing Home’s body content with the structure above. It overrides shared foundations and supplies the new Home layout. CSS cannot repair the target calculation or remove the old sections; those changes are mandatory.

Use this structure:

```html
<main class="m-page m-home">
  <header class="m-home__head">
    <h1 class="m-h1">الأداء التجاري</h1>
    <p class="m-meta">
      السنة المالية <bdi class="m-n">2026</bdi>
      · حتى <bdi class="m-n">16</bdi> سبتمبر
    </p>
  </header>

  <section class="m-card m-card--revenue"
           aria-labelledby="revenue-title">
    <div class="m-revenue__main">
      <h2 class="m-label" id="revenue-title">الإيراد المحقق</h2>
      <p class="m-revenue__value">
        <bdi class="m-n">0</bdi><span>ر.س</span>
      </p>
      <p class="m-body">لا صفقات رابحة حتى 16 سبتمبر</p>
      <p class="m-status m-status--warn">
        لا توجد إيرادات محققة حتى الآن
      </p>
      <div class="m-actions">
        <a class="m-btn m-btn--primary" href="#priced-line">
          مراجعة العرض المسعّر
        </a>
      </div>
    </div>

    <div class="m-revenue__context">
      <dl class="m-facts">
        <div>
          <dt>المستهدف المسجّل</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">34,000</bdi> ر.س
          </dd>
          <dd>الإجازات المرضية · الربع الثالث فقط</dd>
        </div>
        <div>
          <dt>قيمة البنود المفتوحة المسعّرة</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">4,200</bdi> ر.س
          </dd>
          <dd>بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير</dd>
        </div>
      </dl>
      <p class="m-revenue__qualification">
        سبعة منتجات بلا مستهدف.
        لا يمكن تقييم تحقيق مستهدف الشركة.
      </p>
      <a class="m-link" href="perf.html">استكمال المستهدفات</a>
    </div>
  </section>

  <div class="m-home__work">
    <section class="m-card m-card--ledger"
             aria-labelledby="pipeline-title">
      <header class="m-section-head">
        <h2 class="m-h2" id="pipeline-title">فرص البيع المفتوحة</h2>
        <p class="m-meta">
          ستة بنود بلا حركة منذ <bdi class="m-n">29–35</bdi> يومًا
          · آخر حركة في <bdi class="m-n">18</bdi> أغسطس
        </p>
      </header>
      <!-- .m-tablewrap > table.m-table.m-ledger
           Use the six rows above.
           Give the priced row id="priced-line" and tabindex="-1". -->
    </section>

    <aside class="m-home__decisions" aria-labelledby="decisions-title">
      <h2 class="m-h2" id="decisions-title">ما يعطّل البيع</h2>
      <!-- Three .m-decision blocks:
           h3.m-decision__title, p.m-meta, a.m-link -->
    </aside>
  </div>

  <details class="m-evidence" id="indicators">
    <summary>
      <span class="m-h2">تفاصيل المؤشرات</span>
      <span class="m-meta">
        اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات
      </span>
    </summary>
    <!-- Four .m-evidence__row blocks with the exact facts above. -->
  </details>
</main>
```

```css
/* MASSAR — revised foundations and revenue-first Home */
:root {
  /* Near-white ground; blue reserved for action and selection. */
  --m-page: #F6F7F5;
  --m-paper: #FFFFFF;
  --m-sunk: #EEF1EE;
  --m-line: #E3E7E3;
  --m-line-2: #CDD4CE;
  --m-dot: #D9DFDA;

  --m-ink: #17201F;
  --m-ink-2: #46504D;
  --m-mut: #646D69;
  --m-faint: #646D69;

  --m-ac: #245BD6;
  --m-ac-deep: #1947AF;
  --m-ac-dim: #EEF3FF;
  --m-ac-line: #BCCDF7;

  --m-ok: #17603D;
  --m-ok-dim: #EDF6F0;
  --m-ok-line: #BEDBC8;
  --m-warn: #8A4B08;
  --m-warn-dim: #FFF4E5;
  --m-warn-line: #E8CFAB;
  --m-bad: #B42318;
  --m-bad-dim: #FEF0ED;
  --m-bad-line: #F1C5BE;
  --m-idle: #646D69;
  --m-idle-dim: #EEF1EE;
  --m-idle-line: #CDD4CE;

  /* Compatibility for retained views: no violet palette. */
  --m-vi: var(--m-ac);
  --m-vi-dim: var(--m-ac-dim);

  /* Five principal type levels. Supporting figures use 28px. */
  --m-t-micro: 13px;
  --m-t-cap: 13px;
  --m-t-body: 15px;
  --m-t-sub: 15px;
  --m-t-h: 20px;
  --m-t-fig: 28px;
  --m-t-display: 28px;
  --m-t-hero: 72px;

  --m-leading-meta: 22px;
  --m-leading-body: 26px;
  --m-leading-section: 32px;
  --m-leading-title: 44px;
  --m-leading-figure: 40px;
  --m-leading-hero: 80px;

  --m-tracking-text: 0;
  --m-tracking-figure: -0.02em;
  --m-tracking-hero: -0.035em;

  /* 4px rhythm; 24 between groups, 32 between major regions. */
  --m-1: 4px;
  --m-2: 8px;
  --m-3: 12px;
  --m-4: 16px;
  --m-5: 24px;
  --m-6: 32px;
  --m-7: 48px;

  --m-r-chip: 999px;
  --m-r-ctl: 10px;
  --m-r-card: 16px;
  --m-r-band: 20px;

  --m-hair: 0 0 0 1px var(--m-line);
  --m-low: 0 1px 2px rgb(0 0 0 / 3%);
  --m-soft: 0 2px 8px rgb(0 0 0 / 3%);
  --m-lift: 0 8px 24px rgb(0 0 0 / 10%);
  --m-focus: 0 0 0 3px var(--m-ac-line);

  --m-ease: cubic-bezier(.16, 1, .3, 1);
  --m-move: var(--m-ease);
  --m-press: 100ms;
  --m-swap: 120ms;
  --m-in: 180ms;
  --m-out: 120ms;
}

body {
  font-family: Cairo, system-ui, sans-serif;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
  color: var(--m-ink-2);
  background: var(--m-page);
  direction: rtl;
  font-variant-numeric: lining-nums tabular-nums;
}

.m-n {
  display: inline-block;
  direction: ltr;
  unicode-bidi: isolate;
  font-variant-numeric: lining-nums tabular-nums;
  font-feature-settings: "lnum" 1, "tnum" 1;
}

.m-h1,
.m-greet__t {
  margin-block: 0;
  font-size: var(--m-t-display);
  line-height: var(--m-leading-title);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-h2,
.m-card__t {
  margin-block: 0;
  font-size: var(--m-t-h);
  line-height: var(--m-leading-section);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-body,
.m-label {
  margin-block: 0;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
}

.m-label { font-weight: 600; }

.m-meta,
.m-cap,
.m-stat__s,
.m-item__s,
.m-q__s,
.m-hint {
  margin-block: 0;
  font-size: var(--m-t-cap);
  line-height: var(--m-leading-meta);
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-stat__v,
.m-q__v {
  font-size: var(--m-t-fig);
  line-height: var(--m-leading-figure);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-stat__v .m-n,
.m-q__v .m-n {
  letter-spacing: var(--m-tracking-figure);
}

/* A known zero is ordinary data, not disabled content. */
.m-q__v.nil,
.m-stat--mut .m-stat__v {
  color: var(--m-ink);
}

/* Shared shell. */
.m-shell { min-block-size: 100dvh; }

.m-side {
  inline-size: 224px;
  block-size: 100dvh;
  border-inline-start: 0;
  border-inline-end: 1px solid var(--m-line);
  transition-duration: var(--m-in);
}

.m-side[data-collapsed] {
  inline-size: 68px;
  transition-duration: var(--m-out);
}

.m-side__logo { background: var(--m-ac); }

.m-side__grp { letter-spacing: 0; }

.m-nav {
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  border-radius: var(--m-r-ctl);
}

.m-side__w,
.m-nav span {
  transition: opacity var(--m-in) var(--m-ease);
  transform: none;
}

.m-side[data-collapsed] .m-side__w,
.m-side[data-collapsed] .m-nav span {
  transform: none;
  transition: opacity var(--m-out) var(--m-ease);
}

/* Use accessible link names; remove the clipped pseudo-flyout. */
.m-nav::after { content: none; }

.m-page {
  inline-size: 100%;
  max-inline-size: 1264px;
  margin-inline: auto;
  padding-inline: var(--m-6);
  padding-block: var(--m-6) var(--m-7);
}

.m-bar {
  position: static;
  padding-inline: var(--m-6);
  padding-block: var(--m-3);
  background: transparent;
  border-block-end: 0;
}

/* Home has its own useful header; delete its old toolbar markup. */
body[data-nav="home"] .m-bar { display: none; }

/* Shared surfaces: quiet structure, no hover elevation. */
.m-card {
  min-inline-size: 0;
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  background: var(--m-paper);
  border: 1px solid var(--m-line);
  border-radius: var(--m-r-card);
  box-shadow: none;
}

.m-card--pad0,
.m-card--ledger {
  padding-inline: 0;
  padding-block: 0;
}

.m-card--revenue {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: var(--m-6);
  padding-inline: var(--m-6);
  padding-block: var(--m-6);
  border-radius: var(--m-r-band);
  box-shadow: var(--m-soft);
}

/* Home composition. DOM order is also the mobile reading order. */
.m-home {
  display: grid;
  gap: var(--m-6);
}

.m-home__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--m-2) var(--m-5);
}

.m-revenue__main { min-inline-size: 0; }

.m-revenue__value {
  display: flex;
  align-items: baseline;
  gap: var(--m-3);
  margin-block: var(--m-2);
  color: var(--m-ink);
}

.m-revenue__value > .m-n {
  font-size: var(--m-t-hero);
  line-height: var(--m-leading-hero);
  font-weight: 700;
  letter-spacing: var(--m-tracking-hero);
}

.m-revenue__value > :not(.m-n) {
  font-size: 20px;
  line-height: 32px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-revenue__context {
  min-inline-size: 0;
  padding-inline-start: var(--m-6);
  border-inline-start: 1px solid var(--m-line);
}

.m-facts {
  display: grid;
  gap: var(--m-5);
  margin-block: 0;
}

.m-facts dt {
  font-size: 13px;
  line-height: 22px;
  color: var(--m-mut);
}

.m-facts dd {
  margin-inline: 0;
  margin-block: var(--m-1) 0;
  font-size: 13px;
  line-height: 22px;
}

.m-facts .m-facts__value {
  font-size: 20px;
  line-height: 32px;
  font-weight: 600;
  color: var(--m-ink);
}

.m-revenue__qualification {
  margin-block: var(--m-5) var(--m-2);
  font-size: 15px;
  line-height: 26px;
  color: var(--m-ink);
}

.m-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--m-2);
  margin-block-start: var(--m-5);
}

.m-home__work {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: var(--m-6);
  align-items: start;
}

.m-section-head {
  display: grid;
  gap: var(--m-1);
  padding-inline: var(--m-5);
  padding-block: var(--m-5) var(--m-4);
}

.m-home__decisions {
  min-inline-size: 0;
  padding-block-start: var(--m-2);
}

.m-decision {
  display: grid;
  gap: var(--m-2);
  padding-block: var(--m-4);
  border-block-end: 1px solid var(--m-line);
}

.m-decision:last-child { border-block-end: 0; }

.m-decision__title {
  margin-block: 0;
  font-size: 15px;
  line-height: 26px;
  font-weight: 600;
  color: var(--m-ink);
}

/* One readable table, including when records are sparse. */
.m-tablewrap {
  overflow: auto;
  border-radius: 0 0 var(--m-r-card) var(--m-r-card);
}

.m-table th {
  block-size: 44px;
  padding-inline: var(--m-4);
  padding-block: var(--m-2);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  text-align: start;
  color: var(--m-mut);
  background: var(--m-paper);
}

.m-table td {
  padding-inline: var(--m-4);
  padding-block: 10px;
  font-size: 15px;
  line-height: 24px;
  font-weight: 400;
  color: var(--m-ink-2);
}

.m-ledger { min-inline-size: 560px; }

.m-ledger .m-item__s {
  margin-block-start: 2px;
  font-size: 13px;
  line-height: 20px;
}

.m-table td.m-td-v,
.m-table th.num {
  text-align: end;
  color: var(--m-ink);
}

.m-table td.m-td-n {
  font-weight: 600;
  color: var(--m-ink);
}

.m-ledger__unpriced {
  color: var(--m-warn);
  font-size: 13px;
  line-height: 22px;
  white-space: nowrap;
}

#priced-line { scroll-margin-block-start: var(--m-5); }

#priced-line:target { background: var(--m-ac-dim); }

/* Status: readable words plus a dot; never colour alone. */
.m-chip,
.m-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-inline: 10px;
  padding-block: 3px;
  min-block-size: 28px;
  border-radius: var(--m-r-chip);
  background: var(--m-idle-dim);
  color: var(--m-idle);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  letter-spacing: 0;
  white-space: normal;
}

.m-status { margin-block: var(--m-4) 0; }

.m-chip::before,
.m-status::before {
  content: "";
  inline-size: 6px;
  block-size: 6px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: currentColor;
}

.m-status--warn,
.m-chip--warn {
  background: var(--m-warn-dim);
  color: var(--m-warn);
}

.m-chip--bad {
  background: var(--m-bad-dim);
  color: var(--m-bad);
}

.m-chip--ok {
  background: var(--m-ok-dim);
  color: var(--m-ok);
}

.m-chip--ac {
  background: var(--m-ac-dim);
  color: var(--m-ac-deep);
}

/* Controls: one geometry, real hit areas. */
.m-btn {
  min-block-size: 44px;
  justify-content: center;
  padding-inline: var(--m-4);
  padding-block: 9px;
  border: 1px solid var(--m-line-2);
  border-radius: var(--m-r-chip);
  box-shadow: none;
  font-size: 14px;
  line-height: 24px;
  text-decoration: none;
  transition:
    background-color var(--m-out) var(--m-ease),
    transform var(--m-press) var(--m-ease);
}

.m-btn--primary {
  border-color: var(--m-ac);
  background: var(--m-ac);
  color: #FFFFFF;
  box-shadow: none;
}

.m-btn--quiet {
  border-color: transparent;
  background: transparent;
  color: var(--m-ac-deep);
}

.m-btn--icon {
  inline-size: 44px;
  block-size: 44px;
}

.m-link {
  display: inline-flex;
  align-items: center;
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  color: var(--m-ac-deep);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.m-input,
.m-select {
  min-block-size: 44px;
  font-size: 15px;
  line-height: 24px;
  transition: box-shadow var(--m-out) var(--m-ease);
}

/* Restore native select indicator; delete physical background-position. */
.m-select {
  appearance: auto;
  background-image: none;
  padding-inline: var(--m-3);
}

:where(a, button, input, select, textarea, summary):focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

/* Specificity overrides old focus rules. */
.m-btn:focus-visible,
.m-nav:focus-visible,
.m-tab:focus-visible,
.m-input:focus-visible,
.m-select:focus-visible,
.m-range input:focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

.m-btn:not(:disabled):active,
.m-nav:active,
.m-side__t:active,
.m-seg button:active,
.m-x:active {
  transform: scale(.97);
}

.m-btn:disabled:active { transform: none; }

@media (hover: hover) and (pointer: fine) {
  .m-btn:not(:disabled):hover { background: var(--m-page); }
  .m-btn--primary:not(:disabled):hover {
    background: var(--m-ac-deep);
  }
  .m-table tbody tr:hover { background: #F8FAF8; }
  .m-link:hover { color: var(--m-ac); }
}

/* Supporting evidence is a document section, not another dashboard. */
.m-evidence {
  border-block-start: 1px solid var(--m-line-2);
}

.m-evidence > summary {
  padding-block: var(--m-4);
  cursor: pointer;
  min-block-size: 44px;
}

.m-evidence > summary .m-meta {
  display: block;
  margin-block-start: var(--m-1);
}

.m-evidence__row {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: var(--m-4);
  padding-block: var(--m-4);
  border-block-start: 1px solid var(--m-line);
}

.m-evidence__row > * { margin-block: 0; }

/* A genuine empty record list: ordinary editorial content. */
.m-empty {
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  text-align: start;
}

.m-empty__t {
  font-size: 15px;
  line-height: 26px;
}

.m-empty__d {
  max-inline-size: 60ch;
  margin-inline: 0;
  font-size: 13px;
  line-height: 22px;
}

/* No drawing animations or blurred text swaps. */
.m-chart__grow,
.m-arc__fill,
.m-fstep__b i {
  animation: none;
}

.m-fstep__b i,
.m-meter i {
  background: var(--m-ac);
}

.m-view__p,
.m-view__p[data-enter] {
  opacity: 1;
  transform: none;
  filter: none;
  transition: none;
}

.m-input,
.m-select,
.m-tip2,
.m-table tbody tr,
.m-th-sort svg,
.m-cb {
  transition-timing-function: var(--m-ease);
}

.m-dlg__p {
  animation: m-dialog-enter var(--m-in) var(--m-ease);
}

dialog.m-dlg::backdrop {
  animation: m-fade var(--m-in) var(--m-ease);
}

dialog.m-dlg[data-closing] .m-dlg__p {
  animation: m-dialog-exit var(--m-out) var(--m-ease) both;
}

dialog.m-dlg[data-closing]::backdrop {
  animation: m-fade var(--m-out) var(--m-ease) reverse both;
}

@keyframes m-dialog-enter {
  from { opacity: 0; transform: scale(.97); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes m-dialog-exit {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(.97); }
}

@media (max-width: 1200px) {
  .m-home__work { grid-template-columns: minmax(0, 1fr); }
}

/* Reachable mobile navigation without the existing unopened drawer. */
@media (max-width: 900px) {
  .m-shell { display: block; }

  .m-side,
  .m-side[data-collapsed] {
    position: static;
    inline-size: 100%;
    block-size: auto;
    transform: none;
    overflow: visible;
    border-inline-end: 0;
    border-block-end: 1px solid var(--m-line);
    transition: none;
  }

  .m-side__b,
  .m-side__f { display: none; }

  .m-side__nav {
    display: flex;
    overflow: auto;
    padding-inline: var(--m-4);
    padding-block: var(--m-2);
  }

  .m-nav { flex: 0 0 auto; }

  .m-side[data-collapsed] .m-nav span,
  .m-side[data-collapsed] .m-nav b {
    opacity: 1;
    transform: none;
  }

  .m-page,
  .m-bar { padding-inline: var(--m-4); }
}

@media (max-width: 700px) {
  :root {
    --m-t-hero: 56px;
    --m-leading-hero: 64px;
  }

  .m-home { gap: var(--m-5); }

  .m-card--revenue {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-5);
    padding-inline: var(--m-5);
    padding-block: var(--m-5);
  }

  .m-revenue__context {
    padding-inline-start: 0;
    padding-block-start: var(--m-5);
    border-inline-start: 0;
    border-block-start: 1px solid var(--m-line);
  }

  .m-evidence__row {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-2);
  }

  .m-input,
  .m-select { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }

  .m-btn:active,
  .m-nav:active,
  .m-side__t:active,
  .m-seg button:active,
  .m-x:active {
    transform: none;
  }
}
```

For dialog dismissal, `shell.js` must apply `data-closing`, wait for the panel’s exit, then call `close()`. Route the close button, Escape and backdrop through that function. Reduced motion closes immediately. CSS alone cannot delay the existing `close()` calls.

Western numerals also require formatting at the data boundary; `.m-n` does not convert digits:

```js
const formatNumber = new Intl.NumberFormat("ar-SA-u-nu-latn");
```

Counted nouns need authored plural forms. Use **لا بنود، بند واحد، بندان، ثلاثة بنود، 11 بندًا** according to the count and grammatical context. Do not construct Arabic prose with `${n} + noun`.

**4. The near-empty state is the design**

Keep these distinctions explicit:

| Data condition | Display |
|---|---|
| Known booked revenue is zero | **0 ر.س**, full-strength ink |
| An opportunity exists without pricing | **لم يُسعّر** |
| A target has not been configured | **لم يُحدّد** |
| No opportunity lines exist | **لا بنود مفتوحة** |
| A future period has not happened | **لم يبدأ بعد** |
| A value cannot be calculated from available evidence | **غير متاح** plus the specific reason |

Never substitute `—` for all six meanings.

Home remains visually complete with zero revenue because its composition depends on **a number, an explanation and real records**. It does not depend on a chart becoming interesting.

If the opportunity list reaches zero records, retain its heading and replace the rows with:

> **لا توجد فرص بيع مفتوحة**  
> لم تتحول أي جهة مهتمة من الحملة 38 إلى فرصة.  
> **مراجعة المهتمين**

Show that campaign sentence only while that condition remains true. No illustration, dashed drop zone, onboarding confetti or artificially tall blank panel.

Do not render the reference’s gradient bars now. There is no supported monthly target series to plot. When actual booked revenue exists, a compact historical chart can use blue gradient bars with matching cap dots, January at the right, and clearly distinct future periods. The current zero does not need twelve decorative columns.

**5. Explicit delete list**

Delete from **Home**:

- `#vChart`, `#vList`, their chart/list switch and `#quarters`.
- `MONTHLY`, prorated target arithmetic and the fabricated monthly target series.
- The five date presets and custom range controls.
- The readiness arc, account dot matrix, pipeline-health matrix and heat strip.
- Both funnels and every inferred stage-loss percentage.
- The entire embedded Kanban board, including rotated empty-stage rails.
- The standalone four-item decision card; replace it with the three contextual action rows.
- The separate indicators destination.
- The old toolbar, fake search shortcut and duplicate “الرئيسية” breadcrumb.

Delete or replace across **the system**:

- `.m-insight` and its decorative gradient, nested cards and carousel dots.
- Duplicate `.m-chip`, `.m-search`, `.m-crumb` and `.m-form` definitions.
- Negative tracking on Arabic text.
- `700ms`/`900ms` chart animations, text blur swaps and the second easing curve.
- Grab cursors and focusable cards without implemented actions.
- Physical direction declarations such as `background-position:left` and asymmetric physical padding.
- Hard-coded navigation counts.
- “hello”, ZIP filenames and skill-installation copy in product workflows.
- The unsupported weighted forecast and unsupported response-time statistic in Reports.
- The “توزيع بالتساوي” shortcut that silently suggests changing a deliberately Q3-scoped target.
- Repeated product campaign buttons and the second navigation strip on a product record.

Keep Reports for dated analysis and export. Keep the pipeline workspace for stage management. Keep Products for product readiness and configuration. Home owns the executive answer.

**Current design verdict: Block.** The source and proposed text-colour contrast were checked; the proposed layout has not been browser-rendered. No files were modified.
tokens used
84,667
**Massar should feel like a founder’s revenue ledger: one unmistakable number, an honest statement of what it means, and the work that can change it.**

The current page spends its attention budget drawing the database. It needs to spend that budget interpreting it.

**1. The diagnosis**

The most serious problems are factual. Visual polish currently makes them more convincing.

| Severity | Location | Before | Required change |
|---|---|---|---|
| HIGH | [home.html:97](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:97), `MONTHLY`, `sum()`, `paintQuarters()` | `TARGET / 12` distributes a **Q3-only, single-product target** across the year. Initial rendering changes the displayed requirement to **24,178**, and quarters receive **8,500** each. | Delete this allocation. Show **34,000 ر.س · الإجازات المرضية · الربع الثالث**. Other periods have **no target recorded**, not zero targets. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-matrix`, `.m-key` | All six lines are labelled **على المسار**, while all have been stationary for 29–35 days. | Replace the entire widget with **ستة بنود بلا حركة منذ 29–35 يومًا** beside the opportunity list. |
| HIGH | [home.html:79](/Users/abdulaziz/Projects/Massar/massar-ds/home.html:79), `.m-funnel` | Four records in one stage and one in another become a **75% loss**. These are current stage populations, not a tracked conversion cohort. | Delete the leakage claim and percentage. Preserve stage counts as counts. |
| HIGH | [reports.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/reports.html:33) | **3,360** “weighted expected” revenue has no supported probability model in the brief. “Six lines aged 30+ days” includes the 29-day line. | Remove the forecast. Show the actual **29–35-day range**; only five meet a 30-day threshold. |
| HIGH | [shell.js:11](/Users/abdulaziz/Projects/Massar/massar-ds/shell.js:11), Home decisions, Products summary | Navigation says six products; Home says five of six lack targets; reality is eight products, seven without targets. Products says one lacks published pricing, while six rows say otherwise. | Compute summaries from the same records as their tables. No separately maintained counts. |

The visual system then compounds those errors:

| Severity | Location | Before | After and why |
|---|---|---|---|
| MEDIUM | [massar.css:391](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:391), `.m-card`, `.m-grid--3` | Every secondary story gets a white surface, **24px padding**, **16px radius**, the same shadow and a **19px heading**. Equal treatment makes everything equally urgent. | Two substantial surfaces on Home: revenue and opportunities. Decisions and supporting evidence use plain rows. |
| MEDIUM | [massar.css:60](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:60), type tokens | Eight sizes, including **11px** and **12.5px**, push material qualifications into miniature grey text. | Five principal levels: **72, 28, 20, 15, 13px**. Target coverage must be readable body text. |
| MEDIUM | `.m-h1`, `.m-card__t`, `.m-lead__v` | Arabic titles inherit **−1px / −.3px tracking**; the monetary figure and currency share display treatment. | Arabic tracking **0**. Tighten Western display numerals only. Give Cairo room vertically. |
| MEDIUM | [massar.css:273](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:273) and [massar.css:540](/Users/abdulaziz/Projects/Massar/massar-ds/massar.css:540), `.m-chip` | The same component is defined twice: first **12.5px, 6px radius, 1px 7px padding**, later **11px, pill radius, 3px 9px**. | One definition: **13/22px**, pill, used only for actual statuses. The cascade should not make design decisions. |
| MEDIUM | `.m-chart`, `.m-arc`, `.m-heat`, `.m-fstep` | A **900×280** chart, **200px** gauge, **34px** heat cells and **30px** funnel bars illustrate mostly zeros and unsupported subdivisions. | Remove them from Home. Their area exceeds their information. |
| MEDIUM | `.m-col`, `.m-col--rail`, `.m-deal` | **252px columns**, **44px rotated empty rails**, cards inside columns inside a card. Six records require horizontal exploration. | One six-row table. Empty stages remain accessible in the pipeline workspace. |
| MEDIUM | `.m-side__logo`, `.m-insight`, `.m-fstep__b i`, `.m-meter i` | Blue–violet gradients assign decorative excitement to unrelated things. | One blue accent. Status colours carry meaning and readable labels. |
| MEDIUM | `.m-empty`, `.m-q__v.nil`, `.m-stat--mut` | Empty content is centred; zeros become faint. | Align to inline-start. **Booked zero stays black.** Absence is the principal finding. |
| MEDIUM | [products.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/products.html:33) | An implementation ZIP filename interrupts product management; another row literally says **hello**. | Remove both. Product copy describes the business record and its next action. |
| MEDIUM | [product.html:33](/Users/abdulaziz/Projects/Massar/massar-ds/product.html:33) | Global product navigation sits above five record tabs; summary tiles give campaign mentions equal weight to open revenue. | Record page gets a breadcrumb and one record-level tab strip. Overview leads with this product’s revenue, scoped target and two opportunity lines. |
| MEDIUM | Motion rules and `shell.js` | **700ms** chart growth, **900ms** gauges, multiple easing curves, press scales **.98/.985**, and a dialog that closes immediately despite comments promising an exit. | Static charts; one curve; **180ms enter / 120ms exit / 100ms press**, **.97** press scale. Implement the dialog exit before calling `close()`. |

There is also interaction theatre: `.m-search` is a `div` advertising `⌘K`; several “فتح” buttons have no handler; `cursor:grab` suggests dragging that the supplied scripts do not implement. These controls should either work or disappear.

**2. The fixed Home**

Use the brief’s snapshot date: **16 September 2026**.

The page has three parts, in this reading order.

**A. Revenue and its limits**

A compact page header:

> **الأداء التجاري**  
> السنة المالية 2026 · حتى 16 سبتمبر

No breadcrumb saying “الرئيسية” directly above it. No five-way date switch. Historical ranges belong in Reports.

One full-width revenue surface, internally divided into a dominant right column and a quieter left column:

| Right: dominant | Left: supporting |
|---|---|
| الإيراد المحقق | المستهدف المسجّل |
| **0 ر.س** | **34,000 ر.س** |
| لا صفقات رابحة حتى 16 سبتمبر | الإجازات المرضية · الربع الثالث فقط |
| **● لا توجد إيرادات محققة حتى الآن** | **سبعة منتجات بلا مستهدف. لا يمكن تقييم تحقيق مستهدف الشركة.** |
| Primary action: **مراجعة العرض المسعّر** | Secondary link: **استكمال المستهدفات** |
|  | قيمة البنود المفتوحة المسعّرة: **4,200 ر.س** |
|  | بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير |

That is the five-second answer. No invented probability, no company attainment percentage, no red downward arrow pretending a target gap is a period-over-period delta.

The reference’s large number and pill remain. The pill communicates a supported status.

**B. The work that changes the number**

Below the hero, use an asymmetric two-column layout.

The larger **right-hand column** contains the six opportunity lines. Put the priced quotation first because it is the only known money currently available to pursue.

Heading:

> **فرص البيع المفتوحة**  
> ستة بنود بلا حركة منذ 29–35 يومًا · آخر حركة في 18 أغسطس

Columns, in RTL order:

| العميل / المنتج | المرحلة | القيمة | بلا حركة |
|---|---|---:|---:|
| DL000 / الإجازات المرضية | عرض السعر | 4,200 ر.س | 29 يومًا |
| العمدة / الإجازات المرضية | اكتشاف الحاجة | لم يُسعّر | 35 يومًا |
| ابرهيم / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |
| ابرهيم / سجل التطعيمات الوطني | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / خدمات التطعيمات | تواصل أولي | لم يُسعّر | 35 يومًا |
| العمدة / تكامل الأنظمة HIS/ERP | تواصل أولي | لم يُسعّر | 35 يومًا |

Use one explicit record link per row. No repeated pill-shaped “فتح” buttons.

The smaller **left-hand column** is an unboxed action list titled **ما يعطّل البيع**:

1. **خمسة بنود بلا تسعير** — action: **استكمال التسعير**.
2. **16 حسابًا بلا مسؤول وبلا جهة اتصال مرتبطة** — action: **تعيين المسؤولين وربط جهات الاتصال**.
3. **جهتان مهتمتان دون فرصة من الحملة 38** — action: **مراجعة المهتمين**.

Each action opens the relevant filtered records. Do not send the founder to an unfiltered landing page.

Target incompleteness is already beside the target. Staleness is already beside the pipeline. Do not repeat either as another warning card.

**C. Supporting evidence**

One unboxed disclosure titled **تفاصيل المؤشرات**. Closed initially. Its summary reads:

> اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات

Inside, use four plain rows, not four cards:

- **Accounts:** 16 approved accounts; none has an owner or linked contact; seven have a sector and seven have a city. The 21 contacts are a separate entity count, not evidence of account linkage.
- **Campaign 38:** sent 21 → delivered 19 → seen 12 → replied 4 → interested 2 → opportunities 0. Render the sequence from right to left with labels and counts.
- **Activity totals:** 21 contacts, 359 messages, 1,233 events. Label these as recorded totals; do not imply they are today’s activity or revenue.
- **Knowledge:** eight weighted sections; objections, competitors and compliance are each 0%. Link to the named sections. Do not manufacture an overall readiness score from undocumented weights.

**This is the Home/indicators merger:** relevant indicators explain the revenue and actions; the rest remain available in one subordinate disclosure. Remove “مؤشرات الاستخدام” as a separate navigation destination and redirect its existing route to this disclosure.

Keep all eight products and their supplied readiness values in Products. Retain both published annual prices, the four inferred-sector labels, all three sectors plus “بلا قطاع”, and the explicit “لا يبيعه المساعد” status for صحة أعمال Plus. These facts do not need eight widgets on Home.

**3. Pasteable CSS**

Paste this **after the existing stylesheet** while replacing Home’s body content with the structure above. It overrides shared foundations and supplies the new Home layout. CSS cannot repair the target calculation or remove the old sections; those changes are mandatory.

Use this structure:

```html
<main class="m-page m-home">
  <header class="m-home__head">
    <h1 class="m-h1">الأداء التجاري</h1>
    <p class="m-meta">
      السنة المالية <bdi class="m-n">2026</bdi>
      · حتى <bdi class="m-n">16</bdi> سبتمبر
    </p>
  </header>

  <section class="m-card m-card--revenue"
           aria-labelledby="revenue-title">
    <div class="m-revenue__main">
      <h2 class="m-label" id="revenue-title">الإيراد المحقق</h2>
      <p class="m-revenue__value">
        <bdi class="m-n">0</bdi><span>ر.س</span>
      </p>
      <p class="m-body">لا صفقات رابحة حتى 16 سبتمبر</p>
      <p class="m-status m-status--warn">
        لا توجد إيرادات محققة حتى الآن
      </p>
      <div class="m-actions">
        <a class="m-btn m-btn--primary" href="#priced-line">
          مراجعة العرض المسعّر
        </a>
      </div>
    </div>

    <div class="m-revenue__context">
      <dl class="m-facts">
        <div>
          <dt>المستهدف المسجّل</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">34,000</bdi> ر.س
          </dd>
          <dd>الإجازات المرضية · الربع الثالث فقط</dd>
        </div>
        <div>
          <dt>قيمة البنود المفتوحة المسعّرة</dt>
          <dd class="m-facts__value">
            <bdi class="m-n">4,200</bdi> ر.س
          </dd>
          <dd>بند واحد مسعّر من ستة؛ خمسة بنود بلا تسعير</dd>
        </div>
      </dl>
      <p class="m-revenue__qualification">
        سبعة منتجات بلا مستهدف.
        لا يمكن تقييم تحقيق مستهدف الشركة.
      </p>
      <a class="m-link" href="perf.html">استكمال المستهدفات</a>
    </div>
  </section>

  <div class="m-home__work">
    <section class="m-card m-card--ledger"
             aria-labelledby="pipeline-title">
      <header class="m-section-head">
        <h2 class="m-h2" id="pipeline-title">فرص البيع المفتوحة</h2>
        <p class="m-meta">
          ستة بنود بلا حركة منذ <bdi class="m-n">29–35</bdi> يومًا
          · آخر حركة في <bdi class="m-n">18</bdi> أغسطس
        </p>
      </header>
      <!-- .m-tablewrap > table.m-table.m-ledger
           Use the six rows above.
           Give the priced row id="priced-line" and tabindex="-1". -->
    </section>

    <aside class="m-home__decisions" aria-labelledby="decisions-title">
      <h2 class="m-h2" id="decisions-title">ما يعطّل البيع</h2>
      <!-- Three .m-decision blocks:
           h3.m-decision__title, p.m-meta, a.m-link -->
    </aside>
  </div>

  <details class="m-evidence" id="indicators">
    <summary>
      <span class="m-h2">تفاصيل المؤشرات</span>
      <span class="m-meta">
        اكتمال بيانات العملاء · نتائج الحملة · معرفة المنتجات
      </span>
    </summary>
    <!-- Four .m-evidence__row blocks with the exact facts above. -->
  </details>
</main>
```

```css
/* MASSAR — revised foundations and revenue-first Home */
:root {
  /* Near-white ground; blue reserved for action and selection. */
  --m-page: #F6F7F5;
  --m-paper: #FFFFFF;
  --m-sunk: #EEF1EE;
  --m-line: #E3E7E3;
  --m-line-2: #CDD4CE;
  --m-dot: #D9DFDA;

  --m-ink: #17201F;
  --m-ink-2: #46504D;
  --m-mut: #646D69;
  --m-faint: #646D69;

  --m-ac: #245BD6;
  --m-ac-deep: #1947AF;
  --m-ac-dim: #EEF3FF;
  --m-ac-line: #BCCDF7;

  --m-ok: #17603D;
  --m-ok-dim: #EDF6F0;
  --m-ok-line: #BEDBC8;
  --m-warn: #8A4B08;
  --m-warn-dim: #FFF4E5;
  --m-warn-line: #E8CFAB;
  --m-bad: #B42318;
  --m-bad-dim: #FEF0ED;
  --m-bad-line: #F1C5BE;
  --m-idle: #646D69;
  --m-idle-dim: #EEF1EE;
  --m-idle-line: #CDD4CE;

  /* Compatibility for retained views: no violet palette. */
  --m-vi: var(--m-ac);
  --m-vi-dim: var(--m-ac-dim);

  /* Five principal type levels. Supporting figures use 28px. */
  --m-t-micro: 13px;
  --m-t-cap: 13px;
  --m-t-body: 15px;
  --m-t-sub: 15px;
  --m-t-h: 20px;
  --m-t-fig: 28px;
  --m-t-display: 28px;
  --m-t-hero: 72px;

  --m-leading-meta: 22px;
  --m-leading-body: 26px;
  --m-leading-section: 32px;
  --m-leading-title: 44px;
  --m-leading-figure: 40px;
  --m-leading-hero: 80px;

  --m-tracking-text: 0;
  --m-tracking-figure: -0.02em;
  --m-tracking-hero: -0.035em;

  /* 4px rhythm; 24 between groups, 32 between major regions. */
  --m-1: 4px;
  --m-2: 8px;
  --m-3: 12px;
  --m-4: 16px;
  --m-5: 24px;
  --m-6: 32px;
  --m-7: 48px;

  --m-r-chip: 999px;
  --m-r-ctl: 10px;
  --m-r-card: 16px;
  --m-r-band: 20px;

  --m-hair: 0 0 0 1px var(--m-line);
  --m-low: 0 1px 2px rgb(0 0 0 / 3%);
  --m-soft: 0 2px 8px rgb(0 0 0 / 3%);
  --m-lift: 0 8px 24px rgb(0 0 0 / 10%);
  --m-focus: 0 0 0 3px var(--m-ac-line);

  --m-ease: cubic-bezier(.16, 1, .3, 1);
  --m-move: var(--m-ease);
  --m-press: 100ms;
  --m-swap: 120ms;
  --m-in: 180ms;
  --m-out: 120ms;
}

body {
  font-family: Cairo, system-ui, sans-serif;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
  color: var(--m-ink-2);
  background: var(--m-page);
  direction: rtl;
  font-variant-numeric: lining-nums tabular-nums;
}

.m-n {
  display: inline-block;
  direction: ltr;
  unicode-bidi: isolate;
  font-variant-numeric: lining-nums tabular-nums;
  font-feature-settings: "lnum" 1, "tnum" 1;
}

.m-h1,
.m-greet__t {
  margin-block: 0;
  font-size: var(--m-t-display);
  line-height: var(--m-leading-title);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-h2,
.m-card__t {
  margin-block: 0;
  font-size: var(--m-t-h);
  line-height: var(--m-leading-section);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-body,
.m-label {
  margin-block: 0;
  font-size: var(--m-t-body);
  line-height: var(--m-leading-body);
  letter-spacing: 0;
}

.m-label { font-weight: 600; }

.m-meta,
.m-cap,
.m-stat__s,
.m-item__s,
.m-q__s,
.m-hint {
  margin-block: 0;
  font-size: var(--m-t-cap);
  line-height: var(--m-leading-meta);
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-stat__v,
.m-q__v {
  font-size: var(--m-t-fig);
  line-height: var(--m-leading-figure);
  font-weight: 700;
  letter-spacing: 0;
  color: var(--m-ink);
}

.m-stat__v .m-n,
.m-q__v .m-n {
  letter-spacing: var(--m-tracking-figure);
}

/* A known zero is ordinary data, not disabled content. */
.m-q__v.nil,
.m-stat--mut .m-stat__v {
  color: var(--m-ink);
}

/* Shared shell. */
.m-shell { min-block-size: 100dvh; }

.m-side {
  inline-size: 224px;
  block-size: 100dvh;
  border-inline-start: 0;
  border-inline-end: 1px solid var(--m-line);
  transition-duration: var(--m-in);
}

.m-side[data-collapsed] {
  inline-size: 68px;
  transition-duration: var(--m-out);
}

.m-side__logo { background: var(--m-ac); }

.m-side__grp { letter-spacing: 0; }

.m-nav {
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  border-radius: var(--m-r-ctl);
}

.m-side__w,
.m-nav span {
  transition: opacity var(--m-in) var(--m-ease);
  transform: none;
}

.m-side[data-collapsed] .m-side__w,
.m-side[data-collapsed] .m-nav span {
  transform: none;
  transition: opacity var(--m-out) var(--m-ease);
}

/* Use accessible link names; remove the clipped pseudo-flyout. */
.m-nav::after { content: none; }

.m-page {
  inline-size: 100%;
  max-inline-size: 1264px;
  margin-inline: auto;
  padding-inline: var(--m-6);
  padding-block: var(--m-6) var(--m-7);
}

.m-bar {
  position: static;
  padding-inline: var(--m-6);
  padding-block: var(--m-3);
  background: transparent;
  border-block-end: 0;
}

/* Home has its own useful header; delete its old toolbar markup. */
body[data-nav="home"] .m-bar { display: none; }

/* Shared surfaces: quiet structure, no hover elevation. */
.m-card {
  min-inline-size: 0;
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  background: var(--m-paper);
  border: 1px solid var(--m-line);
  border-radius: var(--m-r-card);
  box-shadow: none;
}

.m-card--pad0,
.m-card--ledger {
  padding-inline: 0;
  padding-block: 0;
}

.m-card--revenue {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr);
  gap: var(--m-6);
  padding-inline: var(--m-6);
  padding-block: var(--m-6);
  border-radius: var(--m-r-band);
  box-shadow: var(--m-soft);
}

/* Home composition. DOM order is also the mobile reading order. */
.m-home {
  display: grid;
  gap: var(--m-6);
}

.m-home__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--m-2) var(--m-5);
}

.m-revenue__main { min-inline-size: 0; }

.m-revenue__value {
  display: flex;
  align-items: baseline;
  gap: var(--m-3);
  margin-block: var(--m-2);
  color: var(--m-ink);
}

.m-revenue__value > .m-n {
  font-size: var(--m-t-hero);
  line-height: var(--m-leading-hero);
  font-weight: 700;
  letter-spacing: var(--m-tracking-hero);
}

.m-revenue__value > :not(.m-n) {
  font-size: 20px;
  line-height: 32px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--m-mut);
}

.m-revenue__context {
  min-inline-size: 0;
  padding-inline-start: var(--m-6);
  border-inline-start: 1px solid var(--m-line);
}

.m-facts {
  display: grid;
  gap: var(--m-5);
  margin-block: 0;
}

.m-facts dt {
  font-size: 13px;
  line-height: 22px;
  color: var(--m-mut);
}

.m-facts dd {
  margin-inline: 0;
  margin-block: var(--m-1) 0;
  font-size: 13px;
  line-height: 22px;
}

.m-facts .m-facts__value {
  font-size: 20px;
  line-height: 32px;
  font-weight: 600;
  color: var(--m-ink);
}

.m-revenue__qualification {
  margin-block: var(--m-5) var(--m-2);
  font-size: 15px;
  line-height: 26px;
  color: var(--m-ink);
}

.m-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--m-2);
  margin-block-start: var(--m-5);
}

.m-home__work {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: var(--m-6);
  align-items: start;
}

.m-section-head {
  display: grid;
  gap: var(--m-1);
  padding-inline: var(--m-5);
  padding-block: var(--m-5) var(--m-4);
}

.m-home__decisions {
  min-inline-size: 0;
  padding-block-start: var(--m-2);
}

.m-decision {
  display: grid;
  gap: var(--m-2);
  padding-block: var(--m-4);
  border-block-end: 1px solid var(--m-line);
}

.m-decision:last-child { border-block-end: 0; }

.m-decision__title {
  margin-block: 0;
  font-size: 15px;
  line-height: 26px;
  font-weight: 600;
  color: var(--m-ink);
}

/* One readable table, including when records are sparse. */
.m-tablewrap {
  overflow: auto;
  border-radius: 0 0 var(--m-r-card) var(--m-r-card);
}

.m-table th {
  block-size: 44px;
  padding-inline: var(--m-4);
  padding-block: var(--m-2);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  text-align: start;
  color: var(--m-mut);
  background: var(--m-paper);
}

.m-table td {
  padding-inline: var(--m-4);
  padding-block: 10px;
  font-size: 15px;
  line-height: 24px;
  font-weight: 400;
  color: var(--m-ink-2);
}

.m-ledger { min-inline-size: 560px; }

.m-ledger .m-item__s {
  margin-block-start: 2px;
  font-size: 13px;
  line-height: 20px;
}

.m-table td.m-td-v,
.m-table th.num {
  text-align: end;
  color: var(--m-ink);
}

.m-table td.m-td-n {
  font-weight: 600;
  color: var(--m-ink);
}

.m-ledger__unpriced {
  color: var(--m-warn);
  font-size: 13px;
  line-height: 22px;
  white-space: nowrap;
}

#priced-line { scroll-margin-block-start: var(--m-5); }

#priced-line:target { background: var(--m-ac-dim); }

/* Status: readable words plus a dot; never colour alone. */
.m-chip,
.m-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding-inline: 10px;
  padding-block: 3px;
  min-block-size: 28px;
  border-radius: var(--m-r-chip);
  background: var(--m-idle-dim);
  color: var(--m-idle);
  font-size: 13px;
  line-height: 22px;
  font-weight: 500;
  letter-spacing: 0;
  white-space: normal;
}

.m-status { margin-block: var(--m-4) 0; }

.m-chip::before,
.m-status::before {
  content: "";
  inline-size: 6px;
  block-size: 6px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: currentColor;
}

.m-status--warn,
.m-chip--warn {
  background: var(--m-warn-dim);
  color: var(--m-warn);
}

.m-chip--bad {
  background: var(--m-bad-dim);
  color: var(--m-bad);
}

.m-chip--ok {
  background: var(--m-ok-dim);
  color: var(--m-ok);
}

.m-chip--ac {
  background: var(--m-ac-dim);
  color: var(--m-ac-deep);
}

/* Controls: one geometry, real hit areas. */
.m-btn {
  min-block-size: 44px;
  justify-content: center;
  padding-inline: var(--m-4);
  padding-block: 9px;
  border: 1px solid var(--m-line-2);
  border-radius: var(--m-r-chip);
  box-shadow: none;
  font-size: 14px;
  line-height: 24px;
  text-decoration: none;
  transition:
    background-color var(--m-out) var(--m-ease),
    transform var(--m-press) var(--m-ease);
}

.m-btn--primary {
  border-color: var(--m-ac);
  background: var(--m-ac);
  color: #FFFFFF;
  box-shadow: none;
}

.m-btn--quiet {
  border-color: transparent;
  background: transparent;
  color: var(--m-ac-deep);
}

.m-btn--icon {
  inline-size: 44px;
  block-size: 44px;
}

.m-link {
  display: inline-flex;
  align-items: center;
  min-block-size: 44px;
  font-size: 14px;
  line-height: 24px;
  color: var(--m-ac-deep);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.m-input,
.m-select {
  min-block-size: 44px;
  font-size: 15px;
  line-height: 24px;
  transition: box-shadow var(--m-out) var(--m-ease);
}

/* Restore native select indicator; delete physical background-position. */
.m-select {
  appearance: auto;
  background-image: none;
  padding-inline: var(--m-3);
}

:where(a, button, input, select, textarea, summary):focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

/* Specificity overrides old focus rules. */
.m-btn:focus-visible,
.m-nav:focus-visible,
.m-tab:focus-visible,
.m-input:focus-visible,
.m-select:focus-visible,
.m-range input:focus-visible {
  outline: 2px solid var(--m-ac);
  outline-offset: 3px;
}

.m-btn:not(:disabled):active,
.m-nav:active,
.m-side__t:active,
.m-seg button:active,
.m-x:active {
  transform: scale(.97);
}

.m-btn:disabled:active { transform: none; }

@media (hover: hover) and (pointer: fine) {
  .m-btn:not(:disabled):hover { background: var(--m-page); }
  .m-btn--primary:not(:disabled):hover {
    background: var(--m-ac-deep);
  }
  .m-table tbody tr:hover { background: #F8FAF8; }
  .m-link:hover { color: var(--m-ac); }
}

/* Supporting evidence is a document section, not another dashboard. */
.m-evidence {
  border-block-start: 1px solid var(--m-line-2);
}

.m-evidence > summary {
  padding-block: var(--m-4);
  cursor: pointer;
  min-block-size: 44px;
}

.m-evidence > summary .m-meta {
  display: block;
  margin-block-start: var(--m-1);
}

.m-evidence__row {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: var(--m-4);
  padding-block: var(--m-4);
  border-block-start: 1px solid var(--m-line);
}

.m-evidence__row > * { margin-block: 0; }

/* A genuine empty record list: ordinary editorial content. */
.m-empty {
  padding-inline: var(--m-5);
  padding-block: var(--m-5);
  text-align: start;
}

.m-empty__t {
  font-size: 15px;
  line-height: 26px;
}

.m-empty__d {
  max-inline-size: 60ch;
  margin-inline: 0;
  font-size: 13px;
  line-height: 22px;
}

/* No drawing animations or blurred text swaps. */
.m-chart__grow,
.m-arc__fill,
.m-fstep__b i {
  animation: none;
}

.m-fstep__b i,
.m-meter i {
  background: var(--m-ac);
}

.m-view__p,
.m-view__p[data-enter] {
  opacity: 1;
  transform: none;
  filter: none;
  transition: none;
}

.m-input,
.m-select,
.m-tip2,
.m-table tbody tr,
.m-th-sort svg,
.m-cb {
  transition-timing-function: var(--m-ease);
}

.m-dlg__p {
  animation: m-dialog-enter var(--m-in) var(--m-ease);
}

dialog.m-dlg::backdrop {
  animation: m-fade var(--m-in) var(--m-ease);
}

dialog.m-dlg[data-closing] .m-dlg__p {
  animation: m-dialog-exit var(--m-out) var(--m-ease) both;
}

dialog.m-dlg[data-closing]::backdrop {
  animation: m-fade var(--m-out) var(--m-ease) reverse both;
}

@keyframes m-dialog-enter {
  from { opacity: 0; transform: scale(.97); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes m-dialog-exit {
  from { opacity: 1; transform: scale(1); }
  to { opacity: 0; transform: scale(.97); }
}

@media (max-width: 1200px) {
  .m-home__work { grid-template-columns: minmax(0, 1fr); }
}

/* Reachable mobile navigation without the existing unopened drawer. */
@media (max-width: 900px) {
  .m-shell { display: block; }

  .m-side,
  .m-side[data-collapsed] {
    position: static;
    inline-size: 100%;
    block-size: auto;
    transform: none;
    overflow: visible;
    border-inline-end: 0;
    border-block-end: 1px solid var(--m-line);
    transition: none;
  }

  .m-side__b,
  .m-side__f { display: none; }

  .m-side__nav {
    display: flex;
    overflow: auto;
    padding-inline: var(--m-4);
    padding-block: var(--m-2);
  }

  .m-nav { flex: 0 0 auto; }

  .m-side[data-collapsed] .m-nav span,
  .m-side[data-collapsed] .m-nav b {
    opacity: 1;
    transform: none;
  }

  .m-page,
  .m-bar { padding-inline: var(--m-4); }
}

@media (max-width: 700px) {
  :root {
    --m-t-hero: 56px;
    --m-leading-hero: 64px;
  }

  .m-home { gap: var(--m-5); }

  .m-card--revenue {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-5);
    padding-inline: var(--m-5);
    padding-block: var(--m-5);
  }

  .m-revenue__context {
    padding-inline-start: 0;
    padding-block-start: var(--m-5);
    border-inline-start: 0;
    border-block-start: 1px solid var(--m-line);
  }

  .m-evidence__row {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--m-2);
  }

  .m-input,
  .m-select { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }

  .m-btn:active,
  .m-nav:active,
  .m-side__t:active,
  .m-seg button:active,
  .m-x:active {
    transform: none;
  }
}
```

For dialog dismissal, `shell.js` must apply `data-closing`, wait for the panel’s exit, then call `close()`. Route the close button, Escape and backdrop through that function. Reduced motion closes immediately. CSS alone cannot delay the existing `close()` calls.

Western numerals also require formatting at the data boundary; `.m-n` does not convert digits:

```js
const formatNumber = new Intl.NumberFormat("ar-SA-u-nu-latn");
```

Counted nouns need authored plural forms. Use **لا بنود، بند واحد، بندان، ثلاثة بنود، 11 بندًا** according to the count and grammatical context. Do not construct Arabic prose with `${n} + noun`.

**4. The near-empty state is the design**

Keep these distinctions explicit:

| Data condition | Display |
|---|---|
| Known booked revenue is zero | **0 ر.س**, full-strength ink |
| An opportunity exists without pricing | **لم يُسعّر** |
| A target has not been configured | **لم يُحدّد** |
| No opportunity lines exist | **لا بنود مفتوحة** |
| A future period has not happened | **لم يبدأ بعد** |
| A value cannot be calculated from available evidence | **غير متاح** plus the specific reason |

Never substitute `—` for all six meanings.

Home remains visually complete with zero revenue because its composition depends on **a number, an explanation and real records**. It does not depend on a chart becoming interesting.

If the opportunity list reaches zero records, retain its heading and replace the rows with:

> **لا توجد فرص بيع مفتوحة**  
> لم تتحول أي جهة مهتمة من الحملة 38 إلى فرصة.  
> **مراجعة المهتمين**

Show that campaign sentence only while that condition remains true. No illustration, dashed drop zone, onboarding confetti or artificially tall blank panel.

Do not render the reference’s gradient bars now. There is no supported monthly target series to plot. When actual booked revenue exists, a compact historical chart can use blue gradient bars with matching cap dots, January at the right, and clearly distinct future periods. The current zero does not need twelve decorative columns.

**5. Explicit delete list**

Delete from **Home**:

- `#vChart`, `#vList`, their chart/list switch and `#quarters`.
- `MONTHLY`, prorated target arithmetic and the fabricated monthly target series.
- The five date presets and custom range controls.
- The readiness arc, account dot matrix, pipeline-health matrix and heat strip.
- Both funnels and every inferred stage-loss percentage.
- The entire embedded Kanban board, including rotated empty-stage rails.
- The standalone four-item decision card; replace it with the three contextual action rows.
- The separate indicators destination.
- The old toolbar, fake search shortcut and duplicate “الرئيسية” breadcrumb.

Delete or replace across **the system**:

- `.m-insight` and its decorative gradient, nested cards and carousel dots.
- Duplicate `.m-chip`, `.m-search`, `.m-crumb` and `.m-form` definitions.
- Negative tracking on Arabic text.
- `700ms`/`900ms` chart animations, text blur swaps and the second easing curve.
- Grab cursors and focusable cards without implemented actions.
- Physical direction declarations such as `background-position:left` and asymmetric physical padding.
- Hard-coded navigation counts.
- “hello”, ZIP filenames and skill-installation copy in product workflows.
- The unsupported weighted forecast and unsupported response-time statistic in Reports.
- The “توزيع بالتساوي” shortcut that silently suggests changing a deliberately Q3-scoped target.
- Repeated product campaign buttons and the second navigation strip on a product record.

Keep Reports for dated analysis and export. Keep the pipeline workspace for stage management. Keep Products for product readiness and configuration. Home owns the executive answer.

**Current design verdict: Block.** The source and proposed text-colour contrast were checked; the proposed layout has not been browser-rendered. No files were modified.
