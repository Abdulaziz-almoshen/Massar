# Massar UI transformation — the Pillio/AI-Manager direction

**Design review, 2026-09-07.** Output of `/plan-design-review`. Founder-approved direction, seven
review passes, and the token rewrite DESIGN.md needs before any of it can ship past gate step 22.

> **Status: reviewed, not built.** Nothing in `massar-engine/src/` was touched. Mockups are real
> HTML rendered in the production medium and live in
> `~/.gstack/projects/Abdulaziz-almoshen-Massar/designs/massar-pillio-20260907/`.

---

## 0. The decision record

| # | Decision | Answer | Where |
|---|---|---|---|
| D1 | Review target | Current UI surfaces (`dashboard.ts`, `DESIGN.md`, the prototype) | founder, chat |
| D2 | Transformation depth | **Full visual personality, correctness machinery kept** | founder, chat |
| D3 | Review scope | All seven passes | founder, chat |
| D4 | Dashboard direction | **Variant B** — Pillio grammar at ledger density | founder, chat |
| D5 | Leads page direction | **Variant E** — the AI-Manager table grammar, on Massar's own signals | founder, chat |

**Two references, two jobs.** They do not compete:

- **Pillio** (`00-reference-pillio.png`) governs the **overview** surfaces — one accent-gradient hero
  tile carrying the leading figure, white cards on a lavender-white canvas, a floating rail, a
  greeting that carries the work count.
- **AI Manager** (founder-supplied, 2026-09-07) governs the **list/record** surfaces — a real table
  with a header row and column dividers, outlined status pills, per-row quick actions, KPI cards
  with a delta chip and a circular icon, a grouped rail with section labels.

One token set serves both. That is the system.

### What was rejected, and why

| Variant | Verdict | Reason |
|---|---|---|
| A — Pillio-faithful | rejected | Eight facts on screen. Massar's home answers a manager holding 61 opportunities; A cannot hold them. |
| C — work-owed spine | rejected | Drops the greeting the founder's own reference leads with, and the icon-only rail collides with a known defect (see §7, U-4). |

Both are kept as `variant-A.html` / `variant-C.html`. They are the evidence that the choice was made
between viewed alternatives, not asserted.

---

## 1. What already exists (reuse before building)

| Asset | What it gives this work |
|---|---|
| `src/motion.ts` | **16 named motion patterns**, already token-bound and RTL-correct. The transformation adds no new animation vocabulary; it re-skins what these already drive. |
| `src/crm-primitives.ts` | The shared row/badge/pill helpers. The new table grammar lands here once, not per screen. |
| `src/palette.ts`, `src/seha.ts` | The token emission layer. The colour rewrite is a change to these two files plus DESIGN.md §2 — not 4,447 lines of `dashboard.ts`. |
| `src/signal-domain.ts` | The **seriousness meter (0-100), its four bands, and momentum** — already pure, already unit-tested. The leads page displays these. Nothing new is computed. |
| `scripts/check-design.mjs` | Gate step 22. It already measures contrast and rejects off-ladder values. It enforces the new tokens the day they land. |
| `docs/decisions/0001` | Anchored-replacement rule for `dashboard.ts`. Binds every task below. |

**Not one of these needs to be written.** The transformation is a token swap plus a shell rewrite.

---

## 2. The token delta — measured, not chosen

Every ratio below was computed, not judged. The three marked **CAUGHT** were failures in this
review's own first proposal, found by measuring before drawing.

### Accent — violet replaces Seha blue

```
--v:        #6C5CE7   primary. 4.86:1 on --paper, and white on it is 4.86:1 — legal both ways.
--v-press:  #5A4BD6   pressed / heavier weight. 5.36:1 on --surface (violet text on a grey row).
--v-deep:   #4B3FBF   gradient dark stop, badge text on --v-tint (6.44:1).
--v-mark:   #7A6BEE   THE DOT TOKEN. 3.54:1 on --surface, 4.07:1 on --paper.
--v-light:  #8B7BF5   decorative only — 3.36:1 on paper, 2.93:1 on --surface. NEVER a mark, never a text ground.
--v-tint:   #EDEAFD   selected row, quiet fill.
--v-wash:   #F4F2FD   row hover.
--grad:     linear-gradient(255deg,#4B3FBF,#6C5CE7)
```

**`--grad` is a legal text ground at every stop** — 7.60:1 and 4.86:1. Pillio's own gradient runs to
`#8B7BF5`, where white measures **3.36:1**; that gradient cannot carry the small white labels the
reference puts on it. Ours is darkened so it can. This is the single most important deviation from
the reference and it is not negotiable.

