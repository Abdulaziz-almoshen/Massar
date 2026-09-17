# DESIGN.md — Massar design system

**The system is `massar-ds/ms.css`. This file explains it and states its rules.**
The reference implementation is `massar-ds/home.html`.

> **Status: PROPOSED, awaiting the founder's approval.** The previous system was retired on
> Sep 16 2026 and archived at `docs/designs/archive/DESIGN-v4-tonomo-retired-20260916.md`
> (with its `approved.json`). Nothing in `massar-engine/src/` has been migrated yet.

---

## 0. Why the last system was replaced

The retired `DESIGN.md` was 796 lines and constrained **values** — colour, radius, type,
shadow, motion — and enforced them with `scripts/check-design.mjs`. It never constrained
**components**. So every screen invented its own. Measured in `massar-engine/src/` the day it
was retired:

| | |
| --- | --- |
| CSS class definitions | **2,765** |
| Distinct class prefixes (`ox-`, `px-`, `rx-`, `cf-`, `crm-`, `hm-`, `yt-`…) | **28** |
| Different classes that draw a **card** | **39** |
| Different classes that draw a **row** | **35** |

`ox-` alone carried 196 definitions. That is not one system across twelve screens; it is twelve
private systems that share a blue. Every attempted fix was a CSS override forcing 39 unrelated
card classes to *look* alike (`revamp.ts` §8), which papers over the missing component layer and
can never converge. The accent was also rebranded four times in ten days — teal `#1F7A73` →
Seha blue `#306DB5` → violet → Tonomo blue `#2563EB` — each time chasing the reference site most
recently in view. A palette that changes weekly is a mood board.

**The correction: constrain components, not values.** Values follow from components.

---

## 1. The rule

> A screen may not define a class that draws a surface, a row, a figure, a bar, a chip, a button
> or an empty state. It **composes** the primitives in `ms.css`.
>
> If a screen needs something `ms.css` cannot express, the fix is a **new variant in `ms.css`**,
> decided once — never a private class in the screen.

Two mechanisms keep this true:

1. **The falsifiable test.** `massar-ds/home.html` contains **no `<style>` block and no bespoke
   CSS**. The only inline styles are the primitives' documented parameters (`--ms-cols` on a row
   or table, `--ms-pct` on a bar). If a screen cannot be built this way, the system is missing a
   primitive and must gain one before that screen ships.
2. **The gate.** `scripts/check-components.mjs` (to be written with the migration) fails the
   build when a `*-crm.ts` module defines a class matching the surface/row/figure/bar/chip/button
   shapes. Same enforcement posture as `check-design.mjs`, aimed one level up.

---

## 2. The primitives

Thirteen. Each implemented **once**, in `ms.css`, with variants as modifiers (`ms-card--dark`),
never as new base classes.

| Primitive | What it is | Variants |
| --- | --- | --- |
| `ms-n` | **Every numeral in the product.** Western digits, `tabular-nums`, LTR-isolated | — |
| `ms-shell` / `ms-main` / `ms-rail` | Page frame and navigation rail | — |
| `ms-head` / `ms-sec` | Page title block; a titled region | — |
| `ms-card` | **The one surface** | `--lead` `--flat` `--dark` `--band` `--pad0` |
| `ms-split` | Hairline-divided grid of stats | `--2` `--3` `--4` `--bare` |
| `ms-stat` | **The only way to print a labelled number** | `--hero` `--sm` `--nil` |
| `ms-row` | **The one list row** | `--link` |
| `ms-thead` | Column heads for a row table | — |
| `ms-bar` | A measure | `__fill` (booked) `__open` (weighted) `--sm` |
| `ms-chip` | Status / badge | `--ok` `--warn` `--bad` `--info` `--plain` |
| `ms-btn` | Button | `--primary` `--quiet` `[disabled]` |
| `ms-empty` | **The empty state, as a designed component** | `ms-nil` (inline) |
| `ms-chart` | SVG conventions (not a chart library) | `__target` `__actual` `__proj` `__now` |

Rows and tables are **configured, not redefined**: a screen sets `--ms-cols` on the container.
That is the whole API. `2,765` classes collapse to roughly `150`.

