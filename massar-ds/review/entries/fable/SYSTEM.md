# مسار — the ledger system

Rules, not adjectives. Every value below is the value in the `<style>` block that `home.html` and
`ledger.html` share byte-for-byte (they are assembled from one stylesheet; a screen never carries CSS
of its own). Where a value was measured, the method and the number are stated. Where it was decided,
it says "decided".

---

## 0. The one rule

> **A figure is a ledger line: label · figure · basis.** Nothing on any screen prints a number
> without, on the same line, the records that produced it. If the records cannot produce the number,
> the cell prints the *kind* of empty it is — never a dash, never a zero standing in for null.

Everything else follows from this. The home page is not a dashboard; it is the top of the ledger.
The table is not a view of the data; it is the data, ruled.

Two mechanisms keep it true at runtime, not in a document:

1. **`[data-d="key"]`** marks every printed figure. Each page carries its records as a plain object
   and a script that re-derives every key from them; a printed figure that disagrees with its
   derivation is outlined in the accent (`.is-off`) and logged. A page with an empty console is a
   page whose summaries cannot contradict their tables.
2. **Ranges, sums and counts are never typed.** `3–24`, `4,200`, `5 من 6` are derived in the
   script and asserted against the markup.

---

## 1. Direction

- `dir="rtl"` on `<html>`. **No `left`, no `right`, anywhere** — `inset-inline-start`, `margin-inline`,
  `padding-block`, `border-inline-end`, `text-align:start|end`. The delivered files were grepped: the
  only match is the comment that states this rule.
- **Time runs right to left.** The quarter strip puts 1 July at `inline-start` (the right edge) and
  30 September at `inline-end`; the "today" marker is positioned with `inset-inline-start: 85.9%`
  (day 79 of 92).
- **Every bar fills from `inset-inline-start: 0`**, so a measure grows leftward.
- **Numerals are western**, through one class:

  ```css
  .n { direction:ltr; unicode-bidi:isolate; display:inline-block;
       font-variant-numeric:lining-nums tabular-nums; font-feature-settings:"tnum" 1,"lnum" 1; }
  ```
  A currency or unit that belongs to the number goes **inside** the isolate:
  `<span class="n">4,200 ر.س</span>`. A counted noun goes **outside**: `<span class="n">6</span> بنود`.
- **Counted nouns are four-way.** The forms used in the two screens:

  | n | form | used |
  | --- | --- | --- |
  | 1 | مفرد | بند واحد · منتج واحد · مستهدف واحد |
  | 2 | مثنى | مهتمّان · بندان |
  | 3–10 | جمع القلة، مجرور | 6 بنود · 5 بنود · 7 منتجات · 8 منتجات · 3 أقسام · 9 أيام · 3 أيام · 4 منتجات |
  | 11+ | مفرد منصوب (تمييز) | 16 عميلًا · 13 يومًا · 24 يومًا · 21 مستلمًا · 21 رسالة |

---

## 2. Colour — one accent, four grounds, three inks

Colour means status. The **only chromatic value in the system** is the accent, and it means one
thing: *selling is blocked here and a person must act* (an unpriced line; a product the assistant
will not sell). Navigation, focus, selection, headings and all charts are ink.

| token | value | role |
| --- | --- | --- |
| `--paper` | `#FFFFFF` | the sheet |
| `--page` | `#F4F3EF` | the desk under the sheet; hover ground |
| `--sunk` | `#ECEAE4` | an empty field; the track of every bar |
| `--line` | `#E3E1DA` | every rule |
| `--line-2` | `#BDB9AE` | the ring of a null; the underline of an owed classification |
| `--ink` | `#1A1917` | figures, titles, the current door |
| `--ink-2` | `#45433E` | body, bases |
| `--mut` | `#6B6860` | labels, column heads, dates, true zeros |
| `--ac` | `#B7371A` | the accent |
| `--ac-dim` / `--ac-line` | `#FBEBE5` / `#EBB9A9` | reserved; unused on these two screens |

**Measured contrast** (WCAG relative luminance, computed by script, not estimated):

| pair | ratio |
| --- | --- |
| `--ink` on `--paper` | 17.57 |
| `--ink-2` on `--paper` | 9.88 |
| `--mut` on `--paper` | 5.56 |
| `--mut` on `--page` | 5.01 |
| `--mut` on `--sunk` (the floor: a label inside an empty field) | **4.63** |
| `--ac` on `--paper` | 5.87 |
| `--ac` on `--sunk` | 4.88 |
| white on `--ac` | 5.87 |

