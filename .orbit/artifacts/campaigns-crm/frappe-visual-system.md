# Massar–Frappe visual system (cycle V1)

The founder overruled Rule 3 for *visual-system* scope: option (B), adopt Frappe CRM's actual
visual system, translated to RTL/Arabic. Rule 3 still governs **branding** — name, logo, sidebar,
the teal primary action.

## 1. Type ladder

Frappe's 1.15 line-height is a Latin affordance; Arabic clips below ~1.4. Density is recovered
from the **row box**, not the line-height number.

**Face: IBM Plex Sans Arabic.** Cairo is display-leaning — wide sidebearings, tall ascent, no
weight between 400 and 500. Plex Arabic is a UI face, ships **Text 450** (the exact analogue of
Frappe's 420), and its Latin companion stops phone numbers switching face mid-row. **Cairo
survives only in the sidebar wordmark «مسار» at 700**, and as fallback for one release.

| token | size | line-height | weight | use |
|---|---|---|---|---|
| `2xs` | 11px | 1.5 | 500 | overline, mobile column header |
| `xs` | 12px | 1.5 | 450/500 | meta, column headers |
| `sm` | 13px | 1.45 | 450 | secondary row text, controls |
| **`base`** | **14px** | **1.45 (20px)** | **450** | **row body — the default** |
| `md` | 15px | 1.5 | 500 | section heads |
| `lg` | 18px | 1.5 | 600 | page title |
| `prose` | 13px | 1.75 | 450 | `.sparse`, empty states, help |

**`letter-spacing: 0` on every Arabic run** — Frappe's `0.02em` separates cursive joins. `0.02em`
is permitted only on Latin/LTR spans (phone numbers, IDs).
**Weights:** 420→**450** · 500→500 · 600→600 · 700→700, *retired from list rows*. Massar's
700-weight row names are the loudest "this is Massar" signal on `#kmon`; they go to 450.

## 2. Greys — pure neutral, zero chroma

`oklch(L 0 0)` resolved to sRGB. Every Massar grey it replaces carries blue chroma; this is the
single biggest reason the screens look unchanged.

| step | hex | replaces | semantic |
|---|---|---|---|
| 50 | `#F8F8F8` | `#F9FAFB` | `surface-gray-1` — control strip, hover |
| 100 | `#F3F3F3` | `#F2F4F7` | `surface-gray-2` — selected row, tracks |
| 200 | `#EDEDED` | `#EAECF0` | `outline-gray-2` — **all 1px borders** |
| 300 | `#E2E2E2` | `#E4E7EC` | dividers on grey, disabled border |
| 400 | `#C7C7C7` | `#D0D5DD` | `ink-gray-4` — disabled, dashed edges |
| 500 | `#999999` | `#98A2B3` | `ink-gray-5` — **icons + placeholders only** |
| 600 | `#7C7C7C` | `#667085` | `ink-gray-6` — labels, column headers |
| 700 | `#525252` | `#475467` | `ink-gray-7` — secondary text |
| 800 | `#383838` | — | `ink-gray-8` — **primary row text** |
| 900 | `#171717` | `#101828` | `ink-gray-9` — headings, figures |
| 950 | `#0F0F0F` | — | bulk bar, inverted surfaces |

**A11y floor:** `#7C7C7C` (4.76:1) is the lightest token allowed to carry text. `#999999` (2.85:1)
is icons and placeholders only — Frappe leads with ink-gray-5 because it uses it for chrome.
Canvas: `#F4F6FA` → **`#FFFFFF`**; `#F8F8F8` marks strips, not pages.
**Radii** `0/4/5/6/8/10/12/16/20/999`; on list surfaces the ceiling drops 16→**6**: buttons/inputs
`6`, kanban cards + modals `10`, pills `999`, **`.tblwrap` → `0`**, no border, no shadow.
**Spacing:** row block `8` · gutters `12`(<640)/`20` · control bar `16/20` · gap `8`. Retires the
22px gutter and 24px card padding.

## 3. Colour temperature — what stays Massar

**Kept, deliberately:** (1) **the sidebar untouched** — navy gradient, gold active state, teal
logo; 264px of permanent brand on every screen, because identity belongs in the chrome, not the
data. (2) **Teal `#1F7A73` as the single accent**, in exactly five places: the one primary button
per screen, focus rings, the selected-row `border-inline-start`, checkbox `accent-color`, the
progress fill. (3) **Status hues as 6px dots only** (`#027A48`/`#B54708`/`#B42318`/`#2F5F94`).
(4) **The dashed `.c-read` chip keeps its dash** — that encodes "assistant reading, not recorded
fact"; epistemics, not decoration.

**Removed from the canvas:** gold `#C9A227` (sidebar-only); every teal *fill* (`#DCF1EF`,
`#E9F7F6`, `#F6FCFB`, `#F0FAF9`) → `#F3F3F3`/white; teal text on filters, tabs, counts, links →
`#171717`/`#525252`. Teal may never fill an area larger than a chip.

## 4. List row spec (`#kmon`)

| property | value |
|---|---|
| structure | flush rows, `border-top 1px #EDEDED`; **no card wrapper**; first row no border |
| padding | block `8px`; inline `20px` (≥640) / `12px` (<640) |
| height | 20px line + 16px → **min-height 36px, 37px pitch** (was ~62px) |
| name | 14px / **450** / `#383838` / `truncate` |
| meta | date moves **inline** after the name, 12px `#7C7C7C`, `·` separator — two stacked lines cannot fit 36px, and that is the point |
| state | **dot + plain label**, 13px `#525252`; no fill, border or padding |
| figures | 14px / 500 / `#171717`; fixed grid tracks + `text-align`, not `tabular-nums` (unreliable on Arabic-Indic glyphs) |
| progress | 4px track `#EDEDED`, fill `#1F7A73`, radius 999 |
| icons | 16×16, `#999999`, hover `#525252`; button radius 6, ≥32px touch |
| hover | background `#F8F8F8`. No border change, shadow or transform |
| selected | `#F3F3F3` + `border-inline-start 3px #1F7A73` (keep — never regress to `box-shadow`) |
| focus | `outline: 2px #1F7A73; outline-offset: -2px` |
| header strip | 32px, `#F8F8F8`, 12px/500/`#7C7C7C`, border-bottom `#EDEDED` |

## 5. Control bar

A **strip, not a card**: `background #fff; border-bottom 1px #EDEDED; padding 16px 20px; gap 8px;
radius 0; box-shadow none; margin-bottom 0` — the list starts immediately beneath.
Controls **28px tall, 12–13px, radius 6**, `#fff` on `1px #EDEDED`, text `#525252`; on-state
`#F3F3F3` + `#C7C7C7` border + `#171717` text. The segmented toggle keeps its shape at radius 6
(not 999), white thumb on an `#F3F3F3` track. Search: 28px, placeholder `#999999`, focus 1px
`#1F7A73`, **no glow**. Count pill → plain 12px `#7C7C7C` text. The bar's only colour is the teal
«إنشاء حملة» button.

## 6. `#kmon`, before → after

**Before:** the page floats on a blue-grey field; a 13px-radius control card above a 16px-radius
table card; 62px rows carrying a 700-weight name, a stacked date line, a filled coloured chip,
three figures, a teal bar. Six or seven campaigns visible; every horizontal edge is a card edge.

**After:** the navy sidebar is unchanged and now the only branded surface. Flat white canvas to
the edges. One 60px strip of small neutral controls with a single teal button; a 32px column
header; then hairline-separated 37px rows running to the bottom of the viewport with **no frame at
all**. Fourteen to fifteen campaigns in the same height. One colour per row: the state dot. The
cue is structural — the frame is gone, the field is white, the type is a weight lighter, and twice
as much fits.

## 7. Must NOT change (correctness, not taste)

- **Arabic-Indic numerals** via `fmtN`; `check:numerals` stays green.
- **RTL logical properties only** — no `left`/`right`, no physical offsets.
- **Honest absence**: «لم تُرسل بعد» · «بلا جمهور» · «—»; `crmRate` keeps returning `null`.
- **No invented values** — denser rows must not get filled with placeholders.
- **ADR-0001**: anchored single-property replacements in `dashboard.ts`; never a range edit.

## 8. Migration order

1. **S1 — tokens.** `dashboard.ts` `<style>`: the 11 greys, body → `#FFFFFF`, font stack. Pure
   literal replacement; changes every screen's temperature in one commit. Most of the perceived
   shift, near-zero risk. Ship first.
2. **S2 — list chrome.** `CAMPAIGNS_CRM_CSS` `.crow`/`.thead-*` and `.trow`/`.thead`/`.tblwrap`:
   padding, min-height, separator, radius→0. **Risk:** the 939px media query and the legacy
   `.trow:not(.km)` 900px rule — re-verify 375 and 768.
3. **S3 — type ladder.** Sizes, weights, line-heights, `ls 0`; preload the font.
4. **S4 — chips and bar.** Dot+label, bar de-carded, teal stripped from filters. Highest taste
   risk, lowest structural risk — do it once he has seen the shift.

Each step gated by `npm run check` + `npm run smoke`.
**QA baseline (capture before S1):** `#kmon` and `#kmon/<id>` at **1440×900, 768×1024, 375×812**.