### CAUGHT — three defects in this review's own proposal

| # | Defect | Measured | Fix |
|---|---|---|---|
| C-1 | `--ok #128A5A` as badge text on `--ok-soft` | **3.86:1**, below the 4.5 floor | `--ok: #0E6E48` → 5.55:1 |
| C-2 | `--v-light #8B7BF5` as a status **dot** on `--surface` | **2.93:1**, below the 3:1 non-text floor | added `--v-mark: #7A6BEE` → 3.54:1 |
| C-3 | The ghost pill button's only affordance was a `--line` hairline | **1.29:1** | moved to a `--surface` ground; a border may never be a control's only signal |

C-2 is byte-for-byte the failure DESIGN.md already retired as `--s-sched` (2.93:1). It reappeared
because a new accent family was introduced without re-deriving its mark. **Prior learning applied:
`blue-focus-ring-on-blue-primary-button` (10/10, 2026-09-06).**

### Ground, ink, status

```
--paper:#FFFFFF  --canvas:#F7F6FC  --surface:#F0EEF9  --surface-2:#E9E6F4
--line:#E4E1F0 (1.29 — decorative hairline ONLY)   --line-soft:#EFEDF7
--ink:#16151F (18.09)   --ink-2:#35333F (12.38)   --muted:#6B6880 (5.36 paper / 4.67 surface)

--ok:#0E6E48  --ok-mark:#1E9E63 (3.43)  --ok-soft:#E3F5EC
--warn-mark:#B37F00 (3.53)  --warn-soft:#FDF3D9  --warn-text:#7A5600 (6.01 on soft)
--fail:#D14343 (4.57)  --fail-soft:#FBE9E9  --fail-text:#8E2A27 (7.14 on soft)
--off-mark:#7F8595 (3.69)  --off-soft:#EFEEF5  --off-text:#4A5560 (6.60 on soft)
```

`--muted` stays the lightest text token. The four-value status contract (MARK / FILL / SOFT / TEXT)
survives the rebrand unchanged — only the accent family moved.

### Radius, shadow, and the density rule they need

```
--r-sm:10  --r-md:14  --r-lg:20  --r-xl:26  --r-pill:999
--sh-0: 0 1px 2px rgba(41,35,80,.04)   flat card on a tinted canvas
--sh-1: 0 2px 8px rgba(41,35,80,.06)   resting card on white
--sh-2: 0 8px 24px rgba(41,35,80,.08)  the hero tile, and floating elements
```

**Radius is assigned by object, never uniformly** — uniform bubbly radius is AI-slop pattern #5:

| Object | Radius |
|---|---|
| Rail panel, page-level card | `--r-xl` |
| Card, panel, hero tile | `--r-lg` |
| Nested row-card, tile, input, nav item | `--r-md` |
| Meter segment, chip, skeleton block | `--r-sm` |
| Pill button, badge, avatar, progress track | `--r-pill` |
| Table row | **`--r-none`** — a row inside a panel takes the panel's clip, never its own radius |

### New: hatch is a texture channel

```
.hatch    repeating-linear-gradient(115deg, rgba(255,255,255,.85) 0 3px, rgba(255,255,255,.12) 3px 8px)
.hatch-g  repeating-linear-gradient(115deg, #DAD6EC 0 3px, transparent 3px 7px)
```

Hatch means **"not yet"** — the unfilled remainder of a bar, a stage not reached, a period with no
target. It is a *second channel* on top of colour, so it strengthens §3.0b rather than decorating.
Both references use it; adopting it by name means it means one thing everywhere.

### What §2 keeps unchanged

Cairo, the type ladder, the spacing scale, the z-index steps, the three breakpoints, the motion
tokens, and every rule in §4. **The transformation does not touch a single correctness rule.**

---

## 3. Pass 1 — Information Architecture · **3/10 → 9/10**

### The gap

The ask named a reference and no hierarchy. Measured against the live build: `#home` leads with four
equal-weight KPI tiles, so **nothing leads**. Two primary buttons compete on that one screen
(«حدّد المستهدفات» in `--blue`, «إنشاء حملة» in near-black), against §3.7's one-primary rule. The
reference has exactly the point of view Massar's home is missing, and the one-line ask never
transferred it.

### Constraint worship — if home shows only three things

1. **The money that is moving.** «المتوقع من الفرص المفتوحة» — one figure, on the one gradient tile.
2. **The work owed today.** Six rows, ranked, each ending in a next step or the absence of one.
3. **What is broken.** «يحتاج انتباهك» — three rows, each with a verb.