No text token lands under 4.5:1 on any ground it can occupy. There is no exemption list.

Zero recedes: a printed `0` figure takes `.quiet` (`--mut`, weight 500). It is a consequence, not
news, and it must never be the loudest thing on the sheet.

---

## 3. Type — seven roles, each with a job

Face: **IBM Plex Sans Arabic** 400/500/600/700, fallback `"Noto Sans Arabic", system-ui, sans-serif`.
Chosen for tabular figures and a narrow Arabic body that holds 13px in a 40px row. Decided, not
measured against a reference.

| role | size / leading | exists because |
| --- | --- | --- |
| `micro` | 12 / 16 | column heads, axis labels, the sub-line under an account name. The smallest ink that still clears 4.5:1 in `--mut`. |
| `cell` | 13 / 18 | **the base.** A ledger cell. The densest surface sets the size everything else is measured from. |
| `body` | 14 / 20 | controls, labels beside a figure, the page summary line. One step up so it never competes with a cell. |
| `sub` | 16 / 22 | a sheet title; a row title. The first size the eye can land on across a room. |
| `fig` | 20 / 24, 600, -0.01em | a figure inside a row (the blockers ledger). Large enough to read as a number before the label is read. |
| `head` | 32 / 36, 600, -0.02em | a figure at statement level (collected, priced); the page title. |
| `lead` | `clamp(56px, 5.2vw, 76px)` / 1, 600, -0.03em | **the one leading figure per screen.** 76px at 1440, 56px at 400. It is larger than any chrome on the page by construction: the top bar is 48px. |

Tracking tightens as size grows (0 → -0.03em) because Plex's Latin digits set loose above 32px.
Letter-spacing is never applied to Arabic text.

---

## 4. Space and rhythm

4px base: `--s1 4 · --s2 8 · --s3 12 · --s4 16 · --s5 24 · --s6 32 · --s7 48`.

Fixed heights so an empty cell never changes a row's height:
`--row 40px` (ledger row) · `--ctl 32px` (button, segment) · column head `36px` · top bar `48px`.

One radius: `--r 4px`. Chips and the null ring are `999px`. One ring: `0 0 0 1px var(--line)`.
One shadow, used once (the basis popover): `0 8px 24px rgb(26 25 23 / 8%)` over the ring.
Focus: `0 0 0 2px paper, 0 0 0 4px ink` — ink, never accent, because accent means status.

Page: `max-inline-size: 1280px`, `padding-inline: 24px` (16px under 720px). Side gutter never
drops below 16px.

---

## 5. The six empties

Each is one word-form and one drawing, defined once as `.nil--*`. They differ on two axes at once —
**who owes what**, and **how it is drawn** — so they are never confused by colour alone.

| # | phrase | meaning | class | drawing |
| --- | --- | --- | --- | --- |
| 1 | **لم يُسعَّر** | a line exists; its price was never entered | `.nil--price` | accent, 600, dotted accent underline. The only accented empty: it is money someone owes. |
| 2 | **لم يُصنَّف** | a thing exists; its class was never chosen | `.nil--sector` | `--ink-2`, dotted `--line-2` underline |
| 3 | **لم تُسجَّل** | a record that should exist was never written (account ownership; the opportunity a «مهتم» should have become) | `.nil--rec` | `--ink-2` on a `--sunk` field with an inset 1px ring: an unfilled form field |
| 4 | **لا بنود مفتوحة** | a true zero; nothing is owed | `.nil--none` | `--mut`, nothing drawn. Also carries «لا يُحسب», «لا صفقة رابحة», «لا صفقة خاسرة». |
| 5 | **بلا مستهدف** | the schema's `null` — a target that was never recorded, which is not zero | `.nil--null` | `--ink-2` inside a hollow `--line-2` ring: a slot with nothing in it |
| 6 | **لا سعر منشور** | the product publishes no price statement at all (a basis such as «يحدده المختص» is not this) | `.nil--unpub` | `--ink-2`, dashed `--line-2` underline: the publisher owes a statement |

A seventh mark, `.mark--inf` («مُستنتَج», dashed box), is not an empty: it flags a value that exists
but was inferred rather than recorded.

---

## 6. Component vocabulary

Fourteen classes draw everything on both screens. A screen composes them and sets nothing else.

