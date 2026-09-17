# «الرئيسية» rebuilt — three prototypes, Sep 16 2026

The founder rejected the home page a fifth time: *"your design on the home page is not acceptable
this is not a good design system and ux at all."* Four previous rejections were answered with
incremental patches. This one is answered with three complete systems and a choice.

## The diagnosis

The prior home page leads with a **96px `0`** inside an arc ring reading **0%**. That is the
largest, most expensive element on the screen, and it is spent on the least informative fact in
the product. Worse, it is spent restating a *consequence*: achieved is zero because no
opportunity has been closed won, which the pipeline section already says.

Every rejection has been the same defect in a different costume: the screen is a **pile of cards
that each restate a number**, with no grammar deciding which number leads, and no answer for the
state the data is actually in. The live figures are target 34,000 SAR, achieved 0, 0%, six open
lines worth 4,200 SAR, zero won deals, and five of six products with no target at all. **The
near-empty state is not an edge case here. It is the state.** A design that only looks right once
the database is full is the wrong design for this product today.

So each prototype is defined by a different answer to one question: *what leads when the figure
is zero?*

## The three

| | A — «السجل» The Ledger | B — «سطح العمل» The Worktop | C — «لوحة القياس» The Instrument |
| --- | --- | --- | --- |
| **What leads** | The figure, set as a sentence | The work, ranked by impact | The frame: the year's target line |
| **Surface grammar** | No cards at all. Rules and type only | Cards, but as task rows | One dark instrument band + small multiples |
| **Hierarchy from** | Type weight and ink level | Position in the queue | The gap between two lines |
| **Zero reads as** | An honest, quiet statement | A full to-do list (inverts with data) | A measurable distance below the line |
| **Risk** | Can feel austere; no visual anchor | Demotes the figures the CEO asks for | Most machinery to maintain |
| **Best if** | You want it to feel like serious financial software | You want the screen to drive daily action | You want to see trajectory at a glance |

Files: `~/.gstack/projects/Abdulaziz-almoshen-Massar/designs/massar-home-20260916b/`
(`A-ledger.html`, `B-worktop.html`, `C-instrument.html`, `_tokens.css`, and a PNG of each).
All three are RTL Arabic in Cairo, on the real `DESIGN.md` tokens read out of `:root` in
`src/dashboard.ts` — no invented values — with western numerals and the settled navy rail drawn
so the proportions are honest.

## Measured from the references, not recalled

The reference registry is `docs/designs/ui-component-references.md`. What this pass took:

- **The digit ticker is CSS-only.** From `beui.dev/components/motion/number`: a `1ch`-wide,
  `1.1em`-tall `overflow:hidden` slot over a stacked column of the glyphs 0-9, moved with
  `transform: translateY(calc(-1 * var(--d) * 1.1em))` at `.9s cubic-bezier(.16,1,.3,1)` with a
  `var(--i) * .04s` per-column stagger. No library. It satisfies the western-numerals rule for
  free, because the column literally contains `0..9`. Ported into C's leading figure.
- **`width: 1ch` + `tabular-nums` is the whole trick** for a figure that must not reflow while it
  changes. Applies to every leading figure in the product.
- **Their tab indicator is deliberately over-damped** — spring `170/30/1.2`, not the library's
  own `SPRING_LAYOUT` — because overshoot inside a scrollable rail produces a transient scrollbar
  and a layout shift. That reasoning applies directly to the existing tab rail on
  `#product/<name>`.
- **One curve, many durations.** Effectively everything on beui.dev uses
  `cubic-bezier(.16, 1, .3, 1)`, with duration carrying the meaning: 0.18 swap, 0.3 layout,
  0.5 icon, 0.9 ticker. `DESIGN.md` §2 currently names three curves. Fewer curves plus disciplined
  durations is the more coherent system.

### One finding that needs a decision, not absorption

beui.dev has **no elevation shadow system at all** — four `box-shadow` declarations on the whole
page, every one transparent. Surfaces separate with a single `rgba(255,255,255,.05)` hairline over
a 5%-white fill. The Material pass added to `DESIGN.md` §2 on Sep 16 went the other way: multi-stop
card shadows, `--specular`, `--well`, `--lift`.

Both are internally consistent. **Mixing them is what produces the generic look.** beUI's grammar
is dark-mode-native and the hairline-only approach is much weaker on a light ground, which is what
Massar uses — so the shadow system is probably right for us and the point is to commit to it
rather than to keep half of each. Prototype A tests the opposite bet (rules only, no boxes), which
is the light-ground equivalent of the beUI position.

## Still open

- The motion-reference pass (`kinetics.colorion.co`, `transitions.dev`, `originkit.dev`) stalled
  before finishing. The easing values in use are already settled in `DESIGN.md`, so nothing is
  blocked; re-run it if the chosen direction leans hard on physics.
- `beui.dev` has **no line/bar/area chart component** — three chart pages, two of them calendar
  heatmaps. C's trajectory chart is hand-built on the 21st.dev `line-charts-8` grammar already
  ported in `sparkArea()`.