Everything else moves under a door. The sector rollup, the campaign counts, and the activity band
are supporting, not leading.

### Home (variant B) — the structure

```
┌─ rail (RIGHT, 236px, floating, --r-xl) ──┬─ main ────────────────────────────────┐
│ مسار                                      │ [search ⌘K ............] [🔔²][👤]    │
│ ● الرئيسية      (active: white pill)      │                                       │
│   فرص البيع                                │ صباح الخير، عبدالعزيز      [+ حملة]  │
│   العملاء                                  │ الخميس ١٧ مارس · ٤ جهات تنتظر ردًّا   │
│   المنتجات                                 │                                       │
│   الحملات                                  │ ┌HERO(grad)┐┌KPI┐┌KPI┐┌KPI┐          │
│   التقارير                                 │ │ ٦٠٬٠٠٠  ││محقق││هدف││حملة│          │
│                                           │ │ ▓▓░░░░░ ││spk ││ — ││spk │          │
│                                           │ └─────────┘└───┘└───┘└───┘          │
│                                           │ ┌── ما يستحق اتصالك اليوم ──┐┌أين───┐ │
│   الإعدادات   (bottom group)               │ │ 6 rows, then ١–٦ من ٦١   ││المفتوح│ │
│   الدعم                                    │ └──────────────────────────┘├──────┤ │
└───────────────────────────────────────────┴──────────────────────────────┴يحتاج─┘ │
```

**Reading order, deliberate:** greeting → the money → the work → the exceptions. The eye lands on
the one saturated surface on the page, which is also the one number the business is measured by.

### Two IA moves this makes explicit

1. **Search leaves the rail.** Today `⌘K` sits *inside* the navigation rail. The rail becomes
   navigation only; search becomes the top bar's anchor. This is a structural change, not a move —
   it changes what the rail is for.
2. **The KPI row stops being four equal tiles.** One tile is the hero and carries `--t-num`; the
   other three are supporting at `--t-2xl`. §7.13 already demanded this («A page must have a point
   of view»); the current home does not comply and no one noticed because all four looked equally
   important.

### Leads (variant E) — the structure

```
crumb: نظرة عامة / العملاء
كل الجهات                                    [تصدير] [+ استيراد جهات]
┌KPI كل الجهات ٢١┐┌ردّوا ٩┐┌جاد أو أعلى ٤┐┌طلبوا الإيقاف ١┐   ← each with a delta chip
└ قائمة الجهات ─────────────────────────────────── [🔍][⛛][⬇] ┐
  [الكل ٢١][ردّوا ٩][جاد أو أعلى ٤][صامت ٧][لم يردّوا ١٢][الإيقاف ١]
  الجهة │ الخدمة والمصدر │ درجة الجدية │ الزخم │ آخر تواصل │ إجراء
  ────────────────────────────────────────────────────────────
  د. سليمان العتيبي  تكامل الأنظمة   ٨٢/١٠٠ جاهز للإغلاق  يتصاعد  منذ ساعتين  📞💬
  ...
  أ. خالد الدوسري   ← RED GROUND + inline-start bar: طلب الإيقاف, send disabled, reason in words
  ١–٧ من ٢١ جهة              ٤ جهات جادة · جهة واحدة طلبت الإيقاف
```

**The column that matters:** the reference prints a meaningless `35%` on every row.
Massar has `signal-domain.ts`, which already computes a real 0-100 seriousness score with four named
bands and a momentum read, each traceable to ledger evidence. That column is the difference between
copying a screenshot and shipping a product.

**No issues remain open in this pass.**

---

## 4. Pass 2 — Interaction State Coverage · **1/10 → 9/10**

### The gap, proven by running the live app

`#kmon` renders an **empty white body for roughly five seconds**, then fills at six. No skeleton, no
spinner, nothing that says work is happening. Worse: the smoke assertion for that route is
«الحملات», a string that appears in the nav rail *and* the breadcrumb — so smoke passes on a page
whose content never arrived. Verified 2026-09-07 against production, `bodyLen` 0 at 1.5s and 781 at
6s, zero console errors.

The redesign adds async surfaces (work queue, sector bars, seriousness meters, activity ribbon). With
no state table it ships **more** blank screens, not fewer.

### The state table

