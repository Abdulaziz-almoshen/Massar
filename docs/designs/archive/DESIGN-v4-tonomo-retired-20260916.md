# DESIGN.md — Massar token authority

**Read this before writing any UI code. These tokens override newly invented values.**

> **REBRAND V4 — THE TONOMO BLUE, 2026-09-08.** By founder instruction, the accent moves from the
> V3 violet to a saturated blue (`#2563EB`) on a third chosen reference: the **Tonomo** scheduling
> app. Tonomo is a flat, bordered, tight-radius product, and that is the substance of the change,
> not just the hue: **radii halved** (10/14/20/26 → 6/8/12/16), **shadows retired in favour of a
> `--line` hairline** on every card and panel, **controls compacted** (38px, with the 44px floor
> moved to the coarse-pointer query where §3.10 actually requires it), and the accent surfaces are
> **solid rather than gradient** — Tonomo has no gradients anywhere. Two components came with it:
> the **action row** (a full-width `--accent-bar` control that sits between a primary button and a
> text link) and the **collapsible section header**. Grounds went cooler: the lavender canvas is
> now a neutral `#F6F7F9`.
>
> **1,186 value sites** were remapped. Everything in §3, §4, §6, §7 and §8 is unchanged — this is a
> palette and a geometry, not a new set of rules.
>
> **REBRAND V3 — THE VIOLET SYSTEM, 2026-09-07 (superseded).** By founder instruction, Massar adopts the
> visual language of two chosen references: the **Pillio** healthcare dashboard for the overview
> surfaces (a floating rail, one accent-gradient hero tile, cards on a tinted canvas) and an
> **AI-Manager leads dashboard** for the list surfaces (a real table, outlined status pills,
> per-row quick actions, KPI cards with a delta chip). Both are re-authored for RTL, for Cairo, and
> for ledger density — the references are LTR consumer surfaces and Massar is an Arabic sales
> ledger, so the grammar transferred and the density did not.
>
> **What changed:** the accent moved from Seha blue `#306DB5` to violet `#2563EB`, across 1,164
> value sites in `src/`. Radii grew (8/10/16 → 10/14/20, plus a new `--r-xl:26`). Shadows were
> retuned to a violet-grey and gained a near-flat `--sh-0`. A `--canvas` token was added: the page
> ground is `#F6F7F9` and `--paper` is now the CARD, not the page. `--accent*` aliases were added
> as the forward names; `--blue*` survive as migration aliases so a value remap did not also have
> to be a rename.
>
> **What did NOT change, deliberately:** §3.0 (the measured contrast floor), §3.0b (colour is never
> the only channel), the four-value status contract, §4 in full, and §7. Every pair below was
> re-measured, and `scripts/check-design.mjs` re-derives 17 of them on every build.
>
> **Selection record:** `~/.gstack/projects/Abdulaziz-almoshen-Massar/designs/massar-pillio-20260907/approved.json`.
> **Plan and review:** `docs/designs/massar-ui-transformation.md`.

> **REBRAND, 2026-09-04 (superseded by the above).** This file previously specified a teal accent (`#1F7A73`) over a
> pure-neutral grey ramp with no shadows. It no longer does. By founder instruction, Massar adopts
> the approved Seha design system at
> `~/.gstack/projects/combinedservices/designs/design-system-20260903/preview-v2.html`
> (selection record: that folder's `approved.json`, approved 2026-09-03 after v1 was rejected).
> **Every rule below that carries a colour, radius, shadow, spacing or duration is new. Anything in
> the codebase still using teal, `#171717` ink or `#EDEDED` lines is pre-rebrand and is a migration
> target, not a precedent.** §4 and §7 survived unchanged; §6 survived except rule 4, whose accent
> is now `--blue`. **Spacing changed too and the first version of this banner did not say so:** row
> gutters were 20/12px and are now `--s4`/`--s3` = 24/16px, because 12 and 20 are unrepresentable on
> the new scale. Every list row in the product is 8px wider than before. Migration: `12 → --s3`,
> `20 → --s4`.

---

## 1. Where the brand comes from

The source is a **Seha-native** system: blue, data-as-visual, drawn flat illustration rather than
generated imagery. Its own approval note reads: *"Approved after rejecting v1 (vault/seal/
convergence). Seha-native brand, data-as-visual, seat grid, interior.dev moments, antd kept, hooks
ported to JSX with motion."*

Massar is server-rendered from `src/dashboard.ts`; it does not install antd or React. **The system
is adopted as tokens and behaviour, not as a component dependency.** Where the source ships a React
hook, Massar reads it as a specification and writes the equivalent in plain DOM.

---

## 2. Tokens — copy these, do not re-derive them

### Colour

