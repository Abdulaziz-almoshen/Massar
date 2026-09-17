# مسار — قواعد دفتر المبيعات

## Organising rule

Give a recorded amount a number. Give missing data a named state. Give partial evidence a visible boundary. Never promote one product’s quarter into a company target.

The primary reading order is revenue → target scope → pricing and stagnation → operational records. Keep that order in the DOM and at both viewport sizes. Use ruled sections and tables; do not enclose every fact in a card.

## Tokens

| Token | Value | Rule |
| --- | --- | --- |
| Paper | `#f7f7f2` | Page, header, main content, dialog |
| Surface | `#ffffff` | Small neutral labels; reversed control text |
| Ink | `#252720` | Values, headings, selected navigation and filters |
| Muted | `#62655b` | Scope, supporting labels, unavailable detail |
| Rule | `#d3d5ca` | Row separators and ordinary boundaries |
| Soft | `#eeefe8` | Table heading and pointer hover |
| Shared field | `#f1f2ec` | Cells whose evidence applies to the entire set |
| Selected hover | `#3a3d33` | Hover on an already selected filter |
| Exception | `#a33224` | Missing price, missing target, missing owner; never branding |
| Exception wash | `#faeeea` | Background for those same statuses |
| Scrim | `#25272066` | Modal backdrop |
| Dividers | `1px`; major boundary `2px` | Separate rows; establish reading hierarchy |
| Radius | `0`; empty-list badge `2px` | Controls and surfaces remain square |
| Spacing | `4, 6, 8, 12, 16, 20, 24, 36, 64px` | Prefer these gaps; measured exceptions live in component rules below |
| Gutter | `clamp(20px, 4.45vw, 64px)` | `64px` at 1440; `20px` at 400 |
| Content limit | `1600px` including gutters | Centre using logical margins |
| Focus | `2px` ink outline, `4px` offset | Visible on keyboard focus; independent of status colour |
| Modal shadow | `0 12px 60px #0002` | Only an overlapping surface casts a shadow |

No gradients, decorative colour, avatars, ornamental icons, or data-surface shadows. The tiny outlined square identifies an exception; arrows identify actual navigation.

## Typography

Embed IBM Plex Sans Arabic in each HTML, weights 400/500/600/700. Body fallback is `sans-serif`. No runtime font request. Do not track Arabic letters; negative tracking is confined to numeric displays.

| Role | Desktop / 400px | Weight; line height | Reason |
| --- | --- | --- | --- |
| Revenue | `180 / 144px` | 500; `1.12 / 1.07` | The recorded zero outranks all navigation and other figures |
| Open-line count | `100 / 84px` | 500; `1.15` | Establish the entire ledger population before filtering |
| Recorded target | `49 / 39px` | 500; `1.35 / 1.4` | Legible secondary amount, visibly subordinate to revenue |
| Priced line, ledger header | `43 / 29px` | 500; `1.35` | Labelled as one line’s value, never pipeline total |
| Campaign counts / day range | `36 / 32px`, range `36 / 25px` | 500; `1.4` | Fast comparison of stored counts; readable shared range |
| Page heading | `29 / 26px` | 600; `1.5` | Name the ledger without overpowering its population |
| Section heading | `21 / 20px` | 600; `1.6` | Mark a new record family |
| Table value | `14 / 12px` | 400–500; `1.65` | Keep all four columns visible at 400px |
| Supporting labels | `12–14 / 11–13px` | 400; `1.65` | Carry scope next to the figure it qualifies |
| Shared-cell metadata | `12 / 10px` | 400; `1.8–1.9` | Explain unavailable detail without competing with values |

The mobile metadata size is a deliberate density compromise. Main data and status labels remain larger. Browser zoom is enabled.

## Layout and components

- **Shell:** 69px minimum brand row; 47px navigation row. At 400px these become 62px and 46px. Seven doors remain in one RTL navigation strip. Mobile overflow belongs to that strip, never to the page. Reports and settings are explicitly disabled because this entry implements neither screen. Other doors reach real sections or the ledger.
- **Revenue/target split:** two columns, `1.08fr 1fr`, separated by a 1px rule. At 560px and below, stack revenue before target. The target is always adjacent to `الإجازات المرضية`, `Q3`, and the one-product scope.
- **Coverage strip:** eight equal slots, filled from inline-start; exactly one filled. It encodes products with targets, not money or attainment. No percentage.
- **Exception strip:** two ruled cells for unpriced lines and stationary duration. Stack at 560px. Links reach the complete or unpriced ledger view.
- **Fact table:** full-width semantic table, labels at inline-start, values at inline-end. Rows carry product counts and distinct status text.
- **Operations column:** accounts and knowledge share a ruled column, not KPI cards. Knowledge’s bar uses the recorded score `34/100`; its separate section count remains `3 of 8`.
- **Campaign register:** equal-width cells ordered `21 → 19 → 12 → 4 → 2 → 0` in the DOM and visually from inline-start. At 400px, two rows of three, each read right to left. This is a list of counts, not a conversion funnel or forecast.
- **Ledger:** a semantic four-column table, widths `24% / 23% / 25% / 28%` for group, value, stage, stagnation. Six body rows in the complete view. Minimum row height 66px desktop, 72px mobile; content may increase it. Five separate unpriced value cells preserve the supplied population. Group labels do not impersonate record IDs.
- **Shared cells:** stage and stagnation span the visible rows. Their text explicitly describes the complete six-line population even after filtering. `3–24` is never allocated to individual records. An unavailable stage is not a stored empty stage.
- **Filters:** native buttons, 40px minimum desktop / 44px mobile, `aria-pressed`, instant table replacement, polite live count. The headline remains the fixed population of six. `?view=unpriced` opens the five-line view. No sort controls for unavailable row data.
- **State dictionary:** native modal dialog with six named states, 560px maximum width, 16px viewport clearance, 85dvh maximum height. Keyboard focus stays inside; Escape and the close button dismiss it and restore focus. No invented data appears when it opens.