| class | what it is | parameters |
| --- | --- | --- |
| `.top` / `.mark` / `.doors` / `.asof` | 48px bar: wordmark, seven doors as text, the as-of date. No avatar, no search field. | `aria-current="page"` on one door |
| `.sheet` / `.sheet__h` / `.sheet__t` / `.sheet__m` | the one surface, with a ruled head | `--end` pushes a meta to the far edge |
| `.stmt` / `.stmt__row` / `.stmt__k` / `.stmt__v` / `.stmt__basis` | the statement: label · figure · basis, ruled | `--lead` on the row that carries the leading figure |
| `.figbtn` + `.basis` | a figure that opens the records behind it | `aria-expanded`, `aria-controls` |
| `.strip` / `.track` / `.track__fill` / `.track__tick` / `.track__now` / `.axis` | a measure drawn: a track, a fill, a tick, a now-marker, end labels | `--pct` (fill), `--at` (position) |
| `.ledg` / `.ledg__r` / `.ledg__f` / `.ledg__l` / `.ledg__b` / `.door` | the blockers ledger: figure · label · basis · door | — |
| `.cells` | n of m drawn as m cells | `.on` per filled cell |
| `.bars` | counts of one cohort drawn as bars; no rate printed | `--pct` per bar = count / cohort |
| `.nil--*` / `.mark--inf` / `.stop` | the six empties, the inferred mark, the stop | — |
| `.seg` / `.btn` / `.btn--ink` / `.toolbar` | segmented control, button, the one filled button | `aria-pressed` |
| `.ph` / `.ph__sum` / `.dotsep` | page head with a derived summary line | — |
| `.tw` / `.tbl` | the table | `th[aria-sort]`, `td[data-th]` for the 400px card form, `.num`, `.who`, `.val`, `.idx`, `.date`, `.act` |
| `.stage` / `.stage__t` | stage name + six cells, only the cell the line stands in filled (no earlier stage is implied) | `.on` |
| `.days` | days without a stage change: the number, and the same number drawn to the range max | `--pct` = days / max |
| `.board` / `.col` / `.card` | the same records by stage; eight columns; an empty column says which empty it is | — |
| `.view` / `.pane` | two readings of one set of records, crossfaded | `hidden`, `data-away` |

**The 400px table** is the same `<table>`: `thead` hidden, each `tr` a two-column grid, each cell
labelled by `td::before { content: attr(data-th) }`. Account and product span both columns. No
second markup for mobile.

---

## 7. Motion

One curve: `--ease: cubic-bezier(.22, 1, .36, 1)` — easeOutQuint as published on easings.net.
Duration carries the meaning:

| token | ms | used for |
| --- | --- | --- |
| `--press` | 100 | `transform: scale(.97)` on `:active` of every pressable: button, segment, door, card, row link, figure |
| `--out` | 120 | anything leaving: a pane, a filtered row, a basis popover |
| `--in` | 180 | anything arriving: opacity 0→1 with `translateY(4px)` (pane) or `translateY(-4px) scale(.98)` (popover, `transform-origin: 50% 0`) |

Nothing exceeds 180ms. Nothing enters from `scale(0)`. Only `opacity`, `transform`, `background-color`
and `color` are transitioned; never `all`, never a layout property. Filtering fades rows; the table
never animates its layout.

**No animation at all** on sort (a keyboard act repeated all day), on navigation, on the as-of date.
The gliding indicator, the animated number and the stagger were considered and rejected: the
founder opens this page tens of times a day.

Hover exists only behind `@media (hover:hover) and (pointer:fine)`, and only as a ground change to
`--page` or an ink deepening. No control appears on hover.

`prefers-reduced-motion: reduce`: every transition collapses to `--out` (120ms) and every transform
in an entering, leaving or pressed state is set to `none` — opacity and colour still cross-fade,
movement is removed. Reduced motion is fewer and gentler, not zero.

---

## 8. Provenance

| value | source |
| --- | --- |
| contrast ratios in §2 | computed from the hex values by script (sRGB → relative luminance → (L1+.05)/(L2+.05)) |
| `cubic-bezier(.22,1,.36,1)` | easings.net, easeOutQuint |
| 100 / 120 / 180ms, `scale(.97)`, hover gate, reduced-motion | the brief's motion constraint |
| `tabular-nums` + `1ch` slots for figures that must not reflow | the project's own reference pass on beui.dev (DESIGN.md §6, 16 Sep 2026). Read from the record, not re-measured here. |
| row 40 / control 32 / head 36 / bar 48 | decided |
| Q3 marker at 85.9%, priced tick at 12.35%, campaign bars at count/21, days bars at days/24 | arithmetic on the records, stated inline where drawn |