```
--accent:      #2563EB   primary. The one saturated hue on a surface.   4.86:1 on paper, and
                         white on it is 4.86:1 — legal in BOTH directions.
--accent-press:#1E5FCC   pressed / heavier weight                        5.36:1 on --surface
--accent-deep: #1A47BE   gradient dark stop; badge text on --accent-tint 6.44:1
--accent-mark: #4A7BE8   THE DOT TOKEN                        3.54:1 on --surface, 4.07:1 on paper
--accent-tint: #EAF1FE   selected row, quiet fill
--accent-wash: #F2F6FE   row hover
--accent-bar:      #EAF1FE   the ACTION ROW ground (see §5). Same value as --accent-tint, named
                             separately because the tint is a state and the bar is a control.
--accent-bar-hover:#DCE8FC   the action row, hovered

Migration aliases, one cycle. New code uses --accent*; these exist so a 1,186-site value remap
did not also have to be a rename:
--blue:            #2563EB
--blue-deep:       #1E5FCC
--blue-light:      #5B8DEF   decorative ONLY — white on it is 3.23:1, and as a mark on --surface
                             it is 2.86:1. Never a text ground, never a dot.
--blue-tint:       #EAF1FE
--blue-wash:       #DCE8FC

--grad:        linear-gradient(270deg,#1A47BE,#2563EB)
--wash:        linear-gradient(180deg,#EAF1FE,#FFFFFF)

--canvas:      #F6F7F9   THE PAGE GROUND. Cards sit on this.
--paper:       #FFFFFF   the CARD, not the page
--surface:     #EFF1F5   strips, quiet tiles, nested row grounds
--surface-2:   #E5E8EE   nested strip
--line:        #D8DCE3   a decorative hairline (1.48:1) — never a control's only affordance
--line-soft:   #ECEEF2   a hairline between rows (1.16:1)
--ink:         #14161A   headings, primary text        18.09:1
--ink-2:       #33373E   body                          12.38:1
--muted:       #656B76   labels, secondary — the lightest ink on paper/canvas/surface
                         5.36 on --paper · 5.00 on --canvas · 4.74 on --surface
                         **4.37 on --surface-2 — FAILS.** Use --muted-2 there.
--muted-2:     #545A66   the same role on --surface-2, the darkest grey ground. 5.64:1.
                         Exists for the reason the -mark tokens do: one value for the harder
                         ground, rather than lightening the ground to suit the ink.
                         --surface-2 is a CONTROL TRACK — the view toggle sits on it — so this
                         was not a corner case. It was sixteen inactive segment labels across
                         six screens, found by measuring every rendered node against its real
                         painted ground instead of an assumed one.
```

**`--grad` is a legal white-text ground at BOTH stops** — 7.60:1 and 4.86:1. This is the one place
the references were not followed: Pillio's own gradient runs to a light violet where white measures
**3.36:1**, which cannot legally carry the small labels the reference puts on it. `#5B8DEF` survives
only as a decorative stop and as `--blue-light`; it is **never a text ground and never a mark on a
tinted row** (2.93:1 on `--surface` — the identical failure this file already retired as
`--s-sched`). That is what `--accent-mark` exists for.

**The greys are deliberately violet-tinted now.** The previous invariant banned exactly this. It is
reversed: `#F4F6F9`, `#CBD7E4`, `#536170` are the system, and a pure-neutral `#EDEDED` line is now
the thing that looks foreign.

### Status

Status colour is a **separate channel from the accent**, with three named exceptions. An earlier
version of this file said the channel "never borrows" the accent, which was false in its own code
block: `--s-attend`, `--s-review` and `--s-sched` are byte-identical to `--blue`, `--blue-deep` and
`--blue-light`. They are drawn in the accent family on purpose — they are states of the system's own
work, not outcomes — and they are **exempt from §3.1 by name**. Every other status hue sits outside
the blue family and may never be substituted for the accent, nor the accent for it.

**Every status has four values.** A status without all four is not a status, it is a colour.

```
                   MARK (dot/bar, >=3:1)   FILL           SOFT (badge ground)   TEXT (on soft)
issued / good      --s-issued:#1E9E63      (same)         --s-issued-soft:#E4F5EC  --s-issued-text:#12633F
failed / bad       --s-fail:#D9534F        (same)         --s-fail-soft:#FBE7E6    --s-fail-text:#8E2A27
attention / warn   --s-attn-mark:#B37F00   --s-attn:#D99A00  --s-attn-soft:#FFF5D6 --s-attn-text:#7A5600
scheduled          --s-sched-mark:#4A7BE8  --s-sched:#5B8DEF --s-sched-soft:#E9F0FE --s-sched-text:#1A47BE
under review       --s-review:#1E5FCC      (same)         --s-review-soft:#E7EEFB  --s-review-text:#173FA8
attending          --s-attend:#2563EB      (same)         --s-attend-soft:#EAF1FE  --s-attend-text:#1A47BE
off / inactive     --s-off-mark:#767D89    --s-off:#A2A9B4   --s-off-soft:#EEF0F3  --s-off-text:#464C56
--s-attn-deep:#B37F00   (retained alias of --s-attn-mark)
```

**MARK vs FILL is the whole point, and the V3 rebrand changed WHERE it bites.** `--s-attn`
(2.45:1) and `--s-off` (2.21:1) are still below the 3:1 non-text floor on `--paper`, so as a status
DOT they are invisible to a low-vision reader. `--s-sched` is the one that moved: at the old blue it
measured 2.93:1 on paper and failed there, and at `#5B8DEF` it measures **3.36:1 on `--paper` and
passes** — but **2.93:1 on `--surface`**, which is the ground a status dot actually sits on inside a
tinted row. **Do not read that as the mark token being redundant.** A mark must clear 3:1 against
*every* ground it can land on, and the tinted row is the one that fails. The `-mark` values exist
for dots, bars and chart marks; the base values remain the founder-approved fills, used where the
area is large. No approved colour was changed to fix this.

The `-soft` fill is a **badge ground**; the `-text` is the only legal label on it. Never put a base
`--s-*` on its own `-soft` — the off badge at `--s-off` on `--s-off-soft` is 1.86:1.

### Type

**Cairo**, unchanged from before and unchanged by the rebrand — loaded as the variable face
`wght@200..1000` so it holds intermediate weights natively.

```
--t-xs:12px  --t-sm:14px  --t-md:16px  --t-lg:18px  --t-xl:22px  --t-2xl:28px  --t-3xl:40px
--t-num:44px   the one big figure on a screen — a ladder member, not an exception

--lh-tight:1.3    headings, --t-xl and above
--lh-body:1.45    the default for all Arabic body and label text
--lh-loose:1.7    running prose only (KB answers, agent transcripts)

--w-body:450   --w-med:500   --w-semi:600
```

The first version of this rebrand dropped the base size, the line-height, the weight ladder and the
"weight 700 is retired" rule that the pre-rebrand file carried. It boasted that Cairo is loaded
`wght@200..1000` "so it holds intermediate weights natively" and then named **zero weights**. The
result is measurable: `src/` currently runs **26 distinct font sizes** (11.5px used 103 times,
12.5px 88 times, 10.5px 33 times — none on the ladder), seven different line-heights, and **129**
uses of `font-weight:700`. Restored and made enforceable:

- Base is `--t-sm` (14px) at `--w-body` (450) and `--lh-body` (1.45). Every other size is a
  deliberate step off it.
- **Weight 700 is retired** — from list rows, tables, badges, labels and buttons. It survives only
  on `--t-num` and `--t-3xl`. Three weights is the ladder; a fourth needs an entry here first.
- `letter-spacing: 0` on all Arabic. `0.02em` is for Latin/LTR spans only.
- **Off-ladder sizes are forbidden**, exactly as off-scale radii are (§3.5).
- Migration map: `9.5/10.5/11/11.5 → --t-xs` · `12/12.5 → --t-xs` · `13/13.5 → --t-sm` (labels take
  xs, content takes sm) · `14/14.5/15/15.5 → --t-sm` · `16/17 → --t-md` · `18/19 → --t-lg` ·
  `21/24 → --t-xl` · `26/30 → --t-2xl`.
- `--muted` (`#536170`, 6.34:1) is the lightest text token. Anything lighter is a decorative icon or
  a placeholder, and is subject to §3.0b.

### Space, radius, shadow

```
--s1:4  --s2:8  --s3:16  --s4:24  --s5:32  --s6:48  --s7:64      (px)
--r-none:0  --r-sm:6  --r-md:8  --r-lg:12  --r-xl:16  --r-pill:999

--z-base:0  --z-sticky:100  --z-dropdown:200  --z-overlay:300
--z-modal:310  --z-toast:400  --z-tooltip:500

--bp-sm:560px   phone — /rep, single column
--bp-md:900px   tablet — the rail collapses to icons
--bp-lg:1280px  desktop — the design target
--content-max:1180px

--i-sm:16px  --i-md:20px  --i-lg:24px    icon stroke 1.5px, currentColor
--skeleton:#E5E8EE   --skeleton-hi:#EFF1F5
--sh-0: 0 1px 2px rgba(16,24,40,.04)                      barely there; most surfaces use --line
--sh-1: 0 1px 3px rgba(16,24,40,.08)                      a raised control
--sh-2: 0 6px 20px rgba(16,24,40,.10)                     a floating surface: menu, sheet, toast

**Shadows are nearly retired.** V4 separates with a `--line` hairline, the way the reference does.
A card is `1px solid --line` with NO shadow; `--sh-2` is for things that genuinely float above the
page. A shadow used where a border would do is the V3 look, not this one.
--sh-3: 0 3px 6px -4px rgba(16,24,40,.10),
        0 8px 20px rgba(16,24,40,.10),
        0 12px 32px 8px rgba(16,24,40,.06)                hover / floating
```

`--r-none` exists because §3.5 forbids off-scale radii and §3.6 requires a flush list — zero was
off the scale, so the rule and the component contradicted each other. A flush list wrapper is
`--r-none`; a row never carries a radius of its own.

**No integer `z-index` may appear in `src/`.** There are eleven today (1, 5, 20, 30, 60, 69, 70, 99,
120, 140, 200). A surface that needs to sit between two steps is telling you it belongs at one of
them. **Three breakpoints**, `max-width` queries; `src/` currently carries 25 ad-hoc widths and they
are migration targets.

**Shadows exist now.** The previous file said "no card wrapper, no shadow" as an invariant. That is
lifted: `--sh-1` is the resting state of a card, and `--sh-3` is what a card rises to on hover.
A *list row* still has no shadow — see §5.

### Motion

```
--fast:150ms   --base:220ms   --slow:320ms   --ease:cubic-bezier(.2,.8,.2,1)
--flash:900ms          a value-flash holds its status ground this long
--spinner-delay:300ms  below this, show nothing rather than a spinner
--stagger:24ms         per item, capped at 8 items / 200ms total

THREE NAMED CURVES (added 2026-09-16, after reading transitions.dev and interior.dev end to end).
--ease stays the default; these exist because one curve cannot answer three different questions.
--ease-out:   cubic-bezier(.22,1,.36,1)    something ARRIVING or LEAVING. Fast first, so the eye
                                           is paid on the frame it is watching hardest.
--ease-io:    cubic-bezier(.77,0,.175,1)   something MOVING between two places it already
                                           occupies: a tab indicator, a segmented thumb.
--ease-drawer:cubic-bezier(.32,.72,0,1)    Ionic's sheet curve, for a surface travelling its own
                                           height.
ease-IN is deliberately absent from this file. It delays the first frame, which is the frame the
reader is watching hardest, so a 300ms ease-in FEELS slower than a 300ms ease-out.

--d-in:250ms  --d-out:150ms   ENTER IS SLOWER THAN EXIT. Arriving is information; leaving is only
                              getting out of the way. Write them as two rules on one class: the
                              rest state carries the exit clock, the .is-open state the entry one.
--dist-1:4px  --dist-2:8px  --dist-3:12px   the only travel distances. A longer trip reads as lag.
--blur-1:2px  --blur-2:3px   blur travels WITH opacity on an enter or exit, and bridges a crossfade
                             so two states never sit visibly on top of each other. 2px is the
                             default, 3px for text. **Always write `filter: blur(0)` explicitly** —
                             `blur(2px) → none` does not interpolate and the transition snaps.
```

### Material

Five shadows are a palette of surfaces, not decoration. The V4 rule stands — a card separates with
a `--line` hairline, not a drop shadow — and these add the part a hairline cannot draw: which side
of the page a thing is on.

