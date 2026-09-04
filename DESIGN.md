# DESIGN.md — Massar token authority

**Read this before writing any UI code. These tokens override newly invented values.**

> **REBRAND, 2026-09-04.** This file previously specified a teal accent (`#1F7A73`) over a
> pure-neutral grey ramp with no shadows. It no longer does. By founder instruction, Massar adopts
> the approved Seha design system at
> `~/.gstack/projects/combinedservices/designs/design-system-20260903/preview-v2.html`
> (selection record: that folder's `approved.json`, approved 2026-09-03 after v1 was rejected).
> **Every rule below that carries a colour, radius, shadow or duration is new. Anything in the
> codebase still using teal, `#171717` ink or `#EDEDED` lines is pre-rebrand and is a migration
> target, not a precedent.** The correctness rules (§4) and the chart and list rules (§6, §7)
> survived the rebrand unchanged — they were never about the palette.

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
--blue:        #306DB5   primary. The one saturated hue on a surface.
--blue-deep:   #416CAD   pressed / heavier weight
--blue-light:  #629CCD   secondary data, scheduled state
--blue-tint:   #EAF1F8   selected row, quiet fill
--blue-wash:   #DDEAF3   hover border, gradient stop
--grad:        linear-gradient(270deg,#306DB5,#629CCD)
--wash:        linear-gradient(180deg,#DDEAF3,#FFFFFF)

--paper:       #FFFFFF   the canvas
--surface:     #F4F6F9   strips, quiet tiles
--surface-2:   #EDF1F7   nested strip
--line:        #CBD7E4   a real border
--line-soft:   #E3E9F1   a hairline between rows
--ink:         #212529   headings, primary text
--ink-2:       #3A3A3A   body
--muted:       #536170   labels, secondary — the LIGHTEST text token
```

**The greys are deliberately blue-tinted now.** The previous invariant banned exactly this. It is
reversed: `#F4F6F9`, `#CBD7E4`, `#536170` are the system, and a pure-neutral `#EDEDED` line is now
the thing that looks foreign.

### Status

Status colour is a **separate channel from the accent** and never borrows it.

```
issued / good      --s-issued:#1E9E63   soft --s-issued-soft:#E4F5EC   text --s-issued-text:#12633F
attention / warn   --s-attn:#D99A00     soft --s-attn-soft:#FFF5D6     text --s-attn-text:#7A5600
                   --s-attn-deep:#B37F00
failed / bad       --s-fail:#D9534F     soft --s-fail-soft:#FBE7E6     text --s-fail-text:#8E2A27
scheduled          --s-sched:#629CCD
under review       --s-review:#416CAD
off / inactive     --s-off:#A9B4C0      soft --s-off-soft:#EEF1F4
attending          --s-attend:#306DB5
```

The `-soft` fill exists for a **badge ground**; the `-text` exists so the label on that ground
still passes contrast. Never put `--s-fail` text on `--s-fail-soft` — use `--s-fail-text`.

### Type

**Cairo**, unchanged from before and unchanged by the rebrand — loaded as the variable face
`wght@200..1000` so it holds intermediate weights natively.

```
--t-xs:12px  --t-sm:14px  --t-md:16px  --t-lg:18px  --t-xl:22px  --t-2xl:28px  --t-3xl:40px
--t-num:44px   the one big figure on a screen
```

- `letter-spacing: 0` on all Arabic. `0.02em` is for Latin/LTR spans only.
- `--muted` (`#536170`) is the lightest text token. Anything lighter is an icon or a placeholder.

### Space, radius, shadow

```
--s1:4  --s2:8  --s3:16  --s4:24  --s5:32  --s6:48  --s7:64      (px)
--r-sm:8  --r-md:10  --r-lg:16  --r-pill:999
--sh-1: 0 0 4px rgba(83,97,112,.08)                       resting card
--sh-2: 0 4px 8px rgba(83,97,112,.16)                     raised control
--sh-3: 0 3px 6px -4px rgba(0,0,0,.12),
        0 6px 16px rgba(0,0,0,.08),
        0 9px 28px 8px rgba(0,0,0,.05)                    hover / floating
```

**Shadows exist now.** The previous file said "no card wrapper, no shadow" as an invariant. That is
lifted: `--sh-1` is the resting state of a card, and `--sh-3` is what a card rises to on hover.
A *list row* still has no shadow — see §5.

### Motion

```
--fast:150ms   --base:220ms   --slow:320ms   --ease:cubic-bezier(.2,.8,.2,1)
```

Three durations, one easing. See §8 for which to reach for and why.

---

## 3. Non-negotiable invariants

1. **`--blue` is the only saturated hue on a surface** — primary button, focus ring, selected-row
   border, progress fill, the sidebar mark, and the one leading figure. Status hues (§2) are a
   separate channel and do not count against this.
2. **Canvas is `--paper`. `--surface` marks strips and tiles, never a page.**
3. **Type is Cairo, ladder as in §2, `letter-spacing:0` on Arabic.**
4. **`--muted` is the lightest text.** Never `--s-off` or `--line` for a word a person must read.
5. **Radii come from the four-value scale.** No `4px`, no `12px`, no `20px`.
6. **A row is not a card.** List rows stay flush on `--line-soft`, block padding `--s2`, gutters
   `--s4`/`--s3`, min-height 36px, no shadow. **Row state is a dot plus a label, never a filled
   chip.** A *card* (`--r-md`, `--sh-1`) is a different object and is used where a thing is
   genuinely separable.
7. **One primary button per screen.** Everything else is ghost or text.
8. **Focus is visible and it is blue**: `outline:2px solid var(--blue)` with a 1–2px offset.
   Never `outline:none` without a `:focus-visible` replacement.
9. **Illustration is drawn flat, in brand colour.** No generated imagery, no stock, no 3D render,
   no pastel icon discs.

---

## 4. Correctness rules that outrank all taste

Unchanged by the rebrand. These are about truth, not looks.

- Arabic-Indic numerals via `fmtN`; `check:numerals` must stay green. **A year is not a quantity:**
  use `arYear` (no thousands separator) or `٢٠٢٦` prints as `٢٬٠٢٦`.
- RTL **logical properties only** — no `left`/`right`, no physical offsets. A physical padding
  lands correctly today only because the document is RTL, and flips the moment anything renders LTR.
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

---

## 6. Charts, and what a chart is allowed to encode

1. **A chart's geometry must be its data.** Where a shape cannot be trusted to encode the value,
   use a horizontal bar, whose length is unambiguous.
2. **A funnel is drawn as a funnel** — each band's top edge is the stage above it, so the slope
   between two bands IS the drop. Equal stages draw a column.
3. **Time runs right to left**, like the language. Mirror the x mapping; do not reverse the array.
4. **One accent per surface.** `--blue` is the only saturated hue in a chart. Status hues may
   appear where the chart is *about* status.
5. **A label you truncate is a label you did not draw.** No `text-overflow` on an axis: if the
   category name does not fit horizontally, the chart is the wrong orientation.
6. **Zero denominators render «—», never «٠٪».**
7. **No decoration that carries no data**: no hover lift on a non-interactive card, no gauge over a
   two-state boolean, no gradient that is not a value ramp.

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

**Animate `transform` and `opacity`.** Reach for `width`, `height`, `top`, `mask-position`,
`box-shadow` or `filter` only when there is no transform equivalent, and never on a per-frame loop.
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

## Maintenance

Update this file when the founder changes a token, not when a screen wants an exception. A screen
that needs a value not in §2 is either wrong or is telling you the system is missing a token — in
which case add the token here first, then use it.