### The empty state is a first-class primitive

Massar's real data is mostly empty — on the day this was written the year's target was 34,000 SAR,
achieved 0, with zero won deals and five of six products carrying no target. **The near-empty
state is the default state, not an edge case.** `ms-empty` always says three things: what is
missing, why it matters, and the one action that fixes it. A bare `—` with no reason is a defect.

### Zero recedes

`ms-stat--nil` and `ms-row__v--nil` drop a zero figure to `--ms-idle-mark`. A zero is a
consequence, not news; it must not be the loudest thing on the screen. The retired home page spent
its largest element — a 96px `0` in an arc ring reading `0%` — restating a fact the pipeline
section already explained. That single choice is what "lame" meant across five rejections.

---

## 3. Tokens

Read them from `ms.css` §1; they are not repeated here, so the two can never drift. What matters
is the **discipline**, which is new:

- **Four ink levels** (`--ms-ink`, `--ms-ink-2`, `--ms-mut`, `--ms-fig`) and four grounds. `--ms-fig`
  is for figures only and never for body text.
- **Seven type roles named by job**, not eight sizes to choose from: `micro / cap / body / sub /
  head / fig / hero`. The old ladder had eight sizes and **108 of 140 strings on home landed on
  the smallest one**, which is precisely why every screen read as uniform mush with nowhere for
  the eye to land.
- **One elevation** (`--ms-lift`), one ring, one well. A second elevation is a decision, not a
  default.
- **One easing curve** (`--ms-ease: cubic-bezier(.16,1,.3,1)`), with duration carrying the meaning:
  `press 120ms / swap 180ms / enter 250ms / exit 150ms`. A second curve (`--ms-move`) exists only
  for on-screen movement.
- **One accent**, four stops. `#2563EB` is retained — it was never what the founder objected to.

### Colour is never the only channel

Every tone chip carries a dot as well as a hue (`.ms-chip::before`). Every status prints its label.
This survived from the retired system unchanged and is non-negotiable.

---

## 4. Motion

Governed by the `emil-design-eng` framework, which is mandatory on every Massar design run
(`CLAUDE.md` §4). The binding rules:

- **Ask whether it should animate at all.** Anything a user triggers dozens of times a day gets no
  animation. Never animate a keyboard-initiated action.
- **Never `ease-in`** on UI. Enter with `--ms-ease`; move with `--ms-move`.
- **Exit faster than enter** (150ms vs 250ms).
- **`scale(.97)` press feedback** on every pressable control, at 120ms.
- **Never enter from `scale(0)`.** Nothing in the world appears from nothing.
- **Every hover effect sits behind** `@media (hover:hover) and (pointer:fine)`. A control that
  appears only on hover does not exist on a touch device — so `ms-row__go` is always visible and
  only its ink deepens.
- **`prefers-reduced-motion`** collapses every duration to 1ms, globally, in `ms.css`.

---

## 5. RTL is structural, not a coat of paint

`ms.css` contains **no `left` or `right` property anywhere** — logical properties only
(`inset-inline-start`, `margin-block-end`, `padding-inline`). Arabic is the primary direction, not
a mirror of an English layout.

**Time runs right to left.** On `ms-chart`, January sits at the right edge and December at the
left. Getting this backwards is the most common RTL chart defect.

**Numerals are western** (`0123456789`), per the founder's standing instruction. `ms-n` makes this
structural: every number goes through one class that isolates direction and forces tabular figures,
so it cannot be forgotten per-screen.

**Counted nouns follow Arabic grammar** — `pluralizeArabic` / `opPl`, four-way
(مفرد / مثنى / جمع القلة / تمييز), never `n + noun`.

---

## 6. The references

The founder's standing reference set, given Sep 16 2026. Full notes on what to mine from each:
`docs/designs/ui-component-references.md`.