| Surface | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL |
|---|---|---|---|---|---|
| Hero tile | skeleton block at the exact figure box, ≥400ms hold | «لا فرص مفتوحة» + «أضف فرصة» | «تعذّر حساب المتوقع» + «أعد المحاولة»; never a silent «٠» | `moNumber()` pop-in on CHANGE only | figure renders, bar hatched, «التغطية غير مكتملة» |
| Work queue | `moSkeleton(5)` — **5 rows max** regardless of eventual length | «لا شيء يستحق اتصالك اليوم» + «تصفّح كل الفرص ٦١» | «تعذّر تحميل القائمة» + retry, table chrome stays | rows cross-fade over `--base` | rows shown + «١–٦ من ٦١» + a «تعذّر تحميل الباقي» line |
| Leads table | `moSkeleton(5)` at real row height | «لا جهات بعد» + «استيراد جهات» | inline row, retry, filters stay usable | `.mo-nip` pill for rows arriving mid-read | count chips render, «الجدية» column shows «—» until signals resolve |
| Seriousness meter | grey track, no number | «لم يردّ بعد» + «—» (**never «٠٪»**) | «تعذّر حساب الدرجة» | meter fills once, from zero, on first paint only | score shown, band hidden, «بيانات ناقصة» |
| Sector bars | 3 skeleton bars | «لا قطاعات» | inline | staggered `.mo-stagger`, capped at 8 | hatched track + «—» per §4 |
| Alerts card | 3 skeleton rows | «لا شيء يحتاج انتباهك» — **warm, and a real end state** | inline | `moFlash` on a resolved item | partial list + count |
| Campaigns (`#kmon`) | **`moSkeleton(5)` — this is the fix for the five-second blank** | «لم تُرسل حملة بعد» + «إنشاء حملة» | «تعذّر تحميل الحملات» + retry | list cross-fade | list + «تعذّر تحميل الإحصاءات» |
| Opt-out row | n/a | n/a | n/a | n/a | **always renders with its reason in words** |

### Rules this table encodes

- **Every empty state names itself** (§4 already requires it) — a blank table and a broken query must
  never look alike.
- **A skeleton is at the exact height and inline-size of what it replaces.** A skeleton that resizes
  on swap is interior.dev failure 1.
- **At most 5 skeleton rows**, regardless of the real list length.
- **Nothing below `--spinner-delay` (300ms) shows anything**; once shown, hold 400ms so it cannot
  flash.
- A zero denominator renders «—», never «٠٪».

**No issues remain open in this pass.**

---

## 5. Pass 3 — User Journey & Emotional Arc · **2/10 → 8/10**

| Step | The rep does | Feels | What the design gives them |
|---|---|---|---|
| 1 | Opens Massar at 8am | "What happened overnight?" | The greeting carries the count: «٤ جهات تنتظر ردًّا». Not decoration — the first line is the answer. |
| 2 | Scans for 3 seconds | "Where do I look?" | Exactly one saturated surface. The eye has no competition. |
| 3 | Reads the work queue | "Who first?" | Ranked, and the last column is a next step or its absence. «بلا خطوة · ٩ أيام» in `--fail-text` is the one thing shouting. |
| 4 | Opens a lead | "Is this real?" | ٨٢/١٠٠ «جاهز للإغلاق» + «يتصاعد» — an earned number, with «لماذا هذه القراءة؟» behind it. |
| 5 | Sees an opt-out | "Can I message them?" | Red ground, an inline-start bar, the send control disabled, **and the reason in words**. Impossible to misread. |
| 6 | Finds nothing to do | "Am I done?" | «لا شيء يحتاج انتباهك» is a real end state, not an error. |

### Time horizons

- **5 seconds (visceral).** The gradient tile is the whole first impression. It has to be the number
  the business is measured by, or the design is lying about what matters.
- **5 minutes (behavioral).** The work queue and the filter chips carry counts of work *owed*, never
  totals (§7.10). «فرص البيع ٤» is a reason to click; «العملاء ١٬٧٠٠» is wallpaper.
- **5 years (reflective).** «صباح الخير» is warm on day one and noise on day four hundred — **unless
  it carries the count**, which is why variant B's greeting has a second line and variant A's does
  not. That is the whole reason B beat A on this pass.

### The one thing this pass changes about the reference

Pillio's greeting is pure warmth. Massar's cannot be. It becomes a **status line with a warm
opening** — the tone survives, the emptiness does not.

**No issues remain open in this pass.**

---

## 6. Pass 4 — AI Slop Risk · **4/10 → 8/10**

**Classifier: APP UI.** Workspace-driven, data-dense, task-focused. Landing-page rules do not apply;
the App UI rules do — calm surface hierarchy, few colours, minimal chrome, cards only where the card
*is* the interaction.

### Hard rejection check