## The six empties

| Text | Meaning | Non-colour distinction |
| --- | --- | --- |
| `لم يُسعَّر` | Opportunity line lacks a price | Dashed enclosing border |
| `لم يُصنَّف` | Classification not assigned | Neutral dashed enclosing border |
| `لا بنود مفتوحة` | Known empty open-line collection | Solid neutral enclosing border |
| `بلا مستهدف` | Target absent, not zero | 2px underline |
| `لم تُسجَّل` | Value not entered into a record | Dotted underline |
| `لا سعر منشور` | Product lacks a published price | Inline-start rule and status wash |

Use the three states supported by this dataset on actual data surfaces. Keep all six available through “معاني الحالات”. Do not manufacture unclassified products or an empty opportunity group merely to display a state. `غير متاحة` is a separate evidence qualifier: the brief did not supply that detail. It does not assert that production stores null.

## Data contract

| Supplied evidence | Rendering restriction |
| --- | --- |
| Won revenue `0 ر.س`, no closed deal ever | Label revenue from won deals. Do not relabel it as a separately verified cash-collection balance. |
| `34,000 ر.س`, الإجازات المرضية, Q3 | One product, one quarter. No monthly series, company total, attainment, remaining-to-target or required-to-date figure. |
| Eight products, seven without targets | Preserve null. The eight-slot strip measures coverage only. |
| One without published price; six publish a basis rather than a number | Keep these two facts separate; a basis is not a numerical quote. |
| Four inferred sectors; assistant will not sell one product | Do not infer which products, or classify the remaining four as empty. |
| Six lines; one priced at `4,200 ر.س`, five unpriced | Never label `4,200 ر.س` a complete pipeline total. Do not associate it with the named product. |
| All stationary for 3–24 days | Show the supplied population range; no health score, row-specific days, stage names, or chronological order. |
| Sixteen accounts; all approved, none assigned | Show 16 approved and 16 without an owner; invent no owner or account identity. |
| One campaign, الحملة 38; 21/19/12/4/2/0 | Preserve every count in the supplied order; no drop percentages. |
| Knowledge 34/100; three of eight sections complete | Score and completion are distinct observations. |

No currency arithmetic, probability model, attribution, additional dates, or synthetic identifiers. Both screens are static evidence views, not simulations of database writes.

## RTL and Arabic

Set `lang="ar" dir="rtl"` on the root. Use logical sizes, insets, margins, padding, borders, and start/end text alignment. Keep DOM order equal to RTL reading order. Every visible Western number lives inside `.m-n { direction:ltr; unicode-bidi:isolate; font-variant-numeric:tabular-nums; }`; put the entire currency or percentage inside the same span. Arabic words surrounding numbers retain RTL flow.

Inflect counts by context: `بند واحد`, `بندان`, `3–10 بنود`, `11+ بندًا`; zero uses `لا بنود مفتوحة`. The filter announcer implements these branches. Visible cases include `6 بنود`, `7 منتجات`, `16 حسابًا`, and `مهتمّان`. Do not build labels with a single invariant noun.

## Motion and input

Use exactly one curve: `cubic-bezier(.2,0,0,1)`. Dialog and backdrop enter by opacity in 180ms, exit by opacity in 120ms. Interactive controls transition press, colour and background in 100ms; `:active` uses `scale(.97)`. No entrance scale, page-load choreography, counter animation, delay, or duration above 300ms. Table filters update immediately.

Every hover selector is under `@media (hover:hover) and (pointer:fine)`. Under `prefers-reduced-motion:reduce`, remove animation, transitions and press transforms; dialog closes immediately. Use `touch-action:manipulation` on controls. Disable text selection only on controls. Keep text selectable and zoom available. The page remains a normal scrolling document.

## References and verification

All layout, spacing, size and colour values above are original implementation choices; none is claimed as a measurement of a reference application. The typeface is [IBM Plex Sans Arabic](https://github.com/IBM/plex), distributed through Google Fonts under the SIL Open Font License. The brief supplies the motion timings, active scale, RTL contract and dataset. The better-ui and mobile-native skills informed optical alignment, input and state checks; conflicting skill motion values were overridden by the brief.

Verified in local Chrome at 1440px and 400px: full-page screenshots, Arabic font loading from embedded bytes, no page overflow, six/five/one filter row counts, zero unwrapped visible numerals, no JavaScript errors, modal open/Escape/close and focus restoration, reduced-motion animation removal. Phone hardware behaviour is not verified. QA scripts and images remain outside the deliverable directory.