| Site | Mine it for |
| --- | --- |
| <https://libraries.dev> · [/metal](https://libraries.dev/metal) | Interactive effects; the real-time liquid-metal shader (`metal-fx`, Paper Shaders) |
| <https://transitions.dev> | Transitions and micro-interactions; the easing vocabulary |
| <https://astryx.atmeta.com> | 170+ React components; component API shapes |
| <https://beui.dev> | Animated Motion components. **Charts**, Number Animation, Tabs, Dock, Command Palette, Metallic Button |
| <https://coss.com/ui> | Clean accessible primitives; focus behaviour |
| <https://originkit.dev> | Interaction polish |
| <https://kinetics.colorion.co> | Physics motion; spring configurations |
| <https://21st.dev> | Dashboard layouts; `line-charts-8` (monotone-cubic curve, dashed reference line) |
| <https://www.beautifului.dev> | Card/edge grammar: ring-in-box-shadow, multi-stop shadows, concentric radii |

**Measure them, never recall them.** Open the page and read `getComputedStyle`. What this system
took, with provenance:

- **The digit ticker is CSS-only** — `beui.dev/components/motion/number`: a `1ch`-wide, `1.1em`-tall
  `overflow:hidden` slot over a stacked column of `0..9`, moved by
  `translateY(calc(-1 * var(--d) * 1.1em))` at `.9s cubic-bezier(.16,1,.3,1)` with a
  `var(--i) * .04s` per-column stagger. No library, and western numerals come free because the
  column literally contains the glyphs. Available for any figure that animates to a new value.
- **`width:1ch` + `tabular-nums`** is the whole trick for a figure that must not reflow. It is
  baked into `ms-n`.
- **Over-damp a gliding indicator** — beUI's tab indicator uses spring `170/30/1.2`, deliberately
  *not* their standard layout spring, because overshoot inside a scrollable rail causes a transient
  scrollbar and a layout shift.
- **One curve, many durations** — effectively everything on beui.dev uses
  `cubic-bezier(.16,1,.3,1)`. This system adopted that discipline over the retired file's three
  named curves.

### One reference deliberately *not* followed

beui.dev has **no elevation shadow system at all**: four `box-shadow` declarations on the whole
page, every one transparent, with surfaces separated by a single `rgba(255,255,255,.05)` hairline.
That grammar is **dark-mode-native** and goes weak on a white ground, which is what Massar uses by
the founder's instruction. So `ms.css` commits to ring + soft multi-stop shadow instead. Both are
internally consistent; **mixing them is what produces the generic look.** Recorded here so the
decision is not silently re-litigated.

---

## 7. Correctness rules that outrank taste

Carried forward from the retired system unchanged — these were never the problem.

1. **Measured contrast floors.** Body text ≥ 4.5:1 on its actual ground; a mark ≥ 3:1. An exemption
   must name the exact ground **and** carry its measured ratio, and the gate must re-derive it.
2. **Colour is never the only channel** (§3).
3. **A table a screen reads must have a writer** shipped in the same change
   (`check-ledger-writers.mjs`).
4. **Every emitted value must be readable back** — buttons, markers and filtered strings pair in
   one table, asserted at boot.
5. **A figure on screen is earned from the ledger**, never produced by a model.
6. **`src/dashboard.ts`: anchored string replacements only**, never range edits.
7. **No backticks inside `*-crm.ts` / `revamp.ts` / `dashboard.ts` template literals**, comments
   included.

---

## 8. Migration, not yet started

Nothing in `massar-engine/src/` uses `ms.css` yet. The order, once the founder approves the
direction:

1. Approve `massar-ds/home.html` as the reference screen.
2. Inject `ms.css` into `dashboard.ts` alongside the existing CSS (both live; no screen changes).
3. Rebuild `#home` from the primitives. Delete `hm-*` and the home half of `revamp.ts`.
4. Write `scripts/check-components.mjs` and turn it on for `#home` only.
5. Migrate the remaining screens one at a time, widening the gate's scope each time. `ox-` (196
   definitions) is the largest and goes last.
6. Delete `revamp.ts` §8 — the override layer exists only to hide the missing component layer, and
   has no reason to survive this.

---

## 9. Maintenance

`ms.css` is the source of truth; this file explains it. When they disagree, `ms.css` wins and this
file is wrong. Update both in the same change. A new variant is a decision worth one line of
rationale in the CSS comment where it lives — that is where the next person will look.