| # | Criterion | Verdict |
|---|---|---|
| 1 | Generic SaaS card grid as first impression | **PASS** — one hero + three supporting tiles + a real table. Not a mosaic. |
| 2 | Beautiful image with weak brand | PASS — no imagery at all. |
| 3 | Strong headline with no clear action | PASS — the headline carries a count and a primary button. |
| 4 | Busy imagery behind text | PASS. |
| 5 | Sections repeating the same mood statement | PASS. |
| 6 | Carousel with no narrative purpose | PASS — none. |
| 7 | **App UI made of stacked cards instead of layout** | **FIRES on variant A** — which is why A was rejected. B and E use a table and a panel. **Mitigated by the choice.** |

### Litmus

| # | Check | Answer |
|---|---|---|
| 1 | Brand unmistakable in first screen? | YES — Arabic RTL, Cairo, «مسار», the violet mark. |
| 2 | One strong visual anchor? | YES — the single gradient tile. |
| 3 | Understandable by scanning headlines only? | YES — «ما يستحق اتصالك اليوم» / «أين المفتوح الآن» / «يحتاج انتباهك» each state what the area is. |
| 4 | Each section one job? | YES. |
| 5 | Are cards actually necessary? | **PARTIAL** — see the ruling below. |
| 6 | Motion improves hierarchy? | YES — all 16 patterns come from `motion.ts`; nothing new invented. |
| 7 | Premium with all decorative shadows removed? | YES — `--sh-0` is nearly invisible by design; the layout carries it. |

### The blacklist item this design must answer honestly

**Blacklist #1 is "purple/violet/indigo gradient backgrounds."** This plan proposes a violet accent
with a gradient tile. That is a real signal and it deserves a real answer, not a dismissal:

- The **canvas is `#F7F6FC`**, a near-white. There is no purple background. The gradient occupies
  **one tile on one screen**, and its area encodes the leading figure.
- It is not a blue-to-purple scheme. It is one hue, dark-to-mid, chosen so **both stops carry white
  text legally** (7.60 / 4.86).
- It came from a **named reference the founder chose**, not from a default. The distinction that
  matters is not the hue — it is whether the hue was decided or defaulted into.
- **The binding rule:** one gradient surface per screen, on the tile that carries the leading figure,
  never behind body text, never inside a plotting area (§6.7 stands unchanged).

Blacklist #5 (uniform bubbly radius) is answered by the radius-by-object table in §2. Blacklist #2
(the 3-column icon-in-circle feature grid), #3, #4, #6, #7, #9, #10 do not apply to an app surface.
**#11 does not apply** — Cairo is a real typeface, deliberately chosen, loaded as a variable face.

### Where slop risk actually remains

The KPI card in variant D/E is `circular icon + delta chip + label + figure`, repeated four times.
That is one step from the SaaS template look. **The mitigation is content, not styling:** each of the
four says something different in kind (a count, a ratio, a money figure, a prohibition), and the
fourth — «طلبوا الإيقاف ١ · لا يجوز الإرسال إليهم» — is a card no template would ever produce.

**No issues remain open in this pass.**

---

## 7. Pass 5 — Design System Alignment · **2/10 → 9/10**

### The three invariants the references contradict, and the ruling on each

**§3.6 — "A row is not a card."** Both references make every list row a soft card. DESIGN.md forbids
it in bold. **Ruling: row-as-card is admitted, bounded by density.**

> A row may carry a `--surface` ground and `--r-md` **only where the surface shows at most 12 rows at
> once** (the home work queue, the alerts card, the appointments card). Any surface that can exceed
> 12 rows — the leads table, the opportunity list, the campaign list, every `qa:scale` surface —
> stays a **flush table**: a header row, `--line-soft` dividers, no per-row radius, no per-row
> shadow. Hover is a ground change (`--v-wash`), never a lift.

This is why variant E is a table and variant B's queue is cards. The rule is what makes both legal.

**§3.1 — "one saturated hue on a surface."** Survives, with the accent family swapped. The three
named status exceptions (`--s-attend` / `--s-review` / `--s-sched`) were byte-identical to the old
`--blue` — they must be **re-derived against violet**, or they become the only blue left in the
product. Open decision U-1 below.

**§2 radii.** `--r-xl:26` is a new step, added rather than improvised. The four-value scale becomes
five, and the radius-by-object table (§2) keeps it from becoming uniform mush.

### The delta DESIGN.md needs