```
--specular: inset 0 1px 0 rgba(255,255,255,.9)
            One pixel of light along the top edge. A hairline draws a RECTANGLE; a hairline plus
            this reads as paper lying ON the page. Free: no layout, no colour token.
            Never on a solid accent surface — there it is a seam, not a light.
--well:     inset 0 1px 2px rgba(20,22,26,.06), inset 0 0 0 1px rgba(20,22,26,.08)
            A RECESSED track: the ground under a progress bar, inside a field, behind a thumb.
--fill-face:inset 0 1px 0 rgba(255,255,255,.34), inset 0 -1px 0 rgba(20,22,26,.14)
            The FACE of a bar's fill, so the fill sits in the groove instead of being printed on it.
--lift:     0 1px 2px rgba(16,24,40,.06), 0 8px 18px -12px rgba(16,24,40,.5)
            Hover on something clickable. A long, tight second layer — not a bigger ambient shadow.
```

**Draw an edge as a ring inside a shadow, not as a `border`, on anything whose state changes.**
`inset 0 0 0 1px` occupies no layout, so a row that gains a focus ring or a selected border does
not move its neighbours by a pixel. This is interior.dev's single most portable idea and the reason
nothing on that site shifts between states.

Three durations, one easing, and three named constants. The first version of §8 used `~900ms`,
`~300ms` and `18–30ms` inline — approximate numbers in a token authority are not a specification,
and this file's own Maintenance rule says a needed value not in §2 means the token is missing.

---

## 3. Non-negotiable invariants

0. **Contrast floor — measured, not judged.** Body and label text ≥ **4.5:1** against its actual
   ground. Text at `--t-xl` and above, or `--t-lg` at weight ≥ 600, ≥ **3:1**. Non-text that carries
   meaning — focus rings, status dots, chart marks, control borders, meaningful icons — ≥ **3:1**
   against every surface it sits on. `--line` (1.46:1) and `--line-soft` (1.22:1) are decorative
   hairlines and may never be the only indication that a control exists.
   `scripts/check-design.mjs` re-measures this on every build; it is gate step 22 and it blocks.

   The shipped pairs, measured, so nobody re-derives them:

   | pair | ratio | verdict |
   |---|---|---|
   | `--ink` on `--paper` | 18.11 | pass |
   | `--ink-2` on `--paper` | 11.95 | pass |
   | `--muted` on `--paper` | 5.36 | pass |
   | `--muted` on `--surface` | 4.74 | pass |
   | `--muted` on `--canvas` | 5.00 | pass |
   | `--accent` on `--paper` | 5.17 | pass |
   | white on `--accent` | 5.17 | pass |
   | white on `--accent-deep` | 7.81 | pass — so **both `--grad` stops are legal text grounds** |
   | `--accent-deep` on `--accent-tint` | 6.88 | pass — the action-row label on its bar |
   | **white on `--blue-light`** | 3.23 | **never a text ground** |
   | `--s-issued-text` on `-soft` | 6.44 | pass |
   | `--s-attn-text` on `-soft` | 6.11 | pass |
   | `--s-fail-text` on `-soft` | 7.04 | pass |
   | `--s-sched-text` on `-soft` | 6.83 | pass |
   | `--s-review-text` on `-soft` | 7.79 | pass |
   | `--s-attend-text` on `-soft` | 6.88 | pass |
   | `--s-off-text` on `-soft` | 7.57 | pass |
   | `--s-issued` as a mark | 3.43 | pass |
   | `--s-fail` as a mark | 3.96 | pass |
   | `--s-attn-mark` as a mark | 3.53 | pass |
   | `--s-sched-mark` as a mark | 3.97 | pass |
   | `--s-off-mark` as a mark | 4.15 | pass |
   | `--accent-mark` on `--surface` | 3.51 | pass — the dot token, on the tinted row |
   | `--s-off-mark` as a FIELD ring | 4.15 | pass — see §5, Field |
   | **`--s-attn` as a mark** | 2.45 | **fails — use `--s-attn-mark`** |
   | **`--s-sched` as a mark, on `--surface`** | 2.86 | **fails — use `--s-sched-mark`** |
   | **`--s-off` as a mark** | 2.37 | **fails — use `--s-off-mark`** |
   | `--line` on `--paper` | 1.38 | decorative hairline only — a card edge, never a control boundary |
   | `--line-soft` on `--paper` | 1.16 | decorative hairline only |

0b. **Colour is never the only channel.** Any state distinguished by colour is also distinguished by
   at least one of: a text label, a glyph, a shape, or a position. This binds badges (colour + word),
   chart series (colour + direct label, never a colour-only legend), validation (colour + message +
   `aria-invalid`), deltas (colour + a sign or arrow), and `value-flash` — the flash may only
   re-state a change the figure itself already shows. Raised by a design review on 2026-09-03 and
   absent from this file until 2026-09-06.

1. **`--blue` is the only saturated hue on a surface** — primary button, focus ring, selected-row
   border, progress fill, the sidebar mark, and the one leading figure. Status hues (§2) are a
   separate channel and do not count against this.
2. **The page is `--canvas`. `--paper` is the CARD, not the page.** *(Changed by V3. Before the
   rebrand the page was white and this rule read "canvas is `--paper`" — which now contradicts §2,
   where `--canvas:#F6F7F9` is the ground cards sit on.)* `--surface` marks strips, tiles and nested
   row grounds; it is never the page and never a card.