| DESIGN.md | Change |
|---|---|
| §1 | Rewrite the provenance: the source is now two named references plus the Seha structural inheritance. |
| §2 Colour | Replace the blue ramp with the violet ramp above, with measured ratios inline. |
| §2 Status | `--ok` → `#0E6E48` (C-1). Everything else stands. |
| §2 Radius | Add `--r-xl:26`. Add the radius-by-object table. |
| §2 Shadow | Replace `--sh-1/2/3` with `--sh-0/1/2` retuned to a violet-grey. |
| §2 (new) | **Texture:** `.hatch` / `.hatch-g` and the single meaning "not yet". |
| §3.1 | Same rule, violet. State the status-family re-derivation (U-1). |
| §3.6 | Rewrite per the density ruling above. |
| §3.8 | **Unchanged and re-verified:** a violet ring on the violet button measures **1.00:1**. The inversion (`--paper` ring + a `rgba(108,92,231,.35)` halo) is what makes focus visible. A ring in `--v` on `--canvas` measures 4.52:1 and is fine everywhere else. |
| §5 | Add: **table**, **outlined status pill**, **seriousness meter**, **delta chip**, **filter chip**. Each with rest/hover/active/focus-visible/disabled/loading. |
| §8 | Unchanged. The 16 patterns in `motion.ts` re-skin without renaming. |
| §9 | Re-baseline `check-design.mjs`: the existing violation count is against the old palette and is meaningless after the swap. |

### Gate step 22 — the migration that must not be skipped

`check-design.mjs` fails on any hex in `src/` that is not a §2 token. **On the day the palette
changes, every existing blue literal becomes a violation at once.** The order is not optional:

1. DESIGN.md §2 lands first, with the new tokens.
2. `palette.ts` / `seha.ts` emit them.
3. `check-design.mjs` re-baselines in the same commit.
4. Screens migrate; the baseline count may only go down.

Reversing 1 and 3 puts the repository in a state where nothing builds.

**No issues remain open in this pass.**

---

## 8. Pass 6 — Responsive & Accessibility · **1/10 → 9/10**

### Three breakpoints, three intentional layouts

| Viewport | Rail | Home | Leads |
|---|---|---|---|
| **`--bp-lg` 1280+** (design target) | 236px floating panel, labels visible | hero + 3 KPI, then 1.75fr / 1fr | full table, 6 columns |
| **`--bp-md` 900** | collapses to a **72px icon rail**, labels become `title` + an accessible name | KPI row wraps to 2×2; the two-column body stacks, work queue first | «الزخم» and «آخر تواصل» merge into one stacked cell |
| **`--bp-sm` 560** (`/rep`) | rail becomes a bottom bar, 5 destinations, 44px targets | single column: greeting → hero → work queue → alerts. Sector bars drop below the fold, not out. | **the table becomes cards** — this is the one place the density ruling inverts, because a 6-column table at 375px is not a table |

"Stacked on mobile" is not in this plan. Each viewport gets a decision.

### Accessibility — the floor, restated for the new palette

- **Contrast:** every pair in §2 is measured. Body/label ≥ 4.5:1; non-text that carries meaning
  ≥ 3:1 against **every** ground it lands on — which is exactly how C-2 was caught.
- **Focus:** `:focus-visible` only, `2px solid var(--v)`, offset 2px, **inverting to `--paper` + a
  4px halo on any ground where it drops below 3:1** — the violet button being the case that proves
  the rule (1.00:1 without it).
- **Focus management:** `#body` is rewritten on every keystroke. The focused element must survive the
  re-render, or typing in the leads filter loses the cursor. §3.9 already says this; the new
  filter-chip row makes it reachable in one more place.
- **Touch targets:** 24×24 always, 44×44 under `pointer:coarse`. **Known defect carried forward:**
  the subnav tab measures **43px** on a phone — one pixel short, because the strip carries a 1px
  border. The new table's per-row action buttons are 32px visual and need a transparent `::after` to
  reach 44 on coarse pointers.
- **Colour is never the only channel (§3.0b):** every status pill is colour **+ dot + word**; every
  delta chip is colour **+ arrow glyph + number**; the hatch is a **texture** channel on top of
  colour. The disabled send control on an opt-out row carries **its reason in words**, because a
  dimmed control whose only signal is dimness violates §3.0b.
- **Reduced motion:** the floor stands — the trip is optional, the destination is not. A seriousness
  meter that only reads correctly after animating is a meter that never reads.
- **Bidi:** every Latin run inside Arabic is wrapped — `(HIS/ERP)`, phone numbers, IDs, and every
  `--t-num` figure. Numeric columns align to the inline-end and are `dir="ltr"` internally.

**No issues remain open in this pass.**

---

## 9. Pass 7 — Unresolved decisions

These will haunt the implementation if they stay open. Each is evidenced.

| # | Decision needed | If deferred, what happens |
|---|---|---|
| **U-1** | Do `--s-attend` / `--s-review` / `--s-sched` re-derive against violet, or stay blue? | They are byte-identical to the **old** `--blue`. Left alone, they become the only blue in the product and read as a bug, not a channel. |
| **U-2** | **The target basis — bookings / ACV / TCV.** Still open from the Sep 4 CEO review. | This redesign makes that undecided number the single largest element on the home screen. Shipping the hero tile before the basis is decided means the biggest thing on the page is a number nobody has defined. |
| **U-3** | Which pipeline stages are real? | `opps-domain.ts` carries **six**; «المستهدفات والأداء» ships **eight**. Two are unreachable. The leads meter and the stage column both read from that list, so the redesign inherits the discrepancy on two more screens. |
| **U-4** | Does the 5-second home poll survive a DB-backed home? | `dashboard.ts:4153` polls `#home` and `#kmon` every 5s. Today home reads an in-memory snapshot. A DB-backed work queue turns that into **48 queries a minute per open tab**, on the one shared-CPU machine that also serves the Gupshup webhook. |
| **U-5** | Does the greeting need a real user identity? | Admin is a **token**, not a user record. «صباح الخير، عبدالعزيز» has nothing to read a name from today. Deferred, it ships as a hardcoded string or a generic «صباح الخير». |
| **U-6** | Does `/rep` get the transformation in the same cycle? | Left out, Massar ships two visual systems and the rep — the actual daily user — keeps the old one. |

**U-2, U-3 and U-4 are blocking.** The other three can be decided during the build.

---

## 10. NOT in scope

| Deferred | Why |
|---|---|
| Dark mode | §3.11 says there is none, and both references are light-only. A dark Massar is a separate rebrand of DESIGN.md, not a media query. |
| The `/rep` phone surface | Real scope, real work, and it deserves its own pass. Named as U-6 rather than smuggled in. |
| New charts | §6 stands unchanged. This is a re-skin of existing geometry, not new encodings. |
| New motion patterns | The 16 in `motion.ts` cover every moment in both references. Adding a seventeenth needs a reason written down first. |
| The Arabic counted-noun retrofit beyond `opps-crm.ts` | Pre-existing debt, orthogonal to the visual system. |
| Any change to `*-domain.ts` | The transformation is presentation. Business rules do not move. |

---

## 11. Implementation Tasks

Synthesized from this review's findings. Each derives from a specific finding above.

- [ ] **T1 (P1, human: ~1d / CC: ~25min)** — DESIGN.md — rewrite §1, §2, §3.1, §3.6, §3.8, §5, §9 to the violet system
  - Surfaced by: Pass 5 — "the three invariants the references contradict"
  - Files: `DESIGN.md`
  - Verify: every colour in §2 carries a measured ratio; §3.6 states the 12-row density ruling
- [ ] **T2 (P1, human: ~4h / CC: ~15min)** — palette.ts/seha.ts — emit the new tokens and re-baseline the design gate in the same commit
  - Surfaced by: Pass 5 — "reversing 1 and 3 puts the repository in a state where nothing builds"
  - Files: `src/palette.ts`, `src/seha.ts`, `scripts/check-design.mjs`
  - Verify: `npm run check` exits 0 on the commit that lands the tokens
- [ ] **T3 (P1, human: ~2h / CC: ~10min)** — dashboard.ts — add `moSkeleton(5)` to `#kmon`
  - Surfaced by: Pass 2 — verified live: blank body at 1.5s, content at 6s, no skeleton, no spinner
  - Files: `src/dashboard.ts` (anchored replacements only, ADR-0001)
  - Verify: throttle to Slow 3G; the campaign list shows five skeleton rows, never a blank body
- [ ] **T4 (P1, human: ~1h / CC: ~5min)** — smoke.py — replace the `#kmon` landmark with a body-scoped assertion
  - Surfaced by: Pass 2 — «الحملات» appears in the rail and the breadcrumb, so smoke is green on a blank page
  - Files: `massar-engine/scripts/smoke.py`
  - Verify: temporarily stub the campaigns fetch; smoke must go red
- [ ] **T5 (P1, human: ~3d / CC: ~1 session)** — dashboard shell — rail, top bar, greeting, hero tile, KPI row (variant B)
  - Surfaced by: Pass 1 — "nothing leads" on the current home; two primaries compete
  - Files: `src/dashboard.ts`, `src/crm-primitives.ts`
  - Verify: `npm run smoke`; one primary button per screen; hero figure at `--t-num`