3. **Type is Cairo, ladder as in §2, `letter-spacing:0` on Arabic.**
4. **`--muted` is the lightest text.** Never `--s-off` or `--line` for a word a person must read.
5. **Radii come from the four-value scale.** No `4px`, no `12px`, no `20px`.
6. **A row is a card only under 12 rows.** *(Amended 2026-09-07. Both V3 references make every row
   a soft card; at ledger scale that is a stack of cards pretending to be a table, which is the
   design review's hard-rejection #7.)* A row may carry a `--surface` ground and `--r-md` **only on
   a surface that shows at most 12 rows at once** — the home work queue, the alerts card, the
   appointments card. Any surface that can exceed 12 — the leads list, the campaign list, the
   opportunity list, everything `qa:scale` touches — stays a **flush table**: a header row,
   `--line-soft` dividers, no per-row radius, no per-row shadow, hover as a ground change
   (`--accent-wash`) and never a lift. **The radius belongs to the panel, never to the row.**
   **Row state is a dot plus a label, or an outlined pill (colour + dot + word) — never a filled
   chip.** A *card* (`--r-lg`, `--sh-0`) is a different object, used where a thing is separable.
7. **One primary button per screen.** Everything else is ghost or text.
8. **Focus is visible, and it is measured.** Default `outline:2px solid var(--blue);
   outline-offset:2px`, on `:focus-visible` only — a mouse click must not draw a ring. **On any
   ground where that ring falls below 3:1 the ring inverts** to `outline-color:var(--paper)` with
   `box-shadow:0 0 0 4px rgba(48,109,181,.35)`. This is not hypothetical: a blue ring on the blue
   primary button measures **1.00:1** — the single most important control on every screen had no
   visible keyboard focus, a straight WCAG 2.4.7 failure, and this file specified it that way until
   2026-09-06. `outline:none` is permitted only with a `:focus-visible` replacement meeting the same
   floor.
9. **Focus is managed, not just styled.** Opening an overlay moves focus to its first heading or its
   close control, traps Tab inside it, closes on Escape, and **returns focus to the element that
   opened it**. A surface that re-renders must preserve the focused element across the render —
   `#body` is rewritten on every keystroke here, and losing focus mid-typing is the keyboard
   equivalent of §8.1's button jumping.
10. **Touch targets.** Every interactive element has a hit area of at least **24×24px** always, and
   **44×44px** under `@media (pointer:coarse)`, achieved with padding or a transparent `::after`,
   never by growing the visual mark. List rows keep their 36px visual height and expand to 44px on a
   coarse pointer. Two adjacent targets are separated by at least `--s2`. Measured 2026-09-06: the
   subnav tab is **43px** on a phone — one pixel short, because the strip carries a 1px border.
11. **There is no dark mode.** Massar renders on `--paper` only. `prefers-color-scheme` is not
   consulted, no token has a dark counterpart, and the shadows are a blue-grey tuned for a light
   ground. If dark mode is ever adopted it is a rebrand of this file, not a per-screen media query.
12. **Hatch means NOT YET, and nothing else.** `repeating-linear-gradient` at 115deg is a TEXTURE
   channel layered on colour, so an unfilled remainder still reads in greyscale and under a colour
   deficiency. It marks the empty part of a bar, a stage not reached, and a period with no target.
   It is never decoration and never encodes a second meaning. Adopted from both V3 references,
   which is the only reason a texture is in this file at all.

13. **A destructive action is a HOLD, not a second click.** «حذف» arms nothing; the operator presses
   and holds for 900ms while a fill grows, and releasing early cancels. Arm-then-confirm put the
   second click exactly where the first one was, which is how a row gets deleted by a fast double
   click. **The fill is a transitioned `transform`, never a keyframe**, so an interrupted hold
   resumes from where the element actually is (§8.1 failure 2). **Keyboard never holds** — Enter or
   Space arms, a second press commits — and `prefers-reduced-motion` falls back to the same two-step
   path, because a hold whose only feedback is an invisible timer is §8.1 failure 3.

9. **Illustration is drawn flat, in brand colour.** No generated imagery, no stock, no 3D render,
   no pastel icon discs.

---

## 4. Correctness rules that outrank all taste

Unchanged by the rebrand. These are about truth, not looks.

- Arabic-Indic numerals via `fmtN`; `check:numerals` must stay green. **A year is not a quantity:**
  use `arYear` (no thousands separator) or `٢٠٢٦` prints as `٢٬٠٢٦`.
- RTL **logical properties only** — no `left`/`right`, no physical offsets. A physical padding
  lands correctly today only because the document is RTL, and flips the moment anything renders LTR.
- **Bidi isolation.** Every Latin or numeric run embedded in Arabic text is wrapped in `<bdi>` or an
  element with `dir="auto"` — phone numbers, IDs, currency codes, percentages, and every `--t-num`
  figure. Never rely on the document's own `dir` to place a mixed run's punctuation. Numeric table
  columns align to the inline-end and are `dir="ltr"` internally so digits do not reorder.
- **Directional geometry mirrors with the document.** A horizontal bar grows from the
  **inline-start**. A drawer enters from the **inline-start** unless anchored to a control. The
  segmented indicator's travel is computed from the measured inline offset, never a signed pixel
  constant. A chevron points toward the inline-start when collapsed. Where CSS has no logical form —
  `translateX`, gradient angles, `rotate` — the physical value is authored for RTL and mirrored
  under `[dir="ltr"]`, and the mirror is stated in the same rule. **`--grad` is the named exception
  to the logical-properties rule**: CSS gradient angles never respond to `direction`, so `270deg` is
  physical and always points left. Prefer the vertical `--wash`, which needs no mirror. **No
  gradient sits under text** unless the text clears §3.0 against *both* stops — white is 5.28:1 on
  `#306DB5` and **2.93:1** on `#629CCD`, so `--grad` is a decorative ground only.
- Honest-absence vocabulary: «لم تُرسل بعد» · «بلا جمهور» · «—». A rate over nothing renders «—»,
  never «٠٪». A figure with no target has *no* coverage, which is not 0% coverage.
- **An empty state names itself.** A blank table and a broken query look identical to the reader;
  every screen that can return nothing says which one happened, in words.
- **No invented values.** A denser row is not filled with computed placeholders.
- The dashed `.c-read` chip keeps its dash (assistant reading ≠ recorded fact).
- `src/dashboard.ts`: anchored single-property replacements only (ADR-0001).
- **No backticks inside any `*-crm.ts` / `rep-page.ts` template literal**, comments included.

---

## 5. Components

**Row** — flush, `--line-soft` top border, no shadow, state as dot + label.
**Card** — `--r-md`, `--sh-1`, `--paper`, `--s3`/`--s4` padding; rises to `--sh-3` and
`translateY(-2px)` on hover **only if it is clickable**.
**Tile / KPI** — `--surface` ground, `--r-md`. One figure leads at `--t-num` or `--t-2xl`; the rest
support it. Five identical number cards is a spreadsheet, not a page.
**Badge** — `-soft` ground, `-text` label, `--r-pill`.
**Bar** — `--r-pill`, `--s-off-soft` track, blue fill. A single-hue ramp may encode ORDER; it may
never encode a second meaning.
**Stacked bar** — for large N where individual marks would be unreadable.
**Segmented control / tabs** — the active item carries a blue underline or a pill that *slides*
(§8), never a filled block.

**Control states.** Every interactive control defines rest / hover / active / focus-visible /
disabled / loading. Primary button: `--blue` rest, `--blue-deep` active, `--blue-wash` hover border.
**Disabled** = `--s-off-soft` ground, `--s-off-text` label, `cursor:not-allowed`,
`aria-disabled="true"`, no hover and no motion. Disabled text is exempt from §3.0, but a control
whose *only* signal of unavailability is being dimmed violates §3.0b — say why it is disabled, in
words, beside it.

**Skeleton.** Blocks are `--skeleton` at `--r-sm`, at the **exact** height and inline-size of the
content they stand in for — a skeleton that resizes on swap is §8.1 failure 1. Show one only for
work expected to exceed `--spinner-delay`; once shown, hold it at least 400ms so it cannot flash. At
most **5** skeleton rows regardless of the eventual list length. Cross-fade to content over
`--base`. Shimmer is a single `transform:translateX` sweep at `--slow`, suppressed under reduced
motion. A spinner is permitted only where the layout is unknown (a full route change), never over a
laid-out surface.

**Field error.** The message renders **inline, immediately after the field and before the next
one**, in `--s-fail-text` at `--t-xs`, prefixed by a glyph (§3.0b). The field carries
`aria-invalid="true"` and `aria-describedby` pointing at the message. A form-level error sits above
the submit control, never only in a toast — a toast expires and an error must not. On submit
failure, focus moves to the first invalid field. The shake is decorative and never the only signal.

**Table.** The list surface for anything that can exceed 12 rows (§3.6). A `--surface` header row
at `--t-xs`/600 `--muted`, `--line-soft` dividers, `--r-none` on the row, and the radius on the
PANEL. Hover is a ground change to `--accent-wash`, never a lift. The panel carries `--r-lg` and
`--sh-0`; its header holds the title and a right-aligned cluster of `--r-pill` icon buttons.

**Field.** `--paper` ground with **its own ring**: `inset 0 0 0 1px --s-off-mark` (3.69:1, clearing
the 3:1 floor a control boundary must meet). Focus deepens to a 2px `--accent` ring plus a 3px
`--accent-tint` halo. **A field must never rely on the page for its visibility.** This rule exists
because the first V3 pass made the field a filled `--surface` box with no border, which reads on
white and *vanishes* on a tinted panel — on the opportunity editor, whose ground is also
`--surface`, four price inputs rendered as bare numbers floating with no affordance at all.
`--line` (1.48:1) is why the ring is not drawn in it. **Every field carries a real `<label for>`;
a placeholder is not a label** — it disappears the moment someone types.

**Outlined status pill.** `inset 0 0 0 1.5px <status -mark>` on `--paper`, the `-text` value as the
label, a 7px dot of the same `-mark`, `--r-pill`. Three channels — colour, shape, word — so §3.0b
holds without the reader seeing colour. **`white-space: nowrap`**: a pill that wraps to two lines
moves every row beneath it, which is §8.1 failure 1.

**Meter.** Ten cells at `--r-sm`, `--surface-2` track, `--accent-mark` fill (`--accent-deep` above
the top band). For an EARNED 0-100 score only — never a percentage of something the system made up.
The number and the band label sit beside it, so the reading survives at rest under reduced motion:
a meter that only reads after animating is a meter that never reads.

**Delta chip.** `-soft` ground, `-text` label, `--r-pill`, and an arrow glyph **plus** a word.
Colour is the third channel, never the first. «— بلا تغيّر» is a real state and gets `--s-off-soft`.

**Filter chip.** `--surface` ground, `--r-pill`, `--accent-tint` + `--accent-deep` when active.
Each carries a COUNT, and per §7.10 that count is work OWED, never a total.

**Hold-to-confirm.** See §3.13. `--s-fail-soft` ground at rest inside a row of actions, height
matched to the buttons beside it, and quiet until hovered — a destructive control does not
advertise itself in a resting row.

**Icon.** `--i-sm`/`--i-md`/`--i-lg`, stroke 1.5px, `currentColor`. An icon that carries meaning on
its own clears the 3:1 non-text floor and has an accessible name. An icon that merely repeats a
label beside it is decorative, may be lighter than `--muted`, and is `aria-hidden="true"`. There is
no third case.

---

## 6. Charts, and what a chart is allowed to encode

1. **A chart's geometry must be its data.** Where a shape cannot be trusted to encode the value,
   use a horizontal bar, whose length is unambiguous.
2. **A funnel is drawn as a funnel** — each band's top edge is the stage above it, so the slope
   between two bands IS the drop. Equal stages draw a column.
3. **Time runs right to left**, like the language. Mirror the x mapping; do not reverse the array.
4. **One accent per surface.** `--blue` is the only saturated hue in a chart. Status hues may
   appear where the chart is *about* status.
   **Exception, by founder instruction (2026-09-15): the STAGE channel.** A sales stage has its own
   hue wherever it is drawn — the board summary bar and stage ribbon, the row badge, the kanban
   column cap, the drawer stepper, and «نظرة تنفيذية». V5's single blue ramp made six stages
   indistinguishable, which is what was rejected. The palette is NOT a set of `:root` tokens; it lives
   in `massar-engine/src/stage-tone-domain.ts`, where each tone is three values (solid, soft, text)
   and `tests/stage-tone-domain.test.ts` re-measures every one: white on solid ≥ 4.5:1, text on soft
   ≥ 4.5:1, solid as a mark on `--surface-2` ≥ 3:1, and no two stages share a hue.

   | stage | solid | soft | text |
   | --- | --- | --- | --- |
   | تواصل أولي | #475569 | #EEF1F5 | #334155 |
   | اكتشاف الحاجة | #0F766E | #E3F4F1 | #115E59 |
   | عرض المنتج | #2563EB | #EAF1FE | #1A47BE |
   | التقييم التقني | #7C3AED | #F1EAFD | #5B21B6 |
   | عرض السعر | #A21CAF | #FAE8FB | #86198F |
   | التفاوض والاعتماد | #C2410C | #FDEDE3 | #9A3412 |
   | إغلاق – ربح | #15803D | #E4F5EC | #12633F |
   | إغلاق – خسارة | #B91C1C | #FBE7E6 | #8E2A27 |

   A rung an admin adds takes the next hue from a four-tone cycle (indigo, sky, amber, pink). §3.0b
   still holds without exception: every stage colour is drawn beside the stage's printed label.
5. **A label you truncate is a label you did not draw.** No `text-overflow` on an axis: if the
   category name does not fit horizontally, the chart is the wrong orientation.
6. **Zero denominators render «—», never «٠٪».**
7. **No decoration that carries no data**: no hover lift on a non-interactive card, no gauge over a
   two-state boolean, and **inside a plotting area, no gradient that is not a value ramp**. The
   earlier wording forbade gradients outright, which contradicted the two `--grad`/`--wash` tokens
   §2 ships. They are brand gradients for chrome — a sidebar mark, a hero strip, a button ground —
   and never appear on a mark whose colour a reader might read as a value.

---

## 7. Lists at production scale

8. **Truncation is not pagination.** Every flat list states «٦١–١٢٠ من ١٬٧٠٠» — the range is the
   sentence that tells the reader the list continues.
9. **Per-group preview caps are allowed on GROUPED surfaces only**, and must state the whole
   group's count in its header.
10. **A count in the chrome is a count of work OWED, never a total.** «العملاء ١٬٧٠٠» is
    decoration; «فرص البيع ٤» is a reason to click.
11. **Elapsed time is stated in the unit a person would say it in** — hours under two days, then
    days, then months.
12. **A shortlist must say what it is a top-of.**
13. **A page must have a point of view.** One figure leads at the size that says so.
14. **Every new list design is verified at production scale** (`npm run qa:scale`), not at demo
    scale. Six defects in this file were invisible at 16 contacts.

---

## 8. Motion — the half-second after a click

Two external references are **mandatory reading on any UI work** (founder instruction, standing):

- **transitions.dev** — the catalogue of named UI transitions.
- **interior.dev** — micro-interactions, organised by *what the person is in the middle of*.

They govern **timing and behaviour**. Palette, type and spacing come from §2 and win on those.

### 8.1 The three failures — interior.dev's, and they are the acceptance criteria

Every animated surface in Massar is checked against these three before it ships. They are quoted
because the wording is the specification:

1. **"The button jumps."** A label changes from «حفظ» to «جارٍ الحفظ» and the control resizes, so
   the row beneath moves and the cursor is suddenly over something else. **Every state a component
   can reach must reserve its width before it gets there.** Measure the longest label, not the
   first one.
2. **"The animation cannot be interrupted."** Click again halfway through and a bad transition
   restarts from the beginning, or queues. **A transition must resume from where the element
   actually is** — which for CSS means transitioning a property, never replaying a keyframe on
   re-trigger.
3. **"Motion is the only channel."** With reduced motion on, most libraries either play anyway or
   hide the element. **The information has to arrive either way. The trip is optional, the
   destination is not.** `@media (prefers-reduced-motion:reduce){*{animation:none!important;
   transition:none!important}}` is the floor, and every surface must still be *correct and
   complete* under it — a value that only appears by counting up is a value that never appears.

### 8.2 Which duration

Pick by **usage, not by the number** — that is transitions.dev's own rule, and it is why there are
three tokens instead of a free field.

| token | ms | for |
|---|---|---|
| `--fast` | 150 | hover, focus, colour, a state the user is *holding* |
| `--base` | 220 | the default: open, close, swap, move, reveal |
| `--slow` | 320 | a large surface, or a distance the eye has to follow |

**Distance sets duration.** A 4px hover lift and a full-panel reveal do not share a number.
**Exit is faster than entry** — a menu that appears in `--base` closes in `--fast`; a tooltip is
*appear-only delay, instant exit*. Stagger a group by 18–30ms per item and cap the total: a list of
forty rows does not stagger forty times.

### 8.3 Animate what composites

transitions.dev is blunt about the cost, and the reasoning transfers directly:

> *"Animating mask-position never composites — it repaints the element … the animated property has
> to leave the paint path entirely … transform composites."*

**Animate `transform` and `opacity`.** Reach for `width`, `height`, `inset-block-start`,
`mask-position`, `box-shadow` or `filter` only when there is no transform equivalent, and never on a
per-frame loop. §4's logical-property rule binds animated properties too — an earlier version of
this line said `top`, which §4 forbids, so a reviewer following §8.3 failed §4.
This matters more here than on most products: the engine is one 512MB shared-CPU machine that is
also serving the Gupshup webhook.

### 8.4 The ten moments — organised by what the person is doing

interior.dev's framing, which is the useful one: not by widget, but by the situation.

| moment | the question it answers | where it lands in Massar |
|---|---|---|
| **Action Feedback** | "You did something. Did it land?" | stage move, «سجّل النتيجة», retire a package |
| **Input** | "You are telling the system something it might reject." | target amount, package price, tag rename |
| **Async** | "You are waiting, and you deserve to know on what." | report load, campaign launch, import |
| **Notification** | "The system is telling you something you did not ask for." | new reply, «عميل جاد» alert |
| **Overlay** | "Something came on top. It has to know where it came from." | conversation drawer, package editor |
| **Navigation** | "You moved. The interface should agree about where." | six doors, the tab strip |
| **Scroll** | "You are reading, and the page is reacting to that." | long lists, the activity log |
| **Data** | "A number changed. Which one, and by how much?" | KPI tiles, coverage, «المحقق» |
| **Gesture** | "Your finger is on it. Physics is now part of the API." | `/rep` on a phone |
| **Content** | "The thing itself arrives, resolves, or is missing." | every screen's empty state |

### 8.5 The named patterns Massar actually uses

**They live in one place: `src/motion.ts`.** By founder instruction (2026-09-06), any motion in
Massar with an equivalent in the transitions.dev catalogue comes from that vocabulary rather than
being invented per screen — implemented against the tokens in §2 and named after the catalogue, so
any animation on any screen traces back to a named pattern.

**Half the catalogue is deliberately absent.** Confetti bursts, gooey menus, 3D pointer tilt,
like-button particles, smoky delete, card-stack fans: those are marketing-surface patterns, and
§Pass-4's classifier puts Massar in APP UI, whose rules are calm surfaces and no decoration that
carries no data. The absence is the decision, not an oversight.

| pattern | class / helper | where it is used |
|---|---|---|
| number-pop-in | `moNumber()` | every KPI value and quarter figure, on CHANGE only |
| value-flash | `moFlash(el, dir)` | a figure that moved, holding its `-soft` ground for `--flash` |
| texts-reveal | `.mo-stagger` | ranked lists: «أين المفتوح الآن», the dept rollup |
| skeleton-swap | `moSkeleton(n, widths)` | products, product drill, sector drill, reports |
| accordion | `.mo-acc` + `moAcc()` | collapsibles, on `grid-template-rows` |
| toast | `moToast(msg)` | package retire, and any outcome that must be SAID |
| panel-reveal | `.mo-panel` + `.mo-scrim` | the conversation drawer |
| modal | `.mo-modal` | dialogs |
| icon-swap | `.mo-swap` | two glyphs in one grid cell, so the control never resizes |
| success-check | `.mo-check` | draws on; it does not fade in |
| error-shake | `moShake()` | one shake, never a loop, never the only signal |
| tooltip | `.mo-tipwrap` | appear-only delay (400ms), instant exit |
| text-states-swap | `moReserve()` / `moBusy()` / `moIdle()` | «حفظ» → «جارٍ الحفظ» at a reserved width |
| learn-more-hover | `.mo-more .mo-arrow` | back links; the chevron shifts toward the inline-end |
| tabs-sliding | `moveInd()` | the door tab strip and the report tabs |
| new-items-pill | `.mo-nip` | rows arriving during a read are announced, not injected |

Every one obeys four rules: `transform`/`opacity` only; RTL-correct, authored for the document's own
direction and mirrored under `[dir="ltr"]` where CSS has no logical form; exit faster than entry;
and reduced motion removes the trip, never the destination.

#### The original catalogue notes

From the approved system's own nine moments and transitions.dev's catalogue. **Adopt these by
name**; do not invent a tenth without a reason written down.

| pattern | rule |
|---|---|
| **hold-to-confirm** | for destructive or irreversible actions only, with a filling progress ring |
| **loading-button** | width reserved for the longest state before the click (failure 1) |
| **value-flash** | a changed figure flashes its `-soft` status ground for ~900ms, then returns |
| **poll-results / status share** | proportions animate in from zero once, not on every repaint |
| **task-steps** | the current step is marked, completed steps stay visible |
| **segmented / tabs sliding** | the indicator *slides* between tabs; it does not cut |
| **skeleton-swap** | skeleton lines cross-fade to real content; never a spinner over a layout |
| **new-items-pill** | new rows arriving during a read are announced, not injected under the cursor |
| **collapsible / accordion** | animate `grid-template-rows`, with the chevron rotating |
| **number pop-in** | a counting figure must also be correct at rest (failure 3) |
| **toast** | rises with fade + scale; exits faster than it enters |
| **error shake** | one cubic-bezier shake, never a loop |
| **success check** | the check draws on; it does not fade in |

### 8.6 What is forbidden

- Motion on a non-interactive element.
- A spinner that outlives its request, or one shown for under ~300ms of work.
- A row that jumps as it loads — reserve the height.
- Replaying an entrance animation on every re-render. Massar re-renders `#body` on every keystroke;
  a 420ms slide-up on each one is the jump the designer measured.
- Any animation that is the *only* way a value is communicated.

---

## 9. Enforcement

**`scripts/check-design.mjs` is gate step 22 and it blocks a deploy**, exactly like the numerals,
RTL, nav-destination and ledger-writer checks. It fails on:

- a text/ground pair below the §3.0 floor;
- `--s-off`, `--line` or `--line-soft` used as a text colour;
- a status **base** value used as a dot or bar where a `-mark` exists;
- a hex literal in `src/` that is not a §2 token or a named exception;
- an integer `z-index`;
- a `font-size` off the §2 ladder.

This section exists because the rule it enforces was already written and already violated. §3.4 has
forbidden `--s-off` as text since this file was rebranded, and the codebase carried **165**
`color:#A9B4C0` declarations at 2.10:1 — real sentences, not decoration — plus four using the border
token as text. Twenty-one gate steps ran on every build and not one looked at design.

**A rule in this file that the checker cannot test is either rewritten until it can be, or moved
below and marked non-blocking taste.** The checker starts from a recorded baseline: existing
violations are counted, and the count may only go down. A new violation fails the build immediately.

## Maintenance

Update this file when the founder changes a token, not when a screen wants an exception. A screen
that needs a value not in §2 is either wrong or is telling you the system is missing a token — in
which case add the token here first, then use it.