- [ ] **T6 (P1, human: ~3d / CC: ~1 session)** — leads page — table grammar, seriousness meter, momentum pill, opt-out row (variant E)
  - Surfaced by: Pass 1 — the reference's placeholder `35%` replaced by `signal-domain.ts` output
  - Files: `src/customers-crm.ts`, `src/crm-primitives.ts`
  - Verify: `npm run qa:scale`; the opt-out row renders its reason in words and its send control is `aria-disabled`
- [ ] **T7 (P2, human: ~1d / CC: ~20min)** — the interaction-state table, implemented across all eight surfaces
  - Surfaced by: Pass 2 — the state table
  - Files: `src/dashboard.ts`, `src/customers-crm.ts`, `src/campaigns-crm.ts`, `src/opps-crm.ts`
  - Verify: every surface named in §4 shows a named empty state; zero denominators render «—»
- [ ] **T8 (P2, human: ~4h / CC: ~10min)** — status pill width reserve
  - Surfaced by: Pass 6 / variant D — «ردّ لم يُجَب» and «بلا خطوة» wrap to two lines, interior.dev failure 1
  - Files: `src/crm-primitives.ts`
  - Verify: measure the longest label in each pill family; the control never resizes between states
- [ ] **T9 (P2, human: ~4h / CC: ~10min)** — 44px coarse-pointer targets on the new table's row actions
  - Surfaced by: Pass 6 — 32px visual buttons; the subnav is already one pixel short at 43px
  - Files: `src/crm-primitives.ts`, `src/dashboard.ts`
  - Verify: `pointer:coarse` emulation at 375px; every action ≥44×44
- [ ] **T10 (P2, human: ~2h / CC: ~10min)** — bidi isolation on the new surfaces
  - Surfaced by: Pass 6 / variant E — `(HIS/ERP)` split from its Arabic label across a line break
  - Files: `src/customers-crm.ts`, `src/opps-crm.ts`
  - Verify: `npm run check:numerals`; every Latin run wrapped, numeric columns `dir="ltr"`
- [ ] **T11 (P3, human: ~1d / CC: ~20min)** — three-breakpoint layouts per the Pass 6 table
  - Surfaced by: Pass 6
  - Files: `src/dashboard.ts`
  - Verify: screenshots at 1440×900, 900×1200, 375×812; the leads table becomes cards at `--bp-sm`

---

## GSTACK REVIEW REPORT

| Run | Skill | Status | Findings |
|---|---|---|---|
| 1 | `/plan-design-review` (7 passes) | complete | 11 tasks, 6 unresolved decisions, 3 self-caught palette defects |
| 2 | Live-app verification (`$B` against production) | complete | 2 runtime defects: `#kmon` blank body ≈5s; smoke landmark cannot fail |
| 3 | Contrast measurement (26 token pairs) | complete | 3 failures caught pre-draft: C-1 3.86:1, C-2 2.93:1, C-3 1.29:1 |
| 4 | gstack designer (image mockups) | **unavailable** | `OpenAI organization verification required` — fell back to hand-authored HTML in the production medium |
| 5 | Design outside voices (Codex + subagent) | **not run** | Skipped per the founder's standing instruction on question budget; the passes ran in full |

**Pass ratings:** IA 3→9 · Interaction states 1→9 · Journey 2→8 · AI slop 4→8 · Design system 2→9 ·
Responsive/a11y 1→9 · Unresolved decisions surfaced, not closed.

**Prior learning applied:** `blue-focus-ring-on-blue-primary-button` (10/10, 2026-09-06) — the violet
ramp ships with the ring inversion and a dedicated `-mark` token, so the 1.00:1 focus failure and the
2.93:1 dot failure cannot repeat. `dashboard-home-is-on-a-5-second-poll` (10/10, 2026-09-04) — raised
as blocking decision U-4.

**VERDICT: APPROVED TO BUILD, with three decisions blocking the hero tile and the stage column.**
The shell, the token rewrite, the leads table, and the two runtime fixes (T1-T6, T8-T10) are
unblocked and can start now. T5's hero figure and T6's stage column wait on U-2 and U-3.

**UNRESOLVED DECISIONS:**
- U-2 — the target basis (bookings / ACV / TCV) is undecided, and this design makes that number the largest element on the home screen
- U-3 — `opps-domain.ts` carries six stages, «المستهدفات والأداء» ships eight; two are unreachable and both new screens read that list
- U-4 — `#home` polls every 5 seconds; a DB-backed work queue makes that 48 queries a minute per open tab on the machine that also serves the Gupshup webhook
